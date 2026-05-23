from __future__ import annotations
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import pandas as pd

from app.converters import result_to_jsonable
from investment_lab.engine.portfolio_calculator import portfolio_metrics
from investment_lab.engine.scenario_comparator import analyze_scenarios
from investment_lab.domain.models import ScenarioAssumptions, UserConstraints

router = APIRouter()

class PortfolioCheckRequest(BaseModel):
    positions: list[dict]
    assumptions: dict = Field(default_factory=dict)
    constraints: dict = Field(default_factory=dict)

@router.post('/check')
def portfolio_check(req: PortfolioCheckRequest):
    rows = req.positions
    if not rows:
        raise HTTPException(status_code=422, detail='Добавьте хотя бы одну позицию портфеля')
    required_fields = {"name", "asset_class", "market_value"}
    for idx, row in enumerate(rows):
        if not required_fields.issubset(row.keys()):
            raise HTTPException(status_code=422, detail=f'Позиция #{idx + 1} заполнена неполно')
        if not str(row.get("name", "")).strip():
            raise HTTPException(status_code=422, detail=f'Позиция #{idx + 1}: название не заполнено')
        if not str(row.get("asset_class", "")).strip():
            raise HTTPException(status_code=422, detail=f'Позиция #{idx + 1}: класс актива не заполнен')
        try:
            market_value = float(row.get("market_value"))
        except (TypeError, ValueError):
            raise HTTPException(status_code=422, detail=f'Позиция #{idx + 1}: market_value должен быть числом')
        if market_value <= 0:
            raise HTTPException(status_code=422, detail=f'Позиция #{idx + 1}: market_value должен быть больше 0')
    metrics = portfolio_metrics(rows)
    df = pd.DataFrame(rows)
    scenario = analyze_scenarios(df, ScenarioAssumptions(**req.assumptions), UserConstraints(**req.constraints)) if not df.empty else {}
    sj = result_to_jsonable(scenario)
    summary = (sj.get('summary') or [{}])[0] if sj.get('summary') else {}
    weak_points: list[str] = []
    top1 = float(metrics.get('concentration_top1', 0.0) or 0.0)
    weighted_vol = float(metrics.get('weighted_average_volatility', metrics.get('weighted_volatility', 0.0)) or 0.0)
    max_single = float(req.constraints.get('max_single_position_pct', 100) or 100)
    max_vol = float(req.constraints.get('max_portfolio_volatility_pct', 200) or 200)
    if top1 > max_single:
        weak_points.append(f"Концентрация top-1 выше лимита: {top1:.1f}% > {max_single:.1f}%")
    if weighted_vol > max_vol:
        weak_points.append(f"Взвешенная волатильность выше лимита: {weighted_vol:.1f}% > {max_vol:.1f}%")
    if not weak_points:
        weak_points.append("Критичные замечания по заданным ограничениям не выявлены.")
    return {
        'allocation_by_asset_class': sj.get('asset_allocation', []),
        'concentration': {'top1_pct': metrics.get('concentration_top1', 0.0), 'top2_pct': metrics.get('concentration_top2', 0.0)},
        'liquidity_30d': summary.get('liquid_within_30d_pct', 0.0),
        'liquidity_label': summary.get('liquidity_label', None),
        'expected_return': metrics.get('weighted_return', 0.0),
        'fees_annual_pct': metrics.get('weighted_fee', 0.0),
        'stress_drawdown': summary.get('worst_stress_impact_pct', 0.0),
        'risk_flags': sj.get('flags', []),
        'weak_points': weak_points,
        'cashflows': [],
        'summary': summary,
        'limitations': sj.get('limitations', ['Оценка основана на пользовательском вводе.'])
    }

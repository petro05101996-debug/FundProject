from __future__ import annotations
from fastapi import APIRouter
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
    metrics = portfolio_metrics(rows)
    df = pd.DataFrame(rows)
    scenario = analyze_scenarios(df, ScenarioAssumptions(**req.assumptions), UserConstraints(**req.constraints)) if not df.empty else {}
    sj = result_to_jsonable(scenario)
    summary = (sj.get('summary') or [{}])[0] if sj.get('summary') else {}
    return {
        'allocation_by_asset_class': sj.get('asset_allocation', []),
        'concentration': {'top1_pct': metrics.get('concentration_top1', 0.0), 'top2_pct': metrics.get('concentration_top2', 0.0)},
        'liquidity_30d': summary.get('liquid_within_30d_pct', 0.0),
        'expected_return': metrics.get('weighted_return', 0.0),
        'stress_drawdown': summary.get('worst_stress_impact_pct', 0.0),
        'risk_flags': sj.get('flags', []),
        'weak_points': [f"Концентрация top-1: {metrics.get('concentration_top1',0):.1f}%", f"Средняя волатильность: {metrics.get('weighted_volatility',0):.1f}%"],
        'cashflows': [],
        'summary': summary,
        'limitations': sj.get('limitations', ['Оценка основана на пользовательском вводе.'])
    }

from __future__ import annotations
from dataclasses import asdict
from fastapi import APIRouter
from pydantic import BaseModel, Field
from investment_lab.domain.models import ScenarioAssumptions, UserConstraints
from investment_lab.engine.scenario_comparator import analyze_scenarios
from app.converters import records_to_dataframe, result_to_jsonable
from app.schemas import ScenarioAnalyzeRequest
from investment_lab.domain.models import normalize_asset_class

router = APIRouter()

@router.post('/analyze')
def analyze(req: ScenarioAnalyzeRequest):
    df = records_to_dataframe([item.model_dump() for item in req.positions])
    assumptions = ScenarioAssumptions(**req.assumptions.model_dump())
    constraints = UserConstraints(**req.constraints.model_dump())
    result = analyze_scenarios(df, assumptions=assumptions, constraints=constraints)
    payload = result_to_jsonable(result)
    for row in payload.get("summary", []):
        if row.get("worst_stress_value") is None and row.get("portfolio_value") is not None and row.get("worst_stress_impact_pct") is not None:
            row["worst_stress_value"] = float(row["portfolio_value"]) * float(row["worst_stress_impact_pct"]) / 100
        # Backward compatibility only. New UI must use projected_value.
        if row.get("expected_final_value") is None and row.get("projected_value") is not None:
            row["expected_final_value"] = row.get("projected_value")
    payload['assumptions'] = asdict(assumptions.normalized())
    payload['constraints'] = asdict(constraints.normalized())
    return payload

class WhatIfPayload(BaseModel):
    rate_delta_pct: float = 0
    equity_market_shock_pct: float = 0
    inflation_pct: float = 0
    early_exit: bool = False
    deposit_share_pct: float = 0
    ofz_share_pct: float = 0
    fund_share_pct: float = 0
    equity_share_pct: float = 0

class WhatIfRequest(BaseModel):
    base_request: ScenarioAnalyzeRequest
    what_if: WhatIfPayload = Field(default_factory=WhatIfPayload)


def _target_share_for_class(asset_class: str, wf: WhatIfPayload) -> float | None:
    if asset_class == 'Денежные средства':
        return wf.deposit_share_pct + wf.fund_share_pct
    if asset_class == 'Облигации':
        return wf.ofz_share_pct
    if asset_class == 'Акции':
        return wf.equity_share_pct
    return None


@router.post('/what-if')
def what_if(req: WhatIfRequest):
    base = analyze(req.base_request)
    positions = [p.model_dump() for p in req.base_request.positions]

    # Apply simple class-level share reweighting when user provided any target shares.
    has_share_inputs = any(v > 0 for v in [req.what_if.deposit_share_pct, req.what_if.ofz_share_pct, req.what_if.fund_share_pct, req.what_if.equity_share_pct])
    if has_share_inputs:
        total_value = sum(float(p.get('market_value', 0)) for p in positions) or 1.0
        grouped: dict[str, list[dict]] = {}
        for p in positions:
            grouped.setdefault(normalize_asset_class(p.get('asset_class', 'Другое')), []).append(p)
        for ac, rows in grouped.items():
            target = _target_share_for_class(ac, req.what_if)
            if target is None:
                continue
            class_target_value = total_value * max(0.0, target) / 100.0
            class_current_value = sum(float(r.get('market_value', 0)) for r in rows) or 1.0
            scale = class_target_value / class_current_value
            for r in rows:
                r['market_value'] = max(0.0, float(r.get('market_value', 0)) * scale)

    for p in positions:
        ac = normalize_asset_class(p.get('asset_class', ''))
        if 'Акции' in ac:
            p['expected_return_pct'] = float(p.get('expected_return_pct', 0)) + req.what_if.equity_market_shock_pct
            p['volatility_pct'] = float(p.get('volatility_pct', 0)) + abs(req.what_if.equity_market_shock_pct) / 2
        p['expected_return_pct'] = float(p.get('expected_return_pct', 0)) + req.what_if.rate_delta_pct * 0.2
        if req.what_if.early_exit:
            p['liquidity_days'] = float(p.get('liquidity_days', 0)) + 15

    assumptions = dict(req.base_request.assumptions.model_dump())
    assumptions['inflation_pct'] = req.what_if.inflation_pct
    wf_request = ScenarioAnalyzeRequest(
        assumptions=assumptions,
        constraints=req.base_request.constraints.model_dump(),
        positions=positions,
    )
    wf = analyze(wf_request)
    b = (base.get('summary') or [{}])[0]
    w = (wf.get('summary') or [{}])[0]
    return {
        'base_summary': b,
        'what_if_summary': w,
        'deltas': {
            'projected_value_delta': float(w.get('projected_value', 0)) - float(b.get('projected_value', 0)),
            'stress_delta': float(w.get('worst_stress_impact_pct', 0)) - float(b.get('worst_stress_impact_pct', 0)),
            'liquidity_delta': float(w.get('liquid_within_30d_pct', 0)) - float(b.get('liquid_within_30d_pct', 0)),
        },
        'risk_flags': wf.get('flags', []),
        'stress': wf.get('stress', []),
        'liquidity': w.get('liquid_within_30d_pct', 0),
        'limitations': ['Технический what-if использует упрощённое перераспределение пользовательских позиций и не является прогнозом рынка.'],
        'methodology': {
            'type': 'simplified_sensitivity_model',
            'description': 'Расчёт показывает чувствительность пользовательского сценария к изменению допущений. Это не прогноз рынка и не инвестиционная рекомендация.',
            'limitations': [
                'Не используются реальные рыночные котировки',
                'Не моделируется полная кривая ставок',
                'Корреляции и стресс-параметры являются упрощёнными',
                'Результат зависит от пользовательских вводных',
            ],
        },
    }

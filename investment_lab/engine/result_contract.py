from __future__ import annotations
import pandas as pd
SUMMARY_FIELDS=["scenario","portfolio_value","expected_return_pct","net_return_pct","real_return_pct","projected_value","projected_profit","projected_profit_pct","volatility_pct","liquid_within_30d_pct","fee_and_commission_drag_pct","tax_drag_pct","max_position_pct","max_asset_class_pct","worst_stress_impact_pct","worst_stress_value","constraint_fit_score","status","instrument_count","risk_score","risk_label","liquidity_score","liquidity_label","complexity_score","complexity_label","risk_explanation","data_quality_score","data_quality_label","data_quality_notes"]
POSITION_FIELDS=["scenario","instrument","ticker","asset_class","country","currency","market_value","weight_pct","expected_return_pct","annual_fee_pct","tax_pct","tax_drag_pct","commission_drag_pct","net_return_pct","real_return_pct","volatility_pct","liquidity_days","liquid_within_30d","liquidity_score","liquidity_label","complexity_score","complexity_label","risk_score","risk_label","risk_drivers"]
ASSET_ALLOCATION_FIELDS=["scenario","asset_class","market_value","weight_pct","avg_net_return_pct"]
STRESS_FIELDS=["scenario","stress_case","portfolio_impact_pct","estimated_value_after_stress_pct","estimated_value_after_stress","stress_loss_value","max_drawdown_pct","liquidity_degradation_level"]
FLAG_FIELDS=["scenario","code","severity","title","message","actual","limit"]

def ensure_columns(df: pd.DataFrame, required_fields: list[str]) -> pd.DataFrame:
    out=df.copy() if df is not None else pd.DataFrame()
    for f in required_fields:
        if f not in out.columns: out[f]=None
    return out

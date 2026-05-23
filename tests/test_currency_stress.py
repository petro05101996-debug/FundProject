import pandas as pd
from investment_lab.domain.models import ScenarioAssumptions, UserConstraints
from investment_lab.engine.scenario_comparator import analyze_scenarios


def _impact(df):
    r=analyze_scenarios(df, ScenarioAssumptions(fx_devaluation_pct=20), UserConstraints())
    return float(r["stress"].iloc[0]["portfolio_impact_pct"])


def test_fx_devaluation_uses_real_non_base_currency_weight():
    rub = pd.DataFrame([{"scenario":"S","instrument":"R","ticker":"R","asset_class":"Акции","country":"RU","currency":"RUB","market_value":100,"expected_return_pct":10,"volatility_pct":10,"liquidity_days":1,"annual_fee_pct":0,"tax_pct":13}])
    half = pd.DataFrame([
      {"scenario":"S","instrument":"R","ticker":"R","asset_class":"Акции","country":"RU","currency":"RUB","market_value":50,"expected_return_pct":10,"volatility_pct":10,"liquidity_days":1,"annual_fee_pct":0,"tax_pct":13},
      {"scenario":"S","instrument":"U","ticker":"U","asset_class":"Акции","country":"US","currency":"USD","market_value":50,"expected_return_pct":10,"volatility_pct":10,"liquidity_days":1,"annual_fee_pct":0,"tax_pct":13},
    ])
    assert _impact(half) - _impact(rub) == 10.0

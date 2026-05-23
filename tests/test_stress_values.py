import pandas as pd
from investment_lab.domain.models import ScenarioAssumptions, UserConstraints
from investment_lab.engine.scenario_comparator import analyze_scenarios


def test_worst_stress_value_formula():
    df = pd.DataFrame([{"scenario":"S1","instrument":"A","ticker":"A","asset_class":"Акции","country":"RU","currency":"RUB","market_value":200000,"expected_return_pct":10,"volatility_pct":20,"liquidity_days":2,"annual_fee_pct":0.5,"tax_pct":13}])
    r=analyze_scenarios(df, ScenarioAssumptions(), UserConstraints())
    row=r["summary"].iloc[0]
    assert round(row["worst_stress_value"],6)==round(row["portfolio_value"]*row["worst_stress_impact_pct"]/100,6)

import pandas as pd
from investment_lab.domain.models import ScenarioAssumptions, UserConstraints
from investment_lab.engine.result_contract import SUMMARY_FIELDS, POSITION_FIELDS, ASSET_ALLOCATION_FIELDS, STRESS_FIELDS, FLAG_FIELDS
from investment_lab.engine.scenario_comparator import analyze_scenarios


def test_analyze_scenarios_returns_required_contract_fields():
    df = pd.DataFrame([{"scenario":"S1","instrument":"Вклад","ticker":"D","asset_class":"Денежные средства","country":"RU","currency":"RUB","market_value":100000,"expected_return_pct":8,"volatility_pct":1,"liquidity_days":1,"annual_fee_pct":0,"tax_pct":13}])
    result = analyze_scenarios(df, ScenarioAssumptions(), UserConstraints())
    assert set(SUMMARY_FIELDS).issubset(result["summary"].columns)
    assert set(POSITION_FIELDS).issubset(result["positions"].columns)
    assert set(ASSET_ALLOCATION_FIELDS).issubset(result["asset_allocation"].columns)
    assert set(STRESS_FIELDS).issubset(result["stress"].columns)
    assert set(FLAG_FIELDS).issubset(result["flags"].columns)
    assert "methodology" in result

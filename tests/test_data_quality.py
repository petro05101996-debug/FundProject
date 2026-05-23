import pandas as pd
from investment_lab.domain.models import ScenarioAssumptions, UserConstraints
from investment_lab.engine.scenario_comparator import analyze_scenarios


def test_data_quality_drops_for_unknown_asset_and_defaults():
    df = pd.DataFrame([
        {"scenario":"S1","instrument":"X","ticker":"X","asset_class":"Нечто","country":"RU","currency":"","market_value":100000,"expected_return_pct":10,"volatility_pct":0,"liquidity_days":365,"annual_fee_pct":0.2,"tax_pct":13}
    ])
    r = analyze_scenarios(df, ScenarioAssumptions(), UserConstraints())
    row = r["summary"].iloc[0]
    assert float(row["data_quality_score"]) < 100
    assert row["data_quality_label"] in {"Высокая", "Средняя", "Низкая"}
    assert row["data_quality_notes"]

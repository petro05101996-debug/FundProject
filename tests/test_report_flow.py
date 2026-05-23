import pandas as pd
from investment_lab.domain.models import ScenarioAssumptions, UserConstraints
from investment_lab.engine.scenario_comparator import analyze_scenarios
from investment_lab.engine.report_builder import export_html_report


def test_report_flow_works_with_dataframe_and_records():
    df = pd.DataFrame([{"scenario":"S1","instrument":"D","ticker":"D","asset_class":"Денежные средства","country":"RU","currency":"RUB","market_value":100000,"expected_return_pct":8,"volatility_pct":1,"liquidity_days":1,"annual_fee_pct":0,"tax_pct":13}])
    result = analyze_scenarios(df, ScenarioAssumptions(), UserConstraints())
    html = export_html_report(result)
    assert "Investment Scenario Lab" in html
    result["summary"] = result["summary"].to_dict("records")
    result["positions"] = result["positions"].to_dict("records")
    result["stress"] = result["stress"].to_dict("records")
    result["flags"] = result["flags"].to_dict("records")
    html2 = export_html_report(result)
    assert "Executive summary" in html2

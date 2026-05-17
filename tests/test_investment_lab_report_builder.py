import pytest

pd = pytest.importorskip("pandas")

from investment_lab.engine.report_builder import build_cashflow_table, export_html_report
from investment_lab.engine.scenario_comparator import analyze_scenarios
from investment_lab.domain.models import default_instruments


def test_report_builder_exports_html_and_cashflows():
    result = analyze_scenarios(pd.DataFrame(default_instruments()))
    cashflows = build_cashflow_table(result["summary"], 3)
    html = export_html_report(result)
    assert "Дисклеймер" in html
    assert "Риск-флаги" in html
    assert not cashflows.empty

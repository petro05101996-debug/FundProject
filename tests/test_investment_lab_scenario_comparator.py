import pytest

pd = pytest.importorskip("pandas")

from investment_lab.engine.scenario_comparator import analyze_scenarios
from investment_lab.domain.models import default_instruments


def test_scenario_comparator_returns_structured_flags_and_scores():
    result = analyze_scenarios(pd.DataFrame(default_instruments()))
    assert {"code", "title", "description", "severity", "metric", "limit"}.issubset(result["flags"].columns)
    assert {"risk_score", "liquidity_score", "complexity_score"}.issubset(result["summary"].columns)

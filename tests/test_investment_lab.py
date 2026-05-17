import pytest

pd = pytest.importorskip("pandas")

from investment_lab.analytics import analyze_scenarios
from investment_lab.models import ScenarioAssumptions, UserConstraints, default_instruments


def test_analyze_scenarios_returns_ranked_summary_and_flags():
    df = pd.DataFrame(default_instruments())
    result = analyze_scenarios(df, ScenarioAssumptions(horizon_years=3, inflation_pct=3.0, default_tax_pct=10.0), UserConstraints(max_single_position_pct=60.0, max_asset_class_pct=80.0))
    assert result["leading_constraint_match_scenario"] in set(df["scenario"])
    assert set(result["summary"]["scenario"]) == set(df["scenario"])
    assert "constraint_fit_score" in result["summary"].columns
    assert "risk_score" in result["summary"].columns
    assert "liquidity_score" in result["summary"].columns
    assert "complexity_score" in result["summary"].columns
    assert not result["stress"].empty
    assert not result["flags"].empty


def test_concentration_flag_uses_user_limits():
    df = pd.DataFrame([
        {"scenario": "Concentrated", "instrument": "One large position", "ticker": "ONE", "asset_class": "Акции", "country": "Пользовательский ввод", "currency": "RUB", "market_value": 100000, "expected_return_pct": 7, "volatility_pct": 20, "liquidity_days": 2, "annual_fee_pct": 0.2, "tax_pct": 10}
    ])
    result = analyze_scenarios(df, constraints=UserConstraints(max_single_position_pct=25.0))
    assert "single_position_concentration" in set(result["flags"]["code"])


def test_empty_or_zero_values_return_validation_error_code():
    df = pd.DataFrame(default_instruments())
    df["market_value"] = 0
    result = analyze_scenarios(df)
    assert result["summary"].empty
    assert "zero_market_values" in set(result["flags"]["code"])

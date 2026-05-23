import pandas as pd
from investment_lab.domain.models import ScenarioAssumptions, UserConstraints
from investment_lab.engine.scenario_comparator import analyze_scenarios
from app.converters import records_to_dataframe


def _base_row(asset_class: str):
    return {
        "scenario": "S1",
        "instrument": "X",
        "ticker": "X",
        "asset_class": asset_class,
        "country": "RU",
        "currency": "RUB",
        "market_value": 100000,
        "expected_return_pct": 10,
        "volatility_pct": 10,
        "liquidity_days": 5,
        "annual_fee_pct": 0.2,
        "tax_pct": 13,
    }


def test_records_to_dataframe_preserves_raw_asset_class():
    df = records_to_dataframe([_base_row("Непонятный актив")])
    assert "raw_asset_class" in df.columns
    assert str(df.loc[0, "raw_asset_class"]) == "Непонятный актив"


def test_data_quality_penalizes_unknown_asset_class_but_not_canonical_alternative():
    assumptions = ScenarioAssumptions()
    constraints = UserConstraints()

    unknown_df = records_to_dataframe([_base_row("Непонятный актив")])
    alt_df = records_to_dataframe([_base_row("Альтернативные")])

    unknown = analyze_scenarios(unknown_df, assumptions, constraints)["summary"].iloc[0]
    alternative = analyze_scenarios(alt_df, assumptions, constraints)["summary"].iloc[0]

    assert float(unknown["data_quality_score"]) < float(alternative["data_quality_score"])
    assert "нераспозн" in str(unknown["data_quality_notes"]).lower() or "не распозн" in str(unknown["data_quality_notes"]).lower()


def test_known_aliases_to_alternative_are_not_unknown():
    assumptions = ScenarioAssumptions()
    constraints = UserConstraints()
    etf_df = records_to_dataframe([_base_row("ETF")])
    pif_df = records_to_dataframe([_base_row("ПИФ")])
    unknown_df = records_to_dataframe([_base_row("Супер-фонд")])

    etf_positions = analyze_scenarios(etf_df, assumptions, constraints)["positions"]
    pif_positions = analyze_scenarios(pif_df, assumptions, constraints)["positions"]
    unknown_positions = analyze_scenarios(unknown_df, assumptions, constraints)["positions"]

    assert bool(etf_positions.iloc[0]["asset_class_was_unknown"]) is False
    assert bool(pif_positions.iloc[0]["asset_class_was_unknown"]) is False
    assert bool(unknown_positions.iloc[0]["asset_class_was_unknown"]) is True

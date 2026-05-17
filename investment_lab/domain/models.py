"""Domain models for Investment Scenario Lab.

The lab intentionally works only with user-provided assumptions. It does not
fetch market data, place orders, or produce individual investment advice.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

SUPPORTED_ASSET_CLASSES = (
    "Акции",
    "Облигации",
    "Денежные средства",
    "Товары",
    "Недвижимость",
    "Альтернативные",
)

LEGACY_ASSET_CLASS_MAP = {
    "equity": "Акции",
    "bond": "Облигации",
    "cash": "Денежные средства",
    "commodity": "Товары",
    "real estate": "Недвижимость",
    "alternative": "Альтернативные",
}

SAFE_STATUS_LABELS = {
    "fits_constraints": "Лучше соответствует заданным ограничениям",
    "acceptable_with_flags": "Допустимо с риск-флагами",
    "has_flags": "Есть риск-флаги",
    "does_not_fit": "Не соответствует ограничениям",
    "insufficient_data": "Недостаточно данных",
}


@dataclass(frozen=True)
class UserConstraints:
    """User-defined scenario constraints used for comparison scoring."""

    max_single_position_pct: float = 25.0
    max_asset_class_pct: float = 70.0
    min_liquidity_pct_30d: float = 80.0
    max_portfolio_volatility_pct: float = 20.0
    max_fee_drag_pct: float = 1.5
    max_stress_loss_pct: float = 25.0

    def normalized(self) -> "UserConstraints":
        return UserConstraints(
            max_single_position_pct=_clamp(self.max_single_position_pct, 1.0, 100.0),
            max_asset_class_pct=_clamp(self.max_asset_class_pct, 1.0, 100.0),
            min_liquidity_pct_30d=_clamp(self.min_liquidity_pct_30d, 0.0, 100.0),
            max_portfolio_volatility_pct=_clamp(self.max_portfolio_volatility_pct, 0.0, 200.0),
            max_fee_drag_pct=_clamp(self.max_fee_drag_pct, 0.0, 100.0),
            max_stress_loss_pct=_clamp(self.max_stress_loss_pct, 0.0, 100.0),
        )


@dataclass(frozen=True)
class ScenarioAssumptions:
    """Global assumptions supplied by the user for a scenario run."""

    horizon_years: int = 5
    inflation_pct: float = 4.0
    default_tax_pct: float = 13.0
    transaction_commission_pct: float = 0.1
    rebalance_events_per_year: int = 1
    fx_devaluation_pct: float = 0.0

    def normalized(self) -> "ScenarioAssumptions":
        return ScenarioAssumptions(
            horizon_years=int(_clamp(self.horizon_years, 1, 50)),
            inflation_pct=_clamp(self.inflation_pct, -50.0, 200.0),
            default_tax_pct=_clamp(self.default_tax_pct, 0.0, 100.0),
            transaction_commission_pct=_clamp(self.transaction_commission_pct, 0.0, 100.0),
            rebalance_events_per_year=int(_clamp(self.rebalance_events_per_year, 0, 52)),
            fx_devaluation_pct=_clamp(self.fx_devaluation_pct, -100.0, 500.0),
        )


def required_instrument_columns() -> list[str]:
    return [
        "scenario",
        "instrument",
        "ticker",
        "asset_class",
        "country",
        "currency",
        "market_value",
        "expected_return_pct",
        "volatility_pct",
        "liquidity_days",
        "annual_fee_pct",
        "tax_pct",
    ]


def default_instruments() -> list[dict[str, object]]:
    """Default first-run data aligned with the provided scenario-builder mockup."""

    rows: list[dict[str, object]] = []
    scenario_specs = [
        (
            "Сценарий А",
            [
                ("Вклад", "CASH_A", "Денежные средства", 4_000_000.0, 7.0, 0.5, 1, 0.0),
                ("Фонд денежного рынка", "MMF_A", "Денежные средства", 2_500_000.0, 6.3, 2.0, 2, 0.3),
                ("ОФЗ", "OFZ_A", "Облигации", 2_000_000.0, 8.2, 6.0, 3, 0.1),
                ("Корпоративная облигация", "CORP_A", "Облигации", 1_500_000.0, 10.5, 10.0, 15, 0.2),
            ],
        ),
        (
            "Сценарий Б",
            [
                ("Фонд денежного рынка", "MMF_B", "Денежные средства", 3_000_000.0, 6.2, 2.0, 2, 0.3),
                ("ОФЗ", "OFZ_B", "Облигации", 3_000_000.0, 8.1, 6.0, 3, 0.1),
                ("Корпоративная облигация", "CORP_B", "Облигации", 2_500_000.0, 10.7, 10.0, 15, 0.2),
                ("Вклад", "CASH_B", "Денежные средства", 1_500_000.0, 7.0, 0.5, 1, 0.0),
            ],
        ),
        (
            "Сценарий В",
            [
                ("ОФЗ", "OFZ_C", "Облигации", 2_500_000.0, 8.2, 6.0, 3, 0.1),
                ("Корпоративная облигация", "CORP_C", "Облигации", 2_500_000.0, 10.7, 10.0, 15, 0.2),
                ("Фонд денежного рынка", "MMF_C", "Денежные средства", 2_500_000.0, 6.2, 2.0, 2, 0.3),
                ("Вклад", "CASH_C", "Денежные средства", 2_500_000.0, 7.0, 0.5, 1, 0.0),
            ],
        ),
    ]
    for scenario, instruments in scenario_specs:
        for instrument, ticker, asset_class, value, expected, volatility, liquidity, fee in instruments:
            rows.append(
                {
                    "scenario": scenario,
                    "instrument": instrument,
                    "ticker": ticker,
                    "asset_class": asset_class,
                    "country": "Пользовательский ввод",
                    "currency": "RUB",
                    "market_value": value,
                    "expected_return_pct": expected,
                    "volatility_pct": volatility,
                    "liquidity_days": liquidity,
                    "annual_fee_pct": fee,
                    "tax_pct": 13.0,
                }
            )
    return rows


def default_portfolio() -> list[dict[str, object]]:
    """Default portfolio positions transcribed from the portfolio mockup."""

    from investment_lab.data.mockup_metrics import MOCKUP_PORTFOLIO

    return [{"scenario": "Текущий портфель", "country": "Пользовательский ввод", "currency": "RUB", **row} for row in MOCKUP_PORTFOLIO]


def normalize_asset_class(value: object) -> str:
    text = str(value or "").strip()
    lowered = text.lower()
    if lowered in LEGACY_ASSET_CLASS_MAP:
        return LEGACY_ASSET_CLASS_MAP[lowered]
    for option in SUPPORTED_ASSET_CLASSES:
        if lowered == option.lower():
            return option
    return "Альтернативные"


def missing_columns(columns: Iterable[str]) -> list[str]:
    present = set(columns)
    return [column for column in required_instrument_columns() if column not in present]


def status_for_score(score: float | None, flags_count: int) -> str:
    """Return a safe non-advisory user status."""

    if score is None:
        return SAFE_STATUS_LABELS["insufficient_data"]
    if score >= 90 and flags_count == 0:
        return SAFE_STATUS_LABELS["fits_constraints"]
    if score >= 75:
        return SAFE_STATUS_LABELS["acceptable_with_flags"]
    if score >= 45:
        return SAFE_STATUS_LABELS["has_flags"]
    return SAFE_STATUS_LABELS["does_not_fit"]


def _clamp(value: float, minimum: float, maximum: float) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        number = minimum
    return max(minimum, min(maximum, number))

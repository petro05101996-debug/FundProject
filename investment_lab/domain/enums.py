"""Enums and constants for Investment Scenario Lab."""
from __future__ import annotations

from enum import Enum


class Severity(str, Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    INFO = "Info"
    ERROR = "Error"


class RiskFlagCode(str, Enum):
    SINGLE_POSITION_CONCENTRATION = "single_position_concentration"
    ASSET_CLASS_CONCENTRATION = "asset_class_concentration"
    LOW_LIQUIDITY = "low_liquidity"
    STRESS_LOSS_EXCEEDS_LIMIT = "stress_loss_exceeds_limit"
    HIGH_VOLATILITY = "high_volatility"
    FEE_DRAG_EXCEEDS_LIMIT = "fee_drag_exceeds_limit"
    TAX_ASSUMPTION_SENSITIVE = "tax_assumption_sensitive"
    CURRENCY_RISK = "currency_risk"
    SHORT_HORIZON_MISMATCH = "short_horizon_mismatch"
    INSTRUMENT_COMPLEXITY = "instrument_complexity"
    INSUFFICIENT_DATA = "insufficient_data"
    ZERO_MARKET_VALUES = "zero_market_values"
    NO_CONSTRAINT_BREACHES = "no_constraint_breaches"


class InstrumentKind(str, Enum):
    DEPOSIT = "Вклад"
    SAVINGS = "Накопительный счёт"
    OFZ = "ОФЗ"
    CORPORATE_BOND = "Корпоративная облигация"
    MONEY_MARKET_FUND = "Фонд денежного рынка"
    INDEX_FUND = "Индексный фонд"
    EQUITY_CLASS = "Акции как класс"


SAFE_STATUS_ORDER = [
    "Лучше соответствует заданным ограничениям",
    "Допустимо с риск-флагами",
    "Есть риск-флаги",
    "Не соответствует ограничениям",
    "Недостаточно данных",
]

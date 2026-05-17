"""Validation helpers for user-entered scenario data."""
from __future__ import annotations

from dataclasses import dataclass

from investment_lab.domain.enums import RiskFlagCode, Severity


@dataclass(frozen=True)
class ValidationIssue:
    code: str
    severity: str
    message: str


def validate_positive_market_values(rows: list[dict]) -> list[ValidationIssue]:
    if not rows:
        return [ValidationIssue(RiskFlagCode.INSUFFICIENT_DATA.value, Severity.ERROR.value, "Добавьте хотя бы один инструмент для расчёта.")]
    if all(float(row.get("market_value", 0) or 0) <= 0 for row in rows):
        return [ValidationIssue(RiskFlagCode.ZERO_MARKET_VALUES.value, Severity.ERROR.value, "Все рыночные стоимости равны нулю; введите положительные значения.")]
    return []

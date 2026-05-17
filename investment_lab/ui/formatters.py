"""Readable formatting and table labels for Investment Scenario Lab UI."""
from __future__ import annotations

COLUMN_LABELS = {
    "scenario": "Сценарий",
    "instrument": "Инструмент",
    "ticker": "Тикер/код",
    "asset_class": "Класс",
    "country": "Страна/рынок",
    "currency": "Валюта",
    "market_value": "Сумма",
    "expected_return_pct": "Ожидаемая доходность, %",
    "net_return_pct": "Доходность после комиссий и налогов, %",
    "real_return_pct": "Реальная доходность, %",
    "projected_value": "Расчётная стоимость",
    "volatility_pct": "Волатильность, %",
    "liquidity_days": "Ликвидность, дней",
    "annual_fee_pct": "Комиссия, %",
    "tax_pct": "Налог, %",
    "constraint_fit_score": "Соответствие ограничениям",
    "status": "Статус",
    "severity": "Уровень",
    "code": "Код флага",
    "title": "Флаг",
    "description": "Описание",
    "metric": "Метрика",
    "limit": "Лимит",
    "stress_case": "Стресс-сценарий",
    "portfolio_impact_pct": "Влияние на портфель, %",
    "estimated_value_after_stress_pct": "Стоимость после стресса, %",
    "risk_score": "Риск",
    "risk_label": "Уровень риска",
    "liquidity_score": "Ликвидность",
    "liquidity_label": "Оценка ликвидности",
    "complexity_score": "Сложность",
    "complexity_label": "Оценка сложности",
}


def format_money(value: float, currency: str = "₽") -> str:
    return f"{float(value):,.0f}".replace(",", " ") + f" {currency}"


def format_pct(value: float) -> str:
    return f"{float(value):.1f}%".replace(".", ",")


def format_days(value: float) -> str:
    days = int(round(float(value)))
    suffix = "день" if days % 10 == 1 and days % 100 != 11 else "дня" if days % 10 in {2, 3, 4} and days % 100 not in {12, 13, 14} else "дней"
    return f"{days} {suffix}"


def format_score(value: float) -> str:
    return f"{float(value):.0f} / 100"


def format_status(status: str) -> str:
    return str(status)


def readable_table(df):
    if df is None or not hasattr(df, "rename"):
        return df
    return df.rename(columns={key: value for key, value in COLUMN_LABELS.items() if key in df.columns})

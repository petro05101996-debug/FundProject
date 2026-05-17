"""Risk, liquidity, and complexity scoring helpers."""
from __future__ import annotations


def label_from_score(score: float, low: str, medium: str, high: str) -> str:
    if score <= 2:
        return low
    if score <= 3.5:
        return medium
    return high


def liquidity_score(liquidity_days: float, asset_class: str = "") -> tuple[int, str, str]:
    days = max(0.0, float(liquidity_days))
    if days <= 3:
        score = 5
    elif days <= 30:
        score = 4
    elif days <= 90:
        score = 3
    else:
        score = 1
    label = "Высокая" if score >= 4 else "Средняя" if score >= 3 else "Низкая"
    note = "В стресс-сценарии ликвидность может снизиться на один уровень для рисковых активов."
    if asset_class in {"Акции", "Криптоактивы", "Альтернативные"} and score > 1:
        note = "Для рисковых активов в стресс-сценарии принята пониженная ликвидность."
    return score, label, note


def complexity_score(asset_class: str, instrument: str = "", currency: str = "RUB", volatility_pct: float = 0.0, liquidity_days: float = 0.0, fee_pct: float = 0.0) -> tuple[int, str]:
    text = f"{instrument} {asset_class}".lower()
    if "вклад" in text or "накоп" in text:
        score = 1
    elif "офз" in text or "денежного рынка" in text:
        score = 2
    elif "корп" in text or "индекс" in text or asset_class == "Облигации":
        score = 3
    elif asset_class == "Акции":
        score = 4
    elif asset_class in {"Криптоактивы", "Альтернативные"}:
        score = 5
    else:
        score = 2
    if currency and currency.upper() not in {"RUB", "₽", "БАЗОВАЯ"}:
        score += 1
    if float(volatility_pct) >= 25:
        score += 1
    if float(liquidity_days) > 90:
        score += 1
    if float(fee_pct) > 1:
        score += 1
    score = max(1, min(5, score))
    return score, label_from_score(score, "Низкая", "Средняя", "Высокая")


def risk_score(asset_class: str, volatility_pct: float, stress_loss_pct: float = 0.0, concentration_pct: float = 0.0, currency: str = "RUB") -> tuple[int, str, list[str]]:
    drivers: list[str] = []
    score = 1
    vol = float(volatility_pct)
    if vol >= 25:
        score += 3
        drivers.append("высокая волатильность")
    elif vol >= 12:
        score += 2
        drivers.append("средняя волатильность")
    elif vol >= 5:
        score += 1
    if asset_class in {"Акции", "Криптоактивы", "Альтернативные"}:
        score += 1
        drivers.append("класс актива")
    if abs(float(stress_loss_pct)) >= 25:
        score += 1
        drivers.append("стресс-просадка")
    if float(concentration_pct) >= 35:
        score += 1
        drivers.append("концентрация")
    if currency and currency.upper() not in {"RUB", "₽", "БАЗОВАЯ"}:
        score += 1
        drivers.append("валютный риск")
    score = max(1, min(5, score))
    return score, label_from_score(score, "Низкий", "Средний", "Высокий"), drivers or ["пользовательские допущения"]

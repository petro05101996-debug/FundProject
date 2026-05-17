"""Instrument catalog metadata for educational UI and calculators."""
from __future__ import annotations

INSTRUMENT_CATALOG = {
    "Вклад": {
        "asset_class": "Денежные средства",
        "risk_score": 1,
        "liquidity_score": 3,
        "complexity_score": 1,
        "horizon": "1–36 месяцев",
        "checks": ["ставка", "капитализация", "досрочное снятие", "налог", "лимит страхования"],
    },
    "Накопительный счёт": {
        "asset_class": "Денежные средства",
        "risk_score": 1,
        "liquidity_score": 5,
        "complexity_score": 1,
        "horizon": "1–12 месяцев",
        "checks": ["минимальный остаток", "условия начисления", "изменение ставки", "налог"],
    },
    "ОФЗ": {
        "asset_class": "Облигации",
        "risk_score": 2,
        "liquidity_score": 4,
        "complexity_score": 2,
        "horizon": "до даты погашения или выбранного срока",
        "checks": ["НКД", "цена", "купон", "срок", "комиссия", "налог"],
    },
    "Корпоративная облигация": {
        "asset_class": "Облигации",
        "risk_score": 3,
        "liquidity_score": 3,
        "complexity_score": 3,
        "horizon": "до даты погашения или выбранного срока",
        "checks": ["рейтинг", "спред", "ликвидность выпуска", "кредитный риск", "комиссия"],
    },
    "Фонд денежного рынка": {
        "asset_class": "Денежные средства",
        "risk_score": 1,
        "liquidity_score": 4,
        "complexity_score": 2,
        "horizon": "короткий горизонт",
        "checks": ["комиссия фонда", "биржевая ликвидность", "налог", "валюта"],
    },
    "Индексный фонд": {
        "asset_class": "Акции",
        "risk_score": 4,
        "liquidity_score": 4,
        "complexity_score": 3,
        "horizon": "средний или длинный горизонт",
        "checks": ["волатильность", "комиссия фонда", "валюта", "регион", "tracking error"],
    },
}

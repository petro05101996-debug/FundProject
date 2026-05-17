"""Scenario templates for the scenario builder."""
from __future__ import annotations

SCENARIO_TEMPLATES = [
    {
        "name": "Сбалансированный пример",
        "description": "Пример с денежной частью, облигациями и индексным фондом для проверки формы.",
        "rows": [
            {"scenario": "Сбалансированный пример", "instrument": "Денежная часть", "ticker": "CASH", "asset_class": "Денежные средства", "country": "Пользовательский ввод", "currency": "RUB", "market_value": 30000, "expected_return_pct": 4, "volatility_pct": 1, "liquidity_days": 1, "annual_fee_pct": 0, "tax_pct": 13},
            {"scenario": "Сбалансированный пример", "instrument": "Облигационная часть", "ticker": "BOND", "asset_class": "Облигации", "country": "Пользовательский ввод", "currency": "RUB", "market_value": 40000, "expected_return_pct": 8, "volatility_pct": 7, "liquidity_days": 5, "annual_fee_pct": 0.2, "tax_pct": 13},
            {"scenario": "Сбалансированный пример", "instrument": "Индексная часть", "ticker": "INDEX", "asset_class": "Акции", "country": "Пользовательский ввод", "currency": "RUB", "market_value": 30000, "expected_return_pct": 10, "volatility_pct": 22, "liquidity_days": 2, "annual_fee_pct": 0.6, "tax_pct": 13},
        ],
    },
    {
        "name": "Ликвидный пример",
        "description": "Пример с повышенной долей денежных инструментов.",
        "rows": [
            {"scenario": "Ликвидный пример", "instrument": "Накопительный счёт", "ticker": "SAVE", "asset_class": "Денежные средства", "country": "Пользовательский ввод", "currency": "RUB", "market_value": 70000, "expected_return_pct": 5, "volatility_pct": 1, "liquidity_days": 1, "annual_fee_pct": 0, "tax_pct": 13},
            {"scenario": "Ликвидный пример", "instrument": "Фонд денежного рынка", "ticker": "MMF", "asset_class": "Денежные средства", "country": "Пользовательский ввод", "currency": "RUB", "market_value": 30000, "expected_return_pct": 6, "volatility_pct": 2, "liquidity_days": 2, "annual_fee_pct": 0.3, "tax_pct": 13},
        ],
    },
]

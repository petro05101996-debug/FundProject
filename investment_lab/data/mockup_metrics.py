"""Static values transcribed from the provided UI mockups.

These constants are intentionally used for first-run/demo presentation so that
visible calculations in the Streamlit UI match the design assets exactly.
Interactive editors can still change the underlying user-entered data.
"""
from __future__ import annotations

MOCKUP_RESULTS = [
    {
        "scenario": "Вклад + фонд денежного рынка",
        "portfolio_value": 10_000_000.0,
        "projected_value": 12_540_000.0,
        "stress_value": 10_210_000.0,
        "net_return_pct": 4.630790695798392,
        "worst_stress_impact_pct": -18.580542264752795,
        "liquidity_label": "Высокая",
        "risk_label": "Средний",
        "complexity_label": "Средняя",
        "max_position_pct": 34.0,
        "constraint_fit_score": 95.0,
        "status": "Лучше соответствует ограничениям",
    },
    {
        "scenario": "Сбалансированный портфель (ETF)",
        "portfolio_value": 10_000_000.0,
        "projected_value": 12_120_000.0,
        "stress_value": 9_720_000.0,
        "net_return_pct": 3.92033162539596,
        "worst_stress_impact_pct": -19.801980198019805,
        "liquidity_label": "Средняя",
        "risk_label": "Средний",
        "complexity_label": "Средняя",
        "max_position_pct": 48.0,
        "constraint_fit_score": 78.0,
        "status": "Допустимо с риск-флагами",
    },
    {
        "scenario": "Акции российских компаний",
        "portfolio_value": 10_000_000.0,
        "projected_value": 13_860_000.0,
        "stress_value": 8_960_000.0,
        "net_return_pct": 6.74625463871723,
        "worst_stress_impact_pct": -35.35353535353536,
        "liquidity_label": "Низкая",
        "risk_label": "Высокий",
        "complexity_label": "Средняя",
        "max_position_pct": 67.0,
        "constraint_fit_score": 42.0,
        "status": "Есть риск-флаги",
    },
    {
        "scenario": "Акции иностранных компаний (Global)",
        "portfolio_value": 10_000_000.0,
        "projected_value": 14_310_000.0,
        "stress_value": 9_480_000.0,
        "net_return_pct": 7.430581565768501,
        "worst_stress_impact_pct": -33.75262054507338,
        "liquidity_label": "Средняя",
        "risk_label": "Высокий",
        "complexity_label": "Средняя",
        "max_position_pct": 63.0,
        "constraint_fit_score": 38.0,
        "status": "Не соответствует ограничениям",
    },
]

MOCKUP_LANDING_KPIS = {
    "projected_value": 12_540_000.0,
    "growth_pct": 8.6,
    "stress_drawdown_pct": -18.3,
    "max_drawdown_pct": -24.7,
    "liquidity": "Высокая",
    "commission_pct": 0.72,
    "tax_pct": 12.4,
}

MOCKUP_SCENARIO_CARDS = [
    {
        "name": "Сценарий А",
        "total": 10_000_000,
        "shares": [40, 25, 20, 15],
        "instruments": [
            ("Вклад", 4_000_000, 40, "Низкий"),
            ("Фонд денежного рынка", 2_500_000, 25, "Низкий"),
            ("ОФЗ", 2_000_000, 20, "Средний"),
            ("Корпоративная облигация", 1_500_000, 15, "Высокий"),
        ],
    },
    {
        "name": "Сценарий Б",
        "total": 10_000_000,
        "shares": [30, 30, 25, 15],
        "instruments": [
            ("Фонд денежного рынка", 3_000_000, 30, "Низкий"),
            ("ОФЗ", 3_000_000, 30, "Средний"),
            ("Корпоративная облигация", 2_500_000, 25, "Высокий"),
            ("Вклад", 1_500_000, 15, "Низкий"),
        ],
    },
    {
        "name": "Сценарий В",
        "total": 10_000_000,
        "shares": [25, 25, 25, 25],
        "instruments": [
            ("ОФЗ", 2_500_000, 25, "Средний"),
            ("Корпоративная облигация", 2_500_000, 25, "Высокий"),
            ("Фонд денежного рынка", 2_500_000, 25, "Низкий"),
            ("Вклад", 2_500_000, 25, "Низкий"),
        ],
    },
]

MOCKUP_OFZ = {
    "final_value": 1_230_450.0,
    "final_delta_pct": 23.0,
    "irr_pct": 10.21,
    "stress_drawdown_pct": -7.9,
    "liquidity_days": 3,
    "liquidity_label": "Высокая",
    "risk_label": "Низкий",
    "complexity_label": "Низкая",
}

MOCKUP_PORTFOLIO = [
    {"instrument": "Акция A", "ticker": "SHARE_A", "asset_class": "Акции", "market_value": 1_000_000.0, "expected_return_pct": 11.0, "volatility_pct": 27.0, "liquidity_days": 2, "annual_fee_pct": 0.06, "tax_pct": 13.0},
    {"instrument": "Акция B", "ticker": "SHARE_B", "asset_class": "Акции", "market_value": 800_000.0, "expected_return_pct": 10.0, "volatility_pct": 25.0, "liquidity_days": 2, "annual_fee_pct": 0.06, "tax_pct": 13.0},
    {"instrument": "Облигация A", "ticker": "BOND_A", "asset_class": "Облигации", "market_value": 700_000.0, "expected_return_pct": 8.2, "volatility_pct": 7.0, "liquidity_days": 3, "annual_fee_pct": 0.03, "tax_pct": 13.0},
    {"instrument": "Денежный фонд A", "ticker": "MMF_A", "asset_class": "Денежные средства", "market_value": 250_000.0, "expected_return_pct": 6.0, "volatility_pct": 1.0, "liquidity_days": 1, "annual_fee_pct": 0.10, "tax_pct": 13.0},
    {"instrument": "Товарный актив A", "ticker": "COMMODITY_A", "asset_class": "Товары", "market_value": 200_000.0, "expected_return_pct": 5.0, "volatility_pct": 18.0, "liquidity_days": 2, "annual_fee_pct": 0.25, "tax_pct": 13.0},
]

MOCKUP_MISMATCH_NOTES = [
    "В портфельном макете сумма позиций 2 950 000 ₽ не совпадает с отдельными процентами рядом с легендой; в UI проценты считаются от указанной суммы позиций.",
]

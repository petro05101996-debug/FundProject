"""Bond calculators for OFZ and corporate bonds."""
from __future__ import annotations


def calculate_bond(amount: float, accrued_coupon: float, clean_price_pct: float, nominal: float, coupon_pct: float, years_to_maturity: float, coupon_frequency: int, commission_pct: float, tax_pct: float, default_risk_pct: float = 0.0) -> dict[str, float | str | list[float]]:
    clean_price = nominal * clean_price_pct / 100
    dirty_price = clean_price + accrued_coupon
    units = amount / max(dirty_price, 1)
    annual_coupon = nominal * coupon_pct / 100
    coupon_cashflows = [units * annual_coupon / max(coupon_frequency, 1) for _ in range(int(max(years_to_maturity, 0.1) * max(coupon_frequency, 1)))]
    coupon_total = sum(coupon_cashflows)
    price_gain = max(nominal - clean_price, 0) * units
    tax_on_coupon = max(coupon_total, 0) * tax_pct / 100
    tax_on_price_gain = max(price_gain, 0) * tax_pct / 100
    commission = amount * commission_pct / 100
    final_after_tax = amount + coupon_total + price_gain - tax_on_coupon - tax_on_price_gain - commission
    ytm = ((nominal - dirty_price) / max(years_to_maturity, 0.1) + annual_coupon) / max(dirty_price, 1) * 100 - default_risk_pct
    return {
        "dirty_price": dirty_price,
        "coupon_cashflows": coupon_cashflows,
        "yield_to_maturity_approx": ytm,
        "tax_on_coupon": tax_on_coupon,
        "tax_on_price_gain": tax_on_price_gain,
        "final_after_tax": final_after_tax,
        "duration_proxy": min(max(years_to_maturity * 0.75, 0.1), years_to_maturity),
        "interest_rate_risk_flag": "Цена облигации может снизиться при росте ставок.",
        "sell_before_maturity_flag": "Продажа до погашения может дать результат ниже расчётного.",
        "methodology": {
            "model_type": "simplified_bond_calculation",
            "is_simplified": True,
            "limitations": [
                "не учитывается полный календарь купонов",
                "не учитываются оферты",
                "не учитывается амортизация, если она не введена пользователем",
                "НКД считается упрощённо",
                "YTM является приблизительной оценкой",
            ],
        },
    }

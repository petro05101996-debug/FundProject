"""Fund calculators."""
from __future__ import annotations


def calculate_fund(amount: float, expected_return_pct: float, management_fee_pct: float, term_months: int, tax_pct: float, tracking_error_pct: float = 0.5) -> dict[str, float | str]:
    years = max(term_months, 1) / 12
    gross_return = amount * expected_return_pct / 100 * years
    management_fee_drag = amount * management_fee_pct / 100 * years
    taxable = max(gross_return - management_fee_drag, 0)
    tax_drag = taxable * tax_pct / 100
    return {
        "gross_return": gross_return,
        "management_fee_drag": management_fee_drag,
        "tax_drag": tax_drag,
        "tracking_error_note": f"Tracking error задан как пользовательское допущение: {tracking_error_pct:.1f}%.",
        "liquidity_note": "Биржевая ликвидность зависит от торгов и маркет-мейкера.",
        "final_after_tax": amount + gross_return - management_fee_drag - tax_drag,
        "methodology": {
            "model_type": "simplified_fund_calculation",
            "is_simplified": True,
            "limitations": [
                "результат зависит от пользовательской ожидаемой доходности",
                "не используются реальные котировки фонда",
                "комиссии и tracking error задаются упрощённо",
            ],
        },
    }

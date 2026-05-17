"""Deposit and savings-account calculators."""
from __future__ import annotations


def calculate_deposit(amount: float, annual_rate_pct: float, term_months: int, capitalization: bool, early_withdrawal: bool, tax_pct: float, insurance_limit: float, currency: str) -> dict[str, float | str]:
    years = max(term_months, 1) / 12
    if capitalization:
        final_before_tax = amount * (1 + annual_rate_pct / 100 / 12) ** max(term_months, 1)
        gross_interest = final_before_tax - amount
    else:
        gross_interest = amount * annual_rate_pct / 100 * years
        final_before_tax = amount + gross_interest
    tax = max(gross_interest, 0) * tax_pct / 100
    net_interest = gross_interest - tax
    return {
        "gross_interest": gross_interest,
        "tax": tax,
        "net_interest": net_interest,
        "final_amount": amount + net_interest,
        "early_withdrawal_note": "Досрочное снятие может изменить процентный результат." if early_withdrawal else "Досрочное снятие не учтено в базовом расчёте.",
        "insurance_limit_note": f"Проверьте лимит страхования: {insurance_limit:,.0f} {currency}.",
    }


def calculate_savings_account(amount: float, annual_rate_pct: float, term_months: int, min_balance: float, tax_pct: float, withdrawals_allowed: bool) -> dict[str, float | str]:
    average_balance = max(min_balance, amount)
    gross_interest = average_balance * annual_rate_pct / 100 * max(term_months, 1) / 12
    tax = max(gross_interest, 0) * tax_pct / 100
    return {
        "average_balance": average_balance,
        "gross_interest": gross_interest,
        "tax": tax,
        "net_interest": gross_interest - tax,
        "rate_change_risk": "Ставка может измениться по условиям банка.",
        "withdrawal_note": "Снятие возможно по пользовательскому допущению." if withdrawals_allowed else "Снятие может ограничиваться условиями счёта.",
    }

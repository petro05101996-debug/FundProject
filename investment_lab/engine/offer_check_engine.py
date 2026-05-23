from __future__ import annotations
from pydantic import BaseModel
from investment_lab.data.legal_texts import API_DISCLAIMER
from investment_lab.engine.offer_risk_flags import build_offer_flags

class OfferCheckInput(BaseModel):
    offer_source: str | None = None
    offer_text: str | None = None
    instrument_type: str | None = None
    user_amount: float | None = None
    expected_return_pct: float | None = None
    return_wording: str | None = None
    term_months: int | None = None
    early_exit_type: str | None = None
    fees_known: bool | None = None
    fee_pct: float | None = None
    tax_rate_pct: float | None = None
    capital_protection_claimed: bool | None = None
    guaranteed_wording_present: bool | None = None
    issuer_or_provider: str | None = None
    user_goal: str | None = None
    liquidity_need: str | None = None
    drawdown_tolerance: str | None = None
    experience_level: str | None = None
    unknown_fields: list[str] = []


def analyze_offer(inp: OfferCheckInput) -> dict:
    amount = inp.user_amount or 100000
    ret = inp.expected_return_pct or 12
    fee = inp.fee_pct or (1.0 if inp.fees_known else 1.5)
    tax = inp.tax_rate_pct or 13
    base = amount * (1 + (ret - fee) / 100) * (1 - tax / 100 * 0.1)
    stress = amount * (1 + max(ret - 10, -20) / 100) * (1 - tax / 100 * 0.1)
    unknown_terms = list(inp.unknown_fields)
    if inp.early_exit_type in {None, "unknown"}: unknown_terms.append("early_exit_terms")
    if inp.fees_known is False: unknown_terms.append("fees")
    questions = [
        "Эта доходность гарантирована или это ориентир?",
        "Что означает «до X%»?",
        "Что будет при досрочном выходе?",
        "Какие комиссии применяются?",
        "Кто эмитент или контрагент?",
        "Есть ли риск потери капитала?",
        "Как облагается доход налогом?",
        "Где официальный документ с условиями?",
    ]
    flags = build_offer_flags(inp.model_dump())
    return {
        "plain_summary": "По введённым данным предложение требует проверки ключевых условий перед решением.",
        "extracted_terms": {"instrument_type": inp.instrument_type, "expected_return_pct": inp.expected_return_pct, "term_months": inp.term_months},
        "known_terms": [k for k,v in inp.model_dump().items() if v not in (None, "", [])],
        "unknown_terms": sorted(set(unknown_terms)),
        "red_flags": flags,
        "questions_to_ask": questions,
        "base_scenario": {"start_amount": amount, "expected_after_tax": round(base,2)},
        "stress_scenario": {"stress_after_tax": round(stress,2), "stress_delta": round(stress-amount,2)},
        "risk_score": "elevated" if len(flags) >= 3 else "moderate",
        "liquidity_score": "unknown" if "early_exit_terms" in unknown_terms else "medium",
        "complexity_score": "requires_attention" if inp.instrument_type in {"structured_product", "unknown"} else "medium",
        "benchmark_comparison": {"reference": "deposit", "note": "Для ориентира сравните доходность с простыми инструментами и учтите риск/ликвидность."},
        "assumptions": ["Использован информационный сценарный расчёт.", "Неизвестные параметры заменены осторожными допущениями."],
        "limitations": ["Результат основан на введённых пользователем параметрах.", "Расчёт упрощён и не учитывает все рыночные факторы."],
        "disclaimer": API_DISCLAIMER,
    }

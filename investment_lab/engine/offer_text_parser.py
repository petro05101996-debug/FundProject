from __future__ import annotations
import re

MARKERS = ["до", "потенциально", "гарант", "защита капитала", "без риска", "структур", "купон", "погаш", "досроч", "комис", "оферт", "эмитент", "ликвид"]


def parse_offer_text(offer_text: str) -> dict:
    text = (offer_text or "").lower()
    pct = re.findall(r"(\d+(?:[\.,]\d+)?)\s?%", text)
    detected_return_pct = float(pct[0].replace(',', '.')) if pct else None
    term_months = None
    y = re.search(r"(\d+)\s*год", text)
    m = re.search(r"(\d+)\s*мес", text)
    if y:
        term_months = int(y.group(1)) * 12
    elif m:
        term_months = int(m.group(1))
    claims = [m for m in ["доходность до", "защита капитала", "без риска", "гарантированно"] if m in text]
    detected_instrument_type = "structured_product" if "структур" in text else "bond" if "облига" in text else "fund" if "фонд" in text else "deposit" if "вклад" in text else "unknown"
    missing_fields = []
    if "комис" not in text:
        missing_fields.append("fees")
    if "досроч" not in text:
        missing_fields.append("early_exit_terms")
    if "эмитент" not in text and "банк" not in text and "брокер" not in text:
        missing_fields.append("issuer")
    if "налог" not in text:
        missing_fields.append("tax")
    preliminary_flags = []
    if "до " in text and detected_return_pct is not None:
        preliminary_flags.append("return_wording_not_guaranteed")
    if "защита капитала" in text:
        preliminary_flags.append("capital_protection_terms_unknown")
    if any(x in text for x in ["без риска", "эксклюзив", "лучше вклада"]):
        preliminary_flags.append("marketing_wording_detected")
    return {
        "detected_instrument_type": detected_instrument_type,
        "detected_return_pct": detected_return_pct,
        "detected_term_months": term_months,
        "detected_claims": claims,
        "missing_fields": missing_fields,
        "preliminary_flags": preliminary_flags,
    }

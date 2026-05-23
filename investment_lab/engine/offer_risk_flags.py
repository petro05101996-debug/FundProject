from __future__ import annotations

def build_offer_flags(data: dict) -> list[dict]:
    flags = []
    def add(code, msg):
        flags.append({"code": code, "message": msg})
    if str(data.get("offer_source", "")).lower() in {"telegram", "telegram/соцсети", "блогер"}:
        add("unofficial_source", "Источник предложения требует дополнительной проверки.")
    if data.get("early_exit_type") in {None, "unknown", "Не знаю", "В условиях не указано"}:
        add("unknown_early_exit", "Условия досрочного выхода неизвестны.")
    if not data.get("fees_known", False):
        add("unknown_fees", "Комиссии не указаны.")
    if (data.get("expected_return_pct") or 0) >= 18:
        add("high_return_requires_check", "Заявленная доходность требует дополнительной проверки относительно риска.")
    if data.get("return_wording") and "до" in str(data.get("return_wording")).lower():
        add("return_wording_to", "Доходность указана как «до X%».")
    if data.get("capital_protection_claimed") and not data.get("guaranteed_wording_present"):
        add("capital_protection_unclear", "Заявлена защита капитала, но условия не раскрыты.")
    return flags

from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any
from investment_lab.data.scenario_templates import GUIDED_SCENARIO_TEMPLATES

QUESTION_BANK = {
    "amount": {"id":"amount","title":"Какую сумму хотите проверить?","description":"Сумма влияет на итог и ограничения.","type":"money","allow_unknown":False},
    "horizon": {"id":"horizon","title":"На какой срок рассматриваете сценарий?","description":"Срок влияет на риск и ликвидность.","type":"single_choice","options":[{"value":"6","label":"До 6 месяцев"},{"value":"12","label":"6–12 месяцев"},{"value":"24","label":"1–2 года"},{"value":"36","label":"2–3 года"},{"value":"unknown","label":"Не знаю"}],"allow_unknown":True,"help_topic":"horizon"},
    "liquidity_need": {"id":"liquidity_need","title":"Когда деньги могут понадобиться?","description":"При досрочном выходе результат может ухудшиться.","type":"single_choice","options":[{"value":"anytime","label":"В любой момент"},{"value":"three_months","label":"До 3 месяцев"},{"value":"six_to_twelve","label":"3–12 месяцев"},{"value":"one_to_three_years","label":"1–3 года"},{"value":"more_than_three_years","label":"Более 3 лет"},{"value":"unknown","label":"Не знаю"}],"allow_unknown":True,"help_topic":"liquidity"},
    "drawdown_tolerance": {"id":"drawdown_tolerance","title":"Какую просадку готовы принять?","description":"Помогает оценить стресс-риски.","type":"percent","allow_unknown":True,"help_topic":"drawdown"},
    "experience_level": {"id":"experience_level","title":"Какой у вас опыт?","description":"Нужно, чтобы оценить сложность.","type":"single_choice","options":[{"value":"beginner","label":"Начинающий"},{"value":"intermediate","label":"Есть опыт"},{"value":"advanced","label":"Продвинутый"},{"value":"unknown","label":"Не знаю"}],"allow_unknown":True},
    "has_specific_options": {"id":"has_specific_options","title":"Есть конкретные варианты для проверки?","description":"Можно сравнить типовые или ваши варианты.","type":"yes_no","allow_unknown":True},
    "instrument_type": {"id":"instrument_type","title":"Какой инструмент хотите разобрать?","description":"Это поможет дать объяснение и пример расчёта.","type":"instrument_choice","allow_unknown":False},

    "offer_type": {"id":"offer_type","title":"Что вам предложили?","description":"Это нужно, чтобы выбрать модель проверки.","type":"single_choice","options":[{"value":"deposit","label":"Вклад"},{"value":"savings","label":"Накопительный счёт"},{"value":"bond","label":"Облигация"},{"value":"fund","label":"Фонд"},{"value":"structured_product","label":"Структурный продукт"},{"value":"portfolio","label":"Портфель"},{"value":"unknown","label":"Не знаю"}],"allow_unknown":True},
    "offer_source": {"id":"offer_source","title":"Откуда предложение?","description":"Источник влияет на необходимость дополнительной проверки.","type":"single_choice","options":[{"value":"bank","label":"Банк"},{"value":"broker","label":"Брокер"},{"value":"telegram","label":"Telegram/соцсети"},{"value":"blogger","label":"Финансовый блогер"},{"value":"ad","label":"Реклама"},{"value":"friend","label":"Знакомый"},{"value":"unknown","label":"Не знаю"}],"allow_unknown":True},
    "offer_return": {"id":"offer_return","title":"Какая доходность заявлена?","description":"Если не знаете, оставьте неизвестно.","type":"percent","allow_unknown":True},
    "offer_term": {"id":"offer_term","title":"На какой срок предложение?","description":"Срок влияет на ликвидность и риск.","type":"single_choice","options":[{"value":"3","label":"До 3 месяцев"},{"value":"12","label":"3–12 месяцев"},{"value":"36","label":"1–3 года"},{"value":"60","label":"Более 3 лет"},{"value":"unknown","label":"Не знаю"}],"allow_unknown":True},
    "offer_early_exit": {"id":"offer_early_exit","title":"Можно ли выйти раньше срока?","description":"Ключевой параметр ликвидности.","type":"single_choice","options":[{"value":"no_loss","label":"Да, без потерь"},{"value":"with_loss","label":"Да, с потерями"},{"value":"market_sale","label":"Можно продать на рынке"},{"value":"not_allowed","label":"Нельзя"},{"value":"unknown","label":"Не знаю"}],"allow_unknown":True},
    "offer_fees": {"id":"offer_fees","title":"Известны комиссии?","description":"Комиссии влияют на итоговый результат.","type":"single_choice","options":[{"value":"none","label":"Нет"},{"value":"known","label":"Есть, известны"},{"value":"unknown","label":"Не знаю"}],"allow_unknown":True},
    "main_concern": {"id":"main_concern","title":"Что беспокоит больше всего?","description":"Это влияет на акцент результата.","type":"single_choice","options":[{"value":"capital","label":"Не потерять деньги"},{"value":"liquidity","label":"Не заморозить деньги"},{"value":"return_realism","label":"Проверить доходность"},{"value":"stress","label":"Плохой сценарий"},{"value":"questions","label":"Какие вопросы задать"},{"value":"understanding","label":"Не понимаю инструмент"}],"allow_unknown":True},
}

DEFAULTS = {"horizon": "12", "liquidity_need": "six_to_twelve", "drawdown_tolerance": "10", "experience_level": "beginner", "has_specific_options": "no", "offer_type":"unknown", "offer_source":"unknown", "offer_return":"not_provided", "offer_term":"12", "offer_early_exit":"unknown", "offer_fees":"unknown", "main_concern":"questions"}

@dataclass
class DialogState:
    scenario_template_id: str
    answers: dict[str, Any]
    unknown_fields: list[str]
    assumptions: list[dict[str, Any]]
    current_index: int

class DialogEngine:
    def __init__(self):
        self.templates = {t["id"]: t for t in GUIDED_SCENARIO_TEMPLATES}

    def start(self, template_id: str) -> dict[str, Any]:
        template = self.templates[template_id]
        state = DialogState(template_id, {}, [], [], 0)
        return self._response(state, template)

    def answer(self, state: dict[str, Any], question_id: str, answer: Any) -> dict[str, Any]:
        s = DialogState(**state)
        template = self.templates[s.scenario_template_id]
        if answer == "unknown":
            s.unknown_fields.append(question_id)
            fallback = DEFAULTS.get(question_id, "not_provided")
            s.answers[question_id] = fallback
            s.assumptions.append({"field": question_id, "message": "Параметр не указан пользователем. Использовано осторожное допущение.", "severity": "medium"})
        else:
            s.answers[question_id] = answer
        s.current_index += 1
        return self._response(s, template)

    def preview(self, state: dict[str, Any]) -> dict[str, Any]:
        s = DialogState(**state)
        t = self.templates[s.scenario_template_id]
        return {
            "scenario_title": t["title"],
            "what_will_be_calculated": ["Базовый сценарий", "Стресс-сценарий", "Риск", "Ликвидность", "Сложность"],
            "user_answers": s.answers,
            "assumptions": s.assumptions,
            "unknown_fields": s.unknown_fields,
            "warnings": ["Некоторые параметры не указаны, используется осторожное допущение."] if s.unknown_fields else [],
        }

    def _response(self, s: DialogState, t: dict[str, Any]) -> dict[str, Any]:
        questions = t["questions"]
        if s.current_index >= len(questions):
            return {"session_state": asdict(s), "preview_ready": True}
        qid = questions[s.current_index]
        return {"session_state": asdict(s), "current_question": QUESTION_BANK[qid], "preview_ready": False, "progress": {"current": s.current_index + 1, "total": len(questions)}}

    def to_scenario_payload(self, state: dict[str, Any]) -> dict[str, Any]:
        s = DialogState(**state)
        amount = float(s.answers.get("amount", 100000))
        horizon = int(float(s.answers.get("horizon", 12)))
        if s.scenario_template_id == "offer_check":
            return {"offer_input": {"offer_source": s.answers.get("offer_source"), "instrument_type": s.answers.get("offer_type"), "expected_return_pct": float(s.answers.get("offer_return", 12) or 12) if str(s.answers.get("offer_return","not_provided")).replace(".","",1).isdigit() else 12, "term_months": int(float(s.answers.get("offer_term",12) or 12)), "early_exit_type": s.answers.get("offer_early_exit","unknown"), "fees_known": s.answers.get("offer_fees") == "known", "user_amount": float(s.answers.get("amount",100000) or 100000), "unknown_fields": s.unknown_fields}}

        rows = [
            {"scenario":"Guided A","instrument":"Вклад","ticker":"DEP","asset_class":"Денежные средства","country":"RU","currency":"RUB","market_value":amount,"expected_return_pct":8,"volatility_pct":1,"liquidity_days":1,"annual_fee_pct":0,"tax_pct":13},
            {"scenario":"Guided B","instrument":"ОФЗ","ticker":"OFZ","asset_class":"Облигации","country":"RU","currency":"RUB","market_value":amount,"expected_return_pct":10,"volatility_pct":6,"liquidity_days":3,"annual_fee_pct":0.2,"tax_pct":13},
        ]
        return {"assumptions": {"horizon_years": max(1, horizon // 12)}, "constraints": {}, "positions": rows}

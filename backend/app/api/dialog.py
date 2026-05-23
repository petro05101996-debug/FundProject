from __future__ import annotations
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from investment_lab.data.scenario_templates import GUIDED_SCENARIO_TEMPLATES
from investment_lab.engine.dialog_engine import DialogEngine
from investment_lab.engine.scenario_comparator import analyze_scenarios
from investment_lab.domain.models import ScenarioAssumptions, UserConstraints
from app.converters import result_to_jsonable
from investment_lab.data.legal_texts import API_DISCLAIMER
from investment_lab.engine.offer_check_engine import OfferCheckInput, analyze_offer

router = APIRouter()
engine = DialogEngine()

class StartReq(BaseModel):
    scenario_template_id: str

class AnswerReq(BaseModel):
    session_state: dict
    question_id: str
    answer: str | int | float | bool

class SessionReq(BaseModel):
    session_state: dict

@router.get('/scenarios/templates')
def list_templates():
    return [{"id": t["id"], "title": t["title"], "short_description": t["short_description"], "category": t.get("category", "beginner")} for t in GUIDED_SCENARIO_TEMPLATES]

@router.post('/dialog/start')
def dialog_start(req: StartReq):
    if req.scenario_template_id not in {t['id'] for t in GUIDED_SCENARIO_TEMPLATES}:
        raise HTTPException(422, 'Неизвестный сценарный шаблон')
    return engine.start(req.scenario_template_id)

@router.post('/dialog/answer')
def dialog_answer(req: AnswerReq):
    return engine.answer(req.session_state, req.question_id, req.answer)

@router.post('/dialog/preview')
def dialog_preview(req: SessionReq):
    return engine.preview(req.session_state)

@router.post('/analyze/guided')
def analyze_guided(req: SessionReq):
    payload = engine.to_scenario_payload(req.session_state)
    if 'offer_input' in payload:
        o = analyze_offer(OfferCheckInput(**payload['offer_input']))
        return {
            "plain_summary": o["plain_summary"],
            "base_result": o["base_scenario"],
            "stress_result": o["stress_scenario"],
            "risk": {"risk_score": o["risk_score"]},
            "liquidity": {"liquidity_score": o["liquidity_score"]},
            "complexity": {"complexity_score": o["complexity_score"]},
            "risk_flags": o["red_flags"],
            "checklist": o["questions_to_ask"],
            "details": {"assumptions": o["assumptions"], "methodology": ["offer_check"], "limitations": o["limitations"]},
            "report_payload": o,
            "disclaimer": API_DISCLAIMER,
        }
    result = analyze_scenarios(payload['positions'], ScenarioAssumptions(**payload['assumptions']), UserConstraints(**payload['constraints']))
    j = result_to_jsonable(result)
    summary = (j.get('summary') or [{}])[0]
    return {
        "plain_summary": "По введённым параметрам сценарий показывает возможный базовый результат и стресс-риск. Расчёт не является индивидуальной инвестиционной рекомендацией.",
        "base_result": {"projected_value": summary.get("projected_value"), "projected_profit": summary.get("projected_profit")},
        "stress_result": {"worst_stress_value": summary.get("worst_stress_value"), "worst_stress_impact_pct": summary.get("worst_stress_impact_pct")},
        "risk": {"risk_score": summary.get("risk_score"), "risk_label": summary.get("risk_label")},
        "liquidity": {"liquidity_score": summary.get("liquidity_score"), "liquidity_label": summary.get("liquidity_label")},
        "complexity": {"complexity_score": summary.get("complexity_score"), "complexity_label": summary.get("complexity_label")},
        "risk_flags": j.get("flags", []),
        "checklist": ["Проверьте комиссии и налоги.", "Проверьте условия досрочного выхода.", "Уточните параметры, отмеченные как неизвестные."],
        "details": {"assumptions": req.session_state.get("assumptions", []), "methodology": ["Сценарный анализ с упрощёнными допущениями"], "limitations": j.get("limitations", [])},
        "report_payload": {"result": j, "session_state": req.session_state, "disclaimer": API_DISCLAIMER},
        "disclaimer": API_DISCLAIMER,
    }

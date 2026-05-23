from __future__ import annotations
from fastapi import APIRouter
from pydantic import BaseModel
from investment_lab.engine.offer_text_parser import parse_offer_text
from investment_lab.engine.offer_check_engine import OfferCheckInput, analyze_offer

router = APIRouter()

class OfferTextReq(BaseModel):
    offer_text: str

@router.post('/offer-check/start')
def offer_start():
    return {"scenario": "offer_check", "title": "Проверить предложение"}

@router.post('/offer-check/parse-text')
def offer_parse(req: OfferTextReq):
    return parse_offer_text(req.offer_text)

@router.post('/offer-check/analyze')
def offer_analyze(req: OfferCheckInput):
    return analyze_offer(req)

@router.post('/offer-check/report')
def offer_report(req: OfferCheckInput):
    result = analyze_offer(req)
    return {"title": "Разбор предложения", "result": result}

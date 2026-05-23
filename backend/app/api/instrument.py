from __future__ import annotations
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, field_validator
from investment_lab.data.instrument_catalog import INSTRUMENT_CATALOG
from investment_lab.engine.bond_calculator import calculate_bond
from investment_lab.engine.deposit_calculator import calculate_deposit, calculate_savings_account
from investment_lab.engine.fund_calculator import calculate_fund

router = APIRouter()

def clean_flags(flags):
    return [str(x).strip() for x in flags if x is not None and str(x).strip() and str(x).strip().lower()!='none']

def parse_bool(value, default=False):
    if value is None: return default
    if isinstance(value, bool): return value
    if isinstance(value, (int, float)): return bool(value)
    if isinstance(value, str):
        n=value.strip().lower()
        if n in {'true','1','yes','да','y'}: return True
        if n in {'false','0','no','нет','n'}: return False
    return default

def to_float(value, field_name: str, default=None) -> float:
    try:
        if value is None or value == '':
            if default is not None:
                return float(default)
            raise ValueError
        return float(value)
    except (TypeError, ValueError):
        raise HTTPException(status_code=422, detail=f'Поле {field_name} должно быть числом')

def to_int(value, field_name: str, default=None) -> int:
    try:
        if value is None or value == '':
            if default is not None:
                return int(default)
            raise ValueError
        return int(value)
    except (TypeError, ValueError):
        raise HTTPException(status_code=422, detail=f'Поле {field_name} должно быть целым числом')

def coupon_frequency(value) -> int:
    if isinstance(value, (int, float)):
        freq = int(value)
    else:
        text = str(value or '').strip().lower()
        if 'год' in text and 'пол' not in text:
            freq = 1
        elif 'кварт' in text:
            freq = 4
        elif 'мес' in text:
            freq = 12
        else:
            freq = 2
    if freq not in {1, 2, 4, 12}:
        raise HTTPException(status_code=422, detail='Периодичность купона должна быть 1, 2, 4 или 12 раз в год')
    return freq

def default_risk_from_rating(value: str) -> float:
    text = str(value or '').upper()
    if 'AAA' in text or 'ОФЗ' in text:
        return 0.2
    if 'AA' in text:
        return 0.5
    if 'A' in text:
        return 1.0
    if 'BBB' in text:
        return 2.0
    if 'BB' in text:
        return 5.0
    return 2.0

class InstrumentCheckRequest(BaseModel):
    selectedInstrumentType: str
    params: dict = Field(default_factory=dict)
    @field_validator('selectedInstrumentType')
    @classmethod
    def non_empty(cls,v):
        if not v.strip(): raise ValueError('selectedInstrumentType is required')
        return v

def _labels(name: str):
    item = INSTRUMENT_CATALOG.get(name) or INSTRUMENT_CATALOG.get("Акция как класс") or {}
    r,l,c=item.get('risk_score',3),item.get('liquidity_score',3),item.get('complexity_score',3)
    return ('Низкий' if r<=2 else 'Средний' if r<=3 else 'Высокий','Низкая' if l<=2 else 'Средняя' if l<=3 else 'Высокая','Низкая' if c<=2 else 'Средняя' if c<=3 else 'Высокая',item.get('checks',[]))

@router.post('/check')
def check_instrument(req: InstrumentCheckRequest):
    t,p=req.selectedInstrumentType,req.params
    if not p:
        raise HTTPException(status_code=422, detail='Параметры инструмента не переданы')
    amount=to_float(p.get('amount',p.get('sum',0)), 'amount', 0)
    if amount<=0:
        raise HTTPException(status_code=422, detail='Сумма должна быть больше 0')
    tax_pct=max(0,min(100,to_float(p.get('tax_pct', p.get('tax_rate', 13)), 'tax_pct', 13)))
    risk_label, liquidity_label, complexity_label, checklist = _labels(t)
    if t=='Вклад':
        calc=calculate_deposit(amount, to_float(p.get('annual_rate_pct', p.get('rate', 0)), 'annual_rate_pct', 0), to_int(p.get('term_months',12), 'term_months', 12), parse_bool(p.get('capitalization'),True), parse_bool(p.get('early_withdrawal'),False), tax_pct, to_float(p.get('insurance_limit',1_400_000), 'insurance_limit', 1_400_000), str(p.get('currency','RUB')))
        expected,income=float(calc['final_amount']),float(calc['net_interest']); risk_flags=clean_flags([calc.get('early_withdrawal_note'),calc.get('insurance_limit_note')])
    elif t=='Накопительный счёт':
        calc=calculate_savings_account(amount,to_float(p.get('annual_rate_pct', p.get('rate', 0)), 'annual_rate_pct', 0),to_int(p.get('term_months',12), 'term_months', 12),to_float(p.get('min_balance',amount), 'min_balance', amount),tax_pct,parse_bool(p.get('withdrawals_allowed'),True))
        expected,income=amount+float(calc['net_interest']),float(calc['net_interest']); risk_flags=clean_flags([calc.get('rate_change_risk'),calc.get('withdrawal_note')])
    elif t in {'ОФЗ','Корпоративная облигация'}:
        accrued_coupon = to_float(p.get('accrued_coupon', p.get('nkd', 0)), 'accrued_coupon', 0)
        coupon_freq = coupon_frequency(p.get('coupon_frequency', p.get('coupon_period', 2)))
        default_risk = to_float(p.get('default_risk_pct'), 'default_risk_pct', 0 if t == 'ОФЗ' else default_risk_from_rating(p.get('issuer_rating')))
        calc=calculate_bond(amount,accrued_coupon,to_float(p.get('clean_price_pct',95), 'clean_price_pct', 95),to_float(p.get('nominal',1000), 'nominal', 1000),to_float(p.get('coupon_pct',10), 'coupon_pct', 10),to_float(p.get('years_to_maturity',2), 'years_to_maturity', 2),coupon_freq,to_float(p.get('commission_pct',0.2), 'commission_pct', 0),tax_pct,default_risk)
        expected,income=float(calc['final_after_tax']),float(calc['final_after_tax'])-amount; risk_flags=clean_flags([calc.get('interest_rate_risk_flag'),calc.get('sell_before_maturity_flag')])
    elif t in {'Фонд денежного рынка', 'Индексный фонд', 'Облигационный фонд', 'Акция как класс риска'}:
        calc=calculate_fund(amount,to_float(p.get('expected_return_pct',10), 'expected_return_pct', 0),to_float(p.get('management_fee_pct',0.8), 'management_fee_pct', 0),to_int(p.get('term_months',12), 'term_months', 12),tax_pct,to_float(p.get('tracking_error_pct',0.5), 'tracking_error_pct', 0.5))
        expected,income=float(calc['final_after_tax']),float(calc['final_after_tax'])-amount; risk_flags=clean_flags([calc.get('tracking_error_note'),calc.get('liquidity_note'),'Оценка класса риска, а не расчёт конкретной акции.' if t=='Акция как класс риска' else None])
    else:
        raise HTTPException(status_code=422, detail='Неизвестный тип инструмента')
    stress_default = -20 if 'Акция' in t or 'Индексный' in t else -8
    stress_drawdown = to_float(p.get('stress_drawdown_pct', stress_default), 'stress_drawdown_pct', stress_default)
    return {'instrument_type':t,'explanation':'Инструмент имеет такие последствия при введённых параметрах.','expected_value':expected,'income_estimate':income,'stress_drawdown':stress_drawdown,'liquidity_label':liquidity_label,'risk_label':risk_label,'complexity_label':complexity_label,'risk_flags':risk_flags,'assumptions':p,'limitations':['Оценка основана на пользовательском вводе и упрощённых сценарных допущениях.'],'checklist':checklist}

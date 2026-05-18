from __future__ import annotations
from fastapi import APIRouter
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
    amount=float(p.get('amount',p.get('sum',0)) or 0)
    if amount<=0: raise ValueError('amount must be > 0')
    tax_pct=max(0,min(100,float(p.get('tax_pct', p.get('tax_rate', 13)) or 13)))
    risk_label, liquidity_label, complexity_label, checklist = _labels(t)
    if t=='Вклад':
        calc=calculate_deposit(amount, float(p.get('annual_rate_pct', p.get('rate', 0)) or 0), int(p.get('term_months',12) or 12), parse_bool(p.get('capitalization'),True), parse_bool(p.get('early_withdrawal'),False), tax_pct, float(p.get('insurance_limit',1_400_000) or 1_400_000), str(p.get('currency','RUB')))
        expected,income=float(calc['final_amount']),float(calc['net_interest']); risk_flags=clean_flags([calc.get('early_withdrawal_note'),calc.get('insurance_limit_note')])
    elif t=='Накопительный счёт':
        calc=calculate_savings_account(amount,float(p.get('annual_rate_pct', p.get('rate', 0)) or 0),int(p.get('term_months',12) or 12),float(p.get('min_balance',amount) or amount),tax_pct,parse_bool(p.get('withdrawals_allowed'),True))
        expected,income=amount+float(calc['net_interest']),float(calc['net_interest']); risk_flags=clean_flags([calc.get('rate_change_risk'),calc.get('withdrawal_note')])
    elif t in {'ОФЗ','Корпоративная облигация'}:
        calc=calculate_bond(amount,float(p.get('accrued_coupon',0) or 0),float(p.get('clean_price_pct',95) or 95),float(p.get('nominal',1000) or 1000),float(p.get('coupon_pct',10) or 10),float(p.get('years_to_maturity',2) or 2),int(p.get('coupon_frequency',2) or 2),float(p.get('commission_pct',0.2) or 0),tax_pct,float(p.get('default_risk_pct',0 if t=='ОФЗ' else 2) or 0))
        expected,income=float(calc['final_after_tax']),float(calc['final_after_tax'])-amount; risk_flags=clean_flags([calc.get('interest_rate_risk_flag'),calc.get('sell_before_maturity_flag')])
    else:
        calc=calculate_fund(amount,float(p.get('expected_return_pct',10) or 0),float(p.get('management_fee_pct',0.8) or 0),int(p.get('term_months',12) or 12),tax_pct,float(p.get('tracking_error_pct',0.5) or 0.5))
        expected,income=float(calc['final_after_tax']),float(calc['final_after_tax'])-amount; risk_flags=clean_flags([calc.get('tracking_error_note'),calc.get('liquidity_note'),'Оценка класса риска, а не расчёт конкретной акции.' if t=='Акция как класс риска' else None])
    return {'instrument_type':t,'explanation':'Инструмент имеет такие последствия при введённых параметрах.','expected_value':expected,'income_estimate':income,'stress_drawdown':float(p.get('stress_drawdown_pct',-20 if 'Акция' in t or 'Индексный' in t else -8)),'liquidity_label':liquidity_label,'risk_label':risk_label,'complexity_label':complexity_label,'risk_flags':risk_flags,'assumptions':p,'limitations':['Оценка основана на пользовательском вводе и упрощённых сценарных допущениях.'],'checklist':checklist}

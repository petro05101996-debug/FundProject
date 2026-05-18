from fastapi.testclient import TestClient
from backend.app.main import app


def test_scenario_analyze_real_payload():
    c=TestClient(app)
    payload={
      'assumptions':{'horizon_years':5,'inflation_pct':6,'default_tax_pct':13,'transaction_commission_pct':0.1,'rebalance_events_per_year':1,'fx_devaluation_pct':0},
      'constraints':{'max_single_position_pct':40,'max_asset_class_pct':80,'min_liquidity_pct_30d':60,'max_portfolio_volatility_pct':30,'max_fee_drag_pct':2,'max_stress_loss_pct':25},
      'positions':[
        {'scenario':'A','instrument':'Вклад','ticker':'D1','asset_class':'Денежные средства','country':'RU','currency':'RUB','market_value':200000,'expected_return_pct':8,'volatility_pct':1,'liquidity_days':1,'annual_fee_pct':0,'tax_pct':13},
        {'scenario':'A','instrument':'ОФЗ','ticker':'O1','asset_class':'Облигации','country':'RU','currency':'RUB','market_value':200000,'expected_return_pct':10,'volatility_pct':6,'liquidity_days':3,'annual_fee_pct':0.2,'tax_pct':13},
        {'scenario':'B','instrument':'Индексный фонд','ticker':'F1','asset_class':'Акции','country':'RU','currency':'RUB','market_value':200000,'expected_return_pct':14,'volatility_pct':18,'liquidity_days':2,'annual_fee_pct':1.1,'tax_pct':13},
      ]
    }
    j=c.post('/api/scenario/analyze',json=payload).json()
    assert 'summary' in j and 'stress' in j and 'flags' in j and 'asset_allocation' in j

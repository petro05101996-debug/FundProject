from fastapi.testclient import TestClient
from backend.app.main import app


def test_report_from_real_result():
    c=TestClient(app)
    payload={
      'assumptions':{'horizon_years':3,'inflation_pct':6,'default_tax_pct':13,'transaction_commission_pct':0.1,'rebalance_events_per_year':1,'fx_devaluation_pct':0},
      'constraints':{'max_single_position_pct':40,'max_asset_class_pct':80,'min_liquidity_pct_30d':60,'max_portfolio_volatility_pct':30,'max_fee_drag_pct':2,'max_stress_loss_pct':25},
      'positions':[
        {'scenario':'A','instrument':'Вклад','ticker':'D1','asset_class':'Денежные средства','country':'RU','currency':'RUB','market_value':200000,'expected_return_pct':8,'volatility_pct':1,'liquidity_days':1,'annual_fee_pct':0,'tax_pct':13},
        {'scenario':'B','instrument':'ОФЗ','ticker':'O1','asset_class':'Облигации','country':'RU','currency':'RUB','market_value':200000,'expected_return_pct':10,'volatility_pct':6,'liquidity_days':3,'annual_fee_pct':0.2,'tax_pct':13}
      ]
    }
    scenario=c.post('/api/scenario/analyze',json=payload).json()
    report=c.post('/api/report/build',json={'result':scenario}).json()
    assert report.get('html') and '<html' in report['html'].lower()
    assert report.get('sections') and len(report['sections'])>0

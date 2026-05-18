from fastapi.testclient import TestClient
from backend.app.main import app


def test_what_if_contract():
    c=TestClient(app)
    base_request={
      'assumptions':{'horizon_years':3,'inflation_pct':6,'default_tax_pct':13,'transaction_commission_pct':0.1,'rebalance_events_per_year':1,'fx_devaluation_pct':0},
      'constraints':{'max_single_position_pct':40,'max_asset_class_pct':80,'min_liquidity_pct_30d':60,'max_portfolio_volatility_pct':30,'max_fee_drag_pct':2,'max_stress_loss_pct':25},
      'positions':[{'scenario':'S1','instrument':'Вклад','ticker':'DEP','asset_class':'Денежные средства','country':'RU','currency':'RUB','market_value':100000,'expected_return_pct':8,'volatility_pct':1,'liquidity_days':1,'annual_fee_pct':0,'tax_pct':13},
                   {'scenario':'S2','instrument':'ОФЗ','ticker':'OFZ','asset_class':'Облигации','country':'RU','currency':'RUB','market_value':100000,'expected_return_pct':10,'volatility_pct':6,'liquidity_days':3,'annual_fee_pct':0.2,'tax_pct':13}]
    }
    what_if={'rate_delta_pct':1,'equity_market_shock_pct':-10,'inflation_pct':7,'early_exit':True,'deposit_share_pct':10,'ofz_share_pct':20,'fund_share_pct':30,'equity_share_pct':40}
    j=c.post('/api/scenario/what-if',json={'base_request':base_request,'what_if':what_if}).json()
    assert 'base_summary' in j and 'what_if_summary' in j and 'deltas' in j and 'risk_flags' in j

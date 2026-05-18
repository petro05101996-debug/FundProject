from fastapi.testclient import TestClient
from backend.app.main import app


def test_portfolio_check_real_payload():
    c=TestClient(app)
    positions=[
      {'scenario':'Портфель','instrument':'Вклад','ticker':'D1','asset_class':'Денежные средства','country':'RU','currency':'RUB','market_value':200000,'expected_return_pct':8,'volatility_pct':1,'liquidity_days':1,'annual_fee_pct':0,'tax_pct':13},
      {'scenario':'Портфель','instrument':'ОФЗ','ticker':'O1','asset_class':'Облигации','country':'RU','currency':'RUB','market_value':200000,'expected_return_pct':10,'volatility_pct':6,'liquidity_days':3,'annual_fee_pct':0.2,'tax_pct':13},
      {'scenario':'Портфель','instrument':'Индексный фонд','ticker':'F1','asset_class':'Акции','country':'RU','currency':'RUB','market_value':200000,'expected_return_pct':14,'volatility_pct':18,'liquidity_days':2,'annual_fee_pct':1.1,'tax_pct':13}
    ]
    j=c.post('/api/portfolio/check',json={'positions':positions}).json()
    assert 'allocation_by_asset_class' in j and 'concentration' in j and 'liquidity_30d' in j and 'weak_points' in j

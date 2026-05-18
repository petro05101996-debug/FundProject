from fastapi.testclient import TestClient
from backend.app.main import app


def test_portfolio_check_shape():
    c=TestClient(app)
    positions=[{'scenario':'Портфель','instrument':'ОФЗ','ticker':'OFZ','asset_class':'Облигации','country':'RU','currency':'RUB','market_value':1000000,'expected_return_pct':10,'volatility_pct':8,'liquidity_days':3,'annual_fee_pct':0.2,'tax_pct':13}]
    j=c.post('/api/portfolio/check',json={'positions':positions}).json()
    assert 'allocation_by_asset_class' in j
    assert 'concentration' in j

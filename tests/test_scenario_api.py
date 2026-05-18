from fastapi.testclient import TestClient
from backend.app.main import app

def test_scenario_analyze_response_shape():
    c=TestClient(app)
    payload={'assumptions':{},'constraints':{},'positions':[{'scenario':'S1','instrument':'Вклад','ticker':'D','asset_class':'Денежные средства','country':'RU','currency':'RUB','market_value':100000,'expected_return_pct':8,'volatility_pct':1,'liquidity_days':1,'annual_fee_pct':0,'tax_pct':13}]}
    j=c.post('/api/scenario/analyze',json=payload).json()
    assert 'summary' in j and 'flags' in j and 'stress' in j
    assert isinstance(j['summary'], list)

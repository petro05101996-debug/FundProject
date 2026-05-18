from fastapi.testclient import TestClient
from backend.app.main import app


def test_instrument_types_check():
    c=TestClient(app)
    types=['Вклад','Накопительный счёт','ОФЗ','Корпоративная облигация','Фонд денежного рынка','Облигационный фонд','Индексный фонд','Акция как класс риска']
    for t in types:
        r=c.post('/api/instrument/check',json={'selectedInstrumentType':t,'params':{'amount':1000000,'annual_rate_pct':10,'coupon_pct':10,'expected_return_pct':12}})
        assert r.status_code==200
        j=r.json()
        assert j['instrument_type']==t
        assert 'expected_value' in j

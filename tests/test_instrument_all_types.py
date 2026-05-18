from fastapi.testclient import TestClient
from backend.app.main import app


def test_instrument_all_types():
    c=TestClient(app)
    types=['Вклад','Накопительный счёт','ОФЗ','Корпоративная облигация','Фонд денежного рынка','Облигационный фонд','Индексный фонд','Акция как класс риска']
    banned=['рекомендуем купить','купите','продайте','держите','оптимальный портфель для вас']
    for t in types:
        j=c.post('/api/instrument/check',json={'selectedInstrumentType':t,'params':{'amount':100000,'annual_rate_pct':8,'term_months':12,'tax_pct':13}}).json()
        assert 'expected_value' in j and isinstance(j.get('risk_flags',[]),list)
        text=str(j).lower()
        for b in banned:
            assert b not in text

from fastapi.testclient import TestClient
from backend.app.main import app


def test_safety_wording_rules():
    c = TestClient(app)
    j = c.post('/api/instrument/check', json={'selectedInstrumentType': 'Вклад', 'params': {'amount': 100000, 'annual_rate_pct': 8, 'term_months': 12, 'tax_pct': 13}}).json()
    txt = str(j).lower()
    banned = ['рекомендуем купить', 'купите', 'продайте', 'держите', 'оптимальный портфель для вас']
    for w in banned:
        assert w not in txt

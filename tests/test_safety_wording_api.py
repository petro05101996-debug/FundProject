from fastapi.testclient import TestClient
from backend.app.main import app

BANNED=[
    'рекомендуем купить',
    'лучше купить',
    'продайте',
    'держите',
    'является инвестиционной рекомендацией',
    'оптимальный портфель для вас',
]

def test_wording_not_banned():
    c=TestClient(app)
    j=c.post('/api/instrument/check',json={'selectedInstrumentType':'Вклад','params':{'amount':100,'annual_rate_pct':5}}).json()
    text=str(j).lower()
    for w in BANNED:
        assert w not in text

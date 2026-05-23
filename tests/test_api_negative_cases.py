from fastapi.testclient import TestClient
from app.main import app


def test_instrument_check_rejects_zero_amount():
    c = TestClient(app)
    response = c.post('/api/instrument/check', json={
        'selectedInstrumentType': 'Вклад',
        'params': {'amount': 0}
    })
    assert response.status_code == 422
    assert 'detail' in response.json()


def test_instrument_check_rejects_unknown_type():
    c = TestClient(app)
    response = c.post('/api/instrument/check', json={
        'selectedInstrumentType': 'UNKNOWN',
        'params': {'amount': 1000}
    })
    assert response.status_code == 422

def test_instrument_check_rejects_non_numeric_stress_drawdown():
    c = TestClient(app)
    response = c.post('/api/instrument/check', json={
        'selectedInstrumentType': 'Индексный фонд',
        'params': {'amount': 1000, 'expected_return_pct': 10, 'management_fee_pct': 1, 'term_months': 12, 'stress_drawdown_pct': 'abc'}
    })
    assert response.status_code == 422


def test_portfolio_rejects_empty_positions():
    c = TestClient(app)
    response = c.post('/api/portfolio/check', json={'positions': []})
    assert response.status_code == 422


def test_portfolio_rejects_invalid_position():
    c = TestClient(app)
    response = c.post('/api/portfolio/check', json={'positions': [{'bad': 'x'}]})
    assert response.status_code == 422

def test_portfolio_rejects_invalid_values():
    c = TestClient(app)
    response = c.post('/api/portfolio/check', json={'positions': [{'name': '', 'asset_class': '', 'market_value': 'abc'}]})
    assert response.status_code == 422

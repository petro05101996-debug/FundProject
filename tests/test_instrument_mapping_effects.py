from fastapi.testclient import TestClient
from app.main import app


def test_nkd_changes_bond_result():
    c = TestClient(app)
    base = {
        'selectedInstrumentType': 'ОФЗ',
        'params': {
            'amount': 1000000,
            'clean_price_pct': 98.5,
            'nominal': 1000,
            'coupon_pct': 10,
            'years_to_maturity': 3,
            'coupon_period': 'Полугодовая',
            'commission_pct': 0.1,
            'tax_pct': 13,
        }
    }
    low = c.post('/api/instrument/check', json={**base, 'params': {**base['params'], 'nkd': 0}})
    high = c.post('/api/instrument/check', json={**base, 'params': {**base['params'], 'nkd': 150}})
    assert low.status_code == 200
    assert high.status_code == 200
    assert low.json()['expected_value'] != high.json()['expected_value']


def test_issuer_rating_changes_corporate_bond_result():
    c = TestClient(app)
    payload = {
        'selectedInstrumentType': 'Корпоративная облигация',
        'params': {
            'amount': 1000000,
            'clean_price_pct': 95,
            'nominal': 1000,
            'coupon_pct': 12,
            'years_to_maturity': 3,
            'coupon_period': 'Полугодовая',
            'commission_pct': 0.3,
            'tax_pct': 13,
            'nkd': 0,
        }
    }
    safer = c.post('/api/instrument/check', json={**payload, 'params': {**payload['params'], 'issuer_rating': 'AA'}})
    riskier = c.post('/api/instrument/check', json={**payload, 'params': {**payload['params'], 'issuer_rating': 'BB'}})
    assert safer.status_code == 200
    assert riskier.status_code == 200
    assert safer.json()['expected_value'] != riskier.json()['expected_value']

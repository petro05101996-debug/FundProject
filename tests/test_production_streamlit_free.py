from pathlib import Path


def test_production_code_has_no_streamlit_imports():
    roots = [Path('backend'), Path('investment_lab')]
    for root in roots:
        for path in root.rglob('*.py'):
            text = path.read_text(encoding='utf-8')
            assert 'import streamlit' not in text
            assert 'from streamlit' not in text


def test_catalog_endpoint_smoke():
    from fastapi.testclient import TestClient
    from backend.app.main import app

    c = TestClient(app)
    r = c.get('/api/instruments/catalog')
    assert r.status_code == 200
    j = r.json()
    assert 'items' in j
    assert isinstance(j['items'], list)

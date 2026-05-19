from pathlib import Path


def test_production_code_has_no_streamlit_imports():
    roots = [Path("backend"), Path("investment_lab")]
    for root in roots:
        for path in root.rglob("*.py"):
            text = path.read_text(encoding="utf-8")
            assert "import streamlit" not in text
            assert "from streamlit" not in text


def test_production_artifacts_are_streamlit_free():
    dockerfile = Path("Dockerfile").read_text(encoding="utf-8").lower()
    supervisord = Path("deploy/supervisord.conf").read_text(encoding="utf-8").lower()
    backend_requirements = Path("backend/requirements.txt").read_text(encoding="utf-8").lower()
    deploy_notes = Path("deploy-notes.md").read_text(encoding="utf-8").lower()
    readme = Path("README.md").read_text(encoding="utf-8").lower()

    assert "streamlit" not in dockerfile
    assert "streamlit" not in supervisord
    assert "streamlit" not in backend_requirements
    assert "_stcore" not in deploy_notes
    assert "streamlit app" not in deploy_notes
    assert "streamlit app" not in readme

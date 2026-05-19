# FundProject

## Production architecture

FundProject now runs in production as:

- **React/Vite frontend** (served by nginx)
- **FastAPI backend** (`/api/*`, `/health`)
- **investment_lab engine/domain/data** for calculations

Streamlit is no longer part of the production runtime. The previous Streamlit UI is moved to `legacy_streamlit/` only for historical comparison.

## Module structure

```text
backend/                  # FastAPI app and API routes
frontend/                 # React/Vite UI
investment_lab/           # domain/data/engine/models (calculation core)
legacy_streamlit/         # old Streamlit UI (not used in production)
deploy/nginx.conf
deploy/supervisord.conf
Dockerfile
```

## Run with Docker

```bash
docker build -t fundproject .
docker run --rm -p 8501:8501 fundproject
```

Open: <http://localhost:8501>

Healthcheck: <http://localhost:8501/health>

## Tests

```bash
pytest -q
```

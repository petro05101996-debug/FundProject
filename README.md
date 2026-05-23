# FundProject

## Production architecture

FundProject now runs in production as:

- **React/Vite frontend** (served by nginx)
- **FastAPI backend** (`/api/*`, `/health`)
- **investment_lab engine/domain/data** for calculations

Streamlit is no longer part of the production runtime. The previous Streamlit UI is moved to `archived_streamlit_reference/` only for historical comparison.

## Production runtime

Production runtime uses:

- React/Vite static frontend
- FastAPI backend
- nginx reverse proxy
- supervisor
- port 8080
- healthcheck endpoint `/health`

Streamlit is not used as production runtime.
Old Streamlit files, if present, are legacy/archive only.

## Module structure

```text
backend/                  # FastAPI app and API routes
frontend/                 # React/Vite UI
investment_lab/           # domain/data/engine/models (calculation core)
archived_streamlit_reference/ # archived old Streamlit UI (not used in production)
deploy/nginx.conf
deploy/supervisord.conf
Dockerfile
```

## Run with Docker

```bash
docker build -t fundproject .
docker run --rm -p 8080:8080 fundproject
```

Open: <http://localhost:8080>

Healthcheck: <http://localhost:8080/health>

## Tests

```bash
pytest -q
```

# Production deployment notes

FundProject production deployment does not use Streamlit runtime components.

## Runtime

Production runtime stack:

- nginx (serves React/Vite static frontend and reverse-proxies backend API)
- FastAPI backend (uvicorn)
- React/Vite frontend build artifacts

## Network settings

- Protocol: HTTP
- Port: 8080
- Healthcheck path: `/health`

## Process model

Container entrypoint is supervisor, which runs only:

1. `uvicorn app.main:app` on `127.0.0.1:8000`
2. `nginx` on external port `8080`

No Streamlit process is started in production.

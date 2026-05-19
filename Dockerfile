FROM node:20-slim AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1 PIP_DISABLE_PIP_VERSION_CHECK=1 PORT=8080
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends nginx supervisor curl && rm -rf /var/lib/apt/lists/*
COPY backend/requirements.txt /app/backend/requirements.txt
RUN python -m pip install --upgrade pip setuptools wheel && pip install --no-cache-dir -r /app/backend/requirements.txt
COPY backend/ /app/backend/
COPY investment_lab/ /app/investment_lab/
COPY --from=frontend-builder /app/frontend/dist /app/frontend_dist
COPY deploy/nginx.conf /etc/nginx/nginx.conf
COPY deploy/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=10s --start-period=45s --retries=3 CMD curl -f http://127.0.0.1:8080/health || exit 1
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]

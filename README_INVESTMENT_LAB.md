# Investment Scenario Lab

## Что это

Investment Scenario Lab — модуль сценарного анализа пользовательских финансовых вариантов.

В production используется связка **React/Vite UI + FastAPI API + investment_lab engine**.

## Legacy Streamlit

Старый Streamlit UI сохранён в `legacy_streamlit/` только для исторической сверки поведения. Он не используется в production Docker/runtime.

## Структура

```text
investment_lab/
  domain/      # enums, dataclasses, statuses
  data/        # legal texts, catalog, templates, knowledge base
  engine/      # validation, calculators, stress, flags, report builder
  models.py

backend/       # FastAPI endpoints
frontend/      # React pages
legacy_streamlit/ # old streamlit app/router/ui
```

## Docker / Timeweb

```bash
docker build -t fundproject .
docker run --rm -p 8080:8080 fundproject
```

- UI: `http://localhost:8080/`
- Health: `http://localhost:8080/health`


> Streamlit UI находится только в `archived_streamlit_reference/` и не используется в production runtime.

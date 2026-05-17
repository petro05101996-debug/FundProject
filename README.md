# FundProject

## Investment Scenario Lab

Investment Scenario Lab is an isolated Streamlit product module for comparing user-defined financial scenarios.
It does not fetch market data, execute trades, provide brokerage services, or issue individual investment recommendations.

### Module structure

```text
investment_lab/
  router.py
  domain/                # dataclasses, statuses, input schema
  data/                  # approved legal text, templates, educational content
  engine/                # scenario comparison engine and safety text guard
  ui/                    # dark app shell, components, charts
    pages/               # landing, profile, instrument, scenario, portfolio, results, report, explain
```

### Run locally

```bash
streamlit run app.py --server.address=0.0.0.0 --server.port=8501
```

### Docker

```bash
docker build -t fundproject .
docker run --rm -p 8501:8501 fundproject
```

### Tests

```bash
pytest -q
```

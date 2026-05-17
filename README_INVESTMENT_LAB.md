# Investment Scenario Lab

## Что это

Investment Scenario Lab — отдельный Streamlit-раздел для сценарного анализа пользовательских финансовых вариантов. Пользователь сам вводит параметры, инструменты, портфель и ограничения; сервис сравнивает только эти данные.

## Что не делает

- Не является брокером.
- Не исполняет сделки.
- Не хранит брокерские поручения.
- Не выдаёт индивидуальные инвестиционные рекомендации.
- Не подбирает инструменты вместо пользователя.

## Как запустить

```bash
streamlit run app.py --server.address=0.0.0.0 --server.port=8501
```

## Структура

```text
investment_lab/
  router.py
  domain/      # enums, dataclasses, statuses
  data/        # legal texts, catalog, templates, knowledge base
  engine/      # validation, calculators, stress, flags, report builder
  ui/          # styles, layout, components, charts, pages
```

## Как работает расчёт

1. Нормализуются пользовательские инструменты.
2. Считаются веса, комиссии, налоги, ликвидность, риск и сложность.
3. Проверяются пользовательские ограничения.
4. Формируются risk flags с кодами и severity.
5. Строятся стресс-сценарии и денежные потоки.
6. Report builder собирает HTML-отчёт.

## Допущения

Расчёт использует только пользовательские значения. Рыночные котировки, брокерские данные и персональные рекомендации не используются.

## Тесты

```bash
python -m compileall .
pytest -q
```

## Ручная проверка UI

1. Открыть лендинг.
2. Задать параметры сценария.
3. Проверить инструмент ОФЗ.
4. Добавить сценарии и рассчитать.
5. Проверить портфель.
6. Сформировать HTML-отчёт.
7. Проверить, что все пользовательские тексты на русском и нет advisory wording.

## Safety

Safety guard находится в `investment_lab/engine/safety_text_guard.py`. UI scan тестирует страницы, legal texts и report builder.

## Docker / Timeweb

```bash
docker build -t investment-scenario-lab .
docker run --rm -p 8501:8501 investment-scenario-lab
```

Dockerfile использует `python:3.11-slim`, headless Streamlit и порт `8501`.

"""Report data and HTML export builder for Investment Scenario Lab."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from html import escape
from uuid import uuid4

try:
    import pandas as pd
except ModuleNotFoundError:  # pragma: no cover - runtime dependency in app image
    pd = None

from investment_lab.data.legal_texts import PRIMARY_DISCLAIMER, REPORT_CHECKLIST


@dataclass(frozen=True)
class ReportBundle:
    report_id: str
    created_at: str
    sections: list[str]
    result: dict


def build_report_bundle(result: dict) -> ReportBundle:
    return ReportBundle(
        report_id=f"ISL-{uuid4().hex[:10].upper()}",
        created_at=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        sections=[
            "Дисклеймер",
            "Параметры пользователя",
            "Выбранные сценарии",
            "Сравнение сценариев",
            "Риск-флаги",
            "Стресс-сценарии",
            "Денежные потоки",
            "Расчётные допущения",
            "Ограничения анализа",
            "Чек-лист",
        ],
        result=result,
    )


def build_cashflow_table(summary, horizon_years: int):
    rows = []
    if summary is None:
        return _dataframe(rows)
    for _, row in summary.iterrows():
        previous_value = float(row["portfolio_value"])
        stress_multiplier = 1 + float(row.get("worst_stress_impact_pct", 0)) / 100
        for year in range(horizon_years + 1):
            value_before_stress = float(row["portfolio_value"]) * (1 + float(row["net_return_pct"]) / 100) ** year
            income = max(value_before_stress - previous_value, 0) if year else 0.0
            fees = value_before_stress * float(row.get("fee_and_commission_drag_pct", 0)) / 100 if year else 0.0
            taxes = value_before_stress * float(row.get("tax_drag_pct", 0)) / 100 if year else 0.0
            rows.append({
                "scenario": row["scenario"],
                "year": year,
                "contributions": float(row["portfolio_value"]) if year == 0 else 0.0,
                "additional_contributions": 0.0,
                "income": income,
                "fees": fees,
                "taxes": taxes,
                "value_before_stress": value_before_stress,
                "value_after_stress": value_before_stress * stress_multiplier,
            })
            previous_value = value_before_stress
    return _dataframe(rows)


def export_html_report(result: dict) -> str:
    bundle = build_report_bundle(result)
    constraints_html = _dict_to_html(result.get("constraints", {}))
    assumptions_html = _dict_to_html(result.get("assumptions", {}))
    positions_html = _table_to_html(result.get("positions"))
    summary_html = _table_to_html(result.get("summary"))
    flags_html = _table_to_html(result.get("flags"))
    stress_html = _table_to_html(result.get("stress"))
    cashflows_html = _table_to_html(build_cashflow_table(result.get("summary"), int(result.get("assumptions", {}).get("horizon_years", 5))))
    limitations = "".join(f"<li>{escape(str(item))}</li>" for item in result.get("limitations", []))
    checklist = "".join(f"<li>☐ {escape(item)}</li>" for item in REPORT_CHECKLIST)
    return f"""<!doctype html>
<html lang='ru'>
<head><meta charset='utf-8'><title>Investment Scenario Lab — отчёт</title>
<style>body{{font-family:Inter,Arial,sans-serif;background:#f8fafc;color:#0f172a;padding:32px}}section{{background:#fff;border:1px solid #e2e8f0;border-radius:18px;padding:20px;margin:16px 0;break-inside:avoid}}table{{border-collapse:collapse;width:100%;font-size:13px}}td,th{{border:1px solid #e2e8f0;padding:8px;text-align:left}}th{{background:#f1f5f9}}.muted{{color:#64748b}}</style></head>
<body>
<h1>Investment Scenario Lab — аналитический отчёт</h1>
<p class='muted'>ID: {escape(bundle.report_id)} • Дата: {escape(bundle.created_at)}</p>
<section><h2>1. Дисклеймер</h2><p>{escape(PRIMARY_DISCLAIMER)}</p></section>
<section><h2>2. Параметры пользователя</h2>{constraints_html}</section>
<section><h2>3. Выбранные сценарии</h2>{positions_html}</section>
<section><h2>4. Сравнение сценариев</h2>{summary_html}</section>
<section><h2>5. Риск-флаги</h2>{flags_html}</section>
<section><h2>6. Стресс-сценарии</h2>{stress_html}</section>
<section><h2>7. Денежные потоки</h2>{cashflows_html}</section>
<section><h2>8. Расчётные допущения</h2>{assumptions_html}</section>
<section><h2>9. Ограничения анализа</h2><ul>{limitations}</ul></section>
<section><h2>10. Чек-лист</h2><ul>{checklist}</ul></section>
</body></html>"""


def _table_to_html(table) -> str:
    if table is None:
        return "<p>Данные отсутствуют.</p>"
    if hasattr(table, "to_html"):
        return table.to_html(index=False, escape=True)
    return _dict_to_html({"Значение": table})


def _dict_to_html(data: dict) -> str:
    rows = "".join(f"<tr><th>{escape(str(key))}</th><td>{escape(str(value))}</td></tr>" for key, value in data.items())
    return f"<table><tbody>{rows}</tbody></table>"


def _dataframe(rows: list[dict]):
    if pd is None:
        return rows
    return pd.DataFrame(rows)

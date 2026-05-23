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

REPORT_SECTIONS = [
    "Дисклеймер",
    "Executive summary",
    "Риск-паспорт",
    "Параметры пользователя",
    "Расчётные допущения",
    "Выбранные сценарии",
    "Сравнение сценариев",
    "Риск-флаги",
    "Стресс-сценарии",
    "Денежные потоки",
    "Ограничения анализа",
    "Чек-лист",
]


@dataclass(frozen=True)
class ReportBundle:
    report_id: str
    created_at: str
    sections: list[str]
    result: dict


def build_report_bundle(result: dict) -> ReportBundle:
    result = result or {}
    return ReportBundle(
        report_id=f"ISL-{uuid4().hex[:10].upper()}",
        created_at=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        sections=REPORT_SECTIONS,
        result=result,
    )


def build_cashflow_table(summary, horizon_years: int):
    summary = _ensure_dataframe(summary)
    rows = []
    if summary is None or not hasattr(summary, "iterrows"):
        return _dataframe(rows)
    for _, row in summary.iterrows():
        portfolio_value = float(row.get("portfolio_value", 0) or 0)
        net_return = float(row.get("net_return_pct", 0) or 0)
        scenario = row.get("scenario", "Сценарий")
        previous_value = portfolio_value
        stress_multiplier = 1 + float(row.get("worst_stress_impact_pct", 0)) / 100
        for year in range(horizon_years + 1):
            value_before_stress = portfolio_value * (1 + net_return / 100) ** year
            income = max(value_before_stress - previous_value, 0) if year else 0.0
            fees = value_before_stress * float(row.get("fee_and_commission_drag_pct", 0)) / 100 if year else 0.0
            taxes = value_before_stress * float(row.get("tax_drag_pct", 0)) / 100 if year else 0.0
            rows.append({
                "scenario": scenario,
                "year": year,
                "contributions": portfolio_value if year == 0 else 0.0,
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
    return export_html_report_from_bundle(build_report_bundle(result or {}))


def export_html_report_from_bundle(bundle: ReportBundle) -> str:
    result = bundle.result or {}
    constraints_html = _dict_to_html(result.get("constraints", {}))
    assumptions_html = _dict_to_html(result.get("assumptions", {}))
    positions_html = _table_to_html(result.get("positions"))
    summary = _safe_get_table(result, "summary")
    summary_html = _table_to_html(user_summary_table(summary))
    flags = _safe_get_table(result, "flags")
    flags_html = _table_to_html(flags)
    stress_html = _table_to_html(_safe_get_table(result, "stress"))
    cashflows = build_cashflow_table(summary, int(result.get("assumptions", {}).get("horizon_years", 5)))
    cashflows_html = _table_to_html(user_cashflow_table(cashflows))
    limitations = "".join(f"<li>{escape(str(item))}</li>" for item in result.get("limitations", []))
    checklist = "".join(f"<li>☐ {escape(item)}</li>" for item in REPORT_CHECKLIST)
    executive_html = _executive_summary_html(bundle, summary, flags)
    risk_passport_html = _risk_passport_html(summary)
    return f"""<!doctype html>
<html lang='ru'>
<head><meta charset='utf-8'><title>Investment Scenario Lab — отчёт</title>
<style>body{{font-family:Inter,Arial,sans-serif;background:#f8fafc;color:#0f172a;padding:32px;max-width:1180px;margin:auto}}section{{background:#fff;border:1px solid #e2e8f0;border-radius:18px;padding:20px;margin:16px 0;break-inside:avoid;box-shadow:0 12px 30px rgba(15,23,42,.06)}}table{{border-collapse:collapse;width:100%;font-size:13px}}td,th{{border:1px solid #e2e8f0;padding:8px;text-align:left}}th{{background:#f1f5f9}}.muted{{color:#64748b}}.kpis{{display:grid;grid-template-columns:repeat(5,1fr);gap:12px}}.kpi{{border:1px solid #dbeafe;border-radius:14px;padding:12px;background:#f8fafc}}.chip{{display:inline-block;border-radius:999px;padding:6px 10px;margin:4px;background:#e0f2fe;color:#075985;font-size:12px}}</style></head>
<body>
<h1>Investment Scenario Lab — аналитический отчёт</h1>
<p class='muted'>ID: {escape(bundle.report_id)} • Дата: {escape(bundle.created_at)}</p>
<section><h2>1. Дисклеймер</h2><p>{escape(PRIMARY_DISCLAIMER)}</p></section>
<section><h2>2. Executive summary</h2>{executive_html}</section>
<section><h2>3. Риск-паспорт</h2>{risk_passport_html}</section>
<section><h2>4. Параметры пользователя</h2>{constraints_html}</section>
<section><h2>5. Расчётные допущения</h2>{assumptions_html}</section>
<section><h2>6. Выбранные сценарии</h2>{positions_html}</section>
<section><h2>7. Сравнение сценариев</h2>{summary_html}</section>
<section><h2>8. Риск-флаги</h2>{flags_html}</section>
<section><h2>9. Стресс-сценарии</h2>{stress_html}</section>
<section><h2>10. Денежные потоки</h2>{cashflows_html}</section>
<section><h2>11. Ограничения анализа</h2><ul>{limitations}</ul></section>
<section><h2>12. Чек-лист</h2><ul>{checklist}</ul></section>
<footer class='muted'>{escape(PRIMARY_DISCLAIMER)}</footer>
</body></html>"""


def user_summary_table(summary):
    if summary is None or not hasattr(summary, "empty") or summary.empty:
        return summary
    columns = {
        "scenario": "Сценарий",
        "projected_value": "Базовая стоимость",
        "stress_value": "Стоимость после стресса",
        "liquidity_label": "Ликвидность",
        "risk_label": "Риск",
        "complexity_label": "Сложность",
        "max_position_pct": "Концентрация, %",
        "status": "Статус по ограничениям",
    }
    existing = [column for column in columns if column in summary.columns]
    if not existing:
        message = "Нет пользовательских колонок для отображения сравнения сценариев."
        if pd is None:
            return [{"Комментарий": message}]
        return pd.DataFrame([{"Комментарий": message}])
    return summary[existing].rename(columns=columns).round(2)


def user_cashflow_table(cashflows):
    if cashflows is None or not hasattr(cashflows, "empty") or cashflows.empty:
        return cashflows
    columns = {
        "scenario": "Сценарий",
        "year": "Год",
        "contributions": "Начальная сумма",
        "additional_contributions": "Доп. взносы",
        "income": "Расчётный доход",
        "fees": "Комиссии",
        "taxes": "Налоги",
        "value_before_stress": "Стоимость до стресса",
        "value_after_stress": "Стоимость после стресса",
    }
    existing = [column for column in columns if column in cashflows.columns]
    if not existing:
        return cashflows
    return cashflows[existing].rename(columns=columns).round(2)


def _executive_summary_html(bundle: ReportBundle, summary, flags) -> str:
    if summary is None or not hasattr(summary, "empty") or summary.empty:
        return "<p>Данные отсутствуют.</p>"
    summary_sorted = _sort_summary_by_fit(summary)
    row = summary_sorted.iloc[0]
    chips = _risk_flag_chips_html(flags)
    return (
        f"<p><strong>Дата:</strong> {escape(bundle.created_at)} • <strong>ID:</strong> {escape(bundle.report_id)}</p>"
        f"<p><strong>Сценарий с максимальным соответствием ограничениям:</strong> {escape(str(row.get('scenario', '—')))}</p>"
        f"<ul><li>Ликвидность до 30 дней: {float(row.get('liquid_within_30d_pct', 0)):.1f}%</li>"
        f"<li>Стресс-просадка: {float(row.get('worst_stress_impact_pct', 0)):.1f}%</li>"
        f"<li>Концентрация: {float(row.get('max_position_pct', 0)):.1f}%</li></ul>"
        f"<p><strong>Главные риск-флаги:</strong><br>{chips}</p>"
        f"<p class='muted'>{escape(PRIMARY_DISCLAIMER)}</p>"
    )


def _risk_flag_chips_html(flags) -> str:
    if flags is None or not hasattr(flags, "empty") or flags.empty:
        return "<span class='chip'>Критичные риск-флаги не выявлены по текущим правилам</span>"
    if "title" in flags.columns:
        values = [escape(str(value)) for value in flags["title"].head(3)]
    elif "description" in flags.columns:
        values = [escape(str(value)) for value in flags["description"].head(3)]
    else:
        return "<span class='chip'>Есть риск-флаги, но их структура не распознана в отчёте</span>"
    return "".join(f"<span class='chip'>{value}</span>" for value in values)


def _user_summary_table(summary):
    return user_summary_table(summary)


def _risk_passport_html(summary) -> str:
    if summary is None or not hasattr(summary, "empty") or summary.empty:
        return "<p>Данные отсутствуют.</p>"
    summary_sorted = _sort_summary_by_fit(summary)
    row = summary_sorted.iloc[0]
    items = [
        ("Риск", row.get("risk_label", "—")),
        ("Ликвидность", row.get("liquidity_label", "—")),
        ("Сложность", row.get("complexity_label", "—")),
        ("Концентрация", f"{float(row.get('max_position_pct', 0)):.1f}%"),
        ("Стресс-просадка", f"{float(row.get('worst_stress_impact_pct', 0)):.1f}%"),
    ]
    return "<div class='kpis'>" + "".join(f"<div class='kpi'><div class='muted'>{escape(label)}</div><strong>{escape(str(value))}</strong></div>" for label, value in items) + "</div>"


def _sort_summary_by_fit(summary):
    if summary is None or not hasattr(summary, "empty") or summary.empty or "constraint_fit_score" not in summary.columns:
        return summary
    return summary.sort_values("constraint_fit_score", ascending=False).reset_index(drop=True)


def _table_to_html(table) -> str:
    table = _ensure_dataframe(table)
    if table is None or (hasattr(table, "empty") and table.empty):
        return "<p>Данные отсутствуют.</p>"
    if hasattr(table, "to_html"):
        return table.to_html(index=False, escape=True)
    return _dict_to_html({"Значение": table})


def _dict_to_html(data: dict) -> str:
    rows = "".join(f"<tr><th>{escape(str(key))}</th><td>{_value_to_html(value)}</td></tr>" for key, value in data.items())
    return f"<table><tbody>{rows}</tbody></table>"


def _value_to_html(value) -> str:
    if isinstance(value, dict):
        return _dict_to_html(value)
    if isinstance(value, list):
        items = "".join(f"<li>{escape(str(item))}</li>" for item in value)
        return f"<ul>{items}</ul>"
    return escape(str(value))


def _dataframe(rows: list[dict]):
    if pd is None:
        return rows
    return pd.DataFrame(rows)


def _ensure_dataframe(value):
    if value is None:
        return _dataframe([])
    if pd is not None and isinstance(value, pd.DataFrame):
        return value
    if isinstance(value, list):
        return _dataframe(value)
    if isinstance(value, dict):
        return _dataframe([value])
    return _dataframe([{"value": value}])


def _ensure_records(value):
    if value is None:
        return []
    if pd is not None and isinstance(value, pd.DataFrame):
        return value.to_dict(orient="records")
    if isinstance(value, list):
        return [item for item in value if isinstance(item, dict)]
    if isinstance(value, dict):
        return [value]
    return []


def _safe_get_table(result: dict, key: str):
    return _ensure_dataframe((result or {}).get(key))

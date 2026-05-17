from __future__ import annotations

from html import escape

import pandas as pd
import streamlit as st

from investment_lab.data.legal_texts import REPORT_DISCLAIMER
from investment_lab.engine.report_builder import build_cashflow_table, build_report_bundle, export_html_report, user_cashflow_table, user_summary_table
from investment_lab.engine.scenario_comparator import analyze_scenarios
from investment_lab.ui.charts import cashflow_donut, stress_bar
from investment_lab.ui.components import empty_state, table_card


def render() -> None:
    result = st.session_state.get("investment_lab_results") or analyze_scenarios(pd.DataFrame(st.session_state["investment_lab_scenarios"]), st.session_state["investment_lab_assumptions"], st.session_state["investment_lab_constraints"])
    st.session_state["investment_lab_results"] = result
    if result["summary"].empty:
        empty_state("Отчёт ещё не сформирован", "Сначала выполните анализ сценариев")
        return

    bundle = build_report_bundle(result)
    html_report = export_html_report(result)
    cashflows = build_cashflow_table(result["summary"], int(result["assumptions"]["horizon_years"]))

    st.markdown("## Аналитический отчёт")
    a, b = st.columns([1, 1])
    with a: st.download_button("Экспорт HTML", data=html_report.encode("utf-8"), file_name=f"{bundle.report_id}.html", mime="text/html", use_container_width=True)
    with b: st.markdown("<div class='lab-panel'>PDF-экспорт будет добавлен после MVP-проверки</div>", unsafe_allow_html=True)

    st.markdown("<div class='lab-report-layout'>", unsafe_allow_html=True)
    left, right = st.columns([.28, .72])
    with left:
        st.markdown("<div class='lab-panel'><h3>Содержание</h3>", unsafe_allow_html=True)
        for idx, section in enumerate(bundle.sections, start=1):
            st.markdown(f"{idx}. {section}")
        st.markdown("</div>", unsafe_allow_html=True)
    with right:
        st.markdown("<div class='lab-report-canvas'>", unsafe_allow_html=True)
        st.markdown(f"# Investment Scenario Lab — аналитический отчёт\n**Дата:** {bundle.created_at}  \n**ID отчёта:** {bundle.report_id}")
        st.markdown(f"<div class='lab-report-section'><h2>1. Дисклеймер</h2><p>{REPORT_DISCLAIMER}</p></div>", unsafe_allow_html=True)
        st.markdown(_executive_summary_section(bundle, result), unsafe_allow_html=True)
        table_card("3. Риск-паспорт", _risk_passport_table(result["summary"]))
        table_card("4. Параметры пользователя", _dict_table(result["constraints"]))
        table_card("5. Расчётные допущения", _dict_table(result["assumptions"]))
        table_card("6. Выбранные сценарии", result["positions"].round(2))
        table_card("7. Сравнение сценариев", user_summary_table(result["summary"]))
        table_card("8. Риск-флаги", result["flags"])
        table_card("9. Стресс-сценарии", result["stress"].round(2))
        st.plotly_chart(stress_bar(result["stress"]), use_container_width=True)
        table_card("10. Денежные потоки", user_cashflow_table(cashflows))
        st.plotly_chart(cashflow_donut(cashflows), use_container_width=True)
        st.markdown("<div class='lab-report-section'><h2>11. Ограничения анализа</h2>", unsafe_allow_html=True)
        for item in result["limitations"]: st.markdown(f"- {item}")
        st.markdown("<h2>12. Чек-лист</h2><ul><li>☐ Проверить введённые сценарии.</li><li>☐ Сверить комиссии и налоги.</li><li>☐ Посмотреть стресс-сценарии.</li></ul></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


def _dict_table(data: dict) -> pd.DataFrame:
    return pd.DataFrame([{"Параметр": key, "Значение": value} for key, value in data.items()])


def _sorted_summary(summary: pd.DataFrame) -> pd.DataFrame:
    if summary.empty or "constraint_fit_score" not in summary.columns:
        return summary
    return summary.sort_values("constraint_fit_score", ascending=False).reset_index(drop=True)


def _executive_summary_section(bundle, result: dict) -> str:
    summary = _sorted_summary(result["summary"])
    if summary.empty:
        return "<div class='lab-report-section'><h2>2. Executive summary</h2><p>Данные отсутствуют.</p></div>"
    leader = summary.iloc[0]
    flag_items = _flag_items_html(result.get("flags"))
    return (
        "<div class='lab-report-section'><h2>2. Executive summary</h2>"
        f"<p><strong>Дата:</strong> {escape(str(bundle.created_at))} • <strong>ID отчёта:</strong> {escape(str(bundle.report_id))}</p>"
        f"<p><strong>Сценарий с максимальным соответствием ограничениям:</strong> {escape(str(leader.get('scenario', '—')))}</p>"
        "<ul>"
        f"<li>Ликвидность до 30 дней: {_safe_float(leader.get('liquid_within_30d_pct', 0)):.1f}%</li>"
        f"<li>Стресс-просадка: {_safe_float(leader.get('worst_stress_impact_pct', 0)):.1f}%</li>"
        f"<li>Концентрация: {_safe_float(leader.get('max_position_pct', 0)):.1f}%</li>"
        "</ul>"
        f"<p><strong>Главные риск-флаги:</strong></p><ul>{flag_items}</ul>"
        f"<p>{escape(REPORT_DISCLAIMER)}</p></div>"
    )


def _flag_items_html(flags) -> str:
    if flags is None or not hasattr(flags, "empty") or flags.empty:
        return "<li>Критичные риск-флаги не выявлены по текущим правилам.</li>"
    if "title" in flags.columns:
        values = flags["title"].head(3)
    elif "description" in flags.columns:
        values = flags["description"].head(3)
    else:
        return "<li>Есть риск-флаги, но их структура не распознана в отчёте.</li>"
    return "".join(f"<li>{escape(str(value))}</li>" for value in values)


def _safe_float(value) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def _risk_passport_table(summary: pd.DataFrame) -> pd.DataFrame:
    summary = _sorted_summary(summary)
    if summary.empty:
        return pd.DataFrame(columns=["Метрика", "Значение"])
    leader = summary.iloc[0]
    return pd.DataFrame([
        {"Метрика": "Риск", "Значение": leader.get("risk_label", "—")},
        {"Метрика": "Ликвидность", "Значение": leader.get("liquidity_label", "—")},
        {"Метрика": "Сложность", "Значение": leader.get("complexity_label", "—")},
        {"Метрика": "Концентрация", "Значение": f"{float(leader.get('max_position_pct', 0)):.1f}%"},
        {"Метрика": "Стресс-просадка", "Значение": f"{float(leader.get('worst_stress_impact_pct', 0)):.1f}%"},
    ])

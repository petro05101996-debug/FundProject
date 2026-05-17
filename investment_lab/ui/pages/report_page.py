from __future__ import annotations

import pandas as pd
import streamlit as st

from investment_lab.data.legal_texts import REPORT_DISCLAIMER
from investment_lab.engine.report_builder import build_cashflow_table, build_report_bundle, export_html_report
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
    with b: st.markdown("<div class='lab-panel'>PDF-экспорт не включён в MVP</div>", unsafe_allow_html=True)

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
        table_card("2. Параметры пользователя", _dict_table(result["constraints"]))
        table_card("3. Расчётные допущения", _dict_table(result["assumptions"]))
        table_card("4. Выбранные сценарии", result["positions"].round(2))
        table_card("5. Сравнение сценариев", result["summary"].round(2))
        table_card("6. Риск-флаги", result["flags"])
        table_card("7. Стресс-сценарии", result["stress"].round(2))
        st.plotly_chart(stress_bar(result["stress"]), use_container_width=True)
        table_card("8. Денежные потоки", cashflows.round(2) if hasattr(cashflows, "round") else cashflows)
        st.plotly_chart(cashflow_donut(cashflows), use_container_width=True)
        st.markdown("<div class='lab-report-section'><h2>9. Ограничения анализа</h2>", unsafe_allow_html=True)
        for item in result["limitations"]: st.markdown(f"- {item}")
        st.markdown("<h2>10. Чек-лист</h2><ul><li>☐ Проверить введённые сценарии.</li><li>☐ Сверить комиссии и налоги.</li><li>☐ Посмотреть стресс-сценарии.</li></ul></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


def _dict_table(data: dict) -> pd.DataFrame:
    return pd.DataFrame([{"Параметр": key, "Значение": value} for key, value in data.items()])

from __future__ import annotations

import pandas as pd
import streamlit as st

from investment_lab.data.legal_texts import REPORT_CHECKLIST, REPORT_DISCLAIMER, SHORT_DISCLAIMER
from investment_lab.engine.scenario_comparator import analyze_scenarios
from investment_lab.ui.charts import drawdown_chart, portfolio_allocation_donut, risk_bar_chart, scenario_projection_chart, scenario_score_bar, stress_bar
from investment_lab.ui.components import disclaimer, empty_state, kpi_card, risk_chips, table_card
from investment_lab.ui.layout import go_to


def render() -> None:
    top_left, top_right = st.columns([1.5, .6])
    with top_left:
        st.markdown("## Итог по выбранным пользователем сценариям")
    with top_right:
        if st.button("Сформировать аналитический отчёт", type="primary", use_container_width=True):
            st.session_state["investment_lab_report_ready"] = True
            go_to("Аналитический отчёт")
    disclaimer(SHORT_DISCLAIMER)
    result = st.session_state.get("investment_lab_results") or analyze_scenarios(pd.DataFrame(st.session_state["investment_lab_scenarios"]), st.session_state["investment_lab_assumptions"], st.session_state["investment_lab_constraints"])
    st.session_state["investment_lab_results"] = result
    if result["summary"].empty:
        empty_state("Расчёт ещё не выполнен", "Заполните параметры и нажмите “Рассчитать”", "Перейдите в раздел сравнения сценариев или проверки портфеля.")
        return

    leader = result["summary"].iloc[0]
    st.markdown(f"<div class='lab-panel lab-card-strong'><h3>Сценарий «{leader['scenario']}» лучше соответствует заданным пользователем ограничениям по ликвидности и допустимой просадке среди выбранных сценариев.</h3><p>{REPORT_DISCLAIMER}</p></div>", unsafe_allow_html=True)

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    with c1: kpi_card("Базовый результат", f"{leader['projected_value']:,.0f} ₽".replace(",", " "), "Расчётная стоимость")
    with c2: kpi_card("Стресс-результат", f"{leader['projected_value'] * (1 + leader['worst_stress_impact_pct']/100):,.0f} ₽".replace(",", " "), "Худший стресс")
    with c3: kpi_card("Стресс-просадка", f"{leader['worst_stress_impact_pct']:.1f}%", "По стресс-сценариям")
    with c4: kpi_card("Ликвидность", str(leader["liquidity_label"]), f"{leader['liquid_within_30d_pct']:.1f}% до 30 дней")
    with c5: kpi_card("Риск", str(leader["risk_label"]), f"{leader['risk_score']:.1f} / 5")
    with c6: kpi_card("Сложность", str(leader["complexity_label"]), f"{leader['complexity_score']:.1f} / 5")

    main, side = st.columns([1.55, .75])
    with main:
        table_card("Таблица сравнения сценариев", result["summary"].round(2))
        st.plotly_chart(scenario_projection_chart(result["summary"], st.session_state["investment_lab_assumptions"].horizon_years), use_container_width=True)
        st.plotly_chart(drawdown_chart(result["summary"]), use_container_width=True)
        st.plotly_chart(risk_bar_chart(result["summary"]), use_container_width=True)
    with side:
        st.markdown("<div class='lab-right-panel'><h3>Риск-флаги</h3>", unsafe_allow_html=True)
        risk_chips(result["flags"])
        st.markdown("<h3>Чек-лист перед самостоятельным решением</h3>", unsafe_allow_html=True)
        for item in REPORT_CHECKLIST[:4]:
            st.markdown(f"- [ ] {item}")
        st.markdown("</div>", unsafe_allow_html=True)
        st.plotly_chart(portfolio_allocation_donut(result["asset_allocation"], scenario=str(leader["scenario"]), total_value=float(leader["portfolio_value"])), use_container_width=True)

    with st.expander("Показать расчёты"):
        table_card("Позиции", result["positions"].round(2))
        st.plotly_chart(stress_bar(result["stress"]), use_container_width=True)
    with st.expander("Расчётные допущения"):
        st.json(result["assumptions"])
    with st.expander("Ограничения анализа"):
        for limitation in result["limitations"]:
            st.write(f"- {limitation}")

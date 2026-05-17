from __future__ import annotations

import pandas as pd
import streamlit as st

from investment_lab.domain.models import SUPPORTED_ASSET_CLASSES, default_instruments, required_instrument_columns
from investment_lab.engine.scenario_comparator import analyze_scenarios
from investment_lab.ui.charts import allocation_donut
from investment_lab.ui.components import disclaimer, empty_state, kpi_card, privacy_notice, risk_chips, table_card
from investment_lab.data.legal_texts import FOOTER_DISCLAIMER, SHORT_DISCLAIMER
from investment_lab.ui.layout import go_to


def render() -> None:
    st.markdown("## Проверить портфель")
    st.caption("Анализ структуры существующего портфеля, введённого вручную, без интеграции с брокером.")
    disclaimer(SHORT_DISCLAIMER)
    privacy_notice(FOOTER_DISCLAIMER)
    cta1, cta2, cta3 = st.columns(3)
    with cta1:
        if st.button("Добавить позицию", use_container_width=True):
            st.session_state["investment_lab_portfolio"].append(default_instruments()[0] | {"scenario": "Текущий портфель"})
            st.rerun()
    with cta2:
        if st.button("Добавить из шаблона", use_container_width=True):
            st.session_state["investment_lab_portfolio"] = default_instruments()[:2]
            st.rerun()
    with cta3:
        if st.button("Очистить", use_container_width=True):
            st.session_state["investment_lab_portfolio"] = []
            st.rerun()

    data = _ensure_portfolio_df(pd.DataFrame(st.session_state["investment_lab_portfolio"]))
    left, right = st.columns([1.5, 1])
    with left:
        st.markdown("<div class='lab-table-card'><h3>Позиции портфеля</h3>", unsafe_allow_html=True)
        edited = st.data_editor(
            data,
            num_rows="dynamic",
            use_container_width=True,
            hide_index=True,
            column_config={
                "asset_class": st.column_config.SelectboxColumn("asset_class", options=list(SUPPORTED_ASSET_CLASSES)),
                "market_value": st.column_config.NumberColumn("market_value", min_value=0.0, step=1000.0),
                "liquidity_days": st.column_config.NumberColumn("liquidity_days", min_value=0, step=1),
            },
            key="portfolio_editor",
        )
        st.markdown("</div>", unsafe_allow_html=True)
        st.session_state["investment_lab_portfolio"] = edited.to_dict("records")
    with right:
        result = analyze_scenarios(edited, st.session_state["investment_lab_assumptions"], st.session_state["investment_lab_constraints"])
        if result["summary"].empty:
            empty_state("Нет портфеля", "Введите хотя бы одну позицию с положительной стоимостью.")
        else:
            row = result["summary"].iloc[0]
            kpi_card("Статус", str(row["status"]), "Проверка по пользовательским ограничениям")
            kpi_card("Ликвидно до 30 дней", f"{row['liquid_within_30d_pct']:.1f}%", "Доля портфеля")
            kpi_card("Макс. позиция", f"{row['max_position_pct']:.1f}%", "Концентрация")

    if not result["summary"].empty:
        st.markdown("### Структура портфеля")
        st.plotly_chart(allocation_donut(result["asset_allocation"], scenario="Текущий портфель"), use_container_width=True)
        st.markdown("### Замечания")
        risk_chips(result["flags"])
        table_card("Риск-флаги", result["flags"])
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Проверить портфель", type="primary", use_container_width=True):
                st.session_state["investment_lab_results"] = result
                st.session_state["investment_lab_report_ready"] = True
                go_to("Итог по сценариям")
        with c2:
            if st.button("Сформировать отчёт", use_container_width=True):
                st.session_state["investment_lab_results"] = result
                st.session_state["investment_lab_report_ready"] = True
                go_to("Аналитический отчёт")


def _ensure_portfolio_df(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        df = pd.DataFrame(default_instruments()[:2])
    for column in required_instrument_columns():
        if column not in df.columns:
            df[column] = "Текущий портфель" if column == "scenario" else 0
    df["scenario"] = "Текущий портфель"
    return df[required_instrument_columns()]

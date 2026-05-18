from __future__ import annotations

import pandas as pd
import streamlit as st

from investment_lab.domain.models import SUPPORTED_ASSET_CLASSES, default_instruments, default_portfolio, required_instrument_columns
from investment_lab.engine.report_builder import build_cashflow_table, user_cashflow_table
from investment_lab.engine.scenario_comparator import analyze_scenarios
from investment_lab.ui.charts import allocation_donut
from investment_lab.ui.components import disclaimer, empty_state, kpi_card, privacy_notice, risk_chips, table_card
from investment_lab.data.legal_texts import FOOTER_DISCLAIMER, SHORT_DISCLAIMER
from investment_lab.ui.layout import go_to


def render() -> None:
    st.markdown("<div class='lab-page-header'><div><h2>Проверить портфель</h2><div class='lab-page-kicker'>Анализ структуры существующего портфеля, введённого вручную, без интеграции с брокером.</div></div><span class='lab-pill'>Портфельный контроль</span></div>", unsafe_allow_html=True)
    cta1, cta2, cta3 = st.columns(3)
    with cta1:
        if st.button("Добавить позицию", use_container_width=True):
            st.session_state["investment_lab_portfolio"].append(default_instruments()[0] | {"scenario": "Текущий портфель"})
            st.rerun()
    with cta2:
        if st.button("Добавить из шаблона", use_container_width=True):
            st.session_state["investment_lab_portfolio"] = default_portfolio()
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
                "scenario": st.column_config.TextColumn("Сценарий", disabled=True),
                "instrument": st.column_config.TextColumn("Инструмент"),
                "ticker": st.column_config.TextColumn("Код/метка"),
                "asset_class": st.column_config.SelectboxColumn("Класс актива", options=list(SUPPORTED_ASSET_CLASSES)),
                "country": st.column_config.TextColumn("Страна/источник"),
                "currency": st.column_config.SelectboxColumn("Валюта", options=["RUB", "USD", "EUR", "CNY"]),
                "market_value": st.column_config.NumberColumn("Сумма", min_value=0.0, step=1000.0),
                "expected_return_pct": st.column_config.NumberColumn("Ожидаемая доходность, %", step=0.25),
                "volatility_pct": st.column_config.NumberColumn("Волатильность, %", min_value=0.0, step=0.25),
                "liquidity_days": st.column_config.NumberColumn("Ликвидность, дней", min_value=0, step=1),
                "annual_fee_pct": st.column_config.NumberColumn("Комиссия, %", min_value=0.0, step=0.05),
                "tax_pct": st.column_config.NumberColumn("Налог, %", min_value=0.0, step=0.25),
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
            st.markdown("<div class='lab-sidebar-card'><h3>Структура портфеля</h3>", unsafe_allow_html=True)
            st.plotly_chart(allocation_donut(result["asset_allocation"], scenario="Текущий портфель"), use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown(
                "<div class='lab-sidebar-card'><h3>Быстрые индикаторы</h3>"
                "<div class='lab-result-list'>"
                f"<div class='lab-result-line'><span>Концентрация (топ-2)</span><strong class='lab-value-red'>{row['max_position_pct']:.1f}%</strong></div>"
                f"<div class='lab-result-line'><span>Взвешенный риск</span><strong>{row['risk_label']}</strong></div>"
                f"<div class='lab-result-line'><span>Взвешенная ликвидность</span><strong class='lab-value-green'>{row['liquidity_label']}</strong></div>"
                f"<div class='lab-result-line'><span>Ожидаемая комиссия (в год)</span><strong>{row['fee_and_commission_drag_pct']:.2f}%</strong></div>"
                "</div></div>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<div class='lab-sidebar-card'><h3>Замечания</h3>"
                "<div class='lab-chip-row'><span class='lab-risk-flag danger'>Высокая концентрация</span><span class='lab-risk-flag'>Несоответствие горизонту</span></div>"
                "<p><span class='lab-risk-dot'>Показать все замечания (4) ˄</span></p></div>",
                unsafe_allow_html=True,
            )

    if not result["summary"].empty:
        st.markdown("### Слабые места портфеля")
        risk_chips(result["flags"])
        st.markdown("<div class='lab-action-bar'><span>Концентрация</span><span>Низкая ликвидность</span><span>Рыночный риск</span><span>Валютный риск</span><span>Налоговые и комиссионные допущения</span></div>", unsafe_allow_html=True)
        table_card("Риск-флаги", result["flags"])
        cashflows = build_cashflow_table(result["summary"], int(result["assumptions"].get("horizon_years", 5)))
        table_card("Денежные потоки", user_cashflow_table(cashflows))
        st.markdown("<div class='lab-panel'><h3>Что проверить</h3><ul><li>Соответствие долей вашим ограничениям.</li><li>Реальные комиссии, налоги и сроки выхода.</li><li>Календарь выплат по инструментам.</li></ul><h3>Что не учитывается</h3><p>Нет брокерской интеграции, данные только в сессии; расчёт основан на ручном вводе.</p></div>", unsafe_allow_html=True)
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


def _ensure_portfolio_df(df: pd.DataFrame, fill_defaults: bool = False) -> pd.DataFrame:
    if df.empty:
        if fill_defaults:
            df = pd.DataFrame(default_portfolio())
        else:
            return pd.DataFrame(columns=required_instrument_columns())
    for column in required_instrument_columns():
        if column not in df.columns:
            df[column] = "Текущий портфель" if column == "scenario" else 0
    df["scenario"] = "Текущий портфель"
    return df[required_instrument_columns()]

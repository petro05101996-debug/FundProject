"""Router for the multi-page Investment Scenario Lab product module."""
from __future__ import annotations

import streamlit as st

from investment_lab.ui.layout import apply_shell, init_session_state, sidebar_navigation
from investment_lab.ui.pages import (
    explain_instrument_page,
    instrument_check_page,
    landing_page,
    portfolio_check_page,
    report_page,
    results_page,
    scenario_builder_page,
    scenario_profile_page,
)

PAGE_RENDERERS = {
    "Лендинг": landing_page.render,
    "Параметры сценария": scenario_profile_page.render,
    "Проверить инструмент": instrument_check_page.render,
    "Сравнить мои варианты": scenario_builder_page.render,
    "Проверить портфель": portfolio_check_page.render,
    "Итог по сценариям": results_page.render,
    "Аналитический отчёт": report_page.render,
    "Объяснить инструмент": explain_instrument_page.render,
}


def render_investment_lab_app() -> None:
    init_session_state()
    apply_shell()
    page = sidebar_navigation()
    with st.container():
        st.markdown("<div class='lab-shell'>", unsafe_allow_html=True)
        PAGE_RENDERERS.get(page, landing_page.render)()
        st.markdown("</div>", unsafe_allow_html=True)

"""Router for the multi-page Investment Scenario Lab product module."""
from __future__ import annotations

import streamlit as st

from legacy_streamlit.ui.layout import apply_shell, init_session_state, sidebar_navigation
from legacy_streamlit.ui.pages import (
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
    current_page = st.session_state["investment_lab_page"]
    if current_page == "Лендинг":
        st.markdown("<style>[data-testid='stSidebar']{display:none !important;} .block-container{padding-left:1.8rem !important; padding-right:1.8rem !important;}</style>", unsafe_allow_html=True)
        page = current_page
    else:
        page = sidebar_navigation()
    shell_class = "lab-shell lab-shell-landing" if page == "Лендинг" else "lab-shell"
    with st.container():
        st.markdown(f"<div class='{shell_class}'>", unsafe_allow_html=True)
        PAGE_RENDERERS.get(page, landing_page.render)()
        st.markdown("</div>", unsafe_allow_html=True)

"""Application shell and session flow helpers."""
from __future__ import annotations

import streamlit as st

from investment_lab.data.legal_texts import FOOTER_DISCLAIMER, PRIMARY_DISCLAIMER
from investment_lab.domain.models import ScenarioAssumptions, UserConstraints, default_instruments, default_portfolio
from investment_lab.ui.styles import APP_CSS

PAGES = [
    "Лендинг",
    "Параметры сценария",
    "Проверить инструмент",
    "Сравнить мои варианты",
    "Проверить портфель",
    "Итог по сценариям",
    "Аналитический отчёт",
    "Объяснить инструмент",
]

NAV_GROUPS = {
    "АНАЛИЗ": ["Лендинг", "Параметры сценария", "Проверить инструмент", "Сравнить мои варианты", "Проверить портфель", "Итог по сценариям"],
    "БИБЛИОТЕКА": ["Аналитический отчёт", "Объяснить инструмент"],
    "СЕРВИС": ["О проекте / дисклеймер"],
}


def init_session_state() -> None:
    defaults = {
        "investment_lab_page": "Лендинг",
        "investment_lab_mode": "Сравнить мои варианты",
        "investment_lab_profile": {
            "amount": 500000.0,
            "currency": "RUB",
            "horizon_months": 12,
            "horizon_bucket": "6–12 месяцев",
            "goal": "Сохранить деньги",
            "liquidity_need": "Возможно через 3–6 месяцев",
            "may_need_money_early": True,
            "min_liquidity_pct_30d": 80.0,
            "drawdown_choice": "До 5%",
            "acceptable_drawdown_pct": 5.0,
            "experience": "Не разбираюсь",
            "include_fees": True,
            "include_taxes": True,
            "tax_pct": 13.0,
        },
        "investment_lab_scenarios": default_instruments(),
        "investment_lab_portfolio": default_portfolio(),
        "investment_lab_results": None,
        "investment_lab_report_ready": False,
        "investment_lab_assumptions": ScenarioAssumptions(),
        "investment_lab_constraints": UserConstraints(),
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


def apply_shell() -> None:
    st.markdown(APP_CSS, unsafe_allow_html=True)
    st.markdown(
        "<div class='lab-topbar'>"
        "<div class='lab-brand'><div class='lab-brand-mark'>▱</div><div class='lab-brand-text'>"
        "<div class='lab-brand-title'>Investment Scenario Lab</div>"
        "<div class='lab-brand-subtitle'>Финансовый сценарный анализатор</div></div></div>"
        "<div class='lab-topnav'><span>Возможности</span><span>Как это работает</span><span>Тарифы</span><span>Примеры</span><span>База знаний</span><span>О проекте</span></div>"
        "<div class='lab-top-actions'><span class='lab-icon-btn'>☾</span><span class='lab-pill'>Войти</span><span class='lab-pill lab-primary-pill'>Войти в сервис</span></div>"
        "</div>",
        unsafe_allow_html=True,
    )


def sidebar_navigation() -> str:
    with st.sidebar:
        st.markdown("### ◈ Investment Scenario Lab")
        st.caption("Финансовый сценарный анализатор")
        page = st.session_state["investment_lab_page"]
        for group, items in NAV_GROUPS.items():
            st.markdown(f"<div class='lab-sidebar-group'>{group}</div>", unsafe_allow_html=True)
            for item in items:
                if item == "О проекте / дисклеймер":
                    st.markdown(f"<div class='lab-nav-item'>ⓘ {item}</div>", unsafe_allow_html=True)
                    continue
                active = item == page
                css = "lab-nav-item lab-nav-item-active" if active else "lab-nav-item"
                icon = {'Лендинг': '⌂', 'Параметры сценария': '◫', 'Проверить инструмент': '⌁', 'Сравнить мои варианты': '⚖', 'Проверить портфель': '▣', 'Итог по сценариям': '☷', 'Аналитический отчёт': '▤', 'Объяснить инструмент': 'ⓘ'}.get(item, "○")
                label = f"{icon} {item}"
                if st.button(label, key=f"nav_{item}", use_container_width=True, type="primary" if active else "secondary"):
                    st.session_state["investment_lab_page"] = item
                    page = item
        st.markdown("---")
        st.caption(PRIMARY_DISCLAIMER)
        st.markdown(f"<div class='lab-feedback'><strong>MVP-версия</strong><br>{FOOTER_DISCLAIMER}<br><br>Обратная связь будет добавлена после проверки MVP-гипотезы.</div>", unsafe_allow_html=True)
    return st.session_state["investment_lab_page"]


def go_to(page: str) -> None:
    st.session_state["investment_lab_page"] = page
    st.rerun()

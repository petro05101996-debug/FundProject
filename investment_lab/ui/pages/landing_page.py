from __future__ import annotations

import pandas as pd
import streamlit as st

from investment_lab.data.legal_texts import FOOTER_DISCLAIMER, PRIMARY_DISCLAIMER, WHAT_SERVICE_DOES, WHAT_SERVICE_DOES_NOT_DO
from investment_lab.data.mock_data import MODE_CARDS
from investment_lab.engine.scenario_comparator import analyze_scenarios
from investment_lab.ui.charts import scenario_projection_chart
from investment_lab.ui.components import bullet_card, card, disclaimer, kpi_card, privacy_notice
from investment_lab.ui.layout import go_to


def render() -> None:
    result = analyze_scenarios(pd.DataFrame(st.session_state["investment_lab_scenarios"]), st.session_state["investment_lab_assumptions"], st.session_state["investment_lab_constraints"])
    st.markdown("<div class='lab-hero'>", unsafe_allow_html=True)
    left, right = st.columns([1.05, .95])
    with left:
        st.markdown("<span class='lab-badge'>Финансовый сценарный анализатор</span><h1>Проверьте инвестиционный сценарий до покупки</h1><p>Сравните собственные сценарии, риски, ликвидность, комиссии, налоги и стресс-условия до самостоятельного решения.</p>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Начать проверку сценария", type="primary", use_container_width=True):
                go_to("Параметры сценария")
        with c2:
            if st.button("Сравнить мои варианты", use_container_width=True):
                go_to("Сравнить мои варианты")
        st.markdown("<p>✓ Данные остаются только у вас<br>✓ Методология без конфликта интересов<br>✓ Прозрачные расчёты и допущения</p>", unsafe_allow_html=True)
    with right:
        st.markdown("<div class='lab-preview-dashboard'><h3>Превью сравнения сценариев</h3>", unsafe_allow_html=True)
        if not result["summary"].empty:
            st.plotly_chart(scenario_projection_chart(result["summary"], 5), use_container_width=True)
            k1, k2, k3, k4, k5 = st.columns(5)
            row = result["summary"].iloc[0]
            with k1: st.metric("Риск", row["risk_label"])
            with k2: st.metric("Просадка", f"{row['worst_stress_impact_pct']:.1f}%")
            with k3: st.metric("Ликвидность", row["liquidity_label"])
            with k4: st.metric("Комиссии", f"{row['fee_and_commission_drag_pct']:.1f}%")
            with k5: st.metric("Налоги", f"{row['tax_drag_pct']:.1f}%")
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("### Возможности")
    features = [
        ("Сравнение сценариев", "Сравнивает только варианты, которые ввёл пользователь."),
        ("Паспорт рисков", "Показывает риск-флаги, концентрацию и ограничения."),
        ("Стресс-тестирование", "Проверяет введённые сценарии на стресс-условиях."),
        ("Прозрачный отчёт", "Фиксирует допущения, ограничения и чек-лист."),
    ]
    cols = st.columns(4)
    for col, (title, body) in zip(cols, features):
        with col: card(title, body, badge="Возможность")

    st.markdown("### Как это работает")
    steps = st.columns(3)
    for col, text in zip(steps, ["Загрузите или введите данные", "Сервис рассчитает и проверит ограничения", "Получите отчёт и сравните сценарии"]):
        with col: card("Шаг", text, strong=True)

    left2, right2 = st.columns(2)
    with left2: bullet_card("Что делает сервис", WHAT_SERVICE_DOES, positive=True)
    with right2: bullet_card("Что сервис НЕ делает", WHAT_SERVICE_DOES_NOT_DO, positive=False)
    disclaimer(PRIMARY_DISCLAIMER)
    privacy_notice(FOOTER_DISCLAIMER)

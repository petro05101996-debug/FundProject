from __future__ import annotations

import pandas as pd
import streamlit as st

from investment_lab.data.mockup_metrics import MOCKUP_LANDING_KPIS, MOCKUP_RESULTS
from investment_lab.data.legal_texts import FOOTER_DISCLAIMER, PRIMARY_DISCLAIMER, WHAT_SERVICE_DOES, WHAT_SERVICE_DOES_NOT_DO
from investment_lab.ui.charts import scenario_projection_chart
from investment_lab.ui.components import bullet_card, card, disclaimer, privacy_notice
from investment_lab.ui.layout import go_to


def render() -> None:
    summary = pd.DataFrame(MOCKUP_RESULTS)
    preview = MOCKUP_LANDING_KPIS

    st.markdown("<div class='lab-hero'>", unsafe_allow_html=True)
    left, right = st.columns([1.05, .95])
    with left:
        st.markdown(
            "<span class='lab-badge'>◇ Финансовый сценарный анализатор</span>"
            "<h1>Проверьте <span class='accent'>инвестиционный сценарий</span><br>до покупки</h1>"
            "<p>Сравните выбранные вами варианты, увидьте риски, ликвидность, комиссии, налоги и плохой сценарий. "
            "Без инвестиционных рекомендаций и без продажи инструментов.</p>",
            unsafe_allow_html=True,
        )
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("↗ Проверить сценарий", type="primary", use_container_width=True):
                go_to("Параметры сценария")
        with c2:
            if st.button("⚖ Сравнить варианты", use_container_width=True):
                go_to("Сравнить мои варианты")
        with c3:
            if st.button("▣ Проверить портфель", use_container_width=True):
                go_to("Проверить портфель")
        st.markdown(
            "<div class='lab-trust-row'>"
            "<div class='lab-trust-item'><span class='lab-trust-icon'>🔒</span>Данные остаются только у вас</div>"
            "<div class='lab-trust-item'><span class='lab-trust-icon'>🛡</span>Методология без конфликта интересов</div>"
            "<div class='lab-trust-item'><span class='lab-trust-icon'>▤</span>Прозрачные расчёты и допущения</div>"
            "</div>",
            unsafe_allow_html=True,
        )
    with right:
        st.markdown("<div class='lab-preview-dashboard'><h3>Мини-dashboard сравнения</h3>", unsafe_allow_html=True)
        st.markdown(
            "<div class='lab-instrument-row'><span>Сценарий А<small>лучше по ликвидности</small></span><span class='lab-risk-dot'>ликвидность</span></div>"
            "<div class='lab-instrument-row'><span>Сценарий Б<small>выше риск просадки</small></span><span class='lab-risk-dot'>просадка</span></div>"
            "<div class='lab-instrument-row'><span>Сценарий В<small>нарушает срок</small></span><span class='lab-risk-dot'>срок</span></div>",
            unsafe_allow_html=True,
        )
        st.plotly_chart(scenario_projection_chart(summary, 5), use_container_width=True)
        st.markdown(
            "<div class='lab-metric-strip'>"
            "<span class='lab-risk-chip Medium'>ликвидность</span>"
            "<span class='lab-risk-chip High'>просадка</span>"
            "<span class='lab-risk-chip Medium'>комиссии</span>"
            "<span class='lab-risk-chip Low'>налоги</span>"
            "</div>",
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("### Возможности")
    features = [
        ("⚖", "Сравнение сценариев", "Сравнение по доходности, риску, ликвидности, комиссиям и налогам."),
        ("🛡", "Паспорт рисков", "Выявляет концентрацию, волатильность и ограничения по ликвидности."),
        ("☔", "Стресс-тестирование", "Проверяет устойчивость к просадкам и неблагоприятным событиям."),
        ("▤", "Прозрачный отчёт", "Фиксирует допущения, расчётные ограничения и чек-лист."),
    ]
    cols = st.columns(4)
    for col, (icon, title, body) in zip(cols, features):
        with col:
            card(f"{icon} {title}", body, badge="Модуль")

    st.markdown("### Как это работает")
    steps = st.columns(3)
    for number, (col, text) in enumerate(
        zip(
            steps,
            [
                "Введите параметры и сценарии: укажите сумму, горизонт и инструменты.",
                "Получите риск-флаги, стресс-тест, ликвидность, комиссии и налоги.",
                "Сохраните прозрачный отчёт с допущениями и ограничениями расчёта.",
            ],
        ),
        start=1,
    ):
        with col:
            card(f"{number} Шаг", text, strong=True)

    left2, right2 = st.columns(2)
    with left2:
        bullet_card("Что делает сервис", WHAT_SERVICE_DOES, positive=True)
    with right2:
        bullet_card("Что сервис НЕ делает", WHAT_SERVICE_DOES_NOT_DO, positive=False)
    st.markdown("<div class='lab-action-bar'><span>Без брокерской интеграции</span><span>Без кнопки Купить</span><span>Без инвестиционных рекомендаций</span><span>Только пользовательские сценарии</span></div>", unsafe_allow_html=True)
    disclaimer(PRIMARY_DISCLAIMER)
    privacy_notice(FOOTER_DISCLAIMER)

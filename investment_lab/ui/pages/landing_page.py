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
            "<p>Сравнивайте свои сценарии, оценивайте риски, ликвидность, комиссии и налоги. "
            "Проверяйте устойчивость портфеля в стресс-условиях без продажи инструментов.</p>",
            unsafe_allow_html=True,
        )
        c1, c2 = st.columns([1.05, .95])
        with c1:
            if st.button("↗ Начать проверку сценария", type="primary", use_container_width=True):
                go_to("Параметры сценария")
        with c2:
            if st.button("⚖ Сравнить мои варианты", use_container_width=True):
                go_to("Сравнить мои варианты")
        st.markdown(
            "<div class='lab-trust-row'>"
            "<div class='lab-trust-item'><span class='lab-trust-icon'>🔒</span>Данные остаются только у вас</div>"
            "<div class='lab-trust-item'><span class='lab-trust-icon'>🛡</span>Методология без конфликта интересов</div>"
            "<div class='lab-trust-item'><span class='lab-trust-icon'>▤</span>Прозрачные расчёты и допущения</div>"
            "</div>",
            unsafe_allow_html=True,
        )
    with right:
        st.markdown("<div class='lab-preview-dashboard'><h3>Сравнение сценариев</h3>", unsafe_allow_html=True)
        st.markdown(
            f"<div class='lab-page-kicker'>Сценарий A</div>"
            f"<div class='lab-kpi-value'>{preview['projected_value']:,.0f} ₽</div>".replace(",", " ")
            + f"<div class='lab-page-kicker'>ожидаемая стоимость · +{preview['growth_pct']:.1f}%</div>",
            unsafe_allow_html=True,
        )
        st.plotly_chart(scenario_projection_chart(summary, 5), use_container_width=True)
        st.markdown(
            "<div class='lab-metric-strip'>"
            f"<div class='lab-mini-kpi'><div class='label'>Риск</div><div class='value'>{preview['stress_drawdown_pct']:.1f}%</div></div>"
            f"<div class='lab-mini-kpi'><div class='label'>Макс. просадка</div><div class='value'>{preview['max_drawdown_pct']:.1f}%</div></div>"
            f"<div class='lab-mini-kpi'><div class='label'>Ликвидность</div><div class='value'>{preview['liquidity']}</div></div>"
            f"<div class='lab-mini-kpi'><div class='label'>Комиссия</div><div class='value'>{preview['commission_pct']:.2f}%</div></div>"
            f"<div class='lab-mini-kpi'><div class='label'>Налоги</div><div class='value'>{preview['tax_pct']:.1f}%</div></div>"
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
                "Загрузите или создайте сценарии: укажите сумму, горизонт и инструменты.",
                "Сервис рассчитает риск, ликвидность, комиссии, налоги и стресс-метрики.",
                "Получите отчёт и сравните варианты по единым правилам расчёта.",
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
    disclaimer(PRIMARY_DISCLAIMER)
    privacy_notice(FOOTER_DISCLAIMER)

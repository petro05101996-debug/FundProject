from __future__ import annotations

import streamlit as st

from investment_lab.data.legal_texts import NO_ADVICE_NOTICE, SESSION_DATA_NOTICE, SHORT_DISCLAIMER
from investment_lab.data.mock_data import MODE_CARDS
from investment_lab.domain.models import ScenarioAssumptions, UserConstraints
from investment_lab.ui.components import action_bar, card, disclaimer, privacy_notice
from investment_lab.ui.layout import go_to


def render() -> None:
    st.markdown("<div class='lab-page-header'><div><h2>Параметры пользовательского сценария</h2><div class='lab-page-kicker'>Выберите режим анализа и задайте параметры сценария</div></div><span class='lab-pill'>Рабочее пространство</span></div>", unsafe_allow_html=True)
    disclaimer(SHORT_DISCLAIMER)

    st.markdown("### Режим анализа")
    cols = st.columns(4)
    for col, mode in zip(cols, MODE_CARDS):
        with col:
            active = st.session_state["investment_lab_mode"] == mode["title"]
            card(("✓ " if active else "") + mode["title"], mode["description"], badge="Активно" if active else "Режим", strong=active)
            if st.button("Выбрать", key=f"profile_{mode['key']}", use_container_width=True):
                st.session_state["investment_lab_mode"] = mode["title"]

    left, right = st.columns([1.45, .8])
    profile = st.session_state["investment_lab_profile"]
    with left:
        st.markdown("<div class='lab-panel'><h3>Параметры сценария</h3><p>Укажите вводные данные и предпочтения для анализа.</p>", unsafe_allow_html=True)
        a, b, c = st.columns(3)
        with a:
            profile["amount"] = st.number_input("Сумма", min_value=0.0, value=float(profile.get("amount", 100000)), step=1000.0)
            profile["currency"] = st.selectbox("Валюта", ["RUB", "USD", "EUR", "CNY"], index=["RUB", "USD", "EUR", "CNY"].index(profile.get("currency", "RUB")))
            profile["horizon_months"] = st.slider("Горизонт, месяцев", 1, 240, int(profile.get("horizon_months", 36)))
        with b:
            profile["goal"] = st.text_input("Цель", value=str(profile.get("goal", "Сравнить пользовательские сценарии")))
            profile["may_need_money_early"] = st.checkbox("Деньги могут понадобиться раньше", value=bool(profile.get("may_need_money_early", False)))
            profile["acceptable_drawdown_pct"] = st.slider("Допустимая просадка, %", 0.0, 100.0, float(profile.get("acceptable_drawdown_pct", 20.0)))
        with c:
            profile["experience"] = st.selectbox("Опыт пользователя", ["Начальный", "Средний", "Продвинутый"], index=["Начальный", "Средний", "Продвинутый"].index(profile.get("experience", "Средний")))
            profile["include_fees"] = st.checkbox("Учитывать комиссии", value=bool(profile.get("include_fees", True)))
            profile["include_taxes"] = st.checkbox("Учитывать налог", value=bool(profile.get("include_taxes", True)))
            profile["tax_pct"] = st.number_input("Ставка налога, %", 0.0, 100.0, float(profile.get("tax_pct", 13.0)), step=0.5)
        st.markdown("</div>", unsafe_allow_html=True)
    with right:
        st.markdown("<div class='lab-right-panel'><h3>Краткие правила расчёта</h3><ul><li>Ожидаемая доходность — пользовательское допущение.</li><li>Риск и волатильность считаются приближённо.</li><li>Ликвидность берётся из введённых дней.</li><li>Комиссии и издержки вычитаются из результата.</li><li>Налоги считаются по пользовательской ставке.</li><li>Стресс-сценарии статические.</li></ul></div>", unsafe_allow_html=True)
        privacy_notice(NO_ADVICE_NOTICE)

    st.session_state["investment_lab_profile"] = profile
    st.session_state["investment_lab_assumptions"] = ScenarioAssumptions(horizon_years=max(1, int(profile["horizon_months"] / 12)), default_tax_pct=profile["tax_pct"])
    st.session_state["investment_lab_constraints"] = UserConstraints(max_stress_loss_pct=profile["acceptable_drawdown_pct"])

    action_bar("Ваши данные защищены в рамках текущей сессии", SESSION_DATA_NOTICE)
    c1, c2 = st.columns([1, 1])
    with c1:
        if st.button("Продолжить к сценариям", type="primary", use_container_width=True):
            target = next((mode["page"] for mode in MODE_CARDS if mode["title"] == st.session_state["investment_lab_mode"]), "Сравнить мои варианты")
            go_to(target)
    with c2:
        if st.button("Очистить данные", use_container_width=True):
            st.session_state["investment_lab_profile"] = {}
            st.rerun()

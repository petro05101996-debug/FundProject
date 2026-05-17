from __future__ import annotations

import streamlit as st

from investment_lab.data.legal_texts import NO_ADVICE_NOTICE, SESSION_DATA_NOTICE, SHORT_DISCLAIMER
from investment_lab.data.mock_data import MODE_CARDS
from investment_lab.data.profile_options import DRAWDOWN_OPTIONS, EXPERIENCE_OPTIONS, GOAL_OPTIONS, HORIZON_OPTIONS, LIQUIDITY_OPTIONS, option_index
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
            horizon_options = list(HORIZON_OPTIONS)
            profile["horizon_bucket"] = st.selectbox("Срок", horizon_options, index=option_index(horizon_options, profile.get("horizon_bucket", "3–5 лет"), 4))
            profile["horizon_months"] = HORIZON_OPTIONS[profile["horizon_bucket"]]
        with b:
            profile["goal"] = st.selectbox("Цель сценария", GOAL_OPTIONS, index=option_index(GOAL_OPTIONS, profile.get("goal", "Сравнить варианты"), 4))
            liquidity_options = list(LIQUIDITY_OPTIONS)
            profile["liquidity_need"] = st.selectbox("Могут ли деньги понадобиться раньше срока?", liquidity_options, index=option_index(liquidity_options, profile.get("liquidity_need", "Возможно через 3–6 месяцев"), 1))
            liquidity_settings = LIQUIDITY_OPTIONS[profile["liquidity_need"]]
            profile["may_need_money_early"] = bool(liquidity_settings["may_need_money_early"])
            profile["min_liquidity_pct_30d"] = float(liquidity_settings["min_liquidity_pct_30d"])
        with c:
            drawdown_options = list(DRAWDOWN_OPTIONS)
            profile["drawdown_choice"] = st.selectbox("Какое временное снижение стоимости неприемлемо?", drawdown_options, index=option_index(drawdown_options, profile.get("drawdown_choice", "Больше 10%"), 4))
            profile["acceptable_drawdown_pct"] = DRAWDOWN_OPTIONS[profile["drawdown_choice"]]
            profile["experience"] = st.selectbox("Опыт пользователя", EXPERIENCE_OPTIONS, index=option_index(EXPERIENCE_OPTIONS, profile.get("experience", "Уже покупал вклады/облигации/фонды"), 2))
            profile["include_fees"] = st.checkbox("Учитывать комиссии", value=bool(profile.get("include_fees", True)))
            profile["include_taxes"] = st.checkbox("Учитывать налог", value=bool(profile.get("include_taxes", True)))
            profile["tax_pct"] = st.number_input("Ставка налога, %", 0.0, 100.0, float(profile.get("tax_pct", 13.0)), step=0.5)
        st.markdown("</div>", unsafe_allow_html=True)
    with right:
        st.markdown("<div class='lab-right-panel'><h3>Краткие правила расчёта</h3><ul><li>Ожидаемая доходность — пользовательское допущение.</li><li>Риск и волатильность считаются приближённо.</li><li>Ликвидность берётся из введённых дней.</li><li>Комиссии и издержки вычитаются из результата.</li><li>Налоги считаются по пользовательской ставке.</li><li>Стресс-сценарии статические.</li></ul></div>", unsafe_allow_html=True)
        privacy_notice(NO_ADVICE_NOTICE)

    st.session_state["investment_lab_profile"] = profile
    st.session_state["investment_lab_assumptions"] = ScenarioAssumptions(horizon_years=max(1, int(profile["horizon_months"] / 12)), default_tax_pct=profile["tax_pct"])
    st.session_state["investment_lab_constraints"] = UserConstraints(max_stress_loss_pct=profile["acceptable_drawdown_pct"], min_liquidity_pct_30d=profile.get("min_liquidity_pct_30d", 80.0))

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

from __future__ import annotations

import streamlit as st

from investment_lab.data.legal_texts import NO_ADVICE_NOTICE, SESSION_DATA_NOTICE, SHORT_DISCLAIMER
from investment_lab.data.mock_data import MODE_CARDS
from investment_lab.data.profile_options import DRAWDOWN_OPTIONS, EXPERIENCE_OPTIONS, GOAL_OPTIONS, HORIZON_OPTIONS, LIQUIDITY_OPTIONS, option_index
from investment_lab.domain.models import ScenarioAssumptions, UserConstraints
from investment_lab.ui.components import action_bar, card, disclaimer, privacy_notice
from investment_lab.ui.layout import go_to


def render() -> None:
    st.markdown(
        "<div class='lab-page-header'><div><h2>Параметры пользовательского сценария</h2><div class='lab-page-kicker'>Выберите режим анализа и задайте параметры сценария</div></div>"
        "<div class='lab-workspace-select'><small>Рабочее пространство</small>Основной проект ▾</div></div>",
        unsafe_allow_html=True,
    )

    st.markdown("### Режим анализа")
    cols = st.columns(4)
    for col, mode in zip(cols, MODE_CARDS):
        with col:
            active = st.session_state["investment_lab_mode"] == mode["title"]
            outcome = mode.get("outcome", "получите понятный результат и риск-флаги")
            icon = {"Проверить инструмент": "⌁", "Сравнить мои варианты": "⚖", "Проверить портфель": "▣", "Объяснить инструмент": "☰"}.get(mode["title"], "◇")
            prefix = "✓ " if active else ""
            card(f"{prefix}{icon} {mode['title']}", f"{mode['description']} Что получите: {outcome}", badge="Выбранный режим" if active else "Режим", strong=active)
            if st.button("Выбрать режим", key=f"profile_{mode['key']}", use_container_width=True, type="primary" if active else "secondary"):
                st.session_state["investment_lab_mode"] = mode["title"]

    left, right = st.columns([1.45, .8])
    profile = st.session_state["investment_lab_profile"]
    with left:
        st.markdown("<div class='lab-panel'><h3>Параметры сценария</h3><p>Укажите вводные данные и предпочтения для анализа.</p>", unsafe_allow_html=True)
        a, b, c = st.columns(3)
        with a:
            profile["amount"] = st.number_input("Сумма", min_value=0.0, value=float(profile.get("amount", 500000)), step=1000.0)
            profile["currency"] = st.selectbox("Валюта", ["RUB", "USD", "EUR", "CNY"], index=["RUB", "USD", "EUR", "CNY"].index(profile.get("currency", "RUB")))
            horizon_options = list(HORIZON_OPTIONS)
            profile["horizon_bucket"] = st.selectbox("Срок", horizon_options, index=option_index(horizon_options, profile.get("horizon_bucket", "6–12 месяцев"), 2))
            profile["horizon_months"] = HORIZON_OPTIONS[profile["horizon_bucket"]]
        with b:
            profile["goal"] = st.selectbox("Цель сценария", GOAL_OPTIONS, index=option_index(GOAL_OPTIONS, profile.get("goal", "Сохранить деньги"), 0))
            liquidity_options = list(LIQUIDITY_OPTIONS)
            profile["liquidity_need"] = st.selectbox("Могут ли деньги понадобиться раньше срока?", liquidity_options, index=option_index(liquidity_options, profile.get("liquidity_need", "Возможно через 3–6 месяцев"), 1))
            liquidity_settings = LIQUIDITY_OPTIONS[profile["liquidity_need"]]
            profile["may_need_money_early"] = bool(liquidity_settings["may_need_money_early"])
            profile["min_liquidity_pct_30d"] = float(liquidity_settings["min_liquidity_pct_30d"])
        with c:
            drawdown_options = list(DRAWDOWN_OPTIONS)
            profile["drawdown_choice"] = st.selectbox("Какое временное снижение стоимости неприемлемо?", drawdown_options, index=option_index(drawdown_options, profile.get("drawdown_choice", "До 5%"), 2))
            profile["acceptable_drawdown_pct"] = DRAWDOWN_OPTIONS[profile["drawdown_choice"]]
            profile["experience"] = st.selectbox("Опыт пользователя", EXPERIENCE_OPTIONS, index=option_index(EXPERIENCE_OPTIONS, profile.get("experience", "Не разбираюсь"), 0))
            profile["include_fees"] = st.checkbox("Учитывать комиссии", value=bool(profile.get("include_fees", True)))
            profile["include_taxes"] = st.checkbox("Учитывать налог", value=bool(profile.get("include_taxes", True)))
            profile["tax_pct"] = st.number_input("Ставка налога, %", 0.0, 100.0, float(profile.get("tax_pct", 13.0)), step=0.5)
        st.markdown("</div>", unsafe_allow_html=True)
    with right:
        next_hint = _next_step_hint(st.session_state["investment_lab_mode"])
        st.markdown(
            "<div class='lab-sidebar-card'><h3>Краткие правила расчёта</h3>"
            "<div class='lab-sidebar-list'>"
            "<div><strong>◎ Ожидаемая доходность</strong>Среднегодовая доходность по каждому варианту с учётом горизонта и реинвестирования.</div>"
            "<div><strong>☷ Риск и волатильность</strong>Вероятность потерь, волатильность доходности и максимальная просадка.</div>"
            "<div><strong>◌ Ликвидность</strong>Возможность быстрого выхода из позиции и вероятность досрочного вывода.</div>"
            "<div><strong>⚖ Комиссии и издержки</strong>Влияние всех комиссий на итоговую доходность.</div>"
            "<div><strong>☆ Налоги</strong>Налоговые последствия и чистая доходность после учета налогов.</div>"
            "<div><strong>☰ Стресс-сценарии</strong>Поведение каждого варианта при неблагоприятных условиях.</div>"
            "</div></div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<div class='lab-sidebar-card'><h3>Ваш профиль сценария</h3>"
            f"<p><strong>Сумма:</strong> {profile.get('amount', 0):,.0f} {profile.get('currency', 'RUB')}</p>".replace(',', ' ')
            + f"<p><strong>Срок:</strong> {profile.get('horizon_bucket')}</p>"
            + f"<p><strong>Цель:</strong> {profile.get('goal')}</p>"
            + f"<p><strong>Что будет проверено:</strong> {next_hint}</p></div>",
            unsafe_allow_html=True,
        )
        privacy_notice(NO_ADVICE_NOTICE)

    st.session_state["investment_lab_profile"] = profile
    st.session_state["investment_lab_assumptions"] = ScenarioAssumptions(horizon_years=max(1, int(profile["horizon_months"] / 12)), default_tax_pct=profile["tax_pct"])
    st.session_state["investment_lab_constraints"] = UserConstraints(max_stress_loss_pct=profile["acceptable_drawdown_pct"], min_liquidity_pct_30d=profile.get("min_liquidity_pct_30d", 80.0))

    st.markdown("<div class='lab-action-bar'><span>1. Параметры</span><span>→ 2. Сценарии</span><span>→ 3. Расчёт</span><span>→ 4. Отчёт</span></div>", unsafe_allow_html=True)
    action_bar("Ваши данные защищены в рамках текущей сессии", SESSION_DATA_NOTICE)
    c0, c1, c2 = st.columns([1, 1, 1])
    with c0:
        if st.button("Назад на лендинг", use_container_width=True):
            go_to("Лендинг")
    with c1:
        if st.button("Продолжить", type="primary", use_container_width=True):
            target = next((mode["page"] for mode in MODE_CARDS if mode["title"] == st.session_state["investment_lab_mode"]), "Сравнить мои варианты")
            go_to(target)
    with c2:
        if st.button("Очистить", use_container_width=True):
            st.session_state["investment_lab_profile"] = {}
            st.rerun()


def _next_step_hint(mode: str) -> str:
    return {
        "Проверить инструмент": "введите параметры инструмента → получите паспорт риска",
        "Сравнить мои варианты": "добавьте 2–5 сценариев → получите таблицу и стресс-тест",
        "Проверить портфель": "введите позиции → получите концентрацию, ликвидность, стресс",
        "Объяснить инструмент": "выберите инструмент → получите простое объяснение",
    }.get(mode, "добавьте сценарии → получите сравнение и отчёт")

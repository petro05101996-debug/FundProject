from __future__ import annotations

import pandas as pd
import streamlit as st

from investment_lab.data.legal_texts import SHORT_DISCLAIMER
from investment_lab.engine.bond_calculator import calculate_bond
from investment_lab.engine.deposit_calculator import calculate_deposit, calculate_savings_account
from investment_lab.engine.fund_calculator import calculate_fund
from investment_lab.engine.scenario_comparator import analyze_scenarios
from investment_lab.ui.components import disclaimer, kpi_card, risk_chips, table_card
from investment_lab.ui.formatters import format_money, format_pct

INSTRUMENT_TABS = ["Вклад", "Накопительный счёт", "ОФЗ", "Корпоративная облигация", "Фонд денежного рынка", "Облигационный фонд", "Индексный фонд", "Акция как класс"]

INSTRUMENT_EXPLAINERS = {
    "Вклад": "Банковский продукт с заранее заданной ставкой. Доход формируется процентами банка; главный риск — условия досрочного снятия и лимит страхования.",
    "Накопительный счёт": "Счёт с более гибким доступом к деньгам. Доход зависит от правил начисления; главный риск — изменение ставки и условий банком.",
    "ОФЗ": "Государственная облигация. Доход формируется купонами и ценой погашения; главные риски — процентный риск, продажа до погашения и ликвидность.",
    "Корпоративная облигация": "Долговой инструмент компании. Доход формируется купонами и ценой погашения; главный риск — кредитное качество эмитента и ликвидность.",
    "Фонд денежного рынка": "Фонд коротких денежных инструментов. Доход зависит от ставок и комиссий фонда; главный риск — изменение ставок и правила фонда.",
    "Облигационный фонд": "Фонд с набором облигаций. Доход зависит от купонов, ставок и комиссий; главный риск — процентный и кредитный риск внутри фонда.",
    "Индексный фонд": "Фонд, повторяющий рыночный индекс. Доход зависит от динамики рынка; главный риск — рыночная просадка и валюта активов.",
    "Акция как класс": "Долевая ценная бумага как учебный класс актива. Доход не гарантирован; главный риск — высокая волатильность и просадка рынка.",
}


def render() -> None:
    st.markdown("<div class='lab-page-header'><div><h2>Проверить инструмент</h2><div class='lab-page-kicker'>Смоделируйте один финансовый инструмент и оцените параметры до добавления в сценарий.</div></div><span class='lab-pill'>Предварительная оценка</span></div>", unsafe_allow_html=True)
    disclaimer(SHORT_DISCLAIMER)
    st.markdown("<div class='lab-status-banner'>Информация носит приблизительный характер и не является инвестиционной рекомендацией.</div>", unsafe_allow_html=True)
    tabs = st.tabs(INSTRUMENT_TABS)
    for tab, instrument_type in zip(tabs, INSTRUMENT_TABS):
        with tab:
            if instrument_type == "Вклад": _deposit_tab()
            elif instrument_type == "Накопительный счёт": _savings_tab()
            elif instrument_type in {"ОФЗ", "Корпоративная облигация"}: _bond_tab(instrument_type)
            else: _fund_tab(instrument_type)


def _deposit_tab() -> None:
    st.caption(INSTRUMENT_EXPLAINERS["Вклад"])
    left, right = st.columns([1.2, .85])
    with left:
        amount = st.number_input("Сумма", min_value=0.0, value=100000.0, step=1000.0, key="dep_amount")
        rate = st.number_input("Ставка, %", value=8.0, step=0.25, key="dep_rate", help="Годовая ставка, которую пользователь сам вводит для проверки сценария.")
        months = st.slider("Срок, месяцев", 1, 60, 12, key="dep_months")
        capitalization = st.checkbox("Капитализация", value=True, key="dep_cap")
        early = st.checkbox("Возможность досрочного снятия", value=True, key="dep_early")
        tax = st.number_input("Налог, %", 0.0, 100.0, 13.0, key="dep_tax")
        insurance = st.number_input("Лимит страхования", min_value=0.0, value=1400000.0, step=10000.0, key="dep_ins")
        currency = st.selectbox("Валюта", ["RUB", "USD", "EUR"], key="dep_cur")
    with right:
        calc = calculate_deposit(amount, rate, months, capitalization, early, tax, insurance, currency)
        _instrument_result("Вклад", amount, rate, 0.5, 1, 0.0, tax, calc)


def _savings_tab() -> None:
    st.caption(INSTRUMENT_EXPLAINERS["Накопительный счёт"])
    left, right = st.columns([1.2, .85])
    with left:
        amount = st.number_input("Сумма", min_value=0.0, value=100000.0, step=1000.0, key="sav_amount")
        rate = st.number_input("Ставка, %", value=7.0, step=0.25, key="sav_rate")
        months = st.slider("Срок, месяцев", 1, 36, 6, key="sav_months")
        min_balance = st.number_input("Минимальный остаток", min_value=0.0, value=50000.0, step=1000.0, key="sav_min")
        st.selectbox("Условия начисления", ["на ежедневный остаток", "на минимальный остаток", "по периодам"], key="sav_terms")
        tax = st.number_input("Налог, %", 0.0, 100.0, 13.0, key="sav_tax")
        withdrawals = st.checkbox("Возможность снятия", value=True, key="sav_with")
    with right:
        calc = calculate_savings_account(amount, rate, months, min_balance, tax, withdrawals)
        _instrument_result("Накопительный счёт", amount, rate, 0.5, 1, 0.0, tax, calc)


def _bond_tab(kind: str) -> None:
    st.caption(INSTRUMENT_EXPLAINERS[kind])
    left, right = st.columns([1.2, .85])
    with left:
        amount = st.number_input("Сумма инвестиций", min_value=0.0, value=100000.0, step=1000.0, key=f"{kind}_amount")
        nkd = st.number_input("НКД", min_value=0.0, value=41.27 if kind == "ОФЗ" else 12.0, step=0.01, key=f"{kind}_nkd", help="Накопленный купонный доход: часть купона, которую покупатель обычно компенсирует продавцу при покупке облигации.")
        price = st.number_input("Цена, % от номинала", min_value=0.0, value=98.5, step=0.1, key=f"{kind}_price", help="Если облигация стоит 98%, она покупается ниже номинала. Если 103% — выше номинала.")
        nominal = st.number_input("Номинал", min_value=1.0, value=1000.0, step=10.0, key=f"{kind}_nominal", help="Сумма, от которой считается купон и которая обычно используется как база погашения.")
        coupon = st.number_input("Купон, %", min_value=0.0, value=10.0 if kind == "ОФЗ" else 8.0, step=0.1, key=f"{kind}_coupon", help="Годовой купон в процентах от номинала, введённый пользователем для расчёта.")
        years = st.number_input("Срок до погашения, лет", min_value=0.1, value=2.8 if kind == "ОФЗ" else 3.0, step=0.1, key=f"{kind}_years", help="Оставшийся срок до планового погашения облигации.")
        frequency = st.selectbox("Периодичность купона", [1, 2, 4, 12], index=1, key=f"{kind}_freq", help="Сколько раз в год выплачивается купон: 1 — ежегодно, 2 — раз в полгода, 4 — ежеквартально, 12 — ежемесячно.")
        if kind == "ОФЗ":
            credit_risk = 0.0
            st.caption("Для ОФЗ кредитный риск в MVP принимается как минимальный/нулевой в рамках модели. Основные риски: процентный риск, продажа до погашения, ликвидность.")
        else:
            corp_rating = st.selectbox("Рейтинг эмитента", ["AAA", "AA", "A", "BBB", "BB и ниже"], key=f"{kind}_corp_rating", help="Чем ниже рейтинг, тем выше условная премия за кредитный риск в модели.")
            st.caption("Рейтинг используется как условная поправка риска в MVP, а не как официальная оценка конкретного эмитента.")
            credit_risk = _bond_credit_risk(kind, corp_rating)
            st.number_input("Спред к ОФЗ, %", min_value=0.0, value=2.0, step=0.1, key=f"{kind}_spread", help="Дополнительная доходность к условной государственной кривой; в MVP отображается как справочный ввод.")
        liquidity = st.number_input("Ликвидность, дней", min_value=0, value=3 if kind == "ОФЗ" else 15, key=f"{kind}_liq", help="Оценка количества дней, за которое пользователь ожидает выйти из инструмента без существенного ухудшения цены.")
        commission = st.number_input("Комиссия, %", 0.0, 100.0, 0.10, key=f"{kind}_com", help="Комиссионная нагрузка, которую пользователь хочет учесть в расчёте.")
        include_tax = st.checkbox("Учитывать налог", value=True, key=f"{kind}_inc_tax")
        tax = st.number_input("Ставка налога, %", 0.0, 100.0, 13.0, key=f"{kind}_tax", help="Налоговая ставка для приблизительной оценки после налогов.") if include_tax else 0.0
    with right:
        calc = calculate_bond(amount, nkd, price, nominal, coupon, years, int(frequency), commission, tax, credit_risk)
        _instrument_result(kind, amount, calc["yield_to_maturity_approx"], 6 if kind == "ОФЗ" else 10, liquidity, commission, tax, calc)


def _fund_tab(kind: str) -> None:
    st.caption(INSTRUMENT_EXPLAINERS[kind])
    left, right = st.columns([1.2, .85])
    with left:
        amount = st.number_input("Сумма", min_value=0.0, value=100000.0, step=1000.0, key=f"{kind}_amount")
        defaults = _fund_defaults(kind)
        expected = st.number_input("Ожидаемая доходность, %", value=defaults["expected"], step=0.25, key=f"{kind}_ret", help="Пользовательская оценка годовой доходности для сценарного расчёта, не прогноз сервиса.")
        volatility = st.number_input("Волатильность, %", min_value=0.0, value=defaults["volatility"], step=0.25, key=f"{kind}_vol", help="Оценка колебаний стоимости инструмента: выше значение — сильнее возможные просадки.")
        fee = st.number_input("Комиссия фонда, %", min_value=0.0, value=defaults["fee"], step=0.05, key=f"{kind}_fee", help="Годовая комиссия фонда или аналогичная регулярная нагрузка.")
        currency = st.selectbox("Валюта", ["RUB", "USD", "EUR"], key=f"{kind}_cur")
        if kind in {"Индексный фонд", "Акция как класс"}: st.selectbox("Регион", ["Россия", "США", "Европа", "Глобальный"], key=f"{kind}_region")
        months = st.slider("Срок, месяцев", 1, 240, defaults["months"], key=f"{kind}_months")
        tax = st.number_input("Налог, %", 0.0, 100.0, 13.0, key=f"{kind}_tax", help="Налоговая ставка для приблизительного расчёта результата после налогов.")
        liquidity = st.number_input("Биржевая ликвидность, дней", min_value=0, value=2, key=f"{kind}_liq", help="Сколько дней, по оценке пользователя, может занять выход из биржевого инструмента.")
    with right:
        calc = calculate_fund(amount, expected, fee, months, tax)
        _instrument_result(kind, amount, expected, volatility, liquidity, fee, tax, calc, currency=currency)


def _instrument_result(kind: str, amount: float, expected_return: float, volatility: float, liquidity: float, fee: float, tax: float, calc: dict, currency: str = "RUB") -> None:
    df = pd.DataFrame([{"scenario": f"Проверка: {kind}", "instrument": kind, "ticker": "USER", "asset_class": _asset_class(kind), "country": "Пользовательский ввод", "currency": currency, "market_value": amount, "expected_return_pct": expected_return, "volatility_pct": volatility, "liquidity_days": liquidity, "annual_fee_pct": fee, "tax_pct": tax}])
    result = analyze_scenarios(df, st.session_state["investment_lab_assumptions"], st.session_state["investment_lab_constraints"])
    row = result["summary"].iloc[0]
    st.markdown("<div class='lab-metric-strip'>", unsafe_allow_html=True)
    kpi_card("Ожидаемая стоимость", format_money(calc.get("final_after_tax", calc.get("final_amount", amount)), "₽"), "По введённым параметрам")
    kpi_card("Ориентир дохода", format_pct(calc.get("yield_to_maturity_approx", row["net_return_pct"])), "После налогов и комиссий")
    kpi_card("Стресс-просадка", format_pct(row["worst_stress_impact_pct"]), "Худшая стресс-проверка")
    kpi_card("Ликвидность", str(row["liquidity_label"]), f"{int(liquidity)} дн.")
    kpi_card("Риск", str(row["risk_label"]), "Интегральная оценка")
    kpi_card("Сложность", str(row["complexity_label"]), "Оценка понимания")
    st.markdown("</div>", unsafe_allow_html=True)
    risk_chips(result["flags"])
    table_card("Детали расчёта", pd.DataFrame([calc]))
    st.markdown("<div class='lab-panel'><h3>Что проверить самостоятельно</h3><ul><li>Условия досрочного выхода и доступность ликвидности.</li><li>Налоги, комиссии и возможные скрытые издержки.</li><li>Соответствие горизонта инструмента вашему сроку.</li></ul></div>", unsafe_allow_html=True)
    target_scenario = _target_scenario_select(kind)
    if st.button("Добавить этот инструмент в сценарии", key=f"add_{kind}", use_container_width=True):
        scenario_name = _add_instrument_to_scenarios(df.iloc[0].to_dict(), target_scenario)
        if scenario_name is None:
            st.warning("В MVP можно сравнить до 5 сценариев. Выберите существующий сценарий или удалите один из сценариев.")
        else:
            st.success(f"Инструмент добавлен в сценарий «{scenario_name}». Это не является предложением покупки.")


def _bond_credit_risk(kind: str, rating: str) -> float:
    if kind == "ОФЗ":
        return 0.0
    # Важно: это сценарная поправка кредитного риска, а не рыночная оценка доходности конкретной облигации.
    return {"AAA": 0.3, "AA": 0.6, "A": 1.0, "BBB": 1.8, "BB и ниже": 3.5}.get(str(rating), 2.0)


def _target_scenario_select(kind: str) -> str:
    rows = st.session_state.setdefault("investment_lab_scenarios", [])
    existing_scenarios = _existing_scenarios(rows)
    options = [*existing_scenarios] if len(existing_scenarios) >= 5 else ["Новый сценарий", *existing_scenarios]
    return st.selectbox(
        "Куда добавить инструмент",
        options,
        key=f"target_scenario_{kind}",
        help="Выберите существующий пользовательский сценарий или создайте новый сценарий для этого инструмента.",
    )


def _add_instrument_to_scenarios(row: dict, target_scenario: str) -> str | None:
    rows = st.session_state.setdefault("investment_lab_scenarios", [])
    existing_scenarios = _existing_scenarios(rows)
    if target_scenario == "Новый сценарий":
        if len(existing_scenarios) >= 5:
            return None
        scenario_name = f"Сценарий {len(existing_scenarios) + 1}"
    else:
        scenario_name = target_scenario
    payload = row | {"scenario": scenario_name}
    rows.append(payload)
    return scenario_name


def _existing_scenarios(rows: list[dict]) -> list[str]:
    result = []
    for item in rows:
        raw = item.get("scenario")
        if raw is None:
            continue
        value = str(raw).strip()
        if value:
            result.append(value)
    return sorted(set(result))


def _asset_class(kind: str) -> str:
    if kind in {"Вклад", "Накопительный счёт", "Фонд денежного рынка"}: return "Денежные средства"
    if kind in {"ОФЗ", "Корпоративная облигация", "Облигационный фонд"}: return "Облигации"
    return "Акции"


def _fund_defaults(kind: str) -> dict[str, float | int]:
    if kind == "Фонд денежного рынка":
        return {"expected": 6.0, "volatility": 2.0, "fee": 0.3, "months": 12}
    if kind == "Облигационный фонд":
        return {"expected": 8.0, "volatility": 7.0, "fee": 0.6, "months": 36}
    if kind == "Акция как класс":
        return {"expected": 10.0, "volatility": 28.0, "fee": 0.1, "months": 60}
    return {"expected": 10.0, "volatility": 22.0, "fee": 0.8, "months": 60}

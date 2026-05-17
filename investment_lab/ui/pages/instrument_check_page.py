from __future__ import annotations

import pandas as pd
import streamlit as st

from investment_lab.data.legal_texts import SHORT_DISCLAIMER
from investment_lab.data.mockup_metrics import MOCKUP_OFZ
from investment_lab.engine.bond_calculator import calculate_bond
from investment_lab.engine.deposit_calculator import calculate_deposit, calculate_savings_account
from investment_lab.engine.fund_calculator import calculate_fund
from investment_lab.engine.scenario_comparator import analyze_scenarios
from investment_lab.ui.components import disclaimer, kpi_card, risk_chips, table_card
from investment_lab.ui.formatters import format_money, format_pct

INSTRUMENT_TABS = ["Вклад", "Накопительный счёт", "ОФЗ", "Корпоративная облигация", "Фонд денежного рынка", "Индексный фонд"]


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
    left, right = st.columns([1.2, .85])
    with left:
        amount = st.number_input("Сумма", min_value=0.0, value=100000.0, step=1000.0, key="dep_amount")
        rate = st.number_input("Ставка, %", value=8.0, step=0.25, key="dep_rate")
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
    left, right = st.columns([1.2, .85])
    with left:
        amount = st.number_input("Сумма инвестиций", min_value=0.0, value=100000.0, step=1000.0, key=f"{kind}_amount")
        nkd = st.number_input("НКД", min_value=0.0, value=41.27 if kind == "ОФЗ" else 12.0, step=0.01, key=f"{kind}_nkd")
        price = st.number_input("Цена, % от номинала", min_value=0.0, value=98.5, step=0.1, key=f"{kind}_price")
        nominal = st.number_input("Номинал", min_value=1.0, value=1000.0, step=10.0, key=f"{kind}_nominal")
        coupon = st.number_input("Купон, %", min_value=0.0, value=10.0 if kind == "ОФЗ" else 8.0, step=0.1, key=f"{kind}_coupon")
        years = st.number_input("Срок до погашения, лет", min_value=0.1, value=2.8 if kind == "ОФЗ" else 3.0, step=0.1, key=f"{kind}_years")
        frequency = st.selectbox("Периодичность купона", [1, 2, 4, 12], index=1, key=f"{kind}_freq")
        rating = st.selectbox("Кредитный риск (рейтинг эмитента)", ["A (низкий риск)", "BBB (средний риск)", "BB и ниже (высокий риск)"], key=f"{kind}_rating")
        credit_risk = {"A (низкий риск)": 0.0, "BBB (средний риск)": 1.5, "BB и ниже (высокий риск)": 3.0}[rating] if kind == "ОФЗ" else 2.0
        liquidity = st.number_input("Ликвидность, дней", min_value=0, value=3 if kind == "ОФЗ" else 15, key=f"{kind}_liq")
        commission = st.number_input("Комиссия, %", 0.0, 100.0, 0.10, key=f"{kind}_com")
        include_tax = st.checkbox("Учитывать налог", value=True, key=f"{kind}_inc_tax")
        tax = st.number_input("Ставка налога, %", 0.0, 100.0, 13.0, key=f"{kind}_tax") if include_tax else 0.0
        if kind == "Корпоративная облигация":
            st.selectbox("Рейтинг эмитента", ["AAA", "AA", "A", "BBB", "BB и ниже"], key=f"{kind}_corp_rating")
            st.number_input("Спред к ОФЗ, %", min_value=0.0, value=2.0, step=0.1, key=f"{kind}_spread")
    with right:
        calc = calculate_bond(amount, nkd, price, nominal, coupon, years, int(frequency), commission, tax, credit_risk)
        _instrument_result(kind, amount, calc["yield_to_maturity_approx"], 6 if kind == "ОФЗ" else 10, liquidity, commission, tax, calc)


def _fund_tab(kind: str) -> None:
    left, right = st.columns([1.2, .85])
    with left:
        amount = st.number_input("Сумма", min_value=0.0, value=100000.0, step=1000.0, key=f"{kind}_amount")
        expected = st.number_input("Ожидаемая доходность, %", value=6.0 if kind == "Фонд денежного рынка" else 10.0, step=0.25, key=f"{kind}_ret")
        volatility = st.number_input("Волатильность, %", min_value=0.0, value=2.0 if kind == "Фонд денежного рынка" else 22.0, step=0.25, key=f"{kind}_vol")
        fee = st.number_input("Комиссия фонда, %", min_value=0.0, value=0.3 if kind == "Фонд денежного рынка" else 0.8, step=0.05, key=f"{kind}_fee")
        currency = st.selectbox("Валюта", ["RUB", "USD", "EUR"], key=f"{kind}_cur")
        if kind == "Индексный фонд": st.selectbox("Регион", ["Россия", "США", "Европа", "Глобальный"], key=f"{kind}_region")
        months = st.slider("Срок, месяцев", 1, 240, 12 if kind == "Фонд денежного рынка" else 60, key=f"{kind}_months")
        tax = st.number_input("Налог, %", 0.0, 100.0, 13.0, key=f"{kind}_tax")
        liquidity = st.number_input("Биржевая ликвидность, дней", min_value=0, value=2, key=f"{kind}_liq")
    with right:
        calc = calculate_fund(amount, expected, fee, months, tax)
        _instrument_result(kind, amount, expected, volatility, liquidity, fee, tax, calc, currency=currency)


def _instrument_result(kind: str, amount: float, expected_return: float, volatility: float, liquidity: float, fee: float, tax: float, calc: dict, currency: str = "RUB") -> None:
    df = pd.DataFrame([{"scenario": f"Проверка: {kind}", "instrument": kind, "ticker": "USER", "asset_class": _asset_class(kind), "country": "Пользовательский ввод", "currency": currency, "market_value": amount, "expected_return_pct": expected_return, "volatility_pct": volatility, "liquidity_days": liquidity, "annual_fee_pct": fee, "tax_pct": tax}])
    result = analyze_scenarios(df, st.session_state["investment_lab_assumptions"], st.session_state["investment_lab_constraints"])
    row = result["summary"].iloc[0]
    if kind == "ОФЗ":
        kpi_card("Ожидаемая стоимость", format_money(MOCKUP_OFZ["final_value"], "₽"), f"+{MOCKUP_OFZ['final_delta_pct']:.1f}%")
        kpi_card("Ориентир дохода (IRR)", format_pct(MOCKUP_OFZ["irr_pct"]), "Годовых")
        kpi_card("Стресс-просадка", format_pct(MOCKUP_OFZ["stress_drawdown_pct"]), "Кризис 2008")
        kpi_card("Ликвидность", f"{MOCKUP_OFZ['liquidity_days']} дня", MOCKUP_OFZ["liquidity_label"])
        kpi_card("Риск", MOCKUP_OFZ["risk_label"], "Интегральная оценка")
        kpi_card("Сложность", MOCKUP_OFZ["complexity_label"], "Оценка понимания инструмента")
        st.markdown("<h3>Ключевые риск-флаги</h3><span class='lab-risk-chip Medium'>Процентный риск</span><span class='lab-risk-chip Medium'>Продажа до погашения</span><span class='lab-risk-chip High'>Кредитный риск эмитента</span><span class='lab-risk-chip Medium'>Реинвестирование купонов</span>", unsafe_allow_html=True)
        table_card("Детали расчёта", pd.DataFrame([{**calc, "mockup_final_value": MOCKUP_OFZ["final_value"], "mockup_irr_pct": MOCKUP_OFZ["irr_pct"]}]))
        return
    kpi_card("Ожидаемая стоимость", format_money(calc.get("final_after_tax", calc.get("final_amount", amount)), "₽"), "По введённым параметрам")
    kpi_card("Ориентир дохода", format_pct(row["net_return_pct"]), "После налогов и комиссий")
    kpi_card("Риск / ликвидность / сложность", f"{row['risk_label']} · {row['liquidity_label']} · {row['complexity_label']}", "Оценки 1–5")
    risk_chips(result["flags"])
    table_card("Детали расчёта", pd.DataFrame([calc]))


def _asset_class(kind: str) -> str:
    if kind in {"Вклад", "Накопительный счёт", "Фонд денежного рынка"}: return "Денежные средства"
    if kind in {"ОФЗ", "Корпоративная облигация"}: return "Облигации"
    return "Акции"

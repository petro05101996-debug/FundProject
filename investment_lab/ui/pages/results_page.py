from __future__ import annotations

from html import escape

import pandas as pd
import streamlit as st

from investment_lab.data.legal_texts import REPORT_CHECKLIST, REPORT_DISCLAIMER, SHORT_DISCLAIMER
from investment_lab.domain.models import ScenarioAssumptions
from investment_lab.engine.report_builder import build_cashflow_table
from investment_lab.engine.scenario_comparator import analyze_scenarios
from investment_lab.ui.charts import cashflow_donut, drawdown_chart, portfolio_allocation_donut, scenario_projection_chart, stress_bar
from investment_lab.ui.components import disclaimer, empty_state, kpi_card, risk_chips, table_card
from investment_lab.ui.layout import go_to


def render() -> None:
    top_left, top_right = st.columns([1.5, .6])
    with top_left:
        st.markdown("<h2>Итог по выбранным пользователем сценариям</h2><div class='lab-page-kicker'>Сводная панель результатов, стресс-метрик и риск-флагов.</div>", unsafe_allow_html=True)
    with top_right:
        if st.button("Сформировать аналитический отчёт", type="primary", use_container_width=True):
            st.session_state["investment_lab_report_ready"] = True
            go_to("Аналитический отчёт")
    disclaimer(SHORT_DISCLAIMER)
    result = st.session_state.get("investment_lab_results") or analyze_scenarios(pd.DataFrame(st.session_state["investment_lab_scenarios"]), st.session_state["investment_lab_assumptions"], st.session_state["investment_lab_constraints"])
    st.session_state["investment_lab_results"] = result
    if result["summary"].empty:
        empty_state("Расчёт ещё не выполнен", "Заполните параметры и нажмите “Рассчитать”", "Перейдите в раздел сравнения сценариев или проверки портфеля.")
        return

    assumptions = st.session_state["investment_lab_assumptions"]
    display_summary = _summary_with_what_if(result["summary"].copy(), assumptions.horizon_years)
    display_summary = display_summary.sort_values("constraint_fit_score", ascending=False).reset_index(drop=True)
    leader = display_summary.iloc[0]
    cashflows = build_cashflow_table(display_summary, assumptions.horizon_years)
    leader_cashflows = cashflows[cashflows["scenario"] == leader["scenario"]] if "scenario" in cashflows.columns else cashflows
    reasons = (
        f"ликвидность {leader['liquid_within_30d_pct']:.1f}%, "
        f"стресс-просадка {leader['worst_stress_impact_pct']:.1f}%, "
        f"концентрация {leader['max_position_pct']:.1f}%"
    )
    st.markdown(
        f"<div class='lab-status-ok'>✓ Сценарий «<strong>{escape(str(leader['scenario']))}</strong>» имеет наибольшее соответствие введённым ограничениям среди пользовательских сценариев: {escape(reasons)}.<br><small>{escape(REPORT_DISCLAIMER)}</small></div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "<div class='lab-kpi-row-6'>"
        f"<div class='lab-card lab-kpi-card'><div class='lab-kpi-label'>Базовый результат</div><div class='lab-kpi-value'>{leader['projected_value']:,.0f} ₽</div><p>медианный результат за {assumptions.horizon_years} лет</p></div>".replace(',', ' ')
        + f"<div class='lab-card lab-kpi-card'><div class='lab-kpi-label'>Стресс-результат</div><div class='lab-kpi-value'>{leader['stress_value']:,.0f} ₽</div><p>медианный результат за {assumptions.horizon_years} лет</p></div>".replace(',', ' ')
        + f"<div class='lab-card lab-kpi-card'><div class='lab-kpi-label'>Стресс-просадка</div><div class='lab-kpi-value'>{leader['worst_stress_impact_pct']:.1f}%</div><p>макс. просадка за {assumptions.horizon_years} лет</p></div>"
        + f"<div class='lab-card lab-kpi-card'><div class='lab-kpi-label'>Ликвидность</div><div class='lab-kpi-value'>{escape(str(leader['liquidity_label']))}</div><p>средняя оценка</p></div>"
        + f"<div class='lab-card lab-kpi-card'><div class='lab-kpi-label'>Риск</div><div class='lab-kpi-value'>{escape(str(leader['risk_label']))}</div><p>средняя оценка</p></div>"
        + f"<div class='lab-card lab-kpi-card'><div class='lab-kpi-label'>Сложность</div><div class='lab-kpi-value'>{escape(str(leader['complexity_label']))}</div><p>средняя оценка</p></div>"
        + "</div>",
        unsafe_allow_html=True,
    )

    main, side = st.columns([1.55, .75])
    with main:
        table_card("Таблица сравнения сценариев", _summary_for_user(display_summary))
        st.plotly_chart(scenario_projection_chart(display_summary, assumptions.horizon_years), use_container_width=True)
        st.plotly_chart(drawdown_chart(display_summary), use_container_width=True)
        st.plotly_chart(cashflow_donut(cashflows), use_container_width=True)
    with side:
        st.markdown("<div class='lab-right-panel'><h3>Риск-паспорт</h3>", unsafe_allow_html=True)
        kpi_card("Риск", str(leader["risk_label"]), "Интегральная оценка")
        kpi_card("Ликвидность", str(leader["liquidity_label"]), "Оценка 1–5")
        kpi_card("Сложность", str(leader["complexity_label"]), "Оценка 1–5")
        st.markdown("<h3>Риск-флаги</h3>", unsafe_allow_html=True)
        risk_chips(result["flags"])
        st.markdown("<h3>Чек-лист перед самостоятельным решением</h3>", unsafe_allow_html=True)
        for item in REPORT_CHECKLIST[:4]:
            st.markdown(f"- [ ] {item}")
        st.markdown("</div>", unsafe_allow_html=True)
        st.plotly_chart(portfolio_allocation_donut(result["asset_allocation"], scenario=str(leader["scenario"]), total_value=float(leader["portfolio_value"])), use_container_width=True)

    st.markdown("### Техническая чувствительность")
    st.info("Это техническая проверка чувствительности, а не предложенный портфель. Сервис не предлагает эти доли: он показывает, как изменятся метрики, если пользователь сам задаст условные параметры.")
    what_if_view, what_if_flags, what_if_cashflows = _render_what_if_controls(
        display_summary,
        result["flags"],
        assumptions,
        st.session_state["investment_lab_constraints"],
    )
    table_card("Результат технической чувствительности", _summary_for_user(what_if_view))

    with st.expander("Показать расчёты"):
        table_card("Позиции", result["positions"].round(2))
        st.plotly_chart(stress_bar(result["stress"]), use_container_width=True)
    with st.expander("Расчётные допущения"):
        st.json(result["assumptions"])
    with st.expander("Ограничения анализа"):
        for limitation in result["limitations"]:
            st.write(f"- {limitation}")


def _summary_for_user(summary: pd.DataFrame) -> pd.DataFrame:
    columns = {
        "scenario": "Сценарий",
        "projected_value": "Базовая стоимость",
        "stress_value": "Стоимость после стресса",
        "liquidity_label": "Ликвидность",
        "risk_label": "Риск",
        "max_position_pct": "Концентрация, %",
        "status": "Статус по ограничениям",
    }
    existing = [column for column in columns if column in summary.columns]
    return summary[existing].rename(columns=columns).round(2)


def _summary_with_what_if(summary: pd.DataFrame, horizon_years: int) -> pd.DataFrame:
    """Prepare user-calculated summary for the result dashboard."""

    prepared = summary.copy()
    if "stress_value" not in prepared.columns:
        prepared["stress_value"] = prepared["projected_value"] * (1 + prepared["worst_stress_impact_pct"] / 100.0)
    if "status" not in prepared.columns:
        prepared["status"] = "Расчётный результат по указанным параметрам"
    prepared["horizon_years"] = horizon_years
    return prepared


def _render_what_if_controls(
    summary: pd.DataFrame,
    base_flags: pd.DataFrame,
    assumptions: ScenarioAssumptions,
    constraints,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Apply transparent what-if overlays without changing saved user data."""

    scenario_options = summary["scenario"].astype(str).tolist() if "scenario" in summary.columns else []
    base_scenario = st.selectbox("Базовый сценарий для what-if", scenario_options, help="Выберите пользовательский сценарий, относительно которого будет построена техническая проверка.") if scenario_options else None

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        rate_shift = st.slider("Ставка, п.п.", -2.0, 2.0, 0.0, 0.5, help="Сдвигает расчётную доходность на выбранное число процентных пунктов.")
    with col2:
        equity_stress = st.slider("Рынок акций", -20.0, 0.0, 0.0, 5.0, help="Добавляет стресс-надбавку к сценариям с высоким риском.")
    with col3:
        early_exit = st.slider("Досрочный выход, мес.", 0, 12, 0, 3, help="Усиливает стресс-просадку как проверка раннего выхода.")
    with col4:
        inflation_shift = st.slider("Инфляция, п.п.", 0.0, 5.0, 0.0, 0.5, help="Снижает расчётную реальную доходность.")

    with st.expander("Техническая чувствительность к условным долям", expanded=False):
        st.caption("Сервис не предлагает эти доли. Это демонстрация того, как изменятся метрики, если пользователь сам задаст условное распределение.")
        a, b, c, d = st.columns(4)
        with a:
            deposit_share = st.slider("Доля вклада", 0, 100, 40, 5)
        with b:
            ofz_share = st.slider("Доля ОФЗ", 0, 100, 25, 5)
        with c:
            fund_share = st.slider("Доля фонда", 0, 100, 20, 5)
        with d:
            equity_share = st.slider("Доля акций", 0, 100, 15, 5)
        share_sum = deposit_share + ofz_share + fund_share + equity_share
        st.write(f"Сумма долей: {share_sum}%")
        if share_sum != 100:
            st.warning("Сумма долей отличается от 100%, расчёт будет нормализован.")

    adjusted = summary.copy()
    adjusted["net_return_pct"] = adjusted["net_return_pct"] + rate_shift - inflation_shift
    risk_multiplier = adjusted["risk_label"].astype(str).map({"Высокий": 1.0, "Средний": 0.55, "Низкий": 0.2}).fillna(0.45)
    adjusted["worst_stress_impact_pct"] = adjusted["worst_stress_impact_pct"] + equity_stress * risk_multiplier - early_exit * 0.35
    adjusted["projected_value"] = adjusted["portfolio_value"] * (1 + adjusted["net_return_pct"] / 100.0) ** assumptions.horizon_years
    adjusted["stress_value"] = adjusted["projected_value"] * (1 + adjusted["worst_stress_impact_pct"] / 100.0)

    base_row = adjusted[adjusted["scenario"].astype(str) == str(base_scenario)].iloc[0] if base_scenario else adjusted.iloc[0]
    allocation_result = _allocation_what_if_result(
        base_row,
        deposit_share,
        ofz_share,
        fund_share,
        equity_share,
        rate_shift,
        inflation_shift,
        assumptions,
        constraints,
    )
    if allocation_result is not None and not allocation_result["summary"].empty:
        allocation_summary = _summary_with_what_if(allocation_result["summary"].copy(), assumptions.horizon_years)
        adjusted = pd.concat([adjusted, allocation_summary], ignore_index=True).sort_values("constraint_fit_score", ascending=False).reset_index(drop=True)
        flags = pd.concat([base_flags, allocation_result["flags"], _what_if_delta_flags(adjusted, equity_stress, early_exit)], ignore_index=True)
    else:
        flags = pd.concat([base_flags, _what_if_delta_flags(adjusted, equity_stress, early_exit)], ignore_index=True)

    cashflows = build_cashflow_table(adjusted, assumptions.horizon_years)
    st.caption("What-if меняет только отображение текущего расчёта и не сохраняется как инвестиционное решение.")
    return adjusted, flags, cashflows


def _allocation_what_if_result(leader, deposit_share: int, ofz_share: int, fund_share: int, equity_share: int, rate_shift: float, inflation_shift: float, assumptions: ScenarioAssumptions, constraints):
    total_share = max(1, deposit_share + ofz_share + fund_share + equity_share)
    total_value = float(leader["portfolio_value"])
    rows = [
        ("Вклад", "Денежные средства", deposit_share, 7.0, 0.5, 1, 0.0),
        ("ОФЗ", "Облигации", ofz_share, 8.2, 6.0, 3, 0.1),
        ("Фонд денежного рынка", "Денежные средства", fund_share, 6.3, 2.0, 2, 0.3),
        ("Акция как класс", "Акции", equity_share, 10.0, 28.0, 2, 0.1),
    ]
    what_if_rows = []
    for instrument, asset_class, share, expected, volatility, liquidity_days, fee in rows:
        if share <= 0:
            continue
        what_if_rows.append({
            "scenario": "Техническая чувствительность к условным долям",
            "instrument": instrument,
            "ticker": "WHATIF",
            "asset_class": asset_class,
            "country": "Пользовательский ввод",
            "currency": "RUB",
            "market_value": total_value * share / total_share,
            "expected_return_pct": expected + rate_shift - inflation_shift,
            "volatility_pct": volatility,
            "liquidity_days": liquidity_days,
            "annual_fee_pct": fee,
            "tax_pct": 13.0,
        })
    if not what_if_rows:
        return None
    return analyze_scenarios(pd.DataFrame(what_if_rows), assumptions, constraints)


def _what_if_delta_flags(summary: pd.DataFrame, equity_stress: float, early_exit: int) -> pd.DataFrame:
    rows = []
    if equity_stress < 0:
        rows.append({"scenario": "What-if", "severity": "Medium", "code": "what_if_equity_stress", "title": "Стресс рынка акций", "description": "What-if проверка усиливает просадку для сценариев с рыночным риском.", "metric": f"{equity_stress:.0f}%", "limit": "пользовательский стресс", "flag": "What-if проверка усиливает просадку."})
    if early_exit > 0:
        rows.append({"scenario": "What-if", "severity": "Medium", "code": "what_if_early_exit", "title": "Досрочный выход", "description": "What-if проверка учитывает возможное ухудшение результата при раннем выходе.", "metric": f"{early_exit} мес.", "limit": "пользовательский срок", "flag": "What-if проверка досрочного выхода."})
    if not rows:
        return pd.DataFrame(columns=["scenario", "severity", "code", "title", "description", "metric", "limit", "flag"])
    return pd.DataFrame(rows)

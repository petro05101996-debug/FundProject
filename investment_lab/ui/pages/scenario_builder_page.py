from __future__ import annotations

import io

import pandas as pd
import streamlit as st

from investment_lab.data.legal_texts import FOOTER_DISCLAIMER, SESSION_DATA_NOTICE, SHORT_DISCLAIMER
from investment_lab.data.scenario_templates import SCENARIO_TEMPLATES
from investment_lab.domain.models import SUPPORTED_ASSET_CLASSES, default_instruments, required_instrument_columns
from investment_lab.engine.scenario_comparator import analyze_scenarios
from investment_lab.ui.charts import scenario_score_bar, stress_bar
from investment_lab.ui.components import card, disclaimer, empty_state, kpi_card, privacy_notice, table_card
from investment_lab.ui.layout import go_to


def render() -> None:
    st.markdown("## Сравнить мои варианты")
    disclaimer(SHORT_DISCLAIMER)
    st.markdown("<div class='lab-action-bar'><span>Добавьте сценарий, шаблон или CSV</span><span>Данные хранятся только в текущей сессии</span></div>", unsafe_allow_html=True)
    b1, b2, b3 = st.columns(3)
    with b1:
        if st.button("Добавить сценарий", use_container_width=True):
            rows = st.session_state["investment_lab_scenarios"]
            rows.append(default_instruments()[0] | {"scenario": f"Сценарий {len(set(r.get('scenario') for r in rows)) + 1}"})
            st.rerun()
    with b2:
        if st.button("Добавить из шаблона", use_container_width=True):
            st.session_state["investment_lab_scenarios"].extend(SCENARIO_TEMPLATES[0]["rows"])
            st.rerun()
    with b3:
        if st.button("Очистить", use_container_width=True):
            st.session_state["investment_lab_scenarios"] = []
            st.rerun()

    uploaded = st.file_uploader("Импорт CSV", type=["csv"])
    if uploaded is not None:
        st.session_state["investment_lab_scenarios"] = pd.read_csv(uploaded).to_dict("records")

    data = _ensure_df(pd.DataFrame(st.session_state["investment_lab_scenarios"]))
    if data.empty:
        empty_state("Сценарии ещё не добавлены", "Создайте первый сценарий или используйте шаблон")
        privacy_notice(FOOTER_DISCLAIMER)
        return

    st.markdown("### Карточки сценариев")
    for scenario_name, scenario_df in data.groupby("scenario"):
        total = scenario_df["market_value"].sum()
        card(str(scenario_name), f"Инструментов: {len(scenario_df)} · сумма: {total:,.0f} ₽".replace(",", " "), badge="Сценарий")

    st.markdown("<div class='lab-table-card'><h3>Редактирование сценариев</h3>", unsafe_allow_html=True)
    edited = st.data_editor(
        data,
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True,
        column_config={
            "asset_class": st.column_config.SelectboxColumn("asset_class", options=list(SUPPORTED_ASSET_CLASSES)),
            "market_value": st.column_config.NumberColumn("market_value", min_value=0.0, step=1000.0),
            "expected_return_pct": st.column_config.NumberColumn("expected_return_pct", step=0.25),
            "volatility_pct": st.column_config.NumberColumn("volatility_pct", min_value=0.0, step=0.25),
            "liquidity_days": st.column_config.NumberColumn("liquidity_days", min_value=0, step=1),
            "annual_fee_pct": st.column_config.NumberColumn("annual_fee_pct", min_value=0.0, step=0.05),
            "tax_pct": st.column_config.NumberColumn("tax_pct", min_value=0.0, max_value=100.0, step=0.5),
        },
        key="scenario_builder_editor",
    )
    st.markdown("</div>", unsafe_allow_html=True)
    st.session_state["investment_lab_scenarios"] = edited.to_dict("records")

    actions = st.columns([1, 1, 2])
    with actions[0]:
        if st.button("Вернуть пример", use_container_width=True):
            st.session_state["investment_lab_scenarios"] = default_instruments()
            st.rerun()
    with actions[1]:
        st.download_button("CSV-шаблон", data=_csv_template(), file_name="scenario_template.csv", mime="text/csv", use_container_width=True)
    with actions[2]:
        if st.button("Рассчитать сценарии", type="primary", use_container_width=True):
            result = analyze_scenarios(
                edited,
                st.session_state["investment_lab_assumptions"],
                st.session_state["investment_lab_constraints"],
            )
            st.session_state["investment_lab_results"] = result
            st.session_state["investment_lab_report_ready"] = not result["summary"].empty
            go_to("Итог по сценариям")

    if edited.empty:
        empty_state("Нет сценариев", "Добавьте строки вручную или загрузите CSV, чтобы увидеть сравнение.")
    else:
        preview = analyze_scenarios(edited, st.session_state["investment_lab_assumptions"], st.session_state["investment_lab_constraints"])
        if not preview["summary"].empty:
            c1, c2, c3 = st.columns(3)
            leader = preview["summary"].iloc[0]
            with c1:
                kpi_card("Сценариев", str(preview["summary"]["scenario"].nunique()), "Группировка по пользовательскому названию")
            with c2:
                kpi_card("Статус лидера", str(leader["status"]), "По заданным пользователем ограничениям")
            with c3:
                kpi_card("Риск-флагов", str(len(preview["flags"])), "До формирования отчёта")
            st.plotly_chart(scenario_score_bar(preview["summary"]), use_container_width=True)
            st.plotly_chart(stress_bar(preview["stress"]), use_container_width=True)
    privacy_notice(SESSION_DATA_NOTICE)


def _ensure_df(df: pd.DataFrame) -> pd.DataFrame:
    defaults = pd.DataFrame(default_instruments())
    if df.empty:
        return pd.DataFrame(columns=required_instrument_columns())
    for column in required_instrument_columns():
        if column not in df.columns:
            df[column] = defaults[column].iloc[0] if column in defaults else ""
    return df[required_instrument_columns()]


def _csv_template() -> bytes:
    buffer = io.StringIO()
    pd.DataFrame(default_instruments()).to_csv(buffer, index=False)
    return buffer.getvalue().encode("utf-8")

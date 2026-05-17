from __future__ import annotations

import io
import html

import pandas as pd
import streamlit as st

from investment_lab.data.legal_texts import FOOTER_DISCLAIMER, SESSION_DATA_NOTICE, SHORT_DISCLAIMER
from investment_lab.data.scenario_templates import SCENARIO_TEMPLATES
from investment_lab.domain.models import SUPPORTED_ASSET_CLASSES, default_instruments, required_instrument_columns
from investment_lab.engine.scenario_comparator import analyze_scenarios
from investment_lab.ui.charts import scenario_score_bar, stress_bar
from investment_lab.ui.components import card, disclaimer, empty_state, kpi_card, privacy_notice, table_card
from investment_lab.ui.layout import go_to


MAX_SCENARIOS = 5


def render() -> None:
    st.markdown("<div class='lab-page-header'><div><h2>Сравнить мои варианты</h2><div class='lab-page-kicker'>Добавьте до 5 сценариев для сравнения по доходности, риску, ликвидности и другим параметрам.</div></div><span class='lab-pill'>Конструктор сценариев</span></div>", unsafe_allow_html=True)
    disclaimer(SHORT_DISCLAIMER)
    current_count = _scenario_count(pd.DataFrame(st.session_state["investment_lab_scenarios"]))
    st.markdown(f"<div class='lab-action-bar'><span>Сценариев добавлено: {current_count} из 5</span><span>Минимум для сравнения: 2</span><span>Все варианты введены пользователем</span></div>", unsafe_allow_html=True)
    st.caption("Демонстрационный шаблон нужен только для структуры ввода. Это не рекомендуемый вариант распределения. Заполните параметры так, как вы сами рассматриваете сценарий: сервис не подбирает инструменты вместо вас.")
    b1, b2, b3 = st.columns(3)
    with b1:
        if st.button("Добавить сценарий", use_container_width=True):
            rows = st.session_state["investment_lab_scenarios"]
            scenario_count = len(_scenario_names(rows))
            new_row = default_instruments()[0] | {"scenario": f"Сценарий {scenario_count + 1}"}
            ok, message = can_add_scenarios(rows, [new_row])
            if not ok:
                st.warning(message)
            else:
                rows.append(new_row)
                st.rerun()
    with b2:
        if st.button("Добавить из шаблона", use_container_width=True):
            rows = st.session_state["investment_lab_scenarios"]
            template_rows = SCENARIO_TEMPLATES[0]["rows"]
            ok, message = can_add_scenarios(rows, template_rows)
            if not ok:
                st.warning(message)
            else:
                rows.extend(template_rows)
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
    scenario_groups = list(data.groupby("scenario"))
    for index in range(0, len(scenario_groups), 3):
        cols = st.columns(3)
        for col, (scenario_name, scenario_df) in zip(cols, scenario_groups[index:index + 3]):
            with col:
                total = scenario_df["market_value"].sum()
                shares = scenario_df["market_value"].div(total).fillna(0).mul(100).round(0).astype(int).tolist()[:4] if total else []
                share_badges = "".join(f"<span class='lab-share-pill'>{share}%</span>" for share in shares)
                rows = []
                for _, row in scenario_df.iterrows():
                    amount = f"{row['market_value']:,.0f} ₽".replace(",", " ")
                    share = int(round(row["market_value"] / total * 100)) if total else 0
                    rows.append(
                        "<div class='lab-instrument-row'>"
                        f"<span>{html.escape(str(row['instrument']))}<small>{amount} · {share}%</small></span>"
                        f"<span class='lab-risk-dot'>{html.escape(str(row['asset_class']))}</span>"
                        "</div>"
                    )
                st.markdown(
                    f"<div class='lab-card {'lab-card-strong' if index == 0 else ''}'>"
                    f"<h3>{html.escape(str(scenario_name))} ✎</h3>"
                    f"<div class='lab-page-kicker'>Общая сумма</div><div class='lab-kpi-value'>{total:,.0f} ₽</div>".replace(",", " ")
                    + f"<div class='lab-page-kicker'>Инструменты ({len(scenario_df)})</div><div>{share_badges}</div>"
                    + "".join(rows)
                    + "</div>",
                    unsafe_allow_html=True,
                )
                a1, a2 = st.columns(2)
                with a1:
                    if st.button("＋ Добавить инструмент", key=f"add_row_{scenario_name}", use_container_width=True):
                        st.session_state["investment_lab_scenarios"].append(default_instruments()[0] | {"scenario": scenario_name})
                        st.rerun()
                with a2:
                    if st.button("Дублировать", key=f"dup_{scenario_name}", use_container_width=True):
                        duplicated = [row | {"scenario": f"{scenario_name} копия"} for row in scenario_df.to_dict("records")]
                        ok, message = can_add_scenarios(st.session_state["investment_lab_scenarios"], duplicated)
                        if not ok:
                            st.warning(message)
                        else:
                            st.session_state["investment_lab_scenarios"].extend(duplicated)
                            st.rerun()
                b1, b2 = st.columns(2)
                with b1:
                    if st.button("Удалить", key=f"del_{scenario_name}", use_container_width=True):
                        st.session_state["investment_lab_scenarios"] = [row for row in st.session_state["investment_lab_scenarios"] if row.get("scenario") != scenario_name]
                        st.rerun()
                with b2:
                    with st.expander("Детали"):
                        st.dataframe(scenario_df, hide_index=True, use_container_width=True)

    st.markdown("<div class='lab-table-card'><h3>Редактирование сценариев</h3>", unsafe_allow_html=True)
    edited = st.data_editor(
        data,
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True,
        column_config={
            "scenario": st.column_config.TextColumn("Сценарий"),
            "instrument": st.column_config.TextColumn("Инструмент"),
            "ticker": st.column_config.TextColumn("Код/метка"),
            "asset_class": st.column_config.SelectboxColumn("Класс актива", options=list(SUPPORTED_ASSET_CLASSES)),
            "country": st.column_config.TextColumn("Страна/источник"),
            "currency": st.column_config.TextColumn("Валюта"),
            "market_value": st.column_config.NumberColumn("Сумма", min_value=0.0, step=1000.0),
            "expected_return_pct": st.column_config.NumberColumn("Ожидаемая доходность, %", step=0.25),
            "volatility_pct": st.column_config.NumberColumn("Волатильность, %", min_value=0.0, step=0.25),
            "liquidity_days": st.column_config.NumberColumn("Ликвидность, дней", min_value=0, step=1),
            "annual_fee_pct": st.column_config.NumberColumn("Комиссия, %", min_value=0.0, step=0.05),
            "tax_pct": st.column_config.NumberColumn("Налог, %", min_value=0.0, max_value=100.0, step=0.5),
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
            validation_message = validate_scenario_count(edited)
            if validation_message:
                st.warning(validation_message)
            else:
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
            fit_scenario = preview["summary"].iloc[0]
            with c1:
                kpi_card("Сценариев", str(preview["summary"]["scenario"].nunique()), "Группировка по пользовательскому названию")
            with c2:
                kpi_card("Макс. соответствие", str(fit_scenario["status"]), "По заданным пользователем ограничениям")
            with c3:
                kpi_card("Риск-флагов", str(len(preview["flags"])), "До формирования отчёта")
            table_card("Предпросмотр сравнения", preview["summary"][["scenario", "projected_value", "stress_value", "liquidity_label", "risk_label", "status"]].round(2))
            st.plotly_chart(scenario_score_bar(preview["summary"]), use_container_width=True)
            st.plotly_chart(stress_bar(preview["stress"]), use_container_width=True)
            if not preview["flags"].empty:
                st.markdown("### Что нарушено")
                for _, flag in preview["flags"].head(5).iterrows():
                    st.write(f"- {flag.get('scenario')}: {flag.get('title')} — {flag.get('description')}")
    privacy_notice(SESSION_DATA_NOTICE)


def _scenario_names(rows: list[dict]) -> set[str]:
    return {str(row.get("scenario", "")).strip() for row in rows if str(row.get("scenario", "")).strip()}


def can_add_scenarios(current_rows: list[dict], new_rows: list[dict], max_count: int = MAX_SCENARIOS) -> tuple[bool, str | None]:
    current = _scenario_names(current_rows)
    incoming = _scenario_names(new_rows)
    total = len(current | incoming)
    if total > max_count:
        return False, f"В MVP можно сравнить до {max_count} сценариев. После добавления будет {total}."
    return True, None


def _scenario_count(df: pd.DataFrame) -> int:
    if df.empty or "scenario" not in df.columns:
        return 0
    return int(df["scenario"].dropna().astype(str).str.strip().replace("", pd.NA).dropna().nunique())


def validate_scenario_count(df: pd.DataFrame) -> str | None:
    scenario_count = _scenario_count(df)
    if scenario_count < 2:
        return "Для сравнения добавьте минимум 2 пользовательских сценария."
    if scenario_count > 5:
        return "В MVP можно сравнить до 5 сценариев."
    return None


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

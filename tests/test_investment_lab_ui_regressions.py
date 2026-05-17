from pathlib import Path

import pandas as pd

from investment_lab.engine.bond_calculator import calculate_bond
from investment_lab.engine.report_builder import build_cashflow_table, export_html_report
from investment_lab.engine.scenario_comparator import analyze_scenarios
from investment_lab.domain.models import ScenarioAssumptions, UserConstraints, default_instruments
from investment_lab.ui.pages.instrument_check_page import _bond_credit_risk
from investment_lab.ui.pages.scenario_builder_page import can_add_scenarios, validate_scenario_count


def test_ofz_calculation_changes_when_user_parameters_change():
    first = calculate_bond(100_000, 41.27, 98.5, 1000, 10.0, 2.8, 2, 0.1, 13.0, 0.0)
    second = calculate_bond(200_000, 41.27, 98.5, 1000, 10.0, 2.8, 2, 0.1, 13.0, 0.0)
    assert first["final_after_tax"] != second["final_after_tax"]
    assert second["final_after_tax"] > first["final_after_tax"]


def test_corporate_bond_rating_changes_credit_risk_and_yield():
    aaa_risk = _bond_credit_risk("Корпоративная облигация", "AAA")
    low_rating_risk = _bond_credit_risk("Корпоративная облигация", "BB и ниже")
    assert aaa_risk < low_rating_risk
    high_quality = calculate_bond(100_000, 12.0, 98.5, 1000, 8.0, 3.0, 2, 0.1, 13.0, aaa_risk)
    low_quality = calculate_bond(100_000, 12.0, 98.5, 1000, 8.0, 3.0, 2, 0.1, 13.0, low_rating_risk)
    assert high_quality["yield_to_maturity_approx"] > low_quality["yield_to_maturity_approx"]


def test_scenario_count_validation_limits_mvp_range():
    one = pd.DataFrame([default_instruments()[0] | {"scenario": "Один"}])
    assert validate_scenario_count(one) == "Для сравнения добавьте минимум 2 пользовательских сценария."

    six_rows = pd.DataFrame([default_instruments()[0] | {"scenario": f"Сценарий {idx}"} for idx in range(6)])
    assert validate_scenario_count(six_rows) == "В MVP можно сравнить до 5 сценариев."

    two_rows = pd.DataFrame([default_instruments()[0] | {"scenario": "A"}, default_instruments()[1] | {"scenario": "B"}])
    assert validate_scenario_count(two_rows) is None


def test_interactive_instrument_page_does_not_import_mockup_ofz():
    source = Path("investment_lab/ui/pages/instrument_check_page.py").read_text(encoding="utf-8")
    assert "MOCKUP_OFZ" not in source


def test_html_report_contains_summary_risk_flags_scenarios_and_disclaimer():
    result = analyze_scenarios(pd.DataFrame(default_instruments()), ScenarioAssumptions(horizon_years=3), UserConstraints())
    html = export_html_report(result)
    assert "Executive summary" in html
    assert "Риск-флаги" in html
    assert "Сценарий" in html
    assert "не является" in html.lower()
    assert "Ограничения анализа" in html


def test_streamlit_report_page_contains_summary_and_risk_passport_sections():
    source = Path("investment_lab/ui/pages/report_page.py").read_text(encoding="utf-8")
    assert "2. Executive summary" in source
    assert "3. Риск-паспорт" in source
    assert "10. Денежные потоки" in source


def test_executive_summary_html_handles_flags_without_title_column():
    from investment_lab.engine.report_builder import _executive_summary_html, build_report_bundle

    result = analyze_scenarios(pd.DataFrame(default_instruments()), ScenarioAssumptions(horizon_years=3), UserConstraints())
    flags_without_title = pd.DataFrame([{"scenario": "A", "severity": "Medium"}])
    html = _executive_summary_html(build_report_bundle(result), result["summary"], flags_without_title)
    assert "Executive" not in html  # helper returns section body only
    assert "Есть риск-флаги, но их структура не распознана" in html


def test_bond_tab_does_not_show_general_rating_select_for_ofz():
    source = Path("investment_lab/ui/pages/instrument_check_page.py").read_text(encoding="utf-8")
    assert "Кредитный риск (рейтинг эмитента)" not in source
    assert "Для ОФЗ кредитный риск" in source
    assert 'if kind == "ОФЗ":\n            credit_risk = 0.0' in source


def test_add_instrument_requires_explicit_target_scenario():
    source = Path("investment_lab/ui/pages/instrument_check_page.py").read_text(encoding="utf-8")
    assert "Куда добавить инструмент" in source
    assert "target_scenario" in source
    assert "scenario_names[0]" not in source
    assert "def _add_instrument_to_scenarios(row: dict, target_scenario: str)" in source


def test_portfolio_editor_has_russian_column_labels():
    source = Path("investment_lab/ui/pages/portfolio_check_page.py").read_text(encoding="utf-8")
    for label in [
        "Инструмент",
        "Код/метка",
        "Класс актива",
        "Страна/источник",
        "Валюта",
        "Сумма",
        "Ожидаемая доходность, %",
        "Волатильность, %",
        "Ликвидность, дней",
        "Комиссия, %",
        "Налог, %",
    ]:
        assert label in source


def test_results_page_sorts_summary_before_selecting_leader():
    source = Path("investment_lab/ui/pages/results_page.py").read_text(encoding="utf-8")
    assert 'sort_values("constraint_fit_score", ascending=False)' in source
    assert "leader = display_summary.iloc[0]" in source



def test_template_addition_cannot_exceed_five_scenarios():
    current = [default_instruments()[0] | {"scenario": f"Сценарий {idx}"} for idx in range(1, 5)]
    incoming = [
        default_instruments()[0] | {"scenario": "Сценарий 5"},
        default_instruments()[0] | {"scenario": "Сценарий 6"},
    ]
    ok, message = can_add_scenarios(current, incoming)
    assert ok is False
    assert "до 5 сценариев" in str(message)


def test_empty_portfolio_stays_empty_after_clear():
    from investment_lab.ui.pages.portfolio_check_page import _ensure_portfolio_df

    df = _ensure_portfolio_df(pd.DataFrame())
    assert df.empty
    assert list(df.columns)


def test_leader_cashflow_is_not_sum_of_all_scenarios():
    result = analyze_scenarios(pd.DataFrame(default_instruments()), ScenarioAssumptions(horizon_years=3), UserConstraints())
    display_summary = result["summary"].sort_values("constraint_fit_score", ascending=False).reset_index(drop=True)
    leader = display_summary.iloc[0]
    cashflows = build_cashflow_table(display_summary, 3)
    leader_cashflows = cashflows[cashflows["scenario"] == leader["scenario"]]
    assert leader_cashflows["income"].sum() <= cashflows["income"].sum()
    assert len(cashflows["scenario"].unique()) > 1


def test_streamlit_report_escapes_scenario_name():
    from investment_lab.engine.report_builder import build_report_bundle
    from investment_lab.ui.pages.report_page import _executive_summary_section

    result = analyze_scenarios(pd.DataFrame(default_instruments()), ScenarioAssumptions(horizon_years=3), UserConstraints())
    result["summary"] = result["summary"].copy()
    best_index = result["summary"]["constraint_fit_score"].idxmax()
    result["summary"].loc[best_index, "scenario"] = "<script>alert(1)</script>"
    html = _executive_summary_section(build_report_bundle(result), result)
    assert "<script>" not in html
    assert "&lt;script&gt;" in html


def test_report_page_uses_user_summary_table_for_comparison():
    source = Path("investment_lab/ui/pages/report_page.py").read_text(encoding="utf-8")
    assert 'table_card("7. Сравнение сценариев", user_summary_table(result["summary"]))' in source
    assert 'table_card("7. Сравнение сценариев", result["summary"].round(2))' not in source


def test_instrument_new_scenario_is_hidden_or_blocked_at_limit():
    source = Path("investment_lab/ui/pages/instrument_check_page.py").read_text(encoding="utf-8")
    assert 'len(existing_scenarios) >= 5' in source
    assert 'return None' in source


def test_what_if_is_named_as_technical_sensitivity():
    source = Path("investment_lab/ui/pages/results_page.py").read_text(encoding="utf-8")
    assert "Техническая чувствительность к условным долям" in source
    assert "Базовый сценарий для what-if" in source
    assert "adjusted.iloc[0]," not in source


def test_existing_scenarios_ignores_none():
    from investment_lab.ui.pages.instrument_check_page import _existing_scenarios

    rows = [{"scenario": None}, {"scenario": ""}, {"scenario": " Сценарий 1 "}]
    assert _existing_scenarios(rows) == ["Сценарий 1"]


def test_user_summary_table_has_russian_columns():
    from investment_lab.engine.report_builder import user_summary_table

    summary = pd.DataFrame([
        {
            "scenario": "Сценарий A",
            "projected_value": 110_000,
            "stress_value": 95_000,
            "risk_label": "Средний",
        }
    ])
    table = user_summary_table(summary)
    assert ["Сценарий", "Базовая стоимость", "Стоимость после стресса", "Риск"] == list(table.columns)


def test_user_summary_table_explains_missing_user_columns():
    from investment_lab.engine.report_builder import user_summary_table

    table = user_summary_table(pd.DataFrame([{"technical_only": 1}]))
    assert list(table.columns) == ["Комментарий"]
    assert "Нет пользовательских колонок" in table.iloc[0]["Комментарий"]


def test_user_cashflow_table_has_russian_columns():
    from investment_lab.engine.report_builder import user_cashflow_table

    cashflows = pd.DataFrame([
        {
            "scenario": "Сценарий A",
            "year": 1,
            "income": 1000,
            "fees": 100,
            "taxes": 130,
        }
    ])
    table = user_cashflow_table(cashflows)
    assert ["Сценарий", "Год", "Расчётный доход", "Комиссии", "Налоги"] == list(table.columns)


def test_risk_flag_chips_html_uses_description_when_title_missing():
    from investment_lab.engine.report_builder import _risk_flag_chips_html

    html = _risk_flag_chips_html(pd.DataFrame([{"description": "Проверить ликвидность"}]))
    assert "Проверить ликвидность" in html
    assert "не выявлены" not in html

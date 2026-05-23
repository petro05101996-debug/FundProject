import pandas as pd

from investment_lab.engine.bond_calculator import calculate_bond
from investment_lab.engine.report_builder import (
    _risk_flag_chips_html,
    build_cashflow_table,
    export_html_report,
    user_cashflow_table,
    user_summary_table,
)


def test_ofz_calculation_changes_when_user_parameters_change():
    a = calculate_bond(1_000_000, 0, 98.5, 1000, 10, 3, 2, 0.1, 13, 0)
    b = calculate_bond(2_000_000, 0, 98.5, 1000, 10, 3, 2, 0.1, 13, 0)
    assert a['final_after_tax'] != b['final_after_tax']


def test_html_report_contains_summary_risk_flags_scenarios_and_disclaimer():
    result = {
        'positions': [{'scenario': 'A', 'instrument': 'Вклад'}],
        'summary': [{'scenario': 'A', 'projected_value': 120000, 'liquidity_label': 'Высокая', 'risk_label': 'Низкий', 'complexity_label': 'Низкая', 'max_position_pct': 40, 'status': 'ok'}],
        'flags': [{'title': 'Высокая концентрация'}],
        'stress': [{'scenario': 'A', 'shock': -20}],
        'limitations': ['Ограничение 1'],
        'assumptions': {'horizon_years': 3},
        'constraints': {'max_single_position_pct': 50},
    }
    html = export_html_report(result)
    assert 'Дисклеймер' in html
    assert 'Риск-флаги' in html
    assert 'Выбранные сценарии' in html
    assert 'инвестиционной рекомендацией' in html


def test_leader_cashflow_is_not_sum_of_all_scenarios():
    summary = pd.DataFrame([
        {'scenario': 'A', 'portfolio_value': 100000, 'net_return_pct': 10, 'worst_stress_impact_pct': -10},
        {'scenario': 'B', 'portfolio_value': 200000, 'net_return_pct': 5, 'worst_stress_impact_pct': -5},
    ])
    cashflows = build_cashflow_table(summary, 1)
    leader = cashflows[cashflows['scenario'] == 'A']['contributions'].sum()
    total = cashflows['contributions'].sum()
    assert leader < total


def test_user_summary_table_has_russian_columns():
    summary = pd.DataFrame([{'scenario': 'A', 'projected_value': 100, 'liquidity_label': 'Высокая', 'risk_label': 'Низкий', 'complexity_label': 'Низкая', 'max_position_pct': 10, 'status': 'ok'}])
    table = user_summary_table(summary)
    assert 'Сценарий' in table.columns
    assert 'Базовая стоимость' in table.columns


def test_user_summary_table_explains_missing_user_columns():
    summary = pd.DataFrame([{'foo': 1}])
    table = user_summary_table(summary)
    assert 'Комментарий' in table.columns


def test_user_cashflow_table_has_russian_columns():
    cf = pd.DataFrame([{'scenario': 'A', 'year': 1, 'contributions': 1, 'additional_contributions': 0, 'income': 1, 'fees': 0, 'taxes': 0, 'value_before_stress': 1, 'value_after_stress': 1}])
    table = user_cashflow_table(cf)
    assert 'Сценарий' in table.columns
    assert 'Стоимость после стресса' in table.columns


def test_risk_flag_chips_html_uses_description_when_title_missing():
    flags = pd.DataFrame([{'description': 'Риск из описания'}])
    chips = _risk_flag_chips_html(flags)
    assert 'Риск из описания' in chips

from investment_lab.data.scenario_templates import GUIDED_SCENARIO_TEMPLATES

REQUIRED_IDS = {
    'short_term_cash_parking','six_to_twelve_months','higher_than_deposit','compare_deposit_bond_fund','bond_before_buying','portfolio_health_check','external_idea_check','learn_instrument','beginner_diagnostic'
}

def test_required_templates_exist():
    ids = {t['id'] for t in GUIDED_SCENARIO_TEMPLATES}
    assert REQUIRED_IDS.issubset(ids)

def test_template_contract_fields_present():
    for t in GUIDED_SCENARIO_TEMPLATES:
        assert 'questions' in t and t['questions']
        assert 'default_assumptions' in t
        assert 'unknown_parameter_policy' in t

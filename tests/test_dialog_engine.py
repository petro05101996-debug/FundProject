from investment_lab.engine.dialog_engine import DialogEngine


def test_dialog_unknown_answer_adds_unknown_field():
    e = DialogEngine()
    st = e.start('compare_deposit_bond_fund')
    s1 = e.answer(st['session_state'], st['current_question']['id'], 100000)
    s2 = e.answer(s1['session_state'], s1['current_question']['id'], 'unknown')
    assert 'horizon' in s2['session_state']['unknown_fields']


def test_preview_contains_assumptions_and_unknown_fields():
    e = DialogEngine()
    st = e.start('compare_deposit_bond_fund')
    st = e.answer(st['session_state'], st['current_question']['id'], 100000)
    st = e.answer(st['session_state'], st['current_question']['id'], 'unknown')
    p = e.preview(st['session_state'])
    assert 'assumptions' in p and 'unknown_fields' in p

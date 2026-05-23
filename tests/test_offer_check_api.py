from investment_lab.engine.dialog_engine import DialogEngine
from investment_lab.engine.offer_text_parser import parse_offer_text


def test_offer_template_dialog_starts_without_key_error():
    e = DialogEngine()
    r = e.start('offer_check')
    assert r['current_question']['id'] == 'offer_type'


def test_parse_text_detects_to_wording():
    r = parse_offer_text('Доходность до 18% годовых')
    assert 'return_wording_not_guaranteed' in r['preliminary_flags']

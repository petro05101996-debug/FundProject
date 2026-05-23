from investment_lab.engine.offer_text_parser import parse_offer_text

def test_parse_extracts_return_and_capital_protection():
    r = parse_offer_text('Доходность до 18% годовых, защита капитала 100%, срок 3 года')
    assert r['detected_return_pct'] == 18
    assert 'защита капитала' in r['detected_claims']

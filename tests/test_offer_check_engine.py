from investment_lab.engine.offer_check_engine import OfferCheckInput, analyze_offer


def test_unknowns_and_unofficial_source_flags():
    res = analyze_offer(OfferCheckInput(offer_source='telegram', instrument_type='bond', early_exit_type='unknown', fees_known=False, expected_return_pct=18))
    codes = {f['code'] for f in res['red_flags']}
    assert 'unofficial_source' in codes
    assert 'unknown_early_exit' in codes
    assert 'unknown_fees' in codes
    assert res['questions_to_ask']
    assert 'base_scenario' in res and 'stress_scenario' in res

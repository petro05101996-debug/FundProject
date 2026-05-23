from investment_lab.engine.offer_check_engine import OfferCheckInput, analyze_offer

BANNED=['покупайте','не покупайте','рекомендуем','лучший вариант','мошенничество']

def test_offer_result_safe_wording():
    r = analyze_offer(OfferCheckInput())
    text = str(r).lower()
    for b in BANNED:
        assert b not in text

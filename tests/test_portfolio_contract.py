from app.api.portfolio import portfolio_check, PortfolioCheckRequest


def test_portfolio_check_contract_fields():
    req = PortfolioCheckRequest(
        positions=[{"scenario":"Портфель","instrument":"ОФЗ","ticker":"OFZ","asset_class":"Облигации","country":"RU","currency":"RUB","market_value":100000,"expected_return_pct":9,"volatility_pct":7,"liquidity_days":3,"annual_fee_pct":0.2,"tax_pct":13}],
        assumptions={},
        constraints={},
    )
    j = portfolio_check(req)
    assert 'concentration' in j and 'top2_pct' in j['concentration']
    assert 'liquidity_label' in j
    assert 'fees_annual_pct' in j
    assert 'weak_points' in j

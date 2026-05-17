from investment_lab.engine.validation import validate_positive_market_values


def test_validation_detects_zero_market_values():
    issues = validate_positive_market_values([{"market_value": 0}, {"market_value": 0}])
    assert issues[0].code == "zero_market_values"

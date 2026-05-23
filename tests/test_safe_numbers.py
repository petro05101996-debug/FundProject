import math
import pandas as pd
from investment_lab.domain.models import ScenarioAssumptions, UserConstraints
from investment_lab.engine.scenario_comparator import analyze_scenarios
from app.converters import result_to_jsonable


def _walk(v):
    if isinstance(v, dict):
        for x in v.values():
            yield from _walk(x)
    elif isinstance(v, list):
        for x in v:
            yield from _walk(x)
    else:
        yield v


def test_no_nan_or_inf_after_jsonable_conversion():
    df = pd.DataFrame([{"scenario":"S1","instrument":"A","ticker":"A","asset_class":"Акции","country":"RU","currency":"RUB","market_value":100000,"expected_return_pct":10,"volatility_pct":20,"liquidity_days":2,"annual_fee_pct":0.5,"tax_pct":13}])
    result = analyze_scenarios(df, ScenarioAssumptions(), UserConstraints())
    payload = result_to_jsonable(result)
    for value in _walk(payload):
        if isinstance(value, float):
            assert math.isfinite(value)

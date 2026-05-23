"""Portfolio-level calculation helpers."""
from __future__ import annotations


def weighted_average(rows: list[dict], value_key: str, weight_key: str = "market_value") -> float:
    total = sum(float(row.get(weight_key, 0) or 0) for row in rows)
    if total <= 0:
        return 0.0
    return sum(float(row.get(weight_key, 0) or 0) / total * float(row.get(value_key, 0) or 0) for row in rows)


def portfolio_metrics(rows: list[dict]) -> dict[str, float]:
    # NOTE: this is a weighted average of instrument volatilities, not full portfolio volatility with correlations.
    total = sum(float(row.get("market_value", 0) or 0) for row in rows)
    sorted_weights = sorted([(float(row.get("market_value", 0) or 0) / total * 100) if total else 0 for row in rows], reverse=True)
    weighted_avg_vol = weighted_average(rows, "volatility_pct")
    return {
        "portfolio_value": total,
        "weighted_return": weighted_average(rows, "expected_return_pct"),
        "weighted_average_volatility": weighted_avg_vol,
        "weighted_volatility": weighted_avg_vol,
        "weighted_liquidity": weighted_average(rows, "liquidity_days"),
        "weighted_fee": weighted_average(rows, "annual_fee_pct"),
        "tax_drag": weighted_average(rows, "tax_pct"),
        "concentration_top1": sorted_weights[0] if sorted_weights else 0.0,
        "concentration_top2": sum(sorted_weights[:2]) if sorted_weights else 0.0,
    }

"""Liquidity diagnostics."""
from __future__ import annotations

from investment_lab.engine.scoring import liquidity_score


def liquidity_diagnostics(liquidity_days: float, asset_class: str = "") -> dict[str, float | str]:
    score, label, note = liquidity_score(liquidity_days, asset_class)
    return {
        "liquidity_score": score,
        "liquidity_label": label,
        "liquidity_days": liquidity_days,
        "stress_liquidity_note": note,
    }

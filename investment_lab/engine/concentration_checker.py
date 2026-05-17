"""Concentration diagnostics."""
from __future__ import annotations


def concentration_metrics(weights_pct: list[float]) -> dict[str, float]:
    ordered = sorted([float(value) for value in weights_pct], reverse=True)
    return {
        "concentration_top1": ordered[0] if ordered else 0.0,
        "concentration_top2": sum(ordered[:2]) if ordered else 0.0,
    }

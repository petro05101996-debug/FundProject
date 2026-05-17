"""Build educational explanation view models."""
from __future__ import annotations

from investment_lab.data.instrument_catalog import INSTRUMENT_CATALOG
from investment_lab.data.knowledge_base import INSTRUMENT_GUIDE


def build_instrument_explanation(name: str) -> dict:
    guide = INSTRUMENT_GUIDE.get(name, {})
    catalog = INSTRUMENT_CATALOG.get(name, {})
    return {
        "name": name,
        "summary": guide.get("summary", "Инструмент не найден в текущей базе знаний."),
        "category": guide.get("category", catalog.get("asset_class", "Категория не задана")),
        "horizon": catalog.get("horizon", "Зависит от пользовательских параметров"),
        "risks": guide.get("risks", []),
        "liquidity": guide.get("liquidity", "Ликвидность зависит от условий инструмента."),
        "checks": catalog.get("checks", []),
        "related": guide.get("compare_with", []),
        "risk_score": catalog.get("risk_score", 3),
        "liquidity_score": catalog.get("liquidity_score", 3),
        "complexity_score": catalog.get("complexity_score", 3),
    }

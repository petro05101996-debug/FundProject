from __future__ import annotations

from fastapi import APIRouter, Query

from investment_lab.data.instrument_catalog import INSTRUMENT_CATALOG
from investment_lab.data.knowledge_base import INSTRUMENT_GUIDE

router = APIRouter()


@router.get('/explain')
def explain(query: str = Query(default='')):
    q = query.lower().strip()
    key = next((name for name in INSTRUMENT_GUIDE if q and q in name.lower()), 'Вклад')
    g = INSTRUMENT_GUIDE.get(key, INSTRUMENT_GUIDE['Вклад'])
    c = INSTRUMENT_CATALOG.get(key, {})
    return {
        'title': key,
        'category': g.get('category', 'Общее'),
        'plain_explanation': g.get('summary', ''),
        'how_income_works': 'Доход зависит от пользовательских допущений, комиссий и налогов.',
        'risks': g.get('risks', []),
        'liquidity': g.get('liquidity', ''),
        'complexity': c.get('complexity_score', 2),
        'tax_notes': 'Налоги считаются по ставке из пользовательского ввода.',
        'what_to_check': c.get('checks', []),
        'related_instruments': g.get('compare_with', []),
        'disclaimer': 'Это не является индивидуальной инвестиционной рекомендацией.',
    }


@router.get('/catalog')
def catalog():
    return {'items': [{'name': k, **v} for k, v in INSTRUMENT_CATALOG.items()]}

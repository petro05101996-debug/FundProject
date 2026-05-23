from __future__ import annotations

SUPPORTED_ASSET_CLASSES = (
    "Акции",
    "Облигации",
    "Денежные средства",
    "Товары",
    "Недвижимость",
    "Альтернативные",
)

ASSET_CLASS_ALIASES = {
    "equity": "Акции", "stock": "Акции", "stocks": "Акции", "акции": "Акции", "акции рф": "Акции", "российские акции": "Акции", "иностранные акции": "Акции", "индексный фонд": "Акции", "фонд акций": "Акции",
    "bond": "Облигации", "bonds": "Облигации", "облигации": "Облигации", "облигации рф": "Облигации", "офз": "Облигации", "корпоративная облигация": "Облигации", "корпоративные облигации": "Облигации", "облигационный фонд": "Облигации", "фонд облигаций": "Облигации",
    "cash": "Денежные средства", "депозит": "Денежные средства", "вклад": "Денежные средства", "накопительный счет": "Денежные средства", "накопительный счёт": "Денежные средства", "денежный рынок": "Денежные средства", "фонд денежного рынка": "Денежные средства", "фонды денежного рынка": "Денежные средства",
    "commodity": "Товары", "commodities": "Товары", "товары": "Товары", "сырье": "Товары", "сырьё": "Товары", "золото": "Товары", "драгметаллы": "Товары",
    "real estate": "Недвижимость", "недвижимость": "Недвижимость", "reit": "Недвижимость",
    "alternative": "Альтернативные", "alternatives": "Альтернативные", "альтернативные": "Альтернативные",
    "пиф": "Альтернативные", "бпиф": "Альтернативные", "etf": "Альтернативные", "фонд": "Альтернативные",
    "mmf": "Денежные средства", "money market fund": "Денежные средства", "еврооблигации": "Облигации",
}


def normalize_asset_class(value: object) -> str:
    text = str(value or "").strip()
    normalized = text.lower().replace("ё", "е")
    for option in SUPPORTED_ASSET_CLASSES:
        if normalized == option.lower().replace("ё", "е"):
            return option
    return ASSET_CLASS_ALIASES.get(normalized, "Альтернативные")


def is_known_asset_class(value: object) -> bool:
    text = str(value or "").strip()
    normalized = text.lower().replace("ё", "е")
    if not normalized:
        return False
    for option in SUPPORTED_ASSET_CLASSES:
        if normalized == option.lower().replace("ё", "е"):
            return True
    return normalized in ASSET_CLASS_ALIASES

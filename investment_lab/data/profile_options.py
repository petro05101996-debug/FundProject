"""User-facing profile choices from the v1 product brief."""
from __future__ import annotations

GOAL_OPTIONS = [
    "Сохранить деньги",
    "Накопить на цель",
    "Получить регулярные выплаты",
    "Проверить уже купленный инструмент",
    "Сравнить варианты",
    "Понять риск портфеля",
]

HORIZON_OPTIONS = {
    "До 3 месяцев": 3,
    "3–6 месяцев": 6,
    "6–12 месяцев": 12,
    "1–3 года": 36,
    "3–5 лет": 60,
    "Больше 5 лет": 84,
}

LIQUIDITY_OPTIONS = {
    "Да, в любой момент": {"may_need_money_early": True, "min_liquidity_pct_30d": 95.0},
    "Возможно через 3–6 месяцев": {"may_need_money_early": True, "min_liquidity_pct_30d": 80.0},
    "Скорее всего нет": {"may_need_money_early": False, "min_liquidity_pct_30d": 50.0},
    "Не знаю": {"may_need_money_early": True, "min_liquidity_pct_30d": 70.0},
}

DRAWDOWN_OPTIONS = {
    "Любая просадка неприятна": 1.0,
    "До 3%": 3.0,
    "До 5%": 5.0,
    "До 10%": 10.0,
    "Больше 10%": 20.0,
    "Не знаю": 10.0,
}

EXPERIENCE_OPTIONS = [
    "Не разбираюсь",
    "Немного понимаю",
    "Уже покупал вклады/облигации/фонды",
    "Опытный пользователь",
]


def option_index(options: list[str], value: object, default: int = 0) -> int:
    """Return a safe index for Streamlit selectbox defaults."""

    try:
        return options.index(str(value))
    except ValueError:
        return default

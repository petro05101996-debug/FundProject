import pytest

from investment_lab.data.instrument_catalog import INSTRUMENT_CATALOG
from investment_lab.data.knowledge_base import INSTRUMENT_GUIDE
from investment_lab.domain.enums import InstrumentKind
from investment_lab.domain.models import SUPPORTED_ASSET_CLASSES
from investment_lab.data.profile_options import DRAWDOWN_OPTIONS, GOAL_OPTIONS, HORIZON_OPTIONS, LIQUIDITY_OPTIONS


def test_v1_instrument_scope_matches_safe_concept():
    expected = {
        "Вклад",
        "Накопительный счёт",
        "ОФЗ",
        "Корпоративная облигация",
        "Фонд денежного рынка",
        "Облигационный фонд",
        "Индексный фонд",
        "Акция как класс",
        "ИИС",
        "ПДС",
    }

    assert expected.issubset(INSTRUMENT_CATALOG)
    assert expected.issubset(INSTRUMENT_GUIDE)
    assert "Криптоактивы" not in SUPPORTED_ASSET_CLASSES


def test_instrument_check_covers_core_calculator_tabs():
    pytest.importorskip("pandas")
    pytest.importorskip("streamlit")
    from investment_lab.ui.pages.instrument_check_page import INSTRUMENT_TABS

    assert "Облигационный фонд" in INSTRUMENT_TABS
    assert "Акция как класс" in INSTRUMENT_TABS


def test_v1_profile_inputs_match_brief():
    assert {
        "Сохранить деньги",
        "Накопить на цель",
        "Получить регулярные выплаты",
        "Проверить уже купленный инструмент",
        "Сравнить варианты",
        "Понять риск портфеля",
    }.issubset(GOAL_OPTIONS)
    assert list(HORIZON_OPTIONS) == ["До 3 месяцев", "3–6 месяцев", "6–12 месяцев", "1–3 года", "3–5 лет", "Больше 5 лет"]
    assert "Да, в любой момент" in LIQUIDITY_OPTIONS
    assert "Любая просадка неприятна" in DRAWDOWN_OPTIONS


def test_instrument_enum_includes_safe_v1_modes():
    assert InstrumentKind.BOND_FUND.value == "Облигационный фонд"
    assert InstrumentKind.EQUITY_CLASS.value == "Акция как класс"
    assert InstrumentKind.IIS.value == "ИИС"
    assert InstrumentKind.PDS.value == "ПДС"

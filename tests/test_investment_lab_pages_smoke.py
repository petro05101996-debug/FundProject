import pytest


def test_all_page_modules_import():
    pytest.importorskip("streamlit")
    from investment_lab.ui.pages import (
        explain_instrument_page,
        instrument_check_page,
        landing_page,
        portfolio_check_page,
        report_page,
        results_page,
        scenario_builder_page,
        scenario_profile_page,
    )

    pages = [
        landing_page,
        scenario_profile_page,
        instrument_check_page,
        scenario_builder_page,
        portfolio_check_page,
        results_page,
        report_page,
        explain_instrument_page,
    ]

    for page in pages:
        assert callable(page.render)


def test_router_has_all_required_pages():
    pytest.importorskip("streamlit")
    from investment_lab.router import PAGE_RENDERERS

    required = {
        "Лендинг",
        "Параметры сценария",
        "Проверить инструмент",
        "Сравнить мои варианты",
        "Проверить портфель",
        "Итог по сценариям",
        "Аналитический отчёт",
        "Объяснить инструмент",
    }

    assert required.issubset(PAGE_RENDERERS.keys())


def test_legal_text_names_are_available():
    from investment_lab.data.legal_texts import (
        FOOTER_DISCLAIMER,
        PRIMARY_DISCLAIMER,
        WHAT_SERVICE_DOES,
        WHAT_SERVICE_DOES_NOT_DO,
    )

    assert PRIMARY_DISCLAIMER
    assert FOOTER_DISCLAIMER
    assert WHAT_SERVICE_DOES
    assert WHAT_SERVICE_DOES_NOT_DO

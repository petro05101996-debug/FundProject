"""Mock data used only for empty states, templates, and UI previews."""

from investment_lab.domain.models import default_instruments

MODE_CARDS = [
    {
        "key": "instrument",
        "title": "Проверить инструмент",
        "description": "Оценить введённые параметры одного инструмента, комиссии, налоги, ликвидность и риск-флаги.",
        "page": "Проверить инструмент",
    },
    {
        "key": "scenario",
        "title": "Сравнить мои варианты",
        "description": "Собрать несколько пользовательских сценариев и сравнить их по ограничениям.",
        "page": "Сравнить мои варианты",
    },
    {
        "key": "portfolio",
        "title": "Проверить портфель",
        "description": "Ввести текущий портфель вручную и увидеть концентрацию, ликвидность и стресс-флаги.",
        "page": "Проверить портфель",
    },
    {
        "key": "explain",
        "title": "Объяснить инструмент",
        "description": "Открыть образовательную карточку по типу инструмента и сравнить основные свойства.",
        "page": "Объяснить инструмент",
    },
]

SCENARIO_TEMPLATE = default_instruments

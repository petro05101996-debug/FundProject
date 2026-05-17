import pytest

from investment_lab.domain.models import SAFE_STATUS_LABELS
from investment_lab.engine.safety_text_guard import assert_safe_status, validate_safe_text


@pytest.mark.parametrize("text", ["рекомендуем этот вариант", "купите инструмент", "optimal portfolio", "best fit", "target price"])
def test_guard_blocks_advisory_phrases(text):
    with pytest.raises(AssertionError):
        validate_safe_text(text)


def test_guard_allows_negative_legal_context():
    validate_safe_text("Материал не является рекомендацией и нужен только для сравнения пользовательских сценариев.")


def test_safe_statuses():
    for status in SAFE_STATUS_LABELS.values():
        assert_safe_status(status)

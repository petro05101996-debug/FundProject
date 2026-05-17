from pathlib import Path

import pytest

from investment_lab.domain.models import SAFE_STATUS_LABELS
from investment_lab.engine.safety_text_guard import assert_safe_texts, find_safety_violations


def test_guard_blocks_positive_advisory_wording():
    violations = find_safety_violations({"bad": "We recommend this instrument as the best fit."})

    assert violations


def test_guard_allows_approved_negative_context():
    assert_safe_texts({"legal": "This is not a recommendation to buy, sell, or hold."})


def test_safe_statuses_do_not_use_advisory_language():
    assert_safe_texts(SAFE_STATUS_LABELS)
    assert "Лучше соответствует заданным ограничениям" in SAFE_STATUS_LABELS.values()


def test_investment_lab_source_copy_passes_safety_guard():
    texts = {}
    for path in Path("investment_lab").rglob("*.py"):
        if "safety_text_guard.py" in str(path):
            continue
        texts[str(path)] = path.read_text(encoding="utf-8")

    assert_safe_texts(texts)

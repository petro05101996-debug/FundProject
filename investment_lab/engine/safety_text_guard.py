"""Safety text guard for non-advisory financial wording.

The guard blocks positive advisory wording while allowing approved negative legal
contexts such as "не является рекомендацией".
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

BANNED_POSITIVE_PATTERNS = [
    r"\bwe\s+recommend\b",
    r"\brecommended\s+(portfolio|scenario|instrument|allocation)\b",
    r"\brecommended\s+scenario\b",
    r"\bbuy\s+now\b",
    r"\bsell\s+now\b",
    r"\bhold\s+this\b",
    r"\bshould\s+(buy|sell|hold)\b",
    r"\bwhat\s+to\s+buy\b",
    r"\bwhere\s+to\s+invest\b",
    r"\bentry\s+point\b",
    r"\btarget\s+price\b",
    r"\bbest\s+investment\b",
    r"\bbest\s+fit\b",
    r"\bsuitable\s+for\s+you\b",
    r"\boptimal\s+portfolio\b",
    r"\bguaranteed\s+(return|profit|yield)\b",
    r"\bpersonal\s+investment\s+advice\b",
    r"\bрекомендуем\b",
    r"\bрекомендуется\b",
    r"\bрекомендованн(ый|ая|ое)\s+портфель\b",
    r"\bкупите\b",
    r"\bпродайте\b",
    r"\bдержите\b",
    r"\bчто\s+купить\b",
    r"\bкуда\s+вложить\b",
    r"\bточка\s+входа\b",
    r"\bцелевая\s+цена\b",
    r"\bлучший\s+инструмент\s+для\s+вас\b",
    r"\bлучший\s+вариант\s+для\s+вас\b",
    r"\bлучший\s+инвестиционный\s+вариант\b",
    r"\bоптимальный\s+портфель\b",
    r"\bвам\s+подходит\b",
    r"\bподходит\s+вам\b",
    r"\bгарантированн(ая|ый|ое|ые)\s+(доходность|прибыль|результат)\b",
]

APPROVED_NEGATIVE_CONTEXTS = [
    "not a recommendation",
    "не является рекомендацией",
    "не является индивидуальной инвестиционной рекомендацией",
    "не выдаёт индивидуальные инвестиционные рекомендации",
    "не выдает индивидуальные инвестиционные рекомендации",
]


@dataclass(frozen=True)
class SafetyViolation:
    source: str
    phrase: str
    text: str


def find_safety_violations(texts: dict[str, str]) -> list[SafetyViolation]:
    violations: list[SafetyViolation] = []
    for source, text in texts.items():
        lowered = text.lower()
        for pattern in BANNED_POSITIVE_PATTERNS:
            for match in re.finditer(pattern, lowered, flags=re.IGNORECASE):
                window = lowered[max(0, match.start() - 80) : match.end() + 80]
                if any(allowed in window for allowed in APPROVED_NEGATIVE_CONTEXTS):
                    continue
                violations.append(SafetyViolation(source=source, phrase=match.group(0), text=text))
    return violations


def validate_safe_text(text: str) -> None:
    assert_safe_texts({"text": text})


def assert_safe_status(status: str) -> None:
    validate_safe_text(status)


def scan_ui_texts(paths: list[Path]) -> list[SafetyViolation]:
    texts: dict[str, str] = {}
    for root in paths:
        if root.is_file() and root.suffix == ".py":
            texts[str(root)] = root.read_text(encoding="utf-8")
            continue
        for path in root.rglob("*.py"):
            if "safety_text_guard.py" in str(path) or "/tests/" in str(path):
                continue
            texts[str(path)] = path.read_text(encoding="utf-8")
    return find_safety_violations(texts)


def assert_safe_texts(texts: dict[str, str]) -> None:
    violations = find_safety_violations(texts)
    if violations:
        details = "; ".join(f"{v.source}: {v.phrase}" for v in violations)
        raise AssertionError(f"Unsafe advisory wording detected: {details}")

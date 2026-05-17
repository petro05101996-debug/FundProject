from pathlib import Path

from investment_lab.engine.safety_text_guard import scan_ui_texts


def test_ui_texts_pass_safety_scan():
    paths = [
        Path("investment_lab/ui/pages"),
        Path("investment_lab/ui/components.py"),
        Path("investment_lab/ui/layout.py"),
        Path("investment_lab/data/legal_texts.py"),
        Path("investment_lab/engine/report_builder.py"),
    ]
    assert scan_ui_texts(paths) == []

"""UI package for the Investment Scenario Lab product module."""
from __future__ import annotations


def render_investment_lab() -> None:
    """Backward-compatible Streamlit renderer."""

    from legacy_streamlit.router import render_investment_lab_app

    render_investment_lab_app()

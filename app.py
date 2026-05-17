"""Streamlit entry point for FundProject."""
from __future__ import annotations

import streamlit as st

from investment_lab.router import render_investment_lab_app

st.set_page_config(page_title="Investment Scenario Lab", layout="wide", initial_sidebar_state="expanded")

render_investment_lab_app()

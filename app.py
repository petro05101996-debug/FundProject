"""Streamlit entry point for FundProject.

Investment Scenario Lab is added as an isolated section. Any main-product code
should remain below the lab routing guard.
"""
from __future__ import annotations

import streamlit as st

from investment_lab.router import render_investment_lab_app

st.set_page_config(page_title="FundProject", layout="wide", initial_sidebar_state="expanded")

section = st.sidebar.radio(
    "Раздел приложения",
    ["Основной продукт", "Финансовый сценарный анализатор"],
    index=0,
)

if section == "Финансовый сценарный анализатор":
    render_investment_lab_app()
    st.stop()

# Ниже должна оставаться существующая область основного продукта. В этом
# репозитории исходная бизнес-логика основного продукта отсутствует, поэтому
# здесь нет изменений расчётов или страниц основного продукта.
pass

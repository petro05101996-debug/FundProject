"""Plotly charts for Investment Scenario Lab."""
from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

DARK_TEMPLATE = "plotly_dark"
LIGHT_TEMPLATE = "plotly_white"
COLORWAY = ["#22d3ee", "#2dd4bf", "#60a5fa", "#a78bfa", "#f59e0b", "#fb7185", "#34d399"]


def _transparent(fig: go.Figure) -> go.Figure:
    fig.update_layout(template=DARK_TEMPLATE, colorway=COLORWAY, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(l=10, r=10, t=28, b=10), font=dict(color="#dbeafe"))
    return fig


def allocation_donut(allocation: pd.DataFrame, scenario: str | None = None) -> go.Figure:
    return portfolio_allocation_donut(allocation, scenario=scenario)


def portfolio_allocation_donut(allocation: pd.DataFrame, scenario: str | None = None, total_value: float | None = None) -> go.Figure:
    data = allocation.copy()
    if scenario and "scenario" in data:
        data = data[data["scenario"] == scenario]
    fig = px.pie(data, names="asset_class", values="weight_pct", hole=0.58, color_discrete_sequence=COLORWAY)
    if total_value is not None:
        fig.update_layout(annotations=[dict(text=f"{total_value:,.0f}".replace(",", " "), x=0.5, y=0.5, showarrow=False, font_size=18)])
    return _transparent(fig)


def scenario_score_bar(summary: pd.DataFrame) -> go.Figure:
    fig = px.bar(summary, x="scenario", y="constraint_fit_score", color="status", color_discrete_sequence=COLORWAY)
    fig.update_yaxes(range=[0, 100], title="Соответствие ограничениям")
    fig.update_xaxes(title="Сценарий")
    return _transparent(fig)


def stress_bar(stress: pd.DataFrame) -> go.Figure:
    fig = px.bar(stress, x="stress_case", y="portfolio_impact_pct", color="scenario", barmode="group", color_discrete_sequence=COLORWAY)
    fig.update_yaxes(title="Стресс-просадка, %")
    fig.update_xaxes(title="Стресс-сценарий")
    return _transparent(fig)


def scenario_projection_chart(summary: pd.DataFrame, horizon_years: int, include_stress: bool = True) -> go.Figure:
    fig = go.Figure()
    for _, row in summary.iterrows():
        base_values = [row["portfolio_value"] * (1 + row["net_return_pct"] / 100.0) ** year for year in range(horizon_years + 1)]
        fig.add_trace(go.Scatter(x=list(range(horizon_years + 1)), y=base_values, mode="lines+markers", name=f"{row['scenario']} · базовый"))
        if include_stress:
            stress_values = [value * (1 + row.get("worst_stress_impact_pct", 0) / 100.0) for value in base_values]
            fig.add_trace(go.Scatter(x=list(range(horizon_years + 1)), y=stress_values, mode="lines", line=dict(dash="dash"), name=f"{row['scenario']} · стресс"))
    fig.update_xaxes(title="Год")
    fig.update_yaxes(title="Расчётная стоимость")
    return _transparent(fig)


def projection_line(summary: pd.DataFrame, horizon_years: int) -> go.Figure:
    return scenario_projection_chart(summary, horizon_years, include_stress=False)


def drawdown_chart(summary: pd.DataFrame) -> go.Figure:
    fig = px.bar(summary, x="scenario", y="worst_stress_impact_pct", color="status", color_discrete_sequence=COLORWAY)
    fig.update_yaxes(title="Худшая стресс-просадка, %")
    fig.update_xaxes(title="Сценарий")
    return _transparent(fig)


def risk_bar_chart(summary: pd.DataFrame) -> go.Figure:
    melted = summary.melt(id_vars=["scenario"], value_vars=["risk_score", "liquidity_score", "complexity_score"], var_name="metric", value_name="score")
    names = {"risk_score": "Риск", "liquidity_score": "Ликвидность", "complexity_score": "Сложность"}
    melted["metric"] = melted["metric"].map(names)
    fig = px.bar(melted, x="scenario", y="score", color="metric", barmode="group", color_discrete_sequence=COLORWAY)
    fig.update_yaxes(range=[0, 5], title="Оценка 1–5")
    return _transparent(fig)


def cashflow_donut(cashflows: pd.DataFrame) -> go.Figure:
    totals = {
        "Взносы": cashflows.get("contributions", pd.Series(dtype=float)).sum() + cashflows.get("additional_contributions", pd.Series(dtype=float)).sum(),
        "Доход": cashflows.get("income", pd.Series(dtype=float)).sum(),
        "Налоги": cashflows.get("taxes", pd.Series(dtype=float)).sum(),
        "Комиссии": cashflows.get("fees", pd.Series(dtype=float)).sum(),
    }
    fig = px.pie(names=list(totals.keys()), values=list(totals.values()), hole=0.55, color_discrete_sequence=COLORWAY)
    return _transparent(fig)

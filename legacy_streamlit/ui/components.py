"""Reusable Streamlit/HTML components for Investment Scenario Lab."""
from __future__ import annotations

import html
from typing import Iterable

import streamlit as st

from legacy_streamlit.ui.formatters import readable_table


def card(title: str, body: str, *, badge: str | None = None, strong: bool = False) -> None:
    badge_html = f"<span class='lab-badge'>{html.escape(badge)}</span>" if badge else ""
    css = "lab-card lab-card-strong" if strong else "lab-card"
    st.markdown(f"<div class='{css}'>{badge_html}<h3>{html.escape(title)}</h3><p>{html.escape(body)}</p></div>", unsafe_allow_html=True)


def kpi_card(label: str, value: str, helper: str = "") -> None:
    st.markdown(f"<div class='lab-card lab-kpi-card'><div class='lab-kpi-label'>{html.escape(label)}</div><div class='lab-kpi-value'>{html.escape(value)}</div><p>{html.escape(helper)}</p></div>", unsafe_allow_html=True)


def disclaimer(text: str) -> None:
    st.markdown(f"<div class='lab-disclaimer'>⚠️ {html.escape(text)}</div>", unsafe_allow_html=True)


def privacy_notice(text: str) -> None:
    st.markdown(f"<div class='lab-panel'>🔒 {html.escape(text)}</div>", unsafe_allow_html=True)


def empty_state(title: str, body: str, action: str | None = None) -> None:
    action_text = f"<p><strong>{html.escape(action)}</strong></p>" if action else ""
    st.markdown(f"<div class='lab-empty'><h3>{html.escape(title)}</h3><p>{html.escape(body)}</p>{action_text}</div>", unsafe_allow_html=True)


def bullet_card(title: str, items: Iterable[str], *, positive: bool = True) -> None:
    css = "ok" if positive else "warn"
    bullets = "".join(f"<li>{html.escape(item)}</li>" for item in items)
    st.markdown(f"<div class='lab-card'><span class='lab-badge {css}'>{'Делает' if positive else 'Не делает'}</span><h3>{html.escape(title)}</h3><ul>{bullets}</ul></div>", unsafe_allow_html=True)


def status_badge(status: str) -> str:
    css = "ok" if "Лучше" in status else "warn" if "Допустимо" in status or "флаг" in status else "danger"
    return f"<span class='lab-badge {css}'>{html.escape(status)}</span>"


def risk_chips(flags) -> None:
    if flags is None or getattr(flags, "empty", True):
        st.markdown("<span class='lab-risk-chip Info'>Риск-флаги отсутствуют</span>", unsafe_allow_html=True)
        return
    chips = []
    for _, row in flags.iterrows():
        severity = str(row.get("severity", "Info"))
        title = str(row.get("title", row.get("flag", "Флаг")))
        metric = str(row.get("metric", ""))
        chips.append(f"<span class='lab-risk-chip {html.escape(severity)}'>{html.escape(title)} · {html.escape(metric)}</span>")
    st.markdown(" ".join(chips), unsafe_allow_html=True)


def table_card(title: str, df, *, height: int | None = None) -> None:
    st.markdown(f"<div class='lab-table-card'><h3>{html.escape(title)}</h3>", unsafe_allow_html=True)
    st.dataframe(readable_table(df), use_container_width=True, hide_index=True, height=height)
    st.markdown("</div>", unsafe_allow_html=True)


def action_bar(left_text: str = "", right_text: str = "") -> None:
    st.markdown(f"<div class='lab-action-bar'><span>{html.escape(left_text)}</span><span>{html.escape(right_text)}</span></div>", unsafe_allow_html=True)

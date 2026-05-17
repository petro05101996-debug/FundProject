from __future__ import annotations

import pandas as pd
import streamlit as st

from investment_lab.data.knowledge_base import INSTRUMENT_GUIDE
from investment_lab.data.legal_texts import EDUCATIONAL_DISCLAIMER
from investment_lab.engine.explanation_builder import build_instrument_explanation
from investment_lab.ui.components import card, disclaimer, kpi_card, table_card


def render() -> None:
    st.markdown("## Объяснить инструмент")
    disclaimer(EDUCATIONAL_DISCLAIMER)
    query = st.text_input("Поиск инструмента, например: ОФЗ, фонд, облигации...")
    categories = ["Вклад", "ОФЗ", "Корпоративная облигация", "Фонды", "Акции как класс", "ИИС", "ПДС"]
    cols = st.columns(len(categories))
    selected = st.session_state.get("explain_selected", "ОФЗ")
    for col, category in zip(cols, categories):
        with col:
            if st.button(category, use_container_width=True):
                selected = "Индексный фонд" if category == "Фонды" else category
                st.session_state["explain_selected"] = selected
    if query:
        matches = [name for name in INSTRUMENT_GUIDE if query.lower() in name.lower()]
        if matches:
            selected = matches[0]
        else:
            st.markdown("<div class='lab-empty'><h3>Инструмент не найден</h3><p>Попробуйте выбрать категорию или изменить запрос</p></div>", unsafe_allow_html=True)
            return

    item = build_instrument_explanation(selected)
    main, side = st.columns([1.35, .75])
    with main:
        card(item["name"], f"{item['summary']} Горизонт: {item['horizon']}", badge=item["category"], strong=True)
        st.markdown("<div class='lab-panel'><h3>Как формируется результат</h3><p>Инвестор → Инструмент → Доход / риск / ликвидность</p></div>", unsafe_allow_html=True)
        st.markdown("### Основные риски")
        for risk in item["risks"]: st.markdown(f"- {risk}")
        st.markdown("### Ликвидность")
        st.write(item["liquidity"])
        st.markdown("### Когда пользователь обычно сравнивает такой инструмент")
        st.write("Когда нужно сопоставить пользовательские допущения по доходности, риску, ликвидности, комиссиям и налогам с другими сценариями.")
        st.markdown("### Что проверить самостоятельно")
        for check in item["checks"]: st.markdown(f"- {check}")
        compare = pd.DataFrame([{"Критерий": "Риск", "Выбранный инструмент": item["risk_score"], "Похожие инструменты": ", ".join(item["related"])}, {"Критерий": "Ликвидность", "Выбранный инструмент": item["liquidity_score"], "Похожие инструменты": "зависит от условий"}, {"Критерий": "Сложность", "Выбранный инструмент": item["complexity_score"], "Похожие инструменты": "сравните карточки"}])
        table_card("Сравнение", compare)
    with side:
        kpi_card("Уровень риска", str(item["risk_score"]), "Оценка 1–5")
        kpi_card("Ликвидность", str(item["liquidity_score"]), "Оценка 1–5")
        kpi_card("Сложность", str(item["complexity_score"]), "Оценка 1–5")
        kpi_card("Горизонт", item["horizon"], "Обычно рассматриваемый")
        st.markdown("### Связанные инструменты")
        for related in item["related"]:
            related_item = build_instrument_explanation(related)
            card(related, related_item["summary"], badge=related_item["category"])

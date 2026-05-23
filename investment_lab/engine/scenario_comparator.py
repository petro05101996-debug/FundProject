"""Scenario analytics engine for Investment Scenario Lab.

All outputs are deterministic transformations of user-entered data and clearly
marked assumptions. The module does not recommend trades or securities.
"""
from __future__ import annotations

from dataclasses import asdict
from typing import Any

import numpy as np
import pandas as pd

from investment_lab.data.legal_texts import LIMITATIONS
from investment_lab.domain.enums import RiskFlagCode, Severity
from investment_lab.domain.models import ScenarioAssumptions, UserConstraints, missing_columns, normalize_asset_class, status_for_score
from investment_lab.domain.asset_classes import is_known_asset_class
from investment_lab.engine.risk_flags import make_flag
from investment_lab.engine.methodology import build_methodology
from investment_lab.engine.validation import ValidationIssue
from investment_lab.engine.result_contract import (
    ASSET_ALLOCATION_FIELDS,
    FLAG_FIELDS,
    POSITION_FIELDS,
    STRESS_FIELDS,
    SUMMARY_FIELDS,
    ensure_columns,
)
from investment_lab.engine.scoring import complexity_score, liquidity_score, risk_score
from investment_lab.engine.stress_engine import STRESS_CASES

CORRELATION_BY_CLASS: dict[tuple[str, str], float] = {
    ("Акции", "Облигации"): 0.25,
    ("Акции", "Денежные средства"): 0.05,
    ("Акции", "Товары"): 0.35,
    ("Акции", "Недвижимость"): 0.55,
    ("Облигации", "Денежные средства"): 0.15,
    ("Облигации", "Товары"): 0.05,
    ("Облигации", "Недвижимость"): 0.25,
    ("Денежные средства", "Товары"): 0.00,
    ("Денежные средства", "Недвижимость"): 0.05,
    ("Товары", "Недвижимость"): 0.30,
}

STRESS_SHOCKS: dict[str, dict[str, float]] = STRESS_CASES


def analyze_scenarios(
    instruments: pd.DataFrame,
    assumptions: ScenarioAssumptions | None = None,
    constraints: UserConstraints | None = None,
) -> dict[str, Any]:
    """Analyze all user-entered scenarios and return report-ready tables.

    Parameters are deliberately explicit because the service is a calculator for
    user assumptions, not a source of market recommendations.
    """

    assumptions = (assumptions or ScenarioAssumptions()).normalized()
    constraints = (constraints or UserConstraints()).normalized()
    prepared, validation_errors = prepare_instruments(instruments, assumptions)

    if prepared.empty:
        return {
            "summary": pd.DataFrame(),
            "positions": prepared,
            "asset_allocation": pd.DataFrame(),
            "stress": pd.DataFrame(),
            "flags": pd.DataFrame(_validation_flags(validation_errors)),
            "leading_constraint_match_scenario": None,
            "best_fit_scenario": None,
            "assumptions": asdict(assumptions),
            "constraints": asdict(constraints),
            "limitations": limitations(),
            "methodology": build_methodology(),
        }

    positions = _add_position_metrics(prepared, assumptions)
    asset_allocation = _asset_allocation(positions)
    stress = _stress_table(asset_allocation, positions, assumptions)
    summary = _summary_table(positions, asset_allocation, stress, assumptions, constraints)
    flags = _flags(positions, asset_allocation, stress, summary, constraints, validation_errors)
    summary = _add_safe_statuses(summary, flags)
    leading_constraint_match_scenario = _leading_constraint_match(summary)

    return {
        "summary": ensure_columns(summary, SUMMARY_FIELDS),
        "positions": ensure_columns(positions, POSITION_FIELDS),
        "asset_allocation": ensure_columns(asset_allocation, ASSET_ALLOCATION_FIELDS),
        "stress": ensure_columns(stress, STRESS_FIELDS),
        "flags": ensure_columns(flags, FLAG_FIELDS),
        "leading_constraint_match_scenario": leading_constraint_match_scenario,
        "best_fit_scenario": leading_constraint_match_scenario,
        "assumptions": asdict(assumptions),
        "constraints": asdict(constraints),
        "limitations": limitations(),
        "methodology": build_methodology(),
    }


def prepare_instruments(
    instruments: pd.DataFrame,
    assumptions: ScenarioAssumptions,
) -> tuple[pd.DataFrame, list[ValidationIssue]]:
    """Validate and normalize user instrument rows."""

    errors: list[ValidationIssue] = []
    if instruments is None or instruments.empty:
        return pd.DataFrame(), [ValidationIssue(RiskFlagCode.INSUFFICIENT_DATA.value, Severity.ERROR.value, "Добавьте хотя бы один инструмент для расчёта.")]

    missing = missing_columns(instruments.columns)
    if missing:
        errors.append(ValidationIssue(RiskFlagCode.INSUFFICIENT_DATA.value, Severity.ERROR.value, f"Отсутствуют обязательные колонки: {', '.join(missing)}."))

    df = instruments.copy()
    for column in missing:
        df[column] = np.nan

    text_defaults = {
        "scenario": "Пользовательский сценарий",
        "instrument": "Инструмент без названия",
        "ticker": "",
        "country": "Пользовательский ввод",
        "currency": "Базовая",
    }
    for column, default in text_defaults.items():
        df[column] = df[column].fillna(default).astype(str).str.strip().replace("", default)

    original_asset_class = df.get("raw_asset_class", df["asset_class"]).astype(str).fillna("")
    df["asset_class"] = original_asset_class.map(normalize_asset_class)
    df["asset_class_was_unknown"] = original_asset_class.map(
        lambda value: bool(str(value).strip()) and not is_known_asset_class(value)
    )
    for idx in df[df["asset_class_was_unknown"]].index:
        errors.append(ValidationIssue(RiskFlagCode.INSUFFICIENT_DATA.value, Severity.INFO.value, "Неизвестный класс актива отнесён к Альтернативным.", int(idx), "asset_class"))

    numeric_defaults = {
        "market_value": 0.0,
        "expected_return_pct": 0.0,
        "volatility_pct": 0.0,
        "liquidity_days": 365.0,
        "annual_fee_pct": 0.0,
        "tax_pct": assumptions.default_tax_pct,
    }
    for column, default in numeric_defaults.items():
        df[column] = pd.to_numeric(df[column], errors="coerce").fillna(default)

    df["market_value"] = df["market_value"].clip(lower=0.0)
    df["volatility_pct"] = df["volatility_pct"].clip(lower=0.0)
    df["liquidity_days"] = df["liquidity_days"].clip(lower=0.0)
    df["annual_fee_pct"] = df["annual_fee_pct"].clip(lower=0.0)
    df["tax_pct"] = df["tax_pct"].clip(lower=0.0, upper=100.0)

    removed = df[df["market_value"] <= 0]
    for idx in removed.index:
        errors.append(ValidationIssue(RiskFlagCode.ZERO_MARKET_VALUES.value, Severity.ERROR.value, "Строка исключена: market_value <= 0.", int(idx), "market_value"))
    df = df[df["market_value"] > 0].reset_index(drop=True)
    if df.empty:
        errors.append(ValidationIssue(RiskFlagCode.ZERO_MARKET_VALUES.value, Severity.ERROR.value, "Все рыночные стоимости равны нулю; введите положительные значения.", None, "market_value"))

    return df, errors


def limitations() -> list[str]:
    """Plain-language model limitations shown in the report."""

    return LIMITATIONS


def _add_position_metrics(df: pd.DataFrame, assumptions: ScenarioAssumptions) -> pd.DataFrame:
    positions = df.copy()
    totals = positions.groupby("scenario")["market_value"].transform("sum")
    positions["weight_pct"] = np.where(totals > 0, positions["market_value"] / totals * 100.0, 0.0)
    positions["tax_drag_pct"] = np.maximum(positions["expected_return_pct"], 0.0) * positions["tax_pct"] / 100.0
    positions["commission_drag_pct"] = assumptions.transaction_commission_pct * assumptions.rebalance_events_per_year
    positions["net_return_pct"] = (
        positions["expected_return_pct"]
        - positions["annual_fee_pct"]
        - positions["tax_drag_pct"]
        - positions["commission_drag_pct"]
    )
    positions["real_return_pct"] = ((1 + positions["net_return_pct"] / 100.0) / (1 + assumptions.inflation_pct / 100.0) - 1) * 100.0
    positions["liquid_within_30d"] = positions["liquidity_days"] <= 30
    liquidity_data = [liquidity_score(row["liquidity_days"], row["asset_class"]) for _, row in positions.iterrows()]
    positions["liquidity_score"] = [item[0] for item in liquidity_data]
    positions["liquidity_label"] = [item[1] for item in liquidity_data]
    positions["stress_liquidity_note"] = [item[2] for item in liquidity_data]
    complexity_data = [
        complexity_score(row["asset_class"], row["instrument"], row["currency"], row["volatility_pct"], row["liquidity_days"], row["annual_fee_pct"])
        for _, row in positions.iterrows()
    ]
    positions["complexity_score"] = [item[0] for item in complexity_data]
    positions["complexity_label"] = [item[1] for item in complexity_data]
    risk_data = [risk_score(row["asset_class"], row["volatility_pct"], 0, row["weight_pct"], row["currency"]) for _, row in positions.iterrows()]
    positions["risk_score"] = [item[0] for item in risk_data]
    positions["risk_label"] = [item[1] for item in risk_data]
    positions["risk_drivers"] = [", ".join(item[2]) for item in risk_data]
    return positions


def _asset_allocation(positions: pd.DataFrame) -> pd.DataFrame:
    grouped = positions.groupby(["scenario", "asset_class"], as_index=False).agg(
        market_value=("market_value", "sum"),
        avg_net_return_pct=("net_return_pct", "mean"),
    )
    totals = grouped.groupby("scenario")["market_value"].transform("sum")
    grouped["weight_pct"] = np.where(totals > 0, grouped["market_value"] / totals * 100.0, 0.0)
    return grouped.sort_values(["scenario", "weight_pct"], ascending=[True, False]).reset_index(drop=True)


def _summary_table(
    positions: pd.DataFrame,
    asset_allocation: pd.DataFrame,
    stress: pd.DataFrame,
    assumptions: ScenarioAssumptions,
    constraints: UserConstraints,
) -> pd.DataFrame:
    rows: list[dict[str, float | str | int]] = []
    for scenario, scenario_positions in positions.groupby("scenario"):
        total = scenario_positions["market_value"].sum()
        weights = scenario_positions["weight_pct"].to_numpy() / 100.0
        expected = float(np.dot(weights, scenario_positions["expected_return_pct"]))
        fees = float(np.dot(weights, scenario_positions["annual_fee_pct"]))
        tax_drag = float(np.dot(weights, scenario_positions["tax_drag_pct"]))
        commission_drag = assumptions.transaction_commission_pct * assumptions.rebalance_events_per_year
        net_return = expected - fees - tax_drag - commission_drag
        real_return = ((1 + net_return / 100.0) / (1 + assumptions.inflation_pct / 100.0) - 1) * 100.0
        volatility = _portfolio_volatility(scenario_positions)
        liquid_30d = float(scenario_positions.loc[scenario_positions["liquid_within_30d"], "market_value"].sum() / total * 100.0)
        max_position = float(scenario_positions["weight_pct"].max())
        max_asset_class = float(asset_allocation.loc[asset_allocation["scenario"] == scenario, "weight_pct"].max())
        worst_stress = float(stress.loc[stress["scenario"] == scenario, "portfolio_impact_pct"].min())
        ending_value = total * (1 + net_return / 100.0) ** assumptions.horizon_years
        projected_profit = ending_value - total
        worst_stress_value = total * worst_stress / 100.0
        risk_explanation = _build_risk_explanation(scenario, max_position, liquid_30d, worst_stress, constraints)
        dq_score, dq_label, dq_notes = _data_quality_for_scenario(scenario_positions)
        score = _constraint_score(
            max_position=max_position,
            max_asset_class=max_asset_class,
            liquid_30d=liquid_30d,
            volatility=volatility,
            fee_drag=fees + commission_drag,
            worst_stress=abs(min(worst_stress, 0.0)),
            constraints=constraints,
        )
        rows.append(
            {
                "scenario": scenario,
                "portfolio_value": total,
                "expected_return_pct": expected,
                "net_return_pct": net_return,
                "real_return_pct": real_return,
                "projected_value": ending_value,
                "projected_profit": projected_profit,
                "projected_profit_pct": (ending_value / total - 1) * 100 if total > 0 else 0.0,
                "volatility_pct": volatility,
                "liquid_within_30d_pct": liquid_30d,
                "fee_and_commission_drag_pct": fees + commission_drag,
                "tax_drag_pct": tax_drag,
                "max_position_pct": max_position,
                "max_asset_class_pct": max_asset_class,
                "worst_stress_impact_pct": worst_stress,
                "worst_stress_value": worst_stress_value,
                "constraint_fit_score": score,
                "instrument_count": int(len(scenario_positions)),
                "risk_score": float(np.dot(weights, scenario_positions["risk_score"])),
                "risk_label": _score_label(float(np.dot(weights, scenario_positions["risk_score"])), "Низкий", "Средний", "Высокий"),
                "liquidity_score": float(np.dot(weights, scenario_positions["liquidity_score"])),
                "liquidity_label": _score_label(float(np.dot(weights, scenario_positions["liquidity_score"])), "Низкая", "Средняя", "Высокая"),
                "complexity_score": float(np.dot(weights, scenario_positions["complexity_score"])),
                "complexity_label": _score_label(float(np.dot(weights, scenario_positions["complexity_score"])), "Низкая", "Средняя", "Высокая"),
                "risk_explanation": risk_explanation,
                "data_quality_score": dq_score,
                "data_quality_label": dq_label,
                "data_quality_notes": dq_notes,
            }
        )
    return pd.DataFrame(rows).sort_values("constraint_fit_score", ascending=False).reset_index(drop=True)


def _stress_table(asset_allocation: pd.DataFrame, positions: pd.DataFrame, assumptions: ScenarioAssumptions) -> pd.DataFrame:
    rows: list[dict[str, float | str]] = []
    for scenario, allocation in asset_allocation.groupby("scenario"):
        for stress_name, shocks in STRESS_SHOCKS.items():
            impact = 0.0
            for _, row in allocation.iterrows():
                impact += (row["weight_pct"] / 100.0) * shocks.get(row["asset_class"], shocks["Альтернативные"]) * 100.0
            if assumptions.fx_devaluation_pct != 0:
                scenario_positions = positions.loc[positions["scenario"] == scenario]
                total = float(scenario_positions["market_value"].sum())
                non_base_value = float(
                    scenario_positions.loc[
                        ~scenario_positions["currency"].fillna("RUB").astype(str).str.upper().isin(["RUB", "₽", "БАЗОВАЯ", "BASE"]),
                        "market_value",
                    ].sum()
                )
                non_base_weight = non_base_value / total if total > 0 else 0.0
                impact += non_base_weight * assumptions.fx_devaluation_pct
            scenario_total = float(positions.loc[positions["scenario"] == scenario, "market_value"].sum())
            rows.append(
                {
                    "scenario": scenario,
                    "stress_case": stress_name,
                    "portfolio_impact_pct": impact,
                    "estimated_value_after_stress_pct": 100.0 + impact,
                    "estimated_value_after_stress": scenario_total * (1 + impact / 100.0),
                    "stress_loss_value": min(scenario_total * impact / 100.0, 0.0),
                    "max_drawdown_pct": min(impact, 0.0),
                    "liquidity_degradation_level": 1 if impact < -10 else 0,
                }
            )
    return pd.DataFrame(rows)


def _validation_flags(validation_errors: list[ValidationIssue]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for error in validation_errors:
        rows.append(make_flag("—", error.code, error.severity, "Проблема входных данных", error.message))
    return rows


def _flags(
    positions: pd.DataFrame,
    asset_allocation: pd.DataFrame,
    stress: pd.DataFrame,
    summary: pd.DataFrame,
    constraints: UserConstraints,
    validation_errors: list[ValidationIssue],
) -> pd.DataFrame:
    rows: list[dict[str, str]] = _validation_flags(validation_errors)
    for _, row in summary.iterrows():
        scenario = row["scenario"]
        if row["max_position_pct"] > constraints.max_single_position_pct:
            rows.append(make_flag(scenario, RiskFlagCode.SINGLE_POSITION_CONCENTRATION, Severity.HIGH, "Высокая концентрация", "Доля одной позиции выше пользовательского лимита.", f"{row['max_position_pct']:.1f}%", f"{constraints.max_single_position_pct:.1f}%"))
        if row["max_asset_class_pct"] > constraints.max_asset_class_pct:
            rows.append(make_flag(scenario, RiskFlagCode.ASSET_CLASS_CONCENTRATION, Severity.HIGH, "Концентрация класса активов", "Доля класса активов выше пользовательского лимита.", f"{row['max_asset_class_pct']:.1f}%", f"{constraints.max_asset_class_pct:.1f}%"))
        if row["liquid_within_30d_pct"] < constraints.min_liquidity_pct_30d:
            rows.append(make_flag(scenario, RiskFlagCode.LOW_LIQUIDITY, Severity.MEDIUM, "Низкая ликвидность", "Ликвидность в течение 30 дней ниже пользовательского минимума.", f"{row['liquid_within_30d_pct']:.1f}%", f"{constraints.min_liquidity_pct_30d:.1f}%"))
        if row["volatility_pct"] > constraints.max_portfolio_volatility_pct:
            rows.append(make_flag(scenario, RiskFlagCode.HIGH_VOLATILITY, Severity.MEDIUM, "Повышенная волатильность", "Расчётная волатильность выше пользовательского лимита.", f"{row['volatility_pct']:.1f}%", f"{constraints.max_portfolio_volatility_pct:.1f}%"))
        if row["fee_and_commission_drag_pct"] > constraints.max_fee_drag_pct:
            rows.append(make_flag(scenario, RiskFlagCode.FEE_DRAG_EXCEEDS_LIMIT, Severity.MEDIUM, "Комиссионная нагрузка", "Годовая нагрузка комиссий выше пользовательского лимита.", f"{row['fee_and_commission_drag_pct']:.2f}%", f"{constraints.max_fee_drag_pct:.2f}%"))
        if abs(min(row["worst_stress_impact_pct"], 0.0)) > constraints.max_stress_loss_pct:
            rows.append(make_flag(scenario, RiskFlagCode.STRESS_LOSS_EXCEEDS_LIMIT, Severity.HIGH, "Стресс-просадка выше лимита", "Худшая стресс-просадка выше пользовательского лимита.", f"{abs(min(row['worst_stress_impact_pct'], 0.0)):.1f}%", f"{constraints.max_stress_loss_pct:.1f}%"))
        if row.get("tax_drag_pct", 0) > 3:
            rows.append(make_flag(scenario, RiskFlagCode.TAX_ASSUMPTION_SENSITIVE, Severity.INFO, "Чувствительность к налогам", "Результат заметно зависит от пользовательской налоговой ставки.", f"{row['tax_drag_pct']:.2f}%", "пользовательская ставка"))
        if row.get("complexity_score", 0) >= 4:
            rows.append(make_flag(scenario, RiskFlagCode.INSTRUMENT_COMPLEXITY, Severity.INFO, "Повышенная сложность", "В сценарии есть инструменты или условия с повышенной сложностью.", f"{row['complexity_score']:.1f}/5", "до 3/5"))

    illiquid = positions.loc[positions["liquidity_days"] > 90, ["scenario", "instrument", "liquidity_days"]]
    for _, row in illiquid.iterrows():
        rows.append(make_flag(row["scenario"], RiskFlagCode.LOW_LIQUIDITY, Severity.INFO, "Длинный срок ликвидности", f"{row['instrument']} имеет срок ликвидности выше 90 дней по пользовательскому вводу.", f"{row['liquidity_days']:.0f} дней", "до 90 дней"))

    currencies = positions.loc[~positions["currency"].str.upper().isin(["RUB", "₽", "БАЗОВАЯ"]), ["scenario", "currency"]]
    for scenario in currencies["scenario"].unique():
        rows.append(make_flag(scenario, RiskFlagCode.CURRENCY_RISK, Severity.INFO, "Валютный риск", "В сценарии есть инструменты не в базовой валюте.", "есть", "нет"))

    if not rows:
        rows.append(make_flag("Все сценарии", RiskFlagCode.NO_CONSTRAINT_BREACHES, Severity.INFO, "Нарушений не найдено", "Для введённых сценариев не найдено нарушений ограничений."))
    return pd.DataFrame(rows)


def _add_safe_statuses(summary: pd.DataFrame, flags: pd.DataFrame) -> pd.DataFrame:
    enriched = summary.copy()
    if enriched.empty:
        enriched["status"] = []
        return enriched
    flag_counts = flags.loc[flags["severity"].isin(["High", "Medium"]), "scenario"].value_counts() if not flags.empty else {}
    enriched["status"] = [
        status_for_score(float(row["constraint_fit_score"]), int(flag_counts.get(row["scenario"], 0)))
        for _, row in enriched.iterrows()
    ]
    return enriched


def _leading_constraint_match(summary: pd.DataFrame) -> str | None:
    if summary.empty:
        return None
    return str(summary.iloc[0]["scenario"])


def _portfolio_volatility(scenario_positions: pd.DataFrame) -> float:
    weights = scenario_positions["weight_pct"].to_numpy(dtype=float) / 100.0
    vols = scenario_positions["volatility_pct"].to_numpy(dtype=float) / 100.0
    classes = scenario_positions["asset_class"].tolist()
    corr = np.eye(len(classes))
    for i, left in enumerate(classes):
        for j, right in enumerate(classes):
            if i == j:
                continue
            corr[i, j] = _correlation(left, right)
    covariance = np.outer(vols, vols) * corr
    variance = float(weights.T @ covariance @ weights)
    return float(np.sqrt(max(variance, 0.0)) * 100.0)


def _correlation(left: str, right: str) -> float:
    if left == right:
        return 0.85
    return CORRELATION_BY_CLASS.get((left, right), CORRELATION_BY_CLASS.get((right, left), 0.30))


def _constraint_score(
    *,
    max_position: float,
    max_asset_class: float,
    liquid_30d: float,
    volatility: float,
    fee_drag: float,
    worst_stress: float,
    constraints: UserConstraints,
) -> float:
    penalties = [
        _overage(max_position, constraints.max_single_position_pct),
        _overage(max_asset_class, constraints.max_asset_class_pct),
        _overage(constraints.min_liquidity_pct_30d, liquid_30d),
        _overage(volatility, constraints.max_portfolio_volatility_pct),
        _overage(fee_drag, constraints.max_fee_drag_pct),
        _overage(worst_stress, constraints.max_stress_loss_pct),
    ]
    score = 100.0 - sum(penalties) * 12.5
    return round(max(0.0, min(100.0, score)), 2)


def _overage(value: float, limit: float) -> float:
    if limit <= 0:
        return 1.0 if value > 0 else 0.0
    return max(0.0, (value - limit) / limit)


def _score_label(score: float, low: str, medium: str, high: str) -> str:
    if score <= 2:
        return low
    if score <= 3.5:
        return medium
    return high


def _build_risk_explanation(scenario: str, max_position: float, liquid_30d: float, worst_stress: float, constraints: UserConstraints) -> str:
    reasons: list[str] = []
    if max_position > constraints.max_single_position_pct:
        reasons.append("высокая концентрация")
    if liquid_30d < constraints.min_liquidity_pct_30d:
        reasons.append("низкая ликвидность")
    if abs(min(worst_stress, 0.0)) > constraints.max_stress_loss_pct:
        reasons.append("стресс-просадка выше лимита")
    if not reasons:
        return "Основные причины риска: критичные отклонения по ограничениям не выявлены."
    return f"Основные причины риска: {', '.join(reasons)}."


def _data_quality_for_scenario(scenario_positions: pd.DataFrame) -> tuple[float, str, str]:
    score = 100.0
    notes: list[str] = []
    if scenario_positions.get("asset_class_was_unknown", pd.Series(dtype=bool)).any():
        score -= 20
        notes.append("часть классов активов не распознана")
    if scenario_positions["currency"].astype(str).str.strip().isin(["", "Базовая"]).any():
        score -= 10
        notes.append("по части позиций валюта заполнена по умолчанию")
    risky = scenario_positions["asset_class"].isin(["Акции", "Альтернативные"])
    if (risky & (scenario_positions["volatility_pct"] <= 0)).any():
        score -= 15
        notes.append("для рискованных активов указана нулевая волатильность")
    if (scenario_positions["liquidity_days"] >= 365).any():
        score -= 15
        notes.append("по части позиций ликвидность заполнена модельным допущением")
    score = max(0.0, score)
    label = "Высокая" if score >= 80 else ("Средняя" if score >= 50 else "Низкая")
    return score, label, ("; ".join(notes) if notes else "Качество расчёта высокое: существенные модельные допущения не применялись.")

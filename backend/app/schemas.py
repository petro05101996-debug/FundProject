from __future__ import annotations
from typing import Any
from pydantic import BaseModel, Field, field_validator

class UserConstraintsSchema(BaseModel):
    max_single_position_pct: float = Field(25.0, ge=0, le=100)
    max_asset_class_pct: float = Field(70.0, ge=0, le=100)
    min_liquidity_pct_30d: float = Field(80.0, ge=0, le=100)
    max_portfolio_volatility_pct: float = Field(20.0, ge=0, le=200)
    max_fee_drag_pct: float = Field(1.5, ge=0, le=100)
    max_stress_loss_pct: float = Field(25.0, ge=0, le=100)

class ScenarioAssumptionsSchema(BaseModel):
    horizon_years: int = Field(5, ge=1, le=50)
    inflation_pct: float = Field(4.0, ge=-100, le=300)
    default_tax_pct: float = Field(13.0, ge=0, le=100)
    transaction_commission_pct: float = Field(0.1, ge=0, le=100)
    rebalance_events_per_year: int = Field(1, ge=0, le=52)
    fx_devaluation_pct: float = Field(0.0, ge=-100, le=500)

class InstrumentPositionSchema(BaseModel):
    scenario: str
    instrument: str
    ticker: str = ""
    asset_class: str
    country: str = "Пользовательский ввод"
    currency: str = "RUB"
    market_value: float = Field(..., gt=0)
    expected_return_pct: float = Field(..., ge=-100, le=100)
    volatility_pct: float = Field(..., ge=0, le=150)
    liquidity_days: float = Field(..., ge=0)
    annual_fee_pct: float = Field(..., ge=0)
    tax_pct: float = Field(..., ge=0, le=100)

    @field_validator('scenario','instrument','asset_class')
    @classmethod
    def non_empty(cls,v:str):
        if not str(v).strip(): raise ValueError('field must not be empty')
        return v

class ScenarioAnalyzeRequest(BaseModel):
    assumptions: ScenarioAssumptionsSchema = Field(default_factory=ScenarioAssumptionsSchema)
    constraints: UserConstraintsSchema = Field(default_factory=UserConstraintsSchema)
    positions: list[InstrumentPositionSchema]

    @field_validator('positions')
    @classmethod
    def has_positions(cls,v):
        if not v: raise ValueError('positions must not be empty')
        return v

class ScenarioAnalyzeResponse(BaseModel):
    summary: list[dict[str, Any]]
    positions: list[dict[str, Any]]
    asset_allocation: list[dict[str, Any]]
    stress: list[dict[str, Any]]
    flags: list[dict[str, Any]]
    assumptions: dict[str, Any]
    constraints: dict[str, Any]
    limitations: list[str]
    leading_constraint_match_scenario: str | None = None
    best_fit_scenario: str | None = None

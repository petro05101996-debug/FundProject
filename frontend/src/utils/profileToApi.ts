export type ScenarioProfile = {
  amount: number; horizon_years: number; goal: string; early_exit_required: boolean; max_drawdown_pct: number;
  experience: 'beginner'|'basic'|'advanced'; include_fees: boolean; include_taxes: boolean; tax_pct: number; inflation_pct: number;
  min_liquidity_pct_30d: number; max_single_position_pct: number; max_asset_class_pct: number; max_portfolio_volatility_pct: number; max_fee_drag_pct: number;
};

export const defaultProfile: ScenarioProfile = {
  amount: 1_000_000, horizon_years: 3, goal: 'Сохранить капитал', early_exit_required: true, max_drawdown_pct: 20,
  experience: 'basic', include_fees: true, include_taxes: true, tax_pct: 13, inflation_pct: 6,
  min_liquidity_pct_30d: 70, max_single_position_pct: 35, max_asset_class_pct: 80, max_portfolio_volatility_pct: 25, max_fee_drag_pct: 2,
};

export function profileToAssumptions(profile: ScenarioProfile) { return { horizon_years: profile.horizon_years, inflation_pct: profile.inflation_pct, default_tax_pct: profile.include_taxes ? profile.tax_pct : 0, transaction_commission_pct: profile.include_fees ? 0.1 : 0, rebalance_events_per_year: 1, fx_devaluation_pct: 0}; }
export function profileToConstraints(profile: ScenarioProfile) { return { max_single_position_pct: profile.max_single_position_pct, max_asset_class_pct: profile.max_asset_class_pct, min_liquidity_pct_30d: profile.min_liquidity_pct_30d, max_portfolio_volatility_pct: profile.max_portfolio_volatility_pct, max_fee_drag_pct: profile.max_fee_drag_pct, max_stress_loss_pct: profile.max_drawdown_pct }; }

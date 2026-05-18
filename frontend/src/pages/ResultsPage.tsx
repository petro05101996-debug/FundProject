import React, { useMemo, useState } from 'react';
import MetricCard from '../components/MetricCard';
import RiskFlag from '../components/RiskFlag';
import ScenarioTable from '../components/ScenarioTable';
import AllocationDonut from '../components/AllocationDonut';
import StressChart from '../components/StressChart';
import CashflowChart from '../components/CashflowChart';
import { api, ApiError } from '../api/client';
import { ScenarioProfile } from '../utils/profileToApi';

export default function ResultsPage({ profile, result, onReport, onNavigate }: { profile: ScenarioProfile; result: any; onReport: () => void; onNavigate: (k: any) => void }) {
  const summary = result?.summary || [];
  const top = summary[0] || {};
  const flags = result?.flags || [];
  const [delta, setDelta] = useState({ rate_delta_pct: 0, inflation_pct: profile.inflation_pct, equity_market_shock_pct: 0, early_exit: false, deposit_share_pct: 25, ofz_share_pct: 25, fund_share_pct: 25, equity_share_pct: 25 });
  const [whatIf, setWhatIf] = useState<any>(null); const [loading, setLoading] = useState(false); const [error, setError] = useState('');
  const groupedFlags = useMemo(() => {
    const source = (whatIf?.risk_flags || flags);
    return {
      high: source.filter((f: any) => String(f?.severity || '').toLowerCase().includes('high')),
      medium: source.filter((f: any) => String(f?.severity || '').toLowerCase().includes('med')),
      low: source.filter((f: any) => !String(f?.severity || '').toLowerCase().includes('high') && !String(f?.severity || '').toLowerCase().includes('med')),
    };
  }, [whatIf, flags]);

  if (!result) return <div className='card empty'><h2>Итог</h2><p>Сначала выполните сравнение сценариев.</p><div className='row'><button className='btn' onClick={() => onNavigate('builder')}>Сравнить варианты</button><button className='btn ghost' onClick={() => onNavigate('portfolio')}>Проверить портфель</button><button className='btn ghost' onClick={() => onNavigate('instrument')}>Проверить инструмент</button></div></div>;

  const recalc = async () => {
    setLoading(true); setError('');
    try {
      const payload = { base_request: { assumptions: result.assumptions, constraints: result.constraints, positions: result.positions }, what_if: delta };
      setWhatIf(await api('/api/scenario/what-if', { method: 'POST', body: JSON.stringify(payload) }));
    } catch (e: any) { setError(e instanceof ApiError ? e.message : 'Ошибка what-if'); }
    finally { setLoading(false); }
  };

  const wi = whatIf?.what_if_summary || {};

  return <div className='card'>
    <h2>Итог</h2><p>Среди введённых пользователем сценариев лучше заданным ограничениям соответствует: <b>{result?.leading_constraint_match_scenario || '—'}</b></p><p>Это не является индивидуальной инвестиционной рекомендацией.</p>
    <div className='kpi-grid'>
      <MetricCard label='Базовая стоимость' value={Number(top.projected_value || 0).toFixed(0)} />
      <MetricCard label='Стресс-стоимость' value={Number(top.stress_value || 0).toFixed(0)} />
      <MetricCard label='Стресс-просадка' value={`${Number(top.worst_stress_impact_pct || 0).toFixed(1)}%`} />
      <MetricCard label='Ликвидность 30д' value={`${Number(top.liquidity_30d_pct || 0).toFixed(1)}%`} />
      <MetricCard label='Риск' value={top.risk_label || '—'} />
      <MetricCard label='Сложность' value={top.complexity_label || '—'} />
      <MetricCard label='Риск-флаги' value={String((flags || []).length)} />
    </div>

    <ScenarioTable rows={summary} />
    <div className='grid2'><AllocationDonut items={result?.asset_allocation || []} /><StressChart rows={(whatIf?.stress) || result?.stress || []} /></div>
    <CashflowChart rows={result?.cashflows || []} />

    <div className={`card soft ${loading ? 'loading' : ''}`}>
      <h4>What-if: было / стало</h4>
      <div className='grid3'>
        <label>Ставка, Δ п.п.<input type='number' value={delta.rate_delta_pct} onChange={e => setDelta({ ...delta, rate_delta_pct: Number(e.target.value) })} /></label>
        <label>Инфляция, %<input type='number' value={delta.inflation_pct} onChange={e => setDelta({ ...delta, inflation_pct: Number(e.target.value) })} /></label>
        <label>Шок акций, %<input type='number' value={delta.equity_market_shock_pct} onChange={e => setDelta({ ...delta, equity_market_shock_pct: Number(e.target.value) })} /></label>
        <label>Доля вклада, %<input type='number' value={delta.deposit_share_pct} onChange={e => setDelta({ ...delta, deposit_share_pct: Number(e.target.value) })} /></label>
        <label>Доля ОФЗ, %<input type='number' value={delta.ofz_share_pct} onChange={e => setDelta({ ...delta, ofz_share_pct: Number(e.target.value) })} /></label>
        <label>Доля фондов, %<input type='number' value={delta.fund_share_pct} onChange={e => setDelta({ ...delta, fund_share_pct: Number(e.target.value) })} /></label>
        <label>Доля акций, %<input type='number' value={delta.equity_share_pct} onChange={e => setDelta({ ...delta, equity_share_pct: Number(e.target.value) })} /></label>
        <label>Досрочный выход<input type='checkbox' checked={delta.early_exit} onChange={e => setDelta({ ...delta, early_exit: e.target.checked })} /></label>
      </div>
      <button className='btn ghost' disabled={loading} onClick={recalc}>{loading ? 'Пересчёт...' : 'Пересчитать what-if'}</button>
      {error && <div className='error-banner'>{error}</div>}
      {whatIf && <div className='grid3'>
        <MetricCard label='Было: базовая' value={Number(top.projected_value || 0).toFixed(0)} />
        <MetricCard label='Стало: базовая' value={Number(wi.projected_value || 0).toFixed(0)} />
        <MetricCard label='Δ базовой' value={Number(whatIf?.deltas?.projected_value_delta || 0).toFixed(0)} />
      </div>}
    </div>

    <div className='grid3'>
      <div className='card soft'><h4>Высокий приоритет</h4>{groupedFlags.high.map((f: any, i: number) => <RiskFlag key={i} text={f.title || f.description || 'Есть риск-флаг'} />)}</div>
      <div className='card soft'><h4>Средний приоритет</h4>{groupedFlags.medium.map((f: any, i: number) => <RiskFlag key={i} text={f.title || f.description || 'Есть риск-флаг'} />)}</div>
      <div className='card soft'><h4>Базовый приоритет</h4>{groupedFlags.low.slice(0, 5).map((f: any, i: number) => <RiskFlag key={i} text={f.title || f.description || 'Есть риск-флаг'} />)}</div>
    </div>

    <details className='card soft'><summary>Расчётные допущения</summary><ul>{Object.entries(result?.assumptions||{}).map(([k,v])=><li key={k}><b>{k}:</b> {String(v)}</li>)}</ul></details>
    <details className='card soft'><summary>Ограничения анализа</summary><ul>{Object.entries(result?.constraints||{}).map(([k,v])=><li key={k}><b>{k}:</b> {String(v)}</li>)}</ul></details>
    <details className='card soft'><summary>Методика и checklist</summary><ul><li>Проверить концентрацию в top-позициях.</li><li>Проверить стресс-потери и ликвидность.</li><li>Проверить влияние комиссий и налогов.</li><li>Сверить ограничения с целями пользователя.</li></ul></details>

    <button className='btn' onClick={onReport}>Сформировать отчёт</button>
  </div>;
}

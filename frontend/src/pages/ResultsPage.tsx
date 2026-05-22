import React, { useState } from 'react';
import { api, ApiError } from '../api/client';
import StressChart from '../components/StressChart';
import CashflowChart from '../components/CashflowChart';
import ScenarioTable from '../components/ScenarioTable';
import { PageShell, EmptyState, StatusBanner, KpiCard, RiskChip } from '../components/ui';
import { ScenarioProfile } from '../utils/profileToApi';

export default function ResultsPage({ profile, result, onReport, onNavigate }: { profile: ScenarioProfile; result: any; onReport: () => void; onNavigate: (k: any) => void }) {
  const [whatIf, setWhatIf] = useState<any>(null);
  const [error, setError] = useState('');
  const [delta, setDelta] = useState({ rate_delta_pct: 0, inflation_pct: profile.inflation_pct, equity_market_shock_pct: 0 });
  if (!result) return <EmptyState title='Пока нет результата анализа' description='Сначала рассчитайте сценарий или портфель.' actions={<><button className='btn' onClick={() => onNavigate('builder')}>Перейти к сравнению вариантов</button><button className='btn ghost' onClick={() => onNavigate('portfolio')}>Проверить портфель</button></>} />;

  const top = (result.summary || [])[0] || {};
  const recalc = async () => {
    setError('');
    try { setWhatIf(await api('/api/scenario/what-if', { method: 'POST', body: JSON.stringify({ base_request: { assumptions: result.assumptions, constraints: result.constraints, positions: result.positions }, what_if: delta }) })); }
    catch (e: any) { setError(e instanceof ApiError ? e.message : 'Ошибка what-if'); }
  };

  return (
    <PageShell title='Итоги анализа' subtitle='Сравнение пользовательских сценариев, стресс-тесты, риск-флаги и ограничения.' actions={<button className='btn' onClick={onReport}>Сформировать отчёт</button>}>
      <StatusBanner title='Сводка' description='По введённым параметрам один из сценариев лучше соответствует заданным ограничениям.' />
      <div className='kpi-strip'>{[['Базовый результат', top.projected_value], ['Стресс-результат', top.stress_value], ['Стресс-просадка', `${Number(top.worst_stress_impact_pct || 0).toFixed(1)}%`], ['Ликвидность', `${Number(top.liquidity_30d_pct || 0).toFixed(1)}%`], ['Риск', top.risk_label], ['Сложность', top.complexity_label]].map(([l, v]) => <KpiCard key={String(l)} label={String(l)} value={String(v ?? '—')} />)}</div>
      <div className='results-grid'>
        <div>
          <ScenarioTable rows={result.summary || []} />
          <StressChart rows={whatIf?.stress || result.stress || []} />
          <CashflowChart rows={result.cashflows || []} />
        </div>
        <aside className='side-panel'>
          <div className='card soft'>
            <h3>Риск-флаги</h3>
            <div className='row'>{(result.flags || []).map((f: any, i: number) => <RiskChip key={i}>{f.title || f.description || 'flag'}</RiskChip>)}</div>
          </div>
          <div className='card soft'>
            <h4>Что проверить самостоятельно</h4>
            <ul><li>Проверить стресс-потери и ликвидность.</li><li>Сверить ограничения с целями пользователя.</li><li>Оценить комиссионную и налоговую нагрузку.</li></ul>
          </div>
          <div className='card soft'>
            <h4>Соответствие ограничениям</h4>
            <ul>{(result.summary || []).slice(0, 4).map((r: any, i: number) => <li key={i}><b>{r.scenario}</b>: {r.constraint_match_label || 'Без оценки'}</li>)}</ul>
          </div>
          <div className='card soft'>
            <h4>Ограничения анализа</h4>
            <p className='muted'>{(result.limitations || []).join(' ')}</p>
          </div>
        </aside>
      </div>
      <div className='whatif-panel card'>
        <h3>What-if: было / стало</h3>
        <div className='form-grid'>
          <label>Ставка, Δ п.п.<input type='number' value={delta.rate_delta_pct} onChange={(e) => setDelta({ ...delta, rate_delta_pct: Number(e.target.value) })} /></label>
          <label>Инфляция, %<input type='number' value={delta.inflation_pct} onChange={(e) => setDelta({ ...delta, inflation_pct: Number(e.target.value) })} /></label>
          <label>Шок акций, %<input type='number' value={delta.equity_market_shock_pct} onChange={(e) => setDelta({ ...delta, equity_market_shock_pct: Number(e.target.value) })} /></label>
        </div>
        <button className='btn ghost' onClick={recalc}>Пересчитать what-if</button>
        {whatIf && <p className='muted'>Эффект: Δ базовой стоимости {Number(whatIf?.deltas?.projected_value_delta || 0).toFixed(0)}</p>}
        {error && <div className='error-banner'>{error}</div>}
      </div>
      <div className='accordion-stack'>
        <details className='card soft' open><summary>Допущения</summary><pre>{JSON.stringify(result.assumptions || {}, null, 2)}</pre></details>
        <details className='card soft'><summary>Методика</summary><p>Сравнение сценариев по ограничениям, стрессам и рискам.</p></details>
        <details className='card soft'><summary>Ограничения</summary><pre>{JSON.stringify(result.constraints || {}, null, 2)}</pre></details>
        <details className='card soft'><summary>Проверки безопасности</summary><p>Сервис не является индивидуальной инвестиционной рекомендацией.</p></details>
      </div>
    </PageShell>
  );
}

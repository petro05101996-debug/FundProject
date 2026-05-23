import React, { useState } from 'react';
import { AlertTriangle, BarChart3, CheckCircle2, Download, ShieldAlert, TrendingDown, TrendingUp } from 'lucide-react';
import { api, ApiError } from '../api/client';
import { EmptyState, PageShell } from '../components/ui';
import { ScenarioProfile } from '../utils/profileToApi';

export default function ResultsPage({ profile, result, onReport, onNavigate }: { profile: ScenarioProfile; result: any; onReport: () => void; onNavigate: (k: any) => void }) {
  const [whatIf, setWhatIf] = useState<any>(null);
  const [error, setError] = useState('');
  const [delta, setDelta] = useState({ rate_delta_pct: 0, inflation_pct: profile.inflation_pct, equity_market_shock_pct: 0 });

  if (!result) return <EmptyState title='Пока нет результата анализа' description='Сначала рассчитайте сценарий или портфель.' actions={<><button className='btn' onClick={() => onNavigate('builder')}>Перейти к сравнению вариантов</button><button className='btn ghost' onClick={() => onNavigate('portfolio')}>Проверить портфель</button></>} />;

  const top = (result.summary || [])[0] || {};
  const isGoodFit = top.status === 'Лучше соответствует заданным ограничениям' || Number(top.constraint_fit_score ?? 0) >= 75;
  const stressValue = top.worst_stress_value ?? (top.portfolio_value != null && top.worst_stress_impact_pct != null ? Number(top.portfolio_value) * Number(top.worst_stress_impact_pct) / 100 : null);
  const formatMoney = (v: any) => (v == null ? 'нет данных' : `${Number(v).toLocaleString('ru-RU', { maximumFractionDigits: 0 })} ₽`);
  const formatPct = (v: any) => (v == null ? 'нет данных' : `${Number(v).toFixed(1)}%`);

  const recalc = async () => {
    setError('');
    try {
      setWhatIf(await api('/api/scenario/what-if', { method: 'POST', body: JSON.stringify({ base_request: { assumptions: result.assumptions, constraints: result.constraints, positions: result.positions }, what_if: delta }) }));
    } catch (e: any) {
      setError(e instanceof ApiError ? e.message : 'Ошибка what-if');
    }
  };

  return (
    <PageShell title='Итог по выбранным пользовательским сценариям' subtitle='Сравните ожидаемые результаты, риски и стресс-сценарии' actions={<button className='btn' onClick={onReport}><Download size={14} />Сформировать аналитический отчёт</button>}>
      <div className='card soft' style={{ marginBottom: 10 }}><p><CheckCircle2 size={14} /> {isGoodFit ? `Сценарий «${top.scenario || 'A'}» лучше соответствует заданным пользовательским ограничениям.` : `Сценарий «${top.scenario || 'A'}» имеет риск-флаги и требует ручной проверки.`}</p></div>

      <div className='kpi-strip'>
        <div className='kpi-card'><small>Итоговая стоимость</small><strong>{formatMoney(top.projected_value)}</strong><em><TrendingUp size={12} /> чистая доходность: {formatPct(top.net_return_pct)}</em></div>
        <div className='kpi-card'><small>Стресс-просадка</small><strong>{formatPct(top.worst_stress_impact_pct)}</strong><em><TrendingDown size={12} /> денежная просадка: {formatMoney(stressValue)}</em></div>
        <div className='kpi-card'><small>Ликвидность до 30 дней</small><strong>{formatPct(top.liquid_within_30d_pct)}</strong><em>оценка</em></div>
        <div className='kpi-card'><small>Риск</small><strong>{top.risk_label ?? 'нет данных'}</strong><em>оценка</em></div>
        <div className='kpi-card'><small>Балл соответствия</small><strong>{top.constraint_fit_score ?? 'нет данных'}</strong><em>{top.status ?? 'нет данных'}</em></div>
      </div>

      <section className='scenario-main-grid results-final-grid'>
        <article className='card'>
          <h3>Сравнение выбранных сценариев</h3>
          <table className='table results-table'>
            <thead><tr><th>#</th><th>Сценарий</th><th>Базовый</th><th>Стресс</th><th>Риск</th><th>Статус</th></tr></thead>
            <tbody>
              {(result.summary || []).slice(0, 5).map((r: any, i: number) => (
                <tr key={i}><td>{i + 1}</td><td>{r.scenario}</td><td>{formatMoney(r.projected_value)}</td><td>{formatPct(r.worst_stress_impact_pct)}</td><td>{r.risk_label ?? '—'}</td><td>{r.status ?? '—'}</td></tr>
              ))}
            </tbody>
          </table>

          <div className='card soft' style={{ marginTop: 10 }}>
            <h4><BarChart3 size={14} /> What-if сценарий</h4>
            <div className='form-grid'>
              <label>Ставка, Δ п.п.<input type='number' value={delta.rate_delta_pct} onChange={(e) => setDelta({ ...delta, rate_delta_pct: Number(e.target.value) })} /></label>
              <label>Инфляция, %<input type='number' value={delta.inflation_pct} onChange={(e) => setDelta({ ...delta, inflation_pct: Number(e.target.value) })} /></label>
              <label>Шок акций, %<input type='number' value={delta.equity_market_shock_pct} onChange={(e) => setDelta({ ...delta, equity_market_shock_pct: Number(e.target.value) })} /></label>
            </div>
            <button className='btn ghost' onClick={recalc}>Пересчитать what-if</button>
            {whatIf && <p className='muted'>Эффект: Δ базовой стоимости {Number(whatIf?.deltas?.projected_value_delta || 0).toFixed(0)}</p>}
          </div>
        </article>

        <aside className='card'>
          <h3><ShieldAlert size={16} /> Риск-флаги</h3>
          <ul className='rules-list'>
            {(result.flags || []).slice(0, 6).map((f: any, i: number) => <li key={i}><AlertTriangle size={14} />{f.title || f.description || 'Риск-флаг'}</li>)}
          </ul>
          <div className='card soft'>
            <h4>Чек-лист перед самостоятельным решением</h4>
            <ul>
              <li>Проверить стресс-потери и ликвидность</li>
              <li>Сверить ограничения с целями пользователя</li>
              <li>Оценить комиссионную и налоговую нагрузку</li>
            </ul>
          </div>
        </aside>
      </section>
      {error && <div className='error-banner'>{error}</div>}
    </PageShell>
  );
}

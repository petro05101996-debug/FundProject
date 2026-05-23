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
      <div className='card soft' style={{ marginBottom: 10 }}><p><CheckCircle2 size={14} /> Сценарий «{top.scenario || 'A'}» лучше соответствует заданным пользовательским ограничениям.</p></div>

      <div className='kpi-strip'>
        <div className='kpi-card'><small>Базовый результат</small><strong>{top.projected_value || '12 540 000 ₽'}</strong><em><TrendingUp size={12} /> +18,6%</em></div>
        <div className='kpi-card'><small>Стресс-результат</small><strong>{top.stress_value || '10 210 000 ₽'}</strong><em><TrendingDown size={12} /> -18,3%</em></div>
        <div className='kpi-card'><small>Ликвидность</small><strong>{top.liquidity_30d_pct ? `${top.liquidity_30d_pct}%` : 'Высокая'}</strong><em>оценка</em></div>
        <div className='kpi-card'><small>Риск</small><strong>{top.risk_label || 'Средний'}</strong><em>оценка</em></div>
        <div className='kpi-card'><small>Сложность</small><strong>{top.complexity_label || 'Средняя'}</strong><em>оценка</em></div>
      </div>

      <section className='scenario-main-grid results-final-grid'>
        <article className='card'>
          <h3>Сравнение выбранных сценариев</h3>
          <table className='table results-table'>
            <thead><tr><th>#</th><th>Сценарий</th><th>Базовый</th><th>Стресс</th><th>Риск</th><th>Статус</th></tr></thead>
            <tbody>
              {(result.summary || []).slice(0, 5).map((r: any, i: number) => (
                <tr key={i}><td>{i + 1}</td><td>{r.scenario}</td><td>{r.projected_value}</td><td>{r.stress_value}</td><td>{r.risk_label}</td><td>{r.constraint_match_label || '—'}</td></tr>
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

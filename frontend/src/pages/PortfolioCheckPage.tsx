import React, { useMemo, useState } from 'react';
import { api, ApiError } from '../api/client';
import AllocationDonut from '../components/AllocationDonut';
import StressChart from '../components/StressChart';
import CashflowChart from '../components/CashflowChart';
import { ScenarioProfile, profileToAssumptions, profileToConstraints } from '../utils/profileToApi';
import { PageShell, PortfolioTable, InsightPanel, KpiCard, RiskChip } from '../components/ui';

const seed = { scenario: 'Портфель', instrument: 'ОФЗ', ticker: 'OFZ', asset_class: 'Облигации', country: 'RU', currency: 'RUB', market_value: 1000000, expected_return_pct: 10, volatility_pct: 8, liquidity_days: 5, annual_fee_pct: 0.2, tax_pct: 13 };

export default function PortfolioCheckPage({ profile }: { profile: ScenarioProfile }) {
  const [positions, setPositions] = useState<any[]>([seed]);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState('');

  const q = useMemo(() => {
    const total = positions.reduce((a, b) => a + Number(b.market_value || 0), 0);
    const top = Math.max(...positions.map((p) => Number(p.market_value || 0)), 0);
    const avg = positions.reduce((a, b) => a + Number(b.liquidity_days || 0), 0) / Math.max(positions.length, 1);
    return { total, top, avg };
  }, [positions]);

  const update = (index: number, patch: any) => setPositions((prev) => prev.map((p, i) => (i === index ? { ...p, ...patch } : p)));

  const run = async () => {
    setError('');
    try {
      setResult(await api('/api/portfolio/check', { method: 'POST', body: JSON.stringify({ positions, assumptions: profileToAssumptions(profile), constraints: profileToConstraints(profile) }) }));
    } catch (e: any) {
      setError(e instanceof ApiError ? e.message : 'Ошибка расчёта');
    }
  };

  return (
    <PageShell title='Проверить портфель' subtitle='Проверьте концентрацию, ликвидность, риск-флаги и стресс-сценарии по пользовательскому портфелю.'>
      <div className='action-bar'>
        <div className='row'>
          <button className='btn ghost' onClick={() => setPositions((prev) => [...prev, { ...seed }])}>Добавить позицию</button>
          <button className='btn ghost' onClick={() => setPositions([seed])}>Загрузить пример</button>
          <button className='btn ghost' onClick={() => setPositions([{ ...seed }])}>Очистить</button>
          <button className='btn' onClick={run}>Рассчитать портфель</button>
        </div>
      </div>

      <div className='main-grid'>
        <div>
          <PortfolioTable>
            <table className='table'>
              <thead>
                <tr>
                  <th>Инструмент</th><th>Класс</th><th>Валюта</th><th>Сумма</th><th>Доходность %</th><th>Волатильность %</th><th>Ликвидность, дни</th><th>Комиссия %</th><th>Налог %</th><th>Статус</th><th />
                </tr>
              </thead>
              <tbody>
                {positions.length===0 ? <tr><td colSpan={11}><div className='empty-state'><p>Добавьте хотя бы одну позицию.</p></div></td></tr> : positions.map((p, i) => {
                  const risk = Number(p.volatility_pct || 0) > 20 ? 'high' : Number(p.volatility_pct || 0) > 10 ? 'medium' : 'low';
                  return (
                    <tr key={i}>
                      <td><input value={p.instrument} onChange={(e) => update(i, { instrument: e.target.value })} /></td>
                      <td><input value={p.asset_class} onChange={(e) => update(i, { asset_class: e.target.value })} /></td>
                      <td><input value={p.currency} onChange={(e) => update(i, { currency: e.target.value })} /></td>
                      <td><input type='number' value={p.market_value} onChange={(e) => update(i, { market_value: Number(e.target.value) })} /></td>
                      <td><input type='number' value={p.expected_return_pct} onChange={(e) => update(i, { expected_return_pct: Number(e.target.value) })} /></td>
                      <td><input type='number' value={p.volatility_pct} onChange={(e) => update(i, { volatility_pct: Number(e.target.value) })} /></td>
                      <td><input type='number' value={p.liquidity_days} onChange={(e) => update(i, { liquidity_days: Number(e.target.value) })} /></td>
                      <td><input type='number' value={p.annual_fee_pct} onChange={(e) => update(i, { annual_fee_pct: Number(e.target.value) })} /></td>
                      <td><input type='number' value={p.tax_pct} onChange={(e) => update(i, { tax_pct: Number(e.target.value) })} /></td>
                      <td><RiskChip severity={risk}>{risk === 'high' ? 'Высокий' : risk === 'medium' ? 'Средний' : 'Низкий'}</RiskChip></td>
                      <td><button className='btn ghost' onClick={() => setPositions((prev) => prev.filter((_, j) => j !== i))}>Удалить</button></td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </PortfolioTable>

          {result && (
            <>
              <div className='kpi-strip'>
                {[
                  ['Ликвидность 30д', `${Number(result.liquidity_30d || 0).toFixed(1)}%`],
                  ['Top-1 концентрация', `${Number(result.concentration?.top1_pct || 0).toFixed(1)}%`],
                  ['Стресс-просадка', `${Number(result.stress_drawdown || 0).toFixed(1)}%`],
                ].map(([l, v]) => <KpiCard key={String(l)} label={String(l)} value={String(v)} />)}
              </div>
              <div className='row'>{(result.risk_flags || []).map((f: any, i: number) => <RiskChip key={i}>{f.title || f.description || 'Есть риск-флаг'}</RiskChip>)}</div>
              <StressChart rows={result.stress || []} />
              <CashflowChart rows={result.cashflows || []} />
              <div className='card soft'><h4>Слабые места</h4><ul>{(result.weak_points || []).map((w: string, i: number) => <li key={i}>{w}</li>)}</ul></div>
            </>
          )}
        </div>

        <div>
          <AllocationDonut items={result?.allocation_by_asset_class || []} />
          <div className='card'>
            <KpiCard label='Позиций' value={String(positions.length)} />
            <KpiCard label='Общая сумма' value={q.total.toFixed(0)} />
            <KpiCard label='Крупнейшая позиция' value={q.top.toFixed(0)} />
            <KpiCard label='Средняя ликвидность' value={q.avg.toFixed(1)} />
          </div>
          <InsightPanel items={['Портфель проверяется только по введённым позициям', 'Отображаются риск-флаги, слабые места и стресс', 'Сервис не подключается к брокеру и не загружает автоматические данные']} />
        </div>
      </div>

      {error && <div className='error-banner'>{error}</div>}
    </PageShell>
  );
}

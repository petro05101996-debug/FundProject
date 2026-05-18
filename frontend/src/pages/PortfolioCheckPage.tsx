import React, { useMemo, useState } from 'react';
import { api, ApiError } from '../api/client';
import AllocationDonut from '../components/AllocationDonut';
import MetricCard from '../components/MetricCard';
import RiskPassport from '../components/RiskPassport';
import StressChart from '../components/StressChart';
import CashflowChart from '../components/CashflowChart';
import { ScenarioProfile, profileToAssumptions, profileToConstraints } from '../utils/profileToApi';

const seed = { scenario: 'Портфель', instrument: 'ОФЗ', ticker: 'OFZ', asset_class: 'Облигации', country: 'RU', currency: 'RUB', market_value: 1000000, expected_return_pct: 10, volatility_pct: 8, liquidity_days: 5, annual_fee_pct: 0.2, tax_pct: 13 };

export default function PortfolioCheckPage({ profile }: { profile: ScenarioProfile }) {
  const [positions, setPositions] = useState<any[]>([seed]);
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const update = (i: number, k: string, v: any) => setPositions(positions.map((x, j) => (j === i ? { ...x, [k]: v } : x)));
  const quick = useMemo(() => {
    const total = positions.reduce((a, b) => a + Number(b.market_value || 0), 0);
    const top = Math.max(...positions.map(p => Number(p.market_value || 0)), 0);
    const liquid = positions.filter(p => Number(p.liquidity_days || 0) <= 30).reduce((a, b) => a + Number(b.market_value || 0), 0);
    const stocks = positions.filter(p => String(p.asset_class || '').toLowerCase().includes('акц')).reduce((a, b) => a + Number(b.market_value || 0), 0);
    const avgFee = positions.reduce((a, b) => a + Number(b.annual_fee_pct || 0), 0) / Math.max(positions.length, 1);
    const avgVol = positions.reduce((a, b) => a + Number(b.volatility_pct || 0), 0) / Math.max(positions.length, 1);
    return { total, top, liquidPct: total ? (liquid / total) * 100 : 0, stocksPct: total ? (stocks / total) * 100 : 0, avgFee, avgVol };
  }, [positions]);

  const run = async () => {
    setLoading(true); setError('');
    try {
      setResult(await api('/api/portfolio/check', { method: 'POST', body: JSON.stringify({ positions, assumptions: profileToAssumptions(profile), constraints: profileToConstraints(profile) }) }));
    } catch (e: any) { setError(e instanceof ApiError ? e.message : 'Ошибка расчёта'); }
    finally { setLoading(false); }
  };

  return <div className='card'>
    <h2>Проверить портфель</h2><p className='muted'>Введите позиции вручную. Сервис не подключается к брокеру и не получает данные автоматически.</p>
    <div className='kpi-grid'>
      <MetricCard label='Общая стоимость' value={quick.total.toFixed(0)} />
      <MetricCard label='Крупнейшая позиция' value={quick.top.toFixed(0)} />
      <MetricCard label='Ликвидная часть' value={`${quick.liquidPct.toFixed(1)}%`} />
      <MetricCard label='Доля акций' value={`${quick.stocksPct.toFixed(1)}%`} />
      <MetricCard label='Средняя комиссия' value={`${quick.avgFee.toFixed(2)}%`} />
      <MetricCard label='Средняя волатильность' value={`${quick.avgVol.toFixed(1)}%`} />
    </div>
    {positions.map((p, i) => <div key={i} className='card soft'><div className='grid3'>
      <input value={p.instrument} onChange={e => update(i, 'instrument', e.target.value)} placeholder='Инструмент' />
      <input value={p.ticker} onChange={e => update(i, 'ticker', e.target.value)} placeholder='Тикер' />
      <select value={p.asset_class} onChange={e => update(i, 'asset_class', e.target.value)}><option>Облигации</option><option>Акции</option><option>Фонды денежного рынка</option><option>Смешанные фонды</option><option>Другое</option></select>
      <input value={p.country} onChange={e => update(i, 'country', e.target.value)} placeholder='Страна' />
      <input value={p.currency} onChange={e => update(i, 'currency', e.target.value)} placeholder='Валюта' />
      <input type='number' value={p.market_value} onChange={e => update(i, 'market_value', Number(e.target.value))} placeholder='Сумма' />
      <input type='number' value={p.expected_return_pct} onChange={e => update(i, 'expected_return_pct', Number(e.target.value))} placeholder='Доходность %' />
      <input type='number' value={p.volatility_pct} onChange={e => update(i, 'volatility_pct', Number(e.target.value))} placeholder='Волатильность %' />
      <input type='number' value={p.liquidity_days} onChange={e => update(i, 'liquidity_days', Number(e.target.value))} placeholder='Ликвидность (дни)' />
      <input type='number' value={p.annual_fee_pct} onChange={e => update(i, 'annual_fee_pct', Number(e.target.value))} placeholder='Комиссия %' />
      <input type='number' value={p.tax_pct} onChange={e => update(i, 'tax_pct', Number(e.target.value))} placeholder='Налог %' />
      <button className='btn ghost' onClick={() => setPositions(positions.filter((_, j) => j !== i))}>Удалить</button>
    </div></div>)}
    <div className='row'><button className='btn ghost' onClick={() => setPositions([...positions, { ...seed }])}>Добавить позицию</button><button className='btn ghost' onClick={() => setPositions([seed])}>Очистить</button><button className='btn' disabled={loading} onClick={run}>{loading ? 'Считаем...' : 'Рассчитать портфель'}</button></div>{error && <div className='error-banner'>{error}</div>}
    {result && <>
      <div className='kpi-grid'>
        <MetricCard label='Ликвидность 30д' value={`${Number(result.liquidity_30d || 0).toFixed(1)}%`} />
        <MetricCard label='Top-1 концентрация' value={`${Number(result.concentration?.top1_pct || 0).toFixed(1)}%`} />
        <MetricCard label='Top-2 концентрация' value={`${Number(result.concentration?.top2_pct || 0).toFixed(1)}%`} />
        <MetricCard label='Ожидаемая доходность' value={`${Number(result.expected_return || 0).toFixed(1)}%`} />
        <MetricCard label='Стресс-просадка' value={`${Number(result.stress_drawdown || 0).toFixed(1)}%`} />
        <MetricCard label='Риск-флаги' value={String((result.risk_flags || []).length)} />
      </div>
      <RiskPassport risk={result.summary?.risk_label || '—'} liquidity={result.summary?.liquidity_label || '—'} complexity={result.summary?.complexity_label || '—'} />
      <div className='grid2'>
        <AllocationDonut items={result.allocation_by_asset_class || []} />
        <StressChart rows={result.stress || []} />
      </div>
      <CashflowChart rows={result.cashflows || []} />
      <div className='grid2'>
        <div className='card soft'><h4>Слабые места</h4><ul>{(result.weak_points || []).map((w: string, i: number) => <li key={i}>{w}</li>)}</ul></div>
        <div className='card soft'><h4>Риск-флаги</h4><ul>{(result.risk_flags || []).map((f: any, i: number) => <li key={i}>{f.title || f.description || 'Есть риск-флаг'}</li>)}</ul></div>
      </div>
    </>}
  </div>;
}

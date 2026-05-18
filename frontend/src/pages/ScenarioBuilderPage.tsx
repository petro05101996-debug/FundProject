import React, { useMemo, useState } from 'react';
import { api, ApiError } from '../api/client';
import { ScenarioProfile, profileToAssumptions, profileToConstraints } from '../utils/profileToApi';

const assetClasses = ['Денежные средства', 'Облигации', 'Фонды денежного рынка', 'Акции', 'Смешанные фонды', 'Другое'];
const basePos = { instrument: 'Вклад', ticker: 'DEP', asset_class: 'Денежные средства', country: 'RU', currency: 'RUB', market_value: 500000, expected_return_pct: 10, volatility_pct: 2, liquidity_days: 1, annual_fee_pct: 0, tax_pct: 13 };

export default function ScenarioBuilderPage({ profile, onDone }: { profile: ScenarioProfile; onDone: (r: any) => void }) {
  const [positions, setPositions] = useState<any[]>([{ scenario: 'Сценарий A', ...basePos }, { scenario: 'Сценарий B', ...basePos, instrument: 'ОФЗ', asset_class: 'Облигации', expected_return_pct: 12, volatility_pct: 8 }]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const scenarios = useMemo(() => Array.from(new Set(positions.map(p => p.scenario))), [positions]);
  const totals = useMemo(() => Object.fromEntries(scenarios.map(s => [s, positions.filter(p => p.scenario === s).reduce((a, b) => a + Number(b.market_value || 0), 0)])), [positions, scenarios]);

  const addScenario = () => {
    if (scenarios.length >= 5) return setError('Максимум 5 сценариев.');
    setPositions([...positions, { scenario: `Сценарий ${String.fromCharCode(65 + scenarios.length)}`, ...basePos }]);
  };
  const addPos = (scenario: string) => setPositions([...positions, { scenario, ...basePos }]);
  const removeScenario = (scenario: string) => {
    if (scenarios.length <= 2) return setError('Минимум 2 сценария.');
    setPositions(positions.filter(p => p.scenario !== scenario));
  };

  const validate = () => {
    if (scenarios.length < 2) return 'Нужно минимум 2 сценария.';
    if (positions.some(p => !p.instrument || !p.scenario || p.market_value <= 0)) return 'Заполните корректно название инструмента, сценарий и сумму.';
    if (positions.some(p => p.expected_return_pct < -100 || p.expected_return_pct > 100)) return 'Ожидаемая доходность должна быть в диапазоне от -100 до 100%.';
    if (positions.some(p => p.volatility_pct < 0 || p.volatility_pct > 150)) return 'Волатильность должна быть в диапазоне от 0 до 150%.';
    if (positions.some(p => p.tax_pct < 0 || p.tax_pct > 100)) return 'Налог должен быть в диапазоне 0–100%.';
    return '';
  };

  const submit = async () => {
    const v = validate(); if (v) return setError(v);
    setLoading(true); setError('');
    try {
      const r = await api('/api/scenario/analyze', {
        method: 'POST',
        body: JSON.stringify({ assumptions: profileToAssumptions(profile), constraints: profileToConstraints(profile), positions }),
      });
      localStorage.setItem('analysisResult', JSON.stringify(r));
      localStorage.setItem('scenarioPositions', JSON.stringify(positions));
      onDone(r);
    } catch (e: any) {
      setError(e instanceof ApiError ? e.message : 'Ошибка расчёта');
    } finally { setLoading(false); }
  };

  return <div className='card'>
    <h2>Сравнить мои варианты</h2>
    <p className='muted'>Соберите 2–5 сценариев и сравните их по ограничениям пользователя.</p>
    <div className='row'><button className='btn ghost' onClick={addScenario}>Добавить сценарий</button><button className='btn' disabled={loading} onClick={submit}>{loading ? 'Считаем...' : 'Рассчитать сравнение'}</button></div>
    {scenarios.map(s => <div key={s} className='card soft'>
      <div className='row' style={{ justifyContent: 'space-between' }}><h4>{s}</h4><div className='row'><span className='pill active'>Сумма: {totals[s].toFixed(0)}</span><button className='btn ghost' onClick={() => addPos(s)}>Добавить позицию</button><button className='btn ghost' onClick={() => removeScenario(s)}>Удалить сценарий</button></div></div>
      {positions.map((p, i) => p.scenario === s && <div key={i} className='grid3'>
        <input placeholder='Инструмент' value={p.instrument} onChange={e => setPositions(positions.map((x, j) => j === i ? { ...x, instrument: e.target.value } : x))} />
        <input placeholder='Тикер' value={p.ticker} onChange={e => setPositions(positions.map((x, j) => j === i ? { ...x, ticker: e.target.value } : x))} />
        <select value={p.asset_class} onChange={e => setPositions(positions.map((x, j) => j === i ? { ...x, asset_class: e.target.value } : x))}>{assetClasses.map(a => <option key={a}>{a}</option>)}</select>
        <input placeholder='Страна' value={p.country} onChange={e => setPositions(positions.map((x, j) => j === i ? { ...x, country: e.target.value } : x))} />
        <input placeholder='Валюта' value={p.currency} onChange={e => setPositions(positions.map((x, j) => j === i ? { ...x, currency: e.target.value } : x))} />
        <input type='number' placeholder='Сумма' value={p.market_value} onChange={e => setPositions(positions.map((x, j) => j === i ? { ...x, market_value: Number(e.target.value) } : x))} />
        <input type='number' placeholder='Доходность %' value={p.expected_return_pct} onChange={e => setPositions(positions.map((x, j) => j === i ? { ...x, expected_return_pct: Number(e.target.value) } : x))} />
        <input type='number' placeholder='Волатильность %' value={p.volatility_pct} onChange={e => setPositions(positions.map((x, j) => j === i ? { ...x, volatility_pct: Number(e.target.value) } : x))} />
        <input type='number' placeholder='Ликвидность (дни)' value={p.liquidity_days} onChange={e => setPositions(positions.map((x, j) => j === i ? { ...x, liquidity_days: Number(e.target.value) } : x))} />
        <input type='number' placeholder='Комиссия %' value={p.annual_fee_pct} onChange={e => setPositions(positions.map((x, j) => j === i ? { ...x, annual_fee_pct: Number(e.target.value) } : x))} />
        <input type='number' placeholder='Налог %' value={p.tax_pct} onChange={e => setPositions(positions.map((x, j) => j === i ? { ...x, tax_pct: Number(e.target.value) } : x))} />
        <button className='btn ghost' onClick={() => setPositions(positions.filter((_, j) => j !== i))}>Удалить позицию</button>
      </div>)}
      <p className='muted'>Подсказка: избегайте высокой концентрации и длинной неликвидности в одном сценарии.</p>
    </div>)}
    {error && <div className='error-banner'>{error}</div>}
  </div>;
}

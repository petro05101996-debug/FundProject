import React, { useMemo, useState } from 'react';
import { AlertTriangle, CheckCircle2, Droplets, PieChart, Plus, Trash2 } from 'lucide-react';
import { api, ApiError } from '../api/client';
import { ScenarioProfile, profileToAssumptions, profileToConstraints } from '../utils/profileToApi';
import { PageShell } from '../components/ui';

const ASSET_CLASSES = ['Денежные средства', 'Облигации', 'Акции', 'Товары', 'Недвижимость', 'Альтернативные'];
const seed = { scenario: 'Портфель', instrument: 'Сбербанк (обык.)', ticker: 'SBER', asset_class: 'Акции', currency: 'RUB', market_value: 1000000, expected_return_pct: 10, volatility_pct: 8, liquidity_days: 5, annual_fee_pct: 0.2, tax_pct: 13 };

export default function PortfolioCheckPage({ profile }: { profile: ScenarioProfile }) {
  const [positions, setPositions] = useState<any[]>([seed, { ...seed, instrument: 'ЛУКОЙЛ', ticker: 'LKOH', market_value: 800000 }, { ...seed, instrument: 'ОФЗ 26243', ticker: 'SU26243', asset_class: 'Облигации', market_value: 700000, volatility_pct: 4 }]);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState('');

  const total = useMemo(() => positions.reduce((a, b) => a + Number(b.market_value || 0), 0), [positions]);
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
    <PageShell title='Проверить портфель' subtitle='Анализ структуры существующего портфеля, введенного вручную, без интеграции с брокером.'>
      <div className='row' style={{ marginBottom: 12 }}>
        <button className='btn' onClick={() => setPositions((prev) => [...prev, { ...seed }])}><Plus size={14} />Добавить позицию</button>
        <button className='btn ghost' onClick={() => setPositions([seed])}><Trash2 size={14} />Очистить</button>
      </div>

      <section className='scenario-main-grid portfolio-final-grid'>
        <article className='card'>
          <h3>Позиции портфеля</h3>
          <table className='table portfolio-table-final'>
            <thead><tr><th>Инструмент</th><th>Класс</th><th>Сумма</th><th>Доля</th><th>Риск</th><th>Ликвидность</th><th /></tr></thead>
            <tbody>
              {positions.map((p, i) => (
                <tr key={i}>
                  <td><input value={p.instrument} onChange={(e) => update(i, { instrument: e.target.value })} /></td>
                  <td><select value={p.asset_class} onChange={(e) => update(i, { asset_class: e.target.value })}>{ASSET_CLASSES.map((a)=><option key={a} value={a}>{a}</option>)}</select></td>
                  <td><input type='number' value={p.market_value} onChange={(e) => update(i, { market_value: Number(e.target.value) })} /></td>
                  <td>{((Number(p.market_value || 0) / Math.max(total, 1)) * 100).toFixed(1)}%</td>
                  <td><span className={`risk-chip ${p.volatility_pct > 10 ? 'high' : ''}`}>{p.volatility_pct > 10 ? 'Высокий' : p.volatility_pct > 5 ? 'Средний' : 'Низкий'}</span></td>
                  <td>{Number(p.liquidity_days||0) <= 3 ? 'Высокая' : Number(p.liquidity_days||0) <= 10 ? 'Средняя' : 'Низкая'}</td>
                  <td><button className='btn ghost' onClick={() => setPositions((prev) => prev.filter((_, idx) => idx !== i))}>—</button></td>
                </tr>
              ))}
            </tbody>
          </table>

          <div className='card soft' style={{ marginTop: 10 }}>
            <p className='muted'><AlertTriangle size={14} /> MVP не сохраняет введённые данные после завершения сессии.</p>
          </div>

          <div className='row' style={{ marginTop: 10 }}>
            <button className='btn' onClick={run}>Проверить портфель</button>
            <button className='btn ghost' disabled title='Будет доступно после расчёта'>Сформировать отчёт</button>
          </div>
        </article>

        <aside className='card'>
          <h3><PieChart size={16} /> Структура портфеля</h3>
          <p className='muted'>Общая сумма: {total.toLocaleString('ru-RU')} ₽</p>
          <ul className='rules-list'>
            <li><CheckCircle2 size={16} />Концентрация (top-2): {result?.concentration?.top2_pct?.toFixed?.(1) ?? 'нет данных'}%</li>
            <li><Droplets size={16} />Взвешенная ликвидность: {result?.liquidity_label ?? 'нет данных'}</li>
            <li><AlertTriangle size={16} />Ожидаемая комиссия: {result?.fees_annual_pct != null ? `${result.fees_annual_pct}%` : 'нет данных'}</li>
          </ul>
          <div className='card soft'>
            <h4>Замечания</h4>
            <ul>
              {(result?.weak_points || []).length ? (result.weak_points.map((w: string, i: number) => <li key={i}>{w}</li>)) : <li>нет данных</li>}
            </ul>
          </div>
        </aside>
      </section>

      {error && <div className='error-banner'>{error}</div>}
    </PageShell>
  );
}

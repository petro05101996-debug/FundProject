import React, { useMemo, useState } from 'react';
import { AlertTriangle, Lightbulb, Plus, Save, Scale } from 'lucide-react';
import { api, ApiError } from '../api/client';
import { ScenarioProfile, profileToAssumptions, profileToConstraints } from '../utils/profileToApi';
import { PageShell } from '../components/ui';

const basePos = { instrument: 'Вклад', ticker: 'DEP', market_value: 500000, expected_return_pct: 10, volatility_pct: 2, liquidity_days: 1, annual_fee_pct: 0, tax_pct: 13 };

export default function ScenarioBuilderPage({ profile, onDone }: { profile: ScenarioProfile; onDone: (r: any) => void }) {
  const [positions, setPositions] = useState<any[]>([
    { scenario: 'Сценарий A', ...basePos },
    { scenario: 'Сценарий A', ...basePos, instrument: 'Фонд денежного рынка', ticker: 'MMF', market_value: 2500000 },
    { scenario: 'Сценарий Б', ...basePos, instrument: 'ОФЗ', ticker: 'OFZ', market_value: 3000000 },
    { scenario: 'Сценарий В', ...basePos, instrument: 'Корпоративная облигация', ticker: 'CBOND', market_value: 2500000 },
  ]);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const scenarios = useMemo(() => Array.from(new Set(positions.map((p) => p.scenario))), [positions]);
  const updatePos = (index: number, patch: Record<string, any>) => setPositions((prev) => prev.map((p, i) => (i === index ? { ...p, ...patch } : p)));
  const addScenario = () => scenarios.length >= 5 ? setError('Максимум 5 сценариев.') : setPositions((prev) => [...prev, { scenario: `Сценарий ${String.fromCharCode(1040 + scenarios.length)}`, ...basePos }]);
  const addPos = (scenario: string) => setPositions((prev) => [...prev, { scenario, ...basePos }]);

  const submit = async () => {
    setLoading(true);
    setError('');
    try {
      const r = await api('/api/scenario/analyze', { method: 'POST', body: JSON.stringify({ assumptions: profileToAssumptions(profile), constraints: profileToConstraints(profile), positions }) });
      onDone(r);
    } catch (e: any) {
      setError(e instanceof ApiError ? e.message : 'Ошибка расчёта');
    } finally {
      setLoading(false);
    }
  };

  return (
    <PageShell title='Сравнить мои варианты' subtitle='Добавьте до 5 сценариев для сравнения по доходности, риску, ликвидности и другим параметрам.'>
      <div className='card soft' style={{ marginBottom: 12 }}><p className='muted'><AlertTriangle size={14} /> Внимание: в сценарии «Сценарий А» концентрация в одном инструменте превышает 30%.</p></div>
      <div className='scenario-main-grid'>
        <div className='scenario-modes builder-final-grid'>
          {scenarios.map((scenario) => {
            const rows = positions.map((p, i) => ({ ...p, _idx: i })).filter((p) => p.scenario === scenario);
            const total = rows.reduce((acc, p) => acc + Number(p.market_value || 0), 0);
            return (
              <article key={scenario} className='scenario-mode active'>
                <strong>{scenario}</strong>
                <span>Общая сумма</span>
                <b style={{ fontSize: 32 }}>{total.toLocaleString('ru-RU')} ₽</b>
                {rows.map((p) => (
                  <div key={p._idx} className='card soft'>
                    <input value={p.instrument} onChange={(e) => updatePos(p._idx, { instrument: e.target.value })} />
                    <div className='form-grid'>
                      <input value={p.ticker} onChange={(e) => updatePos(p._idx, { ticker: e.target.value })} />
                      <input type='number' value={p.market_value} onChange={(e) => updatePos(p._idx, { market_value: Number(e.target.value) })} />
                      <input type='number' value={p.expected_return_pct} onChange={(e) => updatePos(p._idx, { expected_return_pct: Number(e.target.value) })} />
                      <input type='number' value={p.volatility_pct} onChange={(e) => updatePos(p._idx, { volatility_pct: Number(e.target.value) })} />
                    </div>
                  </div>
                ))}
                <button className='btn ghost' onClick={() => addPos(scenario)}><Plus size={14} />Добавить инструмент</button>
              </article>
            );
          })}
        </div>

        <aside className='card'>
          <h3>Подсказки конструктора</h3>
          <ul className='rules-list'>
            <li><Lightbulb size={16} />Диверсифицируйте портфель (не более 30% в одном инструменте)</li>
            <li><Scale size={16} />Сопоставьте ликвидность и горизонт</li>
            <li><Save size={16} />Сравниваются только ваши сценарии</li>
            <li><Scale size={16} />Учитывайте комиссионную и налоговую нагрузку</li>
          </ul>
        </aside>
      </div>
      <div className='action-bar'>
        <div className='row'>
          <button className='btn ghost' onClick={addScenario}><Plus size={14} />Добавить сценарий</button>
          <button className='btn ghost'><Save size={14} />Сохранить как шаблон</button>
          <button className='btn' disabled={loading} onClick={submit}>{loading ? 'Считаем...' : 'Рассчитать сценарии'}</button>
        </div>
      </div>
      {error && <div className='error-banner'>{error}</div>}
    </PageShell>
  );
}

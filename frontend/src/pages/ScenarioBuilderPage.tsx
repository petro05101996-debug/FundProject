import React, { useMemo, useState } from 'react';
import { api, ApiError } from '../api/client';
import { ScenarioProfile, profileToAssumptions, profileToConstraints } from '../utils/profileToApi';
import { PageShell, StatusBanner, InsightPanel, ScenarioCard, ActionBar, FormField, RiskChip } from '../components/ui';

const assetClasses = ['Денежные средства', 'Облигации', 'Фонды денежного рынка', 'Акции', 'Смешанные фонды', 'Другое'];
const basePos = { instrument: 'Вклад', ticker: 'DEP', asset_class: 'Денежные средства', country: 'RU', currency: 'RUB', market_value: 500000, expected_return_pct: 10, volatility_pct: 2, liquidity_days: 1, annual_fee_pct: 0, tax_pct: 13 };

export default function ScenarioBuilderPage({ profile, onDone }: { profile: ScenarioProfile; onDone: (r: any) => void }) {
  const [positions, setPositions] = useState<any[]>([{ scenario: 'Сценарий A', ...basePos }, { scenario: 'Сценарий B', ...basePos, instrument: 'ОФЗ', asset_class: 'Облигации' }]);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const scenarios = useMemo(() => Array.from(new Set(positions.map((p) => p.scenario))), [positions]);

  const updatePos = (index: number, patch: Record<string, any>) => {
    setPositions((prev) => prev.map((p, i) => (i === index ? { ...p, ...patch } : p)));
  };

  const addScenario = () => {
    if (scenarios.length >= 5) return setError('Максимум 5 сценариев.');
    setError('');
    setPositions((prev) => [...prev, { scenario: `Сценарий ${String.fromCharCode(65 + scenarios.length)}`, ...basePos }]);
  };

  const addPos = (scenario: string) => setPositions((prev) => [...prev, { scenario, ...basePos }]);

  const removeScenario = (scenario: string) => {
    if (scenarios.length <= 2) return setError('Нужно минимум 2 сценария.');
    setError('');
    setPositions((prev) => prev.filter((p) => p.scenario !== scenario));
  };

  const submit = async () => {
    setLoading(true);
    setError('');
    try {
      const r = await api('/api/scenario/analyze', {
        method: 'POST',
        body: JSON.stringify({ assumptions: profileToAssumptions(profile), constraints: profileToConstraints(profile), positions }),
      });
      onDone(r);
    } catch (e: any) {
      setError(e instanceof ApiError ? e.message : 'Ошибка расчёта');
    } finally {
      setLoading(false);
    }
  };

  return (
    <PageShell title='Сравнить мои варианты' subtitle='Добавьте 2–5 пользовательских сценариев и сравните последствия по заданным ограничениям.'>
      <StatusBanner title='Важно' description='Сервис сравнивает только введённые вами сценарии. Это не рекомендация и не выбор лучшего инструмента.' />
      <div className='main-grid'>
        <div>
          {scenarios.map((scenario) => {
            const rows = positions
              .map((p, i) => ({ ...p, _idx: i }))
              .filter((p) => p.scenario === scenario);
            const total = rows.reduce((acc, p) => acc + Number(p.market_value || 0), 0);

            return (
              <ScenarioCard key={scenario} title={scenario} meta={`Сумма ${total.toFixed(0)} ₽ · Позиций ${rows.length}`}>
                <div className='row'>
                  <RiskChip>Локальный ввод</RiskChip>
                  <RiskChip>Пользовательский сценарий</RiskChip>
                </div>
                <div className='form-grid'>
                  {rows.map((p) => (
                    <div className='card soft' key={p._idx}>
                      <FormField label='Инструмент'><input value={p.instrument} onChange={(e) => updatePos(p._idx, { instrument: e.target.value })} /></FormField>
                      <FormField label='Тикер'><input value={p.ticker} onChange={(e) => updatePos(p._idx, { ticker: e.target.value })} /></FormField>
                      <FormField label='Класс'><select value={p.asset_class} onChange={(e) => updatePos(p._idx, { asset_class: e.target.value })}>{assetClasses.map((a) => <option key={a}>{a}</option>)}</select></FormField>
                      <FormField label='Сумма, ₽'><input type='number' value={p.market_value} onChange={(e) => updatePos(p._idx, { market_value: Number(e.target.value) })} /></FormField>
                      <FormField label='Доходность, %'><input type='number' value={p.expected_return_pct} onChange={(e) => updatePos(p._idx, { expected_return_pct: Number(e.target.value) })} /></FormField>
                      <FormField label='Волатильность, %'><input type='number' value={p.volatility_pct} onChange={(e) => updatePos(p._idx, { volatility_pct: Number(e.target.value) })} /></FormField>
                      <button className='btn ghost' onClick={() => setPositions((prev) => prev.filter((_, i) => i !== p._idx))}>Удалить позицию</button>
                    </div>
                  ))}
                </div>
                <div className='row'>
                  <button className='btn ghost' onClick={() => addPos(scenario)}>Добавить позицию</button>
                  <button className='btn ghost' onClick={() => removeScenario(scenario)}>Удалить сценарий</button>
                </div>
              </ScenarioCard>
            );
          })}
        </div>
        <InsightPanel title='Подсказки конструктора' items={['Правила сравнения: учитываются только введённые параметры', 'Влияют доходность, волатильность, комиссии и налоги', 'Ограничения анализа отражаются в итогах и отчёте']} />
      </div>
      <ActionBar hint='Сценарии сохраняются локально до пересчёта.'>
        <button className='btn ghost' onClick={addScenario}>Добавить сценарий</button>
        <button className='btn' disabled={loading} onClick={submit}>{loading ? 'Считаем...' : 'Рассчитать сравнение'}</button>
        <button className='btn ghost' onClick={() => setPositions([{ scenario: 'Сценарий A', ...basePos }, { scenario: 'Сценарий B', ...basePos, instrument: 'ОФЗ', asset_class: 'Облигации' }])}>Очистить</button>
      </ActionBar>
      {error && <div className='error-banner'>{error}</div>}
    </PageShell>
  );
}

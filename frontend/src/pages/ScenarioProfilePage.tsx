import React from 'react';
import { ScenarioProfile } from '../utils/profileToApi';
import { PageShell, InsightPanel, FormField, ActionBar, RiskChip } from '../components/ui';

const modes = [
  ['instrument', 'Проверить инструмент', 'Оценка одного инструмента по доходу, стрессу, ликвидности и флагам'],
  ['builder', 'Сравнить мои варианты', 'Сопоставление 2–5 пользовательских сценариев по ограничениям'],
  ['portfolio', 'Проверить портфель', 'Анализ концентрации, ликвидности и стресс-устойчивости портфеля'],
  ['explain', 'Объяснить инструмент', 'Образовательный разбор рисков, дохода и ограничений'],
] as const;

export default function ScenarioProfilePage({ profile, setProfile, onNavigate }: { profile: ScenarioProfile; setProfile: (v: ScenarioProfile) => void; onNavigate: (k: any) => void }) {
  const set = (k: keyof ScenarioProfile, v: any) => setProfile({ ...profile, [k]: v });

  return (
    <PageShell title='Параметры сценария' subtitle='Выберите режим анализа и задайте ограничения, по которым сервис будет оценивать введённые варианты.'>
      <div className='mode-grid'>
        {modes.map(([k, t, d]) => (
          <div className='mode-card card' key={k}>
            <h3>{t}</h3>
            <p className='muted'>{d}</p>
            <div className='row'><RiskChip>Сценарный анализ</RiskChip><RiskChip>Риск-флаги</RiskChip><RiskChip>Ограничения</RiskChip></div>
            <button className='btn' onClick={() => onNavigate(k)}>Открыть</button>
          </div>
        ))}
      </div>
      <div className='main-grid'>
        <div>
          <div className='form-section card'><h3>Базовые параметры</h3><div className='form-grid'><FormField label='Сумма, ₽'><input type='number' value={profile.amount} onChange={(e) => set('amount', Number(e.target.value))} /></FormField><FormField label='Горизонт, лет'><input type='number' value={profile.horizon_years} onChange={(e) => set('horizon_years', Number(e.target.value))} /></FormField></div></div>
          <div className='form-section card'><h3>Цель и горизонт</h3><FormField label='Цель'><select value={profile.goal} onChange={(e) => set('goal', e.target.value)}><option>Сохранить капитал</option><option>Получать регулярный доход</option><option>Умеренный рост</option><option>Долгосрочный рост</option></select></FormField><div className='form-grid'><FormField label='Досрочный выход'><input type='checkbox' checked={profile.early_exit_required} onChange={(e) => set('early_exit_required', e.target.checked)} /></FormField><FormField label='Макс. просадка, %'><input type='number' value={profile.max_drawdown_pct} onChange={(e) => set('max_drawdown_pct', Number(e.target.value))} /></FormField></div></div>
          <div className='form-section card'><h3>Риск-ограничения</h3><div className='form-grid'><FormField label='Мин. ликвидность 30д, %'><input type='number' value={profile.min_liquidity_pct_30d} onChange={(e) => set('min_liquidity_pct_30d', Number(e.target.value))} /></FormField><FormField label='Макс. доля позиции, %'><input type='number' value={profile.max_single_position_pct} onChange={(e) => set('max_single_position_pct', Number(e.target.value))} /></FormField><FormField label='Макс. доля класса, %'><input type='number' value={profile.max_asset_class_pct} onChange={(e) => set('max_asset_class_pct', Number(e.target.value))} /></FormField><FormField label='Макс. волатильность, %'><input type='number' value={profile.max_portfolio_volatility_pct} onChange={(e) => set('max_portfolio_volatility_pct', Number(e.target.value))} /></FormField></div></div>
          <div className='form-section card'><h3>Комиссии и налоги</h3><div className='form-grid'><FormField label='Учитывать комиссии'><input type='checkbox' checked={profile.include_fees} onChange={(e) => set('include_fees', e.target.checked)} /></FormField><FormField label='Учитывать налоги'><input type='checkbox' checked={profile.include_taxes} onChange={(e) => set('include_taxes', e.target.checked)} /></FormField><FormField label='Налог, %'><input type='number' value={profile.tax_pct} onChange={(e) => set('tax_pct', Number(e.target.value))} /></FormField><FormField label='Инфляция, %'><input type='number' value={profile.inflation_pct} onChange={(e) => set('inflation_pct', Number(e.target.value))} /></FormField></div></div>
        </div>
        <InsightPanel title='Краткие правила расчёта' items={['Как сервис считает: только по введённым данным', 'Что влияет: доходность, волатильность, комиссии, налоги', 'Ограничения анализа показываются в итогах и отчёте', 'Сервис не является индивидуальной инвестиционной рекомендацией']} />
      </div>
      <ActionBar hint='Параметры сохраняются локально в браузере.'><button className='btn'>Сохранить параметры</button><button className='btn ghost' onClick={() => onNavigate('builder')}>Перейти к сравнению вариантов</button></ActionBar>
    </PageShell>
  );
}

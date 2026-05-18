import React from 'react';
import { ScenarioProfile } from '../utils/profileToApi';

const modes = [
  ['instrument', 'Проверить инструмент', 'Оценка последствий по одному инструменту.'],
  ['builder', 'Сравнить мои варианты', 'Сравнение 2–5 пользовательских сценариев.'],
  ['portfolio', 'Проверить портфель', 'Проверка концентрации, ликвидности и риск-флагов.'],
  ['explain', 'Объяснить инструмент', 'Образовательная справка без рекомендаций.'],
] as const;

export default function ScenarioProfilePage({ profile, setProfile, onNavigate }: { profile: ScenarioProfile; setProfile: (v: ScenarioProfile) => void; onNavigate: (k: any) => void }) {
  const set = (k: keyof ScenarioProfile, v: any) => setProfile({ ...profile, [k]: v });

  return (
    <>
      <div className='card'>
        <h2>Параметры сценария</h2>
        <p className='muted'>Задайте ограничения, по которым сервис будет сравнивать введённые варианты.</p>
      </div>
      <div className='grid2'>
        <div className='card'>
          <h3>Профиль пользователя</h3>
          <div className='grid2'>
            <label>Сумма, ₽<input type='number' value={profile.amount} onChange={e => set('amount', Number(e.target.value))} /></label>
            <label>Горизонт, лет<input type='number' min={1} value={profile.horizon_years} onChange={e => set('horizon_years', Number(e.target.value))} /></label>
          </div>
          <label>Цель
            <select value={profile.goal} onChange={e => set('goal', e.target.value)}>
              <option>Сохранить капитал</option><option>Получать регулярный доход</option><option>Умеренный рост</option><option>Долгосрочный рост</option>
            </select>
          </label>
          <div className='grid2'>
            <label>Нужен досрочный выход<input type='checkbox' checked={profile.early_exit_required} onChange={e => set('early_exit_required', e.target.checked)} /></label>
            <label>Макс. просадка, %<input type='number' min={0} max={100} value={profile.max_drawdown_pct} onChange={e => set('max_drawdown_pct', Number(e.target.value))} /></label>
          </div>
          <div className='grid3'>
            <label>Опыт
              <select value={profile.experience} onChange={e => set('experience', e.target.value as any)}>
                <option value='beginner'>Новичок</option><option value='basic'>Базовый</option><option value='advanced'>Продвинутый</option>
              </select>
            </label>
            <label>Учитывать комиссии<input type='checkbox' checked={profile.include_fees} onChange={e => set('include_fees', e.target.checked)} /></label>
            <label>Учитывать налоги<input type='checkbox' checked={profile.include_taxes} onChange={e => set('include_taxes', e.target.checked)} /></label>
          </div>
          <div className='grid2'>
            <label>Налоговая ставка, %<input type='number' min={0} max={100} value={profile.tax_pct} onChange={e => set('tax_pct', Number(e.target.value))} /></label>
            <label>Инфляция, %<input type='number' min={0} max={100} value={profile.inflation_pct} onChange={e => set('inflation_pct', Number(e.target.value))} /></label>
          </div>
        </div>

        <div className='card'>
          <h3>Ограничения анализа</h3>
          <label>Минимальная ликвидность 30д, %<input type='number' value={profile.min_liquidity_pct_30d} onChange={e => set('min_liquidity_pct_30d', Number(e.target.value))} /></label>
          <label>Максимальная доля одной позиции, %<input type='number' value={profile.max_single_position_pct} onChange={e => set('max_single_position_pct', Number(e.target.value))} /></label>
          <label>Максимальная доля класса активов, %<input type='number' value={profile.max_asset_class_pct} onChange={e => set('max_asset_class_pct', Number(e.target.value))} /></label>
          <label>Максимальная волатильность, %<input type='number' value={profile.max_portfolio_volatility_pct} onChange={e => set('max_portfolio_volatility_pct', Number(e.target.value))} /></label>
          <label>Максимальный fee drag, %<input type='number' value={profile.max_fee_drag_pct} onChange={e => set('max_fee_drag_pct', Number(e.target.value))} /></label>

          <div className='card soft'>
            <h4>Как сервис считает</h4>
            <ul>
              <li>Использует только пользовательский ввод.</li>
              <li>Сравнивает сценарии по заданным ограничениям.</li>
              <li>Показывает риск-флаги и ограничения анализа.</li>
              <li>Не является индивидуальной инвестиционной рекомендацией.</li>
            </ul>
          </div>
        </div>
      </div>

      <div className='grid2'>
        {modes.map(([k, title, desc]) => (
          <div key={k} className='card soft'>
            <h4>{title}</h4>
            <p className='muted'>{desc}</p>
            <button className='btn' onClick={() => onNavigate(k)}>Открыть режим</button>
          </div>
        ))}
      </div>
    </>
  );
}

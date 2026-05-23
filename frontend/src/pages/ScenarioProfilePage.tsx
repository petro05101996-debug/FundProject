import React from 'react';
import { Activity, BarChart3, Briefcase, CircleDollarSign, Scale, ShieldCheck } from 'lucide-react';
import { ScenarioProfile } from '../utils/profileToApi';
import { PageShell } from '../components/ui';

const modes = [
  ['instrument', 'Проверить инструмент', 'Оценка риска, доходности и устойчивости одного инвестиционного инструмента.', Activity],
  ['builder', 'Сравнить мои варианты', 'Сравнение ваших вариантов по риску, доходности, ликвидности и комиссиям.', Scale],
  ['portfolio', 'Проверить портфель', 'Анализ текущего портфеля на устойчивость к рискам и рыночным сценариям.', Briefcase],
  ['explain', 'Объяснить инструмент', 'Понятное объяснение инструмента, рисков и ключевых параметров.', BarChart3],
] as const;

export default function ScenarioProfilePage({ profile, setProfile, onNavigate }: { profile: ScenarioProfile; setProfile: (v: ScenarioProfile) => void; onNavigate: (k: any) => void }) {
  const set = (k: keyof ScenarioProfile, v: any) => setProfile({ ...profile, [k]: v });

  return (
    <PageShell title='Параметры пользовательского сценария' subtitle='Выберите режим анализа и задайте параметры сценария'>
      <section className='scenario-modes'>
        {modes.map(([k, t, d, Icon]) => (
          <button key={k} className={`scenario-mode ${k === 'builder' ? 'active' : ''}`} onClick={() => onNavigate(k)}>
            <Icon size={18} />
            <strong>{t}</strong>
            <span>{d}</span>
          </button>
        ))}
      </section>

      <section className='scenario-main-grid'>
        <article className='card'>
          <h3>Параметры сценария</h3>
          <p className='muted'>Укажите ваши исходные данные и предпочтения для анализа</p>

          <div className='form-grid'>
            <label className='form-field'><span>Сумма</span><div className='input-wrap'><input type='number' value={profile.amount} onChange={(e) => set('amount', Number(e.target.value))} /><em>₽</em></div></label>
            <label className='form-field'><span>Горизонт (мес)</span><div className='input-wrap'><input type='number' value={profile.horizon_years * 12} onChange={(e) => set('horizon_years', Number(e.target.value) / 12)} /><em>мес</em></div></label>
            <label className='form-field'><span>Цель</span><select value={profile.goal} onChange={(e) => set('goal', e.target.value)}><option>Рост капитала</option><option>Сохранение капитала</option><option>Регулярный доход</option></select></label>
          </div>

          <div className='form-grid'>
            <label className='form-field'><span>Могут ли понадобиться раньше?</span><select value={profile.early_exit_required ? 'Да' : 'Нет'} onChange={(e) => set('early_exit_required', e.target.value === 'Да')}><option>Нет</option><option>Возможно</option><option>Да</option></select></label>
            <label className='form-field'><span>Допустимая просадка</span><select value={profile.max_drawdown_pct} onChange={(e) => set('max_drawdown_pct', Number(e.target.value))}><option value={10}>Консервативная (-5% — -10%)</option><option value={20}>Умеренная (-10% — -20%)</option><option value={30}>Агрессивная (-20% — -30%)</option></select></label>
          </div>

          <div className='form-grid'>
            <label className='form-field'><span>Опыт пользователя</span><select><option>Начинающий</option><option>Средний</option><option>Опытный</option><option>Профессионал</option></select></label>
            <label className='form-field'><span>Мин. ликвидность 30д, %</span><div className='input-wrap'><input type='number' value={profile.min_liquidity_pct_30d} onChange={(e) => set('min_liquidity_pct_30d', Number(e.target.value))} /><em>%</em></div></label>
          </div>

          <div className='form-grid'>
            <label className='form-field'><span>Учитывать комиссии</span><input type='checkbox' checked={profile.include_fees} onChange={(e) => set('include_fees', e.target.checked)} /></label>
            <label className='form-field'><span>Учитывать налог</span><input type='checkbox' checked={profile.include_taxes} onChange={(e) => set('include_taxes', e.target.checked)} /></label>
            <label className='form-field'><span>Ставка налога</span><div className='input-wrap'><input type='number' value={profile.tax_pct} onChange={(e) => set('tax_pct', Number(e.target.value))} /><em>%</em></div></label>
          </div>

          <div className='row'>
            <button className='btn' onClick={() => onNavigate('builder')}>Продолжить к сценариям</button>
            <button className='btn ghost'>Очистить данные</button>
          </div>
        </article>

        <aside className='card'>
          <h3>Краткие правила расчёта</h3>
          <ul className='rules-list'>
            <li><CircleDollarSign size={16} />Ожидаемая доходность</li>
            <li><Activity size={16} />Риск и волатильность</li>
            <li><ShieldCheck size={16} />Ликвидность</li>
            <li><Scale size={16} />Комиссии и налоги</li>
            <li><BarChart3 size={16} />Стресс-сценарии</li>
          </ul>
          <div className='card soft'>
            <p className='muted'>Сервис предоставляет информационно-аналитические материалы и не является индивидуальной инвестиционной рекомендацией.</p>
          </div>
        </aside>
      </section>
    </PageShell>
  );
}

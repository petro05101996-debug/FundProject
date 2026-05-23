import React from 'react';
import {
  Activity,
  BarChart3,
  Briefcase,
  Check,
  FileText,
  Lock,
  Moon,
  Scale,
  Shield,
  TrendingUp,
  X,
} from 'lucide-react';
import { LandingShell } from '../components/ui';

const scenarioRows = [
  ['Риск (VaR 95%)', '-18,3%', '1 год'],
  ['Макс. просадка', '-24,7%', 'за период'],
  ['Ликвидность', 'Высокая', 'оценка'],
  ['Комиссии', '0,72%', 'в год'],
  ['Налоги (оценка)', '12,4%', 'в год'],
];

export default function LandingPage({ onStart, onExplain, onOfferCheck }: { onStart: () => void; onExplain: () => void; onOfferCheck: () => void }) {
  return (
    <LandingShell>
      <div className='mock-stage'>
        <section className='mock-frame'>
          <header className='mock-topbar'>
            <div className='brand'>
              <div className='brand-icon'><Briefcase size={16} /></div>
              <div>
                <b>Investment Scenario Lab</b>
                <p>Финансовый сценарный анализатор</p>
              </div>
            </div>
            <nav>
              <a href='#features'>Возможности</a><a href='#how-it-works'>Как это работает</a><a href='#about'>О проекте</a>
            </nav>
            <div className='toolbar-right'>
              <button className='icon-btn'><Moon size={14} /></button>
              <button className='link-btn' onClick={onStart}>Начать</button>
              <button className='btn outline' onClick={onStart}>Перейти к расчёту</button>
            </div>
          </header>

          <div className='mock-main'>
            <article className='hero-left'>
              <h1>Проверьте <span>инвестиционный сценарий</span> до покупки</h1>
              <p>Сравнивайте свои сценарии, оценивайте риски, ликвидность, комиссии и налоги. Проверяйте устойчивость портфеля в стресс-условиях.</p>
              <p>Без инвестиционных рекомендаций и без продажи инструментов.</p>
              <div className='row hero-actions'>
                <button className='btn' onClick={onStart}><TrendingUp size={15} />Начать проверку сценария</button>
                <button className='btn ghost' onClick={onExplain}><Scale size={15} />Сравнить мои варианты</button>
                <button className='btn ghost' onClick={onOfferCheck}><Scale size={15} />Проверить предложение из банка/брокера/Telegram</button>
              </div>
              <div className='mini-tags'>
                <span><Lock size={14} />Данные остаются только у вас</span>
                <span><Shield size={14} />Методология без конфликта интересов</span>
                <span><FileText size={14} />Прозрачные расчёты и допущения</span>
              </div>
            </article>

            <aside className='hero-right card-elevated'>
              <div className='row header-row'><b>Сравнение сценариев</b><div className='row'><span className='pill'>1 год</span><span className='pill active'>5 лет</span><span className='pill'>10 лет</span></div></div>
              <div className='graph-box'>
                <div className='legend'><span className='dot a' />Сценарий A <span className='dot b' />Сценарий B <span className='dot c' />Сценарий C</div>
                <div className='graph-lines'><div className='line la' /><div className='line lb' /><div className='line lc' /></div>
              </div>
              <div className='metrics5'>
                {scenarioRows.map(([k, v, d]) => <div className='kpi-card' key={k}><small>{k}</small><strong>{v}</strong><em>{d}</em></div>)}
              </div>
            </aside>
          </div>

          <section id='features' className='feature-grid'>
            <div className='feature-card'><h3><BarChart3 size={15} />Сравнение сценариев</h3><p>Сопоставьте свои варианты по доходности, риску, просадкам, ликвидности, комиссиям и налогам.</p></div>
            <div className='feature-card'><h3><Shield size={15} />Паспорт рисков и флаги рисков</h3><p>Видите ключевые риски по каждой позиции и по портфелю: концентрация, корреляция, валютные риски и другое.</p></div>
            <div className='feature-card'><h3><Activity size={15} />Стресс-тестирование</h3><p>Проверяйте устойчивость портфеля в исторических и гипотетических стресс-сценариях.</p></div>
            <div className='feature-card'><h3><FileText size={15} />Прозрачный отчёт</h3><p>Получайте понятный отчёт с допущениями, расчётами и выводами. Удобно сохранить или поделиться.</p></div>
          </section>

          <section id='how-it-works' className='bottom-grid'>
            <div className='card'><h3>Как это работает</h3><div className='how-steps'><p><b>1</b> Загрузите данные или создайте сценарии</p><p><b>2</b> Мы рассчитаем и проверим</p><p><b>3</b> Получите отчёт и сравните</p></div></div>
            <div className='card'><h3>Что делает сервис</h3><ul><li><Check size={14} />Анализирует ваши сценарии и данные</li><li><Check size={14} />Оценивает риск, ликвидность, комиссии и налоги</li><li><Check size={14} />Проводит стресс-тестирование</li></ul></div>
            <div id='about' className='card'><h3>Что сервис НЕ делает</h3><ul><li><X size={14} />Не даёт индивидуальные инвестрекомендации</li><li><X size={14} />Не говорит, что покупать, продавать или держать</li><li><X size={14} />Не принимает решения за клиента</li></ul></div>
          </section>

          <footer className='mock-footer'>
            <p>Сервис предоставляет информационно-аналитические материалы. Не является индивидуальной инвестиционной рекомендацией.</p>
            <p>Ваши данные защищены и не передаются третьим лицам.</p>
            <p>© 2024 Investment Scenario Lab</p>
          </footer>
        </section>
      </div>
    </LandingShell>
  );
}

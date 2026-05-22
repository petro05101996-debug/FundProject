import React from 'react';
import StressChart from '../components/StressChart';
import Disclaimer from '../components/Disclaimer';
import { LandingShell, KpiCard, RiskChip } from '../components/ui';

const previewStress = [
  { stress_case: 'Ставки +2 п.п.', portfolio_impact_pct: -6 },
  { stress_case: 'Инфляция +3 п.п.', portfolio_impact_pct: -9 },
  { stress_case: 'Шок акций', portfolio_impact_pct: -14 },
];

const previewComparison = [
  { s: 'A', base: '+9.2%', stress: '-14%', liq: '68%' },
  { s: 'B', base: '+11.8%', stress: '-11%', liq: '72%' },
  { s: 'C', base: '+10.4%', stress: '-18%', liq: '63%' },
];

export default function LandingPage({ onStart, onExplain }: { onStart: () => void; onExplain: () => void }) {
  return (
    <LandingShell>
      <div className='landing-header'>
        <b>Investment Scenario Lab</b>
        <nav className='row'>
          <a href='#features'>Возможности</a>
          <a href='#how'>Как работает</a>
          <a href='#limits'>Ограничения</a>
        </nav>
        <button className='btn' onClick={onStart}>Начать анализ</button>
      </div>

      <section className='landing-hero card'>
        <div className='hero-copy'>
          <p className='eyebrow'>Сценарный анализ до покупки</p>
          <h1 className='hero-title'>Проверьте инвестиционный сценарий до покупки</h1>
          <p>Сервис показывает последствия по пользовательскому вводу: риски, ликвидность, комиссии, налоги, стресс-просадку и денежные потоки. Без индивидуальных инвестиционных рекомендаций.</p>
          <div className='row'>
            <button className='btn' onClick={onStart}>Начать анализ</button>
            <button className='btn ghost' onClick={onExplain}>Объяснить инструмент</button>
          </div>
          <div className='row'>
            <RiskChip>Без брокерской интеграции</RiskChip>
            <RiskChip>Только пользовательский ввод</RiskChip>
            <RiskChip>Stress-test</RiskChip>
            <RiskChip>Risk flags</RiskChip>
          </div>
        </div>

        <div className='hero-dashboard card-elevated'>
          <div className='row' style={{ justifyContent: 'space-between' }}>
            <b>Dashboard preview</b>
            <div className='row'>
              <span className='pill'>1 год</span>
              <span className='pill active'>5 лет</span>
              <span className='pill'>10 лет</span>
            </div>
          </div>
          <div className='hero-kpi-grid'>
            <KpiCard label='Базовый результат' value='+11.8%' />
            <KpiCard label='Стресс-просадка' value='-17%' />
            <KpiCard label='Ликвидность' value='72%' />
            <KpiCard label='Риск-флаги' value='3' />
          </div>
          <StressChart rows={previewStress} />
          <div className='row'>
            <span className='pill'>Сценарий A</span>
            <span className='pill active'>Сценарий B</span>
            <span className='pill'>Сценарий C</span>
          </div>

          <div className='preview-table'>
            <table className='table'>
              <thead><tr><th>Сценарий</th><th>База</th><th>Стресс</th><th>Ликв.</th></tr></thead>
              <tbody>{previewComparison.map((r) => <tr key={r.s}><td>{r.s}</td><td>{r.base}</td><td>{r.stress}</td><td>{r.liq}</td></tr>)}</tbody>
            </table>
          </div>

          <div className='card soft'>
            <p>По введённым параметрам сценарий B лучше соответствует ограничениям по ликвидности и просадке.</p>
            <div className='row'>
              <RiskChip severity='high'>Высокая концентрация</RiskChip>
              <RiskChip>Комиссионная нагрузка</RiskChip>
              <RiskChip>Налоговая чувствительность</RiskChip>
            </div>
          </div>
        </div>
      </section>

      <section id='features' className='feature-strip'>
        {[
          { t: 'Сравнение сценариев', d: 'Сопоставление ваших A/B/C вариантов по доходности, риску и ликвидности.' },
          { t: 'Риск-паспорт', d: 'Единый блок риск-флагов, концентрации и ключевых ограничений.' },
          { t: 'Стресс-тестирование', d: 'Проверка устойчивости в неблагоприятных рыночных сценариях.' },
          { t: 'Прозрачный отчёт', d: 'Документ с параметрами, методикой, стрессами и ограничениями.' },
        ].map((x) => <div key={x.t} className='feature-card'><h3>{x.t}</h3><p className='muted'>{x.d}</p></div>)}
      </section>

      <section id='how' className='card'>
        <h3>Как это работает</h3>
        <div className='how-steps'>{['Введите параметры', 'Добавьте сценарии/портфель', 'Получите расчёт', 'Проверьте риск-флаги'].map((x, i) => <div key={x} className='feature-card'><b>{i + 1}</b><p>{x}</p></div>)}</div>
      </section>

      <section id='limits' className='compliance-grid'>
        <div className='card'><h3>Что сервис делает</h3><ul><li>Считает последствия по введённым параметрам.</li><li>Показывает стресс, ликвидность и риск-флаги.</li></ul></div>
        <div className='card'><h3>Что сервис не делает</h3><ul><li>Не подключается к брокеру.</li><li>Не даёт индивидуальных инвестиционных рекомендаций.</li></ul></div>
      </section>

      <div className='card soft'>
        <div className='grid3'>
          <p className='muted'>Сервис предоставляет информационно-аналитические материалы и не является индивидуальной инвестиционной рекомендацией.</p>
          <p className='muted'>Вы принимаете решение самостоятельно и несёте ответственность за результаты.</p>
          <p className='muted'>Ваши данные защищены и не передаются третьим лицам.</p>
        </div>
      </div>
      <Disclaimer />
    </LandingShell>
  );
}

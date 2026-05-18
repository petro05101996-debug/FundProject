import React from 'react';
import Disclaimer from '../components/Disclaimer';
import MetricCard from '../components/MetricCard';
import StressChart from '../components/StressChart';

const previewStress = [
  { scenario: 'A', portfolio_impact_pct: -8 },
  { scenario: 'B', portfolio_impact_pct: -14 },
  { scenario: 'C', portfolio_impact_pct: -21 },
];

export default function LandingPage({ onStart, onExplain }: { onStart: () => void; onExplain: () => void }) {
  return <section>
    <div className='grid2'>
      <div className='card'>
        <h1 className='hero-title'>Проверьте инвестиционный сценарий до покупки</h1>
        <p className='muted'>Сервис показывает риски, ликвидность, комиссии, налоги, стресс-просадку и денежные потоки — без инвестиционных рекомендаций.</p>
        <div className='row'>
          <button className='btn' onClick={onStart}>Начать анализ</button>
          <button className='btn ghost' onClick={onExplain}>Объяснить инструмент</button>
        </div>
        <div className='row'>
          <span className='pill active'>Риск-флаги видны сразу</span>
          <span className='pill'>Ликвидность 30д</span>
          <span className='pill'>Stress-test</span>
        </div>
      </div>
      <div className='card'>
        <h3>Preview dashboard</h3>
        <div className='kpi-grid'>
          <MetricCard label='Базовый результат' value='10.8M' />
          <MetricCard label='Стресс-просадка' value='-14.2%' />
          <MetricCard label='Ликвидность' value='Высокая' />
          <MetricCard label='Риск-флаги' value='2' />
        </div>
        <StressChart rows={previewStress} />
        <div className='row'><span className='pill active'>Сценарий A</span><span className='pill'>Сценарий B</span><span className='pill'>Сценарий C</span></div>
      </div>
    </div>

    <div className='grid2'>
      <div className='card soft'>
        <h4>Возможности</h4>
        <ul>
          <li>Сравнение сценариев с ограничениями пользователя.</li>
          <li>Риск-паспорт и концентрация портфеля.</li>
          <li>Стресс-тесты и what-if анализ.</li>
          <li>Прозрачный HTML-отчёт.</li>
        </ul>
      </div>
      <div className='card soft'>
        <h4>Как это работает</h4>
        <ol>
          <li>Введите сценарии или позиции портфеля.</li>
          <li>Укажите ограничения и допущения.</li>
          <li>Получите расчёт по существующему ядру.</li>
          <li>Проверьте риск-флаги и ограничения.</li>
        </ol>
      </div>
    </div>

    <div className='card soft'>
      <h4>Что сервис делает / не делает</h4>
      <div className='grid2'>
        <ul>
          <li>Считает последствия по пользовательскому вводу.</li>
          <li>Сравнивает варианты по ограничениям.</li>
          <li>Показывает риск-флаги и слабые места.</li>
          <li>Формирует аналитический отчёт.</li>
        </ul>
        <ul>
          <li>Не советует купить / продать / держать.</li>
          <li>Не подключается к брокеру.</li>
          <li>Не исполняет сделки.</li>
          <li>Не гарантирует доходность.</li>
        </ul>
      </div>
      <Disclaimer />
    </div>
  </section>;
}

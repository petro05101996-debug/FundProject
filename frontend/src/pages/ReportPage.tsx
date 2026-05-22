import React, { useState } from 'react';
import { api, ApiError } from '../api/client';
import { EmptyState, ReportPaper } from '../components/ui';

export default function ReportPage({ result, onNavigate }: { result: any; onNavigate: (k: any) => void }) {
  const [html, setHtml] = useState('');
  const [error, setError] = useState('');
  const toc = ['1. Резюме', '2. Введённые параметры', '3. Сравнение сценариев', '4. Риск-флаги', '5. Стресс-тесты', '6. Денежные потоки', '7. Ликвидность', '8. Комиссии и налоги', '9. Допущения', '10. Ограничения'];

  const build = async () => {
    setError('');
    try {
      const r = await api('/api/report/build', { method: 'POST', body: JSON.stringify({ result }) });
      setHtml(r.html || '');
    } catch (e: any) {
      setError(e instanceof ApiError ? e.message : 'Ошибка отчёта');
    }
  };

  const download = () => {
    const a = document.createElement('a');
    a.href = URL.createObjectURL(new Blob([html], { type: 'text/html' }));
    a.download = 'report.html';
    a.click();
  };
  const copy = () => navigator.clipboard.writeText('Краткое резюме отчёта скопировано.');

  if (!result) return <EmptyState title='Нет данных для отчёта' description='Сначала сформируйте итоги анализа.' actions={<button className='btn' onClick={() => onNavigate('results')}>К итогам</button>} />;

  return (
    <div className='report-shell'>
      <div className='report-toolbar row'>
        <span className='pill'>Отчёт формируется по последним рассчитанным данным</span>
        <button className='btn' onClick={build}>Сформировать отчёт</button>
        <button className='btn ghost' onClick={download} disabled={!html}>Скачать HTML</button>
        <button className='btn ghost' onClick={copy}>Скопировать summary</button>
        <button className='btn ghost' onClick={() => onNavigate('results')}>Вернуться к итогам</button>
      </div>
      <div className='report-layout'>
        <aside className='report-toc'>
          <h3>Содержание</h3>
          <ul>{toc.map((t) => <li key={t}><a href='#' onClick={(e) => e.preventDefault()}>{t}</a></li>)}</ul>
        </aside>
        <div>
          {html ? <ReportPaper html={html} /> : <div className='card'><h3>Report canvas</h3><p className='muted'>Нажмите «Сформировать отчёт».</p></div>}
          {error && <div className='error-banner'>{error}</div>}
        </div>
      </div>
    </div>
  );
}

import React, { useState } from 'react';
import { Download, FileText, Share2 } from 'lucide-react';
import { api, ApiError } from '../api/client';
import { EmptyState, ReportPaper } from '../components/ui';

export default function ReportPage({ result, onNavigate }: { result: any; onNavigate: (k: any) => void }) {
  const [html, setHtml] = useState('');
  const [error, setError] = useState('');
  const toc = ['1. Дисклеймер', '2. Параметры пользователя', '3. Выбранные сценарии', '4. Сравнение сценариев', '5. Риск-флаги', '6. Стресс-сценарии', '7. Денежные потоки', '8. Расчётные допущения', '9. Ограничения анализа', '10. Чек-лист'];

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

  if (!result) return <EmptyState title='Нет данных для отчёта' description='Сначала сформируйте итоги анализа.' actions={<button className='btn' onClick={() => onNavigate('results')}>К итогам</button>} />;

  return (
    <div className='report-shell report-dark'>
      <div className='report-toolbar row'>
        <span className='pill'>Сформировано: 15 мая 2024, 12:45</span>
        <span className='pill'>ID отчёта: RPT-2024-05-15-1245</span>
        <button className='btn ghost' onClick={download} disabled={!html}><Download size={14} />Скачать PDF</button>
        <button className='btn ghost' onClick={download} disabled={!html}><FileText size={14} />Экспорт HTML</button>
        <button className='btn ghost'><Share2 size={14} />Поделиться</button>
        <button className='btn' onClick={build}>Сформировать отчёт</button>
      </div>

      <div className='report-layout'>
        <aside className='report-toc'>
          <h3>Содержание отчёта</h3>
          <ul>{toc.map((t, i) => <li key={t}><a href='#' onClick={(e) => e.preventDefault()}><span>{i + 1}</span>{t.replace(/^\d+\.\s*/, '')}</a></li>)}</ul>
          <div className='card soft'>
            <p className='muted'>Отчёт сформирован автоматически на основе введённых данных.</p>
          </div>
        </aside>

        <div>
          {html ? <ReportPaper html={html} /> : (
            <article className='report-paper'>
              <h1>Аналитический отчёт по пользовательскому сценарию</h1>
              <p>Нажмите «Сформировать отчёт», чтобы построить полный документ с таблицами и графиками.</p>
            </article>
          )}
          {error && <div className='error-banner'>{error}</div>}
        </div>
      </div>
    </div>
  );
}

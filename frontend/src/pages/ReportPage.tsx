import React, { useEffect, useState } from 'react';
import { FileText, Share2 } from 'lucide-react';
import { api, ApiError } from '../api/client';
import { EmptyState, ReportPaper } from '../components/ui';

export default function ReportPage({ result, onNavigate }: { result: any; onNavigate: (k: any) => void }) {
  const [html, setHtml] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [reportMeta, setReportMeta] = useState<{ report_id?: string; created_at?: string }>({});
  const toc = ['1. Дисклеймер', '2. Параметры пользователя', '3. Выбранные сценарии', '4. Сравнение сценариев', '5. Риск-флаги', '6. Стресс-сценарии', '7. Денежные потоки', '8. Расчётные допущения', '9. Ограничения анализа', '10. Чек-лист'];

  const build = async () => {
    if (loading) return;
    setLoading(true);
    setError('');
    try {
      const r = await api('/api/report/build', { method: 'POST', body: JSON.stringify({ result }) });
      setHtml(r.html || '');
      setReportMeta({ report_id: r.report_id, created_at: r.created_at });
    } catch (e: any) {
      setError(e instanceof ApiError ? e.message : 'Ошибка отчёта');
    } finally {
      setLoading(false);
    }
  };
  useEffect(() => {
    if (result && !html && !error) {
      void build();
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [result]);

  const download = () => {
    const a = document.createElement('a');
    a.href = URL.createObjectURL(new Blob([html], { type: 'text/html' }));
    a.download = 'report.html';
    a.click();
  };

  if (!result) return <EmptyState title='Нет данных для отчёта' description='Сначала выполните сценарный анализ. После расчёта здесь появится аналитический отчёт.' actions={<button className='btn' onClick={() => onNavigate('results')}>К итогам</button>} />;

  return (
    <div className='report-shell report-dark'>
      <div className='report-toolbar row'>
        <span className='pill'>Сформировано: {reportMeta.created_at || 'нет данных'}</span>
        <span className='pill'>ID отчёта: {reportMeta.report_id || 'нет данных'}</span>
        <button className='btn ghost' onClick={download} disabled={!html}><FileText size={14} />Экспорт HTML</button>
        <button className='btn ghost' disabled title='Будет доступно позже'><Share2 size={14} />Поделиться</button>
        <button className='btn' onClick={build} disabled={loading}>{loading ? 'Формируем...' : 'Сформировать отчёт'}</button>
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
          {loading && <div className='info-banner'>Формируем отчёт...</div>}
          {html ? <ReportPaper html={html} /> : (
            <article className='report-paper'>
              <h1>Аналитический отчёт по пользовательскому сценарию</h1>
              <p>Отчёт формируется автоматически. Если данные не появились, нажмите «Сформировать отчёт» повторно.</p>
            </article>
          )}
          {error && <div className='error-banner'>Не удалось сформировать отчёт. Проверьте, что сценарий рассчитан корректно, и повторите попытку. <small>{error}</small></div>}
        </div>
      </div>
    </div>
  );
}

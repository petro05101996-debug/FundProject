import React, { useEffect, useState } from 'react';
import { api, ApiError } from '../api/client';
import { PageShell, EmptyState, RiskChip, InsightPanel } from '../components/ui';

export default function ExplainInstrumentPage() {
  const [q, setQ] = useState('');
  const [active, setActive] = useState('');
  const [data, setData] = useState<any>(null);
  const [catalog, setCatalog] = useState<string[]>([]);
  const [error, setError] = useState('');

  useEffect(() => {
    (async () => {
      try {
        const r = await api<{ items?: Array<{ name: string }> }>('/api/instruments/catalog');
        setCatalog((r.items || []).map((x) => x.name));
      } catch {
        // keep empty catalog fallback
      }
    })();
  }, []);

  const load = async (term: string) => {
    const query = term.trim();
    if (!query) return;
    setError('');
    setActive(query);
    try {
      setData(await api('/api/instruments/explain?query=' + encodeURIComponent(query)));
    } catch (e: any) {
      setError(e instanceof ApiError ? e.message : 'Ошибка загрузки');
    }
  };

  return (
    <PageShell title='Объяснить инструмент' subtitle='Разберите инструмент простыми словами: доход, риски, ликвидность, комиссии, налоги и что проверить самостоятельно.'>
      <div className='card'>
        <div className='row'>
          <input value={q} onChange={(e) => setQ(e.target.value)} placeholder='Введите инструмент' />
          <button className='btn' onClick={() => load(q)} disabled={!q.trim()}>Найти</button>
        </div>
        <div className='segmented-tabs' style={{ marginTop: '10px' }}>
          {catalog.map((c) => <button key={c} className={`seg-btn ${active === c ? 'active' : ''}`} onClick={() => load(c)}>{c}</button>)}
        </div>
      </div>

      {!data ? (
        <EmptyState title='Введите инструмент или выберите из каталога' description='После загрузки появится разбор по рискам, ликвидности и ограничениям.' />
      ) : (
        <div className='main-grid'>
          <div className='card'>
            <h3>{data.title}</h3>
            <h4>Простыми словами</h4><p>{data.plain_explanation}</p>
            <h4>Как формируется доход</h4><p>{data.how_income_works}</p>
            <h4>Основные риски</h4><ul>{(data.risks || []).map((r: string, i: number) => <li key={i}>{r}</li>)}</ul>
            <h4>Ликвидность</h4><p>{data.liquidity}</p>
            <h4>Комиссии и налоги</h4><p>{data.tax_notes}</p>
            <h4>Что проверить самостоятельно</h4><ul>{(data.what_to_check || []).map((x: string, i: number) => <li key={i}>{x}</li>)}</ul>
            <h4>Похожие инструменты</h4>
            <div>
              {(data.related_instruments || []).map((x: string) => (
                <div key={x} className='card soft related-row'>{x}</div>
              ))}
            </div>
          </div>
          <div>
            <InsightPanel title='Краткий профиль' items={[`Категория: ${data.category || '—'}`, `Риск: ${data.risk_level || '—'}`, `Ликвидность: ${data.liquidity || '—'}`, `Сложность: ${data.complexity || '—'}`]} />
            <div className='card' style={{ marginTop: '12px' }}>
              <h4>Коротко</h4>
              <div className='row'>
                <RiskChip>Уровень риска: {data.risk_level || '—'}</RiskChip>
                <RiskChip>Ликвидность: {data.liquidity || '—'}</RiskChip>
                <RiskChip>Сложность: {data.complexity || '—'}</RiskChip>
              </div>
              <p className='muted'>Этот раздел носит информационно-образовательный характер и не является индивидуальной инвестиционной рекомендацией.</p>
            </div>
          </div>
        </div>
      )}
      {error && <div className='error-banner'>{error}</div>}
    </PageShell>
  );
}

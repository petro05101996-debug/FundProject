import React, { useEffect, useState } from 'react';
import { BookOpen, CircleCheckBig, Clock3, Search, ShieldAlert, Sparkles } from 'lucide-react';
import { api, ApiError } from '../api/client';
import { EmptyState, PageShell } from '../components/ui';

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
        setCatalog(['Вклад', 'ОФЗ', 'Корпоративная облигация', 'Фонды']);
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
    <PageShell title='Объяснить инструмент' subtitle='Понятное объяснение инструмента, рисков и ключевых параметров.'>
      <div className='card' style={{ marginBottom: 12 }}>
        <div className='row'>
          <input value={q} onChange={(e) => setQ(e.target.value)} placeholder='Поиск инструмента: например, ОФЗ, фонд, облигация' />
          <button className='btn' onClick={() => load(q)} disabled={!q.trim()}><Search size={14} />Найти</button>
        </div>
        <div className='segmented-tabs' style={{ marginTop: 10 }}>
          {catalog.map((c) => <button key={c} className={`seg-btn ${active === c ? 'active' : ''}`} onClick={() => load(c)}>{c}</button>)}
        </div>
      </div>

      {!data ? (
        <EmptyState title='Введите инструмент или выберите из каталога' description='После загрузки появится разбор по рискам, ликвидности и ограничениям.' />
      ) : (
        <section className='scenario-main-grid'>
          <article className='card'>
            <h3>{data.title || active}</h3>
            <p className='muted'>{data.plain_explanation}</p>

            <div className='card soft'>
              <h4><Sparkles size={14} />Как формируется результат</h4>
              <p>{data.how_income_works}</p>
            </div>

            <div className='card soft'>
              <h4><ShieldAlert size={14} />Основные риски</h4>
              <ul>{(data.risks || []).map((r: string, i: number) => <li key={i}>{r}</li>)}</ul>
            </div>

            <div className='card soft'>
              <h4><Clock3 size={14} />Ликвидность</h4>
              <p>{data.liquidity}</p>
            </div>

            <div className='card soft'>
              <h4><BookOpen size={14} />Сравнение с похожими инструментами</h4>
              <ul>{(data.related_instruments || []).map((x: string, i: number) => <li key={i}>{x}</li>)}</ul>
            </div>
          </article>

          <aside className='card'>
            <h3>Коротко</h3>
            <ul className='rules-list'>
              <li><CircleCheckBig size={15} />Уровень риска: {data.risk_level || 'Низкий'}</li>
              <li><CircleCheckBig size={15} />Ликвидность: {data.liquidity || 'Высокая'}</li>
              <li><CircleCheckBig size={15} />Сложность: {data.complexity || 'Низкая'}</li>
              <li><CircleCheckBig size={15} />Горизонт: {data.horizon || 'Короткий (до 1 года)'}</li>
            </ul>
            <div className='card soft'>
              <p className='muted'>Этот раздел носит информационно-образовательный характер и не является индивидуальной инвестиционной рекомендацией.</p>
            </div>
          </aside>
        </section>
      )}
      {error && <div className='error-banner'>{error}</div>}
    </PageShell>
  );
}

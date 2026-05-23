import React, { useMemo, useState } from 'react';
import { AlertTriangle, BarChart3, CalendarDays, CirclePercent, Coins, Landmark, Shield, TrendingUp } from 'lucide-react';
import { api, ApiError } from '../api/client';
import { PageShell, SegmentedTabs } from '../components/ui';

const tabs = ['Вклад', 'Накопительный счёт', 'ОФЗ', 'Корпоративная облигация', 'Фонд денежного рынка', 'Индексный фонд'];
const defaults: any = {
  'Вклад': { amount: 1000000, annual_rate_pct: 12, term_months: 12, tax_pct: 13 },
  'Накопительный счёт': { amount: 1000000, annual_rate_pct: 10, term_months: 12, tax_pct: 13 },
  'ОФЗ': { amount: 1000000, clean_price_pct: 98.5, nominal: 1000, coupon_pct: 10, years_to_maturity: 2.8, nkd: 41.27, commission_pct: 0.1, tax_pct: 13, liquidity_days: 3, issuer_rating: 'A (низкий риск)', coupon_period: 'Полугодовая' },
  'Корпоративная облигация': { amount: 1000000, coupon_pct: 12, years_to_maturity: 3, clean_price_pct: 95, commission_pct: 0.3, default_risk_pct: 2, tax_pct: 13 },
  'Фонд денежного рынка': { amount: 1000000, expected_return_pct: 10, management_fee_pct: 0.5, term_months: 12, tax_pct: 13 },
  'Индексный фонд': { amount: 1000000, expected_return_pct: 16, management_fee_pct: 1.2, term_months: 36, tax_pct: 13, stress_drawdown_pct: -20 }
};

const fieldOrder = ['amount', 'nkd', 'clean_price_pct', 'issuer_rating', 'nominal', 'liquidity_days', 'coupon_pct', 'commission_pct', 'years_to_maturity', 'coupon_period', 'tax_pct'];
const labels: Record<string, string> = {
  amount: 'Сумма инвестиций', nkd: 'НКД (накопленный купонный доход)', clean_price_pct: 'Цена', issuer_rating: 'Кредитный риск (рейтинг эмитента)', nominal: 'Номинал', liquidity_days: 'Ликвидность (средний срок выхода)', coupon_pct: 'Купон (годовой)', commission_pct: 'Комиссия', years_to_maturity: 'Срок до погашения', coupon_period: 'Периодичность купона', tax_pct: 'Ставка налога'
};
const suffixes: Record<string, string> = { amount: '₽', nkd: '₽', clean_price_pct: '% от номинала', nominal: '₽', liquidity_days: 'дней', coupon_pct: '%', commission_pct: '%', years_to_maturity: 'лет', tax_pct: '%' };

export default function InstrumentCheckPage() {
  const [tab, setTab] = useState('ОФЗ');
  const [params, setParams] = useState<any>(defaults['ОФЗ']);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState('');

  const rows = useMemo(() => fieldOrder.filter((k) => params[k] !== undefined), [params]);

  const onTab = (t: string) => {
    setTab(t);
    setResult(null);
    setParams(defaults[t]);
  };

  const onCalc = async () => {
    setError('');
    try {
      setResult(await api('/api/instrument/check', { method: 'POST', body: JSON.stringify({ selectedInstrumentType: tab, params }) }));
    } catch (e: any) {
      setError(e instanceof ApiError ? e.message : 'Ошибка расчёта');
    }
  };

  const metric = {
    value: result?.expected_value ?? '1 230 450 ₽',
    irr: result?.irr ?? '10,21%',
    stress: result?.stress_drawdown ?? '-7,9%',
    liq: result?.liquidity_label ?? '3 дня',
    risk: result?.risk_label ?? 'Низкий',
    complexity: result?.complexity_label ?? 'Низкая',
  };

  return (
    <PageShell title='Проверить инструмент' subtitle='Смоделируйте один финансовый инструмент и оцените его параметры и риски.'>
      <SegmentedTabs items={tabs} active={tab} onChange={onTab} />
      <section className='inst-grid full-pass'>
        <article className='card'>
          <h3>Параметры инструмента ({tab})</h3>
          <div className='inst-form-grid'>
            {rows.map((k) => (
              <label className='form-field inst-field' key={k}>
                <span>{labels[k] || k}</span>
                <div className='input-wrap'>
                  <input value={String(params[k])} onChange={(e) => setParams({ ...params, [k]: isNaN(Number(e.target.value)) ? e.target.value : Number(e.target.value) })} />
                  {suffixes[k] && <em>{suffixes[k]}</em>}
                </div>
              </label>
            ))}
          </div>
          <div className='row'>
            <button className='btn' onClick={onCalc}><BarChart3 size={14} />Рассчитать инструмент</button>
            <button className='btn ghost'>Использовать в сценарии</button>
          </div>
        </article>

        <aside className='card'>
          <h3>Предварительная оценка</h3>
          <ul className='rules-list metrics-list'>
            <li><TrendingUp size={15} />Ожидаемая стоимость: <b>{metric.value}</b></li>
            <li><CirclePercent size={15} />Ориентир дохода (IRR): <b>{metric.irr}</b></li>
            <li><AlertTriangle size={15} />Стресс-просадка: <b>{metric.stress}</b></li>
            <li><CalendarDays size={15} />Ликвидность: <b>{metric.liq}</b></li>
            <li><Shield size={15} />Риск: <b>{metric.risk}</b></li>
            <li><Coins size={15} />Сложность: <b>{metric.complexity}</b></li>
          </ul>
          <div className='card soft'>
            <h4>Ключевые риск-флаги</h4>
            <div className='row'>
              <span className='risk-chip high'>Процентный риск</span>
              <span className='risk-chip'>Продажа до погашения</span>
              <span className='risk-chip'>Кредитный риск эмитента</span>
              <span className='risk-chip'>Реинвестирование купонов</span>
            </div>
          </div>
          <p className='muted disclaimer-line'><Landmark size={14} /> Результаты расчётов являются приблизительными и основаны на введённых данных.</p>
        </aside>
      </section>
      {error && <div className='error-banner'>{error}</div>}
    </PageShell>
  );
}

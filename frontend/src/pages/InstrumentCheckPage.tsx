import React, { useMemo, useState } from 'react';
import { api, ApiError } from '../api/client';
import Disclaimer from '../components/Disclaimer';
import { PageShell, SegmentedTabs, FormField, InsightPanel, KpiCard, RiskChip, ActionBar } from '../components/ui';

const tabs = ['Вклад', 'Накопительный счёт', 'ОФЗ', 'Корпоративная облигация', 'Фонд денежного рынка', 'Облигационный фонд', 'Индексный фонд', 'Акция как класс риска'];
const labels: Record<string, string> = {
  amount: 'Сумма', annual_rate_pct: 'Ставка, % годовых', term_months: 'Срок, месяцев', capitalization: 'Капитализация процентов',
  early_withdrawal: 'Досрочное снятие', tax_pct: 'Налог, %', min_balance: 'Минимальный остаток', years_to_maturity: 'Срок до погашения, лет',
  clean_price_pct: 'Цена, % от номинала', coupon_pct: 'Купон, %', commission_pct: 'Комиссия, %', default_risk_pct: 'Кредитный риск, %',
  expected_return_pct: 'Ожидаемая доходность, %', management_fee_pct: 'Комиссия фонда, % в год', stress_drawdown_pct: 'Стресс-просадка, %', withdrawals_allowed: 'Разрешены снятия'
};
const defaults: any = {
  'Вклад': { amount: 1000000, annual_rate_pct: 12, term_months: 12, capitalization: true, early_withdrawal: false, tax_pct: 13 },
  'Накопительный счёт': { amount: 1000000, annual_rate_pct: 10, term_months: 12, min_balance: 500000, withdrawals_allowed: true, tax_pct: 13 },
  'ОФЗ': { amount: 1000000, coupon_pct: 10, years_to_maturity: 3, clean_price_pct: 96, commission_pct: 0.2, tax_pct: 13 },
  'Корпоративная облигация': { amount: 1000000, coupon_pct: 12, years_to_maturity: 3, clean_price_pct: 95, commission_pct: 0.3, default_risk_pct: 2, tax_pct: 13 },
  'Фонд денежного рынка': { amount: 1000000, expected_return_pct: 10, management_fee_pct: 0.5, term_months: 12, tax_pct: 13 },
  'Облигационный фонд': { amount: 1000000, expected_return_pct: 12, management_fee_pct: 1, term_months: 24, tax_pct: 13 },
  'Индексный фонд': { amount: 1000000, expected_return_pct: 16, management_fee_pct: 1.2, term_months: 36, tax_pct: 13, stress_drawdown_pct: -20 },
  'Акция как класс риска': { amount: 1000000, expected_return_pct: 18, management_fee_pct: 0, term_months: 36, tax_pct: 13, stress_drawdown_pct: -35 }
};

const groups: Record<string, string[]> = {
  base: ['amount', 'term_months', 'tax_pct'],
  yield: ['annual_rate_pct', 'coupon_pct', 'expected_return_pct', 'clean_price_pct', 'years_to_maturity'],
  costs: ['commission_pct', 'management_fee_pct', 'default_risk_pct', 'stress_drawdown_pct'],
  options: ['capitalization', 'early_withdrawal', 'withdrawals_allowed', 'min_balance'],
};

export default function InstrumentCheckPage() {
  const [tab, setTab] = useState('ОФЗ');
  const [params, setParams] = useState<any>(defaults['ОФЗ']);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState('');
  const [configError, setConfigError] = useState('');

  const entries = useMemo(() => Object.entries(params || {}), [params]);
  const keys = new Set(entries.map(([k]) => k));

  const onTab = (t: string) => {
    setTab(t);
    setResult(null);
    if (!defaults[t]) {
      setConfigError(`Ошибка конфигурации: нет defaults для ${t}`);
      return;
    }
    setConfigError('');
    setParams(defaults[t]);
  };

  const onCalc = async () => {
    if (configError) return;
    setError('');
    try {
      setResult(await api('/api/instrument/check', { method: 'POST', body: JSON.stringify({ selectedInstrumentType: tab, params }) }));
    } catch (e: any) {
      setError(e instanceof ApiError ? e.message : 'Ошибка расчёта');
    }
  };

  const field = (k: string, v: any) => (
    <FormField key={k} label={labels[k] || k}>
      {typeof v === 'boolean'
        ? <input type='checkbox' checked={v} onChange={(e) => setParams({ ...params, [k]: e.target.checked })} />
        : <input value={String(v)} onChange={(e) => setParams({ ...params, [k]: isNaN(Number(e.target.value)) ? e.target.value : Number(e.target.value) })} />}
    </FormField>
  );

  return (
    <PageShell title='Проверить инструмент' subtitle='Оцените последствия по одному инструменту: доход, стресс-просадку, ликвидность, комиссии, налоги и риск-флаги.'>
      <SegmentedTabs items={tabs} active={tab} onChange={onTab} />
      {configError && <div className='error-banner'>{configError}</div>}
      <div className='main-grid'>
        <div className='card'>
          <h3>Параметры инструмента</h3>
          <div className='form-section'>
            <h4>Базовые параметры</h4>
            <div className='form-grid'>{groups.base.filter((k) => keys.has(k)).map((k) => field(k, params[k]))}</div>
          </div>
          <div className='form-section'>
            <h4>Доходность и горизонт</h4>
            <div className='form-grid'>{groups.yield.filter((k) => keys.has(k)).map((k) => field(k, params[k]))}</div>
          </div>
          <div className='form-section'>
            <h4>Комиссии и риски</h4>
            <div className='form-grid'>{groups.costs.filter((k) => keys.has(k)).map((k) => field(k, params[k]))}</div>
          </div>
          <div className='form-section'>
            <h4>Дополнительные условия</h4>
            <div className='form-grid'>{groups.options.filter((k) => keys.has(k)).map((k) => field(k, params[k]))}</div>
          </div>
        </div>
        <div>
          {!result ? (
            <InsightPanel title='Предварительная оценка' items={[`Выбранный инструмент: ${tab}`, 'Будут учтены комиссии, налоги, ликвидность и стресс-фактор', 'Проверьте ограничения анализа и риск-флаги перед сравнением', 'Сервис не является индивидуальной инвестиционной рекомендацией']} />
          ) : (
            <div className='card'>
              <div className='kpi-strip'>
                {[
                  ['Ожидаемая стоимость', result.expected_value], ['Доход', result.income_estimate], ['Стресс', result.stress_drawdown],
                  ['Ликвидность', result.liquidity_label], ['Риск', result.risk_label], ['Сложность', result.complexity_label],
                ].map(([l, v]) => <KpiCard key={String(l)} label={String(l)} value={typeof v === 'number' ? v.toFixed(2) : String(v || '—')} />)}
              </div>
              <h4>Ключевые риск-флаги</h4>
              <div className='row'>{(result.risk_flags || []).map((f: string, i: number) => <RiskChip key={i} severity={/высок|риск|просад/i.test(f) ? 'high' : 'neutral'}>{f}</RiskChip>)}</div>
              <div className='card soft'>
                <h4>Что проверить самостоятельно</h4>
                <ul>{(result.checklist || []).map((x: string, i: number) => <li key={i}>{x}</li>)}</ul>
              </div>
              <p className='muted'>{(result.limitations || []).join(' ')}</p>
              <Disclaimer />
            </div>
          )}
        </div>
      </div>
      <ActionBar hint='Проверка проводится только по введённым параметрам.'>
        <button className='btn' onClick={onCalc}>Рассчитать последствия</button>
        {error && <span className='error-banner'>{error}</span>}
      </ActionBar>
    </PageShell>
  );
}

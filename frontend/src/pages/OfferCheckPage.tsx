import React, { useState } from 'react';
import { api } from '../api/client';

export default function OfferCheckPage(){
  const [offerText,setOfferText]=useState('');
  const [source,setSource]=useState('telegram');
  const [instrumentType,setInstrumentType]=useState('unknown');
  const [result,setResult]=useState<any>(null);
  const parse = async()=>{ const r = await api('/api/offer-check/parse-text',{method:'POST',body:JSON.stringify({offer_text:offerText})}); setResult((x:any)=>({...x, parsed:r})); setInstrumentType((r as any).detected_instrument_type || 'unknown'); };
  const analyze = async()=>{ const r = await api('/api/offer-check/analyze',{method:'POST',body:JSON.stringify({offer_source:source,offer_text:offerText,instrument_type:instrumentType,fees_known:false,early_exit_type:'unknown',experience_level:'beginner'})}); setResult((x:any)=>({...x, analyzed:r})); };
  return <div><h1>Проверить предложение</h1><p>Разберите предложение из банка, брокера, рекламы, Telegram или от знакомого: что обещают, что неизвестно, где риски и что нужно уточнить.</p>
    <label>Откуда предложение?</label><select value={source} onChange={e=>setSource(e.target.value)}><option>bank</option><option>broker</option><option>telegram</option><option>blogger</option><option>ad</option><option>friend</option><option>unknown</option></select>
    <label>Что вам предложили?</label><select value={instrumentType} onChange={e=>setInstrumentType(e.target.value)}><option>deposit</option><option>savings</option><option>bond</option><option>fund</option><option>structured_product</option><option>portfolio</option><option>unknown</option></select>
    <label>Вставьте текст предложения</label><textarea value={offerText} onChange={e=>setOfferText(e.target.value)} rows={6} />
    <div><button onClick={parse}>Разобрать текст</button><button onClick={analyze}>Проверить предложение</button></div>
    {result?.parsed && <div><h3>Что удалось извлечь</h3><pre>{JSON.stringify(result.parsed,null,2)}</pre></div>}
    {result?.analyzed && <div><h2>Разбор предложения</h2><p>{result.analyzed.plain_summary}</p><h3>На что обратить внимание</h3><pre>{JSON.stringify(result.analyzed.red_flags,null,2)}</pre><h3>Что нужно уточнить</h3><pre>{JSON.stringify(result.analyzed.questions_to_ask,null,2)}</pre><h3>Базовый сценарий</h3><pre>{JSON.stringify(result.analyzed.base_scenario,null,2)}</pre><h3>Плохой сценарий</h3><pre>{JSON.stringify(result.analyzed.stress_scenario,null,2)}</pre></div>}
  </div>
}

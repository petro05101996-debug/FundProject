import React, { useEffect, useState } from 'react';
import { getScenarioTemplates } from '../api/client';

export default function ScenarioStartPage({ onSelect }: { onSelect: (id: string)=>void }) {
  const [items,setItems]=useState<any[]>([]);
  useEffect(()=>{getScenarioTemplates().then(setItems).catch(()=>setItems([]));},[]);
  return <div><h1>Что вы хотите понять?</h1><p>Выберите жизненную ситуацию — дальше сервис задаст несколько простых вопросов и покажет результат без сложных терминов.</p>
    <div><div><h3>Проверить предложение</h3><p>Разберите предложение из банка, брокера, рекламы или Telegram.</p><button onClick={()=>onSelect('offer_check')}>Начать проверку</button></div>{items.map((t)=><div key={t.id}><h3>{t.title}</h3><p>{t.short_description}</p><button onClick={()=>onSelect(t.id)}>Начать</button></div>)}</div>
  </div>
}

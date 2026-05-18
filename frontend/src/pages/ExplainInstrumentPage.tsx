import React,{useState} from 'react';
import {api, ApiError} from '../api/client';

const categories=['Денежные инструменты','Облигации','Фонды','Акции'];

export default function ExplainInstrumentPage(){
  const [q,setQ]=useState('ОФЗ');
  const [data,setData]=useState<any>(null);
  const [loading,setLoading]=useState(false);
  const [error,setError]=useState('');
  const load=async(term:string)=>{setLoading(true);setError('');try{setData(await api('/api/instruments/explain?query='+encodeURIComponent(term)));}catch(e:any){setError(e instanceof ApiError?e.message:'Ошибка загрузки');}finally{setLoading(false)}};
  return <div className='grid2'><div className='card'><h2>Объяснить инструмент</h2><div className='row'><input value={q} onChange={e=>setQ(e.target.value)} placeholder='Введите инструмент'/><button className='btn' onClick={()=>load(q)} disabled={loading}>{loading?'Загрузка...':'Найти'}</button></div><div className='row'>{categories.map(c=><button key={c} className='btn ghost' onClick={()=>load(c)}>{c}</button>)}</div><p className='muted'>Образовательный раздел: сервис не даёт индивидуальных инвестиционных рекомендаций.</p>{error&&<div className='risk-flag'>{error}</div>}</div>
  <div className='card'>{data?<><h3>{data.title}</h3><p className='muted'>{data.category}</p><h4>Простыми словами</h4><p>{data.plain_explanation}</p><h4>Как формируется доход</h4><p>{data.how_income_works}</p><h4>Основные риски</h4><ul>{(data.risks||[]).map((r:string,i:number)=><li key={i}>{r}</li>)}</ul><h4>Ликвидность</h4><p>{data.liquidity}</p><h4>Комиссии и налоги</h4><p>{data.tax_notes}</p><h4>Что проверить самостоятельно</h4><ul>{(data.what_to_check||[]).map((x:string,i:number)=><li key={i}>{x}</li>)}</ul><h4>Похожие инструменты</h4><div className='row'>{(data.related_instruments||[]).map((x:string)=><span key={x} className='pill'>{x}</span>)}</div><p className='muted'>{data.disclaimer}</p></>:<p className='muted'>Введите запрос и нажмите «Найти».</p>}</div></div>
}

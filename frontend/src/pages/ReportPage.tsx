import React,{useState} from 'react';
import {api, ApiError} from '../api/client';

export default function ReportPage({result,onNavigate}:{result:any;onNavigate:(k:any)=>void}){
  const [html,setHtml]=useState(''); const [loading,setLoading]=useState(false); const [error,setError]=useState('');
  const sections=['Дисклеймер','Executive summary','Риск-паспорт','Параметры пользователя','Расчётные допущения','Выбранные сценарии','Сравнение сценариев','Риск-флаги','Стресс-сценарии','Денежные потоки','Ограничения анализа','Чек-лист'];
  const build=async()=>{setLoading(true);setError('');try{const r=await api('/api/report/build',{method:'POST',body:JSON.stringify({result})});setHtml(r.html||'');}catch(e:any){setError(e instanceof ApiError?e.message:'Ошибка отчёта');}finally{setLoading(false)}};
  const copy=()=>navigator.clipboard.writeText('Executive summary copied from generated report.');
  const download=()=>{const blob=new Blob([html],{type:'text/html'});const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='report.html';a.click();};
  if(!result) return <div className='card'><h2>Аналитический отчёт</h2><p className='muted'>Сначала выполните сравнение сценариев.</p><button className='btn' onClick={()=>onNavigate('builder')}>Перейти к сравнению сценариев</button></div>;
  return <div className='grid2'><div className='card'><h2>Содержание</h2><ul>{sections.map(s=><li key={s}>{s}</li>)}</ul><div className='row'><button className='btn' disabled={loading} onClick={build}>{loading?'Собираем...':'Собрать отчёт'}</button><button className='btn ghost' disabled={!html} onClick={download}>Скачать HTML</button><button className='btn ghost' onClick={copy}>Скопировать executive summary</button></div>{error&&<div className='risk-flag'>{error}</div>}</div><div className='card'><h2>Report canvas</h2><div className='report' style={{background:'#f8fafc',color:'#0f172a',borderRadius:24,padding:32}} dangerouslySetInnerHTML={{__html:html}}/></div></div>;
}

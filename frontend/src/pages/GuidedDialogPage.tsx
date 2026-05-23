import React, { useState } from 'react';
import { answerDialog } from '../api/client';
export default function GuidedDialogPage({state,setState,onPreview}:{state:any,setState:(s:any)=>void,onPreview:()=>void}){
  const q=state?.current_question; const [answer,setAnswer]=useState<any>('');
  if(!q) return <div>Нет вопроса</div>;
  const next=async()=>{const r=await answerDialog(state.session_state,q.id,answer||'unknown');setState(r);if(r.preview_ready) onPreview();};
  return <div><div>Прогресс: {state.progress?.current}/{state.progress?.total}</div><h2>{q.title}</h2><p>{q.description}</p>
    {q.options ? q.options.map((o:any)=><button key={o.value} onClick={()=>setAnswer(o.value)}>{o.label}</button>) : <input value={answer} onChange={e=>setAnswer(e.target.value)} />}
    <div><button onClick={()=>setAnswer('unknown')}>Не знаю</button><button onClick={next}>Дальше</button></div>
  </div>
}

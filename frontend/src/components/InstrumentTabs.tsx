import React from 'react';
export default function InstrumentTabs({tabs,active,onSelect}:{tabs:string[];active:string;onSelect:(v:string)=>void}){return <div className='tabs'>{tabs.map(t=><button key={t} className={active===t?'btn':'btn ghost'} onClick={()=>onSelect(t)}>{t}</button>)}</div>}

import React from 'react';
export default function Sidebar({items,active,onSelect}:{items:{key:string;label:string}[];active:string;onSelect:(k:string)=>void}){return <aside className='sidebar'>{items.map(i=><button key={i.key} className={active===i.key?'nav active':'nav'} onClick={()=>onSelect(i.key)}>{i.label}</button>)}</aside>}

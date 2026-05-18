import React from 'react';

type PageKey = 'landing'|'profile'|'instrument'|'builder'|'portfolio'|'results'|'report'|'explain';
const items:{key:PageKey;label:string}[]=[
  {key:'landing',label:'Лендинг'},{key:'profile',label:'Параметры сценария'},{key:'instrument',label:'Проверить инструмент'},
  {key:'builder',label:'Сравнить варианты'},{key:'portfolio',label:'Проверить портфель'},{key:'results',label:'Итог'},{key:'report',label:'Отчёт'},{key:'explain',label:'Объяснить инструмент'}
];
export default function AppShell({children,page,onNavigate}:{children:React.ReactNode;page:PageKey;onNavigate:(k:PageKey)=>void}){
  return <div className='shell'><header className='topbar'><b>Investment Scenario Lab</b><button className='btn' onClick={()=>onNavigate('profile')}>Начать проверку</button></header>
  <div className='layout'><aside className='sidebar'>{items.map(i=><button key={i.key} className={page===i.key?'nav active':'nav'} onClick={()=>onNavigate(i.key)}>{i.label}</button>)}</aside>
  <main className='content'>{children}</main></div><footer className='footer'>Это не является индивидуальной инвестиционной рекомендацией.</footer></div>
}

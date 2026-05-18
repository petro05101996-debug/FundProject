import React from 'react';
export default function TopNav({onStart}:{onStart:()=>void}){return <header className='topbar'><b>Investment Scenario Lab</b><button className='btn' onClick={onStart}>Начать проверку</button></header>}

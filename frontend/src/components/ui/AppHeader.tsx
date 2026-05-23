import React from 'react';
import { Bell, Moon, User } from 'lucide-react';

export default function AppHeader({ onStart }: { onStart: () => void }) {
  return (
    <header className='app-header dark'>
      <div className='brand-line'>
        <b>Investment Scenario Lab</b>
        <span className='muted'>Финансовый сценарный анализатор</span>
      </div>
      <nav className='top-links'>
        <a>Возможности</a><a>Как это работает</a><a>Тарифы</a><a>Примеры</a><a>База знаний</a><a>О проекте</a>
      </nav>
      <div className='row'>
        <button className='icon-btn'><Moon size={14} /></button>
        <button className='icon-btn'><Bell size={14} /></button>
        <button className='pill'><User size={12} />АД</button>
        <button className='btn' onClick={onStart}>Начать проверку</button>
      </div>
    </header>
  );
}

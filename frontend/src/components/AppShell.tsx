import React from 'react';
import { AppHeader, AppSidebar } from './ui';

type PageKey = 'landing' | 'profile' | 'instrument' | 'builder' | 'portfolio' | 'results' | 'report' | 'explain';

const groups = [
  { title: 'АНАЛИЗ', items: [{ key: 'profile', label: 'Параметры сценария' }, { key: 'instrument', label: 'Проверить инструмент' }, { key: 'builder', label: 'Сравнить варианты' }, { key: 'portfolio', label: 'Проверить портфель' }] },
  { title: 'ИТОГИ', items: [{ key: 'results', label: 'Итог по сценариям' }, { key: 'report', label: 'Прозрачный отчёт' }] },
  { title: 'СПРАВКА', items: [{ key: 'explain', label: 'Объяснить инструмент' }] },
];

export default function AppShell({ children, page, onNavigate }: { children: React.ReactNode; page: PageKey; onNavigate: (k: PageKey) => void }) {
  return <div className='app-shell dark-shell'><AppHeader onStart={() => onNavigate('instrument')} /><div className='layout'><AppSidebar groups={groups as any} page={page} onNavigate={onNavigate} /><main className='app-content'>{children}</main></div></div>;
}

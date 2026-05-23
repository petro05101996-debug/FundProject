import React from 'react';

export default function AppSidebar({ groups, page, onNavigate }: { groups: { title: string; items: { key: any; label: string }[] }[]; page: string; onNavigate: (k: any) => void }) {
  return (
    <aside className='app-sidebar dark'>
      {groups.map((g) => (
        <div key={g.title} className='side-group'>
          <p className='side-title'>{g.title}</p>
          {g.items.map((i) => (
            <button key={i.key} className={page === i.key ? 'nav active' : 'nav'} onClick={() => onNavigate(i.key)}>{i.label}</button>
          ))}
        </div>
      ))}
      <div className='side-footer muted'>v1.0.0</div>
    </aside>
  );
}

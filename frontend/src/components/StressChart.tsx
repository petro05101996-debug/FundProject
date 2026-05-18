import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
export default function StressChart({rows}:{rows:any[]}){const data=rows.slice(0,8).map((r:any)=>({name:r.stress_case||r.scenario,impact:Number(r.portfolio_impact_pct||0)}));return <div className='card soft'><h4>Стресс-тест</h4><div style={{height:220}}><ResponsiveContainer width='100%' height='100%'><BarChart data={data}><XAxis dataKey='name' hide/><YAxis/><Tooltip/><Bar dataKey='impact' fill='#f59e0b' /></BarChart></ResponsiveContainer></div></div>}

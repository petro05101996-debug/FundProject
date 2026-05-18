import React from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
export default function CashflowChart({rows}:{rows:any[]}){const data=(rows||[]).slice(0,10).map((r:any)=>({year:r.year,value:Number(r.value_before_stress||0)}));return <div className='card soft'><h4>Денежные потоки</h4><div style={{height:220}}><ResponsiveContainer width='100%' height='100%'><LineChart data={data}><XAxis dataKey='year'/><YAxis/><Tooltip/><Line type='monotone' dataKey='value' stroke='#22c55e' /></LineChart></ResponsiveContainer></div></div>}

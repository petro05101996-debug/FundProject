import React from 'react';
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from 'recharts';
const COLORS=['#22d3ee','#38bdf8','#818cf8','#f59e0b','#22c55e'];
export default function AllocationDonut({items}:{items:any[]}){const data=items.map((i:any)=>({name:i.asset_class,value:Number(i.weight_pct||0)}));return <div className='card soft'><h4>Структура активов</h4><div style={{height:220}}><ResponsiveContainer width='100%' height='100%'><PieChart><Pie data={data} dataKey='value' nameKey='name' innerRadius={50} outerRadius={80}>{data.map((_:any,i:number)=><Cell key={i} fill={COLORS[i%COLORS.length]} />)}</Pie><Tooltip /></PieChart></ResponsiveContainer></div></div>}

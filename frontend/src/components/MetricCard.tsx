import React from 'react';
export default function MetricCard({label,value}:{label:string;value:string|number}){return <div className='metric'><div className='muted'>{label}</div><div className='metric-value'>{value}</div></div>}

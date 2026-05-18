import React from 'react';
import MetricCard from './MetricCard';
export default function RiskPassport({risk,liquidity,complexity}:{risk:string;liquidity:string;complexity:string}){return <div className='grid3'><MetricCard label='Риск' value={risk}/><MetricCard label='Ликвидность' value={liquidity}/><MetricCard label='Сложность' value={complexity}/></div>}

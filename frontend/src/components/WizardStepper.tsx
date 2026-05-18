import React from 'react';
export default function WizardStepper({steps,current}:{steps:string[];current:number}){return <div className='row'>{steps.map((s,i)=><span key={s} className={i<=current?'pill active':'pill'}>{i+1}. {s}</span>)}</div>}

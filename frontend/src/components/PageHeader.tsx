import React from 'react';
export default function PageHeader({title,subtitle}:{title:string;subtitle?:string}){return <div><h2>{title}</h2>{subtitle&&<p className='muted'>{subtitle}</p>}</div>}

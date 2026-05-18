import React from 'react';
export default function Card({children,soft=false}:{children:React.ReactNode;soft?:boolean}){return <div className={soft?'card soft':'card'}>{children}</div>}

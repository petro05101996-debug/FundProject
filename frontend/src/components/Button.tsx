import React from 'react';
export default function Button({children,onClick,ghost=false}:{children:React.ReactNode;onClick?:()=>void;ghost?:boolean}){return <button className={ghost?'btn ghost':'btn'} onClick={onClick}>{children}</button>}

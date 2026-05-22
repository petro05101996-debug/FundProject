import React from 'react'; export default ({children,severity='neutral'}:{children:React.ReactNode;severity?:string})=><span className={`risk-chip ${severity}`}>{children}</span>;

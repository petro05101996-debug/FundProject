import React from 'react'; export default ({title,description}:{title:string;description?:string})=><div><h3>{title}</h3>{description&&<p className='muted'>{description}</p>}</div>;

import React, { useEffect, useMemo, useState } from 'react';
import AppShell from './components/AppShell';
import LandingPage from './pages/LandingPage';
import ScenarioProfilePage from './pages/ScenarioProfilePage';
import InstrumentCheckPage from './pages/InstrumentCheckPage';
import ScenarioBuilderPage from './pages/ScenarioBuilderPage';
import PortfolioCheckPage from './pages/PortfolioCheckPage';
import ResultsPage from './pages/ResultsPage';
import ReportPage from './pages/ReportPage';
import ExplainInstrumentPage from './pages/ExplainInstrumentPage';
import { defaultProfile, ScenarioProfile } from './utils/profileToApi';

type PageKey = 'landing'|'profile'|'instrument'|'builder'|'portfolio'|'results'|'report'|'explain';

export default function App(){
  const [page,setPage]=useState<PageKey>('landing');
  const [analysisResult,setAnalysisResult]=useState<any>(()=>{try{return JSON.parse(localStorage.getItem('analysisResult')||'null')}catch{return null}});
  const [profile,setProfile]=useState<ScenarioProfile>(()=>{try{return {...defaultProfile,...JSON.parse(localStorage.getItem('userProfile')||'{}')}}catch{return defaultProfile}});
  useEffect(()=>localStorage.setItem('userProfile',JSON.stringify(profile)),[profile]);
  useEffect(()=>localStorage.setItem('analysisResult',JSON.stringify(analysisResult)),[analysisResult]);

  const content = useMemo(()=>({
    landing:<LandingPage onStart={()=>setPage('profile')} onExplain={()=>setPage('explain')} />,
    profile:<ScenarioProfilePage profile={profile} setProfile={setProfile} onNavigate={setPage} />,
    instrument:<InstrumentCheckPage />,
    builder:<ScenarioBuilderPage profile={profile} onDone={(r:any)=>{setAnalysisResult(r);setPage('results')}} />,
    portfolio:<PortfolioCheckPage profile={profile} />,
    results:<ResultsPage profile={profile} result={analysisResult} onReport={()=>setPage('report')} onNavigate={setPage} />,
    report:<ReportPage result={analysisResult} onNavigate={setPage} />,
    explain:<ExplainInstrumentPage />,
  }[page]),[page,analysisResult,profile]);
  if (page==='landing') return <LandingPage onStart={()=>setPage('profile')} onExplain={()=>setPage('explain')} />
  return <AppShell page={page} onNavigate={setPage}>{content}</AppShell>
}

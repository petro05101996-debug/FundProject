import React, { useMemo, useState } from 'react';
import AppShell from './components/AppShell';
import LandingPage from './pages/LandingPage';
import ScenarioProfilePage from './pages/ScenarioProfilePage';
import InstrumentCheckPage from './pages/InstrumentCheckPage';
import ScenarioBuilderPage from './pages/ScenarioBuilderPage';
import PortfolioCheckPage from './pages/PortfolioCheckPage';
import ResultsPage from './pages/ResultsPage';
import ReportPage from './pages/ReportPage';
import ExplainInstrumentPage from './pages/ExplainInstrumentPage';
import ScenarioStartPage from './pages/ScenarioStartPage';
import GuidedDialogPage from './pages/GuidedDialogPage';
import ScenarioPreviewPage from './pages/ScenarioPreviewPage';
import GuidedResultPage from './pages/GuidedResultPage';
import OfferCheckPage from './pages/OfferCheckPage';
import { defaultProfile, ScenarioProfile } from './utils/profileToApi';
import { startDialog, getDialogPreview, analyzeGuided } from './api/client';

type PageKey = 'landing'|'start'|'guided'|'preview'|'guided_result'|'offer_check'|'profile'|'instrument'|'builder'|'portfolio'|'results'|'report'|'explain';

export default function App(){
  const [page,setPage]=useState<PageKey>('landing');
  const [analysisResult,setAnalysisResult]=useState<any>(null);
  const [guidedState,setGuidedState]=useState<any>(null);
  const [guidedPreview,setGuidedPreview]=useState<any>(null);
  const [guidedResult,setGuidedResult]=useState<any>(null);
  const [profile,setProfile]=useState<ScenarioProfile>(defaultProfile);
  const content = useMemo(()=>({
    start:<ScenarioStartPage onSelect={async(id)=>{if(id==='offer_check'){setPage('offer_check');return;} const s=await startDialog(id);setGuidedState(s);setPage('guided')}}/>,
    guided:<GuidedDialogPage state={guidedState} setState={setGuidedState} onPreview={async()=>{const p=await getDialogPreview(guidedState.session_state);setGuidedPreview(p);setPage('preview')}}/>,
    preview:<ScenarioPreviewPage preview={guidedPreview} onCalc={async()=>{const r=await analyzeGuided(guidedState.session_state);setGuidedResult(r);setPage('guided_result')}}/>,
    guided_result:<GuidedResultPage result={guidedResult}/>,
    offer_check:<OfferCheckPage/>,
    profile:<ScenarioProfilePage profile={profile} setProfile={setProfile} onNavigate={setPage as any} />,
    instrument:<InstrumentCheckPage />,
    builder:<ScenarioBuilderPage profile={profile} onDone={(r:any)=>{setAnalysisResult(r);setPage('results')}} />,
    portfolio:<PortfolioCheckPage profile={profile} />,
    results:<ResultsPage profile={profile} result={analysisResult} onReport={()=>setPage('report')} onNavigate={setPage as any} />,
    report:<ReportPage result={analysisResult||guidedResult} onNavigate={setPage as any} />,
    explain:<ExplainInstrumentPage />,
  } as any),[guidedState,guidedPreview,guidedResult,analysisResult,profile]);
  if(page==='landing') return <LandingPage onStart={()=>setPage('start')} onExplain={()=>setPage('explain')} onOfferCheck={()=>setPage('offer_check')} />
  return <AppShell page={page as any} onNavigate={setPage as any}>{content[page]}</AppShell>
}

"""Design system CSS for the dark enterprise Investment Scenario Lab shell."""

APP_CSS = """
<style>
:root {
  --lab-bg: #06111f;
  --lab-bg-2: #071827;
  --lab-rail: #061322;
  --lab-panel: #0b1b2d;
  --lab-panel-2: #10243a;
  --lab-panel-3: #132940;
  --lab-border: rgba(96, 165, 250, 0.16);
  --lab-border-strong: rgba(34, 211, 238, 0.48);
  --lab-text: #edf7ff;
  --lab-muted: #8da4bd;
  --lab-cyan: #23d6e6;
  --lab-teal: #2dd4bf;
  --lab-blue: #60a5fa;
  --lab-purple: #8b5cf6;
  --lab-warn: #f59e0b;
  --lab-danger: #fb7185;
  --lab-ok: #34d399;
  --lab-radius: 18px;
  --lab-shadow: 0 18px 55px rgba(0, 0, 0, 0.36);
}
#MainMenu, footer, header { visibility: hidden; height: 0; }
[data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stStatusWidget"] { display:none !important; }
[data-testid="stAppViewContainer"], .stApp {
  background:
    radial-gradient(circle at 18% 9%, rgba(34, 211, 238, 0.16), transparent 28%),
    radial-gradient(circle at 86% 0%, rgba(45, 212, 191, 0.10), transparent 24%),
    linear-gradient(135deg, #06111f 0%, #081827 54%, #050d18 100%) !important;
  color: var(--lab-text);
}
.block-container { padding: 0.75rem 1.05rem 1.5rem; max-width: 1480px; }
[data-testid="stSidebar"] {
  width: 276px !important;
  min-width: 276px !important;
  background: linear-gradient(180deg, rgba(6,19,34,.98) 0%, rgba(5,16,29,.98) 100%);
  border-right: 1px solid var(--lab-border);
  box-shadow: 20px 0 50px rgba(0,0,0,.18);
}
[data-testid="stSidebar"] [data-testid="stSidebarContent"] { padding: 1.05rem .9rem; }
[data-testid="stSidebar"] h3 { color:#f8fbff; font-size:1.02rem; margin-bottom:.1rem; }
[data-testid="stSidebar"] .stCaption, [data-testid="stSidebar"] p { color: var(--lab-muted); }
[data-testid="stSidebar"] .stButton > button {
  justify-content: flex-start;
  min-height: 40px;
  padding: .45rem .75rem;
  border-radius: 14px;
  border-color: rgba(96,165,250,.16);
  background: rgba(8, 26, 43, .34);
  color: #b7c7dc;
  box-shadow: none;
}
[data-testid="stSidebar"] .stButton > button:hover { border-color: var(--lab-cyan); color: #ecfeff; background: rgba(8, 26, 43, .72); }
[data-testid="stSidebar"] .stButton > button[kind="primary"],
[data-testid="stSidebar"] .stButton [data-testid="baseButton-primary"] {
  border-color: rgba(34,211,238,.52) !important;
  border-left: 4px solid var(--lab-cyan) !important;
  background: linear-gradient(135deg, rgba(34,211,238,.18), rgba(45,212,191,.08)) !important;
  color: #ecfeff !important;
  box-shadow: inset 0 0 0 1px rgba(34,211,238,.08), 0 10px 24px rgba(34,211,238,.08) !important;
}
[data-testid="stSidebar"] .stButton > button[kind="secondary"],
[data-testid="stSidebar"] .stButton [data-testid="baseButton-secondary"] {
  background: rgba(8, 26, 43, .34);
  color: #b7c7dc;
}
.lab-shell {
  border: 1px solid var(--lab-border);
  border-radius: 28px;
  padding: 22px;
  background: linear-gradient(135deg, rgba(8,24,39,.92), rgba(5,15,28,.94));
  box-shadow: var(--lab-shadow);
}
.lab-shell-landing {
  border:0;
  border-radius:0;
  padding:0;
  background:transparent;
  box-shadow:none;
}
.lab-topbar {
  min-height: 68px;
  display:flex;
  justify-content:space-between;
  align-items:center;
  gap:18px;
  margin: 0 0 16px;
  padding: 0 18px;
  border:1px solid var(--lab-border);
  border-radius: 0 0 18px 18px;
  background: rgba(6,17,31,.78);
  box-shadow:0 16px 46px rgba(0,0,0,.22);
  position: sticky;
  top: .25rem;
  z-index:5;
  backdrop-filter: blur(14px);
}
.lab-brand { display:flex; align-items:center; gap:12px; min-width:245px; }
.lab-brand-mark {
  width:38px; height:38px; display:grid; place-items:center; border-radius:12px;
  color:#071827; font-weight:950;
  background: linear-gradient(135deg, var(--lab-cyan), var(--lab-teal));
  box-shadow: 0 0 0 7px rgba(34,211,238,.08), 0 12px 30px rgba(34,211,238,.22);
}
.lab-brand-text { display:flex; flex-direction:column; gap:1px; }
.lab-brand-title { color:var(--lab-text); font-size:1rem; font-weight:900; letter-spacing:-.02em; }
.lab-brand-subtitle { color:var(--lab-muted); font-size:.76rem; }
.lab-topnav { display:flex; gap:18px; color:#b7c7dc; font-size:.82rem; font-weight:750; flex:1; justify-content:center; }
.lab-topnav span { padding:7px 4px; border-bottom:1px solid transparent; }
.lab-topnav span:hover { color:#e0fbff; border-color:rgba(34,211,238,.55); }
.lab-top-actions { display:flex; gap:10px; align-items:center; color:#b7c7dc; }
.lab-icon-btn, .lab-pill {
  display:inline-flex; align-items:center; justify-content:center; gap:8px;
  border:1px solid var(--lab-border); background:rgba(8, 26, 43, .78); color:#a5f3fc;
  padding:8px 12px; border-radius:10px; font-size:.78rem; font-weight:850;
}
.lab-icon-btn { width:34px; height:34px; padding:0; border-radius:50%; }
.lab-primary-pill { border-color: var(--lab-border-strong); color:#dffcff; box-shadow: inset 0 0 0 1px rgba(34,211,238,.08); }
.lab-page-header { display:flex; justify-content:space-between; align-items:flex-start; gap:18px; margin: 4px 0 16px; }
.lab-page-kicker { color:var(--lab-muted); font-size:.88rem; margin-top:4px; }
h1, h2, h3, h4 { color:#f8fbff !important; letter-spacing:-.025em; }
h2 { font-size:2.15rem !important; line-height:1.05 !important; margin: .1rem 0 .25rem !important; }
p, li, label, .stMarkdown, .stCaption { color:#b7c7dc; }
.lab-sidebar-group { color:#64748b; font-size:.70rem; font-weight:950; letter-spacing:.11em; margin:17px 0 7px; }
.lab-nav-item {
  border:1px solid transparent; border-radius:14px; padding:10px 11px; margin:4px 0;
  color:#cbd5e1; font-weight:750; background:rgba(15,23,42,.28);
}
.lab-nav-item-active { border-color:rgba(34,211,238,.40); border-left:4px solid var(--lab-cyan); background:rgba(34,211,238,.13); color:#ecfeff; }
.lab-feedback { border:1px solid var(--lab-border); border-radius:18px; padding:13px; background:rgba(34,211,238,.07); color:#bfdbfe; margin-top:18px; }
.lab-hero {
  display:grid; grid-template-columns: 1.02fr .98fr; gap:26px; padding:28px;
  border-radius:28px;
  background:
    linear-gradient(135deg, rgba(34,211,238,.16), rgba(45,212,191,.05) 43%, rgba(8,24,39,.92)),
    radial-gradient(circle at 72% 24%, rgba(96,165,250,.15), transparent 32%);
  border:1px solid var(--lab-border);
  box-shadow: inset 0 1px 0 rgba(255,255,255,.04);
}
.lab-hero h1 { font-size:3.22rem !important; line-height:1.0 !important; margin:12px 0 16px !important; letter-spacing:-.055em; }
.lab-hero h1 .accent, .accent { color: var(--lab-cyan); }
.lab-hero p { color:#b7c7dc; font-size:1.03rem; max-width:760px; }
.lab-trust-row { display:grid; grid-template-columns:repeat(3,1fr); gap:12px; margin-top:17px; }
.lab-trust-item { display:flex; gap:10px; align-items:center; color:#a8c1db; font-weight:700; font-size:.86rem; }
.lab-trust-icon { width:34px; height:34px; border-radius:50%; display:grid; place-items:center; color:var(--lab-cyan); background:rgba(34,211,238,.10); border:1px solid rgba(34,211,238,.22); }
.lab-preview-dashboard, .lab-card, .lab-panel, .lab-table-card, .lab-mode-card, .lab-mode-card-active, .lab-step-card, .lab-right-panel {
  border:1px solid var(--lab-border);
  background:linear-gradient(180deg, rgba(16,36,58,.90), rgba(9,25,42,.88));
  border-radius:var(--lab-radius);
  padding:18px;
  box-shadow: 0 12px 36px rgba(0,0,0,.22);
  min-height: 104px;
}
.lab-preview-dashboard { min-height:360px; }
.lab-card:hover, .lab-mode-card:hover { border-color: var(--lab-border-strong); box-shadow:0 18px 44px rgba(34,211,238,.11); }
.lab-card-strong, .lab-mode-card-active { border-color:var(--lab-border-strong); background:linear-gradient(180deg, rgba(34,211,238,.14), rgba(9,25,42,.92)); }
.lab-card h3, .lab-panel h3, .lab-right-panel h3, .lab-table-card h3 { margin:0 0 8px; color:#f8fbff; font-size:1.02rem; }
.lab-card p, .lab-card li, .lab-panel p, .lab-panel li, .lab-right-panel p, .lab-right-panel li { color:#a9bfd8; font-size:.88rem; }
.lab-grid { display:grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap:16px; }
.lab-grid-2 { display:grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap:16px; }
.lab-grid-4 { display:grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap:16px; }
.lab-metric-strip { display:grid; grid-template-columns: repeat(5, 1fr); gap:8px; margin-top: 8px; }
.lab-mini-kpi { border:1px solid rgba(96,165,250,.13); background:rgba(5,14,26,.42); border-radius:13px; padding:12px; }
.lab-mini-kpi .label, .lab-kpi-label { color:#8da4bd; font-size:.74rem; font-weight:850; }
.lab-mini-kpi .value, .lab-kpi-value { color:#f8fbff; font-size:1.36rem; font-weight:950; letter-spacing:-.035em; }
.lab-kpi-card { min-height:96px; }
.lab-badge, .lab-risk-chip {
  display:inline-flex; align-items:center; gap:7px; border:1px solid var(--lab-border);
  background:rgba(34,211,238,.08); color:#a5f3fc; padding:7px 10px; border-radius:999px;
  font-size:.74rem; font-weight:900; margin: 2px 4px 8px 0;
}
.lab-badge.ok, .lab-risk-chip.Low, .lab-risk-chip.Info { color:#86efac; background:rgba(52,211,153,.10); border-color:rgba(52,211,153,.28); }
.lab-badge.warn, .lab-risk-chip.Medium { color:#fde68a; background:rgba(245,158,11,.10); border-color:rgba(245,158,11,.30); }
.lab-badge.danger, .lab-risk-chip.High { color:#fecdd3; background:rgba(251,113,133,.10); border-color:rgba(251,113,133,.30); }

.lab-share-pill { display:inline-flex; align-items:center; justify-content:center; min-width:42px; padding:6px 9px; margin:5px 5px 10px 0; border-radius:999px; background:rgba(139,92,246,.18); color:#d8b4fe; font-size:.76rem; font-weight:900; border:1px solid rgba(139,92,246,.26); }
.lab-instrument-row { display:flex; justify-content:space-between; align-items:center; gap:12px; padding:9px 0; border-top:1px solid rgba(96,165,250,.12); color:#e5f0ff; font-weight:800; }
.lab-instrument-row small { display:block; color:#8da4bd; font-size:.72rem; font-weight:700; margin-top:2px; }
.lab-risk-dot { color:#7dd3fc; font-size:.72rem; border:1px solid rgba(34,211,238,.20); background:rgba(34,211,238,.08); border-radius:999px; padding:4px 7px; white-space:nowrap; }
.lab-add-line { color:var(--lab-cyan); text-align:center; font-weight:900; font-size:.83rem; padding-top:10px; border-top:1px solid rgba(96,165,250,.12); }

.lab-disclaimer { border:1px solid rgba(96,165,250,.20); background:rgba(37,99,235,.08); color:#bcd2ed; border-radius:15px; padding:12px 14px; margin:10px 0 16px; font-size:.84rem; }
.lab-status-banner { border:1px solid rgba(34,211,238,.38); background:linear-gradient(135deg, rgba(34,211,238,.16), rgba(45,212,191,.08)); border-radius:18px; padding:16px; color:#e0fbff; }
.lab-action-bar { display:flex; justify-content:space-between; align-items:center; gap:12px; padding:14px; border:1px solid var(--lab-border); border-radius:18px; background:rgba(15,23,42,.50); }
.lab-empty { border:1px dashed rgba(96,165,250,.28); border-radius:18px; padding:24px; color:#b7c7dc; background:rgba(15,23,42,.38); text-align:center; }
.stButton > button, .stDownloadButton > button {
  border-radius: 12px; border: 1px solid var(--lab-border-strong);
  background: linear-gradient(135deg, rgba(35,214,230,.95), rgba(45,212,191,.86));
  color:#04202d; font-weight:900; min-height:42px; box-shadow:0 12px 30px rgba(34,211,238,.12);
}
.stButton > button:hover, .stDownloadButton > button:hover { border-color:#67e8f9; color:#00131c; transform: translateY(-1px); }
.stTextInput input, .stNumberInput input, .stSelectbox [data-baseweb="select"], .stTextArea textarea {
  background: rgba(5, 18, 32, .74) !important; color:#e5f0ff !important; border-color: rgba(96,165,250,.18) !important; border-radius: 12px !important;
}
.stSlider [data-baseweb="slider"] { color: var(--lab-cyan); }
.stTabs [data-baseweb="tab-list"] { gap:8px; background: rgba(5,18,32,.66); border:1px solid var(--lab-border); border-radius:14px; padding:5px; }
.stTabs [data-baseweb="tab"] { border-radius:10px; color:#9fb5cc; font-weight:850; }
.stTabs [aria-selected="true"] { background: linear-gradient(135deg, var(--lab-cyan), var(--lab-teal)); color:#04202d !important; }
[data-testid="stDataFrame"], [data-testid="stDataEditor"] { border-radius: 16px; overflow:hidden; border:1px solid rgba(96,165,250,.14); }
.lab-report-layout { display:grid; grid-template-columns: 260px 1fr; gap:18px; }
.lab-report-canvas { background:#f8fafc; color:#0f172a; border-radius:24px; padding:28px; border:1px solid rgba(226,232,240,1); box-shadow:0 24px 70px rgba(2,6,23,.28); }
.lab-report-canvas h2, .lab-report-canvas h3 { color:#0f172a !important; }
.lab-report-canvas p, .lab-report-canvas li { color:#334155; }
.lab-report-section { background:#fff; border:1px solid #e2e8f0; border-radius:18px; padding:18px; margin:14px 0; }
@media (max-width: 980px) {
  .lab-grid, .lab-grid-2, .lab-grid-4, .lab-hero, .lab-report-layout, .lab-trust-row, .lab-metric-strip { grid-template-columns:1fr; }
  .lab-hero h1 { font-size:2.25rem !important; }
  .lab-topnav { display:none; }
  .lab-topbar { position:relative; flex-wrap:wrap; padding:14px; }
}

/* Mockup fidelity overrides: denser dark desktop workspace matching Download.rar screens. */
html { background:#020914; }
[data-testid="stAppViewContainer"], .stApp {
  background:
    radial-gradient(circle at 8% 0%, rgba(28, 187, 208, .13), transparent 24%),
    radial-gradient(circle at 83% 18%, rgba(32, 115, 214, .12), transparent 25%),
    linear-gradient(180deg, #030b16 0%, #061320 48%, #05101c 100%) !important;
}
.block-container { padding: .55rem 1.15rem 1.1rem !important; max-width: 1440px !important; }
[data-testid="stSidebar"] {
  width: 248px !important;
  min-width: 248px !important;
  background: linear-gradient(180deg, rgba(4,14,26,.99), rgba(5,18,31,.98)) !important;
  border-right:1px solid rgba(96,165,250,.14) !important;
}
[data-testid="stSidebar"] [data-testid="stSidebarContent"] { padding: .85rem .72rem !important; }
[data-testid="stSidebar"] h3 { font-size:.96rem !important; letter-spacing:-.02em; }
.lab-topbar {
  min-height: 54px !important;
  margin: 0 -2px 18px !important;
  padding: 0 18px !important;
  border-width:0 0 1px 0 !important;
  border-radius:0 !important;
  background: rgba(3,11,22,.82) !important;
  box-shadow: 0 10px 36px rgba(0,0,0,.22) !important;
  top:0 !important;
}
.lab-brand { min-width: 252px; gap:10px; }
.lab-brand-mark {
  width:34px !important; height:34px !important; border-radius:11px !important;
  color:transparent !important; position:relative; background: rgba(9,31,48,.76) !important;
  border:1px solid rgba(35,214,230,.62); box-shadow:0 0 0 5px rgba(34,211,238,.05), inset 0 0 22px rgba(34,211,238,.15) !important;
}
.lab-brand-mark:before { content:""; position:absolute; inset:7px; border:1.5px solid #23d6e6; border-radius:5px; transform:rotate(-35deg); opacity:.9; }
.lab-brand-mark:after { content:"▥"; position:absolute; inset:0; display:grid; place-items:center; color:#5eead4; font-size:16px; font-weight:900; }
.lab-brand-title { font-size:.96rem !important; }
.lab-brand-subtitle { font-size:.66rem !important; color:#7890aa !important; }
.lab-topnav { gap:24px !important; font-size:.76rem !important; color:#a8b8cb !important; }
.lab-top-actions { gap:12px !important; }
.lab-pill, .lab-icon-btn { background:rgba(5,17,30,.65) !important; border-color:rgba(96,165,250,.18) !important; }
.lab-primary-pill { border-color:rgba(35,214,230,.44) !important; color:#a5f3fc !important; }
h1 { font-size:3.15rem !important; line-height:1.02 !important; margin:.25rem 0 1rem !important; font-weight:950 !important; }
h2 { font-size:2rem !important; line-height:1.07 !important; font-weight:950 !important; }
h3 { font-size:1.05rem !important; }
.accent { color:#50f0f4; text-shadow:0 0 24px rgba(34,211,238,.18); }
.lab-page-header { margin:2px 0 14px !important; }
.lab-page-kicker { color:#91a8bf !important; font-size:.86rem !important; }
.lab-hero {
  padding: 24px 22px 12px !important;
  border:0 !important;
  border-radius:0 !important;
  background: radial-gradient(circle at 92% 4%, rgba(37,99,235,.20), transparent 32%) !important;
  box-shadow:none !important;
  gap:22px !important;
}
.lab-hero p { max-width:680px; color:#b8c6d6; line-height:1.5; font-size:.98rem; }
.lab-preview-dashboard, .lab-card, .lab-panel, .lab-table-card, .lab-mode-card, .lab-mode-card-active, .lab-step-card, .lab-right-panel {
  border:1px solid rgba(96,165,250,.14) !important;
  background: linear-gradient(180deg, rgba(11,29,47,.94), rgba(7,22,38,.94)) !important;
  border-radius: 14px !important;
  box-shadow: inset 0 1px 0 rgba(255,255,255,.025), 0 14px 34px rgba(0,0,0,.20) !important;
}
.lab-preview-dashboard { min-height:342px !important; padding:18px !important; }
.lab-card, .lab-panel, .lab-table-card, .lab-mode-card, .lab-mode-card-active, .lab-step-card, .lab-right-panel { padding:16px !important; }
.lab-card-strong, .lab-mode-card-active { border-color:rgba(35,214,230,.54) !important; box-shadow:0 0 0 1px rgba(34,211,238,.12), 0 14px 36px rgba(34,211,238,.08) !important; }
.lab-grid, .lab-grid-2, .lab-grid-4 { gap:12px !important; }
.lab-trust-row { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:14px; margin-top:18px; }
.lab-trust-item { display:flex; align-items:center; gap:10px; color:#a9bbcf; font-size:.78rem; }
.lab-trust-icon { display:grid; place-items:center; width:30px; height:30px; border-radius:50%; color:#40e0e7; background:rgba(34,211,238,.10); border:1px solid rgba(34,211,238,.18); }
.lab-badge, .lab-risk-chip { border-radius:999px !important; padding:6px 10px !important; font-size:.70rem !important; }
.lab-instrument-row { padding:10px 0 !important; border-top:1px solid rgba(96,165,250,.10) !important; }
.lab-metric-strip { grid-template-columns:repeat(5,minmax(0,1fr)) !important; }
.lab-mini-kpi { background:rgba(5,15,27,.72) !important; border-color:rgba(96,165,250,.12) !important; border-radius:12px !important; }
.lab-action-bar { border-radius:14px !important; background:rgba(7,22,38,.74) !important; border-color:rgba(96,165,250,.14) !important; }
.stButton > button, .stDownloadButton > button {
  min-height:38px !important; border-radius:9px !important; font-size:.82rem !important;
  background:linear-gradient(135deg, #29dce8, #29c9c3) !important; color:#05212e !important;
}
.stButton > button[kind="secondary"], [data-testid="baseButton-secondary"] {
  background:rgba(5,18,32,.72) !important; color:#bfe7ef !important; border-color:rgba(96,165,250,.26) !important;
}
.stTextInput input, .stNumberInput input, .stSelectbox [data-baseweb="select"], .stTextArea textarea {
  background:rgba(5,18,32,.88) !important; min-height:38px !important; border-radius:8px !important;
}
[data-testid="stSidebar"] .stButton > button { min-height:38px !important; border-radius:10px !important; font-size:.82rem !important; }
.lab-disclaimer { background:rgba(37,99,235,.06) !important; border-color:rgba(96,165,250,.14) !important; font-size:.78rem !important; }
.lab-footer-strip { display:grid; grid-template-columns:1fr 1.1fr 1fr; gap:14px; margin-top:16px; padding:14px 0; border-top:1px solid rgba(96,165,250,.12); color:#8398af; font-size:.76rem; }
.lab-warning-strip { border:1px solid rgba(245,158,11,.22); background:rgba(245,158,11,.08); color:#f8d189; border-radius:10px; padding:10px 12px; margin:10px 0 14px; font-size:.82rem; }
@media (max-width: 980px) {
  h1 { font-size:2.2rem !important; }
  .lab-footer-strip { grid-template-columns:1fr; }
}

.lab-mock-header-actions { display:flex; justify-content:flex-end; align-items:center; gap:10px; }
.lab-workspace-select { min-width:220px; border:1px solid rgba(96,165,250,.14); background:rgba(5,18,32,.82); border-radius:10px; padding:9px 12px; color:#e5f0ff; font-size:.78rem; }
.lab-workspace-select small { display:block; color:#7b91aa; font-weight:800; }
.lab-mode-icon { display:inline-grid; place-items:center; width:34px; height:34px; border-radius:11px; border:1px solid rgba(34,211,238,.23); background:rgba(34,211,238,.08); color:#46e0ea; margin-bottom:12px; }
.lab-mode-check { float:right; width:20px; height:20px; display:grid; place-items:center; border-radius:50%; background:#23d6e6; color:#05202d; font-weight:950; font-size:.72rem; }
.lab-compact-tabs { display:grid; grid-template-columns:repeat(6,minmax(0,1fr)); gap:0; margin:12px 0 14px; border:1px solid rgba(96,165,250,.14); border-radius:10px; overflow:hidden; background:rgba(6,20,35,.72); }
.lab-compact-tab { text-align:center; padding:10px 8px; color:#9fb1c7; font-size:.82rem; border-right:1px solid rgba(96,165,250,.10); }
.lab-compact-tab:last-child { border-right:0; }
.lab-compact-tab.active { background:linear-gradient(135deg,#25dce8,#28cbc5); color:#05212e; font-weight:950; box-shadow:0 0 28px rgba(34,211,238,.22); }
.lab-result-list { display:grid; gap:11px; }
.lab-result-line { display:flex; justify-content:space-between; align-items:center; gap:12px; padding:8px 0; border-bottom:1px solid rgba(96,165,250,.10); color:#dbeafe; }
.lab-result-line small { display:block; color:#7f96ae; font-size:.68rem; margin-top:2px; }
.lab-value-green { color:#4ade80; font-weight:950; }
.lab-value-red { color:#fb7185; font-weight:950; }
.lab-chip-row { display:flex; flex-wrap:wrap; gap:8px; margin-top:8px; }
.lab-risk-flag { display:inline-flex; align-items:center; gap:7px; padding:8px 10px; border-radius:9px; background:rgba(245,158,11,.10); border:1px solid rgba(245,158,11,.20); color:#f8d189; font-size:.76rem; font-weight:850; }
.lab-risk-flag.danger { background:rgba(251,113,133,.11); border-color:rgba(251,113,133,.22); color:#fecdd3; }
.lab-risk-flag.info { background:rgba(34,211,238,.08); border-color:rgba(34,211,238,.20); color:#a5f3fc; }
.lab-sidebar-card { border:1px solid rgba(96,165,250,.14); background:linear-gradient(180deg,rgba(10,30,49,.92),rgba(7,22,38,.92)); border-radius:14px; padding:15px; margin-bottom:12px; }
.lab-sidebar-card h3 { margin-top:0 !important; }
.lab-sidebar-list { display:grid; gap:14px; }
.lab-sidebar-list div { color:#b7c7dc; font-size:.82rem; }
.lab-sidebar-list strong { color:#e5f0ff; display:block; margin-bottom:3px; }
.lab-table-shell [data-testid="stDataFrame"], .lab-table-shell [data-testid="stDataEditor"] { background:rgba(8,24,39,.8); }
.lab-notice-lock { display:flex; align-items:center; gap:10px; border:1px solid rgba(96,165,250,.12); background:rgba(6,20,35,.62); border-radius:12px; padding:11px 13px; color:#94a9c1; font-size:.78rem; }
.lab-status-ok { border:1px solid rgba(34,211,238,.35); background:rgba(34,211,238,.08); border-radius:12px; padding:14px 16px; color:#dffcff; }
.lab-status-ok strong { color:#9ffcf5; }
.lab-kpi-row-6 { display:grid; grid-template-columns:repeat(6,minmax(0,1fr)); gap:12px; margin:14px 0; }
.lab-footer-mini { display:flex; justify-content:space-between; gap:18px; margin-top:16px; color:#758aa3; font-size:.72rem; }
@media (max-width: 1100px) {
  .lab-compact-tabs, .lab-kpi-row-6 { grid-template-columns:repeat(2,minmax(0,1fr)); }
}

</style>
"""

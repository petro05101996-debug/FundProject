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
  min-height: 30px;
  padding: .15rem .65rem;
  border-color: rgba(96,165,250,.16);
  background: rgba(8, 26, 43, .64);
  color: #b7c7dc;
  box-shadow: none;
}
[data-testid="stSidebar"] .stButton > button:hover { border-color: var(--lab-cyan); color: #ecfeff; }
.lab-shell {
  border: 1px solid var(--lab-border);
  border-radius: 28px;
  padding: 22px;
  background: linear-gradient(135deg, rgba(8,24,39,.92), rgba(5,15,28,.94));
  box-shadow: var(--lab-shadow);
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
</style>
"""

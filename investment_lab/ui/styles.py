"""Design system CSS for the dark enterprise Investment Scenario Lab shell."""

APP_CSS = """
<style>
:root {
  --lab-bg: #06111f; --lab-bg-2: #081827; --lab-panel: #0d1b2e; --lab-panel-2: #12243a;
  --lab-border: rgba(148, 163, 184, 0.18); --lab-border-strong: rgba(34, 211, 238, 0.42);
  --lab-text: #e5f0ff; --lab-muted: #91a4bd; --lab-cyan: #22d3ee; --lab-teal: #2dd4bf;
  --lab-warn: #f59e0b; --lab-danger: #fb7185; --lab-ok: #34d399; --lab-radius: 22px;
}
#MainMenu, footer, header { visibility: hidden; height: 0; }
[data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stStatusWidget"] { display:none !important; }
[data-testid="stAppViewContainer"] { background: radial-gradient(circle at 15% 10%, rgba(34, 211, 238, 0.14), transparent 32%), radial-gradient(circle at 90% 0%, rgba(45, 212, 191, 0.10), transparent 28%), linear-gradient(135deg, #06111f 0%, #081827 48%, #0b1020 100%); }
.stApp { background: radial-gradient(circle at top left, rgba(34,211,238,.16), transparent 28%), linear-gradient(135deg, var(--lab-bg), var(--lab-bg-2)); color: var(--lab-text); }
.block-container { padding: 1.1rem 1.4rem 2rem; max-width: 1440px; }
[data-testid="stSidebar"] { width: 270px !important; background: linear-gradient(180deg, #071425 0%, #0b1728 100%); border-right: 1px solid var(--lab-border); }
[data-testid="stSidebar"] .stRadio label { color: #dbeafe !important; }
.stButton > button { border-radius: 999px; border: 1px solid var(--lab-border-strong); background: linear-gradient(135deg, rgba(34,211,238,.24), rgba(45,212,191,.16)); color:#e0fbff; font-weight:800; box-shadow:0 12px 30px rgba(34,211,238,.10); }
.stButton > button:hover { border-color: var(--lab-cyan); color:white; transform: translateY(-1px); }
.lab-page { display:flex; flex-direction:column; gap:18px; } .lab-page-header { display:flex; justify-content:space-between; align-items:flex-start; gap:16px; margin-bottom:14px; }
.lab-shell { border: 1px solid var(--lab-border); border-radius: 28px; padding: 22px; background: linear-gradient(135deg, rgba(13,27,46,.96), rgba(7,17,31,.92)); box-shadow: 0 24px 70px rgba(0,0,0,.34); }
.lab-topbar { min-height:72px; display:flex; justify-content:space-between; align-items:center; gap:16px; margin-bottom:18px; padding:0 14px; border:1px solid var(--lab-border); border-radius:22px; background:rgba(6,17,31,.78); box-shadow:0 16px 46px rgba(0,0,0,.22); position:sticky; top:.5rem; z-index:5; backdrop-filter: blur(14px); }
.lab-brand { display:flex; flex-direction:column; gap:2px; } .lab-topnav { display:flex; gap:14px; color:#b7c7dc; font-size:.86rem; font-weight:700; } .lab-topnav span { padding:7px 10px; border-radius:999px; } .lab-topnav span:hover { background:rgba(34,211,238,.10); color:#e0fbff; }.lab-brand-title { color:var(--lab-text); font-size:1.25rem; font-weight:900; letter-spacing:.02em; }.lab-brand-subtitle { color:var(--lab-muted); font-size:.86rem; }
.lab-pill, .lab-risk-chip { display:inline-flex; align-items:center; gap:8px; border:1px solid var(--lab-border); background:rgba(34,211,238,.08); color:#a5f3fc; padding:8px 12px; border-radius:999px; font-size:.82rem; font-weight:800; }
.lab-hero { display:grid; grid-template-columns: 1.1fr .9fr; gap:24px; padding:34px; border-radius:28px; background: linear-gradient(135deg, rgba(34,211,238,.17), rgba(45,212,191,.07) 44%, rgba(15,23,42,.90)); border:1px solid var(--lab-border); }
.lab-hero h1 { font-size:3.05rem; line-height:1.02; margin:0 0 14px 0; color:#f8fbff; letter-spacing:-.045em; }.lab-hero p { color:#b7c7dc; font-size:1.08rem; max-width:760px; }
.lab-grid { display:grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap:16px; }.lab-grid-2 { display:grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap:16px; }.lab-grid-4 { display:grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap:16px; }
.lab-card, .lab-panel, .lab-table-card, .lab-mode-card, .lab-mode-card-active, .lab-step-card, .lab-preview-dashboard, .lab-right-panel { border:1px solid var(--lab-border); background:linear-gradient(180deg, rgba(18,36,58,.88), rgba(13,27,46,.84)); border-radius:var(--lab-radius); padding:18px; box-shadow: 0 12px 36px rgba(0,0,0,.20); min-height:112px; }
.lab-card:hover, .lab-mode-card:hover { border-color: var(--lab-border-strong); box-shadow:0 18px 44px rgba(34,211,238,.12); }.lab-card-strong, .lab-mode-card-active { border-color:var(--lab-border-strong); background:linear-gradient(180deg, rgba(34,211,238,.14), rgba(13,27,46,.90)); } .lab-status-banner { border:1px solid rgba(34,211,238,.38); background:linear-gradient(135deg, rgba(34,211,238,.16), rgba(45,212,191,.08)); border-radius:22px; padding:18px; color:#e0fbff; }
.lab-card h3, .lab-panel h3 { margin:0 0 8px; color:#f8fbff; font-size:1.05rem; }.lab-card p, .lab-card li, .lab-panel p, .lab-panel li { color:#aebed2; }
.lab-kpi-card, .lab-kpi { border-left: 3px solid var(--lab-cyan); }.lab-kpi-value { font-size:1.75rem; font-weight:900; color:#f8fbff; }.lab-kpi-label { color:var(--lab-muted); font-size:.84rem; }
.lab-badge { display:inline-flex; border-radius:999px; padding:5px 10px; font-weight:800; font-size:.76rem; border:1px solid var(--lab-border); color:#cffafe; background:rgba(34,211,238,.10); }.lab-badge.warn, .lab-risk-chip.Medium { color:#fde68a; background:rgba(245,158,11,.12); border-color:rgba(245,158,11,.32); }.lab-badge.danger, .lab-risk-chip.High { color:#fecdd3; background:rgba(251,113,133,.12); border-color:rgba(251,113,133,.34); }.lab-badge.ok, .lab-risk-chip.Low { color:#bbf7d0; background:rgba(52,211,153,.12); border-color:rgba(52,211,153,.34); }.lab-risk-chip.Info { color:#bfdbfe; background:rgba(96,165,250,.12); border-color:rgba(96,165,250,.34); }
.lab-empty-state { border:1px dashed rgba(148,163,184,.38); border-radius:22px; padding:28px; color:#b7c7dc; background:rgba(15,23,42,.38); text-align:center; }
.lab-disclaimer { border:1px solid rgba(245,158,11,.28); background:rgba(245,158,11,.10); border-radius:18px; padding:14px 16px; color:#fdecc8; }.lab-empty { border:1px dashed rgba(148,163,184,.38); border-radius:22px; padding:28px; color:#b7c7dc; background:rgba(15,23,42,.38); text-align:center; }.lab-action-bar { display:flex; justify-content:space-between; align-items:center; gap:12px; padding:14px; border:1px solid var(--lab-border); border-radius:20px; background:rgba(15,23,42,.52); }
.lab-report-layout { display:grid; grid-template-columns: 260px 1fr; gap:18px; }.lab-report-canvas { background:#f8fafc; color:#0f172a; border-radius:24px; padding:28px; border:1px solid rgba(226,232,240,1); box-shadow:0 24px 70px rgba(2,6,23,.28); }.lab-report-canvas h2, .lab-report-canvas h3 { color:#0f172a; }.lab-report-canvas p, .lab-report-canvas li { color:#334155; }.lab-report-section { background:#fff; border:1px solid #e2e8f0; border-radius:18px; padding:18px; margin:14px 0; }
.lab-sidebar-group { color:#64748b; font-size:.72rem; font-weight:900; letter-spacing:.08em; margin:16px 0 6px; } .lab-nav-item { border:1px solid transparent; border-radius:14px; padding:9px 11px; margin:4px 0; color:#cbd5e1; font-weight:650; background:rgba(15,23,42,.28); } .lab-nav-item-active { border-color:rgba(34,211,238,.40); border-left:4px solid var(--lab-cyan); background:rgba(34,211,238,.13); color:#ecfeff; }.lab-feedback { border:1px solid var(--lab-border); border-radius:18px; padding:12px; background:rgba(34,211,238,.08); color:#bfdbfe; margin-top:18px; }
@media (max-width: 980px) { .lab-grid, .lab-grid-2, .lab-grid-4, .lab-hero, .lab-report-layout { grid-template-columns:1fr; } .lab-hero h1 { font-size:2.2rem; } }
</style>
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import sys
import re
import io
import base64
from datetime import datetime
from crewai import Crew, Process, Task
import SOP

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="AlBrain S&OP Intelligence",
    layout="wide",
    page_icon="🧠",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  GLOBAL CSS — Design premium bleu marine / or
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700;800&family=Inter:wght@300;400;500;600&display=swap');

/* ── BASE ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #04091a;
    color: #e8eaf0;
}
.stApp { background-color: #04091a; }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #07112b 0%, #0a1a3a 100%);
    border-right: 1px solid #1e3a6e;
}
[data-testid="stSidebar"] * { color: #c8d4e8 !important; }
[data-testid="stSidebar"] .stRadio label { font-size: 0.85rem; }

/* ── HEADER LOGO ── */
.albrain-header {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 20px 24px 16px;
    border-bottom: 1px solid #1e3a6e;
    margin-bottom: 8px;
}
.albrain-logo-box {
    width: 44px; height: 44px;
    border: 2.5px solid #2563eb;
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-family: 'Montserrat', sans-serif;
    font-weight: 800; font-size: 15px;
    color: #2563eb;
    background: #071428;
    letter-spacing: -0.5px;
    flex-shrink: 0;
}
.albrain-title { line-height: 1.1; }
.albrain-title .brand { font-family: 'Montserrat', sans-serif; font-weight: 800; font-size: 1.15rem; color: #f0f4ff; letter-spacing: 0.04em; }
.albrain-title .sub { font-size: 0.7rem; color: #5a7ab5; letter-spacing: 0.12em; text-transform: uppercase; font-weight: 500; }

/* ── NAV TABS ── */
.nav-container {
    display: flex;
    gap: 4px;
    background: #07112b;
    border: 1px solid #1e3a6e;
    border-radius: 12px;
    padding: 5px;
    margin-bottom: 28px;
}
.nav-btn {
    flex: 1; padding: 10px 0;
    border: none; border-radius: 8px;
    font-family: 'Montserrat', sans-serif;
    font-weight: 600; font-size: 0.82rem;
    cursor: pointer; transition: all 0.2s;
    letter-spacing: 0.03em;
    background: transparent; color: #5a7ab5;
}
.nav-btn.active { background: #1e40af; color: #ffffff; box-shadow: 0 2px 12px rgba(30,64,175,0.4); }
.nav-btn:hover:not(.active) { background: #0f2040; color: #93b4d8; }

/* ── KPI CARDS ── */
.kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 28px; }
.kpi-card {
    background: #07112b;
    border: 1px solid #1e3a6e;
    border-radius: 14px;
    padding: 20px 22px;
    position: relative; overflow: hidden;
    transition: border-color 0.2s;
}
.kpi-card:hover { border-color: #2563eb; }
.kpi-card::before {
    content: ''; position: absolute;
    top: 0; left: 0; right: 0; height: 3px;
    border-radius: 14px 14px 0 0;
}
.kpi-card.blue::before { background: #2563eb; }
.kpi-card.gold::before { background: #d4a017; }
.kpi-card.green::before { background: #16a34a; }
.kpi-card.red::before { background: #dc2626; }
.kpi-label { font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.1em; color: #5a7ab5; font-weight: 600; margin-bottom: 8px; }
.kpi-value { font-family: 'Montserrat', sans-serif; font-size: 1.9rem; font-weight: 700; color: #f0f4ff; line-height: 1; }
.kpi-delta { font-size: 0.75rem; margin-top: 6px; font-weight: 500; }
.kpi-delta.up { color: #22c55e; }
.kpi-delta.down { color: #ef4444; }
.kpi-delta.neutral { color: #5a7ab5; }

/* ── SECTION TITLES ── */
.section-title {
    font-family: 'Montserrat', sans-serif;
    font-weight: 700; font-size: 1.05rem;
    color: #f0f4ff; letter-spacing: 0.02em;
    margin: 28px 0 16px;
    display: flex; align-items: center; gap: 10px;
}
.section-title::after {
    content: ''; flex: 1; height: 1px;
    background: linear-gradient(90deg, #1e3a6e, transparent);
}

/* ── SCENARIO CARD ── */
.scenario-card {
    background: #07112b;
    border: 1px solid #1e3a6e;
    border-radius: 14px;
    padding: 22px 24px;
    margin-bottom: 20px;
}
.scenario-tag {
    display: inline-block;
    padding: 3px 12px; border-radius: 20px;
    font-size: 0.72rem; font-weight: 600;
    letter-spacing: 0.08em; text-transform: uppercase;
    margin-bottom: 12px;
}
.tag-nominal { background: #052e16; color: #22c55e; border: 1px solid #16a34a; }
.tag-crisis  { background: #2d0a0a; color: #ef4444; border: 1px solid #dc2626; }
.tag-peak    { background: #0c1a4a; color: #60a5fa; border: 1px solid #2563eb; }
.tag-custom  { background: #1a0a2e; color: #c084fc; border: 1px solid #7c3aed; }

/* ── AGENT CHAT ── */
.agent-message {
    display: flex; gap: 14px;
    padding: 16px 20px;
    border-radius: 12px;
    margin-bottom: 12px;
    border: 1px solid #1e3a6e;
    background: #07112b;
    animation: fadeIn 0.4s ease;
}
@keyframes fadeIn { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: none; } }
.agent-avatar {
    width: 38px; height: 38px; border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem; flex-shrink: 0;
    font-weight: 700;
}
.agent-name { font-family: 'Montserrat', sans-serif; font-size: 0.78rem; font-weight: 700; letter-spacing: 0.05em; margin-bottom: 6px; }
.agent-text { font-size: 0.88rem; line-height: 1.65; color: #c8d4e8; }

/* ── REPORT ── */
.report-section {
    background: #07112b;
    border: 1px solid #1e3a6e;
    border-radius: 14px;
    padding: 28px 32px;
    margin-bottom: 20px;
}
.report-header {
    font-family: 'Montserrat', sans-serif;
    font-size: 0.7rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.15em;
    color: #5a7ab5; margin-bottom: 20px;
    padding-bottom: 12px; border-bottom: 1px solid #1e3a6e;
    display: flex; justify-content: space-between; align-items: center;
}
.decision-badge {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 6px 16px; border-radius: 20px;
    font-family: 'Montserrat', sans-serif;
    font-size: 0.78rem; font-weight: 700;
    letter-spacing: 0.06em; text-transform: uppercase;
}
.badge-go    { background: #052e16; color: #22c55e; border: 1px solid #16a34a; }
.badge-wait  { background: #1c1003; color: #fbbf24; border: 1px solid #d97706; }
.badge-stop  { background: #2d0a0a; color: #ef4444; border: 1px solid #dc2626; }

/* ── BUTTONS ── */
.stButton > button {
    background: linear-gradient(135deg, #1e40af, #2563eb) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Montserrat', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.04em !important;
    padding: 12px 28px !important;
    transition: all 0.2s !important;
    box-shadow: 0 4px 16px rgba(37,99,235,0.3) !important;
}
.stButton > button:hover {
    box-shadow: 0 6px 24px rgba(37,99,235,0.5) !important;
    transform: translateY(-1px) !important;
}

/* ── UPLOAD ZONE ── */
[data-testid="stFileUploader"] {
    background: #07112b !important;
    border: 1.5px dashed #1e3a6e !important;
    border-radius: 12px !important;
    padding: 20px !important;
}

/* ── SELECTBOX / SLIDER ── */
[data-testid="stSelectbox"] > div, [data-testid="stMultiSelect"] > div {
    background: #07112b !important;
    border-color: #1e3a6e !important;
    border-radius: 8px !important;
}
.stSlider [data-testid="stThumbValue"] { color: #60a5fa !important; }

/* ── PLOTLY CHARTS ── */
.js-plotly-plot { border-radius: 12px; overflow: hidden; }

/* ── TABLES ── */
[data-testid="stDataFrame"] { border-radius: 12px; overflow: hidden; border: 1px solid #1e3a6e; }

/* ── EXPANDER ── */
[data-testid="stExpander"] {
    background: #07112b !important;
    border: 1px solid #1e3a6e !important;
    border-radius: 12px !important;
}

/* ── ALERT BOXES ── */
.alert-box {
    border-radius: 10px; padding: 14px 18px;
    font-size: 0.85rem; margin-bottom: 12px;
    border-left: 4px solid;
}
.alert-danger { background: #1a0505; border-color: #dc2626; color: #fca5a5; }
.alert-warning { background: #1a1005; border-color: #d97706; color: #fcd34d; }
.alert-success { background: #051a0a; border-color: #16a34a; color: #86efac; }
.alert-info { background: #050e28; border-color: #2563eb; color: #93c5fd; }

/* ── STATUS PILL ── */
.status-pill {
    display: inline-flex; align-items: center; gap: 5px;
    padding: 3px 10px; border-radius: 20px;
    font-size: 0.7rem; font-weight: 600;
}
.pill-ok   { background: #052e16; color: #22c55e; }
.pill-warn { background: #1c1003; color: #fbbf24; }
.pill-crit { background: #2d0a0a; color: #ef4444; }

/* ── DIVIDER ── */
hr { border-color: #1e3a6e !important; margin: 24px 0 !important; }

/* ── HIDE STREAMLIT DEFAULT ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem !important; padding-bottom: 2rem !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────
def strip_ansi(text: str) -> str:
    return re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', text or "")

def fmt_num(n, prefix="", suffix=""):
    try:
        return f"{prefix}{n:,.0f}{suffix}"
    except Exception:
        return str(n)

CHART_THEME = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(7,17,43,0.6)",
    font=dict(family="Inter", color="#c8d4e8", size=12),
    title_font=dict(family="Montserrat", color="#f0f4ff", size=14),
    xaxis=dict(gridcolor="#1e3a6e", linecolor="#1e3a6e", zerolinecolor="#1e3a6e"),
    yaxis=dict(gridcolor="#1e3a6e", linecolor="#1e3a6e", zerolinecolor="#1e3a6e"),
    colorway=["#2563eb","#d4a017","#22c55e","#ef4444","#a855f7","#06b6d4"],
    margin=dict(l=40, r=20, t=50, b=40),
)

AGENT_META = {
    "Marketing":  {"emoji": "📢", "color": "#2563eb", "bg": "#071428"},
    "Ventes":     {"emoji": "🤝", "color": "#d4a017", "bg": "#1a1003"},
    "Supply":     {"emoji": "🏗️", "color": "#22c55e", "bg": "#051a0a"},
    "Achats":     {"emoji": "📦", "color": "#a855f7", "bg": "#130a28"},
    "Finance":    {"emoji": "💰", "color": "#06b6d4", "bg": "#041420"},
    "Rapport":    {"emoji": "🏆", "color": "#f59e0b", "bg": "#1a1003"},
}

class StreamlitCapture:
    def __init__(self): self.buf = []
    def write(self, t):
        clean = strip_ansi(t)
        if clean.strip(): self.buf.append(clean)
    def flush(self): pass
    def getvalue(self): return "".join(self.buf)

# ─────────────────────────────────────────────
#  SESSION STATE INIT
# ─────────────────────────────────────────────
for k, v in {
    "page": "dashboard",
    "run_done": False,
    "outputs": {},
    "df_mkt": None, "df_prod": None, "df_fin": None,
    "df_mkt_sim": None, "df_prod_sim": None, "df_fin_sim": None,
    "contexte_sim": "SITUATION NORMALE",
    "scenario_type": "Nominal",
    "selected_prod": "Tous les produits",
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    # Logo AlBrain
    st.markdown("""
    <div class="albrain-header">
      <div class="albrain-logo-box">AL</div>
      <div class="albrain-title">
        <div class="brand">ALBRAIN</div>
        <div class="sub">Consulting</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### Chargement des données")
    uploaded_file = st.file_uploader(
        "Fichier SOP_Data.xlsx",
        type=["xlsx"],
        help="Onglets requis : Demande · Production · Finance_Achats"
    )

    with st.expander("Format requis", expanded=False):
        st.markdown("""
**Onglet Demande**
`Produit` · `Forecast` · `Sales_Orders`

**Onglet Production**
`Produit` · `Capacity` · `Stock_Level` · `Machine_Status`

**Onglet Finance_Achats**
`Produit` · `Material_Cost` · `Margin_Unit` · `Supplier_LeadTime`
        """)

    st.markdown("---")
    if st.session_state["df_mkt"] is not None:
        df_mkt = st.session_state["df_mkt"]
        produits = ["Tous les produits"] + list(df_mkt["Produit"].unique())
        st.session_state["selected_prod"] = st.selectbox("Filtrer par produit", produits)

    st.markdown("---")
    st.markdown("""
    <div style="font-size:0.7rem; color:#2a4a7a; text-align:center; padding: 8px 0;">
    AlBrain Consulting © 2025<br>
    S&OP Intelligence Platform v2.0
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  CHARGEMENT DONNÉES
# ─────────────────────────────────────────────
if uploaded_file is not None:
    try:
        xls = pd.ExcelFile(uploaded_file)
        df_mkt  = pd.read_excel(xls, "Demande")
        df_prod = pd.read_excel(xls, "Production")
        df_fin  = pd.read_excel(xls, "Finance_Achats")
        for df in [df_mkt, df_prod, df_fin]:
            df.columns = df.columns.str.strip()
        # Colonnes de compatibilité
        if "Forecast" not in df_mkt.columns and "Forecast" in df_mkt.columns:
            df_mkt["Forecast"] = df_mkt["Forecast"]
        st.session_state.update({
            "df_mkt": df_mkt, "df_prod": df_prod, "df_fin": df_fin,
            "df_mkt_sim": df_mkt.copy(), "df_prod_sim": df_prod.copy(), "df_fin_sim": df_fin.copy(),
        })
    except Exception as e:
        st.error(f"Erreur lecture fichier : {e}")
        st.stop()

data_ready = st.session_state["df_mkt"] is not None

# ─────────────────────────────────────────────
#  NAVIGATION PRINCIPALE
# ─────────────────────────────────────────────
col_n1, col_n2, col_n3, col_n4 = st.columns([1,1,1,1])
pages = [
    ("dashboard", "📊  Dashboard",   col_n1),
    ("analyse",   "🧠  Analyse IA",  col_n2),
    ("rapport",   "📄  Rapport",     col_n3),
    ("whatif",    "⚡  What-If",     col_n4),
]
for pid, label, col in pages:
    with col:
        active = "active" if st.session_state["page"] == pid else ""
        if st.button(label, key=f"nav_{pid}", use_container_width=True):
            st.session_state["page"] = pid
            st.rerun()

current_page = st.session_state["page"]

# ─────────────────────────────────────────────
#  PAGE : DASHBOARD
# ─────────────────────────────────────────────
if current_page == "dashboard":

    st.markdown("""
    <div style="margin-bottom:8px;">
      <span style="font-family:Montserrat;font-size:1.4rem;font-weight:800;color:#f0f4ff;">
        Tableau de bord S&OP
      </span>
      <span style="font-size:0.8rem;color:#5a7ab5;margin-left:12px;">
        Vue temps réel · Équilibre Offre / Demande
      </span>
    </div>
    """, unsafe_allow_html=True)

    if not data_ready:
        st.markdown("""
        <div class="alert-box alert-info">
          Chargez votre fichier <strong>SOP_Data.xlsx</strong> dans la barre latérale pour commencer.
        </div>
        """, unsafe_allow_html=True)

        # Dashboard démo vide
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="section-title">Aperçu de la plateforme</div>', unsafe_allow_html=True)
            st.markdown("""
            <div style="background:#07112b;border:1px solid #1e3a6e;border-radius:14px;padding:28px 32px;">
              <p style="color:#5a7ab5;font-size:0.9rem;line-height:1.8;">
              Cette plateforme S&OP alimentée par l'IA vous permet de :<br><br>
              ✦ &nbsp;<strong style="color:#f0f4ff;">Visualiser</strong> l'équilibre offre/demande en temps réel<br>
              ✦ &nbsp;<strong style="color:#f0f4ff;">Simuler</strong> des scénarios de crise ou de croissance<br>
              ✦ &nbsp;<strong style="color:#f0f4ff;">Orchestrer</strong> 6 agents IA spécialisés en débat structuré<br>
              ✦ &nbsp;<strong style="color:#f0f4ff;">Générer</strong> des rapports S&OP actionnables et chiffrés<br>
              </p>
            </div>
            """, unsafe_allow_html=True)
        st.stop()

    df_mkt  = st.session_state["df_mkt_sim"]
    df_prod = st.session_state["df_prod_sim"]
    df_fin  = st.session_state["df_fin_sim"]
    sel = st.session_state["selected_prod"]

    vm = df_mkt  if sel == "Tous les produits" else df_mkt[df_mkt["Produit"]  == sel]
    vp = df_prod if sel == "Tous les produits" else df_prod[df_prod["Produit"] == sel]
    vf = df_fin  if sel == "Tous les produits" else df_fin[df_fin["Produit"]   == sel]

    total_demand   = vm["Forecast"].sum()
    total_capacity = vp["Capacity"].sum()
    saturation     = (total_demand / total_capacity * 100) if total_capacity > 0 else 0
    total_profit   = (vm["Forecast"] * vf["Margin_Unit"]).sum() if "Margin_Unit" in vf.columns else 0
    stock_total    = vp["Stock_Level"].sum() if "Stock_Level" in vp.columns else 0

    # ── KPIs ──
    sat_color = "green" if saturation < 80 else ("gold" if saturation < 95 else "red")
    st.markdown(f"""
    <div class="kpi-grid">
      <div class="kpi-card blue">
        <div class="kpi-label">Demande totale</div>
        <div class="kpi-value">{total_demand:,.0f}</div>
        <div class="kpi-delta neutral">unités · forecast consolidé</div>
      </div>
      <div class="kpi-card blue">
        <div class="kpi-label">Capacité totale</div>
        <div class="kpi-value">{total_capacity:,.0f}</div>
        <div class="kpi-delta neutral">unités · capacité déclarée</div>
      </div>
      <div class="kpi-card {sat_color}">
        <div class="kpi-label">Taux de saturation</div>
        <div class="kpi-value">{saturation:.1f}%</div>
        <div class="kpi-delta {'up' if saturation>95 else ('neutral' if saturation<80 else 'down')}">
          {'⚠ Surcharge critique' if saturation>95 else ('✓ Nominal' if saturation<80 else '△ Tension détectée')}
        </div>
      </div>
      <div class="kpi-card gold">
        <div class="kpi-label">Profit prévisionnel</div>
        <div class="kpi-value">{total_profit:,.0f} €</div>
        <div class="kpi-delta neutral">marge × forecast</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Alertes automatiques ──
    ruptures = df_prod[df_prod["Capacity"] < df_mkt["Forecast"]] if len(df_prod) == len(df_mkt) else pd.DataFrame()
    goulots  = df_prod[df_prod.get("Machine_Status", pd.Series(dtype=str)) == "Goulot"] if "Machine_Status" in df_prod.columns else pd.DataFrame()

    if not ruptures.empty:
        for _, r in ruptures.iterrows():
            st.markdown(f'<div class="alert-box alert-danger">🔴 <strong>{r["Produit"]}</strong> — Capacité insuffisante : demande dépasse la capacité de {r["Forecast"] - r["Capacity"]:,.0f} unités</div>', unsafe_allow_html=True)
    if not goulots.empty:
        for _, r in goulots.iterrows():
            st.markdown(f'<div class="alert-box alert-warning">⚠️ <strong>{r["Produit"]}</strong> — Goulot détecté sur la ligne de production</div>', unsafe_allow_html=True)

    # ── Graphiques ──
    col_g1, col_g2 = st.columns([3, 2])

    with col_g1:
        st.markdown('<div class="section-title">Équilibre Offre / Demande</div>', unsafe_allow_html=True)
        fig_bal = go.Figure()
        fig_bal.add_trace(go.Bar(
            x=vp["Produit"], y=vp["Capacity"],
            name="Capacité", marker_color="#1e3a6e",
            marker_line_color="#2563eb", marker_line_width=1.5,
        ))
        fig_bal.add_trace(go.Bar(
            x=vm["Produit"], y=vm["Forecast"],
            name="Demande", marker_color="#ef4444",
            opacity=0.85, width=0.4,
        ))
        fig_bal.update_layout(
            **CHART_THEME, barmode="overlay", height=320,
            legend=dict(orientation="h", y=1.08, bgcolor="rgba(0,0,0,0)"),
        )
        st.plotly_chart(fig_bal, use_container_width=True)

    with col_g2:
        st.markdown('<div class="section-title">Répartition de la marge</div>', unsafe_allow_html=True)
        if "Margin_Unit" in vf.columns:
            df_m = pd.merge(vm, vf, on="Produit")
            df_m["Marge_Totale"] = df_m["Forecast"] * df_m["Margin_Unit"]
            fig_pie = px.pie(
                df_m, names="Produit", values="Marge_Totale",
                hole=0.55, color_discrete_sequence=["#2563eb","#d4a017","#22c55e","#ef4444","#a855f7"],
            )
            fig_pie.update_layout(**CHART_THEME, height=320, showlegend=True,
                legend=dict(orientation="v", x=1, bgcolor="rgba(0,0,0,0)"))
            fig_pie.update_traces(textposition="inside", textinfo="percent+label",
                textfont_color="white", textfont_size=11)
            st.plotly_chart(fig_pie, use_container_width=True)

    # ── Tableau de synthèse ──
    st.markdown('<div class="section-title">Tableau de pilotage produit</div>', unsafe_allow_html=True)
    df_table = pd.merge(vm[["Produit","Forecast"]], vp[["Produit","Capacity"]], on="Produit", how="outer")
    if "Stock_Level" in vp.columns:
        df_table = pd.merge(df_table, vp[["Produit","Stock_Level"]], on="Produit", how="left")
    if "Margin_Unit" in vf.columns:
        df_table = pd.merge(df_table, vf[["Produit","Margin_Unit"]], on="Produit", how="left")
        df_table["Profit (€)"] = df_table["Forecast"] * df_table["Margin_Unit"]
    if "Capacity" in df_table.columns and "Forecast" in df_table.columns:
        df_table["Saturation %"] = (df_table["Forecast"] / df_table["Capacity"] * 100).round(1)
        df_table["Statut"] = df_table["Saturation %"].apply(
            lambda x: "🟢 Nominal" if x < 80 else ("🟡 Tension" if x < 95 else "🔴 Critique")
        )
    st.dataframe(df_table.style.format({
        "Forecast": "{:,.0f}", "Capacity": "{:,.0f}",
        "Profit (€)": "{:,.0f} €", "Saturation %": "{:.1f}%",
    }), use_container_width=True, hide_index=True)

# ─────────────────────────────────────────────
#  PAGE : ANALYSE IA
# ─────────────────────────────────────────────
elif current_page == "analyse":

    st.markdown("""
    <div style="margin-bottom:8px;">
      <span style="font-family:Montserrat;font-size:1.4rem;font-weight:800;color:#f0f4ff;">
        Analyse multi-agents
      </span>
      <span style="font-size:0.8rem;color:#5a7ab5;margin-left:12px;">
        6 agents IA en débat structuré · Décision collaborative
      </span>
    </div>
    """, unsafe_allow_html=True)

    if not data_ready:
        st.markdown('<div class="alert-box alert-info">Chargez votre fichier Excel pour activer l\'analyse IA.</div>', unsafe_allow_html=True)
        st.stop()

    df_mkt  = st.session_state["df_mkt_sim"]
    df_prod = st.session_state["df_prod_sim"]
    df_fin  = st.session_state["df_fin_sim"]
    sel     = st.session_state["selected_prod"]
    contexte = st.session_state["contexte_sim"]

    # Scénario actif
    sc_type = st.session_state.get("scenario_type", "Nominal")
    sc_colors = {"Nominal":"tag-nominal","Crise":"tag-crisis","Pic":"tag-peak","Personnalisé":"tag-custom"}
    st.markdown(f"""
    <div class="scenario-card">
      <span class="scenario-tag {sc_colors.get(sc_type,'tag-nominal')}">{sc_type}</span>
      <div style="font-family:Montserrat;font-weight:700;color:#f0f4ff;font-size:0.95rem;margin-bottom:6px;">
        Scénario actif : {contexte}
      </div>
      <div style="font-size:0.82rem;color:#5a7ab5;">
        Produit analysé : <strong style="color:#93b4d8;">{sel}</strong>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Filtrage données
    vm = df_mkt  if sel == "Tous les produits" else df_mkt[df_mkt["Produit"]  == sel]
    vp = df_prod if sel == "Tous les produits" else df_prod[df_prod["Produit"] == sel]
    vf = df_fin  if sel == "Tous les produits" else df_fin[df_fin["Produit"]   == sel]
    focus = "l'ensemble du catalogue" if sel == "Tous les produits" else f"le produit {sel}"

    col_btn, col_info = st.columns([2, 3])
    with col_btn:
        launch = st.button(f"🚀  Lancer l'analyse IA", use_container_width=True)
    with col_info:
        st.markdown("""
        <div style="font-size:0.8rem;color:#5a7ab5;padding:12px 0;">
        Les 6 agents vont débattre séquentiellement.<br>
        Durée estimée : 60–120 secondes selon le LLM.
        </div>
        """, unsafe_allow_html=True)

    if launch:
        capture = StreamlitCapture()
        sys.stdout = capture
        progress_bar = st.progress(0, text="Initialisation des agents…")
        status_placeholder = st.empty()
        results_placeholder = st.container()

        try:
            txt_m = vm.to_string(index=False)
            txt_p = vp.to_string(index=False)
            txt_f = vf.to_string(index=False)

            tasks_def = [
                (SOP.marketing,  "Marketing",
                 f"Analyse la Demande pour {focus}. Données : {txt_m}. "
                 f"Identifie les produits à fort potentiel, les tendances et les risques marché. "
                 f"Donne 3 recommandations prioritaires numérotées.",
                 "Analyse marketing avec 3 recommandations."),
                (SOP.sales, "Ventes",
                 f"Valide les volumes commerciaux pour {focus}. Données : {txt_m}. "
                 f"Compare Forecast vs Sales_Orders. Signale les écarts > 15% et propose des actions correctives.",
                 "Analyse commerciale avec actions."),
                (SOP.supply, "Supply",
                 f"Analyse les contraintes de production pour {focus}. Données : {txt_p}. "
                 f"Identifie chaque goulot, la cause probable et une solution chiffrée (ex: +X heures sup = +Y unités).",
                 "Plan supply avec solutions chiffrées."),
                (SOP.purchasing, "Achats",
                 f"Évalue les risques fournisseurs pour {focus}. Données : {txt_f}. "
                 f"Classe les fournisseurs par niveau de risque. Propose un plan d'action pour les lead times > 45j.",
                 "Analyse risques achats."),
                (SOP.finance, "Finance",
                 f"Calcule la rentabilité pour {focus}. Données : {txt_f}. "
                 f"Profit total = Volume × Marge. Donne le ROI du plan et l'impact sur le cash-flow. "
                 f"Contexte : {contexte}.",
                 "Analyse financière chiffrée."),
                (SOP.orchestrator, "Rapport",
                 f"""Rédige le rapport S&OP final pour {focus}. Contexte : {contexte}.
Applique OBLIGATOIREMENT cette structure :

## 1. SYNTHÈSE EXÉCUTIVE
Résume la situation en 3 lignes max.

## 2. ANALYSE OFFRE / DEMANDE
Points bloquants identifiés par Supply et Marketing.

## 3. IMPACT FINANCIER
Chiffrage précis basé sur les données Finance.

## 4. TABLEAU DE DÉCISION
| Produit | Décision | Action | Responsable | Délai | Impact Marge |
|---------|----------|--------|-------------|-------|-------------|
(remplis ce tableau pour chaque produit analysé)

## 5. RECOMMANDATION FINALE
Feu vert / Réserves / Veto avec conditions précises.""",
                 "Rapport S&OP structuré en 5 sections avec tableau."),
            ]

            tasks = []
            for agent, name, desc, expected in tasks_def:
                tasks.append(Task(description=desc, agent=agent, expected_output=expected))

            crew = Crew(
                agents=[SOP.marketing, SOP.sales, SOP.supply,
                        SOP.purchasing, SOP.finance, SOP.orchestrator],
                tasks=tasks,
                memory=False, cache=False, verbose=True,
            )

            agent_names = ["Marketing","Ventes","Supply","Achats","Finance","Rapport"]
            for i, name in enumerate(agent_names):
                progress_bar.progress((i+1)/7, text=f"Agent {name} en cours…")
                status_placeholder.markdown(
                    f'<div class="alert-box alert-info">🔄 Agent <strong>{name}</strong> analyse les données…</div>',
                    unsafe_allow_html=True
                )

            crew.kickoff()
            progress_bar.progress(1.0, text="Analyse terminée ✓")
            status_placeholder.empty()

            outputs = {}
            labels  = ["Marketing","Ventes","Supply","Achats","Finance","Rapport"]
            for i, t in enumerate(tasks):
                outputs[labels[i]] = t.output.raw if t.output else "Aucune réponse."

            st.session_state["outputs"]  = outputs
            st.session_state["run_done"] = True

        except Exception as e:
            st.error(f"Erreur IA : {e}")
            progress_bar.empty()
        finally:
            sys.stdout = sys.__stdout__

    # ── Affichage des résultats ──
    if st.session_state.get("run_done") and st.session_state["outputs"]:
        st.markdown('<div class="section-title">Résultats du débat inter-agents</div>', unsafe_allow_html=True)

        outputs = st.session_state["outputs"]
        for agent_key, content in outputs.items():
            if agent_key == "Rapport":
                continue
            meta = AGENT_META.get(agent_key, {"emoji":"🤖","color":"#5a7ab5","bg":"#07112b"})
            st.markdown(f"""
            <div class="agent-message">
              <div class="agent-avatar" style="background:{meta['bg']};border:1.5px solid {meta['color']};color:{meta['color']};">
                {meta['emoji']}
              </div>
              <div style="flex:1">
                <div class="agent-name" style="color:{meta['color']};">{agent_key.upper()}</div>
                <div class="agent-text">{content.replace(chr(10),'<br>')}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  PAGE : RAPPORT FINAL
# ─────────────────────────────────────────────
elif current_page == "rapport":

    st.markdown("""
    <div style="margin-bottom:8px;">
      <span style="font-family:Montserrat;font-size:1.4rem;font-weight:800;color:#f0f4ff;">
        Rapport S&OP Final
      </span>
      <span style="font-size:0.8rem;color:#5a7ab5;margin-left:12px;">
        Synthèse exécutive · Plan d'action · Décisions
      </span>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.get("run_done"):
        st.markdown("""
        <div class="alert-box alert-warning">
          Lancez d'abord l'analyse IA depuis l'onglet <strong>Analyse IA</strong>.
        </div>
        """, unsafe_allow_html=True)
        st.stop()

    outputs = st.session_state["outputs"]
    rapport = outputs.get("Rapport", "Rapport non disponible.")
    now     = datetime.now().strftime("%d %B %Y — %H:%M")
    sel     = st.session_state["selected_prod"]
    contexte = st.session_state["contexte_sim"]

    # Header rapport
    st.markdown(f"""
    <div class="report-section">
      <div class="report-header">
        <span>RAPPORT S&OP · AlBrain Consulting · {now}</span>
        <span style="color:#5a7ab5;">Produit : {sel} · Scénario : {contexte}</span>
      </div>
      <div style="font-size:0.9rem;line-height:1.8;color:#c8d4e8;">
        {rapport.replace(chr(10),'<br>')}
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Rapports agents détaillés
    st.markdown('<div class="section-title">Rapports détaillés par département</div>', unsafe_allow_html=True)
    dept_labels = {
        "Marketing": ("📢 Marketing","Analyse de la demande"),
        "Ventes":    ("🤝 Ventes","Validation commerciale"),
        "Supply":    ("🏗️ Supply","Plan de production"),
        "Achats":    ("📦 Achats","Risques fournisseurs"),
        "Finance":   ("💰 Finance","Impact financier"),
    }
    for key, (label, subtitle) in dept_labels.items():
        if key in outputs:
            with st.expander(f"{label} — {subtitle}", expanded=False):
                st.markdown(outputs[key])

    # Export
    st.markdown('<div class="section-title">Export</div>', unsafe_allow_html=True)
    col_e1, col_e2 = st.columns(2)
    with col_e1:
        full_text = f"RAPPORT S&OP — AlBrain Consulting\n{now}\n\n"
        full_text += f"Produit : {sel} | Scénario : {contexte}\n\n"
        full_text += "=" * 60 + "\n\nRAPPORT FINAL\n" + "=" * 60 + "\n\n" + rapport + "\n\n"
        for k, v in outputs.items():
            if k != "Rapport":
                full_text += f"\n{'='*60}\n{k.upper()}\n{'='*60}\n{v}\n"
        st.download_button(
            "⬇️  Télécharger le rapport (.txt)",
            data=full_text.encode("utf-8"),
            file_name=f"rapport_sop_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain",
            use_container_width=True,
        )
    with col_e2:
        csv_data = pd.DataFrame([
            {"Section": k, "Contenu": v} for k, v in outputs.items()
        ]).to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️  Télécharger en CSV",
            data=csv_data,
            file_name=f"sop_outputs_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
            use_container_width=True,
        )

# ─────────────────────────────────────────────
#  PAGE : WHAT-IF
# ─────────────────────────────────────────────
elif current_page == "whatif":

    st.markdown("""
    <div style="margin-bottom:8px;">
      <span style="font-family:Montserrat;font-size:1.4rem;font-weight:800;color:#f0f4ff;">
        Simulateur What-If
      </span>
      <span style="font-size:0.8rem;color:#5a7ab5;margin-left:12px;">
        Modélisez l'impact de chaque scénario avant de décider
      </span>
    </div>
    """, unsafe_allow_html=True)

    if not data_ready:
        st.markdown('<div class="alert-box alert-info">Chargez votre fichier Excel pour activer le simulateur.</div>', unsafe_allow_html=True)
        st.stop()

    df_mkt_base  = st.session_state["df_mkt"].copy()
    df_prod_base = st.session_state["df_prod"].copy()
    df_fin_base  = st.session_state["df_fin"].copy()

    # Sélection scénario
    st.markdown('<div class="section-title">Sélection du scénario</div>', unsafe_allow_html=True)
    sc_col1, sc_col2, sc_col3, sc_col4 = st.columns(4)
    scenario_buttons = [
        ("sc_nominal",     "🟢 Nominal",         sc_col1),
        ("sc_crisis",      "🔴 Aléa production",  sc_col2),
        ("sc_peak",        "🔵 Pic de demande",   sc_col3),
        ("sc_custom",      "🟣 Personnalisé",     sc_col4),
    ]
    for k, label, col in scenario_buttons:
        with col:
            if st.button(label, key=k, use_container_width=True):
                st.session_state["active_scenario"] = k

    active_sc = st.session_state.get("active_scenario", "sc_nominal")

    df_mkt_sim  = df_mkt_base.copy()
    df_prod_sim = df_prod_base.copy()
    df_fin_sim  = df_fin_base.copy()
    contexte_sim = "SITUATION NORMALE"
    scenario_type = "Nominal"

    st.markdown('<div class="section-title">Paramètres du scénario</div>', unsafe_allow_html=True)

    if active_sc == "sc_nominal":
        st.markdown('<div class="alert-box alert-success">✓ Scénario nominal — aucune perturbation appliquée.</div>', unsafe_allow_html=True)
        scenario_type = "Nominal"
        contexte_sim  = "SITUATION NORMALE"

    elif active_sc == "sc_crisis":
        scenario_type = "Crise"
        with st.container():
            st.markdown('<div class="scenario-card"><span class="scenario-tag tag-crisis">Aléa Production</span></div>', unsafe_allow_html=True)
            col_p1, col_p2 = st.columns(2)
            with col_p1:
                pct_cap = st.slider("Baisse de capacité (%)", 10, 90, 30, key="sl_cap")
            with col_p2:
                pct_stock = st.slider("Réduction stock de sécurité (%)", 0, 60, 20, key="sl_stock")
            produit_touche = st.selectbox("Produit impacté", ["Tous"] + list(df_prod_base["Produit"].unique()), key="crisis_prod")

        if produit_touche == "Tous":
            df_prod_sim["Capacity"] = df_prod_base["Capacity"] * (1 - pct_cap / 100)
        else:
            mask = df_prod_sim["Produit"] == produit_touche
            df_prod_sim.loc[mask, "Capacity"] = df_prod_base.loc[mask, "Capacity"] * (1 - pct_cap / 100)
        if "Stock_Level" in df_prod_sim.columns:
            df_prod_sim["Stock_Level"] = df_prod_base["Stock_Level"] * (1 - pct_stock / 100)
        contexte_sim = f"CRISE PRODUCTION : Capacité réduite de {pct_cap}%, stock réduit de {pct_stock}% sur {produit_touche}."

    elif active_sc == "sc_peak":
        scenario_type = "Pic"
        st.markdown('<div class="scenario-card"><span class="scenario-tag tag-peak">Pic de demande</span></div>', unsafe_allow_html=True)
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            pct_dem = st.slider("Hausse de la demande (%)", 10, 200, 50, key="sl_dem")
        with col_p2:
            region_options = ["Tous les segments", "B2B", "B2C"]
            segment = st.selectbox("Segment impacté", region_options, key="peak_seg")
        df_mkt_sim["Forecast"] = df_mkt_base["Forecast"] * (1 + pct_dem / 100)
        contexte_sim = f"PIC DEMANDE : Hausse de {pct_dem}% — segment {segment}."

    elif active_sc == "sc_custom":
        scenario_type = "Personnalisé"
        st.markdown('<div class="scenario-card"><span class="scenario-tag tag-custom">Scénario personnalisé</span></div>', unsafe_allow_html=True)
        col_c1, col_c2, col_c3 = st.columns(3)
        with col_c1:
            delta_demand = st.number_input("Δ Demande (%)", -80, 300, 0, step=5, key="c_dem")
        with col_c2:
            delta_cap = st.number_input("Δ Capacité (%)", -80, 100, 0, step=5, key="c_cap")
        with col_c3:
            delta_marge = st.number_input("Δ Marge unitaire (%)", -50, 100, 0, step=5, key="c_mar")
        evt_desc = st.text_area("Description de l'événement", placeholder="Ex: Grève des dockers, nouveau concurrent, rupture matière première…", key="c_desc")

        if delta_demand != 0:
            df_mkt_sim["Forecast"] = df_mkt_base["Forecast"] * (1 + delta_demand / 100)
        if delta_cap != 0:
            df_prod_sim["Capacity"] = df_prod_base["Capacity"] * (1 + delta_cap / 100)
        if delta_marge != 0 and "Margin_Unit" in df_fin_sim.columns:
            df_fin_sim["Margin_Unit"] = df_fin_base["Margin_Unit"] * (1 + delta_marge / 100)
        contexte_sim = f"ÉVÉNEMENT PERSONNALISÉ : {evt_desc or 'Non précisé'} | Δ Demande:{delta_demand}%, Δ Capacité:{delta_cap}%, Δ Marge:{delta_marge}%"

    # ── Aperçu impact ──
    st.markdown('<div class="section-title">Impact simulé vs baseline</div>', unsafe_allow_html=True)

    dem_base = df_mkt_base["Forecast"].sum()
    dem_sim  = df_mkt_sim["Forecast"].sum()
    cap_base = df_prod_base["Capacity"].sum()
    cap_sim  = df_prod_sim["Capacity"].sum()
    mar_base = (df_mkt_base["Forecast"] * df_fin_base["Margin_Unit"]).sum() if "Margin_Unit" in df_fin_base.columns else 0
    mar_sim  = (df_mkt_sim["Forecast"]  * df_fin_sim["Margin_Unit"]).sum()  if "Margin_Unit" in df_fin_sim.columns  else 0

    delta_d = dem_sim  - dem_base
    delta_c = cap_sim  - cap_base
    delta_m = mar_sim  - mar_base

    k1, k2, k3 = st.columns(3)
    with k1:
        sign = "+" if delta_d >= 0 else ""
        col_cls = "up" if delta_d >= 0 else "down"
        st.markdown(f"""
        <div class="kpi-card blue">
          <div class="kpi-label">Demande simulée</div>
          <div class="kpi-value">{dem_sim:,.0f}</div>
          <div class="kpi-delta {col_cls}">{sign}{delta_d:,.0f} vs baseline</div>
        </div>""", unsafe_allow_html=True)
    with k2:
        sign = "+" if delta_c >= 0 else ""
        col_cls = "up" if delta_c >= 0 else "down"
        st.markdown(f"""
        <div class="kpi-card blue">
          <div class="kpi-label">Capacité simulée</div>
          <div class="kpi-value">{cap_sim:,.0f}</div>
          <div class="kpi-delta {col_cls}">{sign}{delta_c:,.0f} vs baseline</div>
        </div>""", unsafe_allow_html=True)
    with k3:
        sign = "+" if delta_m >= 0 else ""
        col_cls = "up" if delta_m >= 0 else "down"
        st.markdown(f"""
        <div class="kpi-card {'gold' if delta_m >= 0 else 'red'}">
          <div class="kpi-label">Profit simulé (€)</div>
          <div class="kpi-value">{mar_sim:,.0f}</div>
          <div class="kpi-delta {col_cls}">{sign}{delta_m:,.0f} € vs baseline</div>
        </div>""", unsafe_allow_html=True)

    # ── Graphique comparatif ──
    fig_comp = make_subplots(
        rows=1, cols=2,
        subplot_titles=["Demande : Baseline vs Simulé", "Capacité : Baseline vs Simulé"],
    )
    produits = df_mkt_base["Produit"].tolist()
    fig_comp.add_trace(go.Bar(x=produits, y=df_mkt_base["Forecast"], name="Baseline",
                              marker_color="#1e3a6e"), row=1, col=1)
    fig_comp.add_trace(go.Bar(x=produits, y=df_mkt_sim["Forecast"],  name="Simulé",
                              marker_color="#2563eb"), row=1, col=1)
    fig_comp.add_trace(go.Bar(x=df_prod_base["Produit"].tolist(), y=df_prod_base["Capacity"],
                              name="Baseline", marker_color="#1e3a6e", showlegend=False), row=1, col=2)
    fig_comp.add_trace(go.Bar(x=df_prod_sim["Produit"].tolist(),  y=df_prod_sim["Capacity"],
                              name="Simulé",   marker_color="#22c55e", showlegend=False), row=1, col=2)
    fig_comp.update_layout(**CHART_THEME, barmode="group", height=360,
                           legend=dict(orientation="h", y=1.1, bgcolor="rgba(0,0,0,0)"))
    st.plotly_chart(fig_comp, use_container_width=True)

    # Sauvegarde pour l'analyse IA
    col_apply, col_reset = st.columns([2, 1])
    with col_apply:
        if st.button("✅  Appliquer ce scénario à l'analyse IA", use_container_width=True):
            st.session_state["df_mkt_sim"]   = df_mkt_sim
            st.session_state["df_prod_sim"]  = df_prod_sim
            st.session_state["df_fin_sim"]   = df_fin_sim
            st.session_state["contexte_sim"] = contexte_sim
            st.session_state["scenario_type"]= scenario_type
            st.session_state["run_done"]     = False
            st.success("✓ Scénario appliqué. Allez dans **Analyse IA** pour lancer l'analyse.")
    with col_reset:
        if st.button("↺  Réinitialiser", use_container_width=True):
            st.session_state["df_mkt_sim"]   = st.session_state["df_mkt"].copy()
            st.session_state["df_prod_sim"]  = st.session_state["df_prod"].copy()
            st.session_state["df_fin_sim"]   = st.session_state["df_fin"].copy()
            st.session_state["contexte_sim"] = "SITUATION NORMALE"
            st.session_state["scenario_type"]= "Nominal"
            st.rerun()
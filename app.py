import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import re
from datetime import datetime
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
#  CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700;800&family=Inter:wght@300;400;500;600&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #04091a; color: #e8eaf0; }
.stApp { background-color: #04091a; }
[data-testid="stSidebar"] { background: linear-gradient(180deg, #07112b 0%, #0a1a3a 100%); border-right: 1px solid #1e3a6e; }
[data-testid="stSidebar"] * { color: #c8d4e8 !important; }
.albrain-header { display: flex; align-items: center; gap: 16px; padding: 20px 24px 16px; border-bottom: 1px solid #1e3a6e; margin-bottom: 8px; }
.albrain-logo-box { width: 44px; height: 44px; border: 2.5px solid #2563eb; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-family: 'Montserrat', sans-serif; font-weight: 800; font-size: 15px; color: #2563eb; background: #071428; flex-shrink: 0; }
.albrain-title .brand { font-family: 'Montserrat', sans-serif; font-weight: 800; font-size: 1.15rem; color: #f0f4ff; }
.albrain-title .sub { font-size: 0.7rem; color: #5a7ab5; text-transform: uppercase; font-weight: 500; }
.kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 28px; }
.kpi-card { background: #07112b; border: 1px solid #1e3a6e; border-radius: 14px; padding: 20px 22px; position: relative; overflow: hidden; }
.kpi-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; border-radius: 14px 14px 0 0; }
.kpi-card.blue::before { background: #2563eb; } .kpi-card.gold::before { background: #d4a017; }
.kpi-card.green::before { background: #16a34a; } .kpi-card.red::before { background: #dc2626; }
.kpi-label { font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.1em; color: #5a7ab5; font-weight: 600; margin-bottom: 8px; }
.kpi-value { font-family: 'Montserrat', sans-serif; font-size: 1.9rem; font-weight: 700; color: #f0f4ff; line-height: 1; }
.kpi-delta { font-size: 0.75rem; margin-top: 6px; font-weight: 500; }
.kpi-delta.up { color: #22c55e; } .kpi-delta.down { color: #ef4444; } .kpi-delta.neutral { color: #5a7ab5; }
.section-title { font-family: 'Montserrat', sans-serif; font-weight: 700; font-size: 1.05rem; color: #f0f4ff; margin: 28px 0 16px; display: flex; align-items: center; gap: 10px; }
.section-title::after { content: ''; flex: 1; height: 1px; background: linear-gradient(90deg, #1e3a6e, transparent); }
.scenario-card { background: #07112b; border: 1px solid #1e3a6e; border-radius: 14px; padding: 22px 24px; margin-bottom: 20px; }
.scenario-tag { display: inline-block; padding: 3px 12px; border-radius: 20px; font-size: 0.72rem; font-weight: 600; text-transform: uppercase; margin-bottom: 12px; }
.tag-nominal { background: #052e16; color: #22c55e; border: 1px solid #16a34a; }
.tag-crisis  { background: #2d0a0a; color: #ef4444; border: 1px solid #dc2626; }
.tag-peak    { background: #0c1a4a; color: #60a5fa; border: 1px solid #2563eb; }
.tag-custom  { background: #1a0a2e; color: #c084fc; border: 1px solid #7c3aed; }
.agent-message { display: flex; gap: 14px; padding: 16px 20px; border-radius: 12px; margin-bottom: 12px; border: 1px solid #1e3a6e; background: #07112b; }
.agent-avatar { width: 38px; height: 38px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 1.1rem; flex-shrink: 0; }
.agent-name { font-family: 'Montserrat', sans-serif; font-size: 0.78rem; font-weight: 700; letter-spacing: 0.05em; margin-bottom: 6px; }
.agent-text { font-size: 0.88rem; line-height: 1.65; color: #c8d4e8; }
.report-section { background: #07112b; border: 1px solid #1e3a6e; border-radius: 14px; padding: 28px 32px; margin-bottom: 20px; }
.report-header { font-family: 'Montserrat', sans-serif; font-size: 0.7rem; font-weight: 700; text-transform: uppercase; color: #5a7ab5; margin-bottom: 20px; padding-bottom: 12px; border-bottom: 1px solid #1e3a6e; display: flex; justify-content: space-between; }
.alert-box { border-radius: 10px; padding: 14px 18px; font-size: 0.85rem; margin-bottom: 12px; border-left: 4px solid; }
.alert-danger  { background: #1a0505; border-color: #dc2626; color: #fca5a5; }
.alert-warning { background: #1a1005; border-color: #d97706; color: #fcd34d; }
.alert-success { background: #051a0a; border-color: #16a34a; color: #86efac; }
.alert-info    { background: #050e28; border-color: #2563eb; color: #93c5fd; }
.stButton > button { background: linear-gradient(135deg, #1e40af, #2563eb) !important; color: white !important; border: none !important; border-radius: 10px !important; font-family: 'Montserrat', sans-serif !important; font-weight: 600 !important; padding: 12px 28px !important; }
hr { border-color: #1e3a6e !important; margin: 24px 0 !important; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem !important; }
</style>
""", unsafe_allow_html=True)

CHART_THEME = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(7,17,43,0.6)",
    font=dict(family="Inter", color="#c8d4e8", size=12),
    title_font=dict(family="Montserrat", color="#f0f4ff", size=14),
    xaxis=dict(gridcolor="#1e3a6e", linecolor="#1e3a6e"),
    yaxis=dict(gridcolor="#1e3a6e", linecolor="#1e3a6e"),
    colorway=["#2563eb","#d4a017","#22c55e","#ef4444","#a855f7","#06b6d4"],
    margin=dict(l=40, r=20, t=50, b=40),
)

AGENT_META = {
    "Marketing": {"emoji": "📢", "color": "#2563eb", "bg": "#071428"},
    "Ventes":    {"emoji": "🤝", "color": "#d4a017", "bg": "#1a1003"},
    "Supply":    {"emoji": "🏗️", "color": "#22c55e", "bg": "#051a0a"},
    "Achats":    {"emoji": "📦", "color": "#a855f7", "bg": "#130a28"},
    "Finance":   {"emoji": "💰", "color": "#06b6d4", "bg": "#041420"},
    "Rapport":   {"emoji": "🏆", "color": "#f59e0b", "bg": "#1a1003"},
}

# ─────────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────────
for k, v in {
    "page": "dashboard", "run_done": False, "outputs": {},
    "df_mkt": None, "df_prod": None, "df_fin": None,
    "df_mkt_sim": None, "df_prod_sim": None, "df_fin_sim": None,
    "contexte_sim": "SITUATION NORMALE", "scenario_type": "Nominal",
    "selected_prod": "Tous les produits",
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="albrain-header">
      <div class="albrain-logo-box">AL</div>
      <div class="albrain-title">
        <div class="brand">ALBRAIN</div>
        <div class="sub">Consulting</div>
      </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("#### Chargement des données")
    uploaded_file = st.file_uploader("Fichier SOP_Data.xlsx", type=["xlsx"],
        help="Onglets requis : Demande · Production · Finance_Achats")

    with st.expander("Format requis", expanded=False):
        st.markdown("""
**Onglet Demande** : `Produit` · `Forecast` · `Sales_Orders`
**Onglet Production** : `Produit` · `Capacity` · `Stock_Level` · `Machine_Status`
**Onglet Finance_Achats** : `Produit` · `Material_Cost` · `Margin_Unit` · `Supplier_LeadTime`
        """)

    st.markdown("---")
    if st.session_state["df_mkt"] is not None:
        produits = ["Tous les produits"] + list(st.session_state["df_mkt"]["Produit"].unique())
        st.session_state["selected_prod"] = st.selectbox("Filtrer par produit", produits)

    st.markdown("---")
    st.markdown('<div style="font-size:0.7rem;color:#2a4a7a;text-align:center;">AlBrain Consulting © 2025<br>S&OP Intelligence Platform v2.0</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  CHARGEMENT DONNÉES
# ─────────────────────────────────────────────
if uploaded_file is not None:
    try:
        xls = pd.ExcelFile(uploaded_file)
        df_mkt  = pd.read_excel(xls, "Demande");        df_mkt.columns  = df_mkt.columns.str.strip()
        df_prod = pd.read_excel(xls, "Production");     df_prod.columns = df_prod.columns.str.strip()
        df_fin  = pd.read_excel(xls, "Finance_Achats"); df_fin.columns  = df_fin.columns.str.strip()
        st.session_state.update({
            "df_mkt": df_mkt, "df_prod": df_prod, "df_fin": df_fin,
            "df_mkt_sim": df_mkt.copy(), "df_prod_sim": df_prod.copy(), "df_fin_sim": df_fin.copy(),
        })
    except Exception as e:
        st.error(f"Erreur lecture fichier : {e}"); st.stop()

data_ready = st.session_state["df_mkt"] is not None

# ─────────────────────────────────────────────
#  NAVIGATION
# ─────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
for pid, label, col in [("dashboard","📊 Dashboard",c1),("analyse","🧠 Analyse IA",c2),("rapport","📄 Rapport",c3),("whatif","⚡ What-If",c4)]:
    with col:
        if st.button(label, key=f"nav_{pid}", use_container_width=True):
            st.session_state["page"] = pid; st.rerun()

page = st.session_state["page"]

# ═══════════════════════════════════════════
#  DASHBOARD
# ═══════════════════════════════════════════
if page == "dashboard":
    st.markdown('<span style="font-family:Montserrat;font-size:1.4rem;font-weight:800;color:#f0f4ff;">Tableau de bord S&OP</span>', unsafe_allow_html=True)

    if not data_ready:
        st.markdown('<div class="alert-box alert-info">Chargez votre fichier <strong>SOP_Data.xlsx</strong> dans la barre latérale pour commencer.</div>', unsafe_allow_html=True)
        st.stop()

    df_mkt  = st.session_state["df_mkt_sim"]
    df_prod = st.session_state["df_prod_sim"]
    df_fin  = st.session_state["df_fin_sim"]
    sel     = st.session_state["selected_prod"]
    vm = df_mkt  if sel=="Tous les produits" else df_mkt[df_mkt["Produit"]==sel]
    vp = df_prod if sel=="Tous les produits" else df_prod[df_prod["Produit"]==sel]
    vf = df_fin  if sel=="Tous les produits" else df_fin[df_fin["Produit"]==sel]

    total_demand   = vm["Forecast"].sum() if "Forecast" in vm.columns else 0
    total_capacity = vp["Capacity"].sum() if "Capacity" in vp.columns else 0
    saturation     = (total_demand/total_capacity*100) if total_capacity>0 else 0

    if "Margin_Unit" in vf.columns and "Forecast" in vm.columns:
        df_p = pd.merge(vm[["Produit","Forecast"]], vf[["Produit","Margin_Unit"]], on="Produit", how="inner")
        total_profit = (df_p["Forecast"]*df_p["Margin_Unit"]).sum()
    else:
        total_profit = 0

    sat_color = "green" if saturation<80 else ("gold" if saturation<95 else "red")
    sat_label = "✓ Nominal" if saturation<80 else ("△ Tension" if saturation<95 else "⚠ Surcharge")
    sat_cls   = "neutral"  if saturation<80 else ("down" if saturation<95 else "up")

    st.markdown(f"""
    <div class="kpi-grid">
      <div class="kpi-card blue"><div class="kpi-label">Demande totale</div><div class="kpi-value">{total_demand:,.0f}</div><div class="kpi-delta neutral">unités · forecast</div></div>
      <div class="kpi-card blue"><div class="kpi-label">Capacité totale</div><div class="kpi-value">{total_capacity:,.0f}</div><div class="kpi-delta neutral">unités · déclarée</div></div>
      <div class="kpi-card {sat_color}"><div class="kpi-label">Taux de saturation</div><div class="kpi-value">{saturation:.1f}%</div><div class="kpi-delta {sat_cls}">{sat_label}</div></div>
      <div class="kpi-card gold"><div class="kpi-label">Profit prévisionnel</div><div class="kpi-value">{total_profit:,.0f} €</div><div class="kpi-delta neutral">marge × forecast</div></div>
    </div>""", unsafe_allow_html=True)

    # Alertes — merge sécurisé
    if "Forecast" in df_mkt.columns and "Capacity" in df_prod.columns:
        df_merged = pd.merge(df_prod[["Produit","Capacity"]], df_mkt[["Produit","Forecast"]], on="Produit", how="inner")
        for _, r in df_merged[df_merged["Capacity"]<df_merged["Forecast"]].iterrows():
            st.markdown(f'<div class="alert-box alert-danger">🔴 <strong>{r["Produit"]}</strong> — Capacité insuffisante : {r["Forecast"]-r["Capacity"]:,.0f} unités de déficit</div>', unsafe_allow_html=True)
    if "Machine_Status" in df_prod.columns:
        for _, r in df_prod[df_prod["Machine_Status"]=="Goulot"].iterrows():
            st.markdown(f'<div class="alert-box alert-warning">⚠️ <strong>{r["Produit"]}</strong> — Goulot détecté</div>', unsafe_allow_html=True)

    # Graphiques
    col_g1, col_g2 = st.columns([3,2])
    with col_g1:
        st.markdown('<div class="section-title">Équilibre Offre / Demande</div>', unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_trace(go.Bar(x=vp["Produit"], y=vp["Capacity"], name="Capacité", marker_color="#1e3a6e", marker_line_color="#2563eb", marker_line_width=1.5))
        fig.add_trace(go.Bar(x=vm["Produit"], y=vm["Forecast"], name="Demande",  marker_color="#ef4444", opacity=0.85, width=0.4))
        fig.update_layout(**CHART_THEME, barmode="overlay", height=320, legend=dict(orientation="h", y=1.08, bgcolor="rgba(0,0,0,0)"))
        st.plotly_chart(fig, use_container_width=True)
    with col_g2:
        st.markdown('<div class="section-title">Répartition de la marge</div>', unsafe_allow_html=True)
        if "Margin_Unit" in vf.columns and "Forecast" in vm.columns:
            df_m = pd.merge(vm[["Produit","Forecast"]], vf[["Produit","Margin_Unit"]], on="Produit", how="inner")
            df_m["Marge_Totale"] = df_m["Forecast"]*df_m["Margin_Unit"]
            fig2 = px.pie(df_m, names="Produit", values="Marge_Totale", hole=0.55, color_discrete_sequence=["#2563eb","#d4a017","#22c55e","#ef4444","#a855f7"])
            fig2.update_layout(**CHART_THEME, height=320)
            fig2.update_traces(textposition="inside", textinfo="percent+label", textfont_color="white", textfont_size=11)
            st.plotly_chart(fig2, use_container_width=True)

    # Tableau
    st.markdown('<div class="section-title">Tableau de pilotage</div>', unsafe_allow_html=True)
    df_t = pd.merge(vm[["Produit","Forecast"]], vp[["Produit","Capacity"]], on="Produit", how="outer")
    if "Margin_Unit" in vf.columns:
        df_t = pd.merge(df_t, vf[["Produit","Margin_Unit"]], on="Produit", how="left")
        df_t["Profit (€)"] = df_t["Forecast"]*df_t["Margin_Unit"]
    if "Capacity" in df_t.columns:
        df_t["Saturation %"] = (df_t["Forecast"]/df_t["Capacity"]*100).round(1)
        df_t["Statut"] = df_t["Saturation %"].apply(lambda x: "🟢 Nominal" if x<80 else ("🟡 Tension" if x<95 else "🔴 Critique"))
    fmt = {"Forecast":"{:,.0f}","Capacity":"{:,.0f}","Saturation %":"{:.1f}%"}
    if "Profit (€)" in df_t.columns: fmt["Profit (€)"]="{:,.0f} €"
    st.dataframe(df_t.style.format(fmt), use_container_width=True, hide_index=True)

# ═══════════════════════════════════════════
#  ANALYSE IA
# ═══════════════════════════════════════════
elif page == "analyse":
    st.markdown('<span style="font-family:Montserrat;font-size:1.4rem;font-weight:800;color:#f0f4ff;">Analyse multi-agents</span> <span style="font-size:0.8rem;color:#5a7ab5;">6 agents IA · Décision collaborative</span>', unsafe_allow_html=True)

    if not data_ready:
        st.markdown('<div class="alert-box alert-info">Chargez votre fichier Excel pour activer l\'analyse IA.</div>', unsafe_allow_html=True); st.stop()

    df_mkt  = st.session_state["df_mkt_sim"]
    df_prod = st.session_state["df_prod_sim"]
    df_fin  = st.session_state["df_fin_sim"]
    sel      = st.session_state["selected_prod"]
    contexte = st.session_state["contexte_sim"]
    sc_type  = st.session_state.get("scenario_type","Nominal")
    sc_colors = {"Nominal":"tag-nominal","Crise":"tag-crisis","Pic":"tag-peak","Personnalisé":"tag-custom"}

    st.markdown(f"""
    <div class="scenario-card">
      <span class="scenario-tag {sc_colors.get(sc_type,'tag-nominal')}">{sc_type}</span>
      <div style="font-family:Montserrat;font-weight:700;color:#f0f4ff;font-size:0.95rem;">{contexte}</div>
      <div style="font-size:0.82rem;color:#5a7ab5;">Produit : <strong style="color:#93b4d8;">{sel}</strong></div>
    </div>""", unsafe_allow_html=True)

    vm = df_mkt  if sel=="Tous les produits" else df_mkt[df_mkt["Produit"]==sel]
    vp = df_prod if sel=="Tous les produits" else df_prod[df_prod["Produit"]==sel]
    vf = df_fin  if sel=="Tous les produits" else df_fin[df_fin["Produit"]==sel]
    focus = "l'ensemble du catalogue" if sel=="Tous les produits" else f"le produit {sel}"

    col_btn, col_info = st.columns([2,3])
    with col_btn:
        launch = st.button("🚀  Lancer l'analyse IA", use_container_width=True)
    with col_info:
        st.markdown('<div style="font-size:0.8rem;color:#5a7ab5;padding:12px 0;">6 agents Groq LLM · Durée estimée : 20–40 secondes</div>', unsafe_allow_html=True)

    if launch:
        progress = st.progress(0, text="Initialisation…")
        agent_names = ["Marketing","Ventes","Supply","Achats","Finance","Rapport"]
        status_ph = st.empty()
        try:
            txt_m = vm.to_string(index=False)
            txt_p = vp.to_string(index=False)
            txt_f = vf.to_string(index=False)

            outputs = {}
            all_agents = ["Marketing","Ventes","Supply","Achats","Finance","Rapport"]
            for i, name in enumerate(all_agents):
                progress.progress((i+1)/7, text=f"Agent {name} en cours…")
                status_ph.markdown(f'<div class="alert-box alert-info">🔄 Agent <strong>{name}</strong> analyse…</div>', unsafe_allow_html=True)

            outputs = SOP.run_all_agents(txt_m, txt_p, txt_f, focus, contexte)
            progress.progress(1.0, text="Analyse terminée ✓")
            status_ph.empty()
            st.session_state["outputs"]  = outputs
            st.session_state["run_done"] = True

        except Exception as e:
            st.error(f"Erreur IA : {e}")
            progress.empty()

    if st.session_state.get("run_done") and st.session_state["outputs"]:
        st.markdown('<div class="section-title">Résultats des agents</div>', unsafe_allow_html=True)
        for agent_key, content in st.session_state["outputs"].items():
            if agent_key == "Rapport": continue
            meta = AGENT_META.get(agent_key, {"emoji":"🤖","color":"#5a7ab5","bg":"#07112b"})
            st.markdown(f"""
            <div class="agent-message">
              <div class="agent-avatar" style="background:{meta['bg']};border:1.5px solid {meta['color']};color:{meta['color']};">{meta['emoji']}</div>
              <div style="flex:1">
                <div class="agent-name" style="color:{meta['color']};">{agent_key.upper()}</div>
                <div class="agent-text">{content.replace(chr(10),'<br>')}</div>
              </div>
            </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════
#  RAPPORT
# ═══════════════════════════════════════════
elif page == "rapport":
    st.markdown('<span style="font-family:Montserrat;font-size:1.4rem;font-weight:800;color:#f0f4ff;">Rapport S&OP Final</span>', unsafe_allow_html=True)

    if not st.session_state.get("run_done"):
        st.markdown('<div class="alert-box alert-warning">Lancez d\'abord l\'analyse IA.</div>', unsafe_allow_html=True); st.stop()

    outputs  = st.session_state["outputs"]
    rapport  = outputs.get("Rapport","Rapport non disponible.")
    now      = datetime.now().strftime("%d %B %Y — %H:%M")
    sel      = st.session_state["selected_prod"]
    contexte = st.session_state["contexte_sim"]

    st.markdown(f"""
    <div class="report-section">
      <div class="report-header">
        <span>RAPPORT S&OP · AlBrain Consulting · {now}</span>
        <span style="color:#5a7ab5;">{sel} · {contexte}</span>
      </div>
      <div style="font-size:0.9rem;line-height:1.8;color:#c8d4e8;">{rapport.replace(chr(10),'<br>')}</div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="section-title">Rapports détaillés</div>', unsafe_allow_html=True)
    for key, (label, subtitle) in {"Marketing":("📢 Marketing","Demande"),"Ventes":("🤝 Ventes","Commercial"),"Supply":("🏗️ Supply","Production"),"Achats":("📦 Achats","Fournisseurs"),"Finance":("💰 Finance","Financier")}.items():
        if key in outputs:
            with st.expander(f"{label} — {subtitle}"):
                st.markdown(outputs[key])

    st.markdown('<div class="section-title">Export</div>', unsafe_allow_html=True)
    full = f"RAPPORT S&OP — AlBrain\n{now}\n{sel} | {contexte}\n\n{'='*60}\n\n{rapport}\n\n"
    full += "\n".join(f"{'='*60}\n{k.upper()}\n{'='*60}\n{v}\n" for k,v in outputs.items() if k!="Rapport")
    c1, c2 = st.columns(2)
    with c1:
        st.download_button("⬇️ Télécharger .txt", data=full.encode("utf-8"),
            file_name=f"rapport_sop_{datetime.now().strftime('%Y%m%d_%H%M')}.txt", mime="text/plain", use_container_width=True)
    with c2:
        csv = pd.DataFrame([{"Section":k,"Contenu":v} for k,v in outputs.items()]).to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Télécharger .csv", data=csv,
            file_name=f"sop_{datetime.now().strftime('%Y%m%d_%H%M')}.csv", mime="text/csv", use_container_width=True)

# ═══════════════════════════════════════════
#  WHAT-IF
# ═══════════════════════════════════════════
elif page == "whatif":
    st.markdown('<span style="font-family:Montserrat;font-size:1.4rem;font-weight:800;color:#f0f4ff;">Simulateur What-If</span>', unsafe_allow_html=True)

    if not data_ready:
        st.markdown('<div class="alert-box alert-info">Chargez votre fichier Excel.</div>', unsafe_allow_html=True); st.stop()

    df_mkt_base  = st.session_state["df_mkt"].copy()
    df_prod_base = st.session_state["df_prod"].copy()
    df_fin_base  = st.session_state["df_fin"].copy()

    st.markdown('<div class="section-title">Sélection du scénario</div>', unsafe_allow_html=True)
    s1,s2,s3,s4 = st.columns(4)
    for k, label, col in [("sc_nominal","🟢 Nominal",s1),("sc_crisis","🔴 Aléa production",s2),("sc_peak","🔵 Pic de demande",s3),("sc_custom","🟣 Personnalisé",s4)]:
        with col:
            if st.button(label, key=k, use_container_width=True):
                st.session_state["active_scenario"] = k

    active_sc     = st.session_state.get("active_scenario","sc_nominal")
    df_mkt_sim    = df_mkt_base.copy()
    df_prod_sim   = df_prod_base.copy()
    df_fin_sim    = df_fin_base.copy()
    contexte_sim  = "SITUATION NORMALE"
    scenario_type = "Nominal"

    st.markdown('<div class="section-title">Paramètres</div>', unsafe_allow_html=True)

    if active_sc == "sc_nominal":
        st.markdown('<div class="alert-box alert-success">✓ Scénario nominal — aucune perturbation.</div>', unsafe_allow_html=True)

    elif active_sc == "sc_crisis":
        scenario_type = "Crise"
        p1,p2 = st.columns(2)
        with p1: pct_cap   = st.slider("Baisse capacité (%)", 10, 90, 30, key="sl_cap")
        with p2: pct_stock = st.slider("Réduction stock (%)",  0, 60, 20, key="sl_stock")
        prod_t = st.selectbox("Produit impacté", ["Tous"]+list(df_prod_base["Produit"].unique()), key="crisis_prod")
        if prod_t == "Tous":
            df_prod_sim["Capacity"] = df_prod_base["Capacity"]*(1-pct_cap/100)
        else:
            mask = df_prod_sim["Produit"]==prod_t
            df_prod_sim.loc[mask,"Capacity"] = df_prod_base.loc[mask,"Capacity"]*(1-pct_cap/100)
        if "Stock_Level" in df_prod_sim.columns:
            df_prod_sim["Stock_Level"] = df_prod_base["Stock_Level"]*(1-pct_stock/100)
        contexte_sim = f"CRISE : Capacité -{pct_cap}%, stock -{pct_stock}% sur {prod_t}."

    elif active_sc == "sc_peak":
        scenario_type = "Pic"
        p1,p2 = st.columns(2)
        with p1: pct_dem = st.slider("Hausse demande (%)", 10, 200, 50, key="sl_dem")
        with p2: segment = st.selectbox("Segment", ["Tous","B2B","B2C"], key="peak_seg")
        df_mkt_sim["Forecast"] = df_mkt_base["Forecast"]*(1+pct_dem/100)
        contexte_sim = f"PIC : Hausse {pct_dem}% — {segment}."

    elif active_sc == "sc_custom":
        scenario_type = "Personnalisé"
        c1,c2,c3 = st.columns(3)
        with c1: dd = st.number_input("Δ Demande (%)",  -80, 300, 0, step=5, key="c_dem")
        with c2: dc = st.number_input("Δ Capacité (%)", -80, 100, 0, step=5, key="c_cap")
        with c3: dm = st.number_input("Δ Marge (%)",    -50, 100, 0, step=5, key="c_mar")
        evt = st.text_area("Description", placeholder="Ex: Grève, nouveau concurrent…", key="c_desc")
        if dd: df_mkt_sim["Forecast"]  = df_mkt_base["Forecast"]*(1+dd/100)
        if dc: df_prod_sim["Capacity"] = df_prod_base["Capacity"]*(1+dc/100)
        if dm and "Margin_Unit" in df_fin_sim.columns:
            df_fin_sim["Margin_Unit"] = df_fin_base["Margin_Unit"]*(1+dm/100)
        contexte_sim = f"CUSTOM : {evt or 'Non précisé'} | Δ D:{dd}% C:{dc}% M:{dm}%"

    # Impact
    st.markdown('<div class="section-title">Impact simulé vs baseline</div>', unsafe_allow_html=True)
    dem_base = df_mkt_base["Forecast"].sum()  if "Forecast"  in df_mkt_base.columns  else 0
    dem_sim  = df_mkt_sim["Forecast"].sum()   if "Forecast"  in df_mkt_sim.columns   else 0
    cap_base = df_prod_base["Capacity"].sum() if "Capacity"  in df_prod_base.columns else 0
    cap_sim  = df_prod_sim["Capacity"].sum()  if "Capacity"  in df_prod_sim.columns  else 0

    if "Margin_Unit" in df_fin_base.columns and "Forecast" in df_mkt_base.columns:
        pb = pd.merge(df_mkt_base[["Produit","Forecast"]], df_fin_base[["Produit","Margin_Unit"]], on="Produit", how="inner")
        ps = pd.merge(df_mkt_sim[["Produit","Forecast"]],  df_fin_sim[["Produit","Margin_Unit"]],  on="Produit", how="inner")
        mar_base = (pb["Forecast"]*pb["Margin_Unit"]).sum()
        mar_sim  = (ps["Forecast"]*ps["Margin_Unit"]).sum()
    else:
        mar_base = mar_sim = 0

    k1,k2,k3 = st.columns(3)
    for col, label, base, sim, color in [(k1,"Demande",dem_base,dem_sim,"blue"),(k2,"Capacité",cap_base,cap_sim,"blue"),(k3,"Profit (€)",mar_base,mar_sim,"gold")]:
        delta = sim-base; sign = "+" if delta>=0 else ""; cls = "up" if delta>=0 else "down"
        unit = " €" if "Profit" in label else ""
        with col:
            st.markdown(f'<div class="kpi-card {color}"><div class="kpi-label">{label} simulé</div><div class="kpi-value">{sim:,.0f}{unit}</div><div class="kpi-delta {cls}">{sign}{delta:,.0f}{unit} vs baseline</div></div>', unsafe_allow_html=True)

    fig_c = make_subplots(rows=1, cols=2, subplot_titles=["Demande","Capacité"])
    prod_m = df_mkt_base["Produit"].tolist(); prod_p = df_prod_base["Produit"].tolist()
    fig_c.add_trace(go.Bar(x=prod_m, y=df_mkt_base["Forecast"],  name="Baseline", marker_color="#1e3a6e"), row=1, col=1)
    fig_c.add_trace(go.Bar(x=prod_m, y=df_mkt_sim["Forecast"],   name="Simulé",   marker_color="#2563eb"), row=1, col=1)
    fig_c.add_trace(go.Bar(x=prod_p, y=df_prod_base["Capacity"], name="Baseline", marker_color="#1e3a6e", showlegend=False), row=1, col=2)
    fig_c.add_trace(go.Bar(x=prod_p, y=df_prod_sim["Capacity"],  name="Simulé",   marker_color="#22c55e", showlegend=False), row=1, col=2)
    fig_c.update_layout(**CHART_THEME, barmode="group", height=360, legend=dict(orientation="h", y=1.1))
    st.plotly_chart(fig_c, use_container_width=True)

    ca, cr = st.columns([2,1])
    with ca:
        if st.button("✅ Appliquer à l'analyse IA", use_container_width=True):
            st.session_state.update({
                "df_mkt_sim": df_mkt_sim, "df_prod_sim": df_prod_sim, "df_fin_sim": df_fin_sim,
                "contexte_sim": contexte_sim, "scenario_type": scenario_type, "run_done": False,
            })
            st.success("✓ Scénario appliqué. Allez dans **Analyse IA**.")
    with cr:
        if st.button("↺ Réinitialiser", use_container_width=True):
            st.session_state.update({
                "df_mkt_sim": st.session_state["df_mkt"].copy(),
                "df_prod_sim": st.session_state["df_prod"].copy(),
                "df_fin_sim": st.session_state["df_fin"].copy(),
                "contexte_sim": "SITUATION NORMALE", "scenario_type": "Nominal",
            })
            st.rerun()

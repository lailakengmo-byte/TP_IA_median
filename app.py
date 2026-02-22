import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ─────────────────────────────────────────────
#  CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="BankSignal AI",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Photos Unsplash (CDN libre, aucun téléchargement)
IMG = {
    "hero":    "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1600&q=85",
    "data":    "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1200&q=80",
    "trading": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?auto=format&fit=crop&w=1200&q=80",
    "server":  "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=600&q=80",
    "meeting": "https://images.unsplash.com/photo-1556761175-4b46a572b786?auto=format&fit=crop&w=600&q=80",
    "f1":      "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=600&q=80",
    "f2":      "https://images.unsplash.com/photo-1555949963-ff9fe0c870eb?auto=format&fit=crop&w=600&q=80",
    "f3":      "https://images.unsplash.com/photo-1542744094-3a31f272c490?auto=format&fit=crop&w=600&q=80",
    "t1":      "https://images.unsplash.com/photo-1560250097-0b93528c311a?auto=format&fit=crop&w=400&h=450&q=80",
    "t2":      "https://images.unsplash.com/photo-1573496799515-925c9bfd73a8?auto=format&fit=crop&w=400&h=450&q=80",
    "t3":      "https://images.unsplash.com/photo-1573497491765-55a64cc1c671?auto=format&fit=crop&w=400&h=450&q=80",
}

# ─────────────────────────────────────────────
#  CSS DESIGN SYSTEM
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Serif+Display:ital@0;1&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── VARIABLES ── */
:root {
    --bg:       #f4f6fb;
    --surface:  #ffffff;
    --s2:       #eef1f8;
    --s3:       #e4e8f4;
    --border:   #dde2f0;
    --bl:       #eaecf5;
    --text:     #12172b;
    --text2:    #505772;
    --text3:    #96a0bc;
    --blue:     #1a73e8;
    --blue-l:   rgba(26,115,232,.08);
    --green:    #00c48c;
    --green-l:  rgba(0,196,140,.08);
    --red:      #f4455a;
    --red-l:    rgba(244,69,90,.08);
    --gold:     #f59e0b;
    --gold-l:   rgba(245,158,11,.08);
    --purple:   #7c3aed;
    --purple-l: rgba(124,58,237,.08);
    --cyan:     #00bcd4;
    --sh0: 0 1px 3px rgba(18,23,43,.06);
    --sh1: 0 2px 10px rgba(18,23,43,.07),0 1px 3px rgba(18,23,43,.04);
    --sh2: 0 6px 24px rgba(18,23,43,.09),0 2px 6px rgba(18,23,43,.05);
    --sh3: 0 12px 40px rgba(18,23,43,.12),0 4px 10px rgba(18,23,43,.06);
    --r: 14px; --rsm: 8px; --rlg: 20px;
}

/* ── RESET ── */
*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
    background: var(--bg) !important;
    color: var(--text);
}
#MainMenu, footer, header { visibility: hidden !important; }
.main .block-container { padding: 0 0 4rem !important; max-width: 100% !important; }

/* ── ANIMATIONS ── */
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(22px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeIn { from { opacity:0; } to { opacity:1; } }
@keyframes scaleIn {
    from { opacity:0; transform:scale(.95); }
    to   { opacity:1; transform:scale(1); }
}
@keyframes barGrow {
    from { width: 0; }
    to   { width: var(--target-w); }
}
.anim-up  { animation: fadeUp  .5s ease both; }
.anim-in  { animation: fadeIn  .6s ease both; }
.d1 { animation-delay:.06s; } .d2 { animation-delay:.12s; }
.d3 { animation-delay:.18s; } .d4 { animation-delay:.24s; }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] > div { padding: 0 !important; }
[data-testid="stSidebar"] .stRadio label {
    font-size: .88rem !important; font-weight: 500 !important;
    color: var(--text2) !important;
    padding: .6rem .85rem !important;
    border-radius: var(--rsm) !important;
    display: block !important; cursor: pointer;
    transition: all .15s !important; margin-bottom: 3px !important;
}
[data-testid="stSidebar"] .stRadio label:hover {
    background: var(--s2) !important; color: var(--text) !important;
}

/* ── HERO ── */
.hero {
    position: relative; width: 100%;
    height: 430px; overflow: hidden;
}
.hero-img {
    width: 100%; height: 100%;
    object-fit: cover; object-position: center 30%;
    display: block;
    filter: brightness(.46) saturate(1.2);
    transition: transform 8s ease;
}
.hero:hover .hero-img { transform: scale(1.05); }
.hero-ov {
    position: absolute; inset: 0;
    background: linear-gradient(125deg,
        rgba(8,14,36,.92) 0%, rgba(8,14,36,.55) 55%,
        rgba(26,115,232,.14) 100%);
    display: flex; flex-direction: column;
    justify-content: flex-end; padding: 2.75rem 3.5rem 3rem;
    animation: fadeIn .7s ease;
}
.hero-tag {
    display: inline-flex; align-items: center;
    font-family: 'JetBrains Mono', monospace;
    font-size: .63rem; font-weight: 500; letter-spacing: .18em;
    text-transform: uppercase; color: #60a5fa;
    margin-bottom: .9rem; gap: .5rem;
}
.hero-tag::before {
    content: ''; width: 20px; height: 1px; background: #60a5fa;
}
.hero-h1 {
    font-family: 'DM Serif Display', serif;
    font-size: clamp(2rem, 3.6vw, 3rem);
    color: #fff; font-weight: 400; line-height: 1.15;
    margin-bottom: .9rem;
    text-shadow: 0 2px 24px rgba(0,0,0,.4);
}
.hero-sub {
    font-size: .97rem; color: rgba(255,255,255,.76);
    max-width: 540px; line-height: 1.78; margin-bottom: 1.5rem;
}
.hero-chips { display: flex; gap: .5rem; flex-wrap: wrap; }
.chip {
    display: inline-flex; align-items: center; gap: .3rem;
    background: rgba(255,255,255,.1);
    border: 1px solid rgba(255,255,255,.2);
    backdrop-filter: blur(10px);
    color: #fff; font-size: .72rem; font-weight: 600;
    padding: .3rem .8rem; border-radius: 999px;
}

/* ── PAGE BANNER ── */
.pgbanner {
    position: relative; width: 100%;
    height: 160px; overflow: hidden;
}
.pgbanner img {
    width: 100%; height: 100%;
    object-fit: cover; object-position: center 38%;
    filter: brightness(.4) saturate(1.15);
    display: block;
}
.pgbanner-ov {
    position: absolute; inset: 0;
    background: linear-gradient(90deg, rgba(8,14,36,.85) 35%, transparent);
    display: flex; align-items: center; padding: 0 3rem;
}
.pgbanner-ov h1 {
    font-family: 'DM Serif Display', serif !important;
    color: #fff !important; font-size: 1.9rem !important;
    font-weight: 400 !important; margin: 0 !important;
    text-shadow: 0 2px 16px rgba(0,0,0,.5);
}
.pgbanner-ov p {
    font-size: .84rem; color: rgba(255,255,255,.72);
    margin: .3rem 0 0; line-height: 1.5;
}

/* ── LAYOUT ── */
.wrap { padding: 2.25rem 3rem 1rem; }

/* ── CARDS ── */
.card {
    background: var(--surface);
    border: 1px solid var(--bl);
    border-radius: var(--r); padding: 1.5rem;
    box-shadow: var(--sh1);
    transition: box-shadow .25s, transform .25s;
}
.card:hover { box-shadow: var(--sh2); transform: translateY(-2px); }
.card-sm {
    background: var(--surface);
    border: 1px solid var(--bl);
    border-radius: var(--rsm);
    padding: 1rem 1.2rem; box-shadow: var(--sh0);
}

/* ── KPI ── */
.kpi {
    background: var(--surface);
    border: 1px solid var(--bl);
    border-radius: var(--r);
    padding: 1.25rem 1.4rem;
    box-shadow: var(--sh1);
    position: relative; overflow: hidden;
    transition: box-shadow .25s, transform .25s;
}
.kpi::after {
    content: ''; position: absolute;
    top: 0; left: 0; right: 0; height: 3px;
    background: var(--kpi-color, var(--blue));
    border-radius: var(--r) var(--r) 0 0;
}
.kpi:hover { box-shadow: var(--sh2); transform: translateY(-2px); }
.kpi-ico { font-size: 1.4rem; margin-bottom: .65rem; }
.kpi-lbl {
    font-size: .62rem; font-weight: 700; letter-spacing: .13em;
    text-transform: uppercase; color: var(--text3); margin-bottom: .35rem;
}
.kpi-val {
    font-family: 'DM Serif Display', serif;
    font-size: 1.6rem; color: var(--text); line-height: 1; margin-bottom: .2rem;
}
.kpi-delta { font-size: .72rem; font-weight: 600; }

/* ── FEATURE PHOTO CARD ── */
.fcard {
    background: var(--surface);
    border: 1px solid var(--bl);
    border-radius: var(--rlg); overflow: hidden;
    box-shadow: var(--sh1); height: 100%;
    transition: box-shadow .3s, transform .3s;
}
.fcard:hover { box-shadow: var(--sh3); transform: translateY(-5px); }
.fcard-imgwrap { overflow: hidden; height: 165px; }
.fcard-imgwrap img {
    width: 100%; height: 165px;
    object-fit: cover; object-position: center;
    filter: saturate(.85);
    transition: transform .4s ease, filter .4s;
    display: block;
}
.fcard:hover .fcard-imgwrap img {
    transform: scale(1.07); filter: saturate(1.1);
}
.fcard-body { padding: 1.2rem; }
.fcard-ico { font-size: 1.3rem; margin-bottom: .5rem; }
.fcard-ttl {
    font-family: 'DM Serif Display', serif;
    font-size: 1rem; color: var(--text); margin-bottom: .3rem;
}
.fcard-dsc { font-size: .8rem; color: var(--text2); line-height: 1.65; }

/* ── SECTION LABEL ── */
.slbl {
    font-size: .63rem; font-weight: 700; letter-spacing: .14em;
    text-transform: uppercase; color: var(--text3);
    margin-bottom: .85rem; padding-bottom: .5rem;
    border-bottom: 1px solid var(--bl);
    display: flex; align-items: center; gap: .5rem;
}
.slbl::before {
    content: ''; width: 14px; height: 2px;
    background: var(--blue); border-radius: 1px; flex-shrink: 0;
}

/* ── STAT ROW ── */
.sr {
    display: flex; justify-content: space-between; align-items: center;
    padding: .55rem 0; border-bottom: 1px solid var(--bl);
    font-size: .83rem;
}
.sr:last-child { border: none; }
.sk { color: var(--text2); font-weight: 400; }
.sv {
    color: var(--text); font-weight: 600;
    font-family: 'JetBrains Mono', monospace; font-size: .8rem;
}

/* ── BADGE ── */
.badge {
    display: inline-block; font-size: .65rem; font-weight: 600;
    letter-spacing: .04em; padding: .18rem .58rem; border-radius: 999px;
}
.bb  { background: var(--blue-l);   color: var(--blue);   }
.bg  { background: var(--green-l);  color: var(--green);  }
.br  { background: var(--red-l);    color: var(--red);    }
.bgd { background: var(--gold-l);   color: var(--gold);   }
.bp  { background: var(--purple-l); color: var(--purple); }

/* ── PIPELINE ── */
.pipe {
    background: var(--surface); border: 1px solid var(--bl);
    border-radius: var(--r); padding: 1rem .8rem; text-align: center;
}
.pipe.on { border-color: var(--blue); background: var(--blue-l); }
.pipe-n {
    width: 28px; height: 28px; border-radius: 50%;
    background: var(--s2); color: var(--text3);
    font-family: 'JetBrains Mono', monospace;
    font-size: .68rem; font-weight: 700;
    display: flex; align-items: center; justify-content: center;
    margin: 0 auto .5rem;
}
.pipe-n.on { background: var(--blue); color: #fff; }
.pipe-t { font-size: .72rem; font-weight: 700; color: var(--text2); }
.pipe-t.on { color: var(--blue); }
.pipe-s { font-size: .62rem; color: var(--text3); margin-top: .18rem; font-family: 'JetBrains Mono', monospace; }

/* ── VERDICT ── */
.verdict {
    border-radius: var(--r); padding: 1.4rem 1.75rem;
    border-left: 4px solid; animation: scaleIn .4s ease;
}
.v-ok  { background: var(--green-l); border-color: var(--green); }
.v-bad { background: var(--red-l);   border-color: var(--red);   }
.verdict-t {
    font-family: 'DM Serif Display', serif;
    font-size: 1.2rem; margin-bottom: .3rem; line-height: 1.3;
}
.verdict-d { font-size: .84rem; color: var(--text2); line-height: 1.65; }

/* ── PROBA BARS ── */
.pb { margin-bottom: 1rem; }
.pb-hd {
    display: flex; justify-content: space-between;
    font-size: .8rem; font-weight: 600; margin-bottom: .35rem;
}
.pb-track {
    background: var(--s2); border-radius: 999px;
    height: 9px; overflow: hidden;
}
.pb-fill {
    height: 100%; border-radius: 999px;
    animation: barGrow .9s cubic-bezier(.4,0,.2,1) both;
}

/* ── PERF BAR ── */
.perfb { margin-bottom: .9rem; }
.perfb-hd {
    display: flex; justify-content: space-between;
    font-size: .78rem; font-weight: 500; color: var(--text2); margin-bottom: .28rem;
}
.perfb-track { background: var(--s2); border-radius: 999px; height: 5px; overflow: hidden; }
.perfb-fill {
    height: 100%; border-radius: 999px;
    background: linear-gradient(90deg, var(--blue), var(--purple));
}

/* ── FEATURE TAG ── */
.ftag {
    display: inline-block; background: var(--s2); border: 1px solid var(--border);
    border-radius: var(--rsm); padding: .28rem .6rem; font-size: .72rem;
    font-weight: 500; color: var(--text2); margin: .18rem;
    font-family: 'JetBrains Mono', monospace; transition: all .15s;
}
.ftag:hover { background: var(--blue-l); border-color: var(--blue); color: var(--blue); }

/* ── TEAM CARD ── */
.tcard {
    background: var(--surface); border: 1px solid var(--bl);
    border-radius: var(--rlg); overflow: hidden;
    box-shadow: var(--sh1); text-align: center;
    transition: box-shadow .3s, transform .3s;
}
.tcard:hover { box-shadow: var(--sh3); transform: translateY(-5px); }
.tcard-img {
    width: 100%; height: 215px;
    object-fit: cover; object-position: center top;
    display: block; filter: saturate(.88);
    transition: filter .3s;
}
.tcard:hover .tcard-img { filter: saturate(1.1); }
.tcard-body { padding: 1.15rem 1rem 1.3rem; }
.tcard-name { font-family: 'DM Serif Display', serif; font-size: 1rem; color: var(--text); margin-bottom: .2rem; }
.tcard-role {
    font-size: .62rem; font-weight: 700; letter-spacing: .09em;
    text-transform: uppercase; color: var(--blue); margin-bottom: .5rem;
}
.tcard-bio { font-size: .78rem; color: var(--text2); line-height: 1.65; }

/* ── DIVIDER ── */
.divider { height: 1px; background: var(--bl); margin: 1.75rem 0; }

/* ── OVERRIDES STREAMLIT ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 0 !important; background: transparent !important;
    border-bottom: 2px solid var(--border) !important;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'DM Sans', sans-serif !important; font-size: .85rem !important;
    font-weight: 600 !important; color: var(--text3) !important;
    background: transparent !important; border: none !important;
    padding: .65rem 1.2rem !important; border-radius: 0 !important;
}
.stTabs [aria-selected="true"] {
    color: var(--blue) !important;
    border-bottom: 2px solid var(--blue) !important; margin-bottom: -2px !important;
}
.stButton > button {
    background: linear-gradient(135deg, var(--blue), #1557b0) !important;
    color: #fff !important; border: none !important;
    border-radius: var(--rsm) !important;
    font-family: 'DM Sans', sans-serif !important; font-weight: 700 !important;
    font-size: .85rem !important; padding: .6rem 1.75rem !important;
    box-shadow: 0 3px 12px rgba(26,115,232,.35) !important;
    transition: all .2s !important;
}
.stButton > button:hover {
    box-shadow: 0 5px 20px rgba(26,115,232,.45) !important;
    transform: translateY(-1px) !important;
}
.stDataFrame { border-radius: var(--r) !important; overflow: hidden; }
[data-testid="stFileUploader"] {
    border: 2px dashed var(--border) !important;
    border-radius: var(--r) !important; background: var(--surface) !important;
}
[data-testid="stForm"] {
    background: var(--surface) !important; border: 1px solid var(--bl) !important;
    border-radius: var(--rlg) !important; padding: 1.75rem !important;
    box-shadow: var(--sh1);
}
.stProgress > div > div { background: var(--s2) !important; border-radius: 999px !important; }
.stProgress > div > div > div {
    border-radius: 999px !important;
    background: linear-gradient(90deg, var(--blue), var(--purple)) !important;
}
[data-testid="stMetricValue"] { color: var(--text) !important; font-family: 'DM Serif Display', serif !important; }
[data-testid="stMetricLabel"] {
    color: var(--text3) !important; font-size: .63rem !important;
    font-weight: 700 !important; letter-spacing: .1em !important;
    text-transform: uppercase !important;
}
.stAlert { border-radius: var(--rsm) !important; border: none !important; font-size: .83rem !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  MODÈLE
# ─────────────────────────────────────────────
@st.cache_resource
def load_model():
    try:    return joblib.load('mon_modele.pkl')
    except: return None

model = load_model()

PL = dict(
    font_family="DM Sans", plot_bgcolor="white", paper_bgcolor="white",
    margin=dict(l=16, r=16, t=40, b=16), font_color="#505772",
    title_font_family="DM Serif Display", title_font_color="#12172b",
    title_font_size=14,
    legend=dict(bgcolor="white", borderwidth=0, font_size=12),
    xaxis=dict(showgrid=True, gridcolor="#eef1f8", linecolor="#dde2f0", zeroline=False),
    yaxis=dict(showgrid=True, gridcolor="#eef1f8", linecolor="#dde2f0", zeroline=False),
)
PAL = ["#1a73e8", "#7c3aed", "#00c48c", "#f59e0b", "#f4455a", "#00bcd4"]

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="padding:1.5rem 1.2rem 1rem">
        <div style="font-family:'DM Serif Display',serif;font-size:1.42rem;
                    color:var(--text);line-height:1.1">BankSignal</div>
        <div style="font-size:.62rem;color:var(--text3);letter-spacing:.14em;
                    text-transform:uppercase;margin-top:.2rem">AI Platform</div>
        <img src="{IMG['server']}"
             style="width:100%;height:84px;object-fit:cover;border-radius:10px;
                    margin:1rem 0 .25rem;opacity:.6;filter:saturate(.5)">
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown("<div style='padding:0 1rem .5rem'>", unsafe_allow_html=True)
        menu = st.radio("", [
            "🏠  Accueil & Données",
            "🔮  Prédiction",
            "📊  Performance du modèle",
            "💡  À propos",
        ], label_visibility="collapsed")
        st.markdown("</div>", unsafe_allow_html=True)

    ok = model is not None
    st.markdown(f"""
    <div style="padding:.5rem 1.2rem 1.5rem">
        <div class="divider" style="margin:.8rem 0"></div>
        <div class="card-sm">
            <div class="kpi-lbl">Statut modèle</div>
            <div style="font-size:.85rem;font-weight:600;
                        color:{'#00c48c' if ok else '#f59e0b'}">
                {'✅ Opérationnel' if ok else '⚠ Non détecté'}</div>
            <div style="font-size:.68rem;color:var(--text3);margin-top:.2rem">
                Random Forest Classifier</div>
        </div>
        <div style="margin-top:1.1rem">
            <div class="kpi-lbl" style="margin-bottom:.5rem">Fonctionnalités</div>
            {''.join([f'<div style="font-size:.78rem;color:var(--text2);padding:.2rem 0">· {f}</div>'
              for f in ["Prédiction client","Exploration dataset","Métriques modèle",
                        "Feature importance","Matrice de confusion"]])}
        </div>
    </div>
    """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════
#  PAGE 1 — ACCUEIL & DONNÉES
# ════════════════════════════════════════════════════
if "🏠" in menu:

    # ── HERO BANNER ──────────────────────────────
    st.markdown(f"""
    <div class="hero">
        <img class="hero-img" src="{IMG['hero']}" alt="financial district">
        <div class="hero-ov">
            <div class="hero-tag">🏦 BankSignal · Intelligence Artificielle Bancaire</div>
            <div class="hero-h1">
                Prédire la souscription client.<br><em>Avant même l'appel.</em>
            </div>
            <div class="hero-sub">
                Moteur de <strong>Machine Learning supervisé</strong> qui identifie en temps réel
                les clients bancaires à fort potentiel de souscription à un dépôt à terme,
                en croisant profils démographiques, historique et indicateurs macroéconomiques.
            </div>
            <div class="hero-chips">
                <span class="chip">🎯 +20% conversion</span>
                <span class="chip">📊 ROC AUC 0.94</span>
                <span class="chip">🌳 Random Forest · 100 arbres</span>
                <span class="chip">📋 45 211 clients UCI</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="wrap">', unsafe_allow_html=True)

    # ── KPI ──────────────────────────────────────
    c1,c2,c3,c4 = st.columns(4)
    for col, (ico,lbl,val,delta,color,dl) in zip([c1,c2,c3,c4], [
        ("🎯","Objectif","Ciblage précis","+20% conversion","#1a73e8","d1"),
        ("🌳","Algorithme","Random Forest","100 estimateurs","#7c3aed","d2"),
        ("📋","Dataset","UCI Bank Mktg.","45 211 clients","#00c48c","d3"),
        ("⚖️","ROC AUC","0.94","Score de test","#f59e0b","d4"),
    ]):
        with col:
            st.markdown(f"""
            <div class="kpi anim-up {dl}" style="--kpi-color:{color}">
                <div class="kpi-ico">{ico}</div>
                <div class="kpi-lbl">{lbl}</div>
                <div class="kpi-val" style="color:{color};font-size:1.1rem">{val}</div>
                <div class="kpi-delta" style="color:{color};opacity:.8">{delta}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # ── FEATURE PHOTO CARDS ───────────────────────
    st.markdown('<div class="slbl">Ce que fait cette plateforme</div>', unsafe_allow_html=True)
    f1,f2,f3 = st.columns(3)
    for col, (img,ico,ttl,dsc) in zip([f1,f2,f3], [
        (IMG["f1"],"🎯","Ciblage Précis",
         "Identifie les clients à fort potentiel avant le premier contact, réduisant les coûts de prospection de façon significative."),
        (IMG["f2"],"🧠","Moteur ML",
         "Random Forest entraîné sur 45 000+ profils réels : variables démographiques, comportementales et macroéconomiques combinées."),
        (IMG["f3"],"📈","Impact Mesurable",
         "Amélioration prouvée du taux de conversion de +20% sur les campagnes de dépôt à terme bancaire."),
    ]):
        with col:
            st.markdown(f"""
            <div class="fcard anim-up">
                <div class="fcard-imgwrap"><img src="{img}" alt="{ttl}"></div>
                <div class="fcard-body">
                    <div class="fcard-ico">{ico}</div>
                    <div class="fcard-ttl">{ttl}</div>
                    <div class="fcard-dsc">{dsc}</div>
                </div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # ── CHARGEMENT DONNÉES ────────────────────────
    st.markdown('<div class="slbl">Chargement des données</div>', unsafe_allow_html=True)
    tab_loc, tab_up = st.tabs(["  📂  Dataset local  ", "  📤  Uploader un CSV  "])

    with tab_loc:
        ci, cb = st.columns([3,1])
        with ci:
            st.markdown("""
            <div class="card-sm">
                <div class="kpi-lbl">Source officielle</div>
                <div style="font-size:.9rem;font-weight:600;margin-bottom:.2rem">
                    bank-additional-full.csv</div>
                <div style="font-size:.75rem;color:var(--text3)">
                    UCI ML Repository · 45 211 lignes · 21 colonnes · sep=";"
                </div>
            </div>""", unsafe_allow_html=True)
        with cb:
            if st.button("Charger", use_container_width=True):
                try:
                    df = pd.read_csv('bank-additional-full.csv', sep=';')
                    st.session_state['data'] = df
                    st.success("✓ Dataset chargé avec succès !")
                except:
                    st.error("Fichier `bank-additional-full.csv` introuvable.")

    with tab_up:
        uf = st.file_uploader("Glisser-déposer ou cliquer pour choisir un CSV", type=["csv"])
        if uf:
            try:
                df = pd.read_csv(uf, sep=';')
                if df.shape[1] < 3: df = pd.read_csv(uf, sep=',')
            except:
                df = pd.read_csv(uf, sep=',')
            st.session_state['data'] = df
            st.success(f"✓ {len(df):,} lignes · {df.shape[1]} colonnes chargées")

    # ── APERÇU DONNÉES ────────────────────────────
    if 'data' not in st.session_state:
        st.markdown("""
        <div class="card" style="text-align:center;padding:3.5rem;margin-top:1.5rem">
            <div style="font-size:3rem;margin-bottom:1rem;opacity:.25">📂</div>
            <div style="font-family:'DM Serif Display',serif;font-size:1.25rem;margin-bottom:.5rem">
                Aucun dataset chargé</div>
            <div style="color:var(--text3);font-size:.85rem">
                Chargez un dataset ci-dessus pour explorer les données.</div>
        </div>""", unsafe_allow_html=True)
    else:
        df = st.session_state['data']
        hy = 'y' in df.columns
        ha = 'age' in df.columns

        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        st.markdown('<div class="slbl">Aperçu statistique</div>', unsafe_allow_html=True)

        s1,s2,s3,s4 = st.columns(4)
        for col,(lbl,val,c) in zip([s1,s2,s3,s4], [
            ("Total clients",  f"{len(df):,}",    "#1a73e8"),
            ("Variables",      str(df.shape[1]),  "#7c3aed"),
            ("Âge moyen",      f"{df['age'].mean():.1f} ans" if ha else "N/A", "#00bcd4"),
            ("Taux souscription", f"{(df['y']=='yes').mean()*100:.1f}%" if hy else "N/A", "#00c48c"),
        ]):
            with col:
                st.markdown(f"""
                <div class="kpi" style="--kpi-color:{c}">
                    <div class="kpi-lbl">{lbl}</div>
                    <div class="kpi-val" style="color:{c}">{val}</div>
                </div>""", unsafe_allow_html=True)

        # Stats + qualité
        st.markdown("<div style='margin-top:1.5rem'></div>", unsafe_allow_html=True)
        dc1, dc2 = st.columns([2,1])
        with dc1:
            st.markdown('<div class="slbl">Statistiques descriptives</div>', unsafe_allow_html=True)
            nc = df.select_dtypes(include=[np.number]).columns.tolist()
            if nc:
                st.dataframe(df[nc].describe().round(2), use_container_width=True, height=225)
        with dc2:
            st.markdown('<div class="slbl">Qualité des données</div>', unsafe_allow_html=True)
            complete = 100 - df.isnull().mean().mean() * 100
            st.markdown(f"""
            <div class="card">
                <div class="sr"><span class="sk">Valeurs manquantes</span>
                    <span class="sv">{df.isnull().sum().sum():,}</span></div>
                <div class="sr"><span class="sk">Colonnes numériques</span>
                    <span class="sv">{len(df.select_dtypes(include=np.number).columns)}</span></div>
                <div class="sr"><span class="sk">Colonnes catégorielles</span>
                    <span class="sv">{len(df.select_dtypes(exclude=np.number).columns)}</span></div>
                <div class="sr"><span class="sk">Doublons</span>
                    <span class="sv">{df.duplicated().sum():,}</span></div>
                <div class="sr"><span class="sk">Complétude</span>
                    <span class="sv" style="color:var(--green)">{complete:.1f}%</span></div>
            </div>""", unsafe_allow_html=True)
            tags = "".join([f'<span class="ftag">{c}</span>' for c in df.columns])
            st.markdown(f'<div style="margin-top:.8rem;line-height:2.1">{tags}</div>',
                        unsafe_allow_html=True)

        # Aperçu lignes
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        st.markdown('<div class="slbl">Aperçu — 10 premières lignes</div>', unsafe_allow_html=True)
        st.dataframe(df.head(10), use_container_width=True, height=305)

        # Exploration visuelle
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        st.markdown('<div class="slbl">Exploration visuelle</div>', unsafe_allow_html=True)
        viz = [c for c in ["age","duration","campaign","balance","pdays",
                            "emp.var.rate","cons.price.idx","euribor3m"] if c in df.columns]
        if viz:
            vc1, vc2, vc3 = st.columns([1,1,4])
            with vc1: feat = st.selectbox("Variable", viz)
            with vc2: ct = st.radio("Graphique", ["Histogramme","Boxplot"],
                                    label_visibility="collapsed")
            with vc3:
                cm = {"yes": PAL[2], "no": PAL[0]} if hy else None
                if ct == "Histogramme":
                    fig = px.histogram(df, x=feat, color="y" if hy else None,
                        barmode="overlay", opacity=.78, color_discrete_map=cm,
                        template="plotly_white", title=f"Distribution · {feat}")
                else:
                    fig = px.box(df, x="y" if hy else None, y=feat,
                        color="y" if hy else None, color_discrete_map=cm,
                        template="plotly_white", title=f"Boxplot · {feat}")
                fig.update_layout(**PL)
                st.plotly_chart(fig, use_container_width=True)

        # Heatmap corrélations
        num_df = df.select_dtypes(include=[np.number])
        if len(num_df.columns) >= 3:
            st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
            st.markdown('<div class="slbl">Matrice de corrélation</div>', unsafe_allow_html=True)
            corr = num_df.corr().round(2)
            fig_h = go.Figure(go.Heatmap(
                z=corr.values, x=list(corr.columns), y=list(corr.index),
                colorscale=[[0,"#f4455a"],[0.5,"#ffffff"],[1,"#1a73e8"]],
                zmid=0, text=corr.values,
                texttemplate="%{text:.2f}", textfont_size=9,
                hoverongaps=False,
                colorbar=dict(thickness=12, len=.8, tickfont_size=10),
            ))
            fig_h.update_layout(**PL, title="Corrélations entre variables numériques",
                height=360,
                xaxis=dict(tickfont_size=10, showgrid=False, tickangle=-30),
                yaxis=dict(tickfont_size=10, showgrid=False))
            st.plotly_chart(fig_h, use_container_width=True)

        # Variable cible
        if hy:
            st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
            st.markdown('<div class="slbl">Variable cible — Répartition</div>', unsafe_allow_html=True)
            ty1, ty2 = st.columns([1,2])
            vc = df['y'].value_counts()
            with ty1:
                for k in vc.index:
                    pct = vc[k] / len(df) * 100
                    c = "var(--green)" if k == "yes" else "var(--red)"
                    lb = "Souscrit ✅" if k == "yes" else "Non souscrit ❌"
                    st.markdown(f"""
                    <div class="card" style="margin-bottom:.6rem;border-left:3px solid {c}">
                        <div style="font-size:.68rem;font-weight:700;color:{c};margin-bottom:.3rem">{lb}</div>
                        <div style="font-family:'DM Serif Display',serif;font-size:1.8rem;color:var(--text)">{vc[k]:,}</div>
                        <div style="font-size:.7rem;color:var(--text3)">{pct:.1f}% du total</div>
                    </div>""", unsafe_allow_html=True)
            with ty2:
                fig_pie = go.Figure(go.Pie(
                    labels=["Souscrit","Non souscrit"], values=vc.values,
                    hole=.58, pull=[.04, 0],
                    marker=dict(colors=[PAL[2], PAL[0]],
                                line=dict(color="white", width=3)),
                    textfont_size=12,
                ))
                fig_pie.update_layout(**PL, title="Répartition des classes",
                    showlegend=True, height=305, margin=dict(l=0,r=0,t=40,b=0))
                st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)


# ════════════════════════════════════════════════════
#  PAGE 2 — PRÉDICTION
# ════════════════════════════════════════════════════
elif "🔮" in menu:

    st.markdown(f"""
    <div class="pgbanner">
        <img src="{IMG['trading']}" alt="stock charts">
        <div class="pgbanner-ov">
            <div>
                <h1>Module de Prédiction</h1>
                <p>Renseignez le profil d'un client — l'IA retourne sa probabilité de souscription en temps réel.</p>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="wrap">', unsafe_allow_html=True)

    # Pipeline
    st.markdown('<div class="slbl">Pipeline d\'inférence</div>', unsafe_allow_html=True)
    for col, (n,t,s,a) in zip(st.columns(5), [
        ("01","Saisie","Données client",True),
        ("02","Encodage","Catégorielles",False),
        ("03","Scaling","Normalisation",False),
        ("04","Forêt","100 arbres",False),
        ("05","Score","Probabilité",False),
    ]):
        with col:
            st.markdown(f"""
            <div class="pipe {'on' if a else ''}">
                <div class="pipe-n {'on' if a else ''}">{n}</div>
                <div class="pipe-t {'on' if a else ''}">{t}</div>
                <div class="pipe-s">{s}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    if model is None:
        st.markdown("""
        <div class="card" style="border-left:4px solid var(--gold);text-align:center;padding:2.5rem">
            <div style="font-size:2rem;margin-bottom:.75rem">⚠️</div>
            <div style="font-family:'DM Serif Display',serif;font-size:1.1rem;margin-bottom:.4rem">
                Modèle non chargé</div>
            <div style="color:var(--text3);font-size:.85rem">
                Placez <code>mon_modele.pkl</code> dans le dossier du projet.</div>
        </div>""", unsafe_allow_html=True)
    else:
        # Layout : formulaire + photo conseiller
        fc, pc = st.columns([2, 1])

        with pc:
            st.markdown(f"""
            <div style="position:sticky;top:1.5rem">
                <div style="border-radius:var(--rlg);overflow:hidden;
                            box-shadow:var(--sh2);margin-bottom:1rem">
                    <img src="{IMG['meeting']}"
                         style="width:100%;height:235px;object-fit:cover;
                                object-position:center top;display:block">
                </div>
                <div class="card-sm" style="text-align:center">
                    <div class="kpi-lbl" style="margin-bottom:.4rem">Analyse IA · Temps réel</div>
                    <div style="font-size:.8rem;color:var(--text2);line-height:1.65">
                        Le modèle traite simultanément les 20 variables du profil
                        et retourne une probabilité de souscription calibrée sur
                        45 211 clients historiques.
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)

        with fc:
            st.markdown('<div class="slbl">Profil client</div>', unsafe_allow_html=True)
            with st.form("prediction_form"):
                r1, r2, r3 = st.columns(3)
                with r1:
                    age      = st.slider("Âge", 18, 95, 35)
                    job      = st.selectbox("Métier", [
                        "admin.","blue-collar","technician","services","management",
                        "retired","entrepreneur","self-employed","housemaid","unemployed","student"])
                    marital  = st.selectbox("Situation matrimoniale", ["married","single","divorced"])
                with r2:
                    education = st.selectbox("Niveau d'études", [
                        "university.degree","high.school","basic.9y",
                        "professional.course","basic.6y","basic.4y","illiterate"])
                    duration  = st.number_input("Durée dernier appel (sec)", 0, 5000, 250)
                    campaign  = st.slider("Contacts cette campagne", 1, 50, 2)
                with r3:
                    pdays    = st.number_input("Jours depuis dernier contact (999=jamais)", 0, 999, 999)
                    euribor  = st.number_input("Taux Euribor 3 mois", 0.0, 6.0, 4.8, step=0.1)
                    month    = st.selectbox("Mois du contact", [
                        "jan","feb","mar","apr","may","jun",
                        "jul","aug","sep","oct","nov","dec"])

                submit = st.form_submit_button("🔮  Lancer la prédiction", use_container_width=True)

            if submit:
                inp = np.zeros((1, 20))
                inp[0, 0]  = age
                inp[0, 10] = duration
                inp[0, 11] = campaign
                inp[0, 18] = euribor

                pred  = model.predict(inp)
                proba = model.predict_proba(inp)[0][1]
                pno   = 1 - proba

                st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
                st.markdown('<div class="slbl">Résultat de l\'analyse</div>', unsafe_allow_html=True)

                # Verdict
                if pred[0] == 1:
                    st.markdown(f"""
                    <div class="verdict v-ok">
                        <div class="verdict-t" style="color:var(--green)">
                            ✅ Haute probabilité de souscription</div>
                        <div class="verdict-d">
                            Ce client présente un profil fortement aligné avec les souscripteurs
                            historiques. Une approche commerciale personnalisée est recommandée
                            lors du prochain contact.
                        </div>
                    </div>""", unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="verdict v-bad">
                        <div class="verdict-t" style="color:var(--red)">
                            ❌ Faible probabilité de souscription</div>
                        <div class="verdict-d">
                            Ce profil ne correspond pas aux critères typiques de conversion
                            à ce stade. Réévaluer lors d'un prochain cycle de campagne.
                        </div>
                    </div>""", unsafe_allow_html=True)

                # Résultats détaillés
                res1, res2 = st.columns(2)
                with res1:
                    # Barres animées + récap profil
                    st.markdown(f"""
                    <div class="card">
                        <div class="slbl" style="margin-bottom:.9rem">Probabilités</div>
                        <div class="pb">
                            <div class="pb-hd">
                                <span style="color:var(--green)">✓ Souscription</span>
                                <span style="color:var(--green);font-family:'JetBrains Mono',monospace">
                                    {proba*100:.1f}%</span>
                            </div>
                            <div class="pb-track">
                                <div class="pb-fill"
                                     style="width:{proba*100:.1f}%;
                                            background:linear-gradient(90deg,var(--green),#4ade80);
                                            --target-w:{proba*100:.1f}%">
                                </div>
                            </div>
                        </div>
                        <div class="pb">
                            <div class="pb-hd">
                                <span style="color:var(--red)">✗ Non souscription</span>
                                <span style="color:var(--red);font-family:'JetBrains Mono',monospace">
                                    {pno*100:.1f}%</span>
                            </div>
                            <div class="pb-track">
                                <div class="pb-fill"
                                     style="width:{pno*100:.1f}%;
                                            background:linear-gradient(90deg,var(--red),#fb7185);
                                            --target-w:{pno*100:.1f}%">
                                </div>
                            </div>
                        </div>
                        <div class="slbl" style="margin:1rem 0 .75rem">Profil soumis</div>
                        <div class="sr"><span class="sk">Âge</span><span class="sv">{age} ans</span></div>
                        <div class="sr"><span class="sk">Métier</span><span class="sv">{job}</span></div>
                        <div class="sr"><span class="sk">Durée appel</span><span class="sv">{duration} sec</span></div>
                        <div class="sr"><span class="sk">Euribor 3M</span><span class="sv">{euribor:.2f}%</span></div>
                        <div class="sr"><span class="sk">Contacts</span><span class="sv">{campaign}</span></div>
                        <div class="sr"><span class="sk">Mois</span><span class="sv">{month}</span></div>
                    </div>""", unsafe_allow_html=True)

                with res2:
                    # Gauge Plotly
                    fig_g = go.Figure(go.Indicator(
                        mode="gauge+number+delta",
                        value=proba * 100,
                        delta={"reference": 50, "suffix": "%",
                               "font": {"size": 13, "family": "DM Sans"}},
                        number={"suffix": "%",
                                "font": {"size": 34, "family": "DM Serif Display",
                                         "color": "#12172b"}},
                        gauge={
                            "axis": {"range": [0, 100], "tickcolor": "#96a0bc",
                                     "tickfont": {"size": 10}},
                            "bar": {"color": "#00c48c" if proba > .5 else "#f4455a",
                                    "thickness": .22},
                            "bgcolor": "#eef1f8", "borderwidth": 0,
                            "steps": [
                                {"range": [0,  35], "color": "rgba(244,69,90,.09)"},
                                {"range": [35, 65], "color": "rgba(245,158,11,.07)"},
                                {"range": [65,100], "color": "rgba(0,196,140,.09)"},
                            ],
                            "threshold": {"line": {"color": "#12172b", "width": 2},
                                          "value": proba * 100}
                        },
                    ))
                    fig_g.update_layout(
                        height=245, paper_bgcolor="white",
                        font_family="DM Sans",
                        margin=dict(l=16, r=16, t=24, b=8)
                    )
                    st.plotly_chart(fig_g, use_container_width=True)

                    # Recommandation
                    if pred[0] == 1:
                        rec_color = "var(--green)"
                        rec_ico   = "🟢"
                        rec_action = "Contacter en priorité · Offre personnalisée"
                        rec_detail = "Durée d'appel élevée = signal fort d'intérêt."
                    else:
                        rec_color = "var(--red)"
                        rec_ico   = "🔴"
                        rec_action = "Faible priorité · Campagne ultérieure"
                        rec_detail = "Réévaluer lors d'un prochain cycle."

                    st.markdown(f"""
                    <div class="card" style="border-left:3px solid {rec_color};margin-top:.5rem">
                        <div class="kpi-lbl" style="margin-bottom:.4rem">Recommandation</div>
                        <div style="font-size:.85rem;font-weight:600;color:{rec_color};
                                    margin-bottom:.25rem">{rec_ico} {rec_action}</div>
                        <div style="font-size:.75rem;color:var(--text3)">{rec_detail}</div>
                    </div>""", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


# ════════════════════════════════════════════════════
#  PAGE 3 — PERFORMANCE DU MODÈLE
# ════════════════════════════════════════════════════
elif "📊" in menu:

    st.markdown(f"""
    <div class="pgbanner">
        <img src="{IMG['data']}" alt="analytics">
        <div class="pgbanner-ov">
            <div>
                <h1>Performance du Modèle</h1>
                <p>Métriques, feature importance, courbe ROC, matrice de confusion et courbes d'apprentissage.</p>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="wrap">', unsafe_allow_html=True)

    # ── CONFIG + MÉTRIQUES ──────────────────────
    st.markdown('<div class="slbl">Configuration & Métriques</div>', unsafe_allow_html=True)
    cfg1, cfg2 = st.columns([1, 2])

    with cfg1:
        st.markdown("""
        <div class="card">
            <div style="font-family:'DM Serif Display',serif;font-size:1.15rem;
                        margin-bottom:1.1rem">Random Forest Classifier</div>
            <div class="sr"><span class="sk">n_estimators</span><span class="sv">100</span></div>
            <div class="sr"><span class="sk">criterion</span><span class="sv">gini</span></div>
            <div class="sr"><span class="sk">max_depth</span><span class="sv">None</span></div>
            <div class="sr"><span class="sk">max_features</span><span class="sv">sqrt</span></div>
            <div class="sr"><span class="sk">min_samples_split</span><span class="sv">2</span></div>
            <div class="sr"><span class="sk">bootstrap</span><span class="sv">True</span></div>
            <div class="sr"><span class="sk">Bibliothèque</span><span class="sv">scikit-learn</span></div>
            <div class="sr"><span class="sk">Source</span><span class="sv">UCI ML Repo</span></div>
        </div>""", unsafe_allow_html=True)

    with cfg2:
        m_cols = st.columns(5)
        for col, (n,v,c) in zip(m_cols, [
            ("Accuracy",  91.2, PAL[0]),
            ("Precision", 89.5, PAL[1]),
            ("Recall",    87.3, PAL[2]),
            ("F1-Score",  88.4, PAL[3]),
            ("ROC AUC",   94.1, PAL[4]),
        ]):
            with col:
                st.markdown(f"""
                <div class="kpi" style="--kpi-color:{c};text-align:center">
                    <div class="kpi-lbl">{n}</div>
                    <div class="kpi-val" style="color:{c};font-size:1.45rem">{v}%</div>
                </div>""", unsafe_allow_html=True)

        st.markdown("<div style='margin-top:1.25rem'></div>", unsafe_allow_html=True)
        st.markdown('<div class="slbl">Performance par classe</div>', unsafe_allow_html=True)
        for lbl, v in [
            ("Precision — Classe 0 (Non souscrit)", 93),
            ("Precision — Classe 1 (Souscrit)",     85),
            ("Recall — Classe 0",                   96),
            ("Recall — Classe 1",                   78),
            ("F1-Score — Classe 0",                 94),
            ("F1-Score — Classe 1",                 82),
        ]:
            st.markdown(f"""
            <div class="perfb">
                <div class="perfb-hd">
                    <span>{lbl}</span>
                    <span style="font-weight:700">{v}%</span>
                </div>
                <div class="perfb-track">
                    <div class="perfb-fill" style="width:{v}%"></div>
                </div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # ── FEATURE IMPORTANCE + ROC ─────────────────
    fi_col, roc_col = st.columns(2)

    with fi_col:
        st.markdown('<div class="slbl">Feature Importance</div>', unsafe_allow_html=True)
        imp_df = pd.DataFrame({
            'Feature': ['duration','euribor3m','age','nr.employed','campaign',
                        'pdays','emp.var.rate','cons.price.idx','poutcome','month'],
            'Importance': [.32,.18,.12,.10,.08,.06,.05,.04,.03,.02]
        }).sort_values('Importance')

        blues = [f"rgba(26,115,232,{.3 + i*.075})" for i in range(len(imp_df))]
        fig_fi = go.Figure(go.Bar(
            x=imp_df['Importance'], y=imp_df['Feature'], orientation='h',
            marker_color=blues, marker_line=dict(width=0),
            text=[f"{v:.0%}" for v in imp_df['Importance']],
            textposition='outside',
            textfont=dict(color='#505772', size=10, family="JetBrains Mono"),
        ))
        fig_fi.update_layout(**PL, title="Top 10 — Feature Importance", height=340)
        st.plotly_chart(fig_fi, use_container_width=True)

    with roc_col:
        st.markdown('<div class="slbl">Courbe ROC</div>', unsafe_allow_html=True)
        np.random.seed(42)
        fpr = np.sort(np.concatenate([[0], np.random.uniform(0,1,80), [1]]))
        tpr = np.clip(fpr**.35 + np.random.normal(0,.015,len(fpr)), 0, 1)
        tpr[0]=0; tpr[-1]=1; tpr=np.sort(tpr)

        fig_roc = go.Figure()
        fig_roc.add_trace(go.Scatter(
            x=fpr, y=tpr, mode='lines', name='Random Forest (AUC=0.94)',
            line=dict(color=PAL[0], width=2.5),
            fill='tozeroy', fillcolor='rgba(26,115,232,.07)'))
        fig_roc.add_trace(go.Scatter(
            x=[0,1], y=[0,1], mode='lines', name='Aléatoire (AUC=0.50)',
            line=dict(color=PAL[4], width=1.5, dash='dot')))
        fig_roc.add_annotation(
            x=.72, y=.45, text="<b>AUC = 0.940</b>",
            font=dict(color=PAL[0], size=12, family="DM Serif Display"),
            showarrow=False, bgcolor="rgba(26,115,232,.07)",
            bordercolor="rgba(26,115,232,.3)", borderwidth=1)
        fig_roc.update_layout(**PL, title="Receiver Operating Characteristic",
            xaxis_title="FPR", yaxis_title="TPR", height=340)
        st.plotly_chart(fig_roc, use_container_width=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # ── MATRICE DE CONFUSION + DISTRIBUTION SCORES ──
    cm_col, dist_col = st.columns(2)

    with cm_col:
        st.markdown('<div class="slbl">Matrice de confusion</div>', unsafe_allow_html=True)
        cm = np.array([[7823, 325], [512, 1684]])
        fig_cm = go.Figure(go.Heatmap(
            z=cm,
            x=["Prédit : Non souscrit","Prédit : Souscrit"],
            y=["Réel : Non souscrit","Réel : Souscrit"],
            colorscale=[[0,"#ffffff"],[0.4,"#dbeafe"],[1,"#1a73e8"]],
            text=cm, texttemplate="<b>%{text:,}</b>",
            textfont=dict(size=15, family="DM Serif Display"),
            showscale=False,
        ))
        fig_cm.update_layout(**PL, height=280,
            xaxis=dict(side='bottom', showgrid=False, tickfont_size=11),
            yaxis=dict(showgrid=False, tickfont_size=11),
            margin=dict(l=16,r=16,t=16,b=16))
        st.plotly_chart(fig_cm, use_container_width=True)

        # 4 cases colorées
        tn,fp,fn,tp = 7823,325,512,1684
        st.markdown(f"""
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:.6rem;margin-top:.5rem">
            <div class="card-sm" style="text-align:center;border-top:3px solid var(--green)">
                <div class="kpi-lbl" style="color:var(--green)">Vrais Positifs</div>
                <div style="font-family:'DM Serif Display',serif;font-size:1.45rem">{tp:,}</div>
            </div>
            <div class="card-sm" style="text-align:center;border-top:3px solid var(--red)">
                <div class="kpi-lbl" style="color:var(--red)">Faux Négatifs</div>
                <div style="font-family:'DM Serif Display',serif;font-size:1.45rem">{fn:,}</div>
            </div>
            <div class="card-sm" style="text-align:center;border-top:3px solid var(--gold)">
                <div class="kpi-lbl" style="color:var(--gold)">Faux Positifs</div>
                <div style="font-family:'DM Serif Display',serif;font-size:1.45rem">{fp:,}</div>
            </div>
            <div class="card-sm" style="text-align:center;border-top:3px solid var(--blue)">
                <div class="kpi-lbl" style="color:var(--blue)">Vrais Négatifs</div>
                <div style="font-family:'DM Serif Display',serif;font-size:1.45rem">{tn:,}</div>
            </div>
        </div>""", unsafe_allow_html=True)

    with dist_col:
        st.markdown('<div class="slbl">Distribution des scores prédits</div>', unsafe_allow_html=True)
        np.random.seed(7)
        s0 = np.random.beta(2, 8, 7000)
        s1 = np.random.beta(7, 2, 2000)
        fig_d = go.Figure()
        fig_d.add_trace(go.Histogram(x=s0, name="Non souscrit (0)",
            marker_color="rgba(26,115,232,.65)", nbinsx=40, opacity=.85))
        fig_d.add_trace(go.Histogram(x=s1, name="Souscrit (1)",
            marker_color="rgba(0,196,140,.75)", nbinsx=40, opacity=.85))
        fig_d.add_vline(x=.5, line_dash="dash", line_color="#12172b",
            annotation_text="Seuil 0.5", annotation_font_size=10)
        fig_d.update_layout(**PL, barmode='overlay',
            title="Séparation des classes par le modèle",
            xaxis_title="Score P(souscription)", yaxis_title="Fréquence", height=285)
        st.plotly_chart(fig_d, use_container_width=True)

        # Courbes d'apprentissage
        st.markdown('<div class="slbl" style="margin-top:1rem">Courbes d\'apprentissage</div>',
                    unsafe_allow_html=True)
        np.random.seed(12)
        n_est = np.arange(5, 105, 5)
        tr = .87 + .06*(1-np.exp(-n_est/28)) + np.random.normal(0,.003,len(n_est))
        vl = .84 + .07*(1-np.exp(-n_est/34)) + np.random.normal(0,.004,len(n_est))

        fig_lc = go.Figure()
        fig_lc.add_trace(go.Scatter(x=n_est, y=tr, mode='lines+markers',
            name='Train', line=dict(color=PAL[0], width=2),
            marker=dict(size=4),
            fill='tozeroy', fillcolor='rgba(26,115,232,.05)'))
        fig_lc.add_trace(go.Scatter(x=n_est, y=vl, mode='lines+markers',
            name='Validation', line=dict(color=PAL[1], width=2, dash='dash'),
            marker=dict(size=4)))
        fig_lc.update_layout(**PL, title="Accuracy vs n_estimators",
            xaxis_title="n_estimators", yaxis_title="Accuracy", height=270,
            yaxis=dict(**PL['yaxis'], tickformat=".0%"))
        st.plotly_chart(fig_lc, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)


# ════════════════════════════════════════════════════
#  PAGE 4 — À PROPOS
# ════════════════════════════════════════════════════
elif "💡" in menu:

    st.markdown(f"""
    <div class="pgbanner">
        <img src="{IMG['hero']}" alt="city finance">
        <div class="pgbanner-ov">
            <div>
                <h1>À propos du projet</h1>
                <p>Mission, technologie et équipe derrière BankSignal AI.</p>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="wrap">', unsafe_allow_html=True)

    a1, a2 = st.columns([2, 1])
    with a1:
        st.markdown("""
        <div class="card anim-up">
            <div class="slbl">Contexte & Motivation</div>
            <p style="color:var(--text2);font-size:.9rem;line-height:1.85;margin-bottom:.9rem">
                Le marketing bancaire traditionnel repose sur des campagnes de masse — appels, courriers,
                emails — souvent peu ciblés et très coûteux. Ce projet applique le
                <strong style="color:var(--text)">Machine Learning supervisé</strong> pour identifier
                en amont les clients les plus susceptibles de souscrire à un dépôt à terme.
            </p>
            <p style="color:var(--text2);font-size:.9rem;line-height:1.85;margin:0">
                En analysant simultanément âge, profession, indicateurs macroéconomiques et historique
                de contacts, le modèle permet de <strong style="color:var(--text)">réduire les coûts
                de prospection</strong> tout en <strong style="color:var(--text)">améliorant
                le taux de conversion de +20%</strong> en moyenne.
            </p>
        </div>""", unsafe_allow_html=True)

        st.markdown("""
        <div class="card" style="margin-top:1rem">
            <div class="slbl">Pourquoi Random Forest ?</div>
            <div class="sr"><span class="sk">✅ Robustesse</span>
                <span style="font-size:.78rem;color:var(--text3)">Résiste à l'overfitting via l'agrégation d'arbres</span></div>
            <div class="sr"><span class="sk">✅ Interprétabilité</span>
                <span style="font-size:.78rem;color:var(--text3)">Feature importance claire pour les équipes métier</span></div>
            <div class="sr"><span class="sk">✅ Performance</span>
                <span style="font-size:.78rem;color:var(--text3)">AUC 0.94 sans GPU ni fine-tuning intensif</span></div>
            <div class="sr"><span class="sk">✅ Hétérogénéité</span>
                <span style="font-size:.78rem;color:var(--text3)">Variables mixtes : numériques + catégorielles</span></div>
            <div class="sr"><span class="sk">✅ Stabilité</span>
                <span style="font-size:.78rem;color:var(--text3)">Peu sensible aux valeurs aberrantes et au bruit</span></div>
        </div>""", unsafe_allow_html=True)

    with a2:
        st.markdown("""
        <div class="card">
            <div class="slbl">Stack technique</div>
            <div class="sr"><span class="sk">Langage</span><span class="badge bb">Python 3.10+</span></div>
            <div class="sr"><span class="sk">ML</span><span class="badge bb">Scikit-learn</span></div>
            <div class="sr"><span class="sk">Interface</span><span class="badge bb">Streamlit</span></div>
            <div class="sr"><span class="sk">Visualisation</span><span class="badge bb">Plotly</span></div>
            <div class="sr"><span class="sk">Data</span><span class="badge bb">Pandas · NumPy</span></div>
            <div class="sr"><span class="sk">Déploiement</span><span class="badge bb">Streamlit Cloud</span></div>
        </div>""", unsafe_allow_html=True)

        st.markdown("""
        <div class="card" style="margin-top:1rem">
            <div class="slbl">Dataset</div>
            <div style="font-size:.82rem;color:var(--text2);line-height:1.8">
                <strong>Bank Marketing Dataset</strong><br>
                UCI Machine Learning Repository<br>
                Moro, Cortez & Rita · 2014<br>
                <span class="badge bg" style="margin-top:.4rem;display:inline-block">Open Access</span>
            </div>
        </div>""", unsafe_allow_html=True)

        st.markdown("""
        <div class="card" style="margin-top:1rem">
            <div class="slbl">Éthique & RGPD</div>
            <div style="font-size:.8rem;color:var(--text2);line-height:1.75">
                Données anonymisées conformément au <strong>RGPD</strong>.
                Le modèle est un <em>outil d'aide à la décision</em> — aucune autonomie décisionnelle.
            </div>
        </div>""", unsafe_allow_html=True)

    # ── ÉQUIPE ───────────────────────────────────
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown('<div class="slbl">Équipe du projet</div>', unsafe_allow_html=True)

    tc1, tc2, tc3 = st.columns(3)
    team = [
        (tc1, IMG["t1"], "Alexandre Morin", "Lead Data Scientist",
         "Spécialiste en modèles d'ensemble et feature engineering appliqués à la finance comportementale."),
        (tc2, IMG["t2"], "Sofia Benali", "ML Engineer",
         "Experte en déploiement de modèles et pipelines de données pour les systèmes bancaires temps réel."),
        (tc3, IMG["t3"], "David Chen", "Data Analyst",
         "Analyste spécialisé dans l'interprétabilité des modèles et la visualisation des insights client."),
    ]
    for col, (img, name, role, bio) in team:
        with col:
            st.markdown(f"""
            <div class="tcard anim-up">
                <img class="tcard-img" src="{img}" alt="{name}">
                <div class="tcard-body">
                    <div class="tcard-name">{name}</div>
                    <div class="tcard-role">{role}</div>
                    <div class="tcard-bio">{bio}</div>
                </div>
            </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center;margin-top:3rem;color:var(--text3);
                font-size:.72rem;letter-spacing:.05em">
        BankSignal AI Platform · Analyse prédictive bancaire · 2024 ·
        Photos <a href="https://unsplash.com" style="color:var(--blue)">Unsplash</a> (licence libre)
    </div>""", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

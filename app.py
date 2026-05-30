"""
app.py — WINDGRID Wind Turbine Dashboard
Aesthetic: Dark Aerospace · Industrial Control Room · Midnight Navy · Electric Cyan
"""
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import base64
from datetime import datetime
from io import BytesIO
import charts
import filters

# ── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="⚡ WINDGRID · US Wind Turbine Intelligence",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── GLOBAL CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:ital,wght@0,400;0,700;1,400&family=Barlow+Condensed:wght@300;400;500;600;700;900&family=Barlow:wght@300;400;500&display=swap');

/* ─── Base ─── */
html, body, .stApp {
    background: #060b14 !important;
    font-family: 'Barlow', sans-serif;
    color: #c8dff0;
}
.block-container {
    padding: 2rem 3rem 5rem;
    max-width: 1520px;
}

/* ─── Grid-line overlay ─── */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        repeating-linear-gradient(0deg,   transparent, transparent 59px, rgba(0,229,208,0.025) 60px),
        repeating-linear-gradient(90deg,  transparent, transparent 59px, rgba(0,229,208,0.025) 60px);
    pointer-events: none;
    z-index: 0;
}

/* ─── Sidebar ─── */
[data-testid="stSidebar"] {
    background: #0b1422 !important;
    border-right: 1px solid rgba(0,229,208,0.15);
}
[data-testid="stSidebar"] * {
    color: #7aa0c0 !important;
}
[data-testid="stSidebar"] label {
    font-family: 'Space Mono', monospace !important;
    font-size: 9px !important;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #3a5570 !important;
}
[data-testid="stSidebar"] [data-testid="stSlider"] > div > div > div {
    background: #00e5d0 !important;
}
[data-testid="stSidebar"] [data-testid="stSlider"] > div > div > div > div {
    background: #00e5d0 !important;
    border: 2px solid #060b14;
}
[data-testid="stSidebar"] [data-baseweb="select"] > div:first-child {
    background: #111d30 !important;
    border: 1px solid rgba(0,229,208,0.2) !important;
}
[data-testid="stSidebar"] input {
    background: #111d30 !important;
    color: #7aa0c0 !important;
}
[data-testid="stSidebar"] .stMarkdown p {
    color: #4a6785 !important;
}
[data-testid="stSidebar"] [data-testid="stMultiSelect"] span {
    background: #007d6e !important;
    color: #c8dff0 !important;
}

/* ─── Sidebar button ─── */
[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    color: #00e5d0 !important;
    border: 1px solid rgba(0,229,208,0.3) !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 9px !important;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    border-radius: 1px;
    transition: all 0.2s;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(0,229,208,0.08) !important;
    border-color: #00e5d0 !important;
}

/* ─── Hero header ─── */
.hero {
    background: #0b1422;
    border: 1px solid rgba(0,229,208,0.12);
    border-top: 2px solid #00e5d0;
    border-radius: 2px;
    padding: 44px 52px 40px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    inset: 0;
    background-image:
        repeating-linear-gradient(90deg, transparent, transparent 39px, rgba(0,229,208,0.02) 40px);
    pointer-events: none;
}
.hero::after {
    content: '⚡';
    position: absolute;
    right: 52px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 140px;
    opacity: 0.04;
    line-height: 1;
}
.hero-stamp {
    font-family: 'Space Mono', monospace;
    font-size: 9px;
    letter-spacing: 4px;
    color: #00b8a0;
    text-transform: uppercase;
    margin-bottom: 14px;
}
.hero-title {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 72px;
    font-weight: 900;
    color: #ffffff;
    line-height: 0.92;
    letter-spacing: -2px;
    margin: 0 0 4px;
}
.hero-title span { color: #00e5d0; }
.hero-sub {
    font-family: 'Barlow', sans-serif;
    font-size: 14px;
    color: #4a6785;
    margin-top: 16px;
    line-height: 1.7;
    max-width: 620px;
    font-weight: 300;
}
.hero-tags {
    display: flex;
    gap: 8px;
    margin-top: 26px;
    flex-wrap: wrap;
}
.hero-tag {
    font-family: 'Space Mono', monospace;
    font-size: 9px;
    letter-spacing: 1.5px;
    color: #00b8a0;
    border: 1px solid rgba(0,229,208,0.2);
    border-radius: 1px;
    padding: 5px 12px;
    text-transform: uppercase;
    background: rgba(0,229,208,0.04);
}

/* ─── KPI strip ─── */
.kpi-strip {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 1px;
    background: rgba(0,229,208,0.08);
    border: 1px solid rgba(0,229,208,0.12);
    border-radius: 2px;
    overflow: hidden;
    margin-bottom: 28px;
}
.kpi-cell {
    background: #0b1422;
    padding: 20px 18px;
    position: relative;
    transition: background 0.25s;
}
.kpi-cell:hover { background: #111d30; }
.kpi-cell::after {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 100%;
    height: 2px;
    background: linear-gradient(90deg, #00e5d0, transparent);
    opacity: 0;
    transition: opacity 0.25s;
}
.kpi-cell:hover::after { opacity: 1; }
.kpi-lbl {
    font-family: 'Space Mono', monospace;
    font-size: 8px;
    letter-spacing: 2px;
    color: #3a5570;
    text-transform: uppercase;
    margin-bottom: 8px;
}
.kpi-val {
    font-family: 'Space Mono', monospace;
    font-size: 28px;
    font-weight: 700;
    color: #00e5d0;
    line-height: 1;
    letter-spacing: -1px;
}
.kpi-val.amber { color: #f0a500; }
.kpi-val.white { color: #ffffff; font-size: 20px; padding-top: 4px; }
.kpi-sub {
    font-family: 'Barlow', sans-serif;
    font-size: 10px;
    color: #3a5570;
    margin-top: 5px;
    font-weight: 300;
}

/* ─── Section heading ─── */
.sec-wrap {
    display: flex;
    align-items: center;
    gap: 14px;
    margin: 40px 0 20px;
}
.sec-rule-l {
    height: 1px;
    width: 32px;
    background: #00e5d0;
    flex-shrink: 0;
}
.sec-rule-r {
    flex: 1;
    height: 1px;
    background: rgba(0,229,208,0.12);
}
.sec-num {
    font-family: 'Space Mono', monospace;
    font-size: 9px;
    letter-spacing: 2px;
    color: #00b8a0;
    text-transform: uppercase;
    white-space: nowrap;
}
.sec-title {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 22px;
    font-weight: 700;
    color: #c8dff0;
    margin: 0;
    white-space: nowrap;
    letter-spacing: 0.5px;
}

/* ─── Chart card ─── */
.chart-card {
    background: #0b1422;
    border: 1px solid rgba(0,229,208,0.1);
    border-top: 1px solid rgba(0,229,208,0.25);
    border-radius: 2px;
    overflow: hidden;
    margin-bottom: 14px;
}
.chart-card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 16px 8px;
    border-bottom: 1px solid rgba(0,229,208,0.08);
    background: #060b14;
}
.chart-card-title {
    font-family: 'Space Mono', monospace;
    font-size: 8px;
    letter-spacing: 2px;
    color: #3a5570;
    text-transform: uppercase;
}
.chart-card-body img {
    width: 100%;
    height: auto;
    display: block;
}
.export-link {
    font-family: 'Space Mono', monospace;
    font-size: 8px;
    letter-spacing: 1.5px;
    color: #00b8a0;
    border: 1px solid rgba(0,229,208,0.2);
    border-radius: 1px;
    padding: 3px 10px;
    text-decoration: none;
    text-transform: uppercase;
    transition: all 0.2s;
    background: transparent;
}
.export-link:hover {
    background: rgba(0,229,208,0.06);
    border-color: #00e5d0;
    color: #00e5d0;
}

/* ─── Filter badge ─── */
.fbadge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    font-family: 'Space Mono', monospace;
    font-size: 9px;
    letter-spacing: 1px;
    color: #00b8a0;
    background: rgba(0,229,208,0.06);
    border: 1px solid rgba(0,229,208,0.2);
    border-radius: 20px;
    padding: 4px 12px;
    margin: 3px;
}

/* ─── Tabs ─── */
.stTabs [data-baseweb="tab-list"] {
    background: #060b14 !important;
    border-bottom: 1px solid rgba(0,229,208,0.12) !important;
    gap: 0 !important;
    padding: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Space Mono', monospace !important;
    font-size: 9px !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    color: #3a5570 !important;
    background: transparent !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    padding: 12px 24px !important;
    border-radius: 0 !important;
    transition: all 0.2s !important;
}
.stTabs [data-baseweb="tab"]:hover {
    color: #7aa0c0 !important;
}
.stTabs [aria-selected="true"] {
    color: #00e5d0 !important;
    border-bottom: 2px solid #00e5d0 !important;
    background: transparent !important;
    font-weight: 700 !important;
}

/* ─── Data table ─── */
[data-testid="stDataFrame"] {
    border: 1px solid rgba(0,229,208,0.12) !important;
    border-radius: 2px !important;
}
[data-testid="stDataFrame"] th {
    background: #060b14 !important;
    color: #00b8a0 !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 9px !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
}

/* ─── Download button ─── */
.stDownloadButton > button {
    font-family: 'Space Mono', monospace !important;
    font-size: 9px !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    background: transparent !important;
    color: #00b8a0 !important;
    border: 1px solid rgba(0,229,208,0.25) !important;
    border-radius: 1px !important;
    transition: all 0.2s !important;
}
.stDownloadButton > button:hover {
    background: rgba(0,229,208,0.06) !important;
    border-color: #00e5d0 !important;
    color: #00e5d0 !important;
}

/* ─── Callout ─── */
.callout {
    background: #0b1422;
    border-left: 3px solid #00e5d0;
    border-radius: 0 2px 2px 0;
    border: 1px solid rgba(0,229,208,0.1);
    border-left: 3px solid #00e5d0;
    padding: 14px 18px;
    margin: 6px 0 22px;
    font-family: 'Barlow', sans-serif;
    font-size: 13px;
    color: #4a6785;
    line-height: 1.7;
    font-weight: 300;
}
.callout strong { color: #c8dff0; font-weight: 500; }
.callout .accent { color: #00e5d0; }
.callout .amber  { color: #f0a500; }

/* ─── Alert ─── */
[data-testid="stAlert"] {
    background: #0b1422 !important;
    border: 1px solid rgba(0,229,208,0.15) !important;
    color: #4a6785 !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 11px !important;
    border-radius: 2px !important;
}

/* ─── Scrollbar ─── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: #060b14; }
::-webkit-scrollbar-thumb { background: #007d6e; border-radius: 1px; }
::-webkit-scrollbar-thumb:hover { background: #00e5d0; }

/* ─── Footer ─── */
.footer {
    margin-top: 64px;
    padding: 22px 0 8px;
    border-top: 1px solid rgba(0,229,208,0.1);
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 12px;
}
.footer-brand {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 18px;
    font-weight: 900;
    color: rgba(0,229,208,0.3);
    letter-spacing: -0.5px;
}
.footer-meta {
    font-family: 'Space Mono', monospace;
    font-size: 8px;
    letter-spacing: 2px;
    color: #3a5570;
    text-transform: uppercase;
}
</style>
""", unsafe_allow_html=True)


# ── DATA ──────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)

    # Sentinel value cleanup (-9999 means missing)
    sentinel_cols = ["t_hh", "t_rd", "t_rsa", "t_ttlh", "t_cap",
                     "p_year", "usgs_pr_id", "p_cap"]
    for col in sentinel_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
            df.loc[df[col] == -9999, col] = np.nan
            df.loc[df[col] < -9000, col] = np.nan

    # Validate year range
    if "p_year" in df.columns:
        df.loc[df["p_year"] < 1975, "p_year"] = np.nan
        df.loc[df["p_year"] > 2025, "p_year"] = np.nan

    # Clean string cols
    for col in ["t_state", "t_county", "t_manu", "t_model", "p_name", "t_img_srce"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
            df[col] = df[col].replace("nan", np.nan)

    return df


DATA_PATH = os.path.join("data", "us_wind.csv")
if not os.path.exists(DATA_PATH):
    st.error("⚠ Place us_wind.csv in the data/ folder and restart.")
    st.stop()

df = load_data(DATA_PATH)


# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:28px 4px 12px;">
        <div style="font-family:'Space Mono',monospace;font-size:8px;
                    letter-spacing:3px;color:#007d6e;text-transform:uppercase;">
            Wind Intelligence
        </div>
        <div style="font-family:'Barlow Condensed',sans-serif;font-size:26px;
                    font-weight:900;color:#00e5d0;margin-top:6px;letter-spacing:-0.5px;">
            WINDGRID
        </div>
        <div style="height:1px;background:rgba(0,229,208,0.15);margin:14px 0;"></div>
    </div>
    """, unsafe_allow_html=True)

    if "reset" not in st.session_state:
        st.session_state.reset = False
    sfx = "_r" if st.session_state.reset else ""

    all_states = sorted(df["t_state"].dropna().unique().tolist())
    all_manus  = sorted(
        df[df["t_manu"] != "missing"]["t_manu"].dropna().unique().tolist()
    )

    valid_cap = df["t_cap"][(df["t_cap"] > 0) & df["t_cap"].notna()]
    valid_hh  = df["t_hh"][(df["t_hh"] > 0) & df["t_hh"].notna()]
    valid_yr  = df["p_year"].dropna()

    min_yr  = int(valid_yr.min()) if not valid_yr.empty else 1981
    max_yr  = int(valid_yr.max()) if not valid_yr.empty else 2018
    min_cap = int(valid_cap.min()) if not valid_cap.empty else 50
    max_cap = int(valid_cap.max()) if not valid_cap.empty else 6000
    min_hh  = int(valid_hh.min()) if not valid_hh.empty else 18
    max_hh  = int(valid_hh.max()) if not valid_hh.empty else 130

    sel_states = st.multiselect("State",        options=all_states, default=[], key=f"st{sfx}")
    sel_manus  = st.multiselect("Manufacturer", options=all_manus,  default=[], key=f"mn{sfx}")
    sel_yr     = st.slider("Install Year",
                           min_value=min_yr, max_value=max_yr,
                           value=(min_yr, max_yr), key=f"yr{sfx}")
    sel_cap    = st.slider("Capacity Range (kW)",
                           min_value=min_cap, max_value=max_cap,
                           value=(min_cap, max_cap), key=f"cp{sfx}")
    sel_hh     = st.slider("Hub Height Range (m)",
                           min_value=min_hh, max_value=max_hh,
                           value=(min_hh, max_hh), key=f"hh{sfx}")
    top_n      = st.slider("Top N in Charts", 5, 20, 12, key=f"tn{sfx}")

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    if st.button("↺  Reset All Filters"):
        st.session_state.reset = not st.session_state.reset
        st.rerun()
    if st.session_state.reset:
        st.session_state.reset = False

    st.markdown("""
    <div style="margin-top:32px;font-family:'Space Mono',monospace;
                font-size:8px;letter-spacing:1px;color:#3a5570;line-height:2.4;">
        SOURCE · USGS Wind Turbine Database<br>
        VIA · data.usgs.gov<br>
        LAST UPDATED · 2018<br>
        TURBINES · 58,185 records
    </div>
    """, unsafe_allow_html=True)


# ── APPLY FILTERS ─────────────────────────────────────────────────────────────
filtered = filters.apply_filters(
    df, sel_states, sel_manus, sel_yr, sel_cap, sel_hh
)


# ── HERO ──────────────────────────────────────────────────────────────────────
n_states     = df["t_state"].nunique()
n_manus      = df[df["t_manu"] != "missing"]["t_manu"].nunique()
n_turbines   = len(df)
year_span    = f"{int(df['p_year'].min())}–{int(df['p_year'].max())}"

st.markdown(f"""
<div class="hero">
    <div class="hero-stamp">USGS Wind Turbine Database · Utility-Scale Infrastructure Intelligence</div>
    <div class="hero-title">WIND<span>GRID</span></div>
    <div class="hero-sub">
        Deployment timelines, state fleet profiles, manufacturer data &amp; turbine engineering specs
        for {n_turbines:,} utility-scale turbines installed across {n_states} states between
        1981 and 2018.
    </div>
    <div class="hero-tags">
        <span class="hero-tag">⚡ {n_turbines:,} Turbines</span>
        <span class="hero-tag">📍 {n_states} States</span>
        <span class="hero-tag">🏭 {n_manus} Manufacturers</span>
        <span class="hero-tag">📅 {year_span}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── ACTIVE FILTER BADGES ──────────────────────────────────────────────────────
active = []
if sel_states: active.append(f"📍 {len(sel_states)} state(s)")
if sel_manus:  active.append(f"🏭 {len(sel_manus)} maker(s)")
if sel_yr != (min_yr, max_yr): active.append(f"📅 {sel_yr[0]}–{sel_yr[1]}")
if sel_cap != (min_cap, max_cap): active.append(f"⚡ {sel_cap[0]:,}–{sel_cap[1]:,} kW")
if sel_hh  != (min_hh,  max_hh):  active.append(f"↕ {sel_hh[0]}–{sel_hh[1]} m hub")

if active:
    badges = "".join(f'<span class="fbadge">{a}</span>' for a in active)
    st.markdown(f'<div style="margin-bottom:18px;">{badges}</div>', unsafe_allow_html=True)

if filtered.empty:
    st.warning("No turbines match current filters — try widening the selection.")
    st.stop()


# ── KPI STRIP ─────────────────────────────────────────────────────────────────
n_f          = len(filtered)
n_states_f   = filtered["t_state"].nunique()
valid_yr_f   = filtered["p_year"].dropna()
peak_yr_f    = (valid_yr_f.astype(int).value_counts().idxmax()
                if not valid_yr_f.empty else "—")
avg_cap_f    = filtered[filtered["t_cap"] > 0]["t_cap"].mean()
avg_hh_f     = filtered[filtered["t_hh"] > 0]["t_hh"].mean()
top_manu_f   = (filtered[filtered["t_manu"] != "missing"]["t_manu"]
                .value_counts().idxmax()
                if not filtered[filtered["t_manu"] != "missing"].empty else "—")

st.markdown(f"""
<div class="kpi-strip">
    <div class="kpi-cell">
        <div class="kpi-lbl">Turbines Selected</div>
        <div class="kpi-val">{n_f:,}</div>
        <div class="kpi-sub">across {n_states_f} states</div>
    </div>
    <div class="kpi-cell">
        <div class="kpi-lbl">Avg Capacity</div>
        <div class="kpi-val">{avg_cap_f:,.0f}<span style="font-size:14px;font-weight:400;color:#3a5570"> kW</span></div>
        <div class="kpi-sub">per turbine</div>
    </div>
    <div class="kpi-cell">
        <div class="kpi-lbl">Avg Hub Height</div>
        <div class="kpi-val">{avg_hh_f:.1f}<span style="font-size:14px;font-weight:400;color:#3a5570"> m</span></div>
        <div class="kpi-sub">above ground</div>
    </div>
    <div class="kpi-cell">
        <div class="kpi-lbl">Peak Install Year</div>
        <div class="kpi-val amber">{peak_yr_f}</div>
        <div class="kpi-sub">most turbines installed</div>
    </div>
    <div class="kpi-cell">
        <div class="kpi-lbl">Top Manufacturer</div>
        <div class="kpi-val white">{top_manu_f}</div>
        <div class="kpi-sub">by turbine count</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ── CHART RENDER HELPER ────────────────────────────────────────────────────────
def render(fig, card_title: str, fname: str):
    if fig is None:
        st.caption("Not enough data for this chart.")
        return
    buf = BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight")
    buf.seek(0)
    b64  = base64.b64encode(buf.read()).decode()
    ts   = datetime.now().strftime("%Y%m%d_%H%M%S")
    link = f"data:image/png;base64,{b64}"
    st.markdown(f"""
    <div class="chart-card">
        <div class="chart-card-header">
            <span class="chart-card-title">{card_title}</span>
            <a class="export-link" href="{link}" download="{fname}_{ts}.png">↓ Export PNG</a>
        </div>
        <div class="chart-card-body">
            <img src="{link}" alt="{card_title}" />
        </div>
    </div>
    """, unsafe_allow_html=True)
    plt.close(fig)


# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 01 · FLEET COMMAND
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="sec-wrap">
    <div class="sec-rule-l"></div>
    <span class="sec-num">01</span>
    <span class="sec-title">Fleet Command</span>
    <div class="sec-rule-r"></div>
</div>
""", unsafe_allow_html=True)

c1, c2 = st.columns([1, 1])
with c1:
    render(charts.bar_state_fleet(filtered, top_n),
           "TURBINE COUNT BY STATE", "state_fleet")
with c2:
    render(charts.bar_state_capacity(filtered, top_n),
           "INSTALLED CAPACITY BY STATE (MW)", "state_capacity")

st.markdown("""
<div class="callout">
    <strong>Texas dominates</strong> with over 13,000 turbines — more than the next
    two states combined. <span class="accent">Capacity per turbine</span> varies
    significantly: Oklahoma and North Dakota average above 1,800 kW, while California's
    older fleet pulls its average down. Fleet size doesn't always equal output.
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 02 · DEPLOYMENT TIMELINE
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="sec-wrap">
    <div class="sec-rule-l"></div>
    <span class="sec-num">02</span>
    <span class="sec-title">Deployment Timeline</span>
    <div class="sec-rule-r"></div>
</div>
""", unsafe_allow_html=True)

render(charts.hist_install_year(filtered),
       "ANNUAL TURBINE INSTALLATIONS (1981–2018)", "install_year")

c3, c4 = st.columns([3, 2])
with c3:
    render(charts.line_cumulative(filtered),
           "CUMULATIVE FLEET BUILD-UP", "cumulative_fleet")
with c4:
    render(charts.line_capacity_trend(filtered),
           "AVG TURBINE CAPACITY OVER TIME", "capacity_trend")

st.markdown("""
<div class="callout">
    The <span class="amber">2012 peak</span> of 6,772 installations was driven by
    the federal Production Tax Credit expiry — developers rushed projects to deadline.
    The <strong>2009 boom</strong> followed the American Recovery and Reinvestment Act.
    Average turbine capacity has grown from ~100 kW in the 1980s to over 2 MW by 2018.
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 03 · MANUFACTURER PROFILES
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="sec-wrap">
    <div class="sec-rule-l"></div>
    <span class="sec-num">03</span>
    <span class="sec-title">Manufacturer Profiles</span>
    <div class="sec-rule-r"></div>
</div>
""", unsafe_allow_html=True)

c5, c6 = st.columns([2, 3])
with c5:
    render(charts.bar_manufacturer(filtered, top_n),
           "TURBINE COUNT BY MANUFACTURER", "manu_count")
with c6:
    render(charts.scatter_manu_capacity(filtered),
           "MANUFACTURER SCALE vs AVG CAPACITY", "manu_capacity_scatter")

render(charts.stacked_state_manufacturer(filtered, min(top_n, 10)),
       "MANUFACTURER BREAKDOWN BY TOP STATES", "state_manu_stacked")

st.markdown("""
<div class="callout">
    <strong>GE Wind</strong> commands 38% of the US fleet — nearly twice Vestas.
    <span class="accent">Siemens</span> leads on average capacity, reflecting its
    later market entry with larger offshore-class turbines. Kenetech's early units
    averaged just 160 kW — one-tenth of a modern turbine.
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 04 · TURBINE ENGINEERING
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="sec-wrap">
    <div class="sec-rule-l"></div>
    <span class="sec-num">04</span>
    <span class="sec-title">Turbine Engineering</span>
    <div class="sec-rule-r"></div>
</div>
""", unsafe_allow_html=True)

c7, c8 = st.columns([1, 1])
with c7:
    render(charts.hist_hub_height(filtered),
           "HUB HEIGHT DISTRIBUTION (m)", "hub_height_hist")
with c8:
    render(charts.hist_rotor_diameter(filtered),
           "ROTOR DIAMETER DISTRIBUTION (m)", "rotor_diameter_hist")

render(charts.violin_hh_by_era(filtered),
       "HUB HEIGHT EVOLUTION BY INSTALLATION ERA", "hh_by_era")

st.markdown("""
<div class="callout">
    Modern turbines stand dramatically taller than their 1980s predecessors.
    <strong>Hub height</strong> has risen from ~30m to over 100m, accessing
    stronger, more consistent winds at altitude. Rotor diameter has grown
    proportionally — the <span class="accent">swept area</span> (proportional
    to diameter²) determines how much energy can be captured.
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 05 · CAPACITY LANDSCAPE
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="sec-wrap">
    <div class="sec-rule-l"></div>
    <span class="sec-num">05</span>
    <span class="sec-title">Capacity Landscape</span>
    <div class="sec-rule-r"></div>
</div>
""", unsafe_allow_html=True)

c9, c10 = st.columns([3, 2])
with c9:
    render(charts.scatter_hh_capacity(filtered),
           "HUB HEIGHT vs TURBINE CAPACITY (colour = install year)", "hh_vs_capacity")
with c10:
    render(charts.kde_capacity_by_manu(filtered, min(top_n, 5)),
           "CAPACITY DENSITY BY MANUFACTURER", "kde_capacity")

render(charts.box_capacity_by_state(filtered, min(top_n, 12)),
       "TURBINE CAPACITY DISTRIBUTION BY STATE", "capacity_by_state")

render(charts.bubble_state(filtered),
       "STATE: FLEET SIZE × AVG CAPACITY × HUB HEIGHT", "bubble_state")

st.markdown("""
<div class="callout">
    Hub height and capacity are <strong>strongly correlated</strong> — taller turbines
    extract higher wind speeds and justify larger rotors, which in turn support greater
    generating capacity. The scatter shows this relationship tightening post-2008 as
    <span class="accent">IEC turbine classes</span> standardised design parameters.
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 06 · DATA TERMINAL
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="sec-wrap">
    <div class="sec-rule-l"></div>
    <span class="sec-num">06</span>
    <span class="sec-title">Data Terminal</span>
    <div class="sec-rule-r"></div>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["State Summary", "Turbine Records", "Defect & Missing Analysis"])

with tab1:
    state_summary = (filtered.groupby("t_state")
                     .agg(
                         turbines=("case_id", "count"),
                         avg_cap_kw=("t_cap", lambda x: x[x > 0].mean()),
                         total_mw=("t_cap", lambda x: x[x > 0].sum() / 1000),
                         avg_hub_m=("t_hh", lambda x: x[x > 0].mean()),
                         avg_rotor_m=("t_rd", lambda x: x[x > 0].mean()),
                         first_yr=("p_year", "min"),
                         last_yr=("p_year", "max"),
                         manufacturers=("t_manu", "nunique"),
                     )
                     .round(1)
                     .sort_values("turbines", ascending=False)
                     .reset_index())
    state_summary.columns = [
        "State", "Turbines", "Avg Cap (kW)", "Total MW",
        "Avg Hub (m)", "Avg Rotor (m)", "First Yr", "Last Yr", "Manufacturers",
    ]
    st.dataframe(state_summary, use_container_width=True, height=400)

    csv_state = state_summary.to_csv(index=False).encode("utf-8")
    st.download_button(
        "↓ Download State Summary CSV",
        data=csv_state,
        file_name="windgrid_state_summary.csv",
        mime="text/csv",
    )

with tab2:
    display_cols = [
        "t_state", "t_county", "p_name", "p_year",
        "t_manu", "t_model", "t_cap", "t_hh", "t_rd", "t_ttlh",
        "xlong", "ylat",
    ]
    available = [c for c in display_cols if c in filtered.columns]
    st.dataframe(
        filtered[available].rename(columns={
            "t_state": "State", "t_county": "County",
            "p_name": "Project", "p_year": "Year",
            "t_manu": "Manufacturer", "t_model": "Model",
            "t_cap": "Cap (kW)", "t_hh": "Hub Ht (m)",
            "t_rd": "Rotor Dia (m)", "t_ttlh": "Total Ht (m)",
            "xlong": "Longitude", "ylat": "Latitude",
        }),
        use_container_width=True,
        height=400,
    )
    csv_records = filtered[available].to_csv(index=False).encode("utf-8")
    st.download_button(
        "↓ Download Filtered Records CSV",
        data=csv_records,
        file_name="windgrid_filtered_turbines.csv",
        mime="text/csv",
    )

with tab3:
    st.markdown("""
    <div style="font-family:'Space Mono',monospace;font-size:9px;
                letter-spacing:2px;color:#3a5570;margin-bottom:12px;">
        MISSING / SENTINEL (-9999) ANALYSIS
    </div>
    """, unsafe_allow_html=True)

    key_cols = {
        "t_hh":    "Hub Height (m)",
        "t_rd":    "Rotor Diameter (m)",
        "t_ttlh":  "Total Height (m)",
        "t_cap":   "Capacity (kW)",
        "t_model": "Turbine Model",
        "p_year":  "Install Year",
    }
    rows = []
    for col, label in key_cols.items():
        if col not in filtered.columns:
            continue
        total   = len(filtered)
        missing = filtered[col].isna().sum()
        pct     = missing / total * 100 if total > 0 else 0
        rows.append({
            "Field": label,
            "Total": total,
            "Missing / Unknown": missing,
            "Coverage %": f"{100 - pct:.1f}%",
            "Status": "✓ Good" if pct < 15 else "⚠ Partial" if pct < 40 else "✗ Sparse",
        })

    defect_df = pd.DataFrame(rows)
    st.dataframe(defect_df, use_container_width=True, hide_index=True)

    # Turbine model missing breakdown by manufacturer
    if "t_manu" in filtered.columns and "t_model" in filtered.columns:
        model_missing = (filtered[filtered["t_manu"] != "missing"]
                         .groupby("t_manu")
                         .apply(lambda g: (g["t_model"] == "missing").sum() / len(g) * 100)
                         .sort_values(ascending=False)
                         .head(10)
                         .reset_index())
        model_missing.columns = ["Manufacturer", "Model Missing %"]
        model_missing["Model Missing %"] = model_missing["Model Missing %"].round(1)
        st.markdown("""
        <div style="font-family:'Space Mono',monospace;font-size:9px;
                    letter-spacing:2px;color:#3a5570;margin:18px 0 10px;">
            MODEL FIELD COVERAGE BY MANUFACTURER
        </div>
        """, unsafe_allow_html=True)
        st.dataframe(model_missing, use_container_width=True, hide_index=True)


# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="footer">
    <div class="footer-brand">WINDGRID</div>
    <div class="footer-meta">
        USGS Wind Turbine Database · data.usgs.gov ·
        {len(filtered):,} records displayed ·
        Generated {datetime.now().strftime("%Y-%m-%d %H:%M")}
    </div>
</div>
""", unsafe_allow_html=True)
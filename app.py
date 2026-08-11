import streamlit as st
from config import get_sector_book, sector_book_options

st.set_page_config(
    page_title="Executive Board Glass Command Surface",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# 1. TOTAL STEALTH CSS OVERRIDE (Eradicates Manage App, Header, Footer & Badges)
# -----------------------------------------------------------------------------
st.markdown("""
    <style>
    /* Absolute Hide for Streamlit Host Chrome, Header, Footer, Watermarks & Manage App Badge */
    header, footer, #MainMenu, .stDeployButton, 
    [data-testid="stHeader"], 
    [data-testid="stToolbar"], 
    [data-testid="stDecoration"], 
    [data-testid="stStatusWidget"], 
    [data-testid="stAppDeployButton"],
    [data-testid="stSidebarNav"],
    [data-testid="manage-app-button"],
    .viewerBadge_container__1A53K,
    div[class*="viewerBadge"],
    div[class*="styles_viewerBadge"],
    button[title*="Manage app"],
    div[data-testid="stAppViewBlockContainer"] > header {
        visibility: hidden !important;
        display: none !important;
        height: 0px !important;
    }

    /* Bottom-right host badges (Streamlit Cloud viewer / GitHub watermark) */
    #GithubIcon,
    [class*="viewerBadge"],
    [class*="ViewerBadge"],
    [class*="styles_viewerBadge"],
    a[data-testid="viewerBadge"],
    .viewerBadge_container__1QSob,
    .styles_viewerBadge__1yB5_,
    .viewerBadge_link__1S137,
    .viewerBadge_text__1JaDK,
    a[href*="share.streamlit.io"],
    a[href^="https://streamlit.io"],
    a[href^="https://www.streamlit.io"] {
        visibility: hidden !important;
        display: none !important;
        opacity: 0 !important;
        pointer-events: none !important;
        height: 0 !important;
        width: 0 !important;
        overflow: hidden !important;
    }

    /* Board Glass Theme Styling */
    .stApp { background-color: #0b0f17; color: #e6edf3; }
    .main-title { font-size: 2.1rem; font-weight: 800; color: #ffffff; margin-bottom: 1.2rem; }
    
    .bridge-banner { 
        background-color: #0d1e36; 
        border-left: 4px solid #2f81f7; 
        padding: 1rem 1.2rem; 
        border-radius: 6px; 
        margin-bottom: 1.2rem; 
    }
    .bridge-title { color: #58a6ff; font-size: 0.8rem; font-weight: 700; text-transform: uppercase; margin-bottom: 0.2rem; }
    .bridge-text { color: #a5d6ff; font-size: 0.92rem; line-height: 1.4; }

    .metric-card { 
        background-color: #131d2a; 
        border: 1px solid #213043; 
        border-radius: 8px; 
        padding: 1.25rem; 
        height: 100%; 
    }
    .metric-label { font-size: 0.85rem; font-weight: 600; color: #8b949e; margin-bottom: 0.4rem; }
    .metric-value { font-size: 2.1rem; font-weight: 800; color: #ffffff; margin-bottom: 0.6rem; }
    .metric-basis { font-size: 0.78rem; color: #6e7681; }

    /* Active Executive Directive HUD Box */
    .directive-box {
        background-color: #0a192f;
        border: 1px solid #1e3a8a;
        border-radius: 8px;
        padding: 1.2rem;
        margin-top: 1.2rem;
        margin-bottom: 1.2rem;
    }
    .directive-title { font-size: 0.85rem; font-weight: 700; color: #38bdf8; text-transform: uppercase; margin-bottom: 0.4rem; }
    .directive-text { font-size: 1.05rem; font-weight: 700; color: #ffffff; margin-bottom: 0.8rem; }
    .directive-stats { font-size: 0.88rem; color: #94a3b8; display: flex; gap: 1.5rem; margin-bottom: 0.6rem; }
    .directive-stat-highlight { color: #4ade80; font-weight: 700; }

    .footer-source { 
        background-color: #0b1626; 
        border: 1px solid #1e2d42; 
        padding: 0.6rem 1rem; 
        border-radius: 6px; 
        font-size: 0.82rem; 
        color: #58a6ff; 
        margin-top: 1.5rem; 
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. SIDEBAR ROUTER (TOP 12 SECTOR MASTER LIST)
# -----------------------------------------------------------------------------
st.sidebar.title("Executive Navigation")
st.sidebar.markdown("**Active Sector Surface**")
options = sector_book_options()
selected_key = st.sidebar.selectbox(
    "Select Sector Book",
    options=list(options.keys()),
    format_func=lambda x: options[x],
    label_visibility="collapsed"
)

data = get_sector_book(selected_key)

# -----------------------------------------------------------------------------
# 3. HEADER & OPERATIONAL BRIDGE
# -----------------------------------------------------------------------------
st.markdown(f'<div class="main-title">{data["title"]}</div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="bridge-banner">
    <div class="bridge-title">⚡ DIRECT OPERATIONAL BRIDGE</div>
    <div class="bridge-text">{data["bridge_text"]}</div>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 4. LAYER 1: 3-KPI STRUCTURAL MIRROR CARDS
# -----------------------------------------------------------------------------
col1, col2, col3 = st.columns(3)
cols = [col1, col2, col3]

for col, m in zip(cols, data["metrics"]):
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{m['label']} 🛈</div>
            <div class="metric-value">{m['value']}</div>
            <div class="metric-basis">📊 Basis: {m['basis']}</div>
        </div>
        """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 5. CLOSED-LOOP ACTIVE DIRECTIVE TELEMETRY HUD (BOARD COMMAND LEVEL)
# -----------------------------------------------------------------------------
ad = data.get("active_directive", {})
if ad:
    st.markdown(f"""
    <div class="directive-box">
        <div class="directive-title">⚡ TIER 1: ACTIVE EXECUTIVE DIRECTIVE TELEMETRY</div>
        <div class="directive-text">{ad['title']}</div>
        <div class="directive-stats">
            <span>Progress: <span class="directive-stat-highlight">{ad['completion_pct']}% Executed</span></span>
            <span>Compliant Units: <span class="directive-stat-highlight">{ad['compliant_units']}</span></span>
            <span>Weekly Burn Reclaimed: <span class="directive-stat-highlight">{ad['burn_reclaimed']}</span></span>
            <span>Elapsed: {ad['days_active']} Days</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.progress(ad['completion_pct'] / 100.0)

# -----------------------------------------------------------------------------
# 6. TIER 2 & 3: MANAGER OPERATIONAL DRIFT & ACTIONABLE CLEARANCE
# -----------------------------------------------------------------------------
with st.expander("🔍 TIER 2 & 3: Manager Operational View — Inspect Site Drift & Execute Clearance", expanded=True):
    st.markdown("### 📊 Operational Unit Breakdown")
    l2_data = data.get("layer2_operations", [])
    if l2_data:
        st.table(l2_data)
    
    st.markdown("---")
    st.markdown("### ⚡ Layer 3: Executive Action Trigger")
    st.info("Override administrative queue friction and issue immediate compliance sign-off.")
    if st.button("Execute Immediate Operational Clearance Directive"):
        st.success(f"Clearance Directive Logged for {selected_key}. Ground-Truth Telemetry updated.")

# -----------------------------------------------------------------------------
# 7. FOOTER GROUND-TRUTH CITATION
# -----------------------------------------------------------------------------
st.markdown(f'<div class="footer-source">{data["footer"]}</div>', unsafe_allow_html=True)

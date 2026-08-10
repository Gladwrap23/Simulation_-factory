import streamlit as st

# ==============================================================================
# 1. PAGE CONFIGURATION
# ==============================================================================
st.set_page_config(
    page_title="ACC Executive Synthesis & Knowledge Engine",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==============================================================================
# 2. CUSTOM EXECUTIVE DARK THEME CSS
# ==============================================================================
st.markdown("""
    <style>
    /* Dark Background & Typography */
    .stApp {
        background-color: #0b0f17;
        color: #e6edf3;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    /* Executive Header */
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 1.5rem;
    }
    
    /* Direct Operational Bridge Callout Banner */
    .bridge-banner {
        background-color: #0d1e36;
        border-left: 4px solid #2f81f7;
        padding: 1.1rem 1.3rem;
        border-radius: 6px;
        margin-bottom: 1.2rem;
    }
    .bridge-title {
        color: #58a6ff;
        font-size: 0.85rem;
        font-weight: 700;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        margin-bottom: 0.3rem;
    }
    .bridge-text {
        color: #a5d6ff;
        font-size: 0.95rem;
        line-height: 1.5;
    }
    
    /* Section Headers */
    .section-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #ffffff;
        margin-top: 2rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Stat Metric Cards */
    .metric-card {
        background-color: #131d2a;
        border: 1px solid #213043;
        border-radius: 8px;
        padding: 1.25rem;
        height: 100%;
    }
    .metric-label {
        font-size: 0.85rem;
        font-weight: 600;
        color: #8b949e;
        margin-bottom: 0.5rem;
    }
    .metric-value {
        font-size: 2.3rem;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: -0.5px;
        margin-bottom: 0.8rem;
    }
    .metric-basis {
        font-size: 0.78rem;
        color: #6e7681;
        display: flex;
        align-items: center;
        gap: 0.3rem;
    }
    
    /* Navigation / Action Button Styling */
    .stButton>button {
        width: 100%;
        background-color: #161f2e;
        color: #c9d1d9;
        border: 1px solid #30363d;
        border-radius: 6px;
        padding: 0.6rem;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background-color: #1f2d42;
        color: #ffffff;
        border-color: #58a6ff;
    }
    
    /* Footer Source Banner */
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

# ==============================================================================
# 3. APP HEADER
# ==============================================================================
st.markdown('<div class="main-title">🧠 ACC Executive Synthesis & Knowledge Engine</div>', unsafe_allow_html=True)

# ==============================================================================
# 4. DIRECT OPERATIONAL BRIDGE BANNER
# ==============================================================================
st.markdown("""
<div class="bridge-banner">
    <div class="bridge-title">⚡ DIRECT OPERATIONAL BRIDGE</div>
    <div class="bridge-text">
        Synthesis reconciles 100% of National Drift ($420k/wk): Northern $320k/wk (76.2%), Midland $40k/wk (9.5%), Central $30k/wk (7.1%), South Island incl. Nelson $30k/wk (7.1%).
    </div>
</div>
""", unsafe_allow_html=True)

# Return Button
if st.button("🏛️ Return to Ministerial Boardroom"):
    st.info("Navigating back to Ministerial Boardroom...")

# ==============================================================================
# 5. STATUTORY BASELINE KNOWLEDGE BASE (METRIC CARDS)
# ==============================================================================
st.markdown('<div class="section-title">📚 Statutory Baseline Knowledge Base (Public Disclosures)</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Total Outstanding Claims Liability (OCL) 🛈</div>
        <div class="metric-value">$63.6 Billion</div>
        <div class="metric-basis">📊 Basis: ACC Actuarial Valuation Disclosures</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Annual New-Year Cost Gap 🛈</div>
        <div class="metric-value">$2.556 Billion</div>
        <div class="metric-basis">📊 Basis: Annual Scheme Underwriting Disclosures</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Cumulative Influenceable OCL Strain 🛈</div>
        <div class="metric-value">$1.209 Billion</div>
        <div class="metric-basis">📊 Basis: 5-Year Financial Condition Report Summary</div>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# 6. EXECUTIVE SYNTHESIS SURFACE (TABS)
# ==============================================================================
st.markdown('<div class="section-title">🎬 Executive Audio Briefing & Synthesis Surface</div>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🟩 NotebookLM Knowledge Synthesis", "📽️ Executive Avatar Briefing"])

with tab1:
    st.markdown("### NotebookLM Ground-Truth Audio & Text Synthesis")
    st.write("Ingested baseline analysis from the 2025 ACC Financial Condition Report.")
    # Place audio player or markdown transcript here
    # st.audio("path_to_audio.mp3")

with tab2:
    st.markdown("### Executive Avatar Video Briefing")
    st.write("AI Generated Ministerial Video Briefing Surface.")
    # Place video player here
    # st.video("path_to_video.mp4")

# ==============================================================================
# 7. FOOTER GROUND-TRUTH BAR
# ==============================================================================
st.markdown("""
<div class="footer-source">
    💡 Ground-Truth Source: Ingested 2025 ACC Financial Condition Report & Live Telemetry Feed.
</div>
""", unsafe_allow_html=True)


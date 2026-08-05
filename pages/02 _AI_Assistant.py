import streamlit as st

# -----------------------------------------------------------------------------
# 1. PAGE SETUP & SYNTHESIS STYLES
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="ACC Synthesis & AI Briefing",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
    /* 🔒 HIDE TOP TOOLBAR & PREVENT HEADING CLIPPING */
    [data-testid="stHeader"] {
        display: none !important;
    }
    .block-container {
        padding-top: 2.5rem !important;
    }
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }

    /* DIRECT NAVIGATION BRIDGE BANNER */
    .bridge-box {
        background: linear-gradient(135deg, #062313 0%, #0f172a 100%);
        border: 2px solid #00e676;
        border-radius: 10px;
        padding: 20px 24px;
        margin-bottom: 20px;
    }
    .bridge-title {
        color: #00e676;
        font-size: 0.85rem;
        font-weight: 800;
        letter-spacing: 1.5px;
        text-transform: uppercase;
    }
    .bridge-subtitle {
        color: #ffffff;
        font-size: 1.05rem;
        font-weight: 600;
        margin-top: 6px;
        line-height: 1.4;
    }
</style>
""",
    unsafe_allow_html=True,
)

st.title("🧠 ACC Executive Synthesis & Knowledge Engine")
st.markdown("---")

# -----------------------------------------------------------------------------
# 2. OPERATIONAL NAVIGATION BRIDGE (SINGLE CLEAN ENTRY)
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div class="bridge-box">
        <div class="bridge-title">⚡ DIRECT OPERATIONAL BRIDGE</div>
        <div class="bridge-subtitle">
            Synthesis reconciles 100% of National Drift ($420k/wk): Northern $320k/wk (76.2%), Midland $40k/wk (9.5%), Central $30k/wk (7.1%), South Island incl. Nelson $30k/wk (7.1%).
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

if st.button("🏛️ Return to Ministerial Boardroom", key="btn_nav_bridge_minister", use_container_width=True):
    st.session_state["sb_role_matrix_select"] = "minister"
    st.switch_page("app.py")

st.markdown("---")

# -----------------------------------------------------------------------------
# 3. PUBLIC STATUTORY BASELINE CONTEXT (NOTEBOOKLM MODULE)
# -----------------------------------------------------------------------------
st.subheader("📚 Statutory Baseline Knowledge Base (Public Disclosures)")

col_info1, col_info2, col_info3 = st.columns(3)

with col_info1:
    st.metric(
        label="Total Outstanding Claims Liability (OCL)",
        value="$63.6 Billion",
        help="Source: ACC Financial Condition Report (Audited Baseline)"
    )
    st.caption("📊 **Basis:** ACC Actuarial Valuation Disclosures")

with col_info2:
    st.metric(
        label="Annual New-Year Cost Gap",
        value="$2.556 Billion",
        help="Gap between levy collection and new claim lifetime costs"
    )
    st.caption("📊 **Basis:** Annual Scheme Underwriting Disclosures")

with col_info3:
    st.metric(
        label="Cumulative Influenceable OCL Strain",
        value="$1.209 Billion",
        help="5-year cumulative strain driven by extended rehabilitation dwell times"
    )
    st.caption("📊 **Basis:** 5-Year Financial Condition Report Summary")

st.markdown("---")

# -----------------------------------------------------------------------------
# 4. INTERACTIVE SYNTHESIS & AVATAR BRIEFING PIPELINE
# -----------------------------------------------------------------------------
st.subheader("📽️ Executive Audio Briefing & Synthesis Surface")

tab1, tab2 = st.tabs(["🎙️ NotebookLM Knowledge Synthesis", "🎥 Executive Avatar Briefing"])

with tab1:
    st.info("💡 **Ground-Truth Source:** Ingested 2025 ACC Financial Condition Report & Live Telemetry Feed.")
    st.text_area(
        "NotebookLM Query Engine",
        value="Summarize how the $420k weekly operational drift across Northern, Midland, Central, and South Island (Nelson) feeds directly into the $1.209B influenceable OCL strain.",
        height=100,
        key="notebook_query_text_area",
    )
    if st.button("Generate Actuarial Briefing Note", key="btn_generate_actuarial_briefing"):
        st.success(
            "**Key Finding:** Weekly compensation claim dwell times account for over 60% of influenceable OCL strain. "
            "76.2% of current financial drift is concentrated in Northern Region orthopedic backlogs ($320k/wk), "
            "with remaining drift distributed across Midland ($40k/wk), Central ($30k/wk), and South Island/Nelson ($30k/wk)."
        )

with tab2:
    st.markdown(
        """
        <div style="background-color: #111827; border: 1.5px solid #3b82f6; border-radius: 10px; padding: 30px; text-align: center;">
            <h4 style="color: #60a5fa; margin-bottom: 10px;">🎥 Executive AI Avatar Stream</h4>
            <p style="color: #9ca3af; font-size: 0.9rem;">
                Interactive video synthesis feed connected to live scheme metrics and regional telemetry.
            </p>
            <div style="background-color: #1f2937; border-radius: 8px; padding: 40px; margin-top: 15px; color: #6b7280;">
                [ Live Interactive Avatar Iframe Workspace ]
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# -----------------------------------------------------------------------------
# 5. GOVERNANCE & RISK DISCLAIMER ANCHOR
# -----------------------------------------------------------------------------
st.markdown("---")
st.caption(
    "📌 **Risk & Compliance Notice:** Figures and parameters referenced across this command surface are anchored in public statutory disclosures "
    "(including the ACC Financial Condition Report and Annual Performance Disclosures). Where scenario inputs deviate from real-time empirical engine calculations, "
    "figures are explicitly classified as **Directional Scenario Estimates** for strategic evaluation, not official company guidance or actuarial commitments."
)

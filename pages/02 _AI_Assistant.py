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
    /* 🔒 HIDE TOP TOOLBAR & STREAMLIT HEADER */
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
        font-size: 1.1rem;
        font-weight: 600;
        margin-top: 6px;
    }
</style>
""",
    unsafe_allow_html=True,
)

st.title("🧠 ACC Executive Synthesis & Knowledge Engine")
st.markdown("---")

# -----------------------------------------------------------------------------
# 2. OPERATIONAL NAVIGATION BRIDGE (DIRECT TARGET: NORTHERN REGION)
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div class="bridge-box">
        <div class="bridge-title">⚡ DIRECT OPERATIONAL BRIDGE</div>
        <div class="bridge-subtitle">Synthesis pinpoints 76% ($320k/wk) of national drift concentrated in Northern Region (Auckland / Whangārei).</div>
    </div>
    """,
    unsafe_allow_html=True,
)

col_b1, col_b2 = st.columns([2, 1])
with col_b1:
    if st.button("🚀 Launch Operational Command Glass: Northern Region (RGM)", key="btn_nav_bridge_rgm_north", use_container_width=True):
        st.query_params["role"] = "rgm_north"
        st.switch_page("app.py")

with col_b2:
    if st.button("🏛️ Return to Ministerial Boardroom", key="btn_nav_bridge_minister", use_container_width=True):
        st.query_params["role"] = "minister"
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
    st.info("💡 **Ground-Truth Source:** Ingested 2025 ACC Financial Condition Report & Treasury Fiscal Review Disclosures.")
    st.text_area(
        "NotebookLM Query Engine",
        value="Summarize the primary drivers of the $1.209B influenceable OCL strain and how weekly compensation dwell times affect overall scheme solvency.",
        height=100,
        key="notebook_query_text_area",
    )
    if st.button("Generate Actuarial Briefing Note", key="btn_generate_actuarial_briefing"):
        st.success(
            "**Key Finding:** Weekly compensation claim dwell times account for over 60% of influenceable OCL strain. "
            "Re-routing orthopedic assessment capacity in metro Auckland directly mitigates extended weekly payout liabilities."
        )

with tab2:
    st.markdown(
        """
        <div style="background-color: #111827; border: 1.5px solid #3b82f6; border-radius: 10px; padding: 30px; text-align: center;">
            <h4 style="color: #60a5fa; margin-bottom: 10px;">🎥 Executive AI Avatar Stream</h4>
            <p style="color: #9ca3af; font-size: 0.9rem;">
                Interactive video synthesis feed connected to live scheme metrics.
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

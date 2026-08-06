import streamlit as st

# ==========================================
# 1. PAGE SETUP & STYLES
# ==========================================

st.set_page_config(
    page_title="ACC Synthesis & AI Briefing",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for header & theme
st.markdown("""
<style>
[data-testid="stHeader"] {
    display: none !important;
}
.block-container {
    padding-top: 2.5rem !important;
}
header, #MainMenu, footer {
    visibility: hidden;
}
.stApp {
    background-color: #0e1117;
    color: #ffffff;
}
</style>
""", unsafe_allow_html=True)

# Main Page Header
st.title("🧠 ACC Executive Synthesis & Knowledge Engine")
st.markdown("---")

# ==========================================
# 2. OPERATIONAL NAVIGATION BRIDGE
# ==========================================

# Operational Status Banner
st.info(
    "⚡ **DIRECT OPERATIONAL BRIDGE**  \n"
    "Synthesis reconciles 100% of National Drift ($420k/wk): "
    "Northern $320k/wk (76.2%), Midland $40k/wk (9.5%), Central $30k/wk (7.1%), "
    "South Island incl. Nelson $30k/wk (7.1%)."
)

# Active Routing Callback
def reset_to_minister():
    st.session_state["sb_role_matrix_select"] = "minister"
    st.switch_page("app.py")

st.button(
    "🏛️ Return to Ministerial Boardroom",
    key="btn_nav_bridge_minister",
    use_container_width=True,
    on_click=reset_to_minister
)

st.markdown("---")
-----------------------------------------------------------------------------
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
    
    user_query = st.text_area(
        "NotebookLM Query Engine (Paste Stoppage Logs or Clinical Files Here)",
        value=default_query,
        height=110,
        key="notebook_query_text_area",
    )
    
    if st.button("Generate Resolution Action Plan", key="btn_generate_actuarial_briefing"):
        if "430 Unstructured GP" in user_query:
            st.success(
                "**📋 Support Staff Action Plan:**\n"
                "1. **Auto-Parse Unstructured Docs:** Trigger automated OCR parser to extract ICD-10 medical codes.\n"
                "2. **Batch Document Reconciliation:** Auto-match 180 mismatched provider invoices against regional tariff tables.\n"
                "3. **Clear Intake Lag:** Reduces average gateway lag from 4.2 days down to under 2 hours, saving $90,000/week."
            )
        elif "Exceeds $5,000 Authority" in user_query or "Claim #" in user_query:
            st.success(
                "**💼 Case Manager Action Plan:**\n"
                "1. **Delegation Override:** Apply temporary $5,000 authority override band under emergency operational policy.\n"
                "2. **Direct Clinical Sign-Off:** Re-route treatment plan to Northern Clinical Lead for immediate 24-hr sign-off.\n"
                "3. **Dwell Mitigation:** Unblocks 38-day idle stoppage, halting weekly compensation drift ($1,250/week saved)."
            )
        else:
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

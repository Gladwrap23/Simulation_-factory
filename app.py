import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AAT Phoenix Command Post",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 1. SECTOR DEFINITIONS & DICTIONARY ---
SECTORS = {
    "ACC": {"name": "ACC Baseline · NZ Scheme Book", "title": "ACC Executive Synthesis & Knowledge Engine", "var": "$63.6 Billion", "drift": "$2.556 Billion", "acl": "$1.209 Billion"},
    "PJM": {"name": "Grid PJM · Interconnection Book", "title": "PJM Infrastructure Capital & Interconnection Command Post", "var": "$35.3 Million", "drift": "$17.68 Million", "acl": "$340,000 / wk"},
    "BIOPHARMA": {"name": "Biopharma Clarity · GMP Book", "title": "Biopharma Sovereign GMP Command Post", "var": "$142.0 Million", "drift": "$18.40 Million", "acl": "$850,000 / wk"},
    "DEFENSE": {"name": "Defense & Aerospace · Sovereign Book", "title": "Sovereign Defense Fleet & Readiness Command Post", "var": "$510.0 Million", "drift": "$42.10 Million", "acl": "$2.100 Million / wk"},
    "ERCOT": {"name": "ERCOT Energy · Storage Book", "title": "ERCOT Grid Storage & Load Command Post", "var": "$88.5 Million", "drift": "$12.30 Million", "acl": "$610,000 / wk"},
    "APRA": {"name": "APRA Banking · Prudential Book", "title": "APRA Capital Reserve & Risk Command Post", "var": "$1.20 Billion", "drift": "$95.00 Million", "acl": "$4.500 Million / wk"},
    "PORT": {"name": "Port Logistics · Freight Book", "title": "Port Freight Velocity & Logistics Command Post", "var": "$64.0 Million", "drift": "$8.20 Million", "acl": "$410,000 / wk"},
    "NHS": {"name": "NHS Recovery · Surgical Book", "title": "NHS Surgical Hub Operations Command Post", "var": "£210.0 Million", "drift": "£31.50 Million", "acl": "£1.150 Million / wk"}
}

# --- 2. URL PARAMETER ROUTING & SESSION LOCK ---
params = st.query_params
url_co = params.get("co", "PJM").upper()

if url_co not in SECTORS:
    url_co = "PJM"

# Lock the authorized company into session state based on incoming URL parameter
if "authorized_co" not in st.session_state:
    st.session_state["authorized_co"] = url_co

# --- 3. SIDEBAR EXECUTIVE NAVIGATION (PEER ROSTER) ---
st.sidebar.title("Executive Navigation")
st.sidebar.caption("Active Enterprise Surfaces")

selected_key = st.sidebar.selectbox(
    "Select Enterprise Surface",
    options=list(SECTORS.keys()),
    format_func=lambda x: SECTORS[x]["name"],
    index=list(SECTORS.keys()).index(url_co)
)

# Active target data
active_data = SECTORS[selected_key]
is_authorized = (selected_key == st.session_state["authorized_co"])

# --- 4. HEADER: COMMAND POST BRANDING ---
st.title(f"🎯 {active_data['title']}")

# --- 5. PEER LOCK SECURITY GATE (IF OTHER COMPANY CLICKED) ---
if not is_authorized:
    st.markdown("---")
    st.error("🔒 EXECUTIVE SECURITY GATE: MULTI-TENANT ISOLATION ACTIVE")
    st.warning(
        f"**Restricted Access:** You are attempting to inspect **{active_data['name']}**.\n\n"
        "Multi-tenant governance is enforced. Access to this specific command surface requires "
        "an authorized executive clearance key for this enterprise.\n\n"
        "*Your primary authorized command post remains accessible via your designated link.*"
    )
    st.info("💡 **Enterprise Social Proof:** All 12 Tier-1 sectors are actively monitored under the Predictive Equilibrium Engine.")
    st.stop()  # Halt rendering for unauthorized peer selection

# --- 6. TIER 1: EXECUTIVE BOARD GLASS (OPEN BY DEFAULT) ---
st.markdown("---")
st.subheader("⚡ Tier 1: Active Executive Directive Telemetry")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Macro Valuation at Risk 🔒", active_data["var"], help="Basis: Total OCL Disclosures")
with col2:
    st.metric("Annual Velocity Drift Cost 🔒", active_data["drift"], help="Basis: Interconnection Queue Dwell Drag")
with col3:
    st.metric("Actionable Controllable Loss 🔒", active_data["acl"], help="Basis: Redundant Manual Study Re-Keying")

# Direct Operational Bridge Directive Banner
st.info("⚡ **DIRECT OPERATIONAL BRIDGE:** Synthesis reconciles 100% of Active Interconnection Drift: Regional Re-Study Backlogs (72%), Substation Lags (18%), Environmental Clearance (10%).")

# --- 7. TIERS 2 & 3: MANAGER OPERATIONAL VIEW (TEASER / ON DEMAND GATE) ---
st.markdown("---")
with st.expander("🔒 TIER 2 & 3: Operational Interconnects Available On Demand (Clearance Required)", expanded=False):
    st.markdown("### 🔍 Site Drift & Operational Unit Breakdown")
    st.warning("💡 **Executive Teaser Mode:** Site-level operational unit breakdowns and sub-second clearance execution triggers are gated for live client onboarding.")
    
    # Optional Password Unlock
    passcode = st.text_input("Enter Executive Passcode to Unlock Operational Layer:", type="password")
    if passcode == "COMMAND2026":
        st.success("Clearance Granted. Operational Unit Breakdown Unlocked.")
        st.table([
            {"Site": "Substation Alpha (Zone 4)", "Drift": "+6.1 Wks", "Burn": "$150k/wk", "Bottleneck": "Manual FERC Re-Study Queue"},
            {"Site": "Substation Beta (Zone 2)", "Drift": "+3.4 Wks", "Burn": "$110k/wk", "Bottleneck": "Paper Land Retainer Audit"},
            {"Site": "Substation Gamma (Zone 1)", "Drift": "+2.0 Wks", "Burn": "$80k/wk", "Bottleneck": "Sequential Environmental Sign-off"}
        ])
        if st.button("Execute Immediate Operational Clearance Directive"):
            st.balloons()
            st.success("Operational clearance directive dispatched to regional hubs.")

# --- 8. NOTEBOOK LANE & EXECUTIVE PROMPTING ---
st.markdown("---")
with st.expander("🧠 Notebook Lane & Executive Prompting Engine", expanded=True):
    st.markdown("### Executive Synthesis & Direct Query Interface")
    user_query = st.text_input("Ask the Predictive Equilibrium Engine:", placeholder="e.g., What is the 90-day drift cost if Substation Alpha clearance lags by 2 weeks?")
    if user_query:
        st.info(f"**Synthesizing response for query:** '{user_query}'...")
        st.write("✨ *Analysis:* Operational drift in Zone 4 impacts CapEx velocity by $150k/wk. Clearance directive recommended.")

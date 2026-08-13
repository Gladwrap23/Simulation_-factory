import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AAT Phoenix Command Post",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CLEAN ENTERPRISE STYLING (WHITE-LABEL: HIDE GITHUB ICON, HEADER, FOOTER, MENU & SIDEBAR NAV) ---
hide_streamlit_style = """
    <style>
        header {visibility: hidden !important;}
        footer {visibility: hidden !important;}
        #MainMenu {visibility: hidden !important;}
        [data-testid="stSidebarNav"] {display: none !important;}
        .stAppHeader {display: none !important;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# --- 1. SECTOR DEFINITIONS & DICTIONARY ---
SECTORS = {
    "PJM": {
        "name": "Grid PJM · Interconnection Book",
        "title": "PJM Infrastructure Capital & Interconnection Command Post",
        "var": "$35.3 Million",
        "drift": "$17.68 Million",
        "acl": "$340,000 / wk",
        "bridge": "Synthesis reconciles 100% of Active Interconnection Drift: Regional Re-Study Backlogs (72%), Substation Lags (18%), Environmental Clearance (10%).",
        "sites": [
            {"Site": "Substation Alpha (Zone 4)", "Drift": "+6.1 Wks", "Burn": "$150k/wk", "Bottleneck": "Manual FERC Re-Study Queue"},
            {"Site": "Substation Beta (Zone 2)", "Drift": "+3.4 Wks", "Burn": "$110k/wk", "Bottleneck": "Paper Land Retainer Audit"},
            {"Site": "Substation Gamma (Zone 1)", "Drift": "+2.0 Wks", "Burn": "$80k/wk", "Bottleneck": "Sequential Environmental Sign-off"}
        ]
    },
    "ACC": {
        "name": "ACC Baseline · NZ Scheme Book",
        "title": "ACC Executive Synthesis & Knowledge Engine",
        "var": "$63.6 Billion",
        "drift": "$2.556 Billion",
        "acl": "$1.209 Billion",
        "bridge": "Synthesis reconciles 100% of National Drift ($420k/wk): Northern $320k/wk (76.2%), Midland $40k/wk (9.5%), Central $30k/wk (7.1%), South Island $30k/wk (7.1%).",
        "sites": [
            {"Site": "Northern Hub 01", "Drift": "+4.2 Wks", "Burn": "$180k/wk", "Bottleneck": "Manual Medical Paper Verification"},
            {"Site": "Midland Hub 02", "Drift": "+1.8 Wks", "Burn": "$40k/wk", "Bottleneck": "Sequential Legal Approval Queue"},
            {"Site": "Central Hub 03", "Drift": "+1.2 Wks", "Burn": "$30k/wk", "Bottleneck": "Treatment Pathway Discrepancy Audit"}
        ]
    },
    "BIOPHARMA": {
        "name": "Biopharma Clarity · GMP Book",
        "title": "Biopharma Sovereign GMP Command Post",
        "var": "$142.0 Million",
        "drift": "$18.40 Million",
        "acl": "$850,000 / wk",
        "bridge": "Synthesis reconciles 100% of GMP Batch Release Lags: Sterility Validation Hold (65%), Multi-site Deviation Review (25%), Certificate Processing (10%).",
        "sites": [
            {"Site": "Facility Alpha (Sterile Suite)", "Drift": "+5.1 Wks", "Burn": "$450k/wk", "Bottleneck": "Manual Batch Record Re-Verification"},
            {"Site": "Facility Beta (Formulation)", "Drift": "+2.8 Wks", "Burn": "$280k/wk", "Bottleneck": "Environmental Monitoring Audit"},
            {"Site": "Facility Gamma (Packaging)", "Drift": "+1.1 Wks", "Burn": "$120k/wk", "Bottleneck": "QC Sampling Queue Backup"}
        ]
    },
    "DEFENSE": {
        "name": "Defense & Aerospace · Sovereign Book",
        "title": "Sovereign Defense Fleet & Readiness Command Post",
        "var": "$510.0 Million",
        "drift": "$42.10 Million",
        "acl": "$2.100 Million / wk",
        "bridge": "Synthesis reconciles 100% of Fleet Maintenance Drift: Depot Level Overhaul Backlogs (58%), Avionics Component Sign-off (27%), Supply Chain Sign-off (15%).",
        "sites": [
            {"Site": "Naval Yard Alpha", "Drift": "+8.4 Wks", "Burn": "$1.2M/wk", "Bottleneck": "Hull Structural Certification Queue"},
            {"Site": "Air Base Wing 04", "Drift": "+4.1 Wks", "Burn": "$600k/wk", "Bottleneck": "Avionics Subsystem Retrofit Delay"},
            {"Site": "Logistics Depot Delta", "Drift": "+2.3 Wks", "Burn": "$300k/wk", "Bottleneck": "Sovereign Component Line Audit"}
        ]
    },
    "ERCOT": {
        "name": "ERCOT Energy · Storage Book",
        "title": "ERCOT Grid Storage & Load Command Post",
        "var": "$88.5 Million",
        "drift": "$12.30 Million",
        "acl": "$610,000 / wk",
        "bridge": "Synthesis reconciles 100% of BESS Interconnection Lag: Battery Telemetry Sign-off (55%), Market Substation Audit (30%), Transformer Clearance (15%).",
        "sites": [
            {"Site": "BESS Storage Hub 01", "Drift": "+4.8 Wks", "Burn": "$320k/wk", "Bottleneck": "Telemetry Synchronization Validation"},
            {"Site": "Solar Substation Beta", "Drift": "+3.1 Wks", "Burn": "$190k/wk", "Bottleneck": "Inverter Capacity Testing Queue"}
        ]
    },
    "APRA": {
        "name": "APRA Banking · Prudential Book",
        "title": "APRA Capital Reserve & Risk Command Post",
        "var": "$1.20 Billion",
        "drift": "$95.00 Million",
        "acl": "$4.500 Million / wk",
        "bridge": "Synthesis reconciles 100% of Capital Prudential Drag: Model Validation Delays (60%), Stress Test Re-Keying (25%), Compliance Reporting Lag (15%).",
        "sites": [
            {"Site": "Risk Modeling Hub Alpha", "Drift": "+6.2 Wks", "Burn": "$2.5M/wk", "Bottleneck": "Internal Rating Model Validation"},
            {"Site": "Capital Treasury Unit", "Drift": "+3.0 Wks", "Burn": "$2.0M/wk", "Bottleneck": "Liquidity Stress Testing Re-Keying"}
        ]
    },
    "PORT": {
        "name": "Port Logistics · Freight Book",
        "title": "Port Freight Velocity & Logistics Command Post",
        "var": "$64.0 Million",
        "drift": "$8.20 Million",
        "acl": "$410,000 / wk",
        "bridge": "Synthesis reconciles 100% of Vessel Dwell Time: Crane Clearance Queue (50%), Customs Documentation Lag (35%), Yard Bottlenecks (15%).",
        "sites": [
            {"Site": "Container Terminal 01", "Drift": "+3.9 Wks", "Burn": "$250k/wk", "Bottleneck": "Automated Crane Sync Delay"},
            {"Site": "Freight Rail Hub North", "Drift": "+2.1 Wks", "Burn": "$160k/wk", "Bottleneck": "Customs Paper Manifest Audit"}
        ]
    },
    "NHS": {
        "name": "NHS Recovery · Surgical Book",
        "title": "NHS Surgical Hub Operations Command Post",
        "var": "£210.0 Million",
        "drift": "£31.50 Million",
        "acl": "£1.150 Million / wk",
        "bridge": "Synthesis reconciles 100% of Elective Backlog Drag: Operating Theatre Scheduling (62%), Post-Op Bed Clearance (23%), Diagnostics Sign-off (15%).",
        "sites": [
            {"Site": "Surgical Hub North", "Drift": "+5.5 Wks", "Burn": "£650k/wk", "Bottleneck": "Pre-Op Assessment Paperwork Queue"},
            {"Site": "Regional Infirmary West", "Drift": "+2.9 Wks", "Burn": "£500k/wk", "Bottleneck": "Theatre Capacity Re-Allocation Queue"}
        ]
    }
}

# --- 2. URL PARAMETER ROUTING & SESSION LOCK ---
params = st.query_params
url_co = params.get("co", "PJM").upper()

if url_co not in SECTORS:
    url_co = "PJM"

# Lock authorized sector into session state
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
    st.info("💡 **Enterprise Social Proof:** All Tier-1 sectors are actively monitored under the Predictive Equilibrium Engine.")
    st.stop()  # Halt rendering for unauthorized peer selection

# --- 6. TIER 1: EXECUTIVE BOARD GLASS (OPEN BY DEFAULT) ---
st.markdown("---")
st.subheader("⚡ Tier 1: Active Executive Directive Telemetry")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Macro Valuation at Risk 🔒", active_data["var"], help="Basis: Total Enterprise Exposure")
with col2:
    st.metric("Annual Velocity Drift Cost 🔒", active_data["drift"], help="Basis: Operational Drag Rate")
with col3:
    st.metric("Actionable Controllable Loss 🔒", active_data["acl"], help="Basis: Administrative Friction Drag")

st.info(f"⚡ **DIRECT OPERATIONAL BRIDGE:** {active_data['bridge']}")

# --- 7. TIERS 2 & 3: MANAGER OPERATIONAL VIEW (UNLOCKED & OPEN) ---
st.markdown("---")
with st.expander("🔓 TIER 2 & 3: Operational Unit Breakdown & Interconnects", expanded=True):
    st.markdown("### 🔍 Site Drift & Operational Unit Breakdown")
    
    st.table(active_data["sites"])
    
    if st.button("Execute Immediate Operational Clearance Directive"):
        st.balloons()
        st.success("Operational clearance directive dispatched to regional hubs.")

# --- 8. NOTEBOOK LANE & EXECUTIVE PROMPTING ---
st.markdown("---")
with st.expander("🧠 Notebook Lane & Executive Prompting Engine", expanded=True):
    st.markdown("### Executive Synthesis & Direct Query Interface")
    user_query = st.text_input("Ask the Predictive Equilibrium Engine:", placeholder="e.g., What is the 90-day drift cost if clearance lags by 2 weeks?")
    if user_query:
        st.info(f"**Synthesizing response for query:** '{user_query}'...")
        st.write("✨ *Analysis:* Operational drift in primary units impacts CapEx velocity. Immediate clearance directive recommended.")

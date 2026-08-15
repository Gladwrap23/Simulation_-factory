import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AAT Phoenix Command Post",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CLEAN ENTERPRISE STYLING & CONTROL PLANE GEOMETRY ---
enterprise_styling = """
    <style>
        /* Suppress default headers, footers, hamburger menus, and page navigation */
        footer {visibility: hidden !important;}
        #MainMenu {visibility: hidden !important;}
        [data-testid="stSidebarNav"] {display: none !important;}
        [data-testid="stDecoration"] {display: none !important;}
        [data-testid="stToolbar"] {display: none !important;}
        
        /* Make header pass-through */
        header {background: transparent !important;}
        [data-testid="stHeader"] {background: transparent !important;}

        /* Widen Sidebar into a true Enterprise Control Plane (390px) */
        [data-testid="stSidebar"] {
            min-width: 390px !important;
            max-width: 390px !important;
            background-color: #0d1117 !important;
            border-right: 1px solid #30363d !important;
        }

        /* Enlarge touch targets on sidebar controls for tablet/touch devices */
        .stSelectbox label, .stRadio label, .stSlider label {
            font-size: 1.05rem !important;
            font-weight: 700 !important;
            color: #c9d1d9 !important;
        }

        /* High-Visibility Floating Mobile Sidebar Toggle Button */
        [data-testid="stSidebarCollapsedControl"],
        [data-testid="collapsedControl"],
        button[data-testid="stSidebarCollapseButton"] {
            display: flex !important;
            visibility: visible !important;
            position: fixed !important;
            top: 14px !important;
            left: 20px !important;
            z-index: 999999 !important;
            background-color: #00E5FF !important;
            color: #0d1117 !important;
            border-radius: 8px !important;
            border: 2px solid #00B4D8 !important;
            padding: 4px 8px !important;
            box-shadow: 0px 4px 14px rgba(0, 229, 255, 0.4) !important;
        }
        
        [data-testid="stSidebarCollapsedControl"] svg,
        [data-testid="collapsedControl"] svg {
            fill: #0d1117 !important;
            stroke: #0d1117 !important;
            width: 24px !important;
            height: 24px !important;
        }
    </style>
"""
st.markdown(enterprise_styling, unsafe_allow_html=True)

# --- 1. SECTOR DEFINITIONS & DATA DICTIONARY ---
SECTORS = {
    "PJM": {
        "name": "Grid PJM · Interconnection Book",
        "title": "PJM Infrastructure Capital & Interconnection Command Post",
        "var_num": 35.30,
        "var_unit": "Million",
        "drift_num": 17.68,
        "drift_unit": "Million",
        "acl_num": 340000,
        "acl_unit": "/ wk",
        "bridge": "Synthesis reconciles 100% of Active Interconnection Drift: Regional Re-Study Backlogs (72%), Substation Lags (18%), Environmental Clearance (10%).",
        "sites": [
            {"Site": "Substation Alpha (Zone 4)", "Base_Drift": 6.1, "Base_Burn": 150, "Bottleneck": "Manual FERC Re-Study Queue"},
            {"Site": "Substation Beta (Zone 2)", "Base_Drift": 3.4, "Base_Burn": 110, "Bottleneck": "Paper Land Retainer Audit"},
            {"Site": "Substation Gamma (Zone 1)", "Base_Drift": 2.0, "Base_Burn": 80, "Bottleneck": "Sequential Environmental Sign-off"}
        ]
    },
    "ACC": {
        "name": "ACC Baseline · NZ Scheme Book",
        "title": "ACC Executive Synthesis & Knowledge Engine",
        "var_num": 63.60,
        "var_unit": "Billion",
        "drift_num": 2556.00,
        "drift_unit": "Million",
        "acl_num": 1209000,
        "acl_unit": "/ wk",
        "bridge": "Synthesis reconciles 100% of National Scheme Friction ($420k/wk): Northern Hub (76.2%), Midland Hub (9.5%), Central Hub (7.1%), South Island Hub (7.1%).",
        "sites": [
            {"Site": "Northern Hub 01", "Base_Drift": 4.2, "Base_Burn": 320, "Bottleneck": "Manual Medical Verification & Re-Keying"},
            {"Site": "Midland Hub 02", "Base_Drift": 1.8, "Base_Burn": 40, "Bottleneck": "Sequential Legal Dispute Queue"},
            {"Site": "Central Hub 03", "Base_Drift": 1.2, "Base_Burn": 30, "Bottleneck": "Treatment Pathway Discrepancy Audit"}
        ]
    },
    "BIOPHARMA": {
        "name": "Biopharma Clarity · GMP Book",
        "title": "Biopharma Sovereign GMP Release Command Post",
        "var_num": 142.00,
        "var_unit": "Million",
        "drift_num": 18.40,
        "drift_unit": "Million",
        "acl_num": 850000,
        "acl_unit": "/ wk",
        "bridge": "Synthesis reconciles 100% of Batch Release Friction ($850k/wk): Sterility Validation Holds (65%), Multi-site Deviation Reviews (25%), Certificate Processing Lags (10%).",
        "sites": [
            {"Site": "Facility Alpha (Sterile Suite)", "Base_Drift": 5.1, "Base_Burn": 450, "Bottleneck": "Manual Batch Record Re-Verification"},
            {"Site": "Facility Beta (Formulation)", "Base_Drift": 2.8, "Base_Burn": 280, "Bottleneck": "Environmental Monitoring Audit Lag"},
            {"Site": "Facility Gamma (Packaging)", "Base_Drift": 1.1, "Base_Burn": 120, "Bottleneck": "QC Sampling Certificate Queue"}
        ]
    },
    "DEFENSE": {
        "name": "Defense & Aerospace · Sovereign Book",
        "title": "Sovereign Fleet Readiness & CapEx Command Post",
        "var_num": 510.00,
        "var_unit": "Million",
        "drift_num": 42.10,
        "drift_unit": "Million",
        "acl_num": 2100000,
        "acl_unit": "/ wk",
        "bridge": "Synthesis reconciles 100% of Fleet Maintenance Drift ($2.1M/wk): Depot Level Overhaul Backlogs (58%), Avionics Component Sign-offs (27%), Sovereign Supply Chain Lags (15%).",
        "sites": [
            {"Site": "Naval Yard Alpha", "Base_Drift": 8.4, "Base_Burn": 1200, "Bottleneck": "Hull Structural Certification Backlog"},
            {"Site": "Air Base Wing 04", "Base_Drift": 4.1, "Base_Burn": 600, "Bottleneck": "Avionics Subsystem Retrofit Delay"},
            {"Site": "Logistics Depot Delta", "Base_Drift": 2.3, "Base_Burn": 300, "Bottleneck": "Sovereign Component Line Audit"}
        ]
    },
    "ERCOT": {
        "name": "ERCOT Energy · Storage Book",
        "title": "ERCOT Grid BESS & Storage Command Post",
        "var_num": 88.50,
        "var_unit": "Million",
        "drift_num": 12.30,
        "drift_unit": "Million",
        "acl_num": 610000,
        "acl_unit": "/ wk",
        "bridge": "Synthesis reconciles 100% of Storage Interconnection Drag ($610k/wk): Battery Telemetry Sign-offs (55%), Market Substation Audits (30%), Transformer Clearances (15%).",
        "sites": [
            {"Site": "BESS Storage Hub 01", "Base_Drift": 4.8, "Base_Burn": 320, "Bottleneck": "Telemetry Synchronization Validation"},
            {"Site": "Solar Substation Beta", "Base_Drift": 3.1, "Base_Burn": 190, "Bottleneck": "Inverter Capacity Testing Queue"},
            {"Site": "Feeder Node Gamma", "Base_Drift": 1.5, "Base_Burn": 100, "Bottleneck": "Manual Land Lease Retainer Sign-off"}
        ]
    },
    "APRA": {
        "name": "APRA Banking · Prudential Book",
        "title": "APRA Capital Reserve & Risk Command Post",
        "var_num": 1.20,
        "var_unit": "Billion",
        "drift_num": 95.00,
        "drift_unit": "Million",
        "acl_num": 4500000,
        "acl_unit": "/ wk",
        "bridge": "Synthesis reconciles 100% of Capital Reserve Drag ($4.5M/wk): Internal Rating Model Validations (60%), Stress Test Re-Keying (25%), Compliance Reporting Friction (15%).",
        "sites": [
            {"Site": "Risk Modeling Hub Alpha", "Base_Drift": 6.2, "Base_Burn": 2500, "Bottleneck": "Internal Rating Model Validation Lag"},
            {"Site": "Capital Treasury Unit", "Base_Drift": 3.0, "Base_Burn": 2000, "Bottleneck": "Liquidity Stress Testing Re-Keying"}
        ]
    },
    "PORT": {
        "name": "Port Logistics · Freight Book",
        "title": "Port Freight Velocity & Dwell Command Post",
        "var_num": 64.00,
        "var_unit": "Million",
        "drift_num": 8.20,
        "drift_unit": "Million",
        "acl_num": 410000,
        "acl_unit": "/ wk",
        "bridge": "Synthesis reconciles 100% of Vessel Dwell Friction ($410k/wk): Crane Automation Clearances (50%), Customs Paperwork Lags (35%), Yard Bottlenecks (15%).",
        "sites": [
            {"Site": "Container Terminal 01", "Base_Drift": 3.9, "Base_Burn": 250, "Bottleneck": "Automated Crane Sync Delay"},
            {"Site": "Freight Rail Hub North", "Base_Drift": 2.1, "Base_Burn": 160, "Bottleneck": "Customs Paper Manifest Audit"}
        ]
    },
    "NHS": {
        "name": "NHS Recovery · Surgical Book",
        "title": "NHS Elective Surgical Hub Command Post",
        "var_num": 210.00,
        "var_unit": "Million",
        "drift_num": 31.50,
        "drift_unit": "Million",
        "acl_num": 1150000,
        "acl_unit": "/ wk",
        "bridge": "Synthesis reconciles 100% of Elective Backlog Friction (£1.15M/wk): Operating Theatre Scheduling (62%), Post-Op Bed Clearance (23%), Diagnostics Sign-offs (15%).",
        "sites": [
            {"Site": "Surgical Hub North", "Base_Drift": 5.5, "Base_Burn": 650, "Bottleneck": "Pre-Op Assessment Paperwork Queue"},
            {"Site": "Regional Infirmary West", "Base_Drift": 2.9, "Base_Burn": 500, "Bottleneck": "Theatre Capacity Re-Allocation Queue"}
        ]
    }
}

# --- 2. URL PARAMETER ROUTING & SESSION LOCK ---
params = st.query_params
url_co = params.get("co", "PJM").upper()

if url_co not in SECTORS:
    url_co = "PJM"

if "authorized_co" not in st.session_state:
    st.session_state["authorized_co"] = url_co

# --- 3. SIDEBAR: THE ENTERPRISE CONTROL PLANE ---
st.sidebar.markdown(
    """
    <div style='padding-bottom: 12px;'>
        <h2 style='color: #00E5FF; font-size: 1.5rem; margin: 0;'>🎛️ CONTROL PLANE</h2>
        <p style='color: #3fb950; font-size: 0.85rem; font-weight: 600; margin: 4px 0 0 0;'>● Live Telemetry Active</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown("---")

# A. Sector Surface Selector
selected_key = st.sidebar.selectbox(
    "🏢 Enterprise Surface",
    options=list(SECTORS.keys()),
    format_func=lambda x: SECTORS[x]["name"],
    index=list(SECTORS.keys()).index(url_co)
)

active_data = SECTORS[selected_key]
is_authorized = (selected_key == st.session_state["authorized_co"])

# B. Governance View Mode Selector
view_mode = st.sidebar.radio(
    "👁️ Governance Layer",
    ["Executive Board Glass", "Site Operations Hub", "Complete Command Post"],
    index=2
)

# C. Interactive Stress-Testing Slider (Role-Gated)
st.sidebar.markdown("---")
st.sidebar.markdown("### ⚡ Live Drift Stress-Tester")

has_governance_authority = (view_mode in ["Executive Board Glass", "Complete Command Post"])

if has_governance_authority:
    stress_lag = st.sidebar.slider(
        "Simulate Friction Lag Escalation:",
        min_value=0,
        max_value=8,
        value=0,
        format="+%d Wks",
        key="active_stress_slider"
    )
else:
    st.sidebar.caption("🔒 Macro Stress Simulation Locked to Tier 1 Executive Authority.")
    stress_lag = st.sidebar.slider(
        "Simulate Friction Lag Escalation (Locked):",
        min_value=0,
        max_value=8,
        value=0,
        format="+%d Wks",
        disabled=True,
        key="locked_stress_slider"
    )

# Sidebar Action Directives
st.sidebar.markdown("---")
if st.sidebar.button("🔄 Sync Telemetry Stream", use_container_width=True):
    st.sidebar.success("Telemetry feed re-indexed from edge nodes.")

# --- 4. COMPUTED DYNAMIC METRICS BASED ON CONTROL PLANE ---
multiplier = 1.0 + (stress_lag * 0.12)
display_var = f"${active_data['var_num'] * multiplier:.2f} {active_data['var_unit']}"
display_drift = f"${active_data['drift_num'] * multiplier:.2f} {active_data['drift_unit']}"
display_acl = f"${int(active_data['acl_num'] * multiplier):,} {active_data['acl_unit']}"

# Update Site Data Table with Stress-Test Lags
computed_sites = []
for site in active_data["sites"]:
    adjusted_drift = site["Base_Drift"] + stress_lag
    adjusted_burn = int(site["Base_Burn"] * multiplier)
    computed_sites.append({
        "Site / Hub": site["Site"],
        "Drift Status": f"+{adjusted_drift:.1f} Wks",
        "Weekly Burn Rate": f"${adjusted_burn}k / wk",
        "Primary Bottleneck Queue": site["Bottleneck"]
    })

# --- 5. HEADER: CENTERED COMMAND POST TITLE ---
st.markdown(
    f"""
    <div style='text-align: center; padding: 10px 0 25px 0;'>
        <h1 style='color: #00E5FF; font-size: 2.7rem; font-weight: 900; letter-spacing: -0.8px; margin: 0; line-height: 1.2;'>
            🎯 {active_data['title']}
        </h1>
    </div>
    """,
    unsafe_allow_html=True
)

# --- 6. PEER LOCK SECURITY GATE (IF OTHER COMPANY CLICKED) ---
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
    st.stop()

# --- 7. TIER 1: EXECUTIVE BOARD GLASS ---
if view_mode in ["Executive Board Glass", "Complete Command Post"]:
    st.markdown("---")
    st.subheader("⚡ Tier 1: Active Executive Directive Telemetry")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Macro Valuation at Risk 🔒", display_var, help="Basis: Total Enterprise Exposure")
    with col2:
        st.metric("Annual Velocity Drift Cost 🔒", display_drift, help="Basis: Operational Drag Rate")
    with col3:
        st.metric("Actionable Controllable Loss 🔒", display_acl, help="Basis: Administrative Friction Drag")

    st.info(f"⚡ **DIRECT OPERATIONAL BRIDGE:** {active_data['bridge']}")

# --- 8. TIERS 2 & 3: MANAGER OPERATIONAL VIEW ---
if view_mode in ["Site Operations Hub", "Complete Command Post"]:
    st.markdown("---")
    with st.expander("🔓 TIER 2 & 3: Operational Unit Breakdown & Interconnects", expanded=True):
        st.markdown("### 🔍 Site Drift & Operational Unit Breakdown")
        
        st.table(computed_sites)
        
        if st.button("⚡ Execute Immediate Operational Clearance Directive"):
            st.balloons()
            st.success("Operational clearance directive dispatched to regional hubs.")

# --- 9. NOTEBOOK LANE & EXECUTIVE PROMPTING ---
st.markdown("---")
with st.expander("🧠 Notebook Lane & Executive Prompting Engine", expanded=True):
    st.markdown("### Executive Synthesis & Direct Query Interface")
    user_query = st.text_input(
        "Ask the Predictive Equilibrium Engine:",
        placeholder="e.g., What is the 90-day drift cost if clearance lags by 2 weeks?"
    )
    if user_query:
        st.info(f"**Synthesizing response for query:** '{user_query}'...")
        st.write("✨ *Analysis:* Operational drift in primary units impacts CapEx velocity. Immediate clearance directive recommended.")

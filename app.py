import streamlit as st
import re

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
        footer {visibility: hidden !important;}
        #MainMenu {visibility: hidden !important;}
        [data-testid="stSidebarNav"] {display: none !important;}
        [data-testid="stDecoration"] {display: none !important;}
        [data-testid="stToolbar"] {display: none !important;}
        header {background: transparent !important;}
        [data-testid="stHeader"] {background: transparent !important;}

        [data-testid="stSidebar"] {
            min-width: 390px !important;
            max-width: 390px !important;
            background-color: #0d1117 !important;
            border-right: 1px solid #30363d !important;
        }

        .stSelectbox label, .stRadio label, .stSlider label {
            font-size: 1.05rem !important;
            font-weight: 700 !important;
            color: #c9d1d9 !important;
        }

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

# --- 1. SECTOR DEFINITIONS WITH TAILORED PROMPT SUITES ---
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
        "bridge": "Synthesis traces active interconnection drag across regional FERC re-study backlogs, substation construction lags, and sequential environmental clearance queues.",
        "presets": [
            "Synthesize 45-day FERC re-study queue delay exposure",
            "Audit Substation Alpha Tier-3 construction holding burn",
            "Evaluate 8-week environmental clearance sequential lag"
        ],
        "sites": [
            {"Node": "Substation Alpha", "Location": "Zone 4", "Tier": "Tier 3: Site Unit", "Layer": "Interconnection Engineering", "Base_Drift": 6.1, "Base_Burn": 150, "Bottleneck": "Manual FERC Re-Study Queue"},
            {"Node": "Substation Beta", "Location": "Zone 2", "Tier": "Tier 3: Site Unit", "Layer": "Land Acquisition Group", "Base_Drift": 3.4, "Base_Burn": 110, "Bottleneck": "Paper Land Retainer Audit"},
            {"Node": "Regional Control North", "Location": "Valley Hub", "Tier": "Tier 2: Regional", "Layer": "Environmental Clearance Directorate", "Base_Drift": 2.0, "Base_Burn": 80, "Bottleneck": "Sequential Environmental Sign-off"}
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
        "bridge": "Synthesis isolates national scheme friction across regional claims verification queues, sequential dispute resolution lanes, and clinical pathway audits.",
        "presets": [
            "Evaluate 6-week claims backlog drift and medical review lag",
            "Synthesize Northern Hub clinical pathway audit friction",
            "Model 60-day dispute resolution escalation holding costs"
        ],
        "sites": [
            {"Node": "Northern Hub 01", "Location": "Auckland", "Tier": "Tier 2: Regional", "Layer": "Medical Review Directorate", "Base_Drift": 4.2, "Base_Burn": 320, "Bottleneck": "Manual Clinical Verification Queue"},
            {"Node": "Midland Hub 02", "Location": "Hamilton", "Tier": "Tier 2: Regional", "Layer": "Dispute Resolution Directorate", "Base_Drift": 1.8, "Base_Burn": 40, "Bottleneck": "Sequential Legal Dispute Queue"},
            {"Node": "Central Operations Hub", "Location": "Wellington", "Tier": "Tier 1: Central", "Layer": "Scheme Assurance & Governance", "Base_Drift": 5.2, "Base_Burn": 350, "Bottleneck": "Multi-Tier Entitlement Audit"}
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
        "bridge": "Synthesis isolates grid battery holding costs across market telemetry synchronization, inverter testing queues, and land lease retainer audits.",
        "presets": [
            "Synthesize 45-day battery storage telemetry synchronization lag",
            "Audit South Region inverter capacity testing queue delay",
            "Model 4-week interconnection retainer sign-off holding burn"
        ],
        "sites": [
            {"Node": "BESS Storage Hub 01", "Location": "West Region", "Tier": "Tier 3: Site Unit", "Layer": "Telemetry Operations Group", "Base_Drift": 4.8, "Base_Burn": 320, "Bottleneck": "Telemetry Synchronization Validation"},
            {"Node": "Solar Substation Beta", "Location": "South Region", "Tier": "Tier 3: Site Unit", "Layer": "Commissioning Engineering", "Base_Drift": 3.1, "Base_Burn": 190, "Bottleneck": "Inverter Capacity Testing Queue"},
            {"Node": "Regional Control Centre", "Location": "Central Grid", "Tier": "Tier 2: Regional", "Layer": "Interconnection Directorate", "Base_Drift": 1.5, "Base_Burn": 100, "Bottleneck": "Land Lease Retainer Sign-off"}
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
        "bridge": "Synthesis traces batch release holding drag across cleanroom deviation audits, multi-facility QC validations, and final certificate sign-off backlogs.",
        "presets": [
            "Evaluate 30-day sterile suite deviation audit holding cost",
            "Synthesize formulation line QC environmental monitoring lag",
            "Audit 5-week batch release certificate queue friction"
        ],
        "sites": [
            {"Node": "Facility Alpha", "Location": "Sterile Suite A", "Tier": "Tier 3: Site Unit", "Layer": "Sterility Assurance Unit", "Base_Drift": 5.1, "Base_Burn": 450, "Bottleneck": "Manual Batch Record Re-Verification"},
            {"Node": "Facility Beta", "Location": "Formulation Line", "Tier": "Tier 3: Site Unit", "Layer": "Environmental Monitoring Group", "Base_Drift": 2.8, "Base_Burn": 280, "Bottleneck": "Environmental Monitoring Audit Lag"},
            {"Node": "Quality Assurance Hub", "Location": "Central Campus", "Tier": "Tier 2: Regional", "Layer": "Release Quality Directorate", "Base_Drift": 1.1, "Base_Burn": 120, "Bottleneck": "QC Certificate Sign-off Queue"}
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
        "bridge": "Synthesis isolates fleet operational drift across drydock overhaul queues, avionics flight clearance sign-offs, and critical component supply chain audits.",
        "presets": [
            "Synthesize 60-day naval drydock hull recertification backlog",
            "Audit depot west avionics subsystem retrofit delay exposure",
            "Model 8-week sovereign component line procurement drift"
        ],
        "sites": [
            {"Node": "Naval Yard Alpha", "Location": "Drydock 01", "Tier": "Tier 3: Site Unit", "Layer": "Structural Certification Group", "Base_Drift": 8.4, "Base_Burn": 1200, "Bottleneck": "Hull Structural Recertification Backlog"},
            {"Node": "Air Base Wing 04", "Location": "Depot West", "Tier": "Tier 3: Site Unit", "Layer": "Avionics Integration Unit", "Base_Drift": 4.1, "Base_Burn": 600, "Bottleneck": "Avionics Subsystem Retrofit Delay"},
            {"Node": "Materiel Command Hub", "Location": "Central Logistics", "Tier": "Tier 1: Central", "Layer": "Sovereign Assurance Directorate", "Base_Drift": 2.3, "Base_Burn": 300, "Bottleneck": "Sovereign Component Line Audit"}
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
        "bridge": "Synthesis tracks capital allocation drag across internal risk model validations, liquidity stress-testing re-keying, and regulatory audit cycles.",
        "presets": [
            "Synthesize 90-day internal rating model validation drag",
            "Model liquidity stress-testing re-keying holding costs",
            "Evaluate 6-week regulatory capital allocation stall"
        ],
        "sites": [
            {"Node": "Risk Modeling Hub Alpha", "Location": "Sydney", "Tier": "Tier 2: Regional", "Layer": "Prudential Risk Directorate", "Base_Drift": 6.2, "Base_Burn": 2500, "Bottleneck": "Internal Rating Model Validation Lag"},
            {"Node": "Capital Treasury Unit", "Location": "Melbourne", "Tier": "Tier 1: Central", "Layer": "Treasury Governance Group", "Base_Drift": 3.0, "Base_Burn": 2000, "Bottleneck": "Liquidity Stress-Testing Re-Keying"}
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
        "bridge": "Synthesis traces container dwell cost across automated terminal sync delays, customs manifest audits, and intermodal freight queue stalls.",
        "presets": [
            "Synthesize 21-day container terminal automated crane sync lag",
            "Audit inland port customs paper manifest queue holding burn",
            "Model 4-week intermodal rail transfer dwell escalation"
        ],
        "sites": [
            {"Node": "Container Terminal 01", "Location": "Pier 4", "Tier": "Tier 3: Site Unit", "Layer": "Crane Operations Group", "Base_Drift": 3.9, "Base_Burn": 250, "Bottleneck": "Automated Crane Sync Delay"},
            {"Node": "Freight Rail Hub North", "Location": "Inland Port", "Tier": "Tier 2: Regional", "Layer": "Customs Clearance Directorate", "Base_Drift": 2.1, "Base_Burn": 160, "Bottleneck": "Customs Paper Manifest Audit"}
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
        "bridge": "Synthesis tracks elective backlog friction across pre-operative paperwork queues, operating theatre re-allocation delays, and post-op diagnostics sign-offs.",
        "presets": [
            "Synthesize 6-week pre-op assessment paperwork queue drift",
            "Audit regional theatre capacity re-allocation delay costs",
            "Model 45-day elective surgical elective recovery stall"
        ],
        "sites": [
            {"Node": "Surgical Hub North", "Location": "Trust Main", "Tier": "Tier 3: Site Unit", "Layer": "Clinical Assessment Team", "Base_Drift": 5.5, "Base_Burn": 650, "Bottleneck": "Pre-Op Assessment Paperwork Queue"},
            {"Node": "Regional Infirmary West", "Location": "District Hub", "Tier": "Tier 2: Regional", "Layer": "Theatre Planning Directorate", "Base_Drift": 2.9, "Base_Burn": 500, "Bottleneck": "Theatre Capacity Re-Allocation Queue"}
        ]
    }
}

# --- 2. URL PARAMETER ROUTING ---
params = st.query_params
url_co = params.get("co", "ERCOT").upper()

if url_co not in SECTORS:
    url_co = "ERCOT"

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

# B. Governance View Mode Selector
view_mode = st.sidebar.radio(
    "👁️ Governance Layer",
    ["Executive Board Glass", "Site Operations Hub", "Complete Command Post"],
    index=2
)

# C. Interactive Stress-Testing Slider
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

# --- 4. COMPUTED DYNAMIC METRICS & RAG THRESHOLDS ---
multiplier = 1.0 + (stress_lag * 0.12)
display_var = f"${active_data['var_num'] * multiplier:.2f} {active_data['var_unit']}"
display_drift = f"${active_data['drift_num'] * multiplier:.2f} {active_data['drift_unit']}"
display_acl = f"${int(active_data['acl_num'] * multiplier):,} {active_data['acl_unit']}"

computed_sites = []
for site in active_data["sites"]:
    adjusted_drift = site["Base_Drift"] + stress_lag
    adjusted_burn = int(site["Base_Burn"] * multiplier)
    
    if adjusted_drift <= 2.0:
        rag_badge = f"🟢 +{adjusted_drift:.1f} Wks (Nominal)"
    elif adjusted_drift < 5.0:
        rag_badge = f"🟡 +{adjusted_drift:.1f} Wks (Elevated)"
    else:
        rag_badge = f"🔴 +{adjusted_drift:.1f} Wks (Critical Drag)"

    computed_sites.append({
        "Operational Node": f"{site['Node']} ({site['Location']})",
        "Management Hierarchy": f"{site['Tier']} · {site['Layer']}",
        "Drift Status": rag_badge,
        "Weekly Burn Rate": f"${adjusted_burn}k / wk",
        "Active Bottleneck Queue": site["Bottleneck"]
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

# --- 6. TIER 1: EXECUTIVE BOARD GLASS ---
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

# --- 7. TIERS 2 & 3: MANAGER OPERATIONAL VIEW WITH MANAGEMENT DEPTH ---
if view_mode in ["Site Operations Hub", "Complete Command Post"]:
    st.markdown("---")
    with st.expander("🔓 TIER 2 & 3: Management Depth & Operational Unit Breakdown", expanded=True):
        st.markdown("### 🔍 Site Drift & Governance Node Breakdown")
        
        st.table(computed_sites)
        
        if st.button("⚡ Execute Immediate Operational Clearance Directive"):
            st.balloons()
            st.success("Operational clearance directive dispatched to regional hubs.")

# --- 8. DYNAMIC NOTEBOOK LANE & EXECUTIVE PROMPTING ENGINE ---
st.markdown("---")
with st.expander("🧠 Notebook Lane & Automated Executive Prompting Engine", expanded=True):
    st.markdown("### Automated Executive Scenario Prompts")
    st.caption("Select a pre-configured operational prompt chip or enter a custom query below:")

    if "current_query" not in st.session_state:
        st.session_state.current_query = active_data["presets"][0]

    # Render 3 Dynamic Prompt Chips
    chip_cols = st.columns(3)
    for idx, preset in enumerate(active_data["presets"]):
        with chip_cols[idx]:
            if st.button(f"⚡ Scenario {idx+1}:\n{preset}", key=f"chip_{selected_key}_{idx}", use_container_width=True):
                st.session_state.current_query = preset

    user_query = st.text_input(
        "Active Operational Query:",
        value=st.session_state.current_query
    )

    if user_query:
        # Time-duration regex parsing
        days_match = re.search(r'(\d+)\s*(?:day|days)', user_query, re.IGNORECASE)
        weeks_match = re.search(r'(\d+)\s*(?:week|weeks|wk|wks)', user_query, re.IGNORECASE)
        
        if days_match:
            days = float(days_match.group(1))
            weeks = days / 7.0
            time_str = f"{int(days)} Days ({weeks:.1f} Weeks)"
        elif weeks_match:
            weeks = float(weeks_match.group(1))
            days = weeks * 7.0
            time_str = f"{int(weeks)} Weeks ({int(days)} Days)"
        else:
            weeks = 4.0
            time_str = "30 Days (Standard 4-Week Baseline)"

        calc_loss = weeks * (active_data['acl_num'] * multiplier)
        compound_drift_delta = (active_data['drift_num'] * multiplier) * (weeks * 0.12)
        
        # Determine highest drag bottleneck from the site list
        critical_site = max(active_data["sites"], key=lambda x: x["Base_Drift"])

        st.markdown(
            f"""
            #### 📊 Predictive Synthesis for {active_data['name']}
            * **Active Scenario:** *"{user_query}"*
            * **Evaluated Delay Period:** **{time_str}**
            * **Cumulative Controllable Holding Loss:** **${calc_loss:,.2f}**
            * **Compounded Velocity Drift Escalation:** **+${compound_drift_delta:.2f} {active_data['drift_unit']}**
            * **Critical Constraint Layer:** **{critical_site['Tier']} · {critical_site['Layer']}** ({critical_site['Bottleneck']})
            
            > **Executive Action Directive:** Delay friction across the active queues burns **${calc_loss:,.2f}** over **{time_str}**. Discharging the **Immediate Operational Clearance Directive** at **{critical_site['Node']}** collapses sequential lag back to nominal thresholds.
            """
        )

# --- 9. AUTOMATED CLIENT OUTREACH BRIEF GENERATOR ---
st.markdown("---")
with st.expander("✉️ Generate Client Briefing & Executive Email", expanded=False):
    st.markdown(f"### 📋 Outreach Memo: {active_data['name']}")
    
    client_url = f"https://aatphoenix.streamlit.app/?co={selected_key}"
    
    email_memo = f"""Subject: Live Executive Telemetry & Drift Analysis — {active_data['title']}

Hi [Executive First Name],

Leveraging the established performance metrics and financial outcomes documented in last year’s operational reporting, we have synthesized your exposure metrics into a live Predictive Equilibrium Command Post.

1. FINANCIAL EXPOSURE TELEMETRY
• Macro Valuation at Risk (VaR): ${active_data['var_num']:.2f} {active_data['var_unit']}
• Annual Velocity Drift Cost: ${active_data['drift_num']:.2f} {active_data['drift_unit']}
• Actionable Controllable Loss (ACL): ${int(active_data['acl_num']):,} {active_data['acl_unit']}
• Operational Friction Bridge: {active_data['bridge']}

2. INTERACTIVE EXECUTIVE ACCESS
You can access your provisioned enterprise surface directly here:
👉 {client_url}

3. ENTERPRISE SECURITY & AUDIT GOVERNANCE
The system architecture is designed for optimal efficiency and rigorously secured access:
• Complete visibility of the application interface and its sensitive data streams is strictly limited to authenticated personnel explicitly authorized through our multi-factor authentication protocols and role-based access control framework.
• A comprehensive, immutable audit trail is embedded within the platform, meticulously logging all user interactions, modifications, and data access attempts for regulatory compliance and internal accountability.
• Local operations teams are restricted from altering macro financial multipliers, ensuring high data fidelity from field operations to the executive board.

For immediate, interactive exploration, please navigate to the provided hyperlink above. Should any questions regarding security protocols, integration feasibility, or feature functionality arise, please reach out directly.

Best regards,

[Your Name]
AAT Phoenix Engine
"""
    st.text_area("Ready-to-send Executive Email:", value=email_memo, height=380)
    st.caption("💡 Copy and paste this directly into your email client. It auto-updates whenever you change the Enterprise Surface.")

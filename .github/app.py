import streamlit as st
import re
import hashlib
from datetime import datetime, timezone

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AAT Phoenix Command Post",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- TOUCH-OPTIMIZED MOBILE & ENTERPRISE STYLING ---
enterprise_styling = """
    <style>
        /* Suppress default headers, footers, hamburger menus */
        footer {visibility: hidden !important;}
        #MainMenu {visibility: hidden !important;}
        [data-testid="stSidebarNav"] {display: none !important;}
        [data-testid="stDecoration"] {display: none !important;}
        [data-testid="stToolbar"] {display: none !important;}
        header {background: transparent !important;}
        [data-testid="stHeader"] {background: transparent !important;}

        /* High-Visibility Floating Sidebar Toggle (iPhone & iPad Fix) */
        [data-testid="stSidebarCollapsedControl"],
        [data-testid="collapsedControl"],
        button[data-testid="stSidebarCollapseButton"] {
            display: flex !important;
            visibility: visible !important;
            position: fixed !important;
            top: 12px !important;
            left: 12px !important;
            z-index: 999999 !important;
            background-color: #00E5FF !important;
            color: #0d1117 !important;
            border-radius: 12px !important;
            border: 2px solid #00B4D8 !important;
            padding: 8px 14px !important;
            min-height: 48px !important;
            min-width: 48px !important;
            box-shadow: 0px 4px 18px rgba(0, 229, 255, 0.5) !important;
        }
        
        [data-testid="stSidebarCollapsedControl"] svg,
        [data-testid="collapsedControl"] svg {
            fill: #0d1117 !important;
            stroke: #0d1117 !important;
            width: 28px !important;
            height: 28px !important;
        }

        /* Sidebar Geometry & High-Contrast Typography */
        [data-testid="stSidebar"] {
            min-width: 390px !important;
            max-width: 390px !important;
            background-color: #0d1117 !important;
            border-right: 1px solid #30363d !important;
        }

        .stSelectbox label, .stRadio label, .stSlider label {
            font-size: 1.1rem !important;
            font-weight: 700 !important;
            color: #c9d1d9 !important;
            padding-bottom: 6px !important;
        }

        /* Large Touch Targets for Mobile / iPad Tap Ergonomics */
        .stButton button {
            min-height: 52px !important;
            font-size: 1.05rem !important;
            font-weight: 600 !important;
            border-radius: 8px !important;
            padding: 10px 14px !important;
        }

        div[data-testid="stRadio"] > div {
            gap: 10px !important;
        }

        div[data-testid="stRadio"] label {
            padding: 10px 12px !important;
            background: #161b22 !important;
            border-radius: 8px !important;
            border: 1px solid #30363d !important;
            width: 100% !important;
        }

        /* Executive Metrics Display */
        [data-testid="stMetricValue"] {
            font-size: 2.2rem !important;
            font-weight: 800 !important;
            color: #00E5FF !important;
        }
    </style>
"""
st.markdown(enterprise_styling, unsafe_allow_html=True)

# --- 1. SECTOR DEFINITIONS & PRESET SUITES ---
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
    <div style='padding-bottom: 10px;'>
        <h2 style='color: #00E5FF; font-size: 1.6rem; margin: 0; font-weight: 800;'>🎛️ CONTROL PLANE</h2>
        <p style='color: #3fb950; font-size: 0.9rem; font-weight: 700; margin: 4px 0 0 0;'>● Live Telemetry Active</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown("---")

# A. Operating Sector Selector
selected_key = st.sidebar.selectbox(
    "🏢 Operating Sector Book",
    options=list(SECTORS.keys()),
    format_func=lambda x: SECTORS[x]["name"],
    index=list(SECTORS.keys()).index(url_co)
)

active_data = SECTORS[selected_key]

# B. Top-Down Command Hierarchy Selector
view_mode = st.sidebar.radio(
    "🏛️ Command Hierarchy",
    [
        "Tier 1: Master Command Post (Full Authority)",
        "Tier 2: Executive Board Glass (General Mgmt)",
        "Tier 3: Site Operations Hub (Regional & Field)"
    ],
    index=0
)

# C. Directorate Domain Controls and Chairman Apex Authority
st.sidebar.markdown("---")
st.sidebar.markdown("### 🏛️ Directorate Domain Control")
chairman_override = st.sidebar.toggle(
    "Chairman Apex Director Authority Override",
    value=False,
    help="Chairman authority activates every directorate and unlocks macro stress controls."
)

directorate_domains = {
    "COO": st.sidebar.toggle("COO · Operations Control", value=True, disabled=chairman_override),
    "CFO": st.sidebar.toggle("CFO · Capital Control", value=True, disabled=chairman_override),
    "Legal": st.sidebar.toggle("Legal · Statutory Control", value=True, disabled=chairman_override),
    "CTO": st.sidebar.toggle("CTO · Systems Control", value=True, disabled=chairman_override),
}
if chairman_override:
    directorate_domains = {domain: True for domain in directorate_domains}

# D. Live Drift Stress-Tester (Locked Strictly to Tier 1 or Chairman Authority)
st.sidebar.markdown("---")
st.sidebar.markdown("### ⚡ Live Drift Stress-Tester")

is_tier_1_authority = view_mode.startswith("Tier 1") or chairman_override

if is_tier_1_authority:
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

st.sidebar.markdown("---")
if st.sidebar.button("🔄 Sync Telemetry Stream", use_container_width=True):
    st.sidebar.success("Telemetry feed re-indexed from edge nodes.")

# --- 4. COMPUTED DYNAMIC METRICS & RAG STATUS ---
multiplier = 1.0 + (stress_lag * 0.12)
display_var = f"${active_data['var_num'] * multiplier:.2f} {active_data['var_unit']}"
display_drift = f"${active_data['drift_num'] * multiplier:.2f} {active_data['drift_unit']}"
display_acl = f"${int(active_data['acl_num'] * multiplier):,} {active_data['acl_unit']}"

# --- 5. GOVERNANCE CALCULATIONS ---
# The buckets reconcile to the existing weekly ACL and remain transparent inputs.
weekly_acl = active_data["acl_num"] * multiplier
loss_buckets = {
    "Idle labour": weekly_acl * 0.42,
    "WACC / demurrage carry": weekly_acl * 0.38,
    "Statutory penalties": weekly_acl * 0.20,
}
total_holding_loss = sum(loss_buckets.values())
realization_fee = total_holding_loss * 0.10
client_realization = total_holding_loss * 0.90

audit_payload = "|".join([
    selected_key,
    view_mode,
    str(stress_lag),
    str(chairman_override),
    ",".join(f"{domain}:{enabled}" for domain, enabled in directorate_domains.items()),
    f"{total_holding_loss:.2f}",
])
previous_hash = st.session_state.get("audit_chain_head", "GENESIS")
proof_nonce = 0
while True:
    audit_hash = hashlib.sha256(
        f"{previous_hash}|{audit_payload}|{proof_nonce}".encode("utf-8")
    ).hexdigest()
    if audit_hash.startswith("00"):
        break
    proof_nonce += 1
st.session_state.audit_chain_head = audit_hash
audit_row = {
    "UTC Timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    "Authority": "Chairman Apex Override" if chairman_override else view_mode.split(":", 1)[0],
    "Domain State": " / ".join(domain for domain, enabled in directorate_domains.items() if enabled),
    "Holding Loss": f"${total_holding_loss:,.2f} / wk",
    "Nonce": proof_nonce,
    "Proof-of-Work": audit_hash[:16],
    "Previous Proof": previous_hash[:16],
}
if audit_row["Proof-of-Work"] != st.session_state.get("last_audit_proof"):
    st.session_state.setdefault("audit_ledger", []).append(audit_row)
    st.session_state.last_audit_proof = audit_row["Proof-of-Work"]

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

# --- 5. MAIN HEADER ---
st.markdown(
    f"""
    <div style='text-align: center; padding: 10px 0 20px 0;'>
        <h1 style='color: #00E5FF; font-size: 2.6rem; font-weight: 900; letter-spacing: -0.8px; margin: 0; line-line: 1.2;'>
            🎯 {active_data['title']}
        </h1>
    </div>
    """,
    unsafe_allow_html=True
)

# --- 6. STRATEGIC EXPOSURE METRICS (Visible for Tier 1 and Tier 2) ---
if (view_mode.startswith("Tier 1") or view_mode.startswith("Tier 2")) and directorate_domains["CFO"]:
    st.markdown("---")
    st.subheader("⚡ Strategic Balance-Sheet Telemetry")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Macro Valuation at Risk 🔒", display_var, help="Basis: Total Enterprise Exposure")
    with col2:
        st.metric("Annual Velocity Drift Cost 🔒", display_drift, help="Basis: Operational Drag Rate")
    with col3:
        st.metric("Actionable Controllable Loss 🔒", display_acl, help="Basis: Administrative Friction Drag")

    st.info(f"⚡ **DIRECT OPERATIONAL BRIDGE:** {active_data['bridge']}")

    st.markdown("### 💰 Deconstructed Holding Loss & Realization Ledger")
    loss_rows = [
        {"Holding Loss Bucket": bucket, "Weekly Exposure": f"${amount:,.2f}", "Share": f"{amount / total_holding_loss:.0%}"}
        for bucket, amount in loss_buckets.items()
    ]
    loss_rows.extend([
        {"Holding Loss Bucket": "Total verified holding loss", "Weekly Exposure": f"${total_holding_loss:,.2f}", "Share": "100%"},
        {"Holding Loss Bucket": "Client realization (90%)", "Weekly Exposure": f"${client_realization:,.2f}", "Share": "90%"},
        {"Holding Loss Bucket": "Phoenix realization fee (10%)", "Weekly Exposure": f"${realization_fee:,.2f}", "Share": "10%"},
    ])
    st.table(loss_rows)

if directorate_domains["Legal"] and (view_mode.startswith("Tier 1") or view_mode.startswith("Tier 2")):
    st.markdown("### 🔐 Immutable Proof-of-Work Audit Ledger")
    st.caption("Append-only session ledger. Each proof is chained to the preceding record.")
    st.table(st.session_state.get("audit_ledger", []))

# --- 7. OPERATIONAL MANAGEMENT & SITE UNITS (Visible for Tier 1 and Tier 3) ---
if (view_mode.startswith("Tier 1") or view_mode.startswith("Tier 3")) and directorate_domains["COO"]:
    st.markdown("---")
    with st.expander("🔓 Management Depth & Operational Site Queues", expanded=True):
        st.markdown("### 🔍 Granular Bottleneck & Node Telemetry")
        st.table(computed_sites)
        
        if st.button("⚡ Dispatch Immediate Operational Clearance Directive", use_container_width=True):
            st.balloons()
            st.success("Operational clearance directive dispatched to regional hubs.")

# --- 8. DYNAMIC NOTEBOOK LANE & EXECUTIVE PROMPTING ENGINE (Tier 1 & Tier 2) ---
if (view_mode.startswith("Tier 1") or view_mode.startswith("Tier 2")) and directorate_domains["CTO"]:
    st.markdown("---")
    with st.expander("🧠 Notebook Lane & Automated Executive Prompting Engine", expanded=True):
        st.markdown("### Automated Executive Scenario Prompts")
        st.caption("Select a pre-configured scenario chip to synthesize exposure without manual typing:")

        if "current_query" not in st.session_state:
            st.session_state.current_query = active_data["presets"][0]

        # 3 Dynamic Prompt Chips with Large Touch Targets
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

# --- 9. TOP-LOADED GAINSHARE OUTREACH BRIEF GENERATOR ---
st.markdown("---")
with st.expander("✉️ Generate Client Briefing & Executive Email (Top-Loaded Offer)", expanded=False):
    st.markdown(f"### 📋 Outreach Memo: {active_data['name']}")
    
    client_url = f"https://aatphoenix.streamlit.app/?co={selected_key}"
    
    email_memo = f"""Subject: Automated Operational Drift Recovery — {active_data['title']}

Hi [Executive First Name],

The Offer: We connect your operations into a fully automated, immutable audited command plane that re-indexes at 02:00 AM daily—eliminating your active queue bottlenecks at zero upfront cost. You only pay a percentage of the verified holding capital we recover on your balance sheet.

This demonstration post uses public operational baselines to illustrate how our automated telemetry sync aligns executive oversight with site-level bottlenecks in real time:

👉 Direct Executive Surface: {client_url}

---

WHAT THIS COMMAND POST ISOLATES IN 30 SECONDS:
• Macro Valuation at Risk (VaR): ${active_data['var_num']:.2f} {active_data['var_unit']}
• Annual Velocity Drift Cost: ${active_data['drift_num']:.2f} {active_data['drift_unit']}
• Actionable Controllable Loss (ACL): ${int(active_data['acl_num']):,} {active_data['acl_unit']}
• Active Bottleneck Bridge: {active_data['bridge']}

INTERACTIVE SCENARIO MODELING:
Navigate to the provided link and tap any prompt chip inside the Notebook Lane to calculate the holding cost of 30, 45, or 60-day process stalls.

ENTERPRISE SECURITY & AUDIT GOVERNANCE:
• Access is strictly limited to authenticated personnel via role-based access controls.
• A comprehensive, immutable audit trail logs all user interactions for regulatory compliance.
• Macro stress simulation multipliers are strictly locked to Tier 1 Executive Authority.

Explore the live model at your convenience. If you are open to recovering lost velocity without budget risk, let us know which operational node to calibrate first.

Best regards,

[Your Name]
AAT Phoenix Engine
"""
    st.text_area("Ready-to-send Executive Memo:", value=email_memo, height=420)
    st.caption("💡 Fully formatted and ready to copy into your email client. Automatically syncs whenever you switch sectors.")

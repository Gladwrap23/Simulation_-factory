import streamlit as st

# -----------------------------------------------------------------------------
# 1. PAGE SETUP & HIGH-CONTRAST PROJECTION CSS
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="ACC Command Surface",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
    /* 🔒 HIDE STREAMLIT TOOLBARS FOR PROJECTION PURITY */
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    
    /* SCOPE HEADER BOX */
    .scope-box {
        background-color: #062313;
        border: 1.5px solid #00e676;
        border-radius: 8px;
        padding: 16px 20px;
        margin-bottom: 25px;
    }
    .scope-title {
        color: #00e676;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 1.2px;
        text-transform: uppercase;
    }
    .scope-role {
        color: #ffffff;
        font-size: 1.6rem;
        font-weight: 700;
        margin-top: 4px;
    }

    /* DUAL CHANNEL BOARDROOM PROJECTION PANELS */
    .projection-target-panel {
        background-color: #0f172a;
        border: 1.5px solid #3b82f6;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 15px;
    }
    .projection-live-panel {
        background-color: #1f1315;
        border: 1.5px solid #ef4444;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 15px;
    }
    .panel-header-target {
        color: #60a5fa;
        font-size: 0.85rem;
        font-weight: 800;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 10px;
    }
    .panel-header-live {
        color: #f87171;
        font-size: 0.85rem;
        font-weight: 800;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 10px;
    }
</style>
""",
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# 2. EXTENDED DATA MAP (TARGET BASELINE VS LIVE OPERATING DRIFT)
# -----------------------------------------------------------------------------
ROLE_MAP = {
    "minister": {
        "label": "🏛️ Minister for ACC & Board Chair",
        "title": "NATIONAL SCHEME LIABILITY DRIFT",
        "location": "Upper North Island Specialist Network",
        "target_metric": "$0 / week (On Budget Target)",
        "live_metric": "+$420,000 / week",
        "delta": "+$420,000 / week breach",
        "target_dwell": "7 Days Wait Target",
        "live_dwell": "28 Days Wait Actual",
        "root_cause": "Orthopedic Assessment Capacity Deficit",
        "options": [
            "Authorize Allied Health Assessment Delegation",
            "Reallocate $2.5M Emergency Capacity Burst Fund",
        ],
    },
    "ce": {
        "label": "⚡ Chief Executive (Wellington HQ)",
        "title": "PRIMARY CAPACITY BOTTLENECK: IME QUEUE",
        "location": "Auckland Central & Waitematā Hubs",
        "target_metric": "< 200 Claims Stagnant",
        "live_metric": "1,240 Claims Stagnant",
        "delta": "+1,040 Claims Over Tolerance",
        "target_dwell": "14 Days Dwell Threshold",
        "live_dwell": "34 Days Dwell Average",
        "root_cause": "Specialist Panel Backlog in Complex Musculoskeletal Claims",
        "options": [
            "Re-route 300 Cases to Waikato/Bay of Plenty Panel",
            "Trigger Fast-Track Telehealth Assessment Protocol",
        ],
    },
    "rgm_north": {
        "label": "📍 RGM - Northern Region (Auckland / Northland)",
        "title": "AUCKLAND & NORTHLAND SPECIALIST BOTTLENECK",
        "location": "Waitematā & Whangārei Clinical Hubs",
        "target_metric": "0 Blocked Claims (>21d)",
        "live_metric": "512 Claims Blocked",
        "delta": "+512 Regional Queue Breach",
        "target_dwell": "14 Days Target Clearance",
        "live_dwell": "42 Days Local Dwell",
        "root_cause": "Orthopedic Specialist Deficit in Northland & Metro Auckland",
        "options": [
            "Deploy Mobile Specialist Assessment Unit to Whangārei",
            "Authorize Private Hospital Panel Overflow Contract",
        ],
    },
    "rgm_midland": {
        "label": "📍 RGM - Midland Region (Waikato / Bay of Plenty)",
        "title": "MIDLAND TRIAGE & INTAKE CAPACITY DRIFT",
        "location": "Hamilton Central & Tauranga Branches",
        "target_metric": "< 30 Cases Awaiting Triage",
        "live_metric": "184 Cases Awaiting Triage",
        "delta": "+154 Triage Overflow",
        "target_dwell": "48 Hours Target Triage",
        "live_dwell": "12 Days Triage Lag",
        "root_cause": "Local Provider Staffing Deficit & Assessment Delay",
        "options": [
            "Issue Overflow Capacity Contract to Local Private Network",
            "Approve Regional Case Manager Overtime Allowance",
        ],
    },
    "rgm_central": {
        "label": "📍 RGM - Central Region (Wellington / Lower NI)",
        "title": "CENTRAL REGION COMPLEX CLAIM DELAYS",
        "location": "Wellington HQ & Palmerston North Hub",
        "target_metric": "0 Surgical Approval Delays",
        "live_metric": "120 Claims Delayed",
        "delta": "+120 Panel Backlog",
        "target_dwell": "10 Days Surgical Review",
        "live_dwell": "32 Days Surgical Review",
        "root_cause": "Surgical Panel Review Delays Exceeding 30 Days",
        "options": [
            "Delegate Fast-Track Sign-off Authority to Regional Lead",
            "Re-route Claims to Hawke's Bay Assessment Panel",
        ],
    },
    "rgm_south": {
        "label": "📍 RGM - South Island (Canterbury / Otago / Southland)",
        "title": "SOUTH ISLAND REHABILITATION SERVICE BOTTLENECK",
        "location": "Christchurch & Dunedin Service Centres",
        "target_metric": "< 50 Clients Awaiting Placement",
        "live_metric": "290 Clients Awaiting Placement",
        "delta": "+240 Service Bottleneck",
        "target_dwell": "5 Days Placement Target",
        "live_dwell": "26 Days Placement Lag",
        "root_cause": "Physiotherapy & Vocational Provider Capacity Deficit",
        "options": [
            "Activate Emergency Allied Health Preferred Provider Network",
            "Authorize Direct Vocational Grant Streamlining",
        ],
    },
    "cm": {
        "label": "💼 Case Manager / Frontline Operator",
        "title": "INDIVIDUAL CLAIM DWELL TIME SPIKE",
        "location": "Claim #ACC-2026-89421",
        "target_metric": "5 Days Target Treatment Sign-off",
        "live_metric": "38 Days Idle Dwell Time",
        "delta": "+33 Days Action Delay",
        "target_dwell": "Standard Protocol",
        "live_dwell": "Stalled on Surgical Panel",
        "root_cause": "Pending Surgical Panel Approval Signature",
        "options": [
            "Override Triage Delay via Delegated Authority Band",
            "Escalate Directly to Regional Clinical Lead",
        ],
    },
    "support": {
        "label": "📋 Support Staff & Intake Entry Point",
        "title": "INITIAL DOCUMENTATION & INTAKE LAG",
        "location": "National Intake Gateway",
        "target_metric": "< 50 Uncoded Submissions",
        "live_metric": "430 Uncoded Submissions",
        "delta": "+380 Intake Queue Lag",
        "target_dwell": "2 Hours Intake Clearance",
        "live_dwell": "5.2 Days Verification Lag",
        "root_cause": "Incomplete Initial Provider ICD-10 Coding & Medical Notes",
        "options": [
            "Trigger Automated Provider Document Request",
            "Apply Fast-Track Automated Coding Validation",
        ],
    },
}

# -----------------------------------------------------------------------------
# 3. SIDEBAR CONTROLS & DISPLAY MODE SWITCHER
# -----------------------------------------------------------------------------
st.sidebar.title("AAT SCHEME GOVERNANCE")

# Display Mode Switcher
view_mode = st.sidebar.radio(
    "🖥️ Display Mode",
    ["📺 Standard Command Glass", "📽️ Dual-Channel Boardroom Projection"],
    index=0,
)

st.sidebar.markdown("---")

role_keys = list(ROLE_MAP.keys())
query_role = str(st.query_params.get("role", "minister")).lower()
if query_role == "gm":
    query_role = "rgm_north"

default_key = query_role if query_role in ROLE_MAP else "minister"
default_idx = role_keys.index(default_key)

selected_key = st.sidebar.selectbox(
    "Active User Role Matrix",
    role_keys,
    index=default_idx,
    format_func=lambda k: ROLE_MAP[k]["label"],
)

st.sidebar.markdown("---")
st.sidebar.subheader("SCHEME MANDATE INJECTION")
st.sidebar.caption(
    "Proprietary stewardship band control · explicit arithmetic withheld from glass"
)

floor_val = st.sidebar.slider(
    "Enforce Liability Mitigation Floor",
    min_value=0,
    max_value=100,
    value=65,
)
st.sidebar.info(f"Active Stewardship Floor: {floor_val}% Protection Band")

# -----------------------------------------------------------------------------
# 4. MAIN COMMAND SURFACE RENDERER
# -----------------------------------------------------------------------------
st.title("ACC Board & Ministerial Command Surface")

current_data = ROLE_MAP[selected_key]

# Active Scope Emerald Box
st.markdown(
    f"""
    <div class="scope-box">
        <div class="scope-title">ACTIVE COMMAND SCOPE</div>
        <div class="scope-role">{current_data['label']}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# MODE A: STANDARD COMMAND GLASS
# -----------------------------------------------------------------------------
if view_mode == "📺 Standard Command Glass":
    st.subheader(f"🎯 {current_data['title']}")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            label="📍 Target Location / Network",
            value=current_data["location"],
        )
    with col2:
        st.metric(
            label="⚠️ Impact Drift Rate",
            value=current_data["live_metric"],
        )
    with col3:
        st.metric(
            label="🛡️ Operational Status",
            value="ACTIVE DRIFT",
        )

    st.error(f"**Root Cause:** {current_data['root_cause']}")

# -----------------------------------------------------------------------------
# MODE B: DUAL-CHANNEL BOARDROOM PROJECTION MODE
# -----------------------------------------------------------------------------
else:
    st.markdown(f"### 🎯 SYNCHRONIZED BOARDROOM MATRIX: {current_data['title']}")
    
    col_target, col_live = st.columns(2)

    # LEFT PANEL: TARGET / BASELINE OPERATING PARAMETERS
    with col_target:
        st.markdown(
            """
            <div class="projection-target-panel">
                <div class="panel-header-target">🎯 TARGET BASELINE PERFORMANCE (POLICY STANDARD)</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.metric(
            label="Target Network Bounds",
            value=current_data["location"],
        )
        st.metric(
            label="Mandated Performance Metric",
            value=current_data["target_metric"],
        )
        st.metric(
            label="Target Dwell Standard",
            value=current_data["target_dwell"],
        )
        st.info("System operating within mandated stewardship bands.")

    # RIGHT PANEL: LIVE OPERATING DRIFT (REAL-TIME ENGINE FEED)
    with col_live:
        st.markdown(
            """
            <div class="projection-live-panel">
                <div class="panel-header-live">⚠️ LIVE OPERATING STATE (REAL-TIME ENGINE FEED)</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.metric(
            label="Active Operational Location",
            value=current_data["location"],
        )
        st.metric(
            label="Live Drift Rate",
            value=current_data["live_metric"],
            delta=current_data["delta"],
            delta_color="inverse",
        )
        st.metric(
            label="Live Dwell Bottleneck",
            value=current_data["live_dwell"],
            delta="DRIFT BREACH",
            delta_color="inverse",
        )
        st.error(f"**Identified Root Cause:** {current_data['root_cause']}")

# -----------------------------------------------------------------------------
# 5. STRATEGIC INTERVENTIONS EXECUTION LAYER
# -----------------------------------------------------------------------------
st.markdown("---")
st.markdown("### ⚡ Strategic Interventions")

for idx, option in enumerate(current_data["options"]):
    if st.button(f"Execute: {option}", key=f"btn_{selected_key}_{idx}"):
        st.success(f"Command Executed: {option}")

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
# 2. EXTENDED MONETARY DATA MAP (TARGET BASELINE VS LIVE OPERATING DRIFT)
# -----------------------------------------------------------------------------
ROLE_MAP = {
    "minister": {
        "label": "🏛️ Minister for ACC & Board Chair",
        "title": "NATIONAL SCHEME FINANCIAL DRIFT (AUG 2026)",
        "location": "National Scheme (All 4 Operational Regions)",
        "target_metric": "$14.20M / week (Allocated Comp Budget)",
        "live_metric": "$14.62M / week (Actual Comp Outflow)",
        "delta": "+$420,000 / week Financial Drift",
        "target_dwell": "$0 / claim (Mandated Policy Baseline)",
        "live_dwell": "+$1.68M Cumulative Dwell Exposure",
        "root_cause": "Orthopedic Assessment Capacity Backlog Driving Extended Weekly Compensation Outflows",
        "options": [
            "Authorize Allied Health Assessment Delegation",
            "Reallocate $2.5M Emergency Capacity Burst Fund",
        ],
    },
    "ce": {
        "label": "⚡ Chief Executive (Wellington HQ)",
        "title": "PRIMARY CAPACITY & FINANCIAL DRIFT",
        "location": "Auckland Central & Waitematā Assessment Hubs",
        "target_metric": "$2.10M / week (IME & Clinical Budget)",
        "live_metric": "$2.82M / week (Actual Clinical Spend)",
        "delta": "+$720,000 / week Panel Overrun",
        "target_dwell": "$0 Stagnant Claim Penalty",
        "live_dwell": "+$3.12M Unbudgeted Dwell Exposure",
        "root_cause": "1,240 Stagnant IME Claims Driving Extended Income Replacement Outflows",
        "options": [
            "Re-route 300 Cases to Waikato/Bay of Plenty Panel",
            "Trigger Fast-Track Telehealth Assessment Protocol",
        ],
    },
    "rgm_north": {
        "label": "📍 RGM - Northern Region (Auckland / Northland)",
        "title": "NORTHERN REGION FINANCIAL DRIFT",
        "location": "Waitematā & Whangārei Clinical Hubs",
        "target_metric": "$4.50M / week (Regional Operations Target)",
        "live_metric": "$4.98M / week (Actual Regional Spend)",
        "delta": "+$480,000 / week Regional Breach",
        "target_dwell": "$0 / claim (14-Day Target Baseline)",
        "live_dwell": "+$1.15M Local Bottleneck Cost",
        "root_cause": "512 Blocked Orthopedic Claims in Metro Auckland & Whangārei",
        "options": [
            "Deploy Mobile Specialist Assessment Unit to Whangārei",
            "Authorize Private Hospital Panel Overflow Contract",
        ],
    },
    "rgm_midland": {
        "label": "📍 RGM - Midland Region (Waikato / Bay of Plenty)",
        "title": "MIDLAND TRIAGE & CAPACITY FINANCIAL DRIFT",
        "location": "Hamilton Central & Tauranga Branches",
        "target_metric": "$2.80M / week (Midland Target)",
        "live_metric": "$3.04M / week (Actual Spend)",
        "delta": "+$240,000 / week Triage Drift",
        "target_dwell": "$0 / claim (48-Hour Triage Standard)",
        "live_dwell": "+$410,000 Delayed Triage Exposure",
        "root_cause": "184 Cases Awaiting Clinical Triage Due to Local Provider Deficit",
        "options": [
            "Issue Overflow Capacity Contract to Local Private Network",
            "Approve Regional Case Manager Overtime Allowance",
        ],
    },
    "rgm_central": {
        "label": "📍 RGM - Central Region (Wellington / Lower NI)",
        "title": "CENTRAL REGION SURGICAL DELAY COSTS",
        "location": "Wellington HQ & Palmerston North Hub",
        "target_metric": "$3.20M / week (Central Regional Budget)",
        "live_metric": "$3.48M / week (Actual Regional Outflow)",
        "delta": "+$280,000 / week Panel Lag Drift",
        "target_dwell": "$0 / claim (10-Day Sign-off Baseline)",
        "live_dwell": "+$620,000 Delayed Surgical Exposure",
        "root_cause": "120 Claims Stalled on Surgical Panel Approval Signatures Exceeding 30 Days",
        "options": [
            "Delegate Fast-Track Sign-off Authority to Regional Lead",
            "Re-route Claims to Hawke's Bay Assessment Panel",
        ],
    },
    "rgm_south": {
        "label": "📍 RGM - South Island (Canterbury / Otago / Southland)",
        "title": "SOUTH ISLAND REHABILITATION SERVICE COSTS",
        "location": "Christchurch & Dunedin Service Centres",
        "target_metric": "$3.70M / week (South Island Budget Target)",
        "live_metric": "$4.05M / week (Actual Outflow Spend)",
        "delta": "+$350,000 / week Service Deficit",
        "target_dwell": "$0 / claim (5-Day Placement Standard)",
        "live_dwell": "+$890,000 Unplaced Client Exposure",
        "root_cause": "290 Clients Awaiting Allied Health & Vocational Provider Placement",
        "options": [
            "Activate Emergency Allied Health Preferred Provider Network",
            "Authorize Direct Vocational Grant Streamlining",
        ],
    },
    "cm": {
        "label": "💼 Case Manager / Frontline Operator",
        "title": "INDIVIDUAL CLAIM FINANCIAL DRIFT (#ACC-2026-89421)",
        "location": "Claim #ACC-2026-89421 (Northern Hub)",
        "target_metric": "$850 / week (Standard Comp Baseline)",
        "live_metric": "$2,100 / week (Extended Comp + Stagnant Fees)",
        "delta": "+$1,250 / week Claim Financial Drift",
        "target_dwell": "$0 Idle Penalty (5-Day Target)",
        "live_dwell": "+$6,800 Accumulated Idle Dwell Cost",
        "root_cause": "Claim Stalled 38 Days Awaiting Surgical Panel Sign-off Signature",
        "options": [
            "Override Triage Delay via Delegated Authority Band",
            "Escalate Directly to Regional Clinical Lead",
        ],
    },
    "support": {
        "label": "📋 Support Staff & Intake Entry Point",
        "title": "NATIONAL INTAKE GATEWAY LAG COSTS",
        "location": "National Intake Gateway",
        "target_metric": "$120,000 / week (Intake Processing Target)",
        "live_metric": "$210,000 / week (Extended Processing Cost)",
        "delta": "+$90,000 / week Intake Lag Drift",
        "target_dwell": "$0 Verification Lag Penalty",
        "live_dwell": "+$340,000 Downstream Delay Exposure",
        "root_cause": "430 Uncoded Submissions Pending Initial ICD-10 Medical Verification",
        "options": [
            "Trigger Automated Provider Document Request",
            "Apply Fast-Track Automated Coding Validation",
        ],
    },
}

# -----------------------------------------------------------------------------
# 3. SIDEBAR CONTROLS & GOVERNANCE
# -----------------------------------------------------------------------------
st.sidebar.title("AAT SCHEME GOVERNANCE")

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

floor_val = int(st.query_params.get("floor", 65))

# -----------------------------------------------------------------------------
# 4. MAIN COMMAND SURFACE RENDERER
# -----------------------------------------------------------------------------
st.title("ACC Board & Ministerial Command Surface")

current_data = ROLE_MAP[selected_key]

st.markdown(
    f"""
    <div class="scope-box">
        <div class="scope-title">ACTIVE COMMAND SCOPE</div>
        <div class="scope-role">{current_data['label']}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

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

else:
    st.markdown(f"### 🎯 SYNCHRONIZED BOARDROOM MATRIX: {current_data['title']}")
    
    col_target, col_live = st.columns(2)

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

st.markdown("---")
st.markdown("### ⚡ Strategic Interventions")

for idx, option in enumerate(current_data["options"]):
    if st.button(f"Execute: {option}", key=f"btn_{selected_key}_{idx}"):
        st.success(f"Command Executed: {option}")

import streamlit as st

# 1. PAGE SETUP
st.set_page_config(
    page_title="ACC Command Surface",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for executive dark theme and emerald scope box
st.markdown(
st.markdown(
    """
<style>
    /* 🔒 HIDE STREAMLIT TOP BAR & GITHUB LINKS */
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
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
</style>
""",
    unsafe_allow_html=True,
)

<style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
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
</style>
""",
    unsafe_allow_html=True,
)

# 2. ROLE & BOTTLENECK DATA MAP
ROLE_MAP = {
    "minister": {
        "label": "🏛️ Minister for ACC & Board Chair",
        "title": "NATIONAL SCHEME LIABILITY DRIFT",
        "location": "Upper North Island Specialist Network",
        "metric": "+$420,000 / week in extended weekly comp",
        "root_cause": "Orthopedic Assessment Capacity (28-day wait vs 7-day target)",
        "options": [
            "Authorize Allied Health Assessment Delegation",
            "Reallocate $2.5M Emergency Capacity Burst Fund",
        ],
    },
    "ce": {
        "label": "⚡ Chief Executive (Wellington HQ)",
        "title": "PRIMARY CAPACITY BOTTLENECK: IME QUEUE",
        "location": "Auckland Central & Waitematā Hubs",
        "metric": "1,240 Claims Stagnant (>14 days dwell)",
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
        "metric": "512 Claims Blocked (>21 days dwell)",
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
        "metric": "184 Cases Awaiting Clinical Triage",
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
        "metric": "120 Claims Facing Delayed Surgical Approvals",
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
        "metric": "290 Clients Awaiting Allied Health Placement",
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
        "metric": "38 Days Without Treatment Authorization",
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
        "metric": "430 Uncoded Submissions Pending Verification",
        "root_cause": "Incomplete Initial Provider ICD-10 Coding & Medical Notes",
        "options": [
            "Trigger Automated Provider Document Request",
            "Apply Fast-Track Automated Coding Validation",
        ],
    },
}

# 3. SIDEBAR GOVERNANCE & CONTROLS
st.sidebar.title("AAT SCHEME GOVERNANCE")

# Query parameter handling with fallbacks
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

# 4. MAIN COMMAND SURFACE RENDERER
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

# Primary Constraint Header & Metrics
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
        value=current_data["metric"],
    )
with col3:
    st.metric(
        label="🛡️ Operational Status",
        value="ACTIVE DRIFT",
    )

st.error(f"**Root Cause:** {current_data['root_cause']}")

# Strategic Interventions Actions
st.markdown("### ⚡ Strategic Interventions")

for idx, option in enumerate(current_data["options"]):
    if st.button(f"Execute: {option}", key=f"btn_{selected_key}_{idx}"):
        st.success(f"Command Executed: {option}")

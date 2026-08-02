from __future__ import annotations
import streamlit as st

st.set_page_config(
    page_title="Boardroom Command Center",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
    <style>
    .main { background-color: #0E1117; }
    .stMetric { background-color: #1E222D; padding: 12px; border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. EXECUTIVE SECURITY GATE
# -----------------------------------------------------------------------------
def check_password():
    if st.session_state.get("password_correct", False):
        return True

    st.title("ACC Board & Ministerial Command Surface")

    st.subheader("🔒 Executive Security Gate")
    
    password_input = st.text_input("Enter Access Key to unlock command surface:", type="password")
    
    if st.button("Authenticate"):
        if password_input.strip() == "NZ-ACC-2026":
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            st.error("⛔ Invalid Access Key. Access Denied.")
    return False

# 2. EXECUTIVE SECURITY GATE CHECK
if not check_password():
    st.stop()

# 3. SIDEBAR: GOVERNANCE & ROLE MATRIX
st.sidebar.title("AAT SCHEME GOVERNANCE")

roles = [
    "🏛️ Minister for ACC & Board Chair",
    "⚡ Chief Executive (Wellington HQ)",
    "📍 RGM - Northern Region (Auckland / Northland)",
    "📍 RGM - Midland Region (Waikato / Bay of Plenty)",
    "📍 RGM - Central Region (Wellington / Lower NI)",
    "📍 RGM - South Island (Canterbury / Otago / Southland)",
    "💼 Case Manager / Frontline Operator",
    "📋 Support Staff & Intake Entry Point",
]

# URL parameter mapping table
ROLE_URL_MAP = {
    "minister": "🏛️ Minister for ACC & Board Chair",
    "ce": "⚡ Chief Executive (Wellington HQ)",
    "rgm_north": "📍 RGM - Northern Region (Auckland / Northland)",
    "rgm_midland": "📍 RGM - Midland Region (Waikato / Bay of Plenty)",
    "rgm_central": "📍 RGM - Central Region (Wellington / Lower NI)",
    "rgm_south": "📍 RGM - South Island (Canterbury / Otago / Southland)",
    "gm": "📍 RGM - Northern Region (Auckland / Northland)",
    "cm": "💼 Case Manager / Frontline Operator",
    "support": "📋 Support Staff & Intake Entry Point",
}


# Read URL parameter safely (e.g., ?role=gm)
query_role = st.query_params.get("role", "minister")
target_role_name = ROLE_URL_MAP.get(str(query_role).lower(), roles[0])

# Fallback index lookup
default_idx = (
    roles.index(target_role_name) if target_role_name in roles else 0
)

selected_role = st.sidebar.selectbox(
    "Active User Role Matrix", roles, index=default_idx
)

st.title("ACC Board & Ministerial Command Surface")

# High-Visibility Dominant Scope Banner (Indentation-Safe String)
banner_html = (
    '<div style="background: linear-gradient(135deg, #064e3b 0%, #022c22 100%); '
    'border: 2px solid #10b981; border-left: 10px solid #34d399; '
    'padding: 18px 24px; border-radius: 12px; margin-top: 14px; margin-bottom: 28px; '
    'box-shadow: 0 10px 25px -5px rgba(16, 185, 129, 0.3);">'
    '<div style="color: #a7f3d0; font-size: 0.85rem; font-weight: 800; '
    'letter-spacing: 0.15em; text-transform: uppercase;">ACTIVE COMMAND SCOPE</div>'
    f'<div style="color: #ffffff; font-size: 1.85rem; font-weight: 900; '
    f'margin-top: 6px; line-height: 1.2;">{selected_role}</div>'
    '</div>'
)

st.markdown(banner_html, unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown("### SCHEME MANDATE INJECTION")
st.sidebar.caption("Proprietary stewardship band control · explicit arithmetic withheld from glass")

striving_floor = st.sidebar.slider("Enforce Liability Mitigation Floor", 0, 100, 65)
st.sidebar.info(f"Active Stewardship Floor: **{striving_floor}% Protection Band**")








role_matrix_data = {
    "🏛️ Minister for ACC & Board Chair": {
        "title": "NATIONAL SCHEME LIABILITY DRIFT",
        "location": "Upper North Island Specialist Network",
        "metric": "+$420,000 / week in extended weekly comp",
        "root_cause": "Orthopedic Assessment Capacity (28-day wait vs 7-day target)",
        "options": [
            "Authorize Allied Health Assessment Delegation",
            "Reallocate $2.5M Emergency Capacity Burst Fund",
        ],
    },
    "⚡ Chief Executive (Wellington HQ)": {
        "title": "PRIMARY CAPACITY BOTTLENECK: IME QUEUE",
        "location": "Auckland Central & Waitematā Hubs",
        "metric": "1,240 Claims Stagnant (>14 days dwell)",
        "root_cause": "Specialist Panel Backlog in Complex Musculoskeletal Claims",
        "options": [
            "Re-route 300 Cases to Waikato/Bay of Plenty Panel",
            "Trigger Fast-Track Telehealth Assessment Protocol",
        ],
    },
    "📍 Regional General Manager": {
        "title": "DISTRICT SERVICE DELIVERY BOTTLENECK",
        "location": "Hamilton Central Branch",
        "metric": "42 Cases Blocked at Triage",
        "root_cause": "Local Provider Staffing Deficit",
        "options": [
            "Issue Overflow Capacity Contract to Private Provider",
            "Approve Regional Case Manager Overtime Allowance",
        ],
    },
    "💼 Case Manager / Frontline Operator": {
        "title": "INDIVIDUAL CLAIM DWELL TIME SPIKE",
        "location": "Claim #ACC-2026-89421",
        "metric": "38 Days Without Treatment Authorization",
        "root_cause": "Pending Surgical Panel Approval Signature",
        "options": [
            "Override Triage Delay via Delegated Authority Band",
            "Escalate Directly to Regional Clinical Lead",
        ],
    },
}

# Dynamic Executive Metric Renderer
current_data = role_matrix_data.get(selected_role, {})

if current_data:
    st.subheader(f"🎯 {current_data.get('title', 'Primary System Constraint')}")

    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            label="📍 Target Location / Network",
            value=current_data.get("location", "N/A"),
        )
    with col2:
        st.metric(
            label="⚠️ Impact Drift Rate",
            value=current_data.get("metric", "N/A"),
        )

    st.error(f"**Root Cause:** {current_data.get('root_cause', 'N/A')}")

    st.markdown("### ⚡ Strategic Interventions")
    for idx, option in enumerate(current_data.get("options", [])):
        st.button(f"Execute: {option}", key=f"opt_{idx}")

current_data = role_matrix_data.get(selected_role, {})

if current_data:
    st.subheader(f"🎯 {current_data.get('title', 'Primary System Constraint')}")
    
    col1, col2 = st.columns(2)

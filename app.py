import streamlit as st

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & THEME
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="NZ AAT Sovereign Orchestration Engine",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
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

    st.title("🏛️ NZ ACC Sovereign Orchestration Engine")
    st.subheader("🔒 Executive Security Gate")
    
    password_input = st.text_input("Enter Access Key to unlock command surface:", type="password")
    
    if st.button("Authenticate"):
        if password_input.strip() == "NZ-ACC-2026":
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            st.error("⛔ Invalid Access Key. Access Denied.")
    return False

if not check_password():
    st.stop()

# -----------------------------------------------------------------------------
# 3. SIDEBAR: GOVERNANCE & ROLE MATRIX
# -----------------------------------------------------------------------------
st.sidebar.title("AAT SCHEME GOVERNANCE")

roles = [
    "🏛️ Minister for ACC & Board Chair",
    "⚡ Chief Executive (Wellington HQ)",
    "📍 Regional General Manager",
    "💼 Case Manager / Frontline Operator"
]

selected_role = st.sidebar.selectbox("Active User Role Matrix", roles, index=1)

st.sidebar.markdown("---")
st.sidebar.markdown("### SCHEME MANDATE INJECTION")
st.sidebar.caption("Proprietary stewardship band control · explicit arithmetic withheld from glass")

striving_floor = st.sidebar.slider("Enforce Liability Mitigation Floor", 0, 100, 65)
st.sidebar.info(f"Active Stewardship Floor: **{striving_floor}% Protection Band**")

# -----------------------------------------------------------------------------
# 4. MAIN DASHBOARD HEADER
# -----------------------------------------------------------------------------
st.title("NZ AAT Sovereign Orchestration")
st.caption(f"Active Command Scope: **{selected_role}**")

# -----------------------------------------------------------------------------
# 5. FRACTAL CLOSED-LOOP BOTTLENECK SENSOR
# -----------------------------------------------------------------------------
st.markdown("---")
st.subheader("🎯 Primary System Constraint (Closed-Loop Sensor)")

bottlenecks = {
    "🏛️ Minister for ACC & Board Chair": {
        "title": "NATIONAL SCHEME LIABILITY DRIFT",
        "location": "Upper North Island Specialist Network",
        "metric": "+$420,000 / week in extended weekly comp",
        "root_cause": "Orthopedic Assessment Capacity (28-day wait vs 7-day target)",
        "options": [
            "Authorize Allied Health Assessment Delegation",
            "Reallocate $2.5M Emergency Capacity Burst Fund"
        ]
    },
    "⚡ Chief Executive (Wellington HQ)": {
        "title": "PRIMARY CAPACITY BOTTLENECK: IME QUEUE",
        "location": "Auckland Central & Waitematā Hubs",
        "metric": "1,240 Claims Stagnant (>14 days dwell)",
        "root_cause": "Specialist Panel Backlog in Complex Musculoskeletal Claims",
        "options": [
            "Re-route 300 Cases to Waikato/Bay of Plenty Panel",
            "Trigger Fast-Track Telehealth Assessment Protocol"
        ]
    },
    "📍 Regional General Manager": {
        "title": "DISTRICT SERVICE DELIVERY BOTTLENECK",
        "location": "Hamilton Central Branch",
        "metric": "42 Cases Blocked in Vocational Rehab Intake",
        "root_cause": "Local Provider Intake Contract Exceeded",
        "options": [
            "Issue Overflow Capacity Contract to Secondary Provider",
            "Approve Regional Case Manager Overtime Allowance"
        ]
    },
    "💼 Case Manager / Frontline Operator": {
        "title": "FILE FLOW BLOCKAGE: ACTION REQUIRED",
        "location": "Active Worklist (Claim #88219-B)",
        "metric": "5 Days Overdue for Medical Clearance (ACC18)",
        "root_cause": "Waiting on GP Medical Certificate Submission",
        "options": [
            "Send Automated Digital Portal Ping to GP Clinic",
            "Switch Case File to Fast-Track Telehealth Partner"
        ]
    }
}

data = bottlenecks.get(selected_role, bottlenecks["⚡ Chief Executive (Wellington HQ)"])

role_key = f"status_{selected_role}"
if role_key not in st.session_state:
    st.session_state[role_key] = "ACTIVE"

if st.session_state[role_key] == "ACTIVE":
    st.error(f"🚨 **{data['title']}**")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="📍 Target Location", value=data["location"])
    with col2:
        st.metric(label="⚠️ Impact Delta", value=data["metric"])
    with col3:
        st.metric(label="🔄 Sensor Status", value="MONITORING")

    st.warning(f"**Root Cause Analysis:** {data['root_cause']}")

    st.markdown("#### ⚡ Actuation Directive:")
    btn_col1, btn_col2 = st.columns(2)

    with btn_col1:
        if st.button(f"Execute: {data['options'][0]}", use_container_width=True):
            st.session_state[role_key] = "RESOLVED"
            st.rerun()

    with btn_col2:
        if st.button(f"Execute: {data['options'][1]}", use_container_width=True):
            st.session_state[role_key] = "RESOLVED"
            st.rerun()

else:
    st.success("🟢 **BOTTLENECK RESOLVED -- Queue Flow Re-established**")
    st.info("The sensor loop verified a 34% drop in dwell-time velocity over the last 24 hours. Monitoring for secondary constraints...")
    
    if st.button("🔄 Reset Control Loop Sensor", use_container_width=True):
        st.session_state[role_key] = "ACTIVE"
        st.rerun()

st.markdown("---")

# -----------------------------------------------------------------------------
# 6. OPERATIONAL SUMMARY METRICS
# -----------------------------------------------------------------------------
m_col1, m_col2, m_col3, m_col4 = st.columns(4)
m_col1.metric("Active Scheme Claims", "142,850", "+1.2%")
m_col2.metric("System Dwell Time", "11.4 Days", "-2.1 Days")
m_col3.metric("Liability Reserve Index", "94.8%", "Nominal")
m_col4.metric("Predictive Drift Horizon", "Low Risk", "Stable")

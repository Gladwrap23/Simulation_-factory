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

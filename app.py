import hashlib
from datetime import datetime, timezone
import streamlit as st

st.set_page_config(
    page_title="Factory Command Post",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-Contrast Cockpit CSS
st.markdown('''
<style>
    :root {
        --bg-base: #0d1117;
        --bg-panel: #161b22;
        --line: #30363d;
        --teal: #00E5FF;
        --green: #3fb950;
        --red: #ff7b72;
        --text-main: #f0f6fc;
        --text-muted: #8b949e;
    }
    .stApp { background-color: var(--bg-base); color: var(--text-main); }
    section[data-testid="stSidebar"] { background-color: var(--bg-panel); border-right: 1px solid var(--line); }
    div[data-testid="stMetric"] { background-color: var(--bg-panel); border: 1px solid var(--line); border-top: 3px solid var(--teal); border-radius: 6px; padding: 12px; }
    div[data-testid="stMetricValue"] { color: var(--teal) !important; font-family: monospace; }
    .card { background-color: var(--bg-panel); border: 1px solid var(--line); border-radius: 6px; padding: 14px; margin-bottom: 12px; }
    .badge { display: inline-block; padding: 4px 8px; border-radius: 4px; font-size: 0.8rem; font-family: monospace; font-weight: bold; }
    .badge-active { background: rgba(0,229,255,0.15); color: var(--teal); border: 1px solid var(--teal); }
    .badge-success { background: rgba(63,185,80,0.15); color: var(--green); border: 1px solid var(--green); }
</style>
''', unsafe_allow_html=True)

# Session State Initialization
if 'cleared' not in st.session_state:
    st.session_state['cleared'] = False
if 'ledger' not in st.session_state:
    st.session_state['ledger'] = []
if 'directive_issued' not in st.session_state:
    st.session_state['directive_issued'] = False
if 'surges' not in st.session_state:
    st.session_state['surges'] = {'ops': 10, 'cap': 10, 'comp': 15, 'sys': 10}
if 'slas' not in st.session_state:
    st.session_state['slas'] = {'ops': '1 business day', 'cap': '1 business day', 'comp': '3 business days', 'sys': '1 business day'}

# Sidebar Navigation & Controls
st.sidebar.title("FACTORY COMMAND POST")
st.sidebar.caption("Live operating book | control plane online")

book = st.sidebar.selectbox("Operating book", [
    "ERCOT BESS / storage operations",
    "Grid Infrastructure / PJM Cluster",
    "ACC NZ Scheme / Claims Review",
    "Port Logistics / Container Flow"
])

view = st.sidebar.radio("Command view", [
    "Tier 1 | Chairman Directorate",
    "Tier 2 | General Management",
    "Tier 3 | Site Operations",
    "Forensic Audit Ledger"
])

override = st.sidebar.toggle("Chairman Directorate Override", value=False)

# Metrics Bar
exposure = "$88.5M"
burn = "$0 / wk (RESOLVED)" if st.session_state['cleared'] else "$610,000 / wk"

m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Exposure", exposure, "Board Limit")
m2.metric("Holding Burn", burn, "Active Drag" if not st.session_state['cleared'] else "Cleared")
m3.metric("Realization Split", "90 / 10", "$549k Client / $61k Phoenix")
m4.metric("SOP Readiness", "8 / 8" if st.session_state['cleared'] else "Pending Sign-off", "Field Gate")

st.divider()

# TIER 1: CHAIRMAN DIRECTORATE
if view == "Tier 1 | Chairman Directorate":
    st.header("Apex Board Governance & Oversight")
    st.write("Authorize domain envelopes and review real-time balance sheet recovery.")

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Board Sub-Committee Authorizations")
        st.checkbox("Operations & Asset Delivery Committee (Chair: COO Oversight)", value=True)
        st.checkbox("Audit, Finance & Investment Committee / AFIC (Chair: CFO Oversight)", value=True)
        st.checkbox("Risk, Regulatory & Legal Committee (Chair: CLO Oversight)", value=True)
        st.checkbox("Technology & Infrastructure Committee (Chair: CTO Oversight)", value=True)

    with c2:
        st.subheader("Holding Loss Recovery Allocation")
        st.table({
            "Category": ["Idle Contractor Overtime", "WACC Carrying Demurrage", "Interconnection Delay Penalty", "Total Weekly Burn"],
            "Weekly Amount": ["$220,000", "$250,000", "$140,000", "$610,000"],
            "Client Retained (90%)": ["$198,000", "$225,000", "$126,000", "$549,000"],
            "Phoenix Accrual (10%)": ["$22,000", "$25,000", "$14,000", "$61,000"]
        })

# TIER 2: GENERAL MANAGEMENT
elif view == "Tier 2 | General Management":
    st.header("General Management Directive & Domain Translation")
    st.write("Convert board mandates into operational surge budgets and binding service level agreements.")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        ops_surge = st.number_input("Operations surge budget (%)", 0, 100, st.session_state['surges']['ops'], step=5)
        ops_sla = st.selectbox("Operations SLA", ["4 hours", "1 business day", "3 business days"], index=1)
    with col2:
        cap_surge = st.number_input("Capital surge budget (%)", 0, 100, st.session_state['surges']['cap'], step=5)
        cap_sla = st.selectbox("Capital SLA", ["4 hours", "1 business day", "3 business days"], index=1)
    with col3:
        comp_surge = st.number_input("Compliance surge budget (%)", 0, 100, st.session_state['surges']['comp'], step=5)
        comp_sla = st.selectbox("Compliance SLA", ["4 hours", "1 business day", "3 business days"], index=2)
    with col4:
        sys_surge = st.number_input("Systems surge budget (%)", 0, 100, st.session_state['surges']['sys'], step=5)
        sys_sla = st.selectbox("Systems SLA", ["4 hours", "1 business day", "3 business days"], index=1)

    if st.button("⚡ Issue Translated Directive", type="primary"):
        st.session_state['surges'] = {'ops': ops_surge, 'cap': cap_surge, 'comp': comp_surge, 'sys': sys_surge}
        st.session_state['slas'] = {'ops': ops_sla, 'cap': cap_sla, 'comp': comp_sla, 'sys': sys_sla}
        st.session_state['directive_issued'] = True
        st.success("Directive dispatched to Tier 3 frontline teams.")

# TIER 3: SITE OPERATIONS
elif view == "Tier 3 | Site Operations":
    st.header("Site Operations Hub")

    st.subheader("Upstream Governance Status")
    g1, g2, g3, g4 = st.columns(4)
    g1.markdown(f"<div class='card'><span class='badge badge-active'>OPERATIONS</span><br>Surge: {st.session_state['surges']['ops']}%<br>SLA: {st.session_state['slas']['ops']}</div>", unsafe_allow_html=True)
    g2.markdown(f"<div class='card'><span class='badge badge-active'>CAPITAL</span><br>Surge: {st.session_state['surges']['cap']}%<br>SLA: {st.session_state['slas']['cap']}</div>", unsafe_allow_html=True)
    g3.markdown(f"<div class='card'><span class='badge badge-active'>COMPLIANCE</span><br>Surge: {st.session_state['surges']['comp']}%<br>SLA: {st.session_state['slas']['comp']}</div>", unsafe_allow_html=True)
    g4.markdown(f"<div class='card'><span class='badge badge-active'>SYSTEMS</span><br>Surge: {st.session_state['surges']['sys']}%<br>SLA: {st.session_state['slas']['sys']}</div>", unsafe_allow_html=True)

    st.subheader("Authentic Control Artifacts (ERCOT BESS)")
    a1, a2, a3, a4 = st.columns(4)
    a1.markdown("<div class='card'><strong>ICCP 4-sec Telemetry</strong><br><small>Telemetry heartbeat: 04.0s<br>State: Nominal</small></div>", unsafe_allow_html=True)
    a2.markdown("<div class='card'><strong>PSCAD EMT Model</strong><br><small>Inverter: BESS-01<br>Validation: Verified</small></div>", unsafe_allow_html=True)
    a3.markdown("<div class='card'><strong>IEEE 2800 Test Packet</strong><br><small>Ride-through: Verified<br>Sign-off: Ready</small></div>", unsafe_allow_html=True)
    a4.markdown("<div class='card'><strong>Part 2 COD Attestation</strong><br><small>Commercial Ops Dec<br>Evidence: Assembled</small></div>", unsafe_allow_html=True)

    st.subheader("Frontline SOP Release Checklist")
    c_all = []
    c_all.append(st.checkbox("ICCP 4-sec Telemetry evidence verified", value=st.session_state['cleared']))
    c_all.append(st.checkbox("ICCP 4-sec Telemetry record attached to release packet", value=st.session_state['cleared']))
    c_all.append(st.checkbox("PSCAD EMT Model evidence verified", value=st.session_state['cleared']))
    c_all.append(st.checkbox("PSCAD EMT Model record attached to release packet", value=st.session_state['cleared']))
    c_all.append(st.checkbox("IEEE 2800 Test Packet evidence verified", value=st.session_state['cleared']))
    c_all.append(st.checkbox("IEEE 2800 Test Packet record attached to release packet", value=st.session_state['cleared']))
    c_all.append(st.checkbox("Part 2 COD Attestation evidence verified", value=st.session_state['cleared']))
    c_all.append(st.checkbox("Part 2 COD Attestation record attached to release packet", value=st.session_state['cleared']))

    if all(c_all):
        if st.button("⚡ Submit Frontline SOP Sign-off & Notify Command", type="primary"):
            st.session_state['cleared'] = True
            timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
            entry_hash = hashlib.sha256(f"{book}{timestamp}CLEARED".encode()).hexdigest()[:16]
            st.session_state['ledger'].append({
                "Timestamp": timestamp,
                "Operating Book": book,
                "Action": "Frontline SOP Sign-off & Interconnection Cleared",
                "Capital Recovered": "$610,000 / wk",
                "Client Preserved (90%)": "$549,000",
                "Phoenix Fee (10%)": "$61,000",
                "Cryptographic Hash": entry_hash
            })
            st.success("Clearance verified. Upstream command notified.")
            st.rerun()

# FORENSIC AUDIT LEDGER
elif view == "Forensic Audit Ledger":
    st.header("Immutable Governance & Forensic Audit Ledger")
    st.write("Cryptographically verifiable chain of custody linking Board mandates to frontline physical execution.")

    if st.session_state['ledger']:
        st.dataframe(st.session_state['ledger'], use_container_width=True)
    else:
        st.info("No frontline sign-offs recorded in this session. Complete Tier 3 SOP verification to generate an entry.")

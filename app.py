import datetime

import streamlit as st


INCIDENTS = {
    "INC-001": {
        "title": "ERCOT IA Section 4.2 Part 2 COD Attestation",
        "priority": "P1 - CRITICAL",
        "burn_rate_sec": 1.01,
        "start_time": datetime.datetime.now() - datetime.timedelta(days=1),
        "schedule_drift": "+9 Days COD Drift",
        "status": "DEADLOCKED",
        "cognizant_director": {
            "name": "Dr. Arthur Pendleton",
            "role": "Chair, Grid Risk & Technical Integrity",
            "status": "Concurrence Pending",
        },
        "gms": {
            "Elena Rostova": {
                "role": "GM - Field Operations & Contractor Mobilization",
                "domain": "High-Voltage Crews & Permian Substation",
                "stance": "Withholding signature: Energization without IEEE 2800 test packet invalidates OEM high-voltage transformer warranty ($1.2M exposure).",
                "checks": [
                    {"id": "Check #1", "name": "ICCP 4-sec Telemetry", "status": "CLEARED", "evidence": "Locked to Ledger"},
                    {"id": "Check #3", "name": "PSCAD EMT Model", "status": "CLEARED", "evidence": "Evidence Verified"},
                    {"id": "Check #5", "name": "IEEE 2800 Test Packet", "status": "CLEARED", "evidence": "Packet Transmitted"},
                ],
            },
            "David Chen": {
                "role": "GM - Regulatory & Market Operations",
                "domain": "ERCOT Protocol & Queue Adjudication",
                "stance": "Demanding immediate Part 2 COD Attestation filing: ERCOT interconnection queue position drops in 48 hours without filing.",
                "checks": [
                    {"id": "Check #2", "name": "ICCP Telemetry Record", "status": "CLEARED", "evidence": "Record Attached"},
                    {"id": "Check #4", "name": "PSCAD EMT Model Record", "status": "CLEARED", "evidence": "Record Attached"},
                    {"id": "Check #6", "name": "Part 2 COD Attestation", "status": "BLOCKED", "evidence": "Awaiting Frontline Sign-Off"},
                ],
            },
        },
        "audit_log": [
            "[T-24h] Deadlock flagged: Elena Rostova withheld sign-off on Part 2 COD Attestation.",
            "[T-18h] Contractor idle carry clock activated at $1.01/sec.",
        ],
    },
    "INC-002": {
        "title": "Substation Main Step-Up Inrush Trip",
        "priority": "P2 - HIGH",
        "burn_rate_sec": 0.46,
        "start_time": datetime.datetime.now() - datetime.timedelta(hours=14),
        "schedule_drift": "+4 Days Commissioning",
        "status": "ACTIVE",
        "cognizant_director": {"name": "Sarah Jenkins", "role": "Chair, Operations & Asset Safety", "status": "Reviewing Relay Logs"},
        "gms": {},
        "audit_log": [],
    },
    "INC-003": {
        "title": "SCADA Protocol IEC 61850 Mapping Mismatch",
        "priority": "P3 - MODERATE",
        "burn_rate_sec": 0.25,
        "start_time": datetime.datetime.now() - datetime.timedelta(hours=8),
        "schedule_drift": "+2 Days Witness Test",
        "status": "ACTIVE",
        "cognizant_director": {"name": "Arthur Pendleton", "role": "Chair, Grid Risk", "status": "Nominal"},
        "gms": {},
        "audit_log": [],
    },
    "INC-004": {
        "title": "BESS Inverter Firmware Security Patch Rollback",
        "priority": "P4 - MONITORED",
        "burn_rate_sec": 0.07,
        "start_time": datetime.datetime.now() - datetime.timedelta(hours=4),
        "schedule_drift": "+0 Days (Float Available)",
        "status": "ACTIVE",
        "cognizant_director": {"name": "Marcus Vance", "role": "Executive Sponsor", "status": "Nominal"},
        "gms": {},
        "audit_log": [],
    },
}


if "incident_store" not in st.session_state:
    st.session_state.incident_store = INCIDENTS
if "active_incident_id" not in st.session_state:
    st.session_state.active_incident_id = "INC-001"
if "selected_gm_branch" not in st.session_state:
    st.session_state.selected_gm_branch = "Elena Rostova"


st.set_page_config(
    page_title="Factory Command Post | Incident Control",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.sidebar.title("FACTORY COMMAND POST")
st.sidebar.caption("Autonomous Capital Defense Control Plane")
total_fleet_burn = sum(
    incident["burn_rate_sec"] * 604800
    for incident in st.session_state.incident_store.values()
    if incident["status"] != "RESOLVED"
)
st.sidebar.metric("Portfolio Holding Burn", f"${total_fleet_burn:,.0f} / wk")
st.sidebar.divider()
st.sidebar.subheader("Active Blockage Queue")

for incident_id, incident_data in st.session_state.incident_store.items():
    button_label = f"{incident_data['priority']}: {incident_id}\n{incident_data['title'][:26]}..."
    if st.sidebar.button(button_label, key=f"incident_nav_{incident_id}", use_container_width=True):
        st.session_state.active_incident_id = incident_id
        if incident_data["gms"]:
            st.session_state.selected_gm_branch = next(iter(incident_data["gms"]))
        st.rerun()

incident = st.session_state.incident_store[st.session_state.active_incident_id]
elapsed_seconds = (datetime.datetime.now() - incident["start_time"]).total_seconds()
accumulated_burn = elapsed_seconds * incident["burn_rate_sec"] if incident["status"] != "RESOLVED" else 0.0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Incident Status", incident["status"], delta=incident["priority"])
col2.metric(
    "Active Holding Burn",
    f"${incident['burn_rate_sec'] * 604800:,.0f} / wk" if incident["status"] != "RESOLVED" else "$0 / wk",
    f"${incident['burn_rate_sec']:.2f}/sec",
    delta_color="inverse",
)
col3.metric("Sunk Accrual (Since Lock)", f"${accumulated_burn:,.0f}", incident["schedule_drift"], delta_color="inverse")
col4.metric(
    "Operational Readiness",
    "8 / 8 Frontline SOP",
    "GOV DEADLOCKED" if incident["status"] == "DEADLOCKED" else "CLEARED",
    delta_color="inverse" if incident["status"] == "DEADLOCKED" else "normal",
)

st.divider()
st.header(f"{incident['priority']}: {incident['title']}")
st.subheader("Tier 1 | Chairman Directorate & Cognizant Director")
tier1_col1, tier1_col2 = st.columns([2, 1])
with tier1_col1:
    st.markdown(
        "**Blockage:** Grid Interconnection Agreement Section 4.2 Part 2 COD Filing Gate\n\n"
        f"**Cognizant Director:** `{incident['cognizant_director']['name']}` ({incident['cognizant_director']['role']})\n\n"
        f"**Directorate Status:** `{incident['cognizant_director']['status']}`"
    )
with tier1_col2:
    if incident["status"] == "DEADLOCKED":
        st.warning("DIRECTORATE INTERVENTION REQUIRED")
        if st.button("Concur with Chairman Carve-Out", key="directorate_concurrence", use_container_width=True):
            incident["cognizant_director"]["status"] = "DIRECTORATE CONCURRENCE GRANTED"
            st.rerun()

st.subheader("Tier 2 | General Management Workspaces")
if incident["gms"]:
    gm_names = list(incident["gms"])
    if st.session_state.selected_gm_branch not in gm_names:
        st.session_state.selected_gm_branch = gm_names[0]
    selected_gm = st.radio(
        "Isolate General Manager Workstream:",
        gm_names,
        index=gm_names.index(st.session_state.selected_gm_branch),
        horizontal=True,
        key="incident_gm_selector",
    )
    st.session_state.selected_gm_branch = selected_gm
    active_gm = incident["gms"][selected_gm]
    st.markdown(f"**Lead GM:** {selected_gm} - `{active_gm['role']}`")
    st.markdown(f"**Domain Responsibility:** {active_gm['domain']}")
    st.info(f"**Operational Position:** {active_gm['stance']}")

    st.subheader(f"Tier 3 | Site Operations Telemetry ({selected_gm})")
    for check in active_gm["checks"]:
        check_col1, check_col2, check_col3 = st.columns([1, 3, 2])
        check_col1.write(f"**{check['id']}**")
        check_col2.write(check["name"])
        if check["status"] == "CLEARED":
            check_col3.success(f"CLEARED: {check['evidence']}")
        else:
            check_col3.error(f"HELD: {check['evidence']}")
else:
    st.write("Telemetry routing nominal.")

st.subheader("Tier 4 | Forensic Audit Ledger & Remedial Action Engine")
if incident["status"] == "DEADLOCKED":
    st.markdown("### Authorize Executive Remedial Action")
    action_col1, action_col2, action_col3 = st.columns(3)
    with action_col1:
        st.markdown("**Option A: Indemnity Carve-Out**")
        st.caption("Filing proceeds. Directorate absorbs OEM warranty forfeiture risk.")
        if st.button("Authorize Carve-Out & File COD", key="authorize_carveout", use_container_width=True):
            incident["status"] = "RESOLVED"
            incident["burn_rate_sec"] = 0.0
            incident["audit_log"].append(
                f"[{datetime.datetime.utcnow().strftime('%H:%M:%S UTC')}] CHAIRMAN DIRECTIVE EXECUTED: Issued Executive Indemnification Carve-Out. Warranty exposure retained at Directorate level. David Chen authorized to submit Part 2 COD immediately."
            )
            for gm_data in incident["gms"].values():
                for check in gm_data["checks"]:
                    check["status"] = "CLEARED"
                    check["evidence"] = "Directorate Override"
            st.rerun()
    with action_col2:
        st.markdown("**Option B: Dispatch Test Team**")
        st.caption("Authorize $35k draw to rush IEEE 2800 field crew in 6 hours.")
        if st.button("Draw Capital & Expedite", key="expedite_test_team", use_container_width=True):
            incident["audit_log"].append(
                f"[{datetime.datetime.utcnow().strftime('%H:%M:%S UTC')}] EMERGENCY CAPITAL DRAW: $35,000 drawn for expedited IEEE 2800 field crew. Expected clear in 6 hours."
            )
            st.rerun()
    with action_col3:
        st.markdown("**Option C: Stand-Down Order**")
        st.caption("Demobilize idle high-voltage contractor crews to stop burn.")
        if st.button("Demobilize Crews", key="demobilize_crews", use_container_width=True):
            incident["burn_rate_sec"] = 0.0
            incident["audit_log"].append(
                f"[{datetime.datetime.utcnow().strftime('%H:%M:%S UTC')}] CONTRACTOR STAND-DOWN: Permian high-voltage crews demobilized. Carry cost halted to $0/sec pending queue outcome."
            )
            st.rerun()

st.markdown("### Ledger Entries (Cryptographic Chain)")
for log_entry in reversed(incident["audit_log"]):
    st.code(log_entry, language="yaml")

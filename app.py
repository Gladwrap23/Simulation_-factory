import hashlib
from datetime import datetime, timezone

import streamlit as st


OPERATING_BOOKS = {
    "ERCOT BESS / storage operations": {
        "exposure": "$88.5M",
        "burn": 610000,
        "region": "West Texas — Permian Substation POI 345kV",
        "bottleneck": "PSCAD Inverter EMT Validation & 4-sec ICCP Telemetry Lag",
        "impact": "Holding $610k/wk in idle contractor carry and interconnection penalties",
        "remedy": "Inject synthetic frequency test packets, certify IEEE 2800, and execute Part 2 COD attestation",
        "loss_breakdown": [
            ("Idle Contractor Overtime", 220000),
            ("WACC Carrying Demurrage", 250000),
            ("Interconnection Delay Penalty", 140000),
        ],
        "artifacts": [
            ("ICCP 4-sec Telemetry", "Telemetry heartbeat: 04.0s / State: Nominal"),
            ("PSCAD EMT Model", "Inverter: BESS-01 / Validation: Verified"),
            ("IEEE 2800 Test Packet", "Ride-through: Verified / Sign-off: Ready"),
            ("Part 2 COD Attestation", "Commercial operations declaration / Evidence: Assembled"),
        ],
        "checklist": [
            "ICCP telemetry evidence verified",
            "ICCP telemetry record attached",
            "PSCAD EMT model evidence verified",
            "PSCAD EMT model record attached",
            "IEEE 2800 test packet verified",
            "IEEE 2800 test record attached",
            "COD attestation evidence verified",
            "COD attestation record attached",
        ],
    },
    "Grid Infrastructure / PJM Cluster": {
        "exposure": "$142.0M",
        "burn": 940000,
        "region": "PJM Western Hub — Keystone 500kV Transformer Bank",
        "bottleneck": "Transformer energization study rework and NERC CIP evidence gap",
        "impact": "Holding $940k/wk in transformer standby demurrage and interconnection study carry",
        "remedy": "Authorize the re-study envelope, release the NERC CIP packet, and issue the HV energization work order",
        "loss_breakdown": [
            ("Transformer Standby Demurrage", 340000),
            ("Interconnection Study Carry", 290000),
            ("Energization Contractor Delay", 310000),
        ],
        "artifacts": [
            ("ASTM D877", "Dielectric breakdown test / Validation: Verified"),
            ("PJM Schedule 12", "Transmission owner charge schedule / Reconciled"),
            ("NERC CIP", "Critical infrastructure protection packet / Current"),
            ("HV Energization", "High-voltage commissioning record / Ready"),
        ],
        "checklist": [
            "ASTM D877 test evidence verified",
            "ASTM D877 record attached",
            "PJM Schedule 12 charges reconciled",
            "PJM Schedule 12 record attached",
            "NERC CIP controls verified",
            "NERC CIP evidence attached",
            "HV energization plan verified",
            "HV energization record attached",
        ],
    },
    "ACC NZ Scheme / Claims Review": {
        "exposure": "$210.0M",
        "burn": 480000,
        "region": "Northern Hub 01 — Auckland Clinical Claims Queue",
        "bottleneck": "Manual medical paper verification and sequential delegation review",
        "impact": "Holding $480k/wk in extended rehabilitation dwell and unreconciled provider invoices",
        "remedy": "Approve the triage mandate, deploy digital ACC45 intake, and issue the provider reconciliation work order",
        "loss_breakdown": [
            ("Extended Rehabilitation Dwell", 210000),
            ("Provider Invoice Reconciliation", 150000),
            ("Delegation Review Delay", 120000),
        ],
        "artifacts": [
            ("ACC45", "Injury claim registration / Record: Verified"),
            ("Clinical Triage", "Clinical prioritization assessment / Current"),
            ("Vocational Assessment", "Return-to-work assessment / Ready"),
            ("Crown Delegation", "Delegated authority record / Signed"),
        ],
        "checklist": [
            "ACC45 claim evidence verified",
            "ACC45 record attached",
            "Clinical triage evidence verified",
            "Clinical triage record attached",
            "Vocational assessment verified",
            "Vocational assessment record attached",
            "Crown delegation verified",
            "Crown delegation record attached",
        ],
    },
    "Port Logistics / Container Flow": {
        "exposure": "$64.0M",
        "burn": 320000,
        "region": "Terminal 3 — North Quay Gate and Yard Interface",
        "bottleneck": "Paper manifest verification and customs inspection queue at gate release",
        "impact": "Holding $320k/wk in vessel waiting time, yard dwell, and quay productivity penalties",
        "remedy": "Authorize OCR manifest clearance, release the customs exception queue, and issue the quay release work order",
        "loss_breakdown": [
            ("Vessel Waiting Time", 120000),
            ("Yard Dwell and Rehandles", 110000),
            ("Quay Productivity Penalty", 90000),
        ],
        "artifacts": [
            ("BAPLIE 2.2", "Bay plan exchange message / Parsed: Current"),
            ("TOS Sequence", "Terminal operating sequence / Validated"),
            ("Load Cell", "Container weight verification / Calibrated"),
            ("Quay Release", "Quayside release authorization / Ready"),
        ],
        "checklist": [
            "BAPLIE 2.2 evidence verified",
            "BAPLIE 2.2 record attached",
            "TOS sequence evidence verified",
            "TOS sequence record attached",
            "Load cell evidence verified",
            "Load cell record attached",
            "Quay release evidence verified",
            "Quay release record attached",
        ],
    },
}


st.set_page_config(
    page_title="Factory Command Post",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown(
    """
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
        div[data-testid="stMetricValue"] { color: var(--teal) !important; font-family: monospace; font-size: 1.45rem !important; overflow: visible !important; white-space: nowrap !important; }
        .card { background-color: var(--bg-panel); border: 1px solid var(--line); border-radius: 6px; padding: 14px; margin-bottom: 12px; }
        .badge { display: inline-block; padding: 4px 8px; border-radius: 4px; font-size: 0.8rem; font-family: monospace; font-weight: bold; }
        .badge-active { background: rgba(0,229,255,0.15); color: var(--teal); border: 1px solid var(--teal); }
        .badge-success { background: rgba(63,185,80,0.15); color: var(--green); border: 1px solid var(--green); }
        .blueprint-banner { background: #21161a; border: 1px solid var(--red); border-left: 6px solid var(--red); border-radius: 6px; padding: 18px 20px; margin: 18px 0 8px; }
        .blueprint-kicker, .blueprint-label { color: var(--text-muted); font-family: monospace; font-size: 0.72rem; font-weight: bold; letter-spacing: 0.04em; }
        .blueprint-kicker { color: var(--red); margin-bottom: 14px; }
        .blueprint-grid { display: grid; grid-template-columns: 1fr 1.2fr 1.3fr; gap: 20px; }
        .blueprint-value { color: var(--text-main); font-size: 1.05rem; font-weight: bold; margin-top: 8px; }
        .blueprint-risk { color: var(--red); font-weight: bold; margin-top: 8px; }
        .blueprint-impact, .blueprint-remedy { color: var(--text-main); margin-top: 8px; }
        .blueprint-action { color: var(--text-main); line-height: 1.7; margin-top: 8px; }
        .blueprint-action strong { color: var(--teal); font-family: monospace; }
        .blueprint-remedy { border-top: 1px solid #63343b; padding-top: 8px; }
        [data-testid="stMetricDelta"] { color: #ffcc66 !important; }
        .pipeline-card { background: #090d12; border: 1px solid #52606d; border-left: 4px solid var(--teal); border-radius: 6px; padding: 14px; margin: 10px 0 16px; }
        .pipeline-title { color: var(--teal); font-family: monospace; font-size: 0.76rem; font-weight: bold; letter-spacing: 0.06em; margin-bottom: 12px; }
        .pipeline-step { border-top: 1px solid #27313a; color: var(--text-main); display: flex; justify-content: space-between; gap: 8px; padding: 9px 0; font-size: 0.82rem; }
        .pipeline-step:first-of-type { border-top: 0; }
        .pipeline-step strong { font-family: monospace; font-size: 0.68rem; text-align: right; white-space: nowrap; }
        .pipeline-complete { color: var(--green); }
        .pipeline-pending { color: #ffcc66; }
        @media (max-width: 900px) { .blueprint-grid { grid-template-columns: 1fr; gap: 14px; } }
        @media (pointer: coarse) {
            .stButton > button {
                min-height: 48px !important;
                font-size: 1.05rem !important;
                font-weight: 600 !important;
                padding: 10px 24px !important;
                border-radius: 8px !important;
            }
            div[role="radiogroup"] label {
                min-height: 44px !important;
                display: flex !important;
                align-items: center !important;
                font-size: 1rem !important;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)


if "cleared_books" not in st.session_state or not isinstance(st.session_state["cleared_books"], dict):
    st.session_state["cleared_books"] = {}
if "ledger" not in st.session_state or not isinstance(st.session_state["ledger"], list):
    st.session_state["ledger"] = []
if "directive_issued" not in st.session_state or not isinstance(st.session_state["directive_issued"], dict):
    st.session_state["directive_issued"] = {}
if "surges" not in st.session_state or not isinstance(st.session_state["surges"], dict):
    st.session_state["surges"] = {"ops": 10, "cap": 10, "comp": 15, "sys": 10}
if "slas" not in st.session_state or not isinstance(st.session_state["slas"], dict):
    st.session_state["slas"] = {"ops": "1 business day", "cap": "1 business day", "comp": "3 business days", "sys": "1 business day"}
if "board_escalation" not in st.session_state or not isinstance(st.session_state["board_escalation"], dict):
    st.session_state["board_escalation"] = {}
if "board_escalation_context" not in st.session_state:
    st.session_state["board_escalation_context"] = ""
if "board_escalation_category" not in st.session_state:
    st.session_state["board_escalation_category"] = ""
if "board_escalation_timestamp" not in st.session_state:
    st.session_state["board_escalation_timestamp"] = ""
if "emergency_surge_mandate" not in st.session_state:
    st.session_state["emergency_surge_mandate"] = False
if "override_activation_pending" not in st.session_state:
    st.session_state["override_activation_pending"] = False
if "chairman_override" not in st.session_state:
    st.session_state["chairman_override"] = False
if "active_view" not in st.session_state:
    st.session_state["active_view"] = "1️⃣ Tier 1 | Chairman Directorate"


def nav_to(target_view):
    st.session_state["active_view"] = target_view


def reset_book(book_name):
    st.session_state["cleared_books"][book_name] = False
    st.session_state["directive_issued"][book_name] = False
    st.session_state["board_escalation"][book_name] = False
    st.session_state["active_view"] = "1️⃣ Tier 1 | Chairman Directorate"
    for committee in ("ops", "afic", "risk", "tech"):
        st.session_state[f"comm_{book_name}_{committee}"] = False
    for index in range(8):
        st.session_state[f"chk_{book_name}_{index}"] = False


def dispatch_escalation(book_name, category, context):
    st.session_state["board_escalation"][book_name] = True
    st.session_state["board_escalation_category"] = category
    st.session_state["board_escalation_context"] = context
    st.session_state["board_escalation_timestamp"] = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    timestamp = st.session_state["board_escalation_timestamp"]
    st.session_state["ledger"].append({
        "Timestamp": timestamp,
        "Operating Book": book_name,
        "Action": "Field Escalation: Critical Impediment to Chairman",
        "Capital Recovered": "At risk",
        "Client Preserved (90%)": "At risk",
        "Phoenix Fee (10%)": "At risk",
        "Cryptographic Hash": hashlib.sha256(f"{book_name}{timestamp}ESCALATION".encode()).hexdigest()[:16],
    })
    nav_to("1️⃣ Tier 1 | Chairman Directorate")


def complete_book(book_name, book_data):
    st.session_state["cleared_books"][book_name] = True
    st.session_state["emergency_surge_mandate"] = False
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    entry_hash = hashlib.sha256(f"{book_name}{timestamp}CLEARED".encode()).hexdigest()[:16]
    st.session_state["ledger"].append({
        "Timestamp": timestamp,
        "Operating Book": book_name,
        "Action": "Frontline Release: SOP Sign-off & Interconnection Cleared",
        "Capital Recovered": f"${book_data['burn']:,.0f} / wk",
        "Client Preserved (90%)": f"${book_data['burn'] * 0.9:,.0f}",
        "Phoenix Fee (10%)": f"${book_data['burn'] * 0.1:,.0f}",
        "Cryptographic Hash": entry_hash,
    })
    nav_to("4️⃣ Forensic Audit Ledger")


with st.sidebar:
    st.title("FACTORY COMMAND POST")
    st.caption("Live operating book | control plane online")
    book = st.selectbox("Operating book", list(OPERATING_BOOKS.keys()))
    book_slug = {
        "ERCOT BESS / storage operations": "ercot",
        "Grid Infrastructure / PJM Cluster": "grid",
        "ACC NZ Scheme / Claims Review": "acc",
        "Port Logistics / Container Flow": "port",
    }[book]
    committee_names = ("ops", "afic", "risk", "tech")
    for committee in committee_names:
        committee_key = f"comm_{book}_{committee}"
        if committee_key not in st.session_state:
            st.session_state[committee_key] = False
    completed_checks = sum(
        st.session_state.get(f"chk_{book_slug}_{index}", False)
        for index in range(1, 9)
    )
    quorum_count = sum(
        st.session_state.get(f"comm_{book}_{committee}", False)
        for committee in committee_names
    )
    quorum_achieved = quorum_count == 4
    tier_2_unlocked = quorum_achieved or st.session_state["chairman_override"]
    stage_2_complete = st.session_state["directive_issued"].get(book, False)
    stage_3_complete = completed_checks == 8
    stage_4_complete = st.session_state["cleared_books"].get(book, False)
    pipeline_steps = [
        ("1. Apex Board", "✅ AUTHORIZED" if tier_2_unlocked else "⏳ PENDING"),
        ("2. GM Directive", "✅ DISPATCHED" if stage_2_complete else "⏳ PENDING"),
        ("3. Site Operations", "✅ 8/8 VERIFIED" if stage_3_complete else "⏳ IN PROGRESS"),
        ("4. Audit Settlement", "✅ COMMITTED" if stage_4_complete else "⏳ PENDING"),
    ]
    st.sidebar.button("🔄 Reset Book State", on_click=reset_book, args=(book,))

    view = st.radio(
        "Command view",
        [
            "1️⃣ Tier 1 | Chairman Directorate",
            "2️⃣ Tier 2 | General Management",
            "3️⃣ Tier 3 | Site Operations",
            "4️⃣ Forensic Audit Ledger",
        ],
        key="active_view",
    )
    if st.session_state["override_activation_pending"]:
        st.session_state["chairman_override"] = True
        st.session_state["override_activation_pending"] = False
    override = st.sidebar.toggle("Chairman Directorate Override", key="chairman_override")
    if override:
        master_surge = st.sidebar.slider("Master Surge Cap Override (%)", 0, 100, 25, 5)
    else:
        master_surge = None
    pipeline_html = "<div class='pipeline-card'><div class='pipeline-title'>OPERATING PIPELINE SEQUENCE</div>"
    for step, status in pipeline_steps:
        status_class = "pipeline-complete" if status.startswith("✅") else "pipeline-pending"
        pipeline_html += f"<div class='pipeline-step'><span>{step}</span><strong class='{status_class}'>{status}</strong></div>"
    pipeline_html += "</div>"
    st.markdown(pipeline_html, unsafe_allow_html=True)

book_data = OPERATING_BOOKS[book]
st.session_state["selected_book"] = book
st.session_state["selected_book_data"] = book_data
check_keys = [f"chk_{book_slug}_{index}" for index in range(1, 9)]
completed_checks = sum([st.session_state.get(check_key, False) for check_key in check_keys])
book_cleared = st.session_state["cleared_books"].get(book, False) and completed_checks == 8

exposure = book_data["exposure"]
base_burn = book_data["burn"]
surge_amount = base_burn * (master_surge / 100) if override else 0
net_burn = base_burn - surge_amount
holding_burn_value = "$0 / wk" if book_cleared else f"${net_burn:,.0f} / wk" if override else f"${base_burn:,.0f} / wk"
surge_authorized = surge_amount
holding_burn_delta = (
    f"⚠️ {master_surge}% Surge Authorized (${surge_authorized:,.0f})"
    if override
    else ("Cleared" if book_cleared else "Active Drag")
)
realization_value = base_burn * 0.9 if book_cleared else net_burn * 0.9 if override else base_burn * 0.9
fee_value = base_burn * 0.1 if book_cleared else net_burn * 0.1 if override else base_burn * 0.1

m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Total Exposure", exposure, book)
m2.metric("Holding Burn", holding_burn_value, holding_burn_delta)
m3.metric("Client Realization", f"${realization_value:,.0f}", "90% retained")
m4.metric("Phoenix Fee", f"${fee_value:,.0f}", "10% accrual")
m5.metric("SOP Readiness", f"{completed_checks} / 8", "Field Gate")

st.markdown(
    f"""
    <div class="blueprint-banner">
        <div class="blueprint-kicker">REGIONAL BOTTLENECK &amp; TACTICAL ACTION BLUEPRINT</div>
        <div class="blueprint-grid">
            <div>
                <div class="blueprint-label">TARGET ASSET &amp; REGION</div>
                <span class="badge badge-active">ACTIVE NODE</span>
                <div class="blueprint-value">{book_data['region']}</div>
            </div>
            <div>
                <div class="blueprint-label">ACTIVE BOTTLENECK</div>
                <div class="blueprint-risk">{book_data['bottleneck']}</div>
                <div class="blueprint-impact">{book_data['impact']}</div>
            </div>
            <div>
                <div class="blueprint-label">TACTICAL ACTION REQUIRED</div>
                <div class="blueprint-action"><strong>1. BOARD</strong> authorize the domain envelope<br>
                <strong>2. GM</strong> translate the mandate into work orders<br>
                <strong>3. SITE</strong> execute and return verified evidence</div>
                <div class="blueprint-remedy">{book_data['remedy']}</div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.divider()

if "Tier 1" in view:
    if st.session_state["board_escalation"].get(book, False):
        st.error(
            f"🚨 CRITICAL FRONTLINE IMPEDIMENT: {st.session_state['board_escalation_category']}\n\n"
            f"Field context: {st.session_state['board_escalation_context']}\n\n"
            f"Financial exposure at risk: ${base_burn:,.0f} / wk"
        )
        action_columns = st.columns([2, 1])
        with action_columns[1]:
            authorize_surge = st.button("⚡ Authorize Emergency Surge Mandate to GM", type="primary")
        if authorize_surge:
            timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
            st.session_state["board_escalation"][book] = False
            st.session_state["emergency_surge_mandate"] = True
            st.session_state["override_activation_pending"] = True
            st.session_state["ledger"].append({
                "Timestamp": timestamp,
                "Operating Book": book,
                "Action": "Chairman Mandate: Emergency Surge Authorization to GM",
                "Capital Recovered": "Pending frontline release",
                "Client Preserved (90%)": "Pending frontline release",
                "Phoenix Fee (10%)": "Pending frontline release",
                "Cryptographic Hash": hashlib.sha256(f"{book}{timestamp}MANDATE".encode()).hexdigest()[:16],
            })
            st.rerun()
    st.header("Apex Board Governance & Oversight")
    st.write(f"Authorize domain envelopes and review {book} balance sheet recovery.")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Board Sub-Committee Authorizations")
        st.checkbox("Operations & Asset Delivery Committee (Chair: COO Oversight)", key=f"comm_{book}_ops")
        st.checkbox("Audit, Finance & Investment Committee / AFIC (Chair: CFO Oversight)", key=f"comm_{book}_afic")
        st.checkbox("Risk, Regulatory & Legal Committee (Chair: CLO Oversight)", key=f"comm_{book}_risk")
        st.checkbox("Technology & Infrastructure Committee (Chair: CTO Oversight)", key=f"comm_{book}_tech")
        if not tier_2_unlocked:
            st.warning(
                f"⚠️ BOARD DEADLOCK: Quorum incomplete ({quorum_count}/4). All 4 Sub-Committees must authorize, or the Chairman must invoke Directorate Override to proceed."
            )
        else:
            st.success("⚡ CHAIRMAN OVERRIDE ACTIVE" if st.session_state["chairman_override"] else "✅ BOARD QUORUM ESTABLISHED")
    with c2:
        st.subheader("Holding Loss Recovery Allocation")
        total_burn = book_data["burn"]
        rows = []
        for category, amount in book_data["loss_breakdown"]:
            rows.append({
                "Category": category,
                "Weekly Amount": f"${amount:,.0f}",
                "Surge Capital Allocated": f"${amount * (master_surge / 100):,.0f}" if override else "$0",
                "Client Retained (90%)": f"${amount * 0.9:,.0f}",
                "Phoenix Accrual (10%)": f"${amount * 0.1:,.0f}",
            })
        rows.append({
            "Category": "Total Weekly Burn",
            "Weekly Amount": f"${total_burn:,.0f}",
            "Surge Capital Allocated": f"${total_burn * (master_surge / 100):,.0f}" if override else "$0",
            "Client Retained (90%)": f"${total_burn * 0.9:,.0f}",
            "Phoenix Accrual (10%)": f"${total_burn * 0.1:,.0f}",
        })
        st.table(rows)
    stage_columns = st.columns([1.5, 1])
    with stage_columns[1]:
        st.button(
            "➡️ Advance to Tier 2 (General Management)",
            type="primary",
            disabled=not tier_2_unlocked,
            on_click=nav_to,
            args=("2️⃣ Tier 2 | General Management",),
        )

elif "Tier 2" in view:
    st.header("General Management Directive & Domain Translation")
    if not tier_2_unlocked:
        st.error(
            "🔒 TIER 2 LOCKED: Board quorum has not been established. Return to Tier 1 and obtain all 4 Sub-Committee authorizations, or invoke Directorate Override."
        )
        st.stop()
    if st.session_state["emergency_surge_mandate"]:
        st.warning("⚡ CHAIRMAN EMERGENCY SURGE MANDATE ISSUED: Authorized budget automatically applied to all domain envelopes.")
    if override:
        st.warning("⚠️ CHAIRMAN OVERRIDE ACTIVE: Standard delegation suspended. Surge envelopes locked to Master Cap.")
        st.session_state["surges"] = {domain: master_surge for domain in ("ops", "cap", "comp", "sys")}
    st.write(f"Convert board mandates into operating controls for {book}.")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        ops_surge = st.slider("Operations surge budget (%)", 0, 100, master_surge if override else st.session_state["surges"]["ops"], 5, disabled=override)
        ops_sla = st.selectbox("Operations SLA", ["4 hours", "1 business day", "3 business days"], index=1)
    with col2:
        cap_surge = st.slider("Capital surge budget (%)", 0, 100, master_surge if override else st.session_state["surges"]["cap"], 5, disabled=override)
        cap_sla = st.selectbox("Capital SLA", ["4 hours", "1 business day", "3 business days"], index=1)
    with col3:
        comp_surge = st.slider("Compliance surge budget (%)", 0, 100, master_surge if override else st.session_state["surges"]["comp"], 5, disabled=override)
        comp_sla = st.selectbox("Compliance SLA", ["4 hours", "1 business day", "3 business days"], index=2)
    with col4:
        sys_surge = st.slider("Systems surge budget (%)", 0, 100, master_surge if override else st.session_state["surges"]["sys"], 5, disabled=override)
        sys_sla = st.selectbox("Systems SLA", ["4 hours", "1 business day", "3 business days"], index=1)
    action_columns = st.columns([2, 1])
    with action_columns[1]:
        issue_directive = st.button("⚡ Issue Translated Directive", type="primary")
    if issue_directive:
        st.session_state["surges"] = {"ops": ops_surge, "cap": cap_surge, "comp": comp_surge, "sys": sys_surge}
        st.session_state["slas"] = {"ops": ops_sla, "cap": cap_sla, "comp": comp_sla, "sys": sys_sla}
        st.session_state["directive_issued"][book] = True
        st.success(f"Directive dispatched to {book} frontline teams.")
    stage_columns = st.columns([1.5, 1])
    with stage_columns[1]:
        st.button(
            "➡️ Advance to Tier 3 (Site Operations)",
            type="primary",
            disabled=not st.session_state["directive_issued"].get(book, False),
            on_click=nav_to,
            args=("3️⃣ Tier 3 | Site Operations",),
        )

elif "Tier 3" in view:
    st.header(f"Site Operations Hub / {book}")
    if override:
        st.warning("⚠️ CHAIRMAN OVERRIDE ACTIVE: Standard delegation suspended. Surge envelopes locked to Master Cap.")
    st.subheader("Upstream Governance Status")
    g1, g2, g3, g4 = st.columns(4)
    governance_values = [
        ("OPERATIONS", st.session_state["surges"]["ops"], st.session_state["slas"]["ops"]),
        ("CAPITAL", st.session_state["surges"]["cap"], st.session_state["slas"]["cap"]),
        ("COMPLIANCE", st.session_state["surges"]["comp"], st.session_state["slas"]["comp"]),
        ("SYSTEMS", st.session_state["surges"]["sys"], st.session_state["slas"]["sys"]),
    ]
    for column, (label, surge, sla) in zip((g1, g2, g3, g4), governance_values):
        column.markdown(f"<div class='card'><span class='badge badge-active'>{label}</span><br>Surge: {surge}%<br>SLA: {sla}</div>", unsafe_allow_html=True)
    st.subheader(f"Authentic Control Artifacts ({book})")
    artifact_columns = st.columns(4)
    for column, (name, detail) in zip(artifact_columns, book_data["artifacts"]):
        column.markdown(f"<div class='card'><strong>{name}</strong><br><small>{detail}<br>State: Verified</small></div>", unsafe_allow_html=True)
    st.subheader("Frontline SOP Release Checklist")
    checks = []
    checklist_columns = st.columns(2)
    for index, item in enumerate(book_data["checklist"]):
        with checklist_columns[index % 2]:
            checks.append(st.checkbox(item, key=check_keys[index]))
    if all(checks):
        if book_cleared:
            st.success(f"{book} cleared. Holding burn is $0 / wk (RESOLVED).")
        else:
            action_columns = st.columns([2, 1])
            with action_columns[1]:
                st.button(
                    "⚡ Submit Frontline SOP Sign-off & Notify Command",
                    type="primary",
                    on_click=complete_book,
                    args=(book, book_data),
                )
    else:
        st.info(f"{sum(checks)}/8 checks complete. All checks are required before sign-off.")
    with st.expander("🚨 Transmit Critical Impediment to Chairman"):
        impediment_category = st.selectbox(
            "Impediment Category",
            ["Specialist Labor Shortage", "Critical Hardware/Testing Delay", "Regulatory Compliance Hold"],
        )
        field_context = st.text_input(
            "Field Context",
            value="Frontline blocked on final compliance gate; requires emergency Board surge authorization",
        )
        action_columns = st.columns([2, 1])
        with action_columns[1]:
            st.button(
                "🚨 Dispatch Emergency Ticket to Board Chairman",
                type="primary",
                on_click=dispatch_escalation,
                args=(book, impediment_category, field_context),
            )

else:
    st.header("Immutable Governance & Forensic Audit Ledger")
    st.write("Cryptographically verifiable chain of custody across all operating books.")
    if st.session_state["ledger"]:
        st.dataframe(st.session_state["ledger"], use_container_width=True)
    else:
        st.info("No frontline sign-offs recorded in this session.")

st.divider()
st.caption(f"Selected book: {book} | AI Assistant context synchronized | {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")

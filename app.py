import datetime
import hashlib
import streamlit as st

st.set_page_config(
    page_title="Factory Command Post | Autonomous Capital Defense",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        .stApp { background-color: #0d1117; color: #c9d1d9; }
        div[data-testid="stMetric"] { background-color: #161b22; border: 1px solid #30363d; padding: 12px 16px; border-radius: 6px; }
        div[data-testid="stMetricLabel"] { color: #8b949e; font-size: .8rem; text-transform: uppercase; letter-spacing: .05em; }
        div[data-testid="stMetricValue"] { color: #f0f6fc; font-family: monospace; font-size: 1.6rem; }
        .stButton>button { border-radius: 4px; height: 44px; font-weight: 600; letter-spacing: .02em; }
    </style>
    """,
    unsafe_allow_html=True,
)

if "micro_drift_active" not in st.session_state:
    st.session_state.micro_drift_active = False
if "drift_minutes" not in st.session_state:
    st.session_state.drift_minutes = 0
if "selected_incident_id" not in st.session_state:
    st.session_state.selected_incident_id = "INC-001"


def work_order(order_id, title, crew, gate, progress, steps, metrics):
    return {
        "id": order_id,
        "title": title,
        "assigned_crew": crew,
        "target_gate": gate,
        "progress_pct": progress,
        "steps": [{"task": task, "done": done} for task, done in steps],
        "telemetry_metrics": metrics,
    }


SECTORS = {
    "ERCOT BESS / Grid Storage": {
        "asset_cap": 88_500_000,
        "directors": {
            "Dr. Arthur Pendleton": {
                "seat": "Chair, Grid Risk & Technical Integrity",
                "focus": "OEM Warranties, IEEE 2800 Compliance, Transformer Covenants",
                "assigned_gm": "Elena Rostova",
            },
            "David Chen (Proxy)": {
                "seat": "Chair, Regulatory & Market Compliance",
                "focus": "ERCOT Standard IA § 4.2, Interconnection Queue Defense",
                "assigned_gm": "David Chen",
            },
        },
        "incidents": {
            "INC-001": {
                "title": "ERCOT IA § 4.2 Part 2 COD Attestation Deadlock",
                "priority": "P1 - CRITICAL",
                "base_burn_rate_sec": 1.01,
                "start_time": datetime.datetime.now() - datetime.timedelta(days=1),
                "schedule_drift": "+9 Days COD Drift",
                "status": "DEADLOCKED",
                "director_seat": "Dr. Arthur Pendleton",
                "deadlock_summary": "Elena Rostova (protecting $1.2M transformer warranty) vs. David Chen (protecting $4.5M queue position).",
                "crossover_days": 13.8,
                "tier3_work_order": work_order(
                    "WO-8821-HARMONIC", "On-Site IEEE 2800 Harmonic & Impedance Sweep",
                    "Permian HV Crew 3 (Lead: Mark Henderson)", "Check #6 (Part 2 COD Attestation)", 75,
                    [("Rack 4 PE Calibration", True), ("Inverter Bank 1-4 Frequency Injection", True), ("Damping Resonance Verification", True), ("PE Digital Stamp & Packet Sign-off", False)],
                    {"THD Harmonics": ("4.1%", "Limit: 5.0% [NOMINAL]"), "Inrush Damping": ("1.18 pu", "Trip: 1.40 pu"), "Frequency Response": ("14.2 MW/0.1Hz", "Compliant"), "ICCP Latency": ("240 ms", "Max Allowed: 1000 ms")},
                ),
                "gms": {
                    "Elena Rostova": {"title": "GM - Field Operations & High-Voltage Crews", "domain": "Permian Substation, 138kV Step-Up Transformer", "position": "Withholding sign-off: Energizing without completed IEEE 2800 harmonic sweeps voids $1.2M OEM warranty under Clause 14.b.", "checks": [
                        {"id": "Check #1", "name": "ICCP 4-sec Telemetry", "status": "CLEARED", "evidence": "240ms Heartbeat"}, {"id": "Check #3", "name": "PSCAD EMT Model", "status": "CLEARED", "evidence": "Waveform Cleared"}, {"id": "Check #5", "name": "Relay Inrush Testing", "status": "CLEARED", "evidence": "1.18 pu Damping"}]},
                    "David Chen": {"title": "GM - Regulatory & Interconnection Accounts", "domain": "ERCOT Gateway & IA § 4.2 COD Filing", "position": "Demanding immediate filing: Part 2 window lapses in 48 hours. Forfeiture triggers $4.5M restudy penalty and 14-month slip.", "checks": [
                        {"id": "Check #2", "name": "ICCP Attestation Record", "status": "CLEARED", "evidence": "Record Locked"}, {"id": "Check #4", "name": "PSCAD Study Submittal", "status": "CLEARED", "evidence": "Submitted"}, {"id": "Check #6", "name": "Part 2 COD Attestation Gate", "status": "BLOCKED", "evidence": "Withheld by Field Ops (WO-8821 held)"}]},
                },
                "ai_dossiers": {"Dr. Arthur Pendleton": [("Financial Crossover Threshold", "Contractor idle burn ($610k/wk) exceeds the unhedged $1.2M transformer value in exactly 13.8 days.")]},
                "audit_log": [{"ts": "2026-09-11 08:00:12 UTC", "hash": "8f3a9e01c4", "event": "INCIDENT INITIALIZED: Elena Rostova withheld sign-off on Check #6."}, {"ts": "2026-09-11 09:15:40 UTC", "hash": "b2c174aa91", "event": "SURVEILLANCE AGENT: Contractor standby carry activated at $1.01/sec."}],
            },
            "INC-002": {
                "title": "Substation Step-Up Inrush Damping Curve Validation", "priority": "P2 - HIGH", "base_burn_rate_sec": 0.45,
                "start_time": datetime.datetime.now() - datetime.timedelta(days=2), "schedule_drift": "+3 Days Drift", "status": "MONITORING", "director_seat": "Dr. Arthur Pendleton",
                "deadlock_summary": "Field engineering awaiting OEM damping curve re-calibration before secondary breaker closure.", "crossover_days": 28.4,
                "tier3_work_order": work_order("WO-8824-INRUSH", "Pre-Insertion Resistor Cycle & Thermal Rise Check", "Substation Maintenance Crew B", "Breaker Actuation Confirmation", 50, [("Thermal Camera Baseline", True), ("Resistor Core Calibration", True), ("Live Inrush Capture", False)], {"Resistor Delta-T": ("38°C", "Max: 45°C"), "Contact Timing": ("12ms", "10-15ms")}),
                "gms": {"Elena Rostova": {"title": "GM - Field Operations", "domain": "Permian Substation Switchgear", "position": "Monitoring breaker actuation counts and damping resistor thermal rise.", "checks": [{"id": "Check #1", "name": "Resistor Core Delta-T", "status": "CLEARED", "evidence": "Within 45°C limit"}]}},
                "audit_log": [{"ts": "2026-09-10 12:00:00 UTC", "hash": "c4d5e6f7a8", "event": "Inrush damping cycle verification active."}],
            },
            "INC-003": {
                "title": "SCADA Protocol IEC 61850 Interoperability Gateway", "priority": "P3 - MODERATE", "base_burn_rate_sec": 0.18,
                "start_time": datetime.datetime.now() - datetime.timedelta(days=3), "schedule_drift": "+1 Day Drift", "status": "MONITORING", "director_seat": "David Chen (Proxy)",
                "deadlock_summary": "Telemetry gateway polling delay between primary RTU and ERCOT secondary node.", "crossover_days": 45.0,
                "tier3_work_order": work_order("WO-8830-SCADA", "IEC 61850 GOOSE Protocol Interop Buffer Re-sync", "Network & SCADA Integration Team", "ERCOT Gateway Handshake", 90, [("RTU Firmware Validation", True), ("GOOSE Buffer Clear", True), ("Handshake Packet Sign-off", False)], {"Modbus Polling": ("180ms", "< 250ms"), "Buffer Drop Rate": ("0.00%", "Target: 0.00%")}),
                "gms": {"David Chen": {"title": "GM - Regulatory & Interconnection", "domain": "SCADA Communications Node", "position": "Telemetry packet ingestion stabilized; awaiting final handshake acknowledgement.", "checks": [{"id": "Check #1", "name": "Modbus RTU Polling", "status": "CLEARED", "evidence": "Latency < 250ms"}]}},
                "audit_log": [{"ts": "2026-09-09 15:30:00 UTC", "hash": "a1b2c3d4e5", "event": "IEC 61850 handshake latency test passed."}],
            },
            "INC-004": {
                "title": "BESS Inverter Firmware Security Patch Rollout", "priority": "P4 - MONITORED", "base_burn_rate_sec": 0.05,
                "start_time": datetime.datetime.now() - datetime.timedelta(days=4), "schedule_drift": "On Schedule", "status": "NOMINAL", "director_seat": "Dr. Arthur Pendleton",
                "deadlock_summary": "Routine OTA patch staging across 48 inverter skids prior to full energization sequence.", "crossover_days": 90.0,
                "tier3_work_order": work_order("WO-8845-OTA", "Inverter Skid SHA-256 Firmware Flashing (48 Units)", "Field Systems Controls", "Firmware Security Gate", 75, [("Skids 1-24 Flashed", True), ("Skids 25-36 Flashed", True), ("Skids 37-48 Pending Overnight", False)], {"Units Updated": ("36 / 48", "75% Complete"), "Checksum Verification": ("100%", "No errors")}),
                "gms": {"Elena Rostova": {"title": "GM - Field Operations", "domain": "Power Conversion Systems", "position": "36 of 48 inverter skids updated. Final 12 skids scheduled for overnight cycle.", "checks": [{"id": "Check #1", "name": "Firmware Cryptographic Hash", "status": "CLEARED", "evidence": "Signed SHA-256 Valid"}]}},
                "audit_log": [{"ts": "2026-09-08 09:00:00 UTC", "hash": "99aabbccdd", "event": "OTA patch cycle stage 3 complete."}],
            },
        },
    }
}

if "app_state" not in st.session_state:
    st.session_state.app_state = SECTORS


def record_ledger_entry(incident, event_text):
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    previous_hash = incident["audit_log"][-1]["hash"] if incident["audit_log"] else "000000"
    entry_hash = hashlib.sha256(f"{timestamp}|{previous_hash}|{event_text}".encode()).hexdigest()[:10]
    incident["audit_log"].append({"ts": timestamp, "hash": entry_hash, "event": event_text})


with st.sidebar:
    st.markdown("### 🏛️ COMMAND POST")
    st.caption("Autonomous Capital Defense Control Plane")
    active_sector = st.selectbox("Operating Book (Top 12 Sectors):", list(st.session_state.app_state))
    sector = st.session_state.app_state[active_sector]
    selected_role = st.radio("Active Governance Profile:", ["Executive Chairman (Panoramic Tree)", "Tier 3: Site Operations / Field Lead"] + [f"Director: {d}" for d in sector["directors"]])
    st.divider()
    st.markdown("#### Active Blockage Queue")
    st.caption("Select branch to inspect and arbitrate:")
    for incident_id, incident in sector["incidents"].items():
        selected = incident_id == st.session_state.selected_incident_id
        if st.button(f"{incident['priority']}: {incident_id}\n{incident['title'][:28]}...", key=f"sidebar_{incident_id}", use_container_width=True, type="primary" if selected else "secondary"):
            st.session_state.selected_incident_id = incident_id
            st.rerun()
    st.divider()
    st.markdown("#### ⚡ Autonomous Tripwire Simulation")
    st.caption("Simulate real-world field drift:")
    if not st.session_state.micro_drift_active:
        if st.button("Simulate +45m Field Slip", use_container_width=True):
            st.session_state.micro_drift_active = True
            st.session_state.drift_minutes = 45
            incident = sector["incidents"]["INC-001"]
            incident["crossover_days"] = 12.1
            incident["schedule_drift"] = "+9 Days 45m COD Drift"
            record_ledger_entry(incident, "MICRO-DRIFT DETECTED: Step 3 frequency injection delayed +45m. System recalibrated Crossover to 12.1 days.")
            st.rerun()
    elif st.button("Reset Field Slip", use_container_width=True):
        st.session_state.micro_drift_active = False
        st.session_state.drift_minutes = 0
        incident = sector["incidents"]["INC-001"]
        incident["crossover_days"] = 13.8
        incident["schedule_drift"] = "+9 Days COD Drift"
        record_ledger_entry(incident, "DRIFT RECOVERY: Field operations re-aligned with nominal baseline.")
        st.rerun()

if st.session_state.selected_incident_id not in sector["incidents"]:
    st.session_state.selected_incident_id = next(iter(sector["incidents"]))
active_inc = sector["incidents"][st.session_state.selected_incident_id]
current_burn_rate = active_inc["base_burn_rate_sec"] if active_inc["status"] != "RESOLVED" else 0.0


def render_ledger(incident):
    for item in reversed(incident["audit_log"]):
        st.code(f"[{item['ts']}] SHA:{item['hash']} | {item['event']}", language="yaml")


def render_telemetry(incident):
    work_order_data = incident.get("tier3_work_order", {})
    for metric_name, (value, tolerance) in work_order_data.get("telemetry_metrics", {}).items():
        st.metric(metric_name, value, tolerance)


if selected_role == "Tier 3: Site Operations / Field Lead":
    st.title("Tier 3 | Site Operations & Field Execution Desk")
    st.caption(f"Ground Floor Task Execution | Assigned Asset: **{active_sector}** | Branch: **{st.session_state.selected_incident_id}**")
    work_order_data = active_inc.get("tier3_work_order", {})
    t1, t2, t3 = st.columns(3)
    t1.metric("Active Work Order", work_order_data.get("id", "N/A"), active_inc["priority"])
    t2.metric("Target Resolution Gate", work_order_data.get("target_gate", "N/A"))
    t3.metric("Execution Progress", f"{work_order_data.get('progress_pct', 0)}%")
    st.divider()
    st.subheader(f"Operational Punch List: {work_order_data.get('title', 'Site Tasks')}")
    st.caption(f"Assigned Field Unit: **{work_order_data.get('assigned_crew', 'Site Ops')}**")
    col_tasks, col_metrics = st.columns([3, 2])
    with col_tasks:
        with st.container(border=True):
            st.markdown("#### Step-by-Step Gating Checklist")
            for index, step in enumerate(work_order_data.get("steps", [])):
                st.write(f"{'✅' if step['done'] else '⏳'} **Step {index + 1}:** {step['task']}")
            st.divider()
            if active_inc["status"] == "DEADLOCKED" and st.button("⚡ Complete Step 4: Digital PE Stamp & Upload Test Packet", use_container_width=True, type="primary"):
                work_order_data["progress_pct"] = 100
                work_order_data["steps"][-1]["done"] = True
                for gm in active_inc["gms"].values():
                    for check in gm["checks"]:
                        if check["id"] == "Check #6":
                            check["status"] = "CLEARED"
                            check["evidence"] = "PE Stamp Verified (WO-8821)"
                active_inc["status"] = "RESOLVED"
                active_inc["base_burn_rate_sec"] = 0.0
                record_ledger_entry(active_inc, f"TIER 3 FIELD EXECUTION: {work_order_data.get('id')} completed by Field Crew. Check #6 cleared. Impasse resolved.")
                st.success("Field verification stamped and transmitted!")
                st.rerun()
    with col_metrics:
        with st.container(border=True):
            st.markdown("#### Live Telemetry Thresholds")
            render_telemetry(active_inc)
    with st.container(border=True):
        st.subheader("Field Audit Ledger Stamping")
        render_ledger(active_inc)

elif selected_role.startswith("Director:"):
    director_name = selected_role.replace("Director: ", "")
    director = sector["directors"][director_name]
    elapsed = (datetime.datetime.now() - active_inc["start_time"]).total_seconds()
    accrued = elapsed * current_burn_rate if active_inc["status"] != "RESOLVED" else 0
    st.title(director["seat"])
    st.caption(f"Mandate: **{director['focus']}** | Designated Director: **{director_name}**")
    m1, m2, m3 = st.columns(3)
    m1.metric("Jurisdiction Status", active_inc["status"], delta=active_inc["priority"])
    m2.metric("Domain Holding Burn", f"${current_burn_rate * 604800:,.0f} / wk", f"${current_burn_rate:.2f}/sec", delta_color="inverse")
    m3.metric("Accrued Delay Burn", f"${accrued:,.0f}", active_inc["schedule_drift"], delta_color="inverse")
    st.divider()
    with st.container(border=True):
        st.subheader("Tier 1B | Directorate Mandate & Concurrence")
        c1, c2 = st.columns([3, 1])
        c1.markdown(f"**Branch Under Review:** `{active_inc['title']}`\n\n**Impasse Summary:** {active_inc['deadlock_summary']}")
        with c2:
            if active_inc["status"] == "DEADLOCKED" and st.button("Issue Director Concurrence", use_container_width=True):
                record_ledger_entry(active_inc, f"COGNIZANT CONCURRENCE: {director_name} executed concurrence for branch {st.session_state.selected_incident_id}.")
                st.success("Concurrence Recorded.")
                st.rerun()
    with st.expander(f"🧠 Command Intelligence Briefing Officer | {director_name}", expanded=True):
        dossiers = active_inc.get("ai_dossiers", {}).get(director_name, [])
        if dossiers:
            for topic, text in dossiers:
                st.markdown(f"**Briefing: {topic}**")
                st.info(text)
        else:
            st.info(f"Nominal: No charter alerts for {director_name}.")
    gm_name = director["assigned_gm"]
    if gm_name in active_inc["gms"]:
        gm = active_inc["gms"][gm_name]
        with st.container(border=True):
            st.subheader(f"Tier 2 | Assigned GM: {gm_name}")
            st.caption(f"Domain: **{gm['domain']}** — Position: *{gm['position']}*")
            st.markdown("#### Tier 3 | Active Field Execution & Telemetry Engine")
            order = active_inc.get("tier3_work_order", {})
            st.info(f"**Work Order:** `{order.get('id', 'N/A')}` — {order.get('title', 'N/A')} | **Progress:** {order.get('progress_pct', 0)}%")
            for check in gm["checks"]:
                ca, cb, cc = st.columns([1, 3, 2])
                ca.write(f"**{check['id']}**")
                cb.write(check["name"])
                (cc.success if check["status"] == "CLEARED" else cc.error)(f"{'CLEARED' if check['status'] == 'CLEARED' else 'HELD'}: {check['evidence']}")
    with st.container(border=True):
        st.subheader("Tier 4 | Cryptographic Audit Log")
        render_ledger(active_inc)

else:
    st.title("Executive Chairman Command Post")
    st.caption(f"Master Autonomous Capital Defense Post | Operating Asset: **{active_sector}** | Fleet Capital Cap: **${sector['asset_cap']:,.0f}**")
    active_incidents = [incident for incident in sector["incidents"].values() if incident["status"] != "RESOLVED"]
    total_burn = sum(incident["base_burn_rate_sec"] for incident in active_incidents)
    k1, k2, k3 = st.columns(3)
    k1.metric("Fleet Holding Burn", f"${total_burn * 604800:,.0f} / wk", f"${total_burn:.2f}/sec", delta_color="inverse")
    k2.metric("Capital Under Direct Lock", f"${sector['asset_cap']:,.0f}", "Asset Defense Escrow Intact")
    k3.metric("Active Operational Block", st.session_state.selected_incident_id, f"Crossover: {active_inc['crossover_days']} Days", delta_color="inverse")

    if st.session_state.micro_drift_active:
        st.error(f"🚨 **AUTONOMOUS TRIPWIRE ALERT | MICRO-DRIFT DETECTED (+{st.session_state.drift_minutes}m)**\n\n**Root Cause:** Harmonic test injection on Permian Relay Rack 4 exceeded time budget by 45 minutes.\n\n**System Recalibration:** Crossover threshold recalibrated from **13.8 days ➔ 12.1 days**.\n\n**Master Recommendation:** Execute **Option A (Directorate Carve-Out)** immediately.")
    elif active_inc["status"] == "DEADLOCKED":
        st.warning(f"⚠️ **MASTER AGENT INTERRUPT:** Active standstill on **{st.session_state.selected_incident_id} ({active_inc['title']})**.\n\nContractor idle carry is bleeding **${current_burn_rate:.2f}/second**. Unhedged holding costs cross the $1.2M transformer value in **{active_inc['crossover_days']} days**.")

    st.markdown("#### Autonomous Agent Fleet Status")
    ag1, ag2, ag3, ag4 = st.columns(4)
    with ag1: st.success("🤖 **Master Orchestrator**\n\n`ACTIVE | Cross-Branch Synthesis`")
    with ag2: st.info("📡 **Site Telemetry Agent**\n\n`POLLING | Substation Modbus #40102`")
    with ag3: st.warning("⚖️ **Market Surveillance**\n\n`ALERT | ERCOT 48h Gate Engaged`")
    with ag4: st.success("🛡️ **Fiduciary Shield Agent**\n\n`ENFORCED | Delaware BJR Active`")

    with st.container(border=True):
        st.markdown("### 🌐 Directorate Collaboration & Evidence Suite")
        links = [("https://meet.google.com/lookup/aat-" + st.session_state.selected_incident_id.lower() + "-arbitration", "📹 Instant Meet Bridge", "#1a73e8", f"Room: `aat-{st.session_state.selected_incident_id.lower()}`"), ("https://notebooklm.google.com", "📓 NotebookLM Dossier", "#161b22", "ERCOT IA § 4.2 & Warranty Docs"), ("https://drive.google.com", "📁 Telemetry Drive Vault", "#161b22", "Raw PSCAD & SCADA Evidence"), ("https://docs.google.com", "📄 Board Resolution Doc", "#161b22", "Auto-Drafted Waiver Template")]
        columns = st.columns(4)
        for column, (url, label, color, caption) in zip(columns, links):
            with column:
                st.markdown(f'<a href="{url}" target="_blank"><button style="width:100%; height:44px; background-color:{color}; color:white; border:none; border-radius:4px; font-weight:600; cursor:pointer;">{label}</button></a>', unsafe_allow_html=True)
                st.caption(caption)

    with st.container(border=True):
        st.markdown("### 🎙️ Instant Diagnostic Agent Conference")
        st.caption("Interrogate the Master Agent and Domain Agents to diagnose why a priority fix has stalled.")
        conf_q1, conf_q2, conf_q3 = st.columns([2, 1, 1])
        prompt = conf_q1.text_input("Conference Query:", placeholder="e.g., Why is Work Order #8821 stalled? / What unblocks Elena?", label_visibility="collapsed")
        why_stalled = conf_q2.button("Why is the Fix Stalled?", use_container_width=True)
        unblock = conf_q3.button("What Unblocks the GM?", use_container_width=True)
        if why_stalled: prompt = "Why is Work Order #8821 stalled?"
        elif unblock: prompt = "What unblocks Elena?"
        if prompt:
            st.markdown(f'**Chairman:** *"{prompt}"*')
            query = prompt.lower()
            if "why" in query or "wo-8821" in query or "stalled" in query or "held" in query:
                st.markdown('**Master Orchestrator ➔ Site Telemetry Agent:** *"Emergency PE crew is physically staged at the Permian relay building. Physical testing is ready; access is legally blocked."*\n\n**Master Orchestrator ➔ Chairman:** *"The fix has not failed mechanically. It is blocked by an access gate. Executing the Directorate Carve-Out releases the OEM engineer immediately."*')
            elif "unblock" in query or "elena" in query or "david" in query:
                st.markdown('**Master Orchestrator ➔ Fiduciary Shield Agent:** *"An executive Board Resolution granting a complete Directorate Indemnity Waiver absorbs liability at the board level. Elena is legally cleared to sign within 5 minutes of execution."*')
            else:
                st.markdown(f'**Master Orchestrator:** *"Evaluating {prompt!r} across telemetry, market queue, and legal indemnities. The dominant path remains Option A."*')

    st.markdown("### The Three Cascading Branches")
    st.caption("Cascading operational tree decomposing the macro threat into physical, market, and fiduciary pillars:")
    b_col1, b_col2, b_col3 = st.columns(3)
    with b_col1:
        with st.container(border=True):
            st.markdown("#### Branch 1: Physical / Field")
            st.caption("Hardware Gate | Substation & Crews")
            field_gm = active_inc["gms"].get("Elena Rostova")
            st.markdown(f"**Lead:** Elena Rostova ({field_gm['title'] if field_gm else 'Field Operations'})")
            st.markdown(f"**Cognizant Director:** {active_inc['director_seat']}")
            st.markdown("**Embedded Agent:** `Site Telemetry Agent` (Active)")
            st.error("🚨 **Friction Point:** Check #6 unverified; harmonic sweep access held.")
            st.info("**Branch Recommendation:** Direct emergency PE stamp upload on the active work order upon legal clearance.")
            order = active_inc.get("tier3_work_order", {})
            st.write(f"**Work Order:** `{order.get('id', 'N/A')}` ({order.get('progress_pct', 0)}%)")
            st.write(f"**THD Harmonics:** {order.get('telemetry_metrics', {}).get('THD Harmonics', ('N/A', ''))[0]}")
    with b_col2:
        with st.container(border=True):
            st.markdown("#### Branch 2: Regulatory / Market")
            st.caption("Commercial Gate | Interconnection Queue")
            market_gm = active_inc["gms"].get("David Chen")
            st.markdown(f"**Lead:** David Chen ({market_gm['title'] if market_gm else 'Regulatory Accounts'})")
            st.markdown("**Cognizant Director:** David Chen (Proxy)")
            st.markdown("**Embedded Agent:** `Market Surveillance Agent` (Active)")
            st.warning("⏳ **Friction Point:** ERCOT Part 2 COD gate expiring in 48 hours ($4.5M queue risk).")
            st.info("**Branch Recommendation:** Stage Part 2 filing packet; execute instant submittal upon Branch 1 clearance.")
            st.write(f"**ICCP Latency:** {active_inc['gms'].get('Elena Rostova', {}).get('checks', [{}])[0].get('evidence', 'N/A')}")
            st.write("**ERCOT Gateway Status:** Handshake Validated")
    with b_col3:
        with st.container(border=True):
            st.markdown("#### Branch 3: Fiduciary / Capital")
            st.caption("Balance Sheet Gate | Liability & Escrow")
            st.markdown("**Lead:** Executive Board Chairman")
            st.markdown("**Cognizant Director:** Chair of Governance / Legal")
            st.markdown("**Embedded Agent:** `Fiduciary Shield Agent` (Active)")
            st.error(f"⚠️ **Friction Point:** $1.2M unhedged transformer risk crossing in {active_inc['crossover_days']} days.")
            st.success("**Branch Recommendation:** Execute Directorate Indemnity Carve-Out to break the GM stalemate.")
            st.write(f"**Holding Burn Velocity:** ${current_burn_rate:.2f}/sec")
            st.write("**BJR Standard:** Fully Compliant")

    with st.container(border=True):
        st.markdown("### Tier 3 | Ground Floor Execution & Telemetry Engine")
        st.caption("Mirrors Chairman priorities into physical punch lists, telemetry tolerances, and crew progress.")
        order = active_inc.get("tier3_work_order", {})
        wo_c1, wo_c2 = st.columns([3, 2])
        with wo_c1:
            st.markdown(f"**Active Work Order:** `{order.get('id', 'N/A')}` — *{order.get('title', 'N/A')}*")
            st.caption(f"Assigned Unit: **{order.get('assigned_crew', 'Site Ops')}** | Gate: **{order.get('target_gate', 'N/A')}**")
            st.progress(order.get("progress_pct", 0) / 100, text=f"Physical Completion: {order.get('progress_pct', 0)}%")
            for step in order.get("steps", []): st.write(f"{'✅' if step['done'] else '⏳'} {step['task']}")
        with wo_c2:
            st.markdown("**Live Engineering Telemetry & Tolerances:**")
            render_telemetry(active_inc)

    st.markdown("### Tier 4 | Executive Remedial Engine & Cryptographic Audit Ledger")
    t4_col1, t4_col2 = st.columns([1, 1])
    with t4_col1:
        with st.container(border=True):
            st.markdown("#### Authorized Remedial Levers")
            choice = st.radio("Select Remedial Action:", ["Option A: Authorize Directorate Indemnity Carve-Out (Dominant)", "Option B: Mobilize Emergency PE Testing Crew ($35k Draw)", "Option C: Demobilize Permian High-Voltage Contractors"])
            if "Option A" in choice:
                st.markdown("* **Holding Burn:** `$610,848/wk` ➔ **`$0/wk`** (Halted instantly).\n* **Elena Rostova:** Exonerated. Board Escrow absorbs $1.2M warranty risk.\n* **David Chen:** Filing transmitted to ERCOT. Queue protected.\n* **Fiduciary Shield:** Delaware Business Judgment Rule satisfied.")
                if active_inc["status"] == "DEADLOCKED" and st.button("Execute Directorate Carve-Out", use_container_width=True):
                    active_inc["status"] = "RESOLVED"
                    active_inc["base_burn_rate_sec"] = 0.0
                    order["progress_pct"] = 100
                    for step in order.get("steps", []): step["done"] = True
                    for gm in active_inc["gms"].values():
                        for check in gm["checks"]: check["status"], check["evidence"] = "CLEARED", "Directorate Override"
                    record_ledger_entry(active_inc, f"CHAIRMAN DIRECTIVE: Option A executed on {st.session_state.selected_incident_id}. Elena Rostova indemnified. WO-8821 verified. Burn halted to $0/sec.")
                    st.success("Directive Enforced. Holding burn halted.")
                    st.rerun()
            elif "Option B" in choice:
                st.markdown("* **Holding Burn:** Bleed continues + $35,000 emergency draw.\n* **Operational Drift:** Consumes 6 hours on the 48-hour ERCOT clock.")
                if active_inc["status"] == "DEADLOCKED" and st.button("Authorize Capital Draw", use_container_width=True):
                    record_ledger_entry(active_inc, f"CHAIRMAN CAPITAL DRAW: $35,000 authorized on {st.session_state.selected_incident_id} for emergency testing.")
                    st.success("Capital Released. Stamped to Ledger.")
                    st.rerun()
            else:
                st.error("Action Inadmissible: Fiduciary Shield Agent has locked Option C due to queue forfeiture.")
    with t4_col2:
        with st.container(border=True):
            st.markdown("#### Cryptographic Audit Log")
            render_ledger(active_inc)

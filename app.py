import datetime
import hashlib
import json
import streamlit as st

st.set_page_config(page_title="Executive Command Post | Capital Defense", page_icon="⚡", layout="wide", initial_sidebar_state="expanded")
st.markdown("""
<style>
.stApp { background-color: #0d1117; color: #c9d1d9; }
div[data-testid="stMetric"] { background-color: #161b22; border: 1px solid #30363d; padding: 14px 18px; border-radius: 6px; }
div[data-testid="stMetricLabel"] { color: #8b949e; font-size: .85rem; text-transform: uppercase; letter-spacing: .05em; }
div[data-testid="stMetricValue"] { color: #f0f6fc; font-family: monospace; }
.stButton>button { border-radius: 4px; height: 46px; font-weight: 600; letter-spacing: .02em; }
</style>
""", unsafe_allow_html=True)

SECTORS = {
    "ERCOT BESS / Grid Storage": {
        "asset_cap": 88_500_000,
        "directors": {
            "Dr. Arthur Pendleton": {"seat": "Chair, Grid Risk & Technical Integrity", "focus": "OEM Warranties, IEEE 2800 Compliance, Transformer Covenants", "assigned_gm": "Elena Rostova"},
            "David Chen (Proxy)": {"seat": "Chair, Regulatory & Market Compliance", "focus": "ERCOT Standard IA § 4.2, Interconnection Queue Defense", "assigned_gm": "David Chen"}},
        "incidents": {"INC-001": {
            "title": "ERCOT IA § 4.2 Part 2 COD Attestation Deadlock", "priority": "P1 - CRITICAL", "burn_rate_sec": 1.01,
            "start_time": datetime.datetime.now() - datetime.timedelta(days=1), "schedule_drift": "+9 Days COD Drift", "status": "DEADLOCKED", "director_seat": "Dr. Arthur Pendleton",
            "deadlock_summary": "Elena Rostova (protecting $1.2M transformer warranty) vs. David Chen (protecting $4.5M queue position).",
            "gms": {
                "Elena Rostova": {"title": "GM - Field Operations & High-Voltage Crews", "domain": "Permian Substation, 138kV Step-Up Transformer", "position": "Withholding sign-off: Energizing without completed IEEE 2800 harmonic sweeps voids $1.2M OEM warranty under Clause 14.b.", "checks": [
                    {"id": "Check #1", "name": "ICCP 4-sec Telemetry", "status": "CLEARED", "evidence": "Register Verified"}, {"id": "Check #3", "name": "PSCAD EMT Model", "status": "CLEARED", "evidence": "Waveform Verified"}, {"id": "Check #5", "name": "Relay Inrush Testing", "status": "CLEARED", "evidence": "Damping Verified"}]},
                "David Chen": {"title": "GM - Regulatory & Interconnection Accounts", "domain": "ERCOT Gateway & IA § 4.2 COD Filing", "position": "Demanding immediate filing: Part 2 window lapses in 48 hours. Forfeiture triggers $4.5M restudy penalty and 14-month slip.", "checks": [
                    {"id": "Check #2", "name": "ICCP Attestation Record", "status": "CLEARED", "evidence": "Record Locked"}, {"id": "Check #4", "name": "PSCAD Study Submittal", "status": "CLEARED", "evidence": "Submitted"}, {"id": "Check #6", "name": "Part 2 COD Attestation Gate", "status": "BLOCKED", "evidence": "Withheld by Field Ops (Elena)"}]}},
            "ai_dossiers": {"Dr. Arthur Pendleton": [("Financial Crossover Threshold", "Contractor idle burn ($610k/wk) exceeds the unhedged $1.2M transformer value in exactly 13.8 days. Board indemnity carve-out stops burn immediately."), ("Warranty Clause 14.b Exclusion", "OEM requires verified harmonic data. Board Directorate Carve-Out indemnifies Elena Rostova personally, shifting liability to corporate defense escrow.")]},
            "audit_log": [{"ts": "2026-09-11 08:00:12 UTC", "hash": "8f3a9e01c4", "event": "INCIDENT INITIALIZED: Elena Rostova withheld sign-off on Check #6."}, {"ts": "2026-09-11 09:15:40 UTC", "hash": "b2c174aa91", "event": "SURVEILLANCE AGENT: Contractor standby carry activated at $1.01/sec."}]},
        "INC-002": {
            "title": "Substation Main Step-Up Inrush Damping Validation", "priority": "P2 - HIGH", "burn_rate_sec": 0.45,
            "start_time": datetime.datetime.now() - datetime.timedelta(days=2), "schedule_drift": "+3 Days Drift", "status": "MONITORING", "director_seat": "Dr. Arthur Pendleton",
            "deadlock_summary": "Field engineering awaiting OEM damping curve re-calibration before secondary breaker closure.",
            "gms": {"Elena Rostova": {"title": "GM - Field Operations", "domain": "Permian Substation Switchgear", "position": "Monitoring breaker actuation counts and damping resistor thermal rise.", "checks": [{"id": "Check #1", "name": "Resistor Core Delta-T", "status": "CLEARED", "evidence": "Within 45°C limit"}, {"id": "Check #2", "name": "Pre-Insertion Resistor Cycle", "status": "CLEARED", "evidence": "Timing Verified"}]}},
            "audit_log": [{"ts": "2026-09-10 12:00:00 UTC", "hash": "c4d5e6f7a8", "event": "Inrush damping cycle verification active."}],
        },
        "INC-003": {
            "title": "SCADA Protocol IEC 61850 Interoperability Gateway", "priority": "P3 - MODERATE", "burn_rate_sec": 0.18,
            "start_time": datetime.datetime.now() - datetime.timedelta(days=3), "schedule_drift": "+1 Day Drift", "status": "MONITORING", "director_seat": "David Chen (Proxy)",
            "deadlock_summary": "Telemetry gateway polling delay between primary RTU and ERCOT secondary collector node.",
            "gms": {"David Chen": {"title": "GM - Regulatory & Interconnection", "domain": "SCADA Communications Node", "position": "Telemetry packet ingestion stabilized; awaiting final handshake acknowledgement.", "checks": [{"id": "Check #1", "name": "Modbus RTU Polling", "status": "CLEARED", "evidence": "Latency < 250ms"}, {"id": "Check #2", "name": "GOOSE Message Publisher", "status": "CLEARED", "evidence": "Buffers Nominal"}]}},
            "audit_log": [{"ts": "2026-09-09 15:30:00 UTC", "hash": "a1b2c3d4e5", "event": "IEC 61850 handshake latency test passed."}],
        },
        "INC-004": {
            "title": "BESS Inverter Firmware Security Patch Rollout", "priority": "P4 - MONITORED", "burn_rate_sec": 0.05,
            "start_time": datetime.datetime.now() - datetime.timedelta(days=4), "schedule_drift": "On Schedule", "status": "NOMINAL", "director_seat": "Dr. Arthur Pendleton",
            "deadlock_summary": "Routine OTA patch staging across 48 inverter skids prior to full energization sequence.",
            "gms": {"Elena Rostova": {"title": "GM - Field Operations", "domain": "Power Conversion Systems", "position": "36 of 48 inverter skids successfully updated. Final 12 skids scheduled for overnight cycle.", "checks": [{"id": "Check #1", "name": "Firmware Cryptographic Hash", "status": "CLEARED", "evidence": "Signed SHA-256 Valid"}]}},
            "audit_log": [{"ts": "2026-09-08 09:00:00 UTC", "hash": "99aabbccdd", "event": "OTA patch cycle stage 3 complete."}],
        }}
    },
    "Hyperscale AI Data Center (96 MW)": {
        "asset_cap": 240_000_000, "directors": {"Sarah Jenkins": {"seat": "Chair, Technology Risk & Infrastructure Integrity", "focus": "Liquid Cooling Loops, CDU Manifolds, GPU Cluster Handover", "assigned_gm": "Tariq Vance"}},
        "incidents": {"P1-HDC-01": {"title": "Tenant Handover SLA vs. 72-Hr Hydrostatic Manifold Hold", "priority": "P1 - CRITICAL", "burn_rate_sec": .86, "start_time": datetime.datetime.now() - datetime.timedelta(hours=20), "schedule_drift": "+4 Days Handover Slip", "status": "DEADLOCKED", "director_seat": "Sarah Jenkins", "deadlock_summary": "Tariq Vance (protecting $140M GPU floor from leaks) vs. Rachel Adams (facing anchor tenant SLA cancellation).", "gms": {"Tariq Vance": {"title": "GM - MEP Delivery", "domain": "Chiller Plant & Manifolds", "position": "18 hours remaining on hydrostatic pressure hold. Powering early risks fluid release onto racks.", "checks": [{"id": "Check #1", "name": "Loop Delta-T", "status": "CLEARED", "evidence": "4.2°C Nominal"}, {"id": "Check #4", "name": "72-Hr Hydrostatic Hold", "status": "BLOCKED", "evidence": "18h Hold Left"}]}}, "ai_dossiers": {"Sarah Jenkins": [("Phased Handover Feasibility", "Ultrasonic weld logs confirm Halls 2-4 are nominal. Issue carve-out for Halls 2-4 and isolate Hall 1.")]}, "audit_log": [{"ts": "2026-09-11 14:00:00 UTC", "hash": "4a9d71...e289", "event": "MEP hold invoked on cooling manifold loop B."}]}}
    },
    "Cold-Chain Food Distribution": {
        "asset_cap": 45_000_000, "directors": {"Dr. Maya Lin": {"seat": "Chair, Food Safety & Statutory Compliance", "focus": "FSMA § 117, HACCP Critical Limits, Pathogen Lab Traceability", "assigned_gm": "QA Lead"}},
        "incidents": {"P1-FOOD-01": {"title": "FSMA CCP2 Thermal Excursion ($3.2M Protein)", "priority": "P1 - CRITICAL", "burn_rate_sec": 10.55, "start_time": datetime.datetime.now() - datetime.timedelta(hours=5), "schedule_drift": "+6 Hours Retail Drift", "status": "DEADLOCKED", "director_seat": "Dr. Maya Lin", "deadlock_summary": "QA Lead (holding for PCR lab swab) vs. Logistics (facing $180k retail OTIF penalty).", "gms": {"QA Lead": {"title": "VP - Quality Assurance", "domain": "Cross-Dock Reefers", "position": "45-minute temperature spike during transfer. Releasing without negative PCR creates statutory liability.", "checks": [{"id": "Check #3", "name": "Core Meat Probe", "status": "CLEARED", "evidence": "Peak 3.8°C (<4°C threshold)"}, {"id": "Check #4", "name": "Rapid PCR Swab", "status": "BLOCKED", "evidence": "90m Incubation Left"}]}}, "ai_dossiers": {"Dr. Maya Lin": [("Biological Pathogen Proliferation", "Core probe telemetry proves internal meat temperature never reached 4.0°C. Bacterial replication risk is zero.")]}, "audit_log": [{"ts": "2026-09-11 16:30:10 UTC", "hash": "1b88e2...3f90", "event": "Cross-dock bay #4 thermal excursion logged."}]}}
    }
}

if "app_state" not in st.session_state:
    st.session_state.app_state = SECTORS

if "selected_incident_id" not in st.session_state:
    st.session_state.selected_incident_id = "INC-001"

def record_ledger_entry(incident: dict, event_text: str):
    ts = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    prev_hash = incident["audit_log"][-1]["hash"] if incident["audit_log"] else "000000"
    entry_hash = hashlib.sha256(f"{ts}|{prev_hash}|{event_text}".encode()).hexdigest()[:12]
    incident["audit_log"].append({"ts": ts, "hash": entry_hash, "event": event_text})

with st.sidebar:
    st.markdown("### 🏛️ COMMAND POST")
    st.caption("Autonomous Capital Defense Control Plane")
    active_sector = st.selectbox("Operating Book (Top 12 Sectors):", ["ERCOT BESS / Grid Storage"])
    sector = st.session_state.app_state[active_sector]
    selected_role = st.radio("Active Governance Profile:", ["Executive Chairman (Panoramic Tree)"] + [f"Director: {d}" for d in sector["directors"]])
    st.divider()

    st.markdown("#### Active Blockage Queue")
    st.caption("Select branch to inspect and arbitrate:")
    for inc_key, inc_obj in sector["incidents"].items():
        is_selected = inc_key == st.session_state.selected_incident_id
        btn_label = f"{inc_obj['priority']}: {inc_key}\n{inc_obj['title'][:32]}..."
        if st.button(btn_label, key=f"sidebar_{inc_key}", use_container_width=True, type="primary" if is_selected else "secondary"):
            st.session_state.selected_incident_id = inc_key
            st.rerun()

if st.session_state.selected_incident_id not in sector["incidents"]:
    st.session_state.selected_incident_id = list(sector["incidents"])[0]

active_inc = sector["incidents"][st.session_state.selected_incident_id]

if selected_role.startswith("Director:"):
    director_name = selected_role.replace("Director: ", "")
    d_meta = sector["directors"][director_name]
    inc = active_inc
    if inc["director_seat"] != director_name:
        st.title(f"Director Desk | {director_name}")
        st.info(f"Selected branch `{st.session_state.selected_incident_id}` is assigned to {inc['director_seat']}.")
    else:
        elapsed = (datetime.datetime.now() - inc["start_time"]).total_seconds()
        accrued = elapsed * inc["burn_rate_sec"] if inc["status"] != "RESOLVED" else 0
        st.title(d_meta["seat"])
        st.caption(f"Mandate: **{d_meta['focus']}** | Designated Director: **{director_name}**")
        m1, m2, m3 = st.columns(3)
        m1.metric("Jurisdiction Status", inc["status"], delta=inc["priority"])
        m2.metric("Domain Holding Burn", f"${inc['burn_rate_sec']*604800:,.0f} / wk", f"${inc['burn_rate_sec']:.2f}/sec", delta_color="inverse")
        m3.metric("Accrued Delay Burn", f"${accrued:,.0f}", inc["schedule_drift"], delta_color="inverse")
        st.divider()
        with st.container(border=True):
            st.subheader("Tier 1B | Directorate Mandate & Formal Concurrence")
            c1, c2 = st.columns([3, 1])
            c1.markdown(f"**Active Blockage:** `{inc['title']}`\n\n**Jurisdictional Stalemate:** {inc['deadlock_summary']}")
            with c2:
                if inc["status"] == "DEADLOCKED" and st.button("Issue Director Concurrence", use_container_width=True):
                    record_ledger_entry(inc, f"COGNIZANT CONCURRENCE: {director_name} executed technical concurrence for Chairman carve-out.")
                    st.success("Concurrence Recorded & Locked.")
                    st.rerun()
        with st.expander(f"🧠 Command Intelligence Briefing Officer | {director_name}", expanded=True):
            st.caption(f"Context Filtered to Charter: {d_meta['focus']}")
            for topic, text in inc.get("ai_dossiers", {}).get(director_name, []):
                st.markdown(f"**Briefing: {topic}**")
                st.info(text)
        gm_name = d_meta["assigned_gm"]
        if gm_name in inc["gms"]:
            gm = inc["gms"][gm_name]
            with st.container(border=True):
                st.subheader(f"Tier 2 | Assigned General Manager: {gm_name}")
                st.caption(f"Operational Domain: **{gm['domain']}** — *{gm['title']}*")
                st.warning(f"**Defensive Position:** {gm['position']}")
                st.markdown("#### Tier 3 | Sensor Ground Truth")
                for chk in gm["checks"]:
                    ca, cb, cc = st.columns([1, 3, 2])
                    ca.write(f"**{chk['id']}**")
                    cb.write(chk["name"])
                    if chk["status"] == "CLEARED": cc.success(f"CLEARED: {chk['evidence']}")
                    else: cc.error(f"HELD: {chk['evidence']}")
        with st.container(border=True):
            st.subheader("Tier 4 | Cryptographic Audit Log (Jurisdiction Chain)")
            for item in reversed(inc["audit_log"]): st.code(f"[{item['ts']}] HASH:{item['hash']} — {item['event']}", language="yaml")
else:
    st.title("Executive Chairman Command Post")
    st.caption(f"Master Autonomous Control Plane | Sector: **{active_sector}** | Fleet Capital Cap: **${sector['asset_cap']:,.0f}**")
    active_incidents = [i for i in sector["incidents"].values() if i["status"] != "RESOLVED"]
    tot_burn_sec = sum(i["burn_rate_sec"] for i in active_incidents)
    k1, k2, k3 = st.columns(3)
    k1.metric("Fleet Holding Burn", f"${tot_burn_sec*604800:,.0f} / wk", f"${tot_burn_sec:.2f}/sec", delta_color="inverse")
    k2.metric("Capital Under Direct Lock", f"${sector['asset_cap']:,.0f}", "Fiduciary Cap Intact")
    k3.metric("Selected Branch", st.session_state.selected_incident_id, active_inc["priority"], delta_color="inverse")
    if active_inc["status"] == "DEADLOCKED": st.error(f"""🚨 **MASTER ORCHESTRATOR INTERRUPT:** Critical standoff on **{st.session_state.selected_incident_id} ({active_inc['title']})**.
Contractor idle carry is bleeding **${active_inc['burn_rate_sec']:.2f}/second**. Holding costs will exceed total asset warranty value in **13.8 days**. Fiduciary review requires immediate arbitration.""")
    with st.container(border=True):
        st.markdown("### 🌐 Directorate Collaboration & Evidence Suite")
        g1, g2, g3, g4 = st.columns(4)
        links = [(g1, "https://meet.google.com/lookup/aat-" + st.session_state.selected_incident_id.lower() + "-arbitration", "📹 Instant Meet Bridge", "#1a73e8", f"Room: `aat-{st.session_state.selected_incident_id.lower()}`"), (g2, "https://notebooklm.google.com", "📓 NotebookLM Dossier", "#161b22", "ERCOT IA § 4.2 & Warranty Docs"), (g3, "https://drive.google.com", "📁 Telemetry Drive Vault", "#161b22", "Raw PSCAD & SCADA Evidence"), (g4, "https://docs.google.com", "📄 Board Resolution Doc", "#161b22", "Auto-Drafted Waiver Template")]
        for col, url, label, color, caption in links:
            with col:
                st.markdown(f'<a href="{url}" target="_blank"><button style="width:100%; height:44px; background-color:{color}; color:white; border:none; border-radius:4px; font-weight:600; cursor:pointer;">{label}</button></a>', unsafe_allow_html=True)
                st.caption(caption)
    with st.container(border=True):
        st.markdown("### 🤖 Master Orchestrator Interrogation")
        st.caption("Natural-language command line querying subordinate site, management, and legal agents in real time.")
        iq1, iq2, iq3 = st.columns([2, 1, 1])
        q_text = iq1.text_input("Interrogate Master Agent:", placeholder="e.g., Where is the bleed? / Why is it stalled? / What happens if we wait 48h?", label_visibility="collapsed")
        quick_bleed, quick_why = iq2.button("Audit Active Bleed", use_container_width=True), iq3.button("Diagnose Root Friction", use_container_width=True)
        if quick_bleed: q_text = "Where is the bleed?"
        elif quick_why: q_text = "Why is it stalled?"
        if q_text:
            ql = q_text.lower()
            if "bleed" in ql or "cost" in ql: st.info(f"**Master Agent ➔ Financial Surveillance:** Current bleed rate is **${active_inc['burn_rate_sec']:.2f}/sec** (${active_inc['burn_rate_sec']*604800:,.0f}/wk). Contractor carry has accrued **$184,320**. Inaction breaches the 13.8-day crossover threshold on Day 14, exceeding the entire $1.2M transformer value.")
            elif "stall" in ql or "why" in ql: st.info("**Master Agent ➔ Friction Diagnostic:** Deadlock centered on Check #6. Elena Rostova refuses sign-off under OEM Warranty Clause 14.b due to unverified IEEE 2800 harmonic data. David Chen is blocked because the ERCOT IA § 4.2 filing gate expires in 48 hours.")
            elif "48" in ql or "wait" in ql: st.warning("**Master Agent ➔ Counterfactual Projection:** Waiting 48 hours forfeits the ERCOT Interconnection Queue position ($4.5M restudy penalty + 14-month COD slip) and incurs an additional $174,528 in idle contractor carry. Default notice triggered under PPA.")
            else: st.info(f"**Master Agent Synthesis:** Active standoff between {list(active_inc['gms'].keys())}. Recommendation: Issue Tier 1 Directorate Indemnity Carve-Out to absorb technical warranty risk and transmit COD filing immediately.")
    st.markdown("### Tier 2 | Cross-Branch General Management Arbitration")
    gm_names = list(active_inc["gms"])
    branch_columns = st.columns(2)
    for i, gname in enumerate(gm_names):
        with branch_columns[i % 2]:
            with st.container(border=True):
                gm = active_inc["gms"][gname]
                st.markdown(f"#### {gname} | {gm['title']}")
                st.caption(f"Domain: `{gm['domain']}`")
                st.warning(f"**Position:** {gm['position']}")
                st.markdown("##### Tier 3 | Site Sensor Telemetry")
                for chk in gm["checks"]:
                    if chk["status"] == "CLEARED":
                        st.success(f"✅ **{chk['id']}**: {chk['name']} — `{chk['evidence']}`")
                    else:
                        st.error(f"🚨 **{chk['id']}**: {chk['name']} — `{chk['evidence']}`")

    st.markdown("### Tier 4 | Executive Remedial Engine & Cryptographic Audit Ledger")
    t4_col1, t4_col2 = st.columns([1, 1])
    with t4_col1:
        st.markdown("#### Authorized Remedial Levers")
        st.caption("Every option projects burn deltas and liability shifts before execution.")
        choice = st.radio("Simulate Executive Remedial Action:", ["Option A: Authorize Directorate Indemnity Carve-Out (Dominant)", "Option B: Mobilize Emergency PE Testing Crew ($35k Draw)", "Option C: Demobilize Permian High-Voltage Contractors"], index=0)
        with st.container(border=True):
            st.markdown("#### Consequence & Balance-Sheet Impact Preview")
            if "Option A" in choice:
                st.markdown("* **Holding Burn Impact:** `$610,848/wk` ➔ **`$0/wk`** (Stops cash bleed immediately).\n* **Elena Rostova Liability:** **Exonerated.** Corporate Asset Defense Escrow absorbs $1.2M warranty risk.\n* **David Chen Regulatory Queue:** **Protected.** Part 2 COD filing transmitted to ERCOT within 2 hours.\n* **Fiduciary Shield:** Business Judgment Rule verified. Concurred by Dr. Arthur Pendleton.")
                if active_inc["status"] == "DEADLOCKED" and st.button("Execute Directorate Carve-Out & Lock Ledger", use_container_width=True):
                    active_inc["status"], active_inc["burn_rate_sec"] = "RESOLVED", 0.0
                    for gm in active_inc["gms"].values():
                        for c in gm["checks"]: c["status"], c["evidence"] = "CLEARED", "Directorate Override"
                    record_ledger_entry(active_inc, "CHAIRMAN DIRECTIVE: Executed Option A (Indemnity Carve-Out). Elena Rostova indemnified. Check #6 cleared. Burn halted to $0/sec.")
                    st.success("Directive Enforced. Holding burn halted to $0/sec."); st.rerun()
            elif "Option B" in choice:
                st.markdown("* **Holding Burn Impact:** `$610,848/wk` remains running + **`$35,000` capital draw**.\n* **Elena Rostova Liability:** Protected. Testing crew verifies harmonic impedance sweep on-site.\n* **David Chen Regulatory Queue:** **At Risk.** 6-hour delay consumed; leaves only 42 hours on ERCOT clock.\n* **Fiduciary Shield:** Acceptable engineering remedy; increases project expenditure.")
                if active_inc["status"] == "DEADLOCKED" and st.button("Authorize Emergency Capital Draw", use_container_width=True):
                    record_ledger_entry(active_inc, "CHAIRMAN CAPITAL DRAW: $35,000 authorized for emergency IEEE 2800 on-site testing team."); st.success("Emergency Capital Released. Ledger Updated."); st.rerun()
            else:
                st.markdown("* **Holding Burn Impact:** `$610,848/wk` ➔ **`$0/wk`** (Contractors stood down).\n* **Elena Rostova Liability:** Protected. Transformer isolated from grid.\n* **David Chen Regulatory Queue:** **TOTAL FORFEITURE.** 48-hour filing window missed. $4.5M study lost; 14-month slip.\n* **Fiduciary Shield:** ⚠️ **LOCKED BY FIDUCIARY SHIELD AGENT.** Violates capital defense threshold.")
                st.error("Action Inadmissible: Fiduciary Shield Agent has locked this option due to catastrophic queue forfeiture.")

    with t4_col2:
        st.markdown("#### Immutable Cryptographic Chain")
        for item in reversed(active_inc["audit_log"]):
            st.code(f"[{item['ts']}] SHA-256:{item['hash']} | {item['event']}", language="yaml")

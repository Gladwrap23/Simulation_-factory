import datetime
import hashlib
import json
import re
import streamlit as st

APP_BUILD_ID = "v3.0_job_capsules_sep15_2026"

if st.session_state.get("build_id") != APP_BUILD_ID:
    st.session_state.clear()
    st.session_state["build_id"] = APP_BUILD_ID

# =========================================================
# 1. APPLICATION SETUP & INDUSTRIAL OBSIDIAN STYLING
# =========================================================
st.set_page_config(
    page_title="Factory Command Post | Autonomous Capital Defense",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
        .stApp { background-color: #0d1117; color: #c9d1d9; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }

        /* Executive Scaffolding & Typography */
        p { font-size: 1.05rem !important; line-height: 1.5 !important; }
        div[data-testid="stCaptionContainer"] p { font-size: 0.95rem !important; color: #8b949e !important; }
        .stRadio label { font-size: 1.05rem !important; font-weight: 500 !important; }

        div[data-testid="stMetric"] {
            background-color: #161b22;
            border: 1px solid #30363d;
            padding: 12px 16px;
            border-radius: 6px;
            min-height: 90px;
        }
        div[data-testid="stMetricLabel"] { color: #8b949e; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600; }
        div[data-testid="stMetricValue"] { color: #f0f6fc; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 1.5rem; font-weight: 700; }

        .stButton>button {
            border-radius: 4px;
            font-weight: 700;
            letter-spacing: 0.03em;
            padding: 8px 16px;
        }
    </style>
""", unsafe_allow_html=True)

# =========================================================
# 2. SOVEREIGN PORTFOLIO & AUDIT DATA PLANE
# =========================================================
SECTORS = {
    "ERCOT BESS / Grid Storage (USA)": {
        "currency": "$",
        "asset_cap": 88_500_000,
        "baseline_docket": "ERCOT IA § 4.2 Interconnection Docket #54219",
        "baseline_date": "15 Sep 2026",
        "statute": "Delaware DGCL § 141 (Business Judgment Rule)",
        "directors": {
            "Dr. Arthur Pendleton": {
                "seat": "Chair, Grid Risk & Technical Integrity",
                "focus": "OEM Warranties, IEEE 2800 Compliance, Transformer Covenants",
                "assigned_gm": "Elena Rostova"
            },
            "David Chen (Proxy)": {
                "seat": "Chair, Regulatory & Market Compliance",
                "focus": "ERCOT Standard IA § 4.2, Interconnection Queue Defense",
                "assigned_gm": "David Chen"
            }
        },
        "incidents": {
            "INC-001": {
                "title": "ERCOT IA § 4.2 Part 2 COD Attestation Deadlock",
                "priority": "P1 - CRITICAL",
                "base_burn_rate_sec": 1.01,
                "status": "DEADLOCKED",
                "director_seat": "Dr. Arthur Pendleton",
                "deadlock_summary": "Elena Rostova (protecting $1.2M warranty) vs. David Chen (protecting $4.5M queue deposit).",
                "tier3_work_order": {
                    "id": "WO-8821-HARMONIC",
                    "title": "On-Site IEEE 2800 Harmonic Sweep",
                    "progress_pct": 75,
                    "steps": [
                        {"task": "Rack 4 PE Calibration", "done": True},
                        {"task": "Inverter Bank 1-4 Frequency Injection", "done": True},
                        {"task": "Damping Resonance Verification", "done": True},
                        {"task": "PE Digital Stamp & Packet Sign-off", "done": False}
                    ],
                    "telemetry_metrics": {
                        "THD Harmonics": ("4.1%", "Limit: 5.0% [NOMINAL]"),
                        "Inrush Damping": ("1.18 pu", "Trip: 1.40 pu"),
                        "Frequency Response": ("14.2 MW/0.1Hz", "Compliant")
                    }
                },
                "gms": {
                    "Elena Rostova": {"title": "GM - Field Operations", "checks": [{"name": "Part 2 COD Attestation Gate", "status": "BLOCKED"}]},
                    "David Chen": {"title": "GM - Regulatory", "checks": [{"name": "ICCP Attestation Record", "status": "CLEARED"}]}
                },
                "audit_log": [
                    {
                        "ts": "2026-09-14 00:00:00 UTC",
                        "hash": "8f3a9e01c4",
                        "event": "REGULATORY BASELINE DOCKET INGESTED: Asset Cap locked at $88,500,000.",
                        "snapshot": {"source": "ERCOT Docket #54219", "burn_sec": 1.01, "bjr_shield": "INITIALIZED"}
                    }
                ]
            },
            "INC-002": {"title": "Substation Step-Up Inrush Damping Validation", "priority": "P2 - HIGH", "base_burn_rate_sec": 0.45, "status": "QUEUED", "daily_bleed": 38880},
            "INC-003": {"title": "SCADA Protocol IEC 61850 Gateway", "priority": "P3 - MODERATE", "base_burn_rate_sec": 0.18, "status": "QUEUED", "daily_bleed": 15552},
            "INC-004": {"title": "BESS Inverter Firmware OTA Security Patch", "priority": "P4 - MONITORED", "base_burn_rate_sec": 0.05, "status": "QUEUED", "daily_bleed": 4320},
            "INC-005": {"title": "Substation Oil DGA Baseline Sweep", "priority": "P5 - MONITORED", "base_burn_rate_sec": 0.08, "status": "QUEUED", "daily_bleed": 6912}
        }
    },
    "Deutsche Bahn AG | Rail Corridor (Germany)": {
        "currency": "€",
        "asset_cap": 34_000_000_000,
        "baseline_docket": "Federal Railway Authority (EBA) Dossier #DE-882",
        "baseline_date": "15 Sep 2026",
        "statute": "German AktG § 93 / § 116 (Aufsichtsrat Dual-Board Shield)",
        "directors": {
            "Werner Gatzer": {"seat": "Aufsichtsratsvorsitzender (Supervisory Chair)", "focus": "EBA Statutory Compliance", "assigned_gm": "Signaling Operations Lead"}
        },
        "incidents": {
            "DB-ETCS-01": {
                "title": "Rhine-Alpine ETCS Level 2 Baseline Handshake Stall",
                "priority": "P1 - CRITICAL",
                "base_burn_rate_sec": 20.00,
                "status": "DEADLOCKED",
                "director_seat": "Werner Gatzer",
                "deadlock_summary": "Signaling GM (holding for safety telegrams) vs. Network Operations.",
                "tier3_work_order": {"id": "WO-DB-9901", "title": "RBC Certification", "progress_pct": 65, "steps": [], "telemetry_metrics": {}},
                "gms": {},
                "audit_log": [
                    {"ts": "2026-09-14 00:00:00 UTC", "hash": "de9910a1b2", "event": "EBA BASELINE INGESTED: Capital Cap €34B locked.", "snapshot": {"burn_sec": 20.00}}
                ]
            },
            "DB-002": {"title": "Track Circuit Frequency Interference", "priority": "P2 - HIGH", "base_burn_rate_sec": 8.50, "status": "QUEUED", "daily_bleed": 734400},
            "DB-003": {"title": "GSM-R Interoperability Key Refresh", "priority": "P3 - MODERATE", "base_burn_rate_sec": 2.20, "status": "QUEUED", "daily_bleed": 190080},
            "DB-004": {"title": "Catenary Tension Thermal Sag Audit", "priority": "P4 - MONITORED", "base_burn_rate_sec": 1.10, "status": "QUEUED", "daily_bleed": 95040},
            "DB-005": {"title": "Balise Telegram Ingestion Buffer Sync", "priority": "P5 - MONITORED", "base_burn_rate_sec": 0.80, "status": "QUEUED", "daily_bleed": 69120}
        }
    },
    "TEPCO Holdings | Transmission Grid (Japan)": {
        "currency": "¥",
        "asset_cap": 42_000_000_000,
        "baseline_docket": "METI Electricity Grid Intertie Filing #TK-402",
        "baseline_date": "15 Sep 2026",
        "statute": "Japanese Companies Act Art. 423 (Fiduciary Defense Shield)",
        "directors": {
            "Keisuke Yokoo": {"seat": "Chairman of the Board (取締役会長)", "focus": "METI Reliability Compliance", "assigned_gm": "Grid Operations Lead"}
        },
        "incidents": {
            "TEPCO-500KV-01": {
                "title": "Shin-Shinano 500kV Frequency Converter Synchronization Stall",
                "priority": "P1 - CRITICAL",
                "base_burn_rate_sec": 1.45,
                "status": "DEADLOCKED",
                "director_seat": "Keisuke Yokoo",
                "deadlock_summary": "Substation Chief holding dampening data vs. Power Grid GM.",
                "tier3_work_order": {"id": "WO-TEPCO-4410", "title": "Converter Verification", "progress_pct": 70, "steps": [], "telemetry_metrics": {}},
                "gms": {},
                "audit_log": [
                    {"ts": "2026-09-14 00:00:00 UTC", "hash": "jp8834f109", "event": "METI BASELINE INGESTED: Capital Cap ¥42B locked.", "snapshot": {"burn_sec": 1.45}}
                ]
            },
            "TEP-002": {"title": "Transformer Bushing Tan-Delta Spike", "priority": "P2 - HIGH", "base_burn_rate_sec": 0.85, "status": "QUEUED", "daily_bleed": 73440},
            "TEP-003": {"title": "50Hz/60Hz Intertie Buffer Calibration", "priority": "P3 - MODERATE", "base_burn_rate_sec": 0.40, "status": "QUEUED", "daily_bleed": 34560},
            "TEP-004": {"title": "SF6 Gas Pressure Telemetry Recalibration", "priority": "P4 - MONITORED", "base_burn_rate_sec": 0.15, "status": "QUEUED", "daily_bleed": 12960},
            "TEP-005": {"title": "Substation Seismic Isolator Verification", "priority": "P5 - MONITORED", "base_burn_rate_sec": 0.20, "status": "QUEUED", "daily_bleed": 17280}
        }
    }
}

# Session State Initialization
TODAY_STR = "15 Sep 2026"
if "app_state" not in st.session_state or "baseline_docket" not in list(st.session_state.app_state.values())[0]:
    st.session_state.app_state = SECTORS

if "selected_incident_id" not in st.session_state:
    st.session_state.selected_incident_id = "INC-001"

if "conference_focus" not in st.session_state:
    st.session_state.conference_focus = "NONE"

if "remedial_simulation" not in st.session_state:
    st.session_state.remedial_simulation = "Option A: Directorate Carve-Out (Dominant Path)"

def append_to_active_package(incident: dict, job_title: str, event_text: str, force_new_package=False):
    packages = incident.setdefault("audit_packages", [])
    now_str = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    if force_new_package or not packages or packages[-1]["status"] == "SEALED & ATTESTED":
        new_hash = hashlib.sha256(f"{now_str}|{job_title}|{event_text}".encode()).hexdigest()[:15]
        packages.append({
            "job_id": job_title,
            "status": "ACTIVE AUDIT IN PROGRESS",
            "opened_at": now_str,
            "package_hash": new_hash,
            "entries": [f"[{now_str}] {event_text}"]
        })
    else:
        active_pkg = packages[-1]
        active_pkg["entries"].append(f"[{now_str}] {event_text}")
        active_pkg["package_hash"] = hashlib.sha256(
            f"{active_pkg['package_hash']}{event_text}".encode()
        ).hexdigest()[:15]


def seal_active_package(incident: dict):
    packages = incident.get("audit_packages", [])
    if packages and packages[-1]["status"] == "ACTIVE AUDIT IN PROGRESS":
        packages[-1]["status"] = "SEALED & ATTESTED"
        packages[-1]["sealed_at"] = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")


def record_ledger_entry(incident: dict, event_text: str, custom_snapshot=None):
    append_to_active_package(incident, "GOVERNANCE EVENT", event_text)

# =========================================================
# 3. SIDEBAR: OPERATING BOOK & WORK ORDER QUEUE
# =========================================================
with st.sidebar:
    st.markdown("### 🏛️ COMMAND POST")
    st.caption("Autonomous Capital Defense Control Plane")

    lang_choice = st.selectbox(
        "Localization / 言語 / Sprache:",
        ["English (US / UK / AU)", "日本語 (Japanese)", "Deutsch (German)"]
    )

    active_sector = st.selectbox(
        "Operating Book (Global Assets):",
        list(st.session_state.app_state.keys())
    )
    sector = st.session_state.app_state[active_sector]
    curr_sym = sector["currency"]

    selected_role = st.radio(
        "Active Governance Profile:",
        ["Executive Chairman (Panoramic Tree)", "Tier 3: Site Operations / Field Lead"] +
        [f"Director: {d}" for d in sector["directors"].keys()]
    )

    st.divider()
    st.markdown("#### Active Incident Queue")
    for inc_key, inc_obj in sector["incidents"].items():
        is_sel = inc_key == st.session_state.selected_incident_id
        btn_label = f"{inc_obj.get('priority', 'MONITORED')}: {inc_key}\n{inc_obj['title'][:26]}..."
        if st.button(btn_label, key=f"sb_{inc_key}", use_container_width=True, type="primary" if is_sel else "secondary"):
            st.session_state.selected_incident_id = inc_key
            st.session_state.conference_focus = "NONE"
            st.rerun()

if st.session_state.selected_incident_id not in sector["incidents"]:
    st.session_state.selected_incident_id = list(sector["incidents"].keys())[0]

active_inc = sector["incidents"][st.session_state.selected_incident_id]
is_resolved = active_inc.get("status") == "RESOLVED"
current_burn_sec = active_inc.get("base_burn_rate_sec", 0.0) if not is_resolved else 0.0

if "audit_packages" not in active_inc:
    legacy_entries = active_inc.pop("audit_log", [])
    active_inc["audit_packages"] = [{
        "job_id": "JOB-001: Statutory Ingestion Baseline",
        "status": "SEALED & ATTESTED",
        "sealed_at": sector.get("baseline_date", f"{TODAY_STR} 00:00 UTC"),
        "package_hash": legacy_entries[0].get("hash", "000000000000000") if legacy_entries else "000000000000000",
        "entries": [entry.get("event", "Baseline docket ingested.") for entry in legacy_entries]
    }]

# =========================================================
# 4. VIEW: EXECUTIVE CHAIRMAN (MASTER COMMAND POST)
# =========================================================
if selected_role == "Executive Chairman (Panoramic Tree)":
    st.title("Executive Chairman Command Post")
    st.caption(f"Asset: **{active_sector}** | Legal Defense: **{sector['statute']}**")

    # ---------------------------------------------------------
    # DUAL-RECORD QUICK-CALIBRATOR (TIMESTAMPED AUDIT ENGINE)
    # ---------------------------------------------------------
    calib_key = f"capex_override_{active_sector}"
    ts_key = f"capex_ts_{active_sector}"

    if calib_key not in st.session_state:
        st.session_state[calib_key] = int(sector["asset_cap"])
    if ts_key not in st.session_state:
        st.session_state[ts_key] = sector["baseline_date"]

    with st.container(border=True):
        qc1, qc2, qc3 = st.columns([2, 1, 1])
        with qc1:
            st.markdown(f"""
                <div style="font-size:0.85rem; color:#8b949e; margin-bottom:4px;">
                    Public Docket Baseline: <strong style="color:#c9d1d9;">{curr_sym}{sector['asset_cap']:,}</strong>
                    <span style="color:#58a6ff;">({sector['baseline_docket']} | {sector['baseline_date']})</span>
                </div>
            """, unsafe_allow_html=True)

            raw_input_str = st.text_input(
                "Chairman Quick-Calibrator: Enter Project Budget / CapEx at Risk:",
                value=f"{st.session_state[calib_key]:,}"
            )
            new_capex = int(re.sub(r"[^\d]", "", raw_input_str) or sector["asset_cap"])

            # Detect Calibration Divergence & Stamp to Audit Ledger
            if new_capex != st.session_state[calib_key]:
                now_str = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
                st.session_state[calib_key] = new_capex
                st.session_state[ts_key] = now_str
                record_ledger_entry(
                    active_inc,
                    f"Chairman established internal valuation of {curr_sym}{new_capex:,} (Delta: {curr_sym}{new_capex - sector['asset_cap']:,}).",
                    {"calibrated_capex": new_capex, "prior_baseline": sector["asset_cap"], "timestamp": now_str}
                )
                st.rerun()

            calibrated_toll_gate = max(25_000, int(round(new_capex * 0.00085, -3)))

            # Dynamic Font & Badge Response
            is_overridden = new_capex != sector["asset_cap"]
            badge_color = "#e3b341" if is_overridden else "#58a6ff"
            badge_label = "EXECUTIVE OVERRIDE LOCKED" if is_overridden else "PUBLIC BASELINE SYNCHRONIZED"
            st.markdown(f"""
                <div style="font-size:0.85rem; font-weight:700; color:{badge_color}; margin-top:4px;">
                    ● {badge_label}: {curr_sym}{new_capex:,} <span style="color:#8b949e; font-weight:400;">(Effective: {st.session_state[ts_key]})</span>
                </div>
            """, unsafe_allow_html=True)

        with qc2:
            if is_resolved:
                st.markdown(f"""
                    <div style="background-color:rgba(46,160,67,0.15); border:1px solid #2ea043; padding:10px 14px; border-radius:6px; min-height:85px;">
                        <div style="color:#3fb950; font-size:0.75rem; font-weight:bold; text-transform:uppercase;">🟢 Toll-Gate Settlement Due</div>
                        <div style="color:#f0f6fc; font-family:monospace; font-size:1.45rem; font-weight:bold;">{curr_sym}{calibrated_toll_gate:,}</div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.metric("Toll-Gate Fee (Milestone)", f"{curr_sym}{calibrated_toll_gate:,}", "0.085% CapEx Escrow")

        with qc3:
            if is_resolved:
                st.markdown("""
                    <div style="background-color:rgba(46,160,67,0.15); border:1px solid #2ea043; padding:10px 14px; border-radius:6px; min-height:85px;">
                        <div style="color:#3fb950; font-size:0.75rem; font-weight:bold; text-transform:uppercase;">✅ BJR Shield Status</div>
                        <div style="color:#f0f6fc; font-family:monospace; font-size:1.45rem; font-weight:bold;">AWAITING WIRE</div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.metric("Live Session Window", "09:42", "Zero-Retention Enforced")

    # ---------------------------------------------------------
    # MAIN TRUNK: DYNAMIC CROSSOVER HORIZON
    # ---------------------------------------------------------
    active_incidents = [i for i in sector["incidents"].values() if i.get("status") != "RESOLVED"]
    total_burn_day = sum(i.get("daily_bleed", i.get("base_burn_rate_sec", 0.0) * 86400) for i in active_incidents)
    total_burn_wk = total_burn_day * 7

    # Mathematical Crossover Formula tied to Chairman's CapEx input
    dynamic_crossover_days = round(new_capex / total_burn_day, 1) if total_burn_day > 0 else 999.9

    k1, k2, k3 = st.columns(3)
    k1.metric(
        "Portfolio Holding Burn",
        f"{curr_sym}{total_burn_wk:,.0f} / wk",
        f"{curr_sym}{total_burn_day:,.0f} / Day",
        delta_color="inverse"
    )
    k2.metric(
        "Capital Under Defense",
        f"{curr_sym}{new_capex:,.0f}",
        "Asset Defense Escrow Intact"
    )
    k3.metric(
        "Active Operational Block",
        f"{st.session_state.selected_incident_id}",
        f"Crossover: {dynamic_crossover_days} Days",
        delta_color="inverse"
    )

    # ---------------------------------------------------------
    # INSTANT AGENT DIAGNOSTIC CONFERENCE
    # ---------------------------------------------------------
    with st.container(border=True):
        st.markdown("### 🎙️ Instant Diagnostic Agent Conference")
        st.caption("Interrogate domain agents to diagnose root friction without micromanaging field physics.")

        cq1, cq2, cq3 = st.columns([2, 1, 1])
        cq1.text_input("Conference Query:", placeholder="Type query...", label_visibility="collapsed")
        if cq2.button("🚨 Why is the Fix Stalled?", use_container_width=True):
            st.session_state.conference_focus = "WHY_STALLED"
            append_to_active_package(active_inc, "DIAGNOSTIC", "Inquiry executed: Why is the fix stalled?")
        if cq3.button("What Unblocks the GM?", use_container_width=True):
            st.session_state.conference_focus = "WHAT_UNBLOCKS"
            append_to_active_package(active_inc, "DIAGNOSTIC", "Inquiry executed: What unblocks the gate?")

        if st.session_state.conference_focus == "WHY_STALLED":
            st.markdown("---")
            st.markdown(
                "🔴 **Master Orchestrator ➔ Site Telemetry Agent:** *'Inquire status on active work order. Why is the gate blocked?'*\n\n"
                "🔴 **Site Telemetry Agent:** *'Crew is staged on site. However, the OEM field supervisor is withholding physical access to the relay cabinet pending written corporate indemnity. Mechanical physics are nominal (THD at 4.1%); access is legally blocked.'*"
            )
        elif st.session_state.conference_focus == "WHAT_UNBLOCKS":
            st.markdown("---")
            st.markdown(
                "🟢 **Master Orchestrator ➔ Fiduciary Shield Agent:** *'What legal instrument unblocks the GM without personal liability exposure?'*\n\n"
                "🟢 **Fiduciary Shield Agent:** *'A Board Resolution (Option A) executing a Directorate Indemnity Carve-Out from the corporate Asset Defense Escrow absorbs all liability at the board level, clearing the GM to sign within 5 minutes.'*"
            )

    # ---------------------------------------------------------
    # POINT-OF-DECISION REMEDIAL LEVERS
    # ---------------------------------------------------------
    st.markdown("### The Three Cascading Branches & Remedial Levers")
    st.caption("Simulate executive levers to project immediate consequences across Physical, Market, and Fiduciary pillars:")

    with st.container(border=True):
        rem_col1, rem_col2 = st.columns([3, 1])
        with rem_col1:
            st.session_state.remedial_simulation = st.radio(
                "Select Executive Action to Simulate:",
                [
                    "Option A: Directorate Carve-Out (Dominant Path)",
                    "Option B: Mobilize Secondary Field Crew ($35k Draw)",
                    "Option C: Demobilize Site Contractors (Standby)"
                ],
                horizontal=True
            )
        with rem_col2:
            st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
            if not is_resolved:
                if "Option A" in st.session_state.remedial_simulation:
                    if st.button("Execute Option A Directive", use_container_width=True, type="primary"):
                        active_inc["status"] = "RESOLVED"
                        active_inc["base_burn_rate_sec"] = 0.0
                        wo = active_inc.get("tier3_work_order", {})
                        wo["progress_pct"] = 100
                        for s in wo.get("steps", []):
                            s["done"] = True
                        for gm in active_inc.get("gms", {}).values():
                            for c in gm.get("checks", []):
                                c["status"] = "CLEARED"
                        record_ledger_entry(
                            active_inc,
                            f"CHAIRMAN DIRECTIVE: Option A executed on {st.session_state.selected_incident_id}. Holding burn halted to 0."
                        )
                        st.session_state.conference_focus = "NONE"
                        st.success("Option A Executed. Holding burn halted to 0.")
                        st.rerun()
                elif "Option B" in st.session_state.remedial_simulation:
                    if st.button("Authorize $35k Capital Draw", use_container_width=True):
                        record_ledger_entry(active_inc, f"CAPITAL DRAW: $35,000 authorized for secondary crew.")
                        st.success("Capital Released.")
                        st.rerun()
                else:
                    st.button("Option Inadmissible", use_container_width=True, disabled=True)
            else:
                if st.button(f"⚡ Settle Milestone Fee ({curr_sym}{calibrated_toll_gate:,})", use_container_width=True, type="primary"):
                    seal_active_package(active_inc)
                    st.success("Milestone Settled. Audit Capsule Sealed. Ready to unlock INC-002.")

    # ---------------------------------------------------------
    # THE THREE CASCADING BRANCHES (ACCOUNTABILITY HEATMAP)
    # ---------------------------------------------------------
    b_col1, b_col2, b_col3 = st.columns(3)

    def render_branch_card(title, domain, director_name, agent_name, status_badge, metric_txt, card_type):
        border_col = "#2ea043" if card_type == "green" else ("#e3b341" if card_type == "amber" else "#da3633")
        bg_col = "rgba(46, 160, 67, 0.15)" if card_type == "green" else ("rgba(227, 179, 65, 0.15)" if card_type == "amber" else "rgba(218, 54, 51, 0.15)")

        return f"""
        <div style="background-color: {bg_col}; border: 2px solid {border_col}; border-radius: 8px; padding: 20px; height: 100%; display: flex; flex-direction: column; gap: 12px;">
            <h3 style="margin:0; color:#f0f6fc; font-size:1.35rem; font-weight:700;">{title}</h3>
            <div style="color:#e6edf3; font-size:1.1rem; font-weight:600; border-bottom: 1px solid #30363d; padding-bottom: 10px; margin-bottom: 4px;">
                {domain}
            </div>
            <div style="font-size:0.95rem; color:#8b949e;">
                Cognizant Director: <br>
                <strong style="color:#ffffff; font-size:1.25rem; display:inline-block; margin-top:4px;">{director_name}</strong>
            </div>
            <div style="font-size:0.95rem; color:#8b949e;">
                Embedded Agent: <br>
                <code style="color:#a5d6ff; background:rgba(56,139,253,0.15); padding:4px 8px; font-size:0.95rem; border-radius:4px; display:inline-block; margin-top:4px;">{agent_name}</code>
            </div>
            <div style="font-weight:700; font-size:1.15rem; padding: 12px 14px; background: rgba(0,0,0,0.3); border-radius: 6px; border-left: 5px solid {border_col}; color:#f0f6fc; margin-top:4px;">
                {status_badge}
            </div>
            <div style="font-family:ui-monospace, monospace; color:#c9d1d9; font-size:1.05rem; margin-top: auto; padding-top: 10px;">
                {metric_txt}
            </div>
        </div>
        """

    with b_col1:
        c_type = "green" if is_resolved else "red"
        s_badge = "🟢 CLEARED: Field access granted." if is_resolved else "🔴 OUTSTANDING: Field access locked."
        wo_id = active_inc.get("tier3_work_order", {}).get("id", "N/A")
        wo_pct = 100 if is_resolved else active_inc.get("tier3_work_order", {}).get("progress_pct", 0)
        st.markdown(render_branch_card(
            "Branch 1: Physical / Field",
            "Hardware Gate | Plant & Crews",
            active_inc.get("director_seat", "Technical Integrity"),
            "Site Telemetry Agent",
            s_badge,
            f"Work Order: {wo_id} ({wo_pct}%)",
            c_type
        ), unsafe_allow_html=True)

    with b_col2:
        c_type = "green" if is_resolved else "amber"
        s_badge = "🟢 CLEARED: Grid filing secured." if is_resolved else "🟡 COLLATERAL: 48h Window Expiring."
        st.markdown(render_branch_card(
            "Branch 2: Regulatory / Market",
            "Commercial Gate | Interconnection",
            "David Chen (Proxy)",
            "Market Surveillance Agent",
            s_badge,
            "Handshake Status: Latency Validated",
            c_type
        ), unsafe_allow_html=True)

    with b_col3:
        c_type = "green" if is_resolved else "red"
        s_badge = "🟢 CLEARED: Capital defended." if is_resolved else f"🔴 OUTSTANDING: Crossover in {dynamic_crossover_days}d."
        vel_txt = f"Velocity: {curr_sym}0.00/sec" if is_resolved else f"Velocity: {curr_sym}{current_burn_sec:.2f}/sec"
        st.markdown(render_branch_card(
            "Branch 3: Fiduciary / Capital",
            "Balance Sheet Gate | Liability Escrow",
            "Executive Board Chair",
            "Fiduciary Shield Agent",
            s_badge,
            vel_txt,
            c_type
        ), unsafe_allow_html=True)

    # ---------------------------------------------------------
    # GATED INCIDENT PIPELINE (HIGH-IMPACT DAILY BLEED)
    # ---------------------------------------------------------
    with st.container(border=True):
        st.markdown("### 🔒 Gated Incident Pipeline (Next 4 Bottlenecks)")
        st.caption("Sequential project bottlenecks locked behind Milestone fee settlement:")

        p1, p2, p3, p4 = st.columns(4)

        def render_pipeline_card(num_title, daily_amt, sec_rate, inc_code, is_threat):
            border = "#e3b341" if is_threat else "#30363d"
            bg = "rgba(227, 179, 65, 0.12)" if is_threat else "#161b22"
            status_txt = "🟡 ACTIVE THREAT" if is_threat else "🔒 QUEUED"
            status_color = "#e3b341" if is_threat else "#8b949e"

            return f"""
            <div style="background-color:{bg}; border:2px solid {border}; border-radius:8px; padding:16px; height:100%; display:flex; flex-direction:column;">
                <div style="font-weight:700; font-size:1.05rem; color:#f0f6fc; margin-bottom:6px;">{num_title}</div>
                <div style="font-family:ui-monospace, monospace; font-size:1.45rem; font-weight:800; color:#f0f6fc; margin-top:4px;">
                    {curr_sym}{daily_amt:,} <span style="font-size:0.9rem; font-weight:500; color:#8b949e;">/ Day</span>
                </div>
                <div style="font-size:0.8rem; color:#8b949e; margin-bottom:12px;">Base rate: {curr_sym}{sec_rate:.2f}/sec</div>
                <div style="font-size:0.9rem; font-weight:700; color:{status_color}; margin-top:auto;">{status_txt}: {inc_code}</div>
            </div>
            """

        pipe_keys = [k for k in sector["incidents"].keys() if k != "INC-001" and k != "DB-ETCS-01" and k != "TEPCO-500KV-01"]

        with p1:
            inc_p1 = sector["incidents"].get(pipe_keys[0] if len(pipe_keys) > 0 else "INC-002", {})
            st.markdown(render_pipeline_card("1. Inrush Damping", inc_p1.get("daily_bleed", 38880), inc_p1.get("base_burn_rate_sec", 0.45), pipe_keys[0] if len(pipe_keys) > 0 else "INC-002", is_resolved), unsafe_allow_html=True)
        with p2:
            inc_p2 = sector["incidents"].get(pipe_keys[1] if len(pipe_keys) > 1 else "INC-003", {})
            st.markdown(render_pipeline_card("2. SCADA IEC 61850", inc_p2.get("daily_bleed", 15552), inc_p2.get("base_burn_rate_sec", 0.18), pipe_keys[1] if len(pipe_keys) > 1 else "INC-003", False), unsafe_allow_html=True)
        with p3:
            inc_p3 = sector["incidents"].get(pipe_keys[2] if len(pipe_keys) > 2 else "INC-004", {})
            st.markdown(render_pipeline_card("3. BESS Firmware OTA", inc_p3.get("daily_bleed", 4320), inc_p3.get("base_burn_rate_sec", 0.05), pipe_keys[2] if len(pipe_keys) > 2 else "INC-004", False), unsafe_allow_html=True)
        with p4:
            inc_p4 = sector["incidents"].get(pipe_keys[3] if len(pipe_keys) > 3 else "INC-005", {})
            st.markdown(render_pipeline_card("4. Substation Oil DGA", inc_p4.get("daily_bleed", 6912), inc_p4.get("base_burn_rate_sec", 0.08), pipe_keys[3] if len(pipe_keys) > 3 else "INC-005", False), unsafe_allow_html=True)

    # ---------------------------------------------------------
    # TIER 4: JOB-PACKAGED CRYPTOGRAPHIC AUDIT CAPSULES
    # ---------------------------------------------------------
    with st.container(border=True):
        st.markdown("### Tier 4 | Sealed Cryptographic Job Capsules")
        st.caption("Discrete decision packages signed and sealed per executive mandate. Immutable proof under the Business Judgment Rule.")
        for pkg in reversed(active_inc.get("audit_packages", [])):
            is_sealed = pkg["status"] == "SEALED & ATTESTED"
            badge_icon = "🔒" if is_sealed else "⚡"
            status_color = "#3fb950" if is_sealed else "#e3b341"
            with st.expander(f"{badge_icon} {pkg['job_id']} | Root Hash: SHA-256:{pkg['package_hash']}", expanded=not is_sealed):
                st.markdown(f"**Status:** <span style='color:{status_color}; font-weight:bold;'>{pkg['status']}</span>", unsafe_allow_html=True)
                for entry in pkg.get("entries", []):
                    st.markdown(f"- `{entry}`")

# =========================================================
# 5. VIEW: TIER 3 SITE OPERATIONS & FIELD DESK
# =========================================================
elif selected_role == "Tier 3: Site Operations / Field Lead":
    st.title("Tier 3 | Site Operations & Field Execution Desk")
    wo = active_inc.get("tier3_work_order", {})
    t1, t2, t3 = st.columns(3)
    t1.metric("Work Order", wo.get("id", "N/A"), active_inc.get("priority", "CRITICAL"))
    t2.metric("Target Gate", "Check #6 (COD Attestation)")
    t3.metric("Progress", f"{wo.get('progress_pct', 0)}%")

    col_t, col_m = st.columns([3, 2])
    with col_t:
        with st.container(border=True):
            st.markdown(f"#### Punch List: {wo.get('title', 'Tasks')}")
            for idx, step in enumerate(wo.get("steps", [])):
                st.write(f"{'✅' if step['done'] else '⏳'} **Step {idx+1}:** {step['task']}")
            if not is_resolved and st.button("Complete Final PE Verification Stamp", use_container_width=True, type="primary"):
                wo["progress_pct"] = 100
                if wo.get("steps"): wo["steps"][-1]["done"] = True
                active_inc["status"] = "RESOLVED"
                active_inc["base_burn_rate_sec"] = 0.0
                record_ledger_entry(active_inc, "TIER 3 FIELD STAMP: Telemetry validated on-site. Burn halted.")
                st.success("Stamped & Transmitted.")
                st.rerun()
    with col_m:
        with st.container(border=True):
            st.markdown("#### Live Telemetry")
            for k, (v, tol) in wo.get("telemetry_metrics", {}).items():
                st.metric(k, v, delta=tol)

# =========================================================
# 6. VIEW: COGNIZANT DIRECTOR
# =========================================================
else:
    dir_name = selected_role.replace("Director: ", "")
    st.title(f"Directorate Oversight: {dir_name}")
    st.metric("Jurisdiction Status", active_inc.get("status", "DEADLOCKED"), active_inc.get("priority", "P1"))
    if not is_resolved and st.button("Issue Directorate Formal Concurrence", use_container_width=True):
        record_ledger_entry(active_inc, f"FORMAL CONCURRENCE: {dir_name} concurred for {st.session_state.selected_incident_id}.")
        st.success("Concurrence sealed to ledger.")
        st.rerun()

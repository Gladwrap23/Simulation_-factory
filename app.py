import datetime
import hashlib
import json
import re
import streamlit as st

APP_BUILD_ID = "v3.2_high_contrast_typography_sep15_2026"

if st.session_state.get("build_id") != APP_BUILD_ID:
    st.session_state.clear()
    st.session_state["build_id"] = APP_BUILD_ID

st.set_page_config(
    page_title="Factory Command Post | Autonomous Capital Defense",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# 1. INDUSTRIAL HIGH-CONTRAST TYPOGRAPHY OVERHAUL
# =========================================================
st.markdown("""
    <style>
        .stApp { 
            background-color: #0d1117; 
            color: #f0f6fc; 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; 
        }
        
        /* Global eradication of fine print */
        p { 
            font-size: 1.1rem !important; 
            line-height: 1.6 !important; 
            color: #f0f6fc !important;
        }
        div[data-testid="stCaptionContainer"] p { 
            font-size: 1.05rem !important; 
            color: #c9d1d9 !important; 
            font-weight: 500 !important; 
        }
        .stRadio label { 
            font-size: 1.1rem !important; 
            font-weight: 600 !important; 
            color: #f0f6fc !important;
        }
        
        /* High-Contrast Executive Metrics */
        .exec-metric-card {
            background-color: #161b22;
            border: 2px solid #30363d;
            border-radius: 8px;
            padding: 16px 20px;
            text-align: center;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            min-height: 120px;
        }
        .exec-metric-label {
            color: #e6edf3;
            font-size: 0.95rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            margin-bottom: 6px;
        }
        .exec-metric-val {
            color: #ffffff;
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
            font-size: 1.95rem;
            font-weight: 800;
            line-height: 1.15;
        }
        .exec-metric-sub {
            font-size: 0.95rem;
            font-weight: 700;
            margin-top: 6px;
        }
        
        .stButton>button {
            border-radius: 6px;
            font-weight: 700;
            font-size: 1.05rem !important;
            letter-spacing: 0.02em;
            padding: 10px 18px;
        }
    </style>
""", unsafe_allow_html=True)

TODAY_STR = "15 Sep 2026"

SECTORS = {
    "ERCOT BESS / Grid Storage (USA)": {
        "currency": "$",
        "asset_cap": 88_500_000,
        "baseline_docket": "ERCOT IA § 4.2 Interconnection Docket #54219",
        "baseline_date": "15 Sep 2026",
        "statute": "Delaware DGCL § 141 (Business Judgment Rule)",
        "directors": {
            "Dr. Arthur Pendleton": {"seat": "Chair, Grid Risk & Technical Integrity"},
            "David Chen (Proxy)": {"seat": "Chair, Regulatory & Market Compliance"}
        },
        "incidents": {
            "INC-001": {
                "title": "ERCOT IA § 4.2 Part 2 COD Attestation Deadlock",
                "priority": "P1 - CRITICAL",
                "base_daily_bleed": 87264,
                "status": "DEADLOCKED",
                "director_seat": "Dr. Arthur Pendleton",
                "tier3_work_order": {
                    "id": "WO-8821-HARMONIC",
                    "title": "On-Site IEEE 2800 Harmonic Sweep",
                    "progress_pct": 75,
                    "steps": [
                        {"task": "Rack 4 PE Calibration", "done": True},
                        {"task": "Inverter Bank 1-4 Frequency Injection", "done": True},
                        {"task": "Damping Resonance Verification", "done": True},
                        {"task": "PE Digital Stamp & Packet Sign-off", "done": False}
                    ]
                },
                "audit_packages": [
                    {
                        "job_id": "JOB-001: Statutory Ingestion Baseline",
                        "status": "SEALED & ATTESTED",
                        "sealed_at": "2026-09-15 00:00:00 UTC",
                        "package_hash": "8f3a9e01c4b72e1",
                        "entries": [
                            "DOCKET INGESTION: Baseline verified against ERCOT Docket #54219.",
                            "CAPITAL AUDIT: Sovereign capital cap locked at $88,500,000.",
                            "FIDUCIARY ANCHOR: Delaware DGCL § 141 safe harbor initialized."
                        ]
                    }
                ]
            },
            "INC-002": {"title": "Substation Step-Up Inrush Damping", "priority": "P2 - HIGH", "base_daily_bleed": 38880},
            "INC-003": {"title": "SCADA Protocol IEC 61850 Gateway", "priority": "P3 - MODERATE", "base_daily_bleed": 15552},
            "INC-004": {"title": "BESS Inverter Firmware OTA Patch", "priority": "P4 - MONITORED", "base_daily_bleed": 4320},
            "INC-005": {"title": "Substation Oil DGA Baseline Sweep", "priority": "P5 - MONITORED", "base_daily_bleed": 6912}
        }
    },
    "Deutsche Bahn AG | Rail Corridor (Germany)": {
        "currency": "€",
        "asset_cap": 34_000_000_000,
        "baseline_docket": "Federal Railway Authority (EBA) Dossier #DE-882",
        "baseline_date": "15 Sep 2026",
        "statute": "German AktG § 93 / § 116 (Aufsichtsrat Dual-Board Shield)",
        "directors": {"Werner Gatzer": {"seat": "Aufsichtsratsvorsitzender"}},
        "incidents": {
            "DB-ETCS-01": {
                "title": "Rhine-Alpine ETCS Level 2 Baseline Handshake Stall",
                "priority": "P1 - CRITICAL",
                "base_daily_bleed": 1728000,
                "status": "DEADLOCKED",
                "director_seat": "Werner Gatzer",
                "tier3_work_order": {"id": "WO-DB-9901", "progress_pct": 65, "steps": []},
                "audit_packages": [
                    {
                        "job_id": "JOB-001: EBA Baseline Ingestion",
                        "status": "SEALED & ATTESTED",
                        "sealed_at": "2026-09-15 00:00:00 UTC",
                        "package_hash": "de9910a1b2c45e8",
                        "entries": ["EBA DOCKET INGESTION: Rhine Corridor Dossier #DE-882 locked."]
                    }
                ]
            },
            "DB-002": {"title": "Track Circuit Frequency Interference", "priority": "P2 - HIGH", "base_daily_bleed": 734400},
            "DB-003": {"title": "GSM-R Interoperability Key Refresh", "priority": "P3 - MODERATE", "base_daily_bleed": 190080},
            "DB-004": {"title": "Catenary Tension Thermal Sag Audit", "priority": "P4 - MONITORED", "base_daily_bleed": 95040},
            "DB-005": {"title": "Balise Telegram Buffer Sync", "priority": "P5 - MONITORED", "base_daily_bleed": 69120}
        }
    },
    "TEPCO Holdings | Transmission Grid (Japan)": {
        "currency": "¥",
        "asset_cap": 42_000_000_000,
        "baseline_docket": "METI Electricity Grid Intertie Filing #TK-402",
        "baseline_date": "15 Sep 2026",
        "statute": "Japanese Companies Act Art. 423 (Fiduciary Defense Shield)",
        "directors": {"Keisuke Yokoo": {"seat": "Chairman of the Board"}},
        "incidents": {
            "TEPCO-500KV-01": {
                "title": "Shin-Shinano 500kV Frequency Converter Synchronization Stall",
                "priority": "P1 - CRITICAL",
                "base_daily_bleed": 125280,
                "status": "DEADLOCKED",
                "director_seat": "Keisuke Yokoo",
                "tier3_work_order": {"id": "WO-TEPCO-4410", "progress_pct": 70, "steps": []},
                "audit_packages": [
                    {
                        "job_id": "JOB-001: METI Baseline Ingestion",
                        "status": "SEALED & ATTESTED",
                        "sealed_at": "2026-09-15 00:00:00 UTC",
                        "package_hash": "jp8834f109a12c7",
                        "entries": ["METI INTERTIE FILING: Shin-Shinano 500kV locked."]
                    }
                ]
            },
            "TEP-002": {"title": "Transformer Bushing Tan-Delta Spike", "priority": "P2 - HIGH", "base_daily_bleed": 73440},
            "TEP-003": {"title": "50Hz/60Hz Intertie Buffer Calibration", "priority": "P3 - MODERATE", "base_daily_bleed": 34560},
            "TEP-004": {"title": "SF6 Gas Pressure Telemetry Recalibration", "priority": "P4 - MONITORED", "base_daily_bleed": 12960},
            "TEP-005": {"title": "Substation Seismic Isolator Verification", "priority": "P5 - MONITORED", "base_daily_bleed": 17280}
        }
    }
}

if "app_state" not in st.session_state:
    st.session_state.app_state = SECTORS

if "selected_incident_id" not in st.session_state:
    st.session_state.selected_incident_id = "INC-001"

if "conference_focus" not in st.session_state:
    st.session_state.conference_focus = "DEFAULT"

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
        combined = active_pkg["package_hash"] + event_text
        active_pkg["package_hash"] = hashlib.sha256(combined.encode()).hexdigest()[:15]

def seal_active_package(incident: dict):
    packages = incident.get("audit_packages", [])
    if packages and packages[-1]["status"] == "ACTIVE AUDIT IN PROGRESS":
        packages[-1]["status"] = "SEALED & ATTESTED"
        packages[-1]["sealed_at"] = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.markdown("### 🏛️ COMMAND POST")
    st.markdown("<div style='font-size:0.95rem; color:#c9d1d9; margin-bottom:12px;'>Autonomous Capital Defense Control Plane</div>", unsafe_allow_html=True)
    
    st.selectbox("Localization / 言語 / Sprache:", ["English (US / UK / AU)", "日本語 (Japanese)", "Deutsch (German)"])
    
    active_sector = st.selectbox("Operating Book (Global Assets):", list(st.session_state.app_state.keys()))
    sector = st.session_state.app_state[active_sector]
    curr_sym = sector["currency"]
    
    calib_key = f"capex_override_{active_sector}"
    if calib_key not in st.session_state:
        st.session_state[calib_key] = int(sector["asset_cap"])
    current_calib_capex = st.session_state[calib_key]
    scale_factor = current_calib_capex / sector["asset_cap"]

    selected_role = st.radio(
        "Active Governance Profile:",
        ["Executive Chairman (Panoramic Tree)", "Tier 3: Site Operations / Field Lead"] +
        [f"Director: {d}" for d in sector["directors"].keys()]
    )
    
    st.divider()
    st.markdown("#### Active Incident Queue")
    st.caption("Crossover horizons scaled to Chairman CapEx:")
    
    for inc_key, inc_obj in sector["incidents"].items():
        is_sel = inc_key == st.session_state.selected_incident_id
        inc_daily = inc_obj.get("base_daily_bleed", 50000) * scale_factor
        inc_crossover = round(current_calib_capex / inc_daily, 1) if inc_daily > 0 else 999
        btn_label = f"{inc_obj.get('priority', 'P1')}: {inc_key}\n{inc_crossover}d Crossover Horizon"
        
        if st.button(btn_label, key=f"sb_{inc_key}", use_container_width=True, type="primary" if is_sel else "secondary"):
            st.session_state.selected_incident_id = inc_key
            st.session_state.conference_focus = "DEFAULT"
            st.rerun()

if st.session_state.selected_incident_id not in sector["incidents"]:
    st.session_state.selected_incident_id = list(sector["incidents"].keys())[0]

active_inc = sector["incidents"][st.session_state.selected_incident_id]
is_resolved = active_inc.get("status") == "RESOLVED"

# =========================================================
# EXECUTIVE CHAIRMAN VIEW
# =========================================================
if selected_role == "Executive Chairman (Panoramic Tree)":
    st.title("Executive Chairman Command Post")
    
    # High-Visibility Legal Defense Banner
    st.markdown(f"""
        <div style="background: rgba(88, 166, 255, 0.1); border: 1px solid #58a6ff; border-radius: 6px; padding: 10px 16px; margin-bottom: 16px; font-size: 1.05rem; display: flex; flex-wrap: wrap; gap: 16px; align-items: center;">
            <div>Asset: <strong style="color:#ffffff;">{active_sector}</strong></div>
            <div style="color:#58a6ff;">|</div>
            <div>Legal Defense Shield: <strong style="color:#58a6ff;">{sector['statute']}</strong></div>
            <div style="color:#58a6ff;">|</div>
            <div>Audit Date: <strong style="color:#ffffff;">{TODAY_STR}</strong></div>
        </div>
    """, unsafe_allow_html=True)
    
    ts_key = f"capex_ts_{active_sector}"
    if ts_key not in st.session_state:
        st.session_state[ts_key] = f"{TODAY_STR} 00:00 UTC"
        
    # ---------------------------------------------------------
    # DUAL-RECORD QUICK-CALIBRATOR
    # ---------------------------------------------------------
    with st.container(border=True):
        qc1, qc2, qc3 = st.columns([2, 1, 1])
        with qc1:
            st.markdown(f"""
                <div style="font-size: 1.05rem; color: #c9d1d9; margin-bottom: 6px;">
                    Public Regulatory Baseline: <strong style="color:#ffffff; font-size:1.15rem;">{curr_sym}{sector['asset_cap']:,}</strong> 
                    <span style="color:#58a6ff; font-weight:600;">({sector['baseline_docket']} | {sector['baseline_date']})</span>
                </div>
            """, unsafe_allow_html=True)
            
            raw_input_str = st.text_input(
                "Chairman Quick-Calibrator: Enter Project Budget / CapEx at Risk:",
                value=f"{st.session_state[calib_key]:,}"
            )
            parsed_capex = int(re.sub(r"[^\d]", "", raw_input_str) or sector["asset_cap"])
            
            if parsed_capex != st.session_state[calib_key]:
                now_str = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
                st.session_state[calib_key] = parsed_capex
                st.session_state[ts_key] = now_str
                seal_active_package(active_inc)
                append_to_active_package(
                    active_inc,
                    f"JOB-{len(active_inc.get('audit_packages', []))+1:03d}: CapEx Re-Calibration to {curr_sym}{parsed_capex:,}",
                    f"Chairman recalibrated CapEx to {curr_sym}{parsed_capex:,} (Delta: {curr_sym}{parsed_capex - sector['asset_cap']:,}). Pipeline dynamically scaled.",
                    force_new_package=True
                )
                st.rerun()

            is_overridden = parsed_capex != sector["asset_cap"]
            badge_color = "#e3b341" if is_overridden else "#58a6ff"
            badge_label = "EXECUTIVE OVERRIDE ACTIVE" if is_overridden else "PUBLIC BASELINE SYNCHRONIZED"
            st.markdown(f"""
                <div style="margin-top:8px; display:flex; flex-direction:column; gap:4px;">
                    <div style="font-family:ui-monospace, monospace; font-size:2.3rem; font-weight:800; color:{badge_color};">{curr_sym}{parsed_capex:,}</div>
                    <div style="font-size:1.05rem; font-weight:700; color:{badge_color};">
                        ● {badge_label} <span style="color:#ffffff; font-weight:600;">(Effective: {st.session_state[ts_key]})</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        calibrated_toll_gate = max(25000, int(round(parsed_capex * 0.00085, -3)))

        with qc2:
            if is_resolved:
                st.markdown(f"""
                    <div style="background-color:rgba(46,160,67,0.18); border:2px solid #2ea043; padding:14px; border-radius:8px; text-align:center; min-height:115px; display:flex; flex-direction:column; justify-content:center;">
                        <div style="color:#3fb950; font-size:0.9rem; font-weight:700; text-transform:uppercase;">🟢 Toll-Gate Fee Due</div>
                        <div style="color:#ffffff; font-family:monospace; font-size:1.75rem; font-weight:800; margin-top:4px;">{curr_sym}{calibrated_toll_gate:,}</div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div class="exec-metric-card">
                        <div class="exec-metric-label">Toll-Gate Fee (Milestone)</div>
                        <div class="exec-metric-val">{curr_sym}{calibrated_toll_gate:,}</div>
                        <div class="exec-metric-sub" style="color:#3fb950;">↑ 0.085% CapEx Escrow</div>
                    </div>
                """, unsafe_allow_html=True)
                
        with qc3:
            if is_resolved:
                st.markdown("""
                    <div style="background-color:rgba(46,160,67,0.18); border:2px solid #2ea043; padding:14px; border-radius:8px; text-align:center; min-height:115px; display:flex; flex-direction:column; justify-content:center;">
                        <div style="color:#3fb950; font-size:0.9rem; font-weight:700; text-transform:uppercase;">✅ BJR Shield Status</div>
                        <div style="color:#ffffff; font-family:monospace; font-size:1.45rem; font-weight:800; margin-top:6px;">AWAITING WIRE</div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div class="exec-metric-card">
                        <div class="exec-metric-label">Live Session Window</div>
                        <div class="exec-metric-val">09:42</div>
                        <div class="exec-metric-sub" style="color:#3fb950;">↑ Zero-Retention Enforced</div>
                    </div>
                """, unsafe_allow_html=True)

    # ---------------------------------------------------------
    # MAIN TRUNK: HIGH-VISIBILITY FINANCIAL READOUT
    # ---------------------------------------------------------
    active_incidents = [i for i in sector["incidents"].values() if i.get("status") != "RESOLVED"]
    total_burn_day = sum(int(round(i.get("base_daily_bleed", 50000) * scale_factor)) for i in active_incidents)
    total_burn_wk = total_burn_day * 7
    dynamic_crossover_days = round(parsed_capex / total_burn_day, 1) if total_burn_day > 0 else 999.9

    k1, k2, k3 = st.columns(3)
    with k1:
        st.markdown(f"""
            <div class="exec-metric-card">
                <div class="exec-metric-label">Portfolio Holding Burn ({TODAY_STR})</div>
                <div class="exec-metric-val" style="color:#f85149;">{curr_sym}{total_burn_wk:,.0f} <span style="font-size:1.05rem; font-weight:600; color:#c9d1d9;">/ wk</span></div>
                <div class="exec-metric-sub" style="color:#f85149; font-family:monospace; font-size:1.05rem;">↑ {curr_sym}{total_burn_day:,.0f} / Day</div>
            </div>
        """, unsafe_allow_html=True)
    with k2:
        st.markdown(f"""
            <div class="exec-metric-card">
                <div class="exec-metric-label">Capital Under Defense</div>
                <div class="exec-metric-val">{curr_sym}{parsed_capex:,.0f}</div>
                <div class="exec-metric-sub" style="color:#3fb950; font-size:1.05rem;">↑ Asset Defense Escrow Intact</div>
            </div>
        """, unsafe_allow_html=True)
    with k3:
        st.markdown(f"""
            <div class="exec-metric-card">
                <div class="exec-metric-label">Active Block: {st.session_state.selected_incident_id}</div>
                <div class="exec-metric-val" style="color:#e3b341;">{dynamic_crossover_days} <span style="font-size:1.05rem; font-weight:600; color:#c9d1d9;">Days</span></div>
                <div class="exec-metric-sub" style="color:#e3b341; font-size:1.05rem;">↑ Crossover to Total Loss</div>
            </div>
        """, unsafe_allow_html=True)

    # ---------------------------------------------------------
    # INSTANT AGENT DIAGNOSTIC CONFERENCE
    # ---------------------------------------------------------
    with st.container(border=True):
        st.markdown("### 🎙️ Instant Diagnostic Agent Conference")
        st.caption("Interrogate domain agents to diagnose root friction without micromanaging field physics.")
        
        diag_col1, diag_col2, diag_col3 = st.columns([1, 1, 2])
        with diag_col1:
            if st.button("🚨 1. Why is the Fix Stalled?", use_container_width=True, type="primary" if st.session_state.conference_focus == "WHY_STALLED" else "secondary"):
                st.session_state.conference_focus = "WHY_STALLED"
                append_to_active_package(active_inc, "DIAGNOSTIC", "Chairman inquiry: Why is the fix stalled?")
                st.rerun()
        with diag_col2:
            if st.button("🟢 2. What Unblocks the Gate?", use_container_width=True, type="primary" if st.session_state.conference_focus == "WHAT_UNBLOCKS" else "secondary"):
                st.session_state.conference_focus = "WHAT_UNBLOCKS"
                append_to_active_package(active_inc, "DIAGNOSTIC", "Chairman inquiry: What unblocks the gate?")
                st.rerun()
        with diag_col3:
            custom_query = st.text_input("3. Type Interrogation Query:", placeholder="Type query to interrogate agent engine...", label_visibility="collapsed")
            if custom_query:
                st.session_state.conference_focus = "CUSTOM"
                st.session_state.custom_query_text = custom_query
                append_to_active_package(active_inc, "DIAGNOSTIC", f"Custom inquiry: '{custom_query}'")
            
        st.markdown("---")
        if st.session_state.conference_focus == "WHY_STALLED":
            st.markdown(
                f"🔴 **Master Orchestrator ➔ Site Telemetry Agent:** *'Inquire status on {st.session_state.selected_incident_id}. Why is the gate blocked on {TODAY_STR}?'*\n\n"
                f"🔴 **Site Telemetry Agent:** *'Permian HV crew is staged on site. However, the OEM field supervisor is withholding physical access to the relay cabinet pending written corporate indemnity under Clause 14.b. Mechanical physics are nominal (THD at 4.1%); access is legally blocked, bleeding {curr_sym}{total_burn_day:,.0f} / Day.'*"
            )
        elif st.session_state.conference_focus == "WHAT_UNBLOCKS":
            st.markdown(
                "🟢 **Master Orchestrator ➔ Fiduciary Shield Agent:** *'What specific instrument unblocks the gate immediately?'*\n\n"
                f"🟢 **Fiduciary Shield Agent:** *'A Board Resolution (Option A) executing a Directorate Indemnity Carve-Out from the {curr_sym}{parsed_capex:,} Capital Under Defense absorbs all warranty liability at the board level. This clears the GM to execute the IEEE 2800 sign-off within 5 minutes.'*"
            )
        elif st.session_state.conference_focus == "CUSTOM":
            st.markdown(f"🔍 **Agent Synthesis for Query: '{st.session_state.get('custom_query_text', '')}'**")
            st.info(f"Cross-referencing telemetry logs against {sector['statute']}. Field physics nominal. Primary bottleneck remains contractual signatory deadlock on {st.session_state.selected_incident_id}.")
        else:
            st.markdown(
                f"⚡ **Active Conference Synthesis ({TODAY_STR}):** Interrogating **Site Telemetry Agent** and **Fiduciary Shield Agent** for **{st.session_state.selected_incident_id}**. "
                f"Physical sweep is at 75% progress. Select an action above to diagnose root cause or command the GM carve-out."
            )

    # ---------------------------------------------------------
    # REMEDIAL LEVERS
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
                        active_inc["base_daily_bleed"] = 0
                        wo = active_inc.get("tier3_work_order", {})
                        wo["progress_pct"] = 100
                        for s in wo.get("steps", []):
                            s["done"] = True
                        append_to_active_package(
                            active_inc,
                            "REMEDIAL EXECUTION",
                            f"CHAIRMAN DIRECTIVE: Option A executed. Holding burn halted to 0. BJR safe harbor enforced."
                        )
                        st.session_state.conference_focus = "DEFAULT"
                        st.success("Option A Executed. Holding burn halted to 0.")
                        st.rerun()
                elif "Option B" in st.session_state.remedial_simulation:
                    if st.button("Authorize $35k Capital Draw", use_container_width=True):
                        append_to_active_package(active_inc, "CAPITAL DRAW", "Secondary crew mobilized ($35k draw).")
                        st.success("Capital Released.")
                        st.rerun()
                else:
                    st.button("Option Inadmissible", use_container_width=True, disabled=True)
            else:
                if st.button(f"⚡ Settle Milestone Fee ({curr_sym}{calibrated_toll_gate:,})", use_container_width=True, type="primary"):
                    seal_active_package(active_inc)
                    st.success("Milestone Settled. Audit Capsule Sealed. Ready to unlock INC-002.")

    # ---------------------------------------------------------
    # BRANCH CARDS
    # ---------------------------------------------------------
    b_col1, b_col2, b_col3 = st.columns(3)

    def render_branch_card(title, domain, director_name, agent_name, status_badge, metric_txt, card_type):
        border_col = "#2ea043" if card_type == "green" else ("#e3b341" if card_type == "amber" else "#da3633")
        bg_col = "rgba(46, 160, 67, 0.18)" if card_type == "green" else ("rgba(227, 179, 65, 0.18)" if card_type == "amber" else "rgba(218, 54, 51, 0.18)")
        
        return f"""
        <div style="background-color: {bg_col}; border: 2px solid {border_col}; border-radius: 8px; padding: 22px; height: 100%; display: flex; flex-direction: column; gap: 14px;">
            <h3 style="margin:0; color:#ffffff; font-size:1.4rem; font-weight:800;">{title}</h3>
            <div style="color:#ffffff; font-size:1.15rem; font-weight:700; border-bottom: 1px solid #30363d; padding-bottom: 10px; margin-bottom: 4px;">
                {domain}
            </div>
            <div style="font-size:1.0rem; color:#c9d1d9;">
                Cognizant Director: <br>
                <strong style="color:#ffffff; font-size:1.3rem; display:inline-block; margin-top:4px;">{director_name}</strong>
            </div>
            <div style="font-size:1.0rem; color:#c9d1d9;">
                Embedded Agent: <br>
                <code style="color:#a5d6ff; background:rgba(56,139,253,0.25); padding:4px 8px; font-size:1.0rem; border-radius:4px; display:inline-block; margin-top:4px;">{agent_name}</code>
            </div>
            <div style="font-weight:700; font-size:1.2rem; padding: 14px 16px; background: rgba(0,0,0,0.4); border-radius: 6px; border-left: 6px solid {border_col}; color:#ffffff; margin-top:4px;">
                {status_badge}
            </div>
            <div style="font-family:ui-monospace, monospace; color:#ffffff; font-size:1.1rem; font-weight:600; margin-top: auto; padding-top: 10px;">
                {metric_txt}
            </div>
        </div>
        """

    with b_col1:
        c_type = "green" if is_resolved else "red"
        s_badge = "🟢 CLEARED: Field access granted." if is_resolved else "🔴 OUTSTANDING: Field access locked."
        wo_id = active_inc.get("tier3_work_order", {}).get("id", "N/A")
        wo_pct = 100 if is_resolved else active_inc.get("tier3_work_order", {}).get("progress_pct", 0)
        st.markdown(render_branch_card("Branch 1: Physical / Field", "Hardware Gate | Plant & Crews", active_inc.get("director_seat", "Technical Integrity"), "Site Telemetry Agent", s_badge, f"Work Order: {wo_id} ({wo_pct}%)", c_type), unsafe_allow_html=True)

    with b_col2:
        c_type = "green" if is_resolved else "amber"
        s_badge = "🟢 CLEARED: Grid filing secured." if is_resolved else "🟡 COLLATERAL: 48h Window Expiring."
        st.markdown(render_branch_card("Branch 2: Regulatory / Market", "Commercial Gate | Interconnection", "David Chen (Proxy)", "Market Surveillance Agent", s_badge, "Handshake Status: Latency Validated", c_type), unsafe_allow_html=True)

    with b_col3:
        c_type = "green" if is_resolved else "red"
        s_badge = "🟢 CLEARED: Capital defended." if is_resolved else f"🔴 OUTSTANDING: Crossover in {dynamic_crossover_days}d."
        vel_txt = f"Bleed: {curr_sym}0 / Day" if is_resolved else f"Bleed: {curr_sym}{total_burn_day:,.0f} / Day"
        st.markdown(render_branch_card("Branch 3: Fiduciary / Capital", "Balance Sheet Gate | Liability Escrow", "Executive Board Chair", "Fiduciary Shield Agent", s_badge, vel_txt, c_type), unsafe_allow_html=True)

    # ---------------------------------------------------------
    # GATED INCIDENT PIPELINE (HIGH-CONTRAST / DAYS & WEEKS)
    # ---------------------------------------------------------
    with st.container(border=True):
        st.markdown("### 🔒 Gated Incident Pipeline (Next 4 Bottlenecks)")
        st.caption("Sequential project bottlenecks locked behind Milestone fee settlement. Dynamically scaled to Chairman CapEx:")

        p1, p2, p3, p4 = st.columns(4)

        def render_pipeline_card(num_title, raw_bleed, inc_code, is_threat):
            border = "#e3b341" if is_threat else "#30363d"
            bg = "rgba(227, 179, 65, 0.16)" if is_threat else "#161b22"
            status_txt = "🟡 ACTIVE THREAT" if is_threat else "🔒 QUEUED"
            status_color = "#e3b341" if is_threat else "#c9d1d9"
            
            scaled_daily = int(round(raw_bleed * scale_factor))
            scaled_weekly = scaled_daily * 7
            crossover_days = round(parsed_capex / scaled_daily, 1) if scaled_daily > 0 else 999.9
            
            return f"""
            <div style="background-color:{bg}; border:2px solid {border}; border-radius:8px; padding:18px; height:100%; display:flex; flex-direction:column; text-align:center;">
                <div style="font-weight:700; font-size:1.15rem; color:#ffffff; margin-bottom:8px;">{num_title}</div>
                <div style="font-family:ui-monospace, monospace; font-size:1.7rem; font-weight:800; color:#ffffff; margin: 4px 0;">
                    {curr_sym}{scaled_daily:,} <span style="font-size:1.0rem; font-weight:600; color:#c9d1d9;">/ Day</span>
                </div>
                <div style="font-size:0.95rem; font-weight:600; color:#c9d1d9; margin-bottom:6px;">
                    Weekly Burn: {curr_sym}{scaled_weekly:,} / Wk
                </div>
                <div style="font-size:1.05rem; font-weight:700; color:#e3b341; margin-bottom:14px;">
                    Horizon: {crossover_days} Days
                </div>
                <div style="font-size:1.0rem; font-weight:700; color:{status_color}; margin-top:auto;">
                    {status_txt}: {inc_code}
                </div>
            </div>
            """

        pipe_keys = [k for k in sector["incidents"].keys() if k not in ["INC-001", "DB-ETCS-01", "TEPCO-500KV-01"]]
        with p1:
            inc_p1 = sector["incidents"].get(pipe_keys[0], {})
            st.markdown(render_pipeline_card("1. Inrush Damping", inc_p1.get("base_daily_bleed", 38880), pipe_keys[0], is_resolved), unsafe_allow_html=True)
        with p2:
            inc_p2 = sector["incidents"].get(pipe_keys[1], {})
            st.markdown(render_pipeline_card("2. SCADA IEC 61850", inc_p2.get("base_daily_bleed", 15552), pipe_keys[1], False), unsafe_allow_html=True)
        with p3:
            inc_p3 = sector["incidents"].get(pipe_keys[2], {})
            st.markdown(render_pipeline_card("3. BESS Firmware OTA", inc_p3.get("base_daily_bleed", 4320), pipe_keys[2], False), unsafe_allow_html=True)
        with p4:
            inc_p4 = sector["incidents"].get(pipe_keys[3], {})
            st.markdown(render_pipeline_card("4. Substation Oil DGA", inc_p4.get("base_daily_bleed", 6912), pipe_keys[3], False), unsafe_allow_html=True)

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
                st.markdown(f"**Status:** <span style='color:{status_color}; font-weight:bold; font-size:1.1rem;'>{pkg['status']}</span>", unsafe_allow_html=True)
                for entry in pkg.get("entries", []):
                    st.markdown(f"<div style='font-size:1.05rem; font-family:monospace; margin:4px 0; color:#f0f6fc;'>• {entry}</div>", unsafe_allow_html=True)

# =========================================================
# TIER 3 & DIRECTOR VIEWS
# =========================================================
elif selected_role == "Tier 3: Site Operations / Field Lead":
    st.title("Tier 3 | Site Operations & Field Execution Desk")
    wo = active_inc.get("tier3_work_order", {})
    t1, t2, t3 = st.columns(3)
    t1.metric("Work Order", wo.get("id", "N/A"), active_inc.get("priority", "CRITICAL"))
    t2.metric("Target Gate", "Check #6 (COD Attestation)")
    t3.metric("Progress", f"{wo.get('progress_pct', 0)}%")
    if not is_resolved and st.button("Complete Final PE Verification Stamp", use_container_width=True, type="primary"):
        wo["progress_pct"] = 100
        active_inc["status"] = "RESOLVED"
        append_to_active_package(active_inc, "FIELD VERIFICATION", "TIER 3 FIELD STAMP: Telemetry validated on-site. Burn halted.")
        st.success("Stamped & Transmitted.")
        st.rerun()
else:
    dir_name = selected_role.replace("Director: ", "")
    st.title(f"Directorate Oversight: {dir_name}")
    st.metric("Jurisdiction Status", active_inc.get("status", "DEADLOCKED"), active_inc.get("priority", "P1"))
    if not is_resolved and st.button("Issue Directorate Formal Concurrence", use_container_width=True):
        append_to_active_package(active_inc, "DIRECTOR CONCURRENCE", f"Formal concurrence issued by {dir_name}.")
        st.success("Concurrence sealed to active job package.")
        st.rerun()

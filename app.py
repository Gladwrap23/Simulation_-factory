import datetime
import hashlib
import json
import re
import streamlit as st

APP_BUILD_ID = "v5.8_purged_duplicate_sidebar_sep17_2026"

if st.session_state.get("build_id") != APP_BUILD_ID:
    st.session_state.clear()
    st.session_state["build_id"] = APP_BUILD_ID

st.set_page_config(
    page_title="Autonomous Capital Defense | Forensic Claims Engine",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# 1. INDUSTRIAL STYLING & MOBILE RESPONSIVENESS
# =========================================================
st.markdown("""
    <style>
        .stApp { 
            background-color: #0d1117; 
            color: #f0f6fc; 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; 
        }
        
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
        
        .capex-throttle div[data-testid="stTextInput"] input,
        .capex-throttle input[type="text"] {
            font-size: 2.8rem !important;
            font-weight: 900 !important;
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace !important;
            color: #ff4b4b !important;
            background-color: #090d13 !important;
            border: 2px solid #58a6ff !important;
            border-radius: 8px !important;
            padding: 16px 18px !important;
            text-align: center !important;
            box-shadow: 0 0 16px rgba(88, 166, 255, 0.25) !important;
            height: auto !important;
        }
        
        div[data-testid="stButton"] button {
            white-space: normal !important;
            word-break: break-word !important;
            height: auto !important;
            min-height: 48px !important;
            padding: 12px 18px !important;
            line-height: 1.35 !important;
            font-size: 1.1rem !important;
            font-weight: 800 !important;
            border-radius: 8px !important;
        }
        
        /* DEDICATED FULL-WIDTH TAP TO HALT BUTTON */
        .tap-to-halt-container button {
            background-color: #da3633 !important;
            color: #ffffff !important;
            border: 2px solid #f85149 !important;
            font-size: 1.35rem !important;
            font-weight: 900 !important;
            letter-spacing: 0.04em !important;
            padding: 18px 24px !important;
            box-shadow: 0 0 24px rgba(218, 54, 51, 0.55) !important;
            border-radius: 8px !important;
        }
        .tap-to-halt-container button:hover {
            background-color: #b62324 !important;
            border-color: #ff7b72 !important;
            box-shadow: 0 0 30px rgba(255, 75, 75, 0.8) !important;
        }

        .sidebar-brand-card {
            background: linear-gradient(180deg, rgba(88, 166, 255, 0.14) 0%, rgba(22, 27, 34, 0.9) 100%);
            border: 1px solid #388bfd;
            border-radius: 8px;
            padding: 14px 16px;
            margin-bottom: 16px;
        }

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
            min-height: 110px;
        }
        .exec-metric-card-secondary {
            background-color: #11151c;
            border: 1px solid #21262d;
            border-radius: 6px;
            padding: 10px 14px;
            text-align: center;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            min-height: 80px;
        }
        .circuit-breaker-card {
            background-color: rgba(248, 81, 73, 0.12);
            border: 2px solid #f85149;
            border-radius: 8px;
            padding: 14px 16px;
            text-align: center;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            min-height: 110px;
        }
        .circuit-defended-card {
            background-color: rgba(46, 160, 67, 0.15);
            border: 2px solid #2ea043;
            border-radius: 8px;
            padding: 14px 16px;
            text-align: center;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            min-height: 110px;
        }
        .claim-demand-card {
            background-color: rgba(227, 179, 65, 0.12);
            border: 2px solid #e3b341;
            border-radius: 8px;
            padding: 14px 16px;
            text-align: center;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            min-height: 110px;
        }
        .exec-metric-label {
            color: #e6edf3;
            font-size: 0.85rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 4px;
        }
        .exec-metric-val {
            color: #ffffff;
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
            font-size: 1.85rem;
            font-weight: 800;
            line-height: 1.15;
        }
        .exec-metric-val-secondary {
            color: #ffffff;
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
            font-size: 1.3rem;
            font-weight: 700;
            line-height: 1.15;
        }
        .exec-metric-sub {
            font-size: 0.9rem;
            font-weight: 700;
            margin-top: 4px;
        }
        
        .legal-document-box {
            background-color: #0d1117;
            border: 2px solid #30363d;
            border-left: 6px solid #58a6ff;
            border-radius: 6px;
            padding: 18px 20px;
            font-family: Georgia, Cambria, "Times New Roman", Times, serif;
            color: #e6edf3;
            line-height: 1.7;
        }
        .legal-header {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-size: 0.95rem;
            font-weight: 800;
            color: #58a6ff;
            margin-bottom: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# =========================================================
# 2. LOCALIZATION DICTIONARY & UNIFIED TIER HIERARCHY
# =========================================================
I18N = {
    "English [USA · UK · Australia]": {
        "tier1_title": "Tier 1 | Chairman Tactical Command Post (Part One)",
        "tier2_title": "Tier 2 | Directorate Governance Desk",
        "tier3_title": "Tier 3 | Site Operations & Operator Remediation Desk",
        "tier4_title": "Tier 4 | Forensic Cost Recovery Vault (Part Two)",
        "sub_app": "Autonomous Capital Defense & Forensic Claims Engine",
        "calib_red_header": "COMMAND GATEWAY: ENTER NEW PROJECT BUDGET / CAPEX AT RISK (TAP TO RE-CALIBRATE)",
        "override_active": "EXECUTIVE OVERRIDE ACTIVE",
        "baseline_synced": "PUBLIC BASELINE SYNCHRONIZED",
        "toll_fee": "Toll-Gate Fee (Milestone)",
        "escrow_desc": "↑ 0.085% CapEx Escrow",
        "session_window": "Live Session Window",
        "session_desc": "↑ Cryptographic Epoch Active",
        "holding_burn": "Portfolio Holding Burn",
        "cap_under_def": "Capital Under Defense",
        "active_block": "Active Block",
        "crossover_sub": "↑ Crossover to Total Loss",
        "tap_to_halt_btn": "🛑 TAP TO HALT (PRESS TO ACTIVATE)",
        "tap_to_halt_desc": "Executing this directive issues an emergency Directorate Hold-Harmless Resolution under statute (Delaware DGCL § 141). It absorbs 100% of warranty liability from the Lead PE onto the corporate balance sheet, authorizes immediate transmission of the digital PE stamp, and halts daily burn to $0.",
        "circuit_defended": "🟢 CAPITAL DEFENDED — HOLDING BLEED: $0 / DAY",
        "why_stalled": "🚨 1. Why is the Fix Stalled?",
        "what_unblocks": "🟢 2. What Document Unblocks the Gate?",
        "interrogate_hint": "Type query to interrogate agents...",
        "branches_title": "The Three Cascading Branches & Remedial Levers",
        "pipeline_title": "🔒 Forward Incident Pipeline (Next 4 Bottlenecks)",
        "claim_total_label": "Direct Liquidated Claim Due",
        "claim_sub": "↑ Reimbursable under Schedule D",
        "audit_title": "Tier 4 | Sealed Cryptographic Job Packages"
    }
}

TODAY_STR = "16 Sep 2026"

SECTORS = {
    "ERCOT BESS / Grid Storage (USA)": {
        "currency": "$",
        "asset_cap": 88_500_000,
        "baseline_docket": "ERCOT IA § 4.2 Interconnection Docket #54219",
        "baseline_date": "16 Sep 2026",
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
                "days_in_deadlock": 7,
                "status": "DEADLOCKED",
                "director_seat": "Dr. Arthur Pendleton",
                "director_signed": False,
                "manual_pe_bypass": False,
                "counterparty": {
                    "name": "Apex Power Conversion Systems Corp (OEM)",
                    "contract": "Turnkey EPC & Inverter Supply Agreement #TX-9011",
                    "clause_invoked": "Clause 14.b (Inverter Warranty Voidance Disclaimer)",
                    "breach_clause": "Schedule D § 3 (Unexcused Commissioning Demurrage)"
                },
                "tier3_work_order": {
                    "id": "WO-8821-HARMONIC",
                    "title": "On-Site IEEE 2800 Harmonic Sweep & Attestation",
                    "target_gate": "Check #6 (COD Attestation Gate)",
                    "contractor": "Permian HV Field Services LLC",
                    "field_lead": "Marcus Vance, PE",
                    "progress_pct": 75,
                    "plain_english_trap": {
                        "headline": "🚨 Why the Fix is Blocked (Plain English):",
                        "who_blocks": "Marcus Vance, PE (Lead Engineer) refuses to sign off on Step 4.",
                        "reason": "Apex (Inverter OEM) is threatening to void the plant's multi-million dollar warranty under Clause 14.b if anyone touches the inverter cabinets without their off-site supervisor present.",
                        "consequence": "Signing without protection leaves Marcus personally liable and risks voiding the plant warranty. Not signing burns $87,264 every day.",
                        "fix": "Clicking the button executes the Board Indemnity Instrument (Delaware DGCL § 141(e)). This absorbs all liability onto the company balance sheet, legally protects Marcus Vance, and submits his digital PE stamp to ERCOT immediately."
                    },
                    "steps": [
                        {"task": "Rack 4 PE Calibration & Neutral Grounding Sweep", "done": True, "evidence": "Calibration log #PER-409 PASS (Exhibit B-1)"},
                        {"task": "Inverter Bank 1-4 Sub-Cycle Injection Sweep", "done": True, "evidence": "THD 4.1% confirmed (< 5.0% threshold) (Exhibit A-1)"},
                        {"task": "Damping Resonance Pulse Verification", "done": True, "evidence": "Active damping ratio: 1.18 pu nominal (Exhibit A-2)"},
                        {"task": "PE Digital Stamp & Packet Submission", "done": False, "evidence": "Marcus Vance refuses sign-off pending Board Indemnity"}
                    ],
                    "telemetry": [
                        {"param": "THD Harmonics (IEEE 2800)", "val": "4.1%", "status": "NOMINAL", "limit": "< 5.0%"},
                        {"param": "Inrush Damping Ratio", "val": "1.18 pu", "status": "NOMINAL", "limit": "Trip: 1.40 pu"},
                        {"param": "Frequency Injection Stability", "val": "14.2 MW/0.1Hz", "status": "COMPLIANT", "limit": "ERCOT § 4.2"}
                    ]
                },
                "legal_instrument": {
                    "title": "DIRECTORATE INDEMNITY & STATUTORY HOLD-HARMLESS RESOLUTION",
                    "authority": "Delaware General Corporation Law (DGCL) § 141(e) & Company Bylaws Art. VIII",
                    "effective_date": "16 Sep 2026 00:00:00 UTC",
                    "recitals": [
                        "WHEREAS, Permian BESS Feeder 4A is sustaining a daily portfolio holding bleed of $87,264/day due to unexcused attestation deadlock under ERCOT Docket #54219;",
                        "WHEREAS, sub-cycle oscillography records (Exhibit A) prove inverter hardware operates within IEEE 2800 nominal standards (4.1% THD), refuting counterparty claims of external grid disturbance;",
                        "WHEREAS, Lead Professional Engineer Marcus Vance, PE is subject to contractual intimidation by Apex Power Conversion Systems under Clause 14.b warranty voidance threats;"
                    ],
                    "operative_resolution": (
                        "NOW, THEREFORE, BE IT RESOLVED: The Board of Directors hereby executes full corporate indemnification "
                        "and holds harmless Marcus Vance, PE and Permian HV Field Services LLC from all liability, claims, or damages "
                        "arising from the execution of Step 4 (PE Digital Attestation Stamp). The Corporation formally assumes full legal responsibility "
                        "for contested Clause 14.b claims and authorizes immediate bypass and grid energization."
                    ),
                    "signatories": [
                        {"role": "Chairman of the Board", "name": "Executive Chairman", "status": "EXECUTED & ATTESTED", "hash": "sha256:7b910e12d4a1"},
                        {"role": "Cognizant Technical Director", "name": "Dr. Arthur Pendleton", "status": "PENDING DIRECTOR COUNTERSIGNATURE", "hash": "sha256:f48a901c22e9"},
                        {"role": "Lead Professional Engineer", "name": "Marcus Vance, PE (TX Lic #114902)", "status": "HELD PENDING INDEMNITY", "hash": "sha256:1a8904df88b3"}
                    ]
                },
                "exhibits": [
                    {
                        "code": "EXHIBIT A-1",
                        "title": "IEEE COMTRADE Oscillography Binary Extract",
                        "filename": "ERCOT_FEEDER4A_FAULT_RECORDER_20260909_0814.DAT",
                        "size": "44.2 MB",
                        "sha256": "4b92cf88e1049ad08f12399cb1a40293ee019b882310b14c339a0ef28b123456",
                        "significance": "10 kHz digital fault recorder captures grid dip at 4.2%; proves ride-through compliance."
                    },
                    {
                        "code": "EXHIBIT B-1",
                        "title": "Site Security Turnstile Badge Database Extract",
                        "filename": "PERMIAN_BESS_GATE_ACCESS_LOGS_SEP09_2026.CSV",
                        "size": "1.8 MB",
                        "sha256": "91ab802eec8912b4501a39d889b7102ce094a318894cb10e4a77e9921004ab12",
                        "significance": "Proves Apex Commissioning Lead was off-site during trip sequence."
                    }
                ],
                "forensic_timeline": [
                    {"time": "2026-09-09 08:14:02.104 UTC", "party": "Grid Physics", "event": "Raw 10 kHz oscillography records grid voltage dip of 4.2%."},
                    {"time": "2026-09-09 08:14:02.118 UTC", "party": "Apex Inverter OEM", "event": "Inverter Bank 2 trips out prematurely due to threshold miscalibration."}
                ],
                "audit_packages": [
                    {
                        "job_id": "JOB-001: Statutory Ingestion Baseline",
                        "status": "SEALED & ATTESTED",
                        "sealed_at": "2026-09-16 00:00:00 UTC",
                        "package_hash": "8f3a9e01c4b72e1",
                        "entries": ["DOCKET INGESTION: Baseline verified against ERCOT Docket #54219."]
                    }
                ]
            },
            "INC-002": {"title": "Substation Step-Up Inrush Damping", "priority": "P2 - HIGH", "base_daily_bleed": 38880},
            "INC-003": {"title": "SCADA Protocol IEC 61850 Gateway", "priority": "P3 - MODERATE", "base_daily_bleed": 15552},
            "INC-004": {"title": "BESS Inverter Firmware OTA Patch", "priority": "P4 - MONITORED", "base_daily_bleed": 4320},
            "INC-005": {"title": "Substation Oil DGA Baseline Sweep", "priority": "P5 - MONITORED", "base_daily_bleed": 6912}
        }
    }
}

if "app_state" not in st.session_state:
    st.session_state.app_state = SECTORS

if "selected_incident_id" not in st.session_state:
    st.session_state.selected_incident_id = "INC-001"

if "conference_focus" not in st.session_state:
    st.session_state.conference_focus = "DEFAULT"

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

def execute_unified_circuit_breaker(incident: dict, statute: str, daily_bleed: float):
    incident["status"] = "RESOLVED"
    incident["director_signed"] = True
    incident["manual_pe_bypass"] = True
    incident["base_daily_bleed"] = 0
    wo = incident.get("tier3_work_order", {})
    wo["progress_pct"] = 100
    if wo.get("steps"):
        for s in wo["steps"]:
            s["done"] = True
    
    inst = incident.get("legal_instrument", {})
    for sig in inst.get("signatories", []):
        if "Director" in sig["role"]:
            sig["status"] = "COUNTERSIGNED & SEALED"
        elif "Engineer" in sig["role"]:
            sig["status"] = "DIGITAL STAMP TRANSMITTED"
            
    append_to_active_package(
        incident,
        f"JOB-{len(incident.get('audit_packages', []))+1:03d}: Unified Circuit Breaker Directive",
        f"UNIFIED EXECUTIVE DIRECTIVE: Faced with {daily_bleed:,.0f}/Day holding bleed, burn halted across all branches.",
        force_new_package=True
    )

def reset_incident_to_neutral(incident: dict):
    incident["status"] = "DEADLOCKED"
    incident["director_signed"] = False
    incident["manual_pe_bypass"] = False
    incident["base_daily_bleed"] = 87264
    wo = incident.get("tier3_work_order", {})
    wo["progress_pct"] = 75
    if wo.get("steps"):
        for s in wo["steps"][:-1]: s["done"] = True
        wo["steps"][-1]["done"] = False
        
    inst = incident.get("legal_instrument", {})
    for sig in inst.get("signatories", []):
        if "Director" in sig["role"]:
            sig["status"] = "PENDING DIRECTOR COUNTERSIGNATURE"
        elif "Engineer" in sig["role"]:
            sig["status"] = "HELD PENDING INDEMNITY"
            
    append_to_active_package(
        incident,
        f"JOB-{len(incident.get('audit_packages', []))+1:03d}: Neutral Counterfactual Reset",
        "Executive counterfactual reset executed.",
        force_new_package=True
    )

# =========================================================
# 3. SIDEBAR NAVIGATION: COMPLETE RESTORED LEFT PANEL
# =========================================================
with st.sidebar:
    st.markdown("""
        <div class="sidebar-brand-card">
            <div style="font-size: 1.15rem; font-weight: 900; color: #58a6ff; letter-spacing: 0.04em; text-transform: uppercase; line-height: 1.25;">
                ⚡ Autonomous Capital Defense
            </div>
            <div style="font-size: 0.95rem; font-weight: 700; color: #ffffff; margin-top: 4px;">
                Forensic Claims Engine
            </div>
            <div style="font-size: 0.8rem; color: #8b949e; margin-top: 6px; font-family: monospace;">
                Pactum Sovereign OS · Build v5.7
            </div>
        </div>
    """, unsafe_allow_html=True)
    t = I18N["English [USA · UK · Australia]"]
    
    active_sector = st.selectbox("Operating Book (Global Assets):", list(st.session_state.app_state.keys()))
    sector = st.session_state.app_state[active_sector]
    curr_sym = sector["currency"]

    st.selectbox(
        "Sovereign Legal Jurisdiction:",
        [
            "🇺🇸 ERCOT / Delaware (DGCL § 141)",
            "🇩🇪 EBA / Germany (AktG § 93)",
            "🇨🇱 CEN / Chile (Art. 72-1)",
            "🇫🇷 RTE / France (L225-251)",
            "🇯🇵 METI / Japan (Art. 423)"
        ]
    )
    
    calib_key = f"capex_override_{active_sector}"
    if calib_key not in st.session_state:
        st.session_state[calib_key] = int(sector["asset_cap"])
    current_calib_capex = st.session_state[calib_key]
    scale_factor = current_calib_capex / sector["asset_cap"]

    nav_options = [
        t["tier1_title"], 
        t["tier2_title"],
        t["tier3_title"],
        t["tier4_title"]
    ]
    
    if "selected_view" not in st.session_state or st.session_state.selected_view not in nav_options:
        st.session_state.selected_view = t["tier1_title"]

    selected_view = st.radio(
        "Chain of Command & Forensic Vault:",
        nav_options,
        index=nav_options.index(st.session_state.selected_view)
    )
    st.session_state.selected_view = selected_view
    
    # RESTORED: ACTIVE INCIDENT QUEUE ON LEFT PANEL
    st.divider()
    st.markdown("#### Active Incident Queue")
    for inc_key, inc_obj in sector["incidents"].items():
        is_sel = inc_key == st.session_state.selected_incident_id
        inc_daily = inc_obj.get("base_daily_bleed", 50000) * scale_factor
        inc_crossover = round(current_calib_capex / inc_daily, 1) if inc_daily > 0 else 999
        btn_label = f"{inc_obj.get('priority', 'P1')}: {inc_key}\n{inc_crossover}d Crossover"
        
        if st.button(btn_label, key=f"sb_{inc_key}", use_container_width=True, type="primary" if is_sel else "secondary"):
            st.session_state.selected_incident_id = inc_key
            st.session_state.conference_focus = "DEFAULT"
            st.session_state.selected_view = t["tier1_title"]
            st.rerun()

active_inc = sector["incidents"]["INC-001"]
is_resolved = active_inc.get("status") == "RESOLVED"
is_dir_signed = active_inc.get("director_signed", False) or is_resolved
is_bypassed = active_inc.get("manual_pe_bypass", False) or is_resolved

# =========================================================
# 4. VIEW: TIER 1 — CHAIRMAN TACTICAL COMMAND POST
# =========================================================
if selected_view == t["tier1_title"]:
    st.markdown("""
        <div style="background: #1f6feb; color: #ffffff; padding: 6px 12px; border-radius: 4px; font-weight: 800; font-size: 0.9rem; margin-bottom: 12px; text-align: center;">
            ⚡ ACTIVE BUILD: v5.8 | CLEAN SIDEBAR HIERARCHY (NO DUPLICATE ROSTER)
        </div>
    """, unsafe_allow_html=True)

    st.title(t["tier1_title"])
    
    if is_resolved:
        st.markdown(f"""
            <div style="background: rgba(46, 160, 67, 0.2); border: 2px solid #2ea043; border-radius: 8px; padding: 14px 18px; margin-bottom: 16px; display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <strong style="color: #3fb950; font-size: 1.15rem;">⚡ ATTESTATION CONFIRMED:</strong> 
                    <span style="color: #ffffff; font-size: 1.05rem; margin-left: 6px;">Lead PE digital stamp received. Holding burn halted to <strong>$0/day</strong>.</span>
                </div>
                <div style="color: #3fb950; font-weight: 800; font-size: 1.0rem;">SAFE HARBOR ACTIVE</div>
            </div>
        """, unsafe_allow_html=True)

    ts_key = f"capex_ts_{active_sector}"
    if ts_key not in st.session_state:
        st.session_state[ts_key] = f"{TODAY_STR} 00:00 UTC"
        
    with st.container(border=True):
        parsed_current_capex = st.session_state[calib_key]
        is_overridden = parsed_current_capex != sector["asset_cap"]
        badge_color = "#e3b341" if is_overridden else "#58a6ff"
        badge_label = t["override_active"] if is_overridden else t["baseline_synced"]
        
        st.markdown(f"""
            <div style="text-align: center; margin-bottom: 8px;">
                <div style="font-size: 1.05rem; font-weight: 700; color: #58a6ff; letter-spacing: 0.05em; text-transform: uppercase;">
                    ⚡ {active_sector} — {sector['baseline_docket']}
                </div>
                <div style="font-size: 1.05rem; color: #c9d1d9; margin: 6px 0;">
                    Statutory Baseline CapEx at Risk: <strong style="color:#ffffff; font-size:1.15rem;">{curr_sym}{sector['asset_cap']:,}</strong> 
                    <span style="color:#58a6ff;">(Effective: {sector['baseline_date']})</span>
                </div>
                <div style="margin-top: 4px; margin-bottom: 14px;">
                    <span style="font-size: 1.05rem; font-weight: 800; color: {badge_color};">
                        ● {badge_label}
                    </span>
                    <span style="color: #8b949e; font-size: 0.95rem; font-weight: 600; margin-left: 8px;">
                        (Effective Audit Timestamp: {st.session_state[ts_key]})
                    </span>
                </div>
                <div style="height: 1px; background: #30363d; margin: 12px 0 16px 0;"></div>
                <div style="color: #ff4b4b; font-size: 1.45rem; font-weight: 900; letter-spacing: 0.04em; text-transform: uppercase; line-height: 1.3;">
                    🚨 {t['calib_red_header']}
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="capex-throttle">', unsafe_allow_html=True)
        raw_input_str = st.text_input(
            label="Chairman Quick-Calibrator Input",
            value=f"{st.session_state[calib_key]:,}",
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        parsed_capex = int(re.sub(r"[^\d]", "", raw_input_str) or sector["asset_cap"])
        if parsed_capex != st.session_state[calib_key]:
            now_str = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
            st.session_state[calib_key] = parsed_capex
            st.session_state[ts_key] = now_str
            st.rerun()

    # PRIMARY 3-CARD LEVEL ROW (NO SQUEEZED BUTTONS)
    total_burn_day = 87264 * scale_factor if not is_resolved else 0
    total_burn_wk = total_burn_day * 7
    dynamic_crossover_days = round(parsed_capex / total_burn_day, 1) if total_burn_day > 0 else 999.9

    k1, k2, k3 = st.columns(3)
    with k1:
        if not is_resolved:
            st.markdown(f"""
                <div class="circuit-breaker-card">
                    <div class="exec-metric-label">{t['holding_burn']} ({TODAY_STR})</div>
                    <div class="exec-metric-val" style="color:#f85149;">{curr_sym}{total_burn_wk:,.0f} <span style="font-size:1.05rem; font-weight:600; color:#c9d1d9;">/ wk</span></div>
                    <div class="exec-metric-sub" style="color:#f85149; font-family:monospace; font-size:1.05rem;">↑ {curr_sym}{total_burn_day:,.0f} / Day</div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="circuit-defended-card">
                    <div class="exec-metric-label">{t['holding_burn']} ({TODAY_STR})</div>
                    <div class="exec-metric-val" style="color:#3fb950;">{curr_sym}0 <span style="font-size:1.05rem; font-weight:600; color:#c9d1d9;">/ wk</span></div>
                    <div class="exec-metric-sub" style="color:#3fb950; font-family:monospace; font-size:1.05rem;">{t['circuit_defended']}</div>
                </div>
            """, unsafe_allow_html=True)
                
    with k2:
        st.markdown(f"""
            <div class="exec-metric-card">
                <div class="exec-metric-label">{t['cap_under_def']}</div>
                <div class="exec-metric-val">{curr_sym}{parsed_capex:,.0f}</div>
                <div class="exec-metric-sub" style="color:#3fb950; font-size:1.05rem;">↑ Escrow Intact</div>
            </div>
        """, unsafe_allow_html=True)
        
    with k3:
        st.markdown(f"""
            <div class="exec-metric-card">
                <div class="exec-metric-label">{t['active_block']}: INC-001</div>
                <div class="exec-metric-val" style="color:#e3b341;">{dynamic_crossover_days} <span style="font-size:1.05rem; font-weight:600; color:#c9d1d9;">Days</span></div>
                <div class="exec-metric-sub" style="color:#e3b341; font-size:1.05rem;">{t['crossover_sub']}</div>
            </div>
        """, unsafe_allow_html=True)

    # SECONDARY ADMINISTRATIVE ROW
    calibrated_toll_gate = max(25000, int(round(parsed_capex * 0.00085, -3)))
    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
    sub1, sub2 = st.columns(2)
    with sub1:
        st.markdown(f"""
            <div class="exec-metric-card-secondary">
                <div class="exec-metric-label" style="font-size:0.8rem; margin-bottom:2px;">{t['toll_fee']}</div>
                <div class="exec-metric-val-secondary">{curr_sym}{calibrated_toll_gate:,}</div>
                <div style="color:#3fb950; font-size:0.85rem; font-weight:600;">{t['escrow_desc']}</div>
            </div>
        """, unsafe_allow_html=True)
    with sub2:
        st.markdown(f"""
            <div class="exec-metric-card-secondary">
                <div class="exec-metric-label" style="font-size:0.8rem; margin-bottom:2px;">{t['session_window']}</div>
                <div class="exec-metric-val-secondary">09:42</div>
                <div style="color:#3fb950; font-size:0.85rem; font-weight:600;">{t['session_desc']}</div>
            </div>
        """, unsafe_allow_html=True)

    # DIAGNOSTIC AGENT CONFERENCE
    st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("### 🎙️ Instant Diagnostic Agent Conference")
        diag_col1, diag_col2, diag_col3 = st.columns([1, 1, 2])
        with diag_col1:
            if st.button(t["why_stalled"], use_container_width=True, type="primary" if st.session_state.conference_focus == "WHY_STALLED" else "secondary"):
                st.session_state.conference_focus = "WHY_STALLED"
                st.rerun()
        with diag_col2:
            if st.button(t["what_unblocks"], use_container_width=True, type="primary" if st.session_state.conference_focus == "WHAT_UNBLOCKS" else "secondary"):
                st.session_state.conference_focus = "WHAT_UNBLOCKS"
                st.rerun()
        with diag_col3:
            custom_query = st.text_input("3. Custom Interrogation Query", placeholder=t["interrogate_hint"], label_visibility="collapsed")
            if custom_query:
                st.session_state.conference_focus = "CUSTOM"
                st.session_state.custom_query_text = custom_query
            
        st.markdown("---")
        if st.session_state.conference_focus == "WHY_STALLED":
            st.markdown("🔴 **Telemetry Agent:** *'Physical telemetry is nominal (THD 4.1% < 5.0%). Marcus Vance refuses sign-off because Apex OEM threatens warranty cancellation under Clause 14.b. Site deadlock is contractual, not physical.'*")
        elif st.session_state.conference_focus == "WHAT_UNBLOCKS":
            inst = active_inc.get("legal_instrument", {})
            st.markdown(f"🟢 **Fiduciary Shield Agent:** *'The **{inst.get('title', 'Board Resolution')}** pursuant to **{sector['statute']}**.'*")
        else:
            st.markdown(f"⚡ **Active Interrogation Standby ({TODAY_STR}):** Agents synchronized with {sector['statute']}. Select an action above or tap the Holding Burn Circuit Breaker below to halt exposure.")

    # =========================================================
    # RELOCATED CIRCUIT BREAKER: DIRECTLY BELOW DIAGNOSTIC AGENT
    # =========================================================
    st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)
    with st.container(border=True):
        if not is_resolved:
            st.markdown(f"""
                <div style="background: rgba(248, 81, 73, 0.12); border: 2px solid #f85149; border-radius: 8px; padding: 18px 20px; margin-bottom: 14px;">
                    <div style="color: #f85149; font-weight: 900; font-size: 1.25rem; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.04em;">
                        ⚡ HOLDING BURN CIRCUIT BREAKER
                    </div>
                    <div style="color: #f0f6fc; font-size: 1.05rem; line-height: 1.6;">
                        {t['tap_to_halt_desc']}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown('<div class="tap-to-halt-container">', unsafe_allow_html=True)
            if st.button(t['tap_to_halt_btn'], use_container_width=True):
                execute_unified_circuit_breaker(active_inc, sector["statute"], total_burn_day)
                st.session_state.conference_focus = "DEFAULT"
                st.success("Executive directive executed. Capital defended across all branches.")
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div style="background: rgba(46, 160, 67, 0.15); border: 2px solid #2ea043; border-radius: 8px; padding: 18px 20px; text-align: center; margin-bottom: 10px;">
                    <div style="color: #3fb950; font-weight: 900; font-size: 1.35rem; margin-bottom: 6px;">
                        {t['circuit_defended']}
                    </div>
                    <div style="color: #f0f6fc; font-size: 1.05rem;">
                        Directive is sealed. Lead PE Marcus Vance is protected under Delaware DGCL § 141. Work order completed at 100%.
                    </div>
                </div>
            """, unsafe_allow_html=True)
            if st.button("↩️ Revert to Neutral (Simulate Exposure)", use_container_width=True):
                reset_incident_to_neutral(active_inc)
                st.rerun()

    # THE THREE CASCADING BRANCHES
    st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)
    st.markdown(f"### {t['branches_title']}")
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
        st.markdown(render_branch_card("Branch 1: Physical / Field", "Hardware Gate | Plant & Crews", "Dr. Arthur Pendleton", "Site Telemetry Agent", s_badge, "Work Order: WO-8821-HARMONIC", c_type), unsafe_allow_html=True)
    with b_col2:
        c_type = "green" if is_resolved else "amber"
        s_badge = "🟢 CLEARED: Grid filing secured." if is_resolved else "🟡 COLLATERAL: 48h Window Expiring."
        st.markdown(render_branch_card("Branch 2: Regulatory / Market", "Commercial Gate | Interconnection", "David Chen (Proxy)", "Market Surveillance Agent", s_badge, "Handshake Status: Latency Validated", c_type), unsafe_allow_html=True)
    with b_col3:
        c_type = "green" if is_resolved else "red"
        s_badge = "🟢 CLEARED: Capital defended." if is_resolved else f"🔴 OUTSTANDING: Crossover in {dynamic_crossover_days}d."
        vel_txt = "Bleed: $0 / Day" if is_resolved else f"Bleed: ${total_burn_day:,.0f} / Day"
        st.markdown(render_branch_card("Branch 3: Fiduciary / Capital", "Balance Sheet Gate | Liability Escrow", "Executive Board Chair", "Fiduciary Shield Agent", s_badge, vel_txt, c_type), unsafe_allow_html=True)

    # OPERATIONAL CHAIN OF COMMAND
    st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)
    st.markdown("### 📡 Operational Chain of Command (Single-Line Descending Hierarchy)")
    st.caption("Inspect and drill directly into Directorate governance and Tier 3 field desks:")
    
    with st.container(border=True):
        st.markdown(f"""
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px;">
                <div>
                    <div style="font-weight:800; color:#58a6ff; font-size:1.2rem;">🏛️ Tier 2: Directorate Governance Desk</div>
                    <div style="font-size:1.0rem; color:#c9d1d9; margin-top:4px;">
                        Cognizant Director: <strong style="color:#ffffff;">Dr. Arthur Pendleton</strong> | 
                        Statutory Shield: <strong style="color:#58a6ff;">{sector['statute']}</strong>
                    </div>
                </div>
                <div style="font-size:1.1rem; font-weight:800; color:{'#3fb950' if is_dir_signed else '#e3b341'};">
                    ● {'DIRECTORATE INDEMNITY SEALED' if is_dir_signed else 'AWAITING DIRECTOR COUNTERSIGNATURE'}
                </div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)
        if st.button("🏛️ Drill Down to Tier 2: Directorate Governance Desk", use_container_width=True):
            st.session_state.selected_view = t["tier2_title"]
            st.rerun()

    wo = active_inc.get("tier3_work_order", {})
    with st.container(border=True):
        st.markdown(f"""
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px;">
                <div>
                    <div style="font-weight:800; color:#e3b341; font-size:1.2rem;">👷 Tier 3: Site Operations & Remediation Desk</div>
                    <div style="font-size:1.0rem; color:#c9d1d9; margin-top:4px;">
                        Work Order: <strong style="color:#ffffff;">WO-8821-HARMONIC</strong> | 
                        Lead PE: <strong style="color:#ffffff;">Marcus Vance, PE</strong> |
                        Progress: <strong style="color:#ffffff;">{wo.get('progress_pct', 75)}% Completed</strong>
                    </div>
                </div>
                <div style="font-size:1.1rem; font-weight:800; color:{'#3fb950' if is_resolved else '#da3633'};">
                    ● {'PE DIGITAL STAMP TRANSMITTED' if is_resolved else 'BLOCKED BEHIND CLAUSE 14.b'}
                </div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)
        if st.button("⚡ Drill Down to Tier 3: Operator Remediation Desk", use_container_width=True):
            st.session_state.selected_view = t["tier3_title"]
            st.rerun()

elif selected_view == t["tier2_title"]:
    st.title(t["tier2_title"])
    st.info("Tier 2: Directorate Governance Desk Active")
    if st.button("↩️ Return to Tier 1"):
        st.session_state.selected_view = t["tier1_title"]
        st.rerun()

elif selected_view == t["tier3_title"]:
    st.title(t["tier3_title"])
    st.info("Tier 3: Site Operations & Remediation Desk Active")
    if st.button("↩️ Return to Tier 1"):
        st.session_state.selected_view = t["tier1_title"]
        st.rerun()

elif selected_view == t["tier4_title"]:
    st.title(t["tier4_title"])
    st.info("Tier 4: Forensic Cost Recovery Vault Active")
    if st.button("↩️ Return to Tier 1"):
        st.session_state.selected_view = t["tier1_title"]
        st.rerun()

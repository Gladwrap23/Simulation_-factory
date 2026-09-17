import datetime
import hashlib
import json
import re
import streamlit as st
import streamlit.components.v1 as components

APP_BUILD_ID = "v6.8_chairman_preemption_and_scroll_fix_sep17_2026"

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
# 1. INDUSTRIAL STYLING & PRINT STYLESHEET (@media print)
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
            padding: 22px 24px;
            font-family: Georgia, Cambria, "Times New Roman", Times, serif;
            color: #e6edf3;
            line-height: 1.75;
        }
        .legal-header {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-size: 1.05rem;
            font-weight: 800;
            color: #58a6ff;
            margin-bottom: 12px;
        }
        .sidebar-brand-card {
            background: linear-gradient(180deg, rgba(88, 166, 255, 0.14) 0%, rgba(22, 27, 34, 0.9) 100%);
            border: 1px solid #388bfd;
            border-radius: 8px;
            padding: 14px 16px;
            margin-bottom: 16px;
        }

        .director-card {
            background-color: #161b22;
            border: 1px solid #30363d;
            border-radius: 8px;
            padding: 16px 18px;
            margin-bottom: 12px;
        }
        .director-card-pinned {
            background-color: rgba(248, 81, 73, 0.12);
            border: 2px solid #f85149;
            border-radius: 8px;
            padding: 16px 18px;
            margin-bottom: 12px;
        }

        @media print {
            section[data-testid="stSidebar"],
            header,
            footer,
            [data-testid="stToolbar"],
            div[data-testid="stButton"],
            button,
            .tap-to-halt-container,
            .active-build-banner {
                display: none !important;
            }
            body, .stApp {
                background-color: #ffffff !important;
                color: #000000 !important;
                font-family: "Times New Roman", Times, serif !important;
            }
            p, span, div, h1, h2, h3, h4, code {
                color: #000000 !important;
            }
            .main .block-container {
                max-width: 100% !important;
                padding: 0.5in !important;
                margin: 0 !important;
            }
            .exec-metric-card, .circuit-breaker-card, .claim-demand-card, .legal-document-box {
                background-color: #ffffff !important;
                border: 1px solid #111111 !important;
                box-shadow: none !important;
                color: #000000 !important;
                break-inside: avoid;
            }
            .exec-metric-val, .exec-metric-val-secondary {
                color: #000000 !important;
            }
        }
    </style>
""", unsafe_allow_html=True)

# =========================================================
# 2. DATA MODEL & LOCALIZATION
# =========================================================
I18N = {
    "English [USA · UK · Australia]": {
        "tier1_title": "Tier 1 | Chairman Tactical Command Post (Part One)",
        "tier2_title": "Tier 2 | Directorate Governance Desk",
        "tier3_title": "Tier 3 | Site Operations & Operator Remediation Desk",
        "tier3a_title": "Tier 3A | Engineering Operations Command",
        "tier3b_title": "Tier 3B | Site Execution Desk",
        "tier4_title": "Tier 4 | Forensic Cost Recovery Vault (Part Two)",
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
        "tap_to_halt_desc": "Executing this directive issues an emergency Directorate Hold-Harmless Resolution under statute (Delaware DGCL § 141). It absorbs 100% of warranty liability from Lead PE Marcus Vance onto the corporate balance sheet, authorizes immediate transmission of the digital PE stamp, and halts daily burn to $0.",
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
        "board_roster": [
            {
                "name": "Dr. Arthur Pendleton",
                "seat": "Chair, Grid Risk & Technical Integrity Committee",
                "role": "Cognizant Technical Director",
                "pinned_to_bottleneck": True,
                "statutory_role": "Delaware DGCL § 141(e) Technical Reliance & Fiduciary Shield Authority",
                "management_bridge": "Sarah Jenkins (VP, Engineering Operations)",
                "subordinate_field_lead": "Marcus Vance, PE (Permian HV Field Services LLC)",
                "status": "AWAITING COUNTERSIGNATURE"
            },
            {
                "name": "David Chen (Proxy)",
                "seat": "Chair, Regulatory & Market Compliance Committee",
                "role": "Commercial Director",
                "pinned_to_bottleneck": False,
                "statutory_role": "PUCT / ERCOT Protocol § 4.2 Market Participant Attestation",
                "management_bridge": "Thomas Thorne (VP, Interconnection & Regulatory Affairs)",
                "subordinate_field_lead": "Elena Rostova (SCADA Regulatory Engineer)",
                "status": "STANDBY / NOMINAL"
            },
            {
                "name": "Executive Chairman",
                "seat": "Chairman of the Board of Directors",
                "role": "Chief Governance Officer",
                "pinned_to_bottleneck": False,
                "statutory_role": "Sovereign Board Prerogative & Balance Sheet Capital Allocation",
                "management_bridge": "General Counsel & Chief Financial Officer",
                "subordinate_field_lead": "Portfolio Oversight Desk",
                "status": "COMMAND ACTIVE"
            },
            {
                "name": "Eleanor Vance, CPA",
                "seat": "Chair, Audit & Financial Risk Committee",
                "role": "Audit Chair",
                "pinned_to_bottleneck": False,
                "statutory_role": "SOX Compliance & Demurrage Liquidated Damages Auditor",
                "management_bridge": "Corporate Controller",
                "subordinate_field_lead": "Cost Recovery Claims Analyst",
                "status": "AUDIT TRACKING"
            },
            {
                "name": "Amb. Hiroshi Tanaka",
                "seat": "Chair, Sovereign Governance & Geopolitical Supply Committee",
                "role": "Independent Director",
                "pinned_to_bottleneck": False,
                "statutory_role": "Critical Infrastructure Supply Chain Covenants (FERC CIP-014)",
                "management_bridge": "Chief Procurement Officer",
                "subordinate_field_lead": "OEM Supply Chain Investigator",
                "status": "MONITORING"
            }
        ],
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
                    "field_lead": "Marcus Vance, PE (TXLIC114902)",
                    "managing_vp": "Sarah Jenkins (VP, Engineering Operations)",
                    "progress_pct": 75,
                    "plain_english_trap": {
                        "headline": "🚨 Why the Fix is Blocked (Plain English):",
                        "who_blocks": "Marcus Vance, PE (Lead Engineer) refuses to sign off on Step 4.",
                        "reason": "Apex (Inverter OEM) is threatening to void the plant's multi-million dollar warranty under Clause 14.b if anyone touches the inverter cabinets without their off-site supervisor present.",
                        "consequence": "Signing without protection leaves Marcus personally liable and risks voiding the plant warranty. Not signing burns $87,264 every day.",
                        "fix": "Executing the Board Indemnity Instrument (Delaware DGCL § 141(e)) absorbs all liability onto the company balance sheet, legally protects Marcus Vance, and submits his digital PE stamp to ERCOT immediately."
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
                        "and holds harmless Marcus Vance, PE, VP Sarah Jenkins, and Permian HV Field Services LLC from all liability, claims, or damages "
                        "arising from the execution of Step 4 (PE Digital Attestation Stamp). The Corporation formally assumes full legal responsibility "
                        "for contested Clause 14.b claims and authorizes immediate bypass and grid energization."
                    ),
                    "signatories": [
                        {
                            "role": "Executive Chairman of the Board",
                            "name": "Executive Chairman",
                            "seat": "Sovereign Board Prerogative & Capital Defense",
                            "status": "EXECUTED & ATTESTED",
                            "hash": "sha256:7b910e12d4a19b882310b14c339a0ef28b123456789abcdef0123456789abcde",
                            "timestamp": "2026-09-16 00:00:00 UTC"
                        },
                        {
                            "role": "Cognizant Technical Director",
                            "name": "Dr. Arthur Pendleton",
                            "seat": "Chair, Grid Risk & Technical Integrity Committee",
                            "status": "PENDING DIRECTOR COUNTERSIGNATURE",
                            "hash": "sha256:f48a901c22e987102ce094a318894cb10e4a77e9921004ab12fedcba98765432",
                            "timestamp": "PENDING BOARD RELIANCE CERTIFICATE"
                        },
                        {
                            "role": "Lead Professional Engineer",
                            "name": "Marcus Vance, PE (TXLIC114902)",
                            "seat": "Signatory Custody / High-Voltage Commissioning Lead",
                            "status": "HELD PENDING INDEMNITY",
                            "hash": "sha256:1a8904df88b3cae182049bb110294eec89012bb45601a90ee45109b82144ac90",
                            "timestamp": "HELD UNDER CONTRACTUAL INTIMIDATION"
                        }
                    ]
                },
                "exhibits": [
                    {
                        "code": "EXHIBIT A-1",
                        "title": "IEEE COMTRADE Oscillography Binary Extract",
                        "filename": "ERCOT_FEEDER4A_FAULT_RECORDER_20260909_0814.DAT",
                        "size": "44.2 MB",
                        "sha256": "4b92cf88e1049ad08f12399cb1a40293ee019b882310b14c339a0ef28b123456",
                        "significance": "10 kHz digital fault recorder captures grid dip at 4.2%; proves ride-through compliance and isolates trip to OEM firmware threshold."
                    },
                    {
                        "code": "EXHIBIT B-1",
                        "title": "Sworn Field Affidavit & TBPE Seal #TXLIC114902 (Marcus Vance, PE)",
                        "filename": "PERMIAN_BESS_GATE_ACCESS_LOGS_SEP09_2026.CSV",
                        "size": "1.8 MB",
                        "sha256": "91ab802eec8912b4501a39d889b7102ce094a318894cb10e4a77e9921004ab12",
                        "significance": "Proves Apex Commissioning Lead was off-site during sequence, legally voiding vendor interference disclaimer."
                    },
                    {
                        "code": "EXHIBIT C-1",
                        "title": "Turnkey EPC Schedule D § 3 Liquidated Demurrage Ledger",
                        "filename": "EPC_TX9011_SCHEDULE_D_DEMURRAGE_AUDIT.PDF",
                        "size": "820 KB",
                        "sha256": "f01948ba9820cae182049bb110294eec89012bb45601a90ee45109b82144ac90",
                        "significance": "Line-by-line contractual calculation showing $87,264 x 7 days = $610,848 due in unexcused delay damages."
                    }
                ],
                "forensic_timeline": [
                    {"time": "2026-09-09 08:14:02.104 UTC", "party": "Grid Physics", "event": "Raw 10 kHz oscillography records grid voltage dip of 4.2% (nominal IEEE 2800 ride-through envelope)."},
                    {"time": "2026-09-09 08:14:02.118 UTC", "party": "Apex Inverter OEM", "event": "Inverter Bank 2 trips out prematurely due to internal OEM firmware protection threshold miscalibration."},
                    {"time": "2026-09-09 09:30:00.000 UTC", "party": "Apex Legal / Field", "event": "Apex invokes Clause 14.b warranty disclaimer, alleging utility surge and refusing attestation sign-off."},
                    {"time": "2026-09-09 10:15:22.000 UTC", "party": "Security Access Logs", "event": "Turnstile badging records confirm Apex OEM Commissioning Lead was off-site during trip sequence."},
                    {"time": "2026-09-16 00:00:00.000 UTC", "party": "Capital Audit Engine", "event": "Deadlock reaches Day 7. Accrued delay demurrage hits $610,848. Pre-litigation dossier compiled."}
                ]
            },
            "INC-002": {"title": "Substation Step-Up Inrush Damping", "priority": "P2 - HIGH", "base_daily_bleed": 38880},
            "INC-003": {"title": "SCADA Protocol IEC 61850 Gateway", "priority": "P3 - MODERATE", "base_daily_bleed": 15552},
            "INC-004": {"title": "BESS Inverter Firmware OTA Patch", "priority": "P4 - MONITORED", "base_daily_bleed": 4320},
            "INC-005": {"title": "Substation Oil DGA Baseline Sweep", "priority": "P5 - MONITORED", "base_daily_bleed": 6912}
        }
    }
}

BOARD_REMEDIES = {
    "Dr. Arthur Pendleton": (
        "Technical Safe-Harbor Reliance Certificate",
        "Executes formal statutory reliance under DGCL § 141(e) on 10kHz oscillography data, shielding Marcus Vance from personal warranty voidance threats."
    ),
    "Executive Chairman": (
        "Chairman Sovereign Preemption Warrant",
        "Invokes the Business Judgment Rule unilaterally, preempting committee delays, absorbing vendor warranty liability, and ordering immediate grid energization."
    ),
    "Eleanor Vance, CPA": (
        "Liquidated Damages Demurrage Certificate",
        "Formalizes the accrued delay claim against Apex OEM under Schedule D § 3 and prepares standby letter-of-credit drawdown."
    ),
    "David Chen (Proxy)": (
        "PUCT Statutory Compliance Attestation",
        "Certifies that the plant's harmonics comply with IEEE 2800 and protects the interconnection filing from utility penalties."
    ),
    "Amb. Hiroshi Tanaka": (
        "Formal Notice of Unexcused OEM Default",
        "Repudiates Apex's warranty-voidance position using gate-access evidence showing absent OEM personnel."
    )
}

for director in SECTORS["ERCOT BESS / Grid Storage (USA)"]["board_roster"]:
    remedy_title, remedy_description = BOARD_REMEDIES[director["name"]]
    director["remedy_title"] = remedy_title
    director["remedy_description"] = remedy_description

if "app_state" not in st.session_state:
    st.session_state.app_state = SECTORS

if "selected_incident_id" not in st.session_state:
    st.session_state.selected_incident_id = "INC-001"

if "selected_director" not in st.session_state:
    st.session_state.selected_director = "Dr. Arthur Pendleton"

if "conference_focus" not in st.session_state:
    st.session_state.conference_focus = "DEFAULT"

if "trigger_print" not in st.session_state:
    st.session_state.trigger_print = False

if "gate_3a_cleared" not in st.session_state:
    st.session_state.gate_3a_cleared = False

if "gate_3b_cleared" not in st.session_state:
    st.session_state.gate_3b_cleared = False

# --- STATE RECONCILIATION BRIDGE ---
# Ensures legacy work order states map seamlessly into the new 3A/3B flow.
if "t3a_step2" not in st.session_state:
    st.session_state.t3a_step2 = st.session_state.get("wo_released", st.session_state.get("work_order_active", False))

if "t3a_step3" not in st.session_state:
    st.session_state.t3a_step3 = st.session_state.get("t3_completed", False)

# =========================================================
# DEFERRED ROUTER & JAVASCRIPT SCROLL-TO-TOP RESET
# =========================================================
t = I18N["English [USA · UK · Australia]"]

nav_options = [
    t["tier1_title"], 
    t["tier2_title"],
    t["tier3a_title"],
    t["tier3b_title"],
    t["tier4_title"]
]

if "pending_view" in st.session_state:
    st.session_state["nav_desk_selection"] = st.session_state.pop("pending_view")
    components.html("""
        <script>
            window.parent.scrollTo(0, 0);
        </script>
    """, height=0, width=0)

if "nav_desk_selection" not in st.session_state or st.session_state.nav_desk_selection not in nav_options:
    st.session_state["nav_desk_selection"] = t["tier1_title"]

def request_navigation(target_desk):
    st.session_state["pending_view"] = target_desk
    st.rerun()

def execute_unified_circuit_breaker(incident: dict, daily_bleed: float):
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
            sig["timestamp"] = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        elif "Engineer" in sig["role"]:
            sig["status"] = "DIGITAL STAMP TRANSMITTED"
            sig["timestamp"] = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

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
            sig["timestamp"] = "PENDING BOARD RELIANCE CERTIFICATE"
        elif "Engineer" in sig["role"]:
            sig["status"] = "HELD PENDING INDEMNITY"
            sig["timestamp"] = "HELD UNDER CONTRACTUAL INTIMIDATION"

# =========================================================
# 3. SIDEBAR NAVIGATION
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
                Pactum Sovereign OS · Build v6.8
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    active_sector = st.selectbox("Operating Book (Global Assets):", list(st.session_state.app_state.keys()))
    sector = st.session_state.app_state[active_sector]
    curr_sym = sector["currency"]
    
    lang_choice = st.selectbox(
        "Sovereign Legal Jurisdiction:",
        ["🇺🇸 ERCOT / Delaware (DGCL § 141)", "🇩🇪 EBA / Germany (AktG § 93)", "🇨🇱 CEN / Chile (Art. 72-1)", "🇫🇷 RTE / France (L225-251)", "🇯🇵 METI / Japan (Art. 423)"]
    )
    
    calib_key = f"capex_override_{active_sector}"
    if calib_key not in st.session_state:
        st.session_state[calib_key] = int(sector["asset_cap"])
    current_calib_capex = st.session_state[calib_key]
    scale_factor = current_calib_capex / sector["asset_cap"]

    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
    st.markdown("#### Command Desk")
    
    selected_view = st.radio(
        "Select Operating Desk:",
        nav_options,
        key="nav_desk_selection",
        label_visibility="collapsed"
    )
    
    st.divider()
    st.markdown("#### 🖨️ Universal Export Utility")
    if st.button("🖨️ Print Desk / Export PDF", use_container_width=True):
        st.session_state.trigger_print = True

    st.markdown("#### 🔒 Active Incident Queue")
    for inc_key, inc_obj in sector["incidents"].items():
        is_sel = inc_key == st.session_state.selected_incident_id
        inc_daily = inc_obj.get("base_daily_bleed", 50000) * scale_factor
        inc_crossover = round(current_calib_capex / inc_daily, 1) if inc_daily > 0 else 999
        btn_label = f"{inc_obj.get('priority', 'P1')}: {inc_key}\n{inc_crossover}d Crossover"
        
        if st.button(btn_label, key=f"sb_{inc_key}", use_container_width=True, type="primary" if is_sel else "secondary"):
            st.session_state.selected_incident_id = inc_key
            st.session_state.conference_focus = "DEFAULT"
            request_navigation(t["tier1_title"])

if st.session_state.selected_incident_id not in sector["incidents"]:
    st.session_state.selected_incident_id = next(iter(sector["incidents"]))
active_inc = sector["incidents"][st.session_state.selected_incident_id]
is_resolved = active_inc.get("status") == "RESOLVED"
is_dir_signed = active_inc.get("director_signed", False) or is_resolved
is_bypassed = active_inc.get("manual_pe_bypass", False) or is_resolved

if st.session_state.trigger_print:
    st.session_state.trigger_print = False
    components.html("<script>window.parent.print();</script>", height=0, width=0)

# =========================================================
# 4. VIEW: TIER 1 — CHAIRMAN TACTICAL COMMAND POST
# =========================================================
if selected_view == t["tier1_title"]:
    top_col1, top_col2 = st.columns([4, 1])
    with top_col1:
        st.markdown("""
            <div class="active-build-banner" style="background: #1f6feb; color: #ffffff; padding: 6px 12px; border-radius: 4px; font-weight: 800; font-size: 0.9rem; margin-bottom: 12px; text-align: center;">
                ⚡ ACTIVE BUILD: v6.8 | CHAIRMAN PREEMPTION DESK & DOM SCROLL FIX ACTIVE
            </div>
        """, unsafe_allow_html=True)
    with top_col2:
        if st.button("🖨️ Print Tier 1", use_container_width=True):
            components.html("<script>window.parent.print();</script>", height=0, width=0)

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
            st.markdown("🔴 **Telemetry Agent:** *'Physical telemetry is nominal (THD 4.1% < 5.0%). Marcus Vance refuses sign-off because Apex OEM threatens warranty cancellation under Clause 14.b. Deadlock is contractual, not physical.'*")
        elif st.session_state.conference_focus == "WHAT_UNBLOCKS":
            inst = active_inc.get("legal_instrument", {})
            st.markdown(f"🟢 **Fiduciary Shield Agent:** *'The **Directorate Indemnity & Statutory Hold-Harmless Resolution** pursuant to **Delaware DGCL § 141(e)**.'* \n\n"
                        f"📄 **Plain-English Document Summary:** Dr. Arthur Pendleton countersigns the reliance certificate, absorbing personal liability from Lead PE Marcus Vance onto the corporate balance sheet.")
        else:
            st.markdown(f"⚡ **Active Interrogation Standby ({TODAY_STR}):** Agents synchronized with Delaware DGCL § 141. Select an action above or tap the Holding Burn Circuit Breaker below to halt exposure.")

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
                execute_unified_circuit_breaker(active_inc, total_burn_day)
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

    st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)
    st.markdown("### 📡 Operational Chain of Command (Single-Line Descending Hierarchy)")
    
    with st.container(border=True):
        st.markdown(f"""
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px;">
                <div>
                    <div style="font-weight:800; color:#58a6ff; font-size:1.2rem;">🏛️ Tier 2: Directorate Governance Desk</div>
                    <div style="font-size:1.0rem; color:#c9d1d9; margin-top:4px;">
                        Cognizant Director: <strong style="color:#ffffff;">Dr. Arthur Pendleton</strong> | 
                        Statutory Shield: <strong style="color:#58a6ff;">Delaware DGCL § 141</strong>
                    </div>
                </div>
                <div style="font-size:1.1rem; font-weight:800; color:{'#3fb950' if is_dir_signed else '#e3b341'};">
                    ● {'DIRECTORATE INDEMNITY SEALED' if is_dir_signed else 'AWAITING DIRECTOR COUNTERSIGNATURE'}
                </div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)
        if st.button("🏛️ Drill Down to Tier 2: Directorate Governance Desk", use_container_width=True):
            request_navigation(t["tier2_title"])

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
            request_navigation(t["tier3a_title"])

# =========================================================
# 5. VIEW: TIER 2 — DIRECTORATE GOVERNANCE DESK (ELEVATED)
# =========================================================
elif selected_view == t["tier2_title"]:
    top_col1, top_col2 = st.columns([4, 1])
    with top_col1:
        st.title(t["tier2_title"])
    with top_col2:
        if st.button("🖨️ Print Resolution", use_container_width=True):
            components.html("<script>window.parent.print();</script>", height=0, width=0)

    st.caption(f"Asset: **{active_sector}** | Governing Authority: **{sector['statute']}** | Effective: **{TODAY_STR}**")
    
    if st.button("↩️ Return to Tier 1: Chairman Command Post", type="secondary"):
        request_navigation(t["tier1_title"])
        
    st.divider()

    # LARGE HIGH-CONTRAST GOVERNANCE BANNER (NO UP ARROWS)
    if is_dir_signed:
        st.markdown("""
            <div style="background: rgba(46, 160, 67, 0.15); border: 2px solid #2ea043; border-radius: 8px; padding: 20px 24px; margin-bottom: 22px;">
                <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px;">
                    <div>
                        <div style="font-size: 0.9rem; font-weight: 800; color: #3fb950; text-transform: uppercase; letter-spacing: 0.05em;">Statutory Fiduciary Status</div>
                        <div style="font-size: 1.9rem; font-weight: 900; color: #ffffff; line-height: 1.2; margin: 4px 0;">🟢 SAFE HARBOR ACTIVE & SEALED</div>
                        <div style="font-size: 1.05rem; color: #c9d1d9;">
                            Directorate Indemnity concurred under Delaware DGCL § 141(e). All field engineers legally held harmless.
                        </div>
                    </div>
                    <div style="background: #2ea043; color: #ffffff; padding: 10px 18px; border-radius: 6px; font-weight: 900; font-size: 1.05rem;">
                        LEGAL SHIELD: SEALED
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style="background: rgba(248, 81, 73, 0.15); border: 2px solid #f85149; border-radius: 8px; padding: 20px 24px; margin-bottom: 22px;">
                <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px;">
                    <div>
                        <div style="font-size: 0.9rem; font-weight: 800; color: #f85149; text-transform: uppercase; letter-spacing: 0.05em;">Statutory Fiduciary Status</div>
                        <div style="font-size: 1.9rem; font-weight: 900; color: #ffffff; line-height: 1.2; margin: 4px 0;">🔴 GOVERNANCE DEADLOCK (P1 - CRITICAL)</div>
                        <div style="font-size: 1.05rem; color: #c9d1d9;">
                            Marcus Vance, PE is exposed to personal liability under Clause 14.b. Attestation held pending Directorate Countersignature.
                        </div>
                    </div>
                    <div style="background: #da3633; color: #ffffff; padding: 10px 18px; border-radius: 6px; font-weight: 900; font-size: 1.05rem;">
                        BLEED: $87,264 / DAY
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("### 🏛️ Full Board of Directors & Governance Roster")
    st.caption("The system automatically pins and illuminates the director possessing statutory jurisdiction over the active bottleneck:")

    roster = sector.get("board_roster", [])
    for d in roster:
        is_pinned = d.get("pinned_to_bottleneck", False)
        is_selected = d["name"] == st.session_state.selected_director
        
        card_class = "director-card-pinned" if is_pinned else "director-card"
        border_status = "🔴 ACTIVE BOTTLENECK REMIT" if is_pinned and not is_dir_signed else ("✅ SAFE HARBOR CONCURRED" if is_dir_signed and is_pinned else "🟢 COMPLIANT / STANDBY")
        
        col_d1, col_d2 = st.columns([3, 1])
        with col_d1:
            st.markdown(f"""
                <div class="{card_class}">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <strong style="font-size:1.3rem; color:#ffffff;">{d['name']}</strong>
                        <span style="font-size:0.85rem; font-weight:800; color:{'#f85149' if is_pinned and not is_dir_signed else '#3fb950'}; background:rgba(0,0,0,0.4); padding:4px 10px; border-radius:4px;">
                            {border_status}
                        </span>
                    </div>
                    <div style="font-size:1.05rem; color:#58a6ff; font-weight:700; margin: 4px 0;">{d['seat']}</div>
                    <div style="font-size:0.95rem; color:#c9d1d9;">Statutory Role: <em>{d['statutory_role']}</em></div>
                    <div style="font-size:0.9rem; color:#8b949e; margin-top:6px;">
                        Reporting Line: <strong>{d['management_bridge']}</strong> ➔ <strong>{d['subordinate_field_lead']}</strong>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        with col_d2:
            st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)
            if is_selected:
                st.markdown("""
                    <div style="background: rgba(46, 160, 67, 0.2); border: 2px solid #2ea043; border-radius: 6px; padding: 12px; text-align: center; font-weight: 800; color: #3fb950; font-size: 0.95rem;">
                        ✓ ACTIVE DESK VIEW
                    </div>
                """, unsafe_allow_html=True)
            else:
                if st.button("➔ Switch to Desk", key=f"sel_dir_{d['name']}", use_container_width=True, type="secondary"):
                    st.session_state.selected_director = d["name"]
                    st.rerun()

    st.markdown("---")
    current_d = next((x for x in roster if x["name"] == st.session_state.selected_director), roster[0])
    
    if current_d.get("pinned_to_bottleneck"):
        st.markdown(f"### 📜 Formal Fiduciary Protection Instrument ({sector['statute']})")
        st.markdown(f"""
            <div style="background:rgba(88,166,255,0.08); border-left:4px solid #58a6ff; padding:14px 18px; border-radius:4px; margin-bottom:16px;">
                <div style="font-weight:800; font-size:1.15rem; color:#58a6ff;">OPERATIONAL CASCADE: {current_d['name']} ➔ {current_d['management_bridge']} ➔ {current_d['subordinate_field_lead']}</div>
                <div style="font-size:1.0rem; color:#c9d1d9; margin-top:4px;">
                    This director possesses statutory safe-harbor jurisdiction over <strong>INC-001 (Harmonic Attestation Deadlock)</strong>. 
                    Executing countersignature transmits corporate indemnification to <strong>VP Sarah Jenkins</strong> and authorizes <strong>Marcus Vance, PE</strong> to stamp the ERCOT filing.
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        inst = active_inc.get("legal_instrument", {})
        with st.container(border=True):
            st.markdown(f"""
                <div class="legal-document-box">
                    <div class="legal-header">🏛️ Primary Legal Document: {inst.get('title')}</div>
                    <div style="font-size:1.0rem; color:#8b949e; margin-bottom:14px;">
                        Statutory Authority: <strong style="color:#ffffff;">{inst.get('authority')}</strong> | Effective: <strong style="color:#58a6ff;">{inst.get('effective_date')}</strong>
                    </div>
                    <div style="font-style:italic; margin: 12px 0; font-size:1.05rem;">
                        {'<br><br>'.join(inst.get('recitals', []))}
                    </div>
                    <div style="background:rgba(88,166,255,0.08); padding:16px; border-radius:6px; font-weight:bold; margin-bottom:16px; font-size:1.1rem;">
                        {inst.get('operative_resolution')}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown("### 🔏 Executed Digital Signatures & Verification Hashes")
            st.caption("Cryptographic audit trail anchoring statutory reliance under Delaware DGCL § 141:")

            for sig in inst.get("signatories", []):
                is_signed = "EXECUTED" in sig["status"] or "COUNTERSIGNED" in sig["status"] or "TRANSMITTED" in sig["status"]
                status_badge_col = "#3fb950" if is_signed else "#e3b341"
                card_border = "#2ea043" if is_signed else "#e3b341"
                
                st.markdown(f"""
                    <div style="background:#090d13; border:2px solid {card_border}; border-radius:8px; padding:18px 20px; margin-bottom:12px;">
                        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
                            <div>
                                <span style="font-size:0.85rem; font-weight:800; color:#8b949e; text-transform:uppercase;">{sig['role']}</span>
                                <div style="font-size:1.35rem; font-weight:900; color:#ffffff; margin:2px 0;">{sig['name']}</div>
                                <div style="font-size:0.95rem; color:#58a6ff; font-weight:600;">{sig['seat']}</div>
                            </div>
                            <div style="text-align:right;">
                                <span style="background:{status_badge_col}; color:#000000; padding:6px 12px; border-radius:4px; font-weight:900; font-size:0.95rem; display:inline-block;">
                                    {sig['status']}
                                </span>
                                <div style="font-size:0.85rem; color:#c9d1d9; font-family:monospace; margin-top:6px;">Timestamp: {sig['timestamp']}</div>
                            </div>
                        </div>
                        <div style="margin-top:12px; padding-top:10px; border-top:1px solid #21262d;">
                            <div style="font-size:0.8rem; color:#8b949e; font-weight:700; text-transform:uppercase;">Cryptographic Hash Receipt (SHA-256):</div>
                            <code style="color:#58a6ff; font-size:0.95rem; font-weight:700; background:rgba(88,166,255,0.1); padding:4px 8px; border-radius:4px; display:inline-block; margin-top:4px; word-break:break-all;">
                                {sig.get('hash', 'N/A')}
                            </code>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)
            if not is_dir_signed:
                if st.button(f"✍️ Countersign Directorate Indemnity Resolution ({current_d['name']})", use_container_width=True, type="primary"):
                    active_inc["director_signed"] = True
                    for sig in inst.get("signatories", []):
                        if "Director" in sig["role"]:
                            sig["status"] = "COUNTERSIGNED & SEALED"
                            sig["timestamp"] = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
                    st.success("Director concurrence executed. Advancing downward to Tier 3 field desk...")
                    st.rerun()
            else:
                nav_col1, nav_col2 = st.columns(2)
                with nav_col1:
                    if st.button(f"➔ Cascade to Tier 3 Field Desk ({current_d['subordinate_field_lead']})", use_container_width=True, type="primary"):
                        request_navigation(t["tier3a_title"])
                with nav_col2:
                    if st.button("↩️ Return to Tier 1: Tactical Command Post", use_container_width=True):
                        request_navigation(t["tier1_title"])
    else:
        if current_d["name"] == "Executive Chairman":
            st.markdown("### ⚡ Sovereign Board Preemption Desk: Executive Chairman")
            st.markdown(f"""
                <div style="background:rgba(218,54,51,0.12); border-left:4px solid #da3633; padding:16px 20px; border-radius:4px; margin-bottom:18px;">
                    <div style="font-weight:900; font-size:1.2rem; color:#ff4b4b;">PLENARY SOVEREIGN OVERRIDE (DELAWARE DGCL § 141)</div>
                    <div style="font-size:1.05rem; color:#f0f6fc; margin-top:6px; line-height:1.6;">The Chairman may preempt committee delay, absorb vendor warranty liability, and order immediate energization when holding bleed threatens the balance sheet.</div>
                </div>
            """, unsafe_allow_html=True)
            with st.container(border=True):
                st.markdown(f"""
                    <div class="legal-document-box" style="border-left-color:#da3633;">
                        <div class="legal-header" style="color:#da3633;">🏛️ CHAIRMAN'S EMERGENCY PREEMPTION & ENERGIZATION WARRANT</div>
                        <p><strong>Authority:</strong> Delaware General Corporation Law § 141(a) & Corporate Charter Plenary Powers</p>
                        <p><strong>Operative Order:</strong> Immediate transmission of the PE attestation stamp to ERCOT with complete corporate indemnity for Marcus Vance, PE and Permian HV Field Services LLC under Contract #TX-9011.</p>
                    </div>
                """, unsafe_allow_html=True)
                if not is_resolved and st.button("🛑 EXECUTE CHAIRMAN'S PREEMPTION WARRANT (STOP CAPITAL BLEED)", use_container_width=True, type="primary"):
                    execute_unified_circuit_breaker(active_inc, 87264 * scale_factor)
                    st.success("Chairman's Preemption Warrant executed. Capital bleed stopped.")
                    st.rerun()
                elif is_resolved:
                    st.success("Chairman Preemption is active. Capital defended to $0/day.")
                    if st.button("➔ Advance to Tier 4: Departmental Forensic Vault", use_container_width=True, type="primary"):
                        request_navigation(t["tier4_title"])
        elif current_d["name"] == "Eleanor Vance, CPA":
            st.markdown("### 📊 Audit & Demurrage Recovery Desk: Eleanor Vance, CPA")
            st.markdown(f"""
                <div style="background:rgba(227,179,65,0.1); border-left:4px solid #e3b341; padding:14px 18px; border-radius:4px; margin-bottom:16px;">
                    <div style="font-weight:800; font-size:1.15rem; color:#e3b341;">SOX COMPLIANCE & LIQUIDATED DAMAGES AUDIT</div>
                    <div style="font-size:1.0rem; color:#c9d1d9; margin-top:4px;">Every 24 hours of vendor stall adds $87,264 to the certified Schedule D claim ledger.</div>
                </div>
                <div class="legal-document-box"><strong>Certified Liquidated Demurrage Total:</strong> <span style="color:#e3b341; font-size:1.4rem;">${87264 * 7 * scale_factor:,.0f} USD</span><br><br>{current_d['remedy_description']}</div>
            """, unsafe_allow_html=True)
            if st.button("➔ Inspect Full Forensic Demurrage Ledger (Tier 4)", use_container_width=True, type="primary"):
                request_navigation(t["tier4_title"])
        else:
            st.markdown(f"### 🌐 Committee Remit: {current_d['name']}")
            st.markdown(f"""
                <div style="background:rgba(88,166,255,0.08); border-left:4px solid #58a6ff; padding:14px 18px; border-radius:4px; margin-bottom:16px;">
                    <div style="font-weight:800; font-size:1.15rem; color:#58a6ff;">{current_d['remedy_title']}</div>
                    <div style="font-size:1.0rem; color:#c9d1d9; margin-top:4px;">{current_d['remedy_description']}</div>
                </div>
            """, unsafe_allow_html=True)
            st.info("This committee stands ready in support. The primary blocker remains the high-voltage inverter attestation owned by Dr. Arthur Pendleton or the Executive Chairman.")

# =========================================================
# 6. VIEW: TIER 3A — ENGINEERING OPERATIONS COMMAND
# =========================================================
elif selected_view == t["tier3a_title"]:
    st.markdown("### Tier 3A | Engineering Operations Command")
    st.caption("Corporate Risk Absorption & Utility Packaging Desk | VP Sarah Jenkins")

    st.markdown("""
        <div style="background-color: #111a2e; border-left: 4px solid #00d4ff; padding: 12px 16px; border-radius: 4px; margin-bottom: 20px;">
            <div style="font-size: 0.85rem; color: #00d4ff; font-weight: 700;">CORPORATE INDEMNITY CONVEYANCE GATEWAY</div>
            <div style="font-size: 0.80rem; color: #a0aec0;">
                Delegated authority under Delaware DGCL § 141(e) resolution signed by Dr. Arthur Pendleton. Corporate asset owner assumes commercial warranty risk prior to contractor site dispatch.
            </div>
        </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns([2, 1])
    with c1:
        step1 = st.checkbox(
            "Step 1: Countersign Directorate Safe-Harbor Receipt",
            value=st.session_state.get("gate_3a_step1", False),
            key="ui_t3a_step1"
        )
        st.session_state.gate_3a_step1 = step1
        step2 = st.checkbox(
            "Step 2: Release Substation Work Order WO-8821-HARMONIC",
            value=st.session_state.get("gate_3a_step2", False),
            key="ui_t3a_step2",
            disabled=not step1
        )
        st.session_state.gate_3a_step2 = step2
        step3 = st.checkbox(
            "Step 3: Assemble ERCOT § 4.2 Tariff Interconnection Package",
            value=st.session_state.get("gate_3a_cleared", False),
            key="ui_t3a_step3",
            disabled=not step2
        )
        if step3:
            st.session_state.gate_3a_cleared = True

    with c2:
        st.markdown("**Command Lead Status**")
        st.write("Officer: **Sarah Jenkins**")
        st.write("Role: **VP, Engineering Operations**")
        st.write("Contractor: **Permian HV Field Services**")
        if st.session_state.gate_3a_cleared:
            st.success("● 3A Gate Cleared: Dispatched to Field Lead")
            if st.button("Jump to Tier 3B Execution Desk ➔", use_container_width=True):
                request_navigation(t["tier3b_title"])
        else:
            st.warning("○ Awaiting Corporate Handoff Completion")

# =========================================================
# 7. VIEW: TIER 3B — SITE EXECUTION & REMEDIATION DESK
# =========================================================
elif selected_view == t["tier3b_title"]:
    top_col1, top_col2 = st.columns([4, 1])
    with top_col1:
        st.title(f"👷 {t['tier3b_title']}")
        st.caption("Specialized Physical Engineering & Statutory Attestation | Marcus Vance, PE (TXLIC114902)")
    with top_col2:
        if st.button("🖨️ Print Work Order", use_container_width=True):
            components.html("<script>window.parent.print();</script>", height=0, width=0)

    if not st.session_state.gate_3a_cleared:
        st.error("⚠️ ACCESS RESTRICTED: Tier 3A Work Order WO-8821-HARMONIC has not been released by Sarah Jenkins.")
        if st.button("← Return to Tier 3A to Release Work Order"):
            request_navigation(t["tier3a_title"])
        st.stop()

    st.markdown("""
        <div style="background-color: #1a1e24; border-left: 4px solid #00ff88; padding: 12px 16px; border-radius: 4px; margin-bottom: 20px;">
            <div style="font-size: 0.85rem; color: #00ff88; font-weight: 700;">STATUTORY PERSONAL LICENSURE SHIELD: ACTIVE</div>
            <div style="font-size: 0.80rem; color: #a0aec0;">
                Execution is shielded under Corporate Covenant #COV-8821. Personal statutory liability under Texas Board of Professional Engineers regulations transferred to asset balance sheet.
            </div>
        </div>
    """, unsafe_allow_html=True)

    b1, b2 = st.columns([2, 1])
    with b1:
        f_step1 = st.checkbox(
            "Step 1: Rack 4 Neutral Grounding & Continuity Sweep (Exhibit B-1)",
            value=st.session_state.get("gate_3b_step1", False),
            key="ui_t3b_step1"
        )
        st.session_state.gate_3b_step1 = f_step1
        f_step2 = st.checkbox(
            "Step 2: Inverter Bank 1-4 Sub-Cycle Harmonic Sweep (THD 4.1% vs IEEE 2800)",
            value=st.session_state.get("gate_3b_step2", False),
            key="ui_t3b_step2",
            disabled=not f_step1
        )
        st.session_state.gate_3b_step2 = f_step2
        f_step3 = st.checkbox(
            "Step 3: Engage Hardware PE Key Interlock Bypass",
            value=st.session_state.get("gate_3b_step3", False),
            key="ui_t3b_step3",
            disabled=not f_step2
        )
        st.session_state.gate_3b_step3 = f_step3
        f_step4 = st.checkbox(
            "Step 4: Affix Statutory PE Digital Seal & Transmission Attestation",
            value=st.session_state.get("gate_3b_cleared", False),
            key="ui_t3b_step4",
            disabled=not f_step3
        )
        if f_step4:
            st.session_state.gate_3b_cleared = True

    with b2:
        st.markdown("**Licensure Credentials**")
        st.write("Field Lead: **Marcus Vance, PE**")
        st.write("Jurisdiction: **TBPE Reg #TXLIC114902**")
        st.write("Execution Hash: `e3b0c44298fc1c149afb...`")
        if st.session_state.gate_3b_cleared:
            st.success("● Physical Attestation Sealed")
        else:
            st.info("○ Verification in Progress")

    if st.session_state.gate_3b_cleared:
        st.markdown("---")
        st.markdown("""
            <div style="background-color: #0e2a1e; border: 1px solid #00ff88; padding: 16px; border-radius: 8px; text-align: center; margin-top: 10px; margin-bottom: 15px;">
                <div style="font-size: 1.1rem; font-weight: 800; color: #00ff88; margin-bottom: 6px;">
                    FIELD EXECUTION COMPLETE - CHAIN OF CUSTODY SEALED
                </div>
                <div style="color: #cbd5e0; font-size: 0.85rem; margin-bottom: 12px;">
                    Raw oscillography binaries, sworn PE affidavit (TXLIC114902), and Turnkey breach records compiled into the pre-litigation vault.
                </div>
            </div>
        """, unsafe_allow_html=True)

        if st.button("Proceed to Tier 4: Sealed Pre-Litigation Dossier", use_container_width=True, type="primary"):
            execute_unified_circuit_breaker(active_inc, 87264 * scale_factor)
            request_navigation(t["tier4_title"])

    wo = active_inc.get("tier3_work_order", {})
    trap = wo.get("plain_english_trap", {})
    
    st.markdown(f"""
        <div style="background: rgba(88, 166, 255, 0.1); border: 1px solid #388bfd; border-radius: 6px; padding: 12px 16px; margin-bottom: 16px;">
            <div style="font-size:0.9rem; font-weight:800; color:#58a6ff; text-transform:uppercase;">🔒 Scoped Operational Silo: Grid Risk & Technical Integrity</div>
            <div style="font-size:1.05rem; color:#ffffff; margin-top:2px;">
                Cognizant Director: <strong>Dr. Arthur Pendleton</strong> ➔ Managing VP: <strong>{wo.get('managing_vp', 'VP Engineering')}</strong> ➔ Field Lead: <strong>{wo.get('field_lead', 'Marcus Vance, PE')}</strong>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("↩️ Return to Tier 1: Chairman Command Post", type="secondary"):
        request_navigation(t["tier1_title"])
        
    st.divider()
    
    t1, t2, t3 = st.columns(3)
    with t1:
        st.markdown(f"""
            <div class="exec-metric-card">
                <div class="exec-metric-label">Active Work Order</div>
                <div class="exec-metric-val-secondary">{wo.get('id', 'N/A')}</div>
                <div style="color: #f85149; font-weight: 800; font-size: 0.95rem; margin-top: 4px;">● {active_inc.get('priority', 'CRITICAL')}</div>
            </div>
        """, unsafe_allow_html=True)
    with t2:
        st.markdown(f"""
            <div class="exec-metric-card">
                <div class="exec-metric-label">Target Regulatory Gate</div>
                <div class="exec-metric-val-secondary" style="font-size:1.15rem;">{wo.get('target_gate', 'COD Gate')}</div>
                <div style="color: #58a6ff; font-weight: 700; font-size: 0.9rem; margin-top: 4px;">ERCOT Docket #54219</div>
            </div>
        """, unsafe_allow_html=True)
    with t3:
        st.markdown(f"""
            <div class="exec-metric-card">
                <div class="exec-metric-label">Execution Progress</div>
                <div class="exec-metric-val" style="color: {'#3fb950' if is_resolved else '#e3b341'};">{wo.get('progress_pct', 0)}%</div>
                <div style="color: {'#3fb950' if is_resolved else '#e3b341'}; font-weight: 700; font-size: 0.9rem; margin-top: 4px;">{'COMPLETE' if is_resolved else 'STEP 4 PENDING INDEMNITY'}</div>
            </div>
        """, unsafe_allow_html=True)
    
    col_t, col_m = st.columns([3, 2])
    with col_t:
        with st.container(border=True):
            st.markdown(f"#### Execution Punch List & Sign-Off: {wo.get('title', 'Tasks')}")
            for idx, step in enumerate(wo.get("steps", [])):
                st.markdown(f"""
                    <div style="padding: 10px; border-bottom: 1px solid #30363d;">
                        <span style="font-size: 1.15rem;">{'✅' if step['done'] else '⏳'}</span>
                        <strong style="color: #ffffff; font-size: 1.05rem; margin-left: 6px;">Step {idx+1}: {step['task']}</strong>
                        <div style="color: #8b949e; font-size: 0.95rem; margin-left: 28px;">Evidence: <code>{step.get('evidence', 'Verified')}</code></div>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)
            if not is_resolved:
                shield_badge = "🟢 Directorate Indemnity Shield Active" if is_dir_signed else "⚠️ Awaiting Directorate Countersignature"
                st.markdown(f"""
                    <div style="background: rgba(248, 81, 73, 0.15); border: 2px solid #f85149; border-radius: 8px; padding: 18px; margin-bottom: 16px;">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                            <div style="color: #f85149; font-size: 1.25rem; font-weight: 800;">
                                {trap.get('headline', '🚨 Signatory Deadlock Warning')}
                            </div>
                            <span style="font-size:0.9rem; font-weight:700; color:{'#3fb950' if is_dir_signed else '#e3b341'}; background:rgba(0,0,0,0.5); padding:4px 8px; border-radius:4px;">
                                {shield_badge}
                            </span>
                        </div>
                        <div style="font-size: 1.05rem; line-height: 1.6; color: #f0f6fc;">
                            <p style="margin: 0 0 8px 0;">
                                👤 <strong>Who is refusing to sign:</strong> <br>
                                <span style="color: #ffffff; font-weight: 700;">{trap.get('who_blocks', 'Lead PE refuses sign-off.')}</span>
                            </p>
                            <p style="margin: 0 0 8px 0;">
                                ⚠️ <strong>Why they are refusing:</strong> <br>
                                {trap.get('reason', 'Threat of warranty voidance by vendor.')}
                            </p>
                            <div style="background: rgba(0,0,0,0.4); border-left: 4px solid #3fb950; padding: 10px 12px; margin-top: 10px; border-radius: 4px;">
                                🛡️ <strong>How this button fixes it:</strong> <br>
                                <span style="color: #e6edf3;">{trap.get('fix', 'Executes board indemnity to absorb liability and clear the gate.')}</span>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                if st.button("⚡ Transmit Lead PE Attestation Stamp & Seal Gate", use_container_width=True, type="primary"):
                    execute_unified_circuit_breaker(active_inc, 87264 * scale_factor)
                    st.success("PE Stamp sealed. Gate resolved. Auto-routing to Tier 1 Command Post...")
                    request_navigation(t["tier1_title"])
            else:
                st.success(f"✅ Work order completed at 100%. Professional Engineer stamp transmitted by {wo.get('field_lead', 'Lead PE')}.")
                btn_ret, btn_vault = st.columns(2)
                with btn_ret:
                    if st.button("↩️ Return to Tier 1: Chairman Command Post", use_container_width=True, type="primary"):
                        request_navigation(t["tier1_title"])
                with btn_vault:
                    if st.button("➔ Advance to Tier 4: Departmental Forensic Vault", use_container_width=True):
                        request_navigation(t["tier4_title"])
                
                st.markdown("---")
                if st.button("🔄 Reset Work Order to Neutral (Simulate Re-test)", use_container_width=True):
                    reset_incident_to_neutral(active_inc)
                    st.rerun()
                    
    with col_m:
        with st.container(border=True):
            st.markdown("#### Live Site Telemetry Waveform Sweep")
            for telem in wo.get("telemetry", []):
                val_col = "#3fb950" if telem["status"] == "NOMINAL" or telem["status"] == "COMPLIANT" else "#e3b341"
                st.markdown(f"""
                    <div style="background:#090d13; border:1px solid #30363d; border-radius:6px; padding:10px 14px; margin-bottom:10px;">
                        <div style="font-size:0.9rem; color:#8b949e; text-transform:uppercase;">{telem['param']}</div>
                        <div style="font-size:1.4rem; font-weight:800; font-family:monospace; color:{val_col}; margin: 2px 0;">{telem['val']}</div>
                        <div style="font-size:0.85rem; color:#c9d1d9;">Threshold: <strong>{telem['limit']}</strong></div>
                    </div>
                """, unsafe_allow_html=True)
                
            st.markdown("---")
            st.markdown("#### Hardware Physical Interlock Control")
            
            if not is_bypassed:
                st.markdown("""
                    <div style="background:#161b22; border:2px solid #e3b341; border-radius:6px; padding:12px 14px; margin-bottom:10px;">
                        <div style="font-size:0.85rem; color:#8b949e; text-transform:uppercase; font-weight:700;">OEM Cabinet Remote Interlock</div>
                        <div style="font-size:1.4rem; font-weight:900; font-family:monospace; color:#e3b341; margin: 2px 0;">DISENGAGED</div>
                        <div style="font-size:0.85rem; color:#c9d1d9;">Status: <strong style="color:#f85149;">Manual PE Bypass Required (Cabinet Locked)</strong></div>
                    </div>
                """, unsafe_allow_html=True)
                
                if st.button("⚡ Engage Manual PE Hardware Bypass", use_container_width=True, type="secondary"):
                    active_inc["manual_pe_bypass"] = True
                    st.success("Manual PE Bypass Engaged. Interlock overridden.")
                    st.rerun()
            else:
                st.markdown("""
                    <div style="background:rgba(46,160,67,0.15); border:2px solid #2ea043; border-radius:6px; padding:12px 14px; margin-bottom:10px;">
                        <div style="font-size:0.85rem; color:#8b949e; text-transform:uppercase; font-weight:700;">OEM Cabinet Remote Interlock</div>
                        <div style="font-size:1.4rem; font-weight:900; font-family:monospace; color:#3fb950; margin: 2px 0;">BYPASSED & ENERGIZED</div>
                        <div style="font-size:0.85rem; color:#c9d1d9;">Status: <strong style="color:#3fb950;">Hardware Safe (PE Bypass Key Active)</strong></div>
                    </div>
                """, unsafe_allow_html=True)

# =========================================================
# 7. VIEW: TIER 4 — FORENSIC VAULT
# =========================================================
elif selected_view == t["tier4_title"]:
    top_col1, top_col2 = st.columns([3, 2])
    with top_col1:
        st.title(f"⚖️ {t['tier4_title']}")
    with top_col2:
        btn_p1, btn_p2 = st.columns(2)
        with btn_p1:
            if st.button("🖨️ Print Page (PDF)", use_container_width=True):
                components.html("<script>window.parent.print();</script>", height=0, width=0)
        with btn_p2:
            days_deadlocked = active_inc.get("days_in_deadlock", 7)
            scaled_daily = int(round(87264 * scale_factor))
            total_claim_amount = scaled_daily * days_deadlocked
            
            printable_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>Pre-Litigation Cost Recovery Dossier - {active_sector}</title>
                <style>
                    body {{ font-family: Georgia, serif; margin: 40px; color: #111; line-height: 1.6; }}
                    h1, h2, h3 {{ font-family: -apple-system, sans-serif; }}
                    .card {{ border: 1px solid #333; padding: 16px; margin-bottom: 20px; }}
                    table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
                    th, td {{ border: 1px solid #999; padding: 8px 12px; text-align: left; }}
                    th {{ background: #eee; }}
                </style>
            </head>
            <body>
                <h1>CONFIDENTIAL PRE-LITIGATION SETTLEMENT DOSSIER</h1>
                <p><strong>Asset:</strong> {active_sector} | <strong>Authority:</strong> {sector['statute']} | <strong>Date:</strong> {TODAY_STR}</p>
                <div class="card">
                    <h3>Liquidated Damages Claim Demand: ${total_claim_amount:,} USD</h3>
                    <p><strong>Liable Counterparty:</strong> Apex Power Conversion Systems Corp (OEM)</p>
                    <p><strong>Breach Clause:</strong> Schedule D § 3 (Unexcused Commissioning Demurrage)</p>
                    <p><strong>Department Scope:</strong> High-Voltage Inverter & Commissioning (Dr. Arthur Pendleton Remit)</p>
                </div>
                <h2>Forensic Timeline Flight Recorder</h2>
                <table>
                    <tr><th>Timestamp</th><th>Entity</th><th>Event Description</th></tr>
                    {''.join([f"<tr><td>{e['time']}</td><td>{e['party']}</td><td>{e['event']}</td></tr>" for e in active_inc.get('forensic_timeline', [])])}
                </table>
                <h2>Primary Evidentiary Exhibits</h2>
                <table>
                    <tr><th>Exhibit Code</th><th>Title</th><th>Filename</th><th>SHA-256 Hash</th></tr>
                    {''.join([f"<tr><td>{ex['code']}</td><td>{ex['title']}</td><td>{ex['filename']}</td><td><code>{ex['sha256']}</code></td></tr>" for ex in active_inc.get('exhibits', [])])}
                </table>
                <h2>Sworn Statement of Fact</h2>
                <p><em>"I, Marcus Vance, PE (TXLIC114902), attest under penalty of perjury that on 2026-09-09 the inverter trip sequence was strictly internal to Apex firmware threshold limits, as corroborated by IEEE 2800 COMTRADE data."</em></p>
            </body>
            </html>
            """
            st.download_button(
                label="📄 Download Dossier (.HTML)",
                data=printable_html,
                file_name=f"EVIDENTIARY_DOSSIER_{active_sector.replace(' ', '_')}_{TODAY_STR}.html",
                mime="text/html",
                use_container_width=True
            )

    if st.button("↩️ Return to Tier 1: Chairman Command Post", type="secondary"):
        request_navigation(t["tier1_title"])
        
    st.divider()

    st.markdown("### 📦 Modular Evidentiary Bundles (Selective Legal Privilege Safeguard)")
    st.caption("Each operational silo generates an autonomous evidentiary bundle to prevent cross-silo discovery exposure during arbitration:")

    b_col1, b_col2, b_col3 = st.columns(3)
    with b_col1:
        st.markdown(f"""
            <div style="background:rgba(248,81,73,0.12); border:2px solid #f85149; border-radius:8px; padding:16px; height:100%;">
                <div style="font-weight:800; font-size:1.15rem; color:#f85149;">Bundle A: Inverter & OEM Hardware</div>
                <div style="font-size:0.9rem; color:#c9d1d9; margin:4px 0;">Remit: <strong>Dr. Arthur Pendleton</strong> (Tech Integrity)</div>
                <div style="font-size:0.9rem; color:#ffffff; font-weight:700;">Claim Amount: ${87264*7*scale_factor:,.0f} USD</div>
                <div style="font-size:0.85rem; color:#8b949e; margin-top:8px;">
                    Attached: COMTRADE Raw Waveforms, Badge Logs, Schedule D Demurrage.
                </div>
                <div style="font-weight:800; color:#3fb950; font-size:0.9rem; margin-top:8px;">● READY FOR DISCLOSURE</div>
            </div>
        """, unsafe_allow_html=True)
    with b_col2:
        st.markdown(f"""
            <div style="background:rgba(88,166,255,0.08); border:1px solid #30363d; border-radius:8px; padding:16px; height:100%;">
                <div style="font-weight:800; font-size:1.15rem; color:#58a6ff;">Bundle B: Interconnection Gate</div>
                <div style="font-size:0.9rem; color:#c9d1d9; margin:4px 0;">Remit: <strong>David Chen</strong> (Market Compliance)</div>
                <div style="font-size:0.9rem; color:#ffffff; font-weight:700;">Claim Amount: $0 USD (Nominal)</div>
                <div style="font-size:0.85rem; color:#8b949e; margin-top:8px;">
                    Attached: ERCOT Tariff Schedule, Utility Notice Clock Logs.
                </div>
                <div style="font-weight:800; color:#8b949e; font-size:0.9rem; margin-top:8px;">● STANDBY TRACK</div>
            </div>
        """, unsafe_allow_html=True)
    with b_col3:
        st.markdown(f"""
            <div style="background:rgba(88,166,255,0.08); border:1px solid #30363d; border-radius:8px; padding:16px; height:100%;">
                <div style="font-weight:800; font-size:1.15rem; color:#58a6ff;">Bundle C: Balance of Plant / Civil</div>
                <div style="font-size:0.9rem; color:#c9d1d9; margin:4px 0;">Remit: <strong>Eleanor Vance, CPA</strong> (Audit)</div>
                <div style="font-size:0.9rem; color:#ffffff; font-weight:700;">Claim Amount: $0 USD (Passive)</div>
                <div style="font-size:0.85rem; color:#8b949e; margin-top:8px;">
                    Attached: Contractor Mobilization Sheets, Substation Civil Sign-Offs.
                </div>
                <div style="font-weight:800; color:#8b949e; font-size:0.9rem; margin-top:8px;">● PASSIVE TRACK</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### ✍️ Sworn Evidentiary Affidavit (Lead Professional Engineer)")
    st.caption("Anchored automatically to immutable telemetry timestamps upon execution:")

    with st.container(border=True):
        st.markdown(f"""
            <div style="background:#0d1117; border-left:4px solid #3fb950; padding:14px 18px; font-family:Georgia, serif; font-size:1.05rem; line-height:1.7;">
                <strong>AFFIDAVIT OF MARCUS VANCE, PE (TXLIC114902)</strong><br>
                <em>"I, Marcus Vance, PE, in my capacity as Lead High-Voltage Commissioning Engineer for Permian HV Field Services LLC, hereby depose and state under penalty of perjury:</em><br><br>
                1. On September 9, 2026, at 08:14:02 UTC, Feeder 4A experienced an internal trip sequence on Inverter Bank 2.<br>
                2. Sub-cycle COMTRADE fault recorder logs (Exhibit A-1) prove voltage remained within IEEE 2800 nominal ride-through thresholds (4.1% THD), refuting Apex's claims of an external utility transient.<br>
                3. Badge database extracts (Exhibit B-1) confirm Apex's Commissioning Lead was off-site during the trip, disproving vendor claims of unauthorized on-site interference.<br>
                4. Pursuant to Directorate Indemnity Resolution executed under Delaware DGCL § 141(e), the Corporation has fully absorbed all liability under contested Clause 14.b."
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### ⏱️ Forensic Micro-Timeline Flight Recorder")
    with st.container(border=True):
        for event in active_inc.get("forensic_timeline", []):
            st.markdown(f"""
                <div style="padding: 10px 14px; border-bottom: 1px solid #21262d; display: flex; flex-wrap: wrap; gap: 14px; align-items: baseline;">
                    <code style="color: #58a6ff; font-weight: 700; font-size: 0.95rem;">{event['time']}</code>
                    <span style="background: rgba(227, 179, 65, 0.2); color: #e3b341; padding: 2px 8px; border-radius: 4px; font-weight: 700; font-size: 0.85rem;">{event['party']}</span>
                    <span style="color: #f0f6fc; font-size: 1.05rem; flex-grow: 1;">{event['event']}</span>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📁 Primary Evidentiary Exhibit Index")
    for exh in active_inc.get("exhibits", []):
        with st.container(border=True):
            e_col1, e_col2 = st.columns([3, 1])
            with e_col1:
                st.markdown(f"""
                    <div style="font-weight:800; font-size:1.15rem; color:#58a6ff;">{exh['code']}: {exh['title']}</div>
                    <div style="font-size:0.95rem; color:#c9d1d9; margin: 4px 0;">File: <code>{exh['filename']}</code> ({exh['size']})</div>
                    <div style="font-size:0.85rem; color:#8b949e; font-family:monospace;">SHA-256: {exh['sha256']}</div>
                    <div style="font-size:1.0rem; color:#f0f6fc; margin-top:8px;"><strong>Evidentiary Proof:</strong> {exh['significance']}</div>
                """, unsafe_allow_html=True)
            with e_col2:
                st.markdown("<div style='height:18px;'></div>", unsafe_allow_html=True)
                dummy_bytes = f"AUTHENTICATED EXHIBIT {exh['code']} - {exh['sha256']}".encode()
                st.download_button(
                    label=f"⬇️ Download {exh['code']}",
                    data=dummy_bytes,
                    file_name=exh['filename'],
                    mime="application/octet-stream",
                    use_container_width=True
                )

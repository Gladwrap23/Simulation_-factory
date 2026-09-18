import datetime
import hashlib
import json
import re
from copy import deepcopy
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

# --- HIGH-VISIBILITY COMMAND STYLING (TABLET / TACTICAL DISPLAY) ---
st.markdown("""
<style>
    /* Global Page Headings */
    h1, h2, h3 {
        color: #ffffff !important;
        font-weight: 900 !important;
        letter-spacing: 0.5px !important;
    }
    
    /* Global Streamlit Primary Buttons (Jump to Tier / Dispatch) */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #0072ff 0%, #00d4ff 100%) !important;
        color: #000000 !important;
        font-weight: 900 !important;
        font-size: 1.15rem !important;
        border: 2px solid #ffffff !important;
        border-radius: 8px !important;
        padding: 0.75rem 1.5rem !important;
        box-shadow: 0 4px 15px rgba(0, 212, 255, 0.4) !important;
        transition: all 0.2s ease-in-out !important;
    }
    div.stButton > button[kind="primary"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 212, 255, 0.7) !important;
    }

    /* Secondary Navigation Buttons (Jump / Preset Selectors) */
    div.stButton > button[kind="secondary"] {
        background: #1e293b !important;
        color: #00ff88 !important;
        font-weight: 800 !important;
        font-size: 1.05rem !important;
        border: 1.5px solid #00ff88 !important;
        border-radius: 6px !important;
    }
    div.stButton > button[kind="secondary"]:hover {
        background: #00ff88 !important;
        color: #000000 !important;
    }
</style>
""", unsafe_allow_html=True)

# iPad Safari needs an explicit scrolling surface for Streamlit's sidebar.
st.markdown("""
<style>
    section[data-testid="stSidebar"] > div {
        overflow-y: auto !important;
        -webkit-overflow-scrolling: touch !important;
        max-height: 100vh !important;
    }

    div[data-baseweb="select"] ul {
        max-height: 280px !important;
        -webkit-overflow-scrolling: touch !important;
    }
</style>
""", unsafe_allow_html=True)

# --- NATIVE PRINT & PDF EXPORT STYLING ---
st.markdown("""
<style>
@media print {
    section[data-testid="stSidebar"],
    header,
    footer,
    div.stButton,
    div[data-testid="stToolbar"],
    .stSelectbox,
    .stSlider {
        display: none !important;
    }

    body, .stApp {
        background: #ffffff !important;
        color: #000000 !important;
    }

    div[style*="background"] {
        background: #ffffff !important;
        border: 1px solid #000000 !important;
        color: #000000 !important;
        box-shadow: none !important;
    }

    h1, h2, h3, h4, span, div, strong {
        color: #000000 !important;
    }
}
</style>
""", unsafe_allow_html=True)

# --- GLOBAL OPERATING BOOKS REGISTRY ---
OPERATING_BOOKS = {
    "ERCOT BESS / Grid Storage (USA)": {
        "docket": "ERCOT IA § 4.2 Docket #54219",
        "jurisdiction": "ERCOT / Delaware (DGCL § 141)",
        "jurisdiction_options": ["ERCOT / Delaware (DGCL § 141)", "FERC / PJM Interconnection", "NYISO / New York Law"],
        "counterparty": "Apex Power Conversion Systems Corp (OEM)",
        "contract": "Turnkey EPC Agreement #TX-9011 — Schedule D § 3",
        "default_capex": 88_500_000.0,
        "daily_burn_base": 87_264.0,
        "lead_pe": "Marcus Vance, PE (TXLIC114902)",
        "lead_director": "Dr. Arthur Pendleton",
        "tech_standard": "IEEE 2800 Harmonic Breach (4.1% THD)"
    },
    "UK BESS / National Grid (UK)": {
        "docket": "Ofgem Grid Code Compliance Ref #UK-88301",
        "jurisdiction": "National Grid / England & Wales (Companies Act 2006 § 172)",
        "jurisdiction_options": ["National Grid / England & Wales (Companies Act 2006 § 172)", "Ofgem / Scots Law (Arbitration Act)"],
        "counterparty": "Vanguard Inverter Systems Ltd",
        "contract": "FIDIC Silver Book EPC #UK-BESS-04",
        "default_capex": 62_000_000.0,
        "daily_burn_base": 61_500.0,
        "lead_pe": "Alastair Finch, CEng",
        "lead_director": "Dame Eleanor Cross",
        "tech_standard": "Engineering Recommendation G99 Sub-Cycle Trip"
    },
    "NEM BESS / Hornsdale Expansion (Australia)": {
        "docket": "AEMO GPS Connection Agreement #NEM-5512",
        "jurisdiction": "AEMO NEM / New South Wales (Corporations Act 2001 § 180)",
        "jurisdiction_options": ["AEMO NEM / New South Wales (Corporations Act 2001 § 180)", "WEM / Western Australia Law"],
        "counterparty": "Australis Power Dynamics Pty",
        "contract": "AS 4300-1995 Turnkey EPC Annexure E",
        "default_capex": 115_000_000.0,
        "daily_burn_base": 112_800.0,
        "lead_pe": "Cameron Ross, FIEAust CPEng",
        "lead_director": "Marcus Thorne",
        "tech_standard": "NER S5.2.5.5 Voltage Support Non-Compliance"
    }
}

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
        "tier1_title": "Tier 1 | Chairman Tactical Command Post",
        "tier2_title": "Tier 2 | Directorate Governance Desk",
        "tier3_title": "Tier 3 | Site Operations & Operator Remediation Desk",
        "tier3a_title": "Tier 3A | Engineering Operations Command",
        "tier3b_title": "Tier 3B | Site Execution Desk",
        "tier4_title": "Tier 4 | Forensic Cost Recovery Vault",
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

# --- STRICT DESK TAXONOMY ---
DESK_OPTIONS = [
    "Tier 1 | Chairman Tactical Command Post",
    "Tier 2 | Directorate Governance Desk",
    "Tier 3A | Engineering Operations Command",
    "Tier 3B | Site Execution Desk",
    "Tier 4 | Forensic Recovery Vault"
]

if "active_desk" not in st.session_state:
    st.session_state.active_desk = DESK_OPTIONS[0]

# --- SAFE NAVIGATION HANDLER ---
def navigate_to(target_desk):
    st.session_state.active_desk = target_desk
    if "nav_radio" in st.session_state:
        st.session_state.nav_radio = target_desk

def on_sidebar_change():
    st.session_state.active_desk = st.session_state.nav_radio

def render_breadcrumb(active_index):
    stages = [
        "Tier 1: Command",
        "Tier 2: Governance",
        "Tier 3A: Eng Ops",
        "Tier 3B: Field PE",
        "Tier 4: Vault"
    ]
    trail = []
    for index, stage in enumerate(stages):
        color = "#00ff88" if index < active_index else ("#00d4ff" if index == active_index else "#64748b")
        weight = "900" if index == active_index else "700"
        trail.append(f"<span style='color:{color}; font-weight:{weight};'>{stage}</span>")
    st.markdown(
        "<div style='display:flex; align-items:center; gap:8px; flex-wrap:wrap; background:#0b1220; border:1px solid #26354d; padding:10px 14px; border-radius:6px; margin-bottom:16px; font-size:0.82rem;'>"
        + " <span style='color:#64748b;'>➔</span> ".join(trail)
        + "</div>",
        unsafe_allow_html=True
    )

def render_forward_gateway(cleared, next_desk, next_label, gateway_key):
    st.markdown("---")
    if cleared:
        st.markdown("""
            <div style="background:#062b19; border:2px solid #00ff88; padding:16px 20px; border-radius:8px; margin-bottom:15px;">
                <div style="font-size:1.15rem; font-weight:900; color:#00ff88;">✅ FORWARD EXECUTION GATE CLEARED</div>
                <div style="font-size:0.9rem; color:#f8fafc; margin-top:4px;">Prerequisites verified. Downstream operational authority is ready.</div>
            </div>
        """, unsafe_allow_html=True)
        nav_c1, nav_c2 = st.columns([1, 2])
        with nav_c1:
            st.button("⌂ Return to Command Post (Tier 1)", key=f"{gateway_key}_back", on_click=navigate_to, args=(DESK_OPTIONS[0],), use_container_width=True)
        with nav_c2:
            st.button(f"➔ PROCEED TO {next_label}", key=f"{gateway_key}_forward", on_click=navigate_to, args=(next_desk,), use_container_width=True, type="primary")
    else:
        st.info("ℹ️ Complete the required controls above to unlock the next operational tier.")
        st.button("⌂ Return to Command Post (Tier 1)", key=f"{gateway_key}_back_incomplete", on_click=navigate_to, args=(DESK_OPTIONS[0],), use_container_width=True)

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


def build_operating_book(book_name):
    """Overlay a selected global book onto the existing tiered workflow template."""
    config = OPERATING_BOOKS[book_name]
    template = SECTORS["ERCOT BESS / Grid Storage (USA)"]
    active_sector = deepcopy(template)
    active_sector["asset_cap"] = config["default_capex"]
    active_sector["baseline_docket"] = config["docket"]
    active_sector["statute"] = config["jurisdiction"]
    active_sector["operating_book"] = config

    for incident in active_sector["incidents"].values():
        incident["base_daily_bleed"] = config["daily_burn_base"]
        incident["director_seat"] = config["lead_director"]
        counterparty = incident.get("counterparty", {})
        counterparty["name"] = config["counterparty"]
        counterparty["contract"] = config["contract"]
        work_order = incident.get("tier3_work_order", {})
        work_order["field_lead"] = config["lead_pe"]
        for telemetry in work_order.get("telemetry", []):
            if telemetry["param"] == "THD Harmonics (IEEE 2800)":
                telemetry["param"] = config["tech_standard"]

    for director in active_sector["board_roster"]:
        if director.get("role") == "Cognizant Technical Director":
            director["name"] = config["lead_director"]
        if director.get("subordinate_field_lead"):
            director["subordinate_field_lead"] = config["lead_pe"]
    return active_sector

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

nav_options = DESK_OPTIONS

if "active_desk" not in st.session_state or st.session_state.active_desk not in DESK_OPTIONS:
    st.session_state.active_desk = DESK_OPTIONS[0]

if "pending_view" in st.session_state:
    st.session_state["nav_desk_selection"] = st.session_state.pop("pending_view")
    st.session_state["active_desk"] = st.session_state["nav_desk_selection"]
    components.html("""
        <script>
            window.parent.scrollTo(0, 0);
        </script>
    """, height=0, width=0)

if "nav_desk_selection" not in st.session_state or st.session_state.nav_desk_selection not in nav_options:
    st.session_state["nav_desk_selection"] = st.session_state.active_desk

if "active_desk" not in st.session_state or st.session_state.active_desk not in nav_options:
    st.session_state["active_desk"] = st.session_state.nav_desk_selection

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
if "selected_book_name" not in st.session_state:
    st.session_state.selected_book_name = st.session_state.get("selected_book", next(iter(OPERATING_BOOKS)))
if st.session_state.selected_book_name not in OPERATING_BOOKS:
    st.session_state.selected_book_name = next(iter(OPERATING_BOOKS))

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

    st.markdown("""
        <div style="font-size: 0.85rem; font-weight: 800; color: #94a3b8; text-transform: uppercase; margin-bottom: 6px; letter-spacing: 0.5px;">
            📁 OPERATING BOOK (GLOBAL DISPUTED ASSETS)
        </div>
    """, unsafe_allow_html=True)
    
    selected_book = st.selectbox(
        "Operating Book:",
        options=list(OPERATING_BOOKS.keys()),
        key="selected_book_name",
        label_visibility="collapsed"
    )
    active_cfg = OPERATING_BOOKS[selected_book]

    if st.session_state.get("last_loaded_book") != selected_book:
        st.session_state.capex_baseline = active_cfg["default_capex"]
        st.session_state.active_docket = active_cfg["docket"]
        st.session_state.active_counterparty = active_cfg["counterparty"]
        st.session_state.selected_incident_id = "INC-001"
        st.session_state.selected_director = active_cfg["lead_director"]
        st.session_state.last_loaded_book = selected_book

    st.markdown("""
        <div style="font-size: 0.85rem; font-weight: 800; color: #94a3b8; text-transform: uppercase; margin-top: 14px; margin-bottom: 6px; letter-spacing: 0.5px;">
            ⚖️ SOVEREIGN LEGAL JURISDICTION
        </div>
    """, unsafe_allow_html=True)
    selected_jurisdiction = st.selectbox(
        "Governing Jurisdiction:",
        options=active_cfg["jurisdiction_options"],
        key=f"jurisdiction_{selected_book}",
        label_visibility="collapsed"
    )
    st.session_state.active_jurisdiction = selected_jurisdiction

    active_sector = selected_book
    sector = build_operating_book(active_sector)
    sector["statute"] = selected_jurisdiction
    book_config = sector["operating_book"]
    curr_sym = sector["currency"]
    st.caption(f"Docket: {book_config['docket']}")
    st.caption(f"Law: {selected_jurisdiction}")
    st.caption(f"Counterparty: {book_config['counterparty']}")
    
    calib_key = f"capex_override_{active_sector}"
    if calib_key not in st.session_state:
        st.session_state[calib_key] = int(sector["asset_cap"])
    current_calib_capex = st.session_state[calib_key]
    scale_factor = current_calib_capex / sector["asset_cap"]

    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
    st.markdown("#### Command Desk")
    
    selected_desk = st.radio(
        "Command Desk:",
        DESK_OPTIONS,
        index=DESK_OPTIONS.index(st.session_state.active_desk) if st.session_state.active_desk in DESK_OPTIONS else 0,
        key="nav_radio",
        on_change=on_sidebar_change,
        label_visibility="collapsed"
    )
    st.session_state["nav_desk_selection"] = st.session_state.active_desk
    
    st.divider()
    st.markdown("""
        <div style="font-size: 0.8rem; font-weight: 800; color: #94a3b8; text-transform: uppercase; margin-bottom: 6px;">
            🖨️ UNIVERSAL EXPORT UTILITY
        </div>
    """, unsafe_allow_html=True)

    if st.button("🖨️ Print Desk / Save as PDF", key="btn_trigger_print", use_container_width=True):
        components.html("""
            <script>
                window.parent.print();
            </script>
        """, height=0)

    export_incident = sector["incidents"].get(
        st.session_state.selected_incident_id,
        next(iter(sector["incidents"].values()))
    )
    active_capex = st.session_state.get("capex_baseline", active_cfg["default_capex"])
    scale_factor = active_capex / sector["asset_cap"]
    daily_burn = export_incident.get("base_daily_bleed", active_cfg["daily_burn_base"]) * scale_factor
    accrued_claim = daily_burn * 7.0
    t3b_sealed = st.session_state.get("gate_3b_cleared", False)
    merkle_root = "0x8f4d92a1c674b09e13d58a74e2b091f8c412e690bb3561a09d3b749e7b25c34e" if t3b_sealed else "UNSEALED_PRE_LITIGATION_DRAFT"
    active_vector = st.session_state.get("active_defense_vector", "Vector 1: Warranty Spoliation Pretext (Clause 14.b)")
    unified_executive_bundle = f"""================================================================================
PACTUM SOVEREIGN ASSET DEFENSE SYSTEM — MASTER DOCKET BRIEF
CERTIFIED COURT & ARBITRATION FILING DOSSIER
================================================================================
DISPUTE DOCKET:    {active_cfg['docket']}
ASSET / BOOK:      {selected_book}
JURISDICTION:      {selected_jurisdiction}
COUNTERPARTY:      {active_cfg['counterparty']}
CONTRACT BASELINE: {active_cfg['contract']}

I. CAPITAL EXPOSURE & CERTIFIED LIQUIDATED DAMAGES
--------------------------------------------------------------------------------
CapEx Under Defense:        ${active_capex:,.2f} USD
Daily Burn Holding Rate:    ${daily_burn:,.2f} USD / Day
Accrued Delay Demurrage:    ${accrued_claim:,.2f} USD (7-Day Baseline)
Crossover to Total Loss:    {active_capex / daily_burn if daily_burn > 0 else 0:,.1f} Operating Days

II. STATUTORY CHAIN OF COMMAND & FIDUCIARY GOVERNANCE
--------------------------------------------------------------------------------
Tier 1 Executive Chairman:  Capital Allocation Recalibration Active
Lead Director:              {active_cfg['lead_director']}
Statutory Reliance Shield:  {selected_jurisdiction}
Active Work Order:          WO-8821-HARMONIC Dispatched

III. PHYSICAL FORENSICS & PROFESSIONAL ENGINEER ATTESTATION
--------------------------------------------------------------------------------
Lead Field PE:              {active_cfg['lead_pe']}
Technical Standard:         {active_cfg['tech_standard']}
Cryptographic Merkle Root:  {merkle_root}

IV. ACTIVE PREEMPTIVE ADVERSARIAL COUNTER-MEASURE
--------------------------------------------------------------------------------
Active Defense Vector:      {active_vector}
Remedy Demanded:            Immediate Escrow Release / ISP98 Standby LC Drawdown

CERTIFIED UNDER STATUTORY CORPORATE COVENANT.
================================================================================
"""

    st.download_button(
        label="📑 Download Full Master Docket File",
        data=unified_executive_bundle,
        file_name=f"Master_Docket_Filing_{active_cfg['docket'].replace(' ', '_').replace('#', '')}.txt",
        mime="text/plain",
        key="btn_download_full_docket",
        use_container_width=True
    )

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
if st.session_state.active_desk == DESK_OPTIONS[0]:
    render_breadcrumb(0)
    # Ultra-Prominent Tier 1 Header
    st.markdown(f"""
        <div style="background: linear-gradient(90deg, #0f172a 0%, #1e293b 100%); border-left: 8px solid #00d4ff; padding: 18px 24px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.5);">
            <div style="font-size: 2.2rem; font-weight: 900; color: #ffffff; line-height: 1.2;">
                TIER 1 | CHAIRMAN TACTICAL COMMAND POST
            </div>
            <div style="font-size: 1.15rem; font-weight: 800; color: #00d4ff; margin-top: 6px; letter-spacing: 0.5px;">
                ⚡ {active_sector.upper()} — {sector['baseline_docket']}
            </div>
            <div style="font-size: 0.95rem; font-weight: 600; color: #94a3b8; margin-top: 4px;">
                ● STATUTORY REGIME: {selected_jurisdiction} | COUNTERPARTY: {book_config['counterparty']}
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Touch-Friendly CapEx Controller for iPad
    st.markdown("#### 🎛️ Command Gateway: Project CapEx at Risk (Recalibrate)")
    
    if "capex_baseline" not in st.session_state:
        st.session_state.capex_baseline = sector["asset_cap"]

    b_col1, b_col2, b_col3, b_col4 = st.columns(4)
    if b_col1.button("Set $50M Mini-Build"):
        st.session_state.capex_baseline = 50_000_000.0
        st.rerun()
    if b_col2.button("Set Active Book Baseline"):
        st.session_state.capex_baseline = sector["asset_cap"]
        st.rerun()
    if b_col3.button("Set $150M Utility Scale"):
        st.session_state.capex_baseline = 150_000_000.0
        st.rerun()
    if b_col4.button("Set $300M Giga-Facility"):
        st.session_state.capex_baseline = 300_000_000.0
        st.rerun()

    slider_capex = st.slider(
        "Fine CapEx Recalibration ($ USD):",
        min_value=10_000_000.0,
        max_value=500_000_000.0,
        value=float(st.session_state.capex_baseline),
        step=2_500_000.0,
        format="$%.0f"
    )
    st.session_state.capex_baseline = slider_capex
    parsed_capex = int(slider_capex)

    default_base = sector["asset_cap"]
    scale_factor = slider_capex / default_base
    daily_burn = active_inc.get("base_daily_bleed", 87_264.0) * scale_factor
    weekly_burn = daily_burn * 7.0
    crossover_days = slider_capex / daily_burn if daily_burn > 0 else 0

    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #131722 0%, #1a2234 100%); border: 1px solid #ff4b4b; border-radius: 8px; padding: 18px; margin-top: 15px; margin-bottom: 20px;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; border-bottom: 1px solid rgba(255, 75, 75, 0.3); padding-bottom: 12px; margin-bottom: 14px;">
                <div>
                    <span style="background-color: #ff4b4b; color: white; padding: 3px 8px; border-radius: 4px; font-size: 0.75rem; font-weight: 800; letter-spacing: 0.5px;">ACTIVE CONTRACTUAL BREACH CLAIM</span>
                    <h3 style="margin: 8px 0 0 0; color: #ffffff; font-size: 1.25rem;">{book_config['contract']}</h3>
                    <p style="margin: 4px 0 0 0; color: #a0aec0; font-size: 0.82rem;">Liable Counterparty: <strong style="color: #ffffff;">{book_config['counterparty']}</strong> | Governing Law: {book_config['jurisdiction']}</p>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 0.75rem; color: #ff8080; font-weight: 700; text-transform: uppercase;">Certified Accrued Recovery Demand</div>
                    <div style="font-size: 1.7rem; font-weight: 900; color: #ff4b4b; line-height: 1.1;">${weekly_burn:,.0f} <span style="font-size: 0.85rem; color: #ffffff;">USD</span></div>
                    <div style="font-size: 0.78rem; color: #ff8080;">Burn Velocity: ${daily_burn:,.0f} / Day</div>
                </div>
            </div>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; font-size: 0.82rem;">
                <div style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px;">
                    <span style="color: #a0aec0; display: block; font-size: 0.72rem;">STATUTORY DEFENSE PREROGATIVE</span>
                    <strong style="color: #00d4ff;">{book_config['jurisdiction']}</strong> Statutory Shield
                </div>
                <div style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px;">
                    <span style="color: #a0aec0; display: block; font-size: 0.72rem;">CAPITAL UNDER ACTIVE DEFENSE</span>
                    <strong style="color: #00ff88;">${slider_capex:,.0f} USD</strong> (100% Escrow Intact)
                </div>
                <div style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 6px;">
                    <span style="color: #a0aec0; display: block; font-size: 0.72rem;">CROSSOVER TO TOTAL LOSS</span>
                    <strong style="color: #ffa500;">{crossover_days:,.1f} Days</strong> (At Current Bleed Rate)
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    total_burn_day = active_inc.get("base_daily_bleed", 87_264.0) * scale_factor if not is_resolved else 0
    total_burn_wk = total_burn_day * 7
    dynamic_crossover_days = round(parsed_capex / total_burn_day, 1) if total_burn_day > 0 else 999.9

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

    # --------------------------------------------------------------------------
    # OPERATIONAL CHAIN OF COMMAND (5-TIER SYNCHRONIZED HIERARCHY)
    # --------------------------------------------------------------------------
    st.markdown("#### ⚖️ Operational Chain of Command (Single-Line Descending Hierarchy)")

    st.markdown("""
        <div style="background: #111a2e; border-left: 4px solid #00d4ff; padding: 12px 16px; border-radius: 6px; margin-bottom: 8px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <strong style="color: #ffffff; font-size: 1.05rem;">🏛️ Tier 2: Directorate Governance Desk</strong>
                <span style="color: #00d4ff; font-weight: 700; font-size: 0.8rem;">SAFE HARBOR ACTIVE</span>
            </div>
            <div style="color: #94a3b8; font-size: 0.85rem; margin-top: 4px;">
                Cognizant Director: <strong>Dr. Arthur Pendleton</strong> | Statutory Shield: <strong>Delaware DGCL § 141(e)</strong>
            </div>
        </div>
    """, unsafe_allow_html=True)
    st.button(
        "➔ Drill Down to Tier 2: Directorate Governance Desk",
        key="cmd_jump_t2",
        on_click=navigate_to,
        args=(DESK_OPTIONS[1],),
        use_container_width=True
    )

    st.write("")

    t3a_cleared = st.session_state.get("gate_3a_cleared", False)
    t3a_status_color = "#00ff88" if t3a_cleared else "#ffa500"
    t3a_status_text = "WORK ORDER DISPATCHED" if t3a_cleared else "AWAITING UTILITY PACKAGING"

    st.markdown(f"""
        <div style="background: #111a2e; border-left: 4px solid {t3a_status_color}; padding: 12px 16px; border-radius: 6px; margin-bottom: 8px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <strong style="color: #ffffff; font-size: 1.05rem;">⚡ Tier 3A: Engineering Operations Command</strong>
                <span style="color: {t3a_status_color}; font-weight: 700; font-size: 0.8rem;">{t3a_status_text}</span>
            </div>
            <div style="color: #94a3b8; font-size: 0.85rem; margin-top: 4px;">
                Officer: <strong>Sarah Jenkins (VP Eng Ops)</strong> | Instrument: <strong>Work Order WO-8821-HARMONIC</strong>
            </div>
        </div>
    """, unsafe_allow_html=True)
    st.button(
        "➔ Drill Down to Tier 3A: Engineering Operations Command",
        key="cmd_jump_t3a",
        on_click=navigate_to,
        args=(DESK_OPTIONS[2],),
        use_container_width=True
    )

    st.write("")

    t3b_cleared = st.session_state.get("gate_3b_cleared", False)
    t3b_status_color = "#00ff88" if t3b_cleared else "#ff4b4b"
    t3b_status_text = "TBPE DIGITAL SEAL ACTIVE" if t3b_cleared else "ACCESS HELD (CLAUSE 14.b)"

    st.markdown(f"""
        <div style="background: #111a2e; border-left: 4px solid {t3b_status_color}; padding: 12px 16px; border-radius: 6px; margin-bottom: 8px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <strong style="color: #ffffff; font-size: 1.05rem;">👷 Tier 3B: Site Execution Desk</strong>
                <span style="color: {t3b_status_color}; font-weight: 700; font-size: 0.8rem;">{t3b_status_text}</span>
            </div>
            <div style="color: #94a3b8; font-size: 0.85rem; margin-top: 4px;">
                Field Lead: <strong>Marcus Vance, PE (TXLIC114902)</strong> | Protocol: <strong>IEEE 2800 Sub-Cycle Bypass</strong>
            </div>
        </div>
    """, unsafe_allow_html=True)
    st.button(
        "➔ Drill Down to Tier 3B: Site Execution Desk",
        key="cmd_jump_t3b",
        on_click=navigate_to,
        args=(DESK_OPTIONS[3],),
        use_container_width=True
    )

    st.write("")

    vault_status_color = "#00ff88" if t3b_cleared else "#94a3b8"
    vault_status_text = "DOSSIER SEALED" if t3b_cleared else "AUDIT BUFFER ACTIVE"
    st.markdown(f"""
        <div style="background: #111a2e; border-left: 4px solid {vault_status_color}; padding: 12px 16px; border-radius: 6px; margin-bottom: 8px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <strong style="color: #ffffff; font-size: 1.05rem;">🏛️ Tier 4: Forensic Recovery Vault</strong>
                <span style="color: {vault_status_color}; font-weight: 700; font-size: 0.8rem;">{vault_status_text}</span>
            </div>
            <div style="color: #94a3b8; font-size: 0.85rem; margin-top: 4px;">
                Evidence Custodian: <strong>Pactum Sovereign OS</strong> | Standby LC: <strong>ISP98 / UCP 600 Package</strong>
            </div>
        </div>
    """, unsafe_allow_html=True)
    st.button(
        "➔ Drill Down to Tier 4: Forensic Recovery Vault",
        key="cmd_jump_t4",
        on_click=navigate_to,
        args=(DESK_OPTIONS[4],),
        use_container_width=True
    )

# =========================================================
# 5. VIEW: TIER 2 — DIRECTORATE GOVERNANCE DESK (ELEVATED)
# =========================================================
elif st.session_state.active_desk == DESK_OPTIONS[1]:
    render_breadcrumb(1)
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

    render_forward_gateway(is_dir_signed, DESK_OPTIONS[2], "TIER 3A: ENGINEERING OPERATIONS", "t2_gateway")

# =========================================================
# 6. VIEW: TIER 3A — ENGINEERING OPERATIONS COMMAND
# =========================================================
elif st.session_state.active_desk == DESK_OPTIONS[2]:
    render_breadcrumb(2)
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

    render_forward_gateway(st.session_state.get("gate_3a_cleared", False), DESK_OPTIONS[3], "TIER 3B: SITE EXECUTION", "t3a_gateway")

# =========================================================
# 7. VIEW: TIER 3B — SITE EXECUTION & REMEDIATION DESK
# =========================================================
elif st.session_state.active_desk == DESK_OPTIONS[3]:
    st.markdown("""
        <div style="background: linear-gradient(90deg, #0f172a 0%, #1e293b 100%); border-left: 8px solid #00ff88; padding: 18px 24px; border-radius: 8px; margin-bottom: 20px;">
            <div style="font-size: 2rem; font-weight: 900; color: #ffffff;">TIER 3B | SITE EXECUTION DESK</div>
            <div style="font-size: 1.05rem; font-weight: 700; color: #00ff88; margin-top: 4px;">
                SPECIALIZED PHYSICAL ENGINEERING & STATUTORY ATTESTATION | MARCUS VANCE, PE (TXLIC114902)
            </div>
        </div>
    """, unsafe_allow_html=True)

    if not st.session_state.get("gate_3a_cleared", False):
        st.error("⚠️ ACCESS RESTRICTED: Tier 3A Work Order WO-8821-HARMONIC has not been released by Sarah Jenkins.")
        st.button("← Return to Tier 3A", on_click=navigate_to, args=(DESK_OPTIONS[2],))
        st.stop()

    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown("""
            <div style="background: #111a2e; border-top: 3px solid #00d4ff; padding: 12px; border-radius: 6px;">
                <div style="font-size: 0.75rem; color: #94a3b8;">ACTIVE WORK ORDER</div>
                <div style="font-size: 1.1rem; font-weight: 800; color: #ffffff;">WO-8821-HARMONIC</div>
                <div style="font-size: 0.75rem; color: #ff4b4b; font-weight: 600;">● P1 - CRITICAL BYPASS</div>
            </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown("""
            <div style="background: #111a2e; border-top: 3px solid #ffa500; padding: 12px; border-radius: 6px;">
                <div style="font-size: 0.75rem; color: #94a3b8;">TARGET REGULATORY GATE</div>
                <div style="font-size: 1.1rem; font-weight: 800; color: #ffffff;">Check #6 (COD Attestation)</div>
                <div style="font-size: 0.75rem; color: #a0aec0;">ERCOT Docket #54219</div>
            </div>
        """, unsafe_allow_html=True)
    with m3:
        t3b_sealed = st.session_state.get("gate_3b_cleared", False)
        st.markdown(f"""
            <div style="background: #111a2e; border-top: 3px solid {'#00ff88' if t3b_sealed else '#ff4b4b'}; padding: 12px; border-radius: 6px;">
                <div style="font-size: 0.75rem; color: #94a3b8;">STATUTORY TBPE STATUS</div>
                <div style="font-size: 1.1rem; font-weight: 800; color: {'#00ff88' if t3b_sealed else '#ff8080'};">
                    {'100% SEALED' if t3b_sealed else 'PENDING ATTESTATION'}
                </div>
                <div style="font-size: 0.75rem; color: #94a3b8;">Delaware DGCL § 141 Shield Active</div>
            </div>
        """, unsafe_allow_html=True)

    st.write("")
    p_col1, p_col2 = st.columns([3, 2])
    with p_col1:
        st.markdown("#### Execution Punch List & Statutory Sign-Off")
        s1 = st.checkbox("Step 1: Rack 4 PE Calibration & Neutral Grounding Sweep", value=st.session_state.get("t3b_s1", False), key="cb_t3b_s1")
        st.session_state.t3b_s1 = s1
        s2 = st.checkbox("Step 2: Inverter Bank 1–4 Sub-Cycle Injection Sweep (THD 4.1%)", value=st.session_state.get("t3b_s2", False), disabled=not s1, key="cb_t3b_s2")
        st.session_state.t3b_s2 = s2
        s3 = st.checkbox("Step 3: Hardware PE Key Interlock Bypass (Covenant #COV-8821)", value=st.session_state.get("t3b_s3", False), disabled=not s2, key="cb_t3b_s3")
        st.session_state.t3b_s3 = s3
        s4 = st.checkbox("Step 4: Affix Statutory PE Digital Seal & Formally Lock Evidence", value=st.session_state.get("gate_3b_cleared", False), disabled=not s3, key="cb_t3b_s4")
        st.session_state.gate_3b_cleared = s4

    with p_col2:
        st.markdown("#### Live Telemetry (Fluke 1775)")
        st.markdown("""
            <div style="background: #091322; border: 1px solid #1e293b; padding: 14px; border-radius: 6px; font-family: monospace;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;"><span style="color: #94a3b8;">THD HARMONICS:</span><strong style="color: #ff4b4b; font-size: 1.1rem;">4.1%</strong></div>
                <div style="font-size: 0.75rem; color: #64748b; margin-bottom: 12px;">Threshold: &lt; 3.0% (IEEE 2800 Breach)</div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 4px;"><span style="color: #94a3b8;">INRUSH DAMPING:</span><strong style="color: #00d4ff;">1.18 pu</strong></div>
                <div style="display: flex; justify-content: space-between;"><span style="color: #94a3b8;">RELAY COMTRADE:</span><strong style="color: #00ff88;">SYNCED (10 kHz)</strong></div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    if st.session_state.get("gate_3b_cleared", False):
        st.markdown("""
            <div style="background: #062b19; border: 2px solid #00ff88; padding: 16px 20px; border-radius: 8px; margin-bottom: 15px;">
                <div style="font-size: 1.15rem; font-weight: 900; color: #00ff88;">🔒 FIELD EXECUTION COMPLETE — CHAIN OF CUSTODY SEALED</div>
                <div style="font-size: 0.9rem; color: #f8fafc; margin-top: 4px;">Raw oscillography binaries and sworn PE affidavit (TXLIC114902) compiled into pre-litigation vault.</div>
            </div>
        """, unsafe_allow_html=True)
        b_c1, b_c2 = st.columns([1, 2])
        with b_c1:
            st.button("⌂ Command Post (Tier 1)", key="t3b_back_t1", on_click=navigate_to, args=(DESK_OPTIONS[0],), use_container_width=True)
        with b_c2:
            st.button("➔ PROCEED TO TIER 4: FORENSIC RECOVERY VAULT", key="t3b_fwd_t4", on_click=navigate_to, args=(DESK_OPTIONS[4],), use_container_width=True, type="primary")
    else:
        st.button("⌂ Return to Command Post (Tier 1)", key="t3b_back_t1_idle", on_click=navigate_to, args=(DESK_OPTIONS[0],), use_container_width=True)

# =========================================================
# 7. VIEW: TIER 4 — FORENSIC VAULT
# =========================================================
elif st.session_state.active_desk == DESK_OPTIONS[4]:
    render_breadcrumb(4)
    t3b_sealed = st.session_state.get("gate_3b_cleared", False)
    override_seal = st.toggle("⚡ Tactical Override: Force Self-Authenticating Merkle Seal", value=t3b_sealed)
    effective_seal = t3b_sealed or override_seal
    if effective_seal:
        st.session_state.gate_3b_cleared = True
        merkle_root = "0x8f4d92a1c674b09e13d58a74e2b091f8c412e690bb3561a09d3b749e7b25c34e"
        status_label = "SEALED & ADMISSIBLE (FRE 902)"
    else:
        merkle_root = "UNSEALED_DRAFT_STAGE"
        status_label = "PRE-FILING DRAFT (UNAUTHENTICATED)"
    active_capex = st.session_state.get("capex_baseline", sector["asset_cap"])
    scale_factor = active_capex / sector["asset_cap"]
    daily_burn = active_inc.get("base_daily_bleed", 87_264.0) * scale_factor
    accrued_claim = daily_burn * 7.0

    # Prominent Tier 4 Vault Title Banner
    st.markdown("""
        <div style="background: linear-gradient(90deg, #091e3a 0%, #102a45 100%); border-left: 8px solid #00ff88; padding: 20px 24px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.6);">
            <div style="font-size: 2.2rem; font-weight: 900; color: #ffffff; line-height: 1.2;">
                TIER 4 | FORENSIC RECOVERY VAULT
            </div>
            <div style="font-size: 1.1rem; font-weight: 700; color: #00ff88; margin-top: 6px;">
                IMMUTABLE PRE-LITIGATION DOSSIER & EVIDENCE CUSTODIAN AGENT (FRE 902 / ISP98)
            </div>
        </div>
    """, unsafe_allow_html=True)

    # High-Contrast Audit Status Box
    if not effective_seal:
        st.markdown("""
            <div style="background: #2b1d05; border: 2px solid #ffb703; border-left: 10px solid #ffb703; padding: 16px 20px; border-radius: 8px; margin-bottom: 25px;">
                <div style="font-size: 1.25rem; font-weight: 900; color: #ffb703; letter-spacing: 0.5px;">
                    ⚠️ PRE-FILING AUDIT STAGE: WORKING DRAFT MODE
                </div>
                <div style="font-size: 1.0rem; font-weight: 600; color: #f8fafc; margin-top: 6px; line-height: 1.4;">
                    Documents can be inspected and downloaded as unsealed discovery drafts.
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style="background: #062b19; border: 2px solid #00ff88; border-left: 10px solid #00ff88; padding: 16px 20px; border-radius: 8px; margin-bottom: 25px;">
                <div style="font-size: 1.25rem; font-weight: 900; color: #00ff88; letter-spacing: 0.5px;">
                    🔒 CHAIN OF CUSTODY SEALED | MERKLE ROOT ACTIVE
                </div>
                <div style="font-size: 1.0rem; font-weight: 600; color: #f8fafc; margin-top: 6px; line-height: 1.4;">
                    Statutory conditions met under FRE 902(14). Master court package ready for immediate filing.
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("#### Evidentiary Completeness Audit (Self-Authenticating Rule 902 Baseline)")
    
    evidence_items = [
        {"Doc": "DGCL § 141(e) Corporate Safe-Harbor Resolution", "Owner": "Dr. Arthur Pendleton", "Status": "Verified & Bound", "Admissibility": "FRE 902(11)"},
        {"Doc": "Substation Work Order WO-8821-HARMONIC", "Owner": "Sarah Jenkins (VP Eng)", "Status": "Executed & Stamped", "Admissibility": "FRE 803(6)"},
        {"Doc": "COMTRADE 10 kHz Oscillography (THD 4.1%)", "Owner": "Substation Relay R-04", "Status": "SHA-256 Validated", "Admissibility": "FRE 902(13)"},
        {"Doc": "Sworn Field Affidavit & Licensure Attestation", "Owner": "Marcus Vance, PE (TXLIC114902)", "Status": "Digitally Sealed" if effective_seal else "Draft - Pending Stamp", "Admissibility": "FRE 902(14)"},
        {"Doc": "Fluke 1775 Power Quality Analyzer Calibration Cert", "Owner": "Permian HV Labs (ISO 17025)", "Status": "Current (Exp: Dec 2026)", "Admissibility": "FRE 702 Foundational"}
    ]

    cols = st.columns([3, 2, 2, 2])
    cols[0].markdown("**Contemporaneous Instrument**")
    cols[1].markdown("**Originating Authority**")
    cols[2].markdown("**Audit Clearance**")
    cols[3].markdown("**Rules of Evidence**")

    for item in evidence_items:
        c = st.columns([3, 2, 2, 2])
        c[0].write(item["Doc"])
        c[1].write(item["Owner"])
        if effective_seal or "Current" in item["Status"] or "Verified" in item["Status"]:
            c[2].markdown(f"<span style='color: #00ff88; font-weight:600;'>● {item['Status']}</span>", unsafe_allow_html=True)
        else:
            c[2].markdown(f"<span style='color: #ffa500; font-weight:600;'>○ {item['Status']}</span>", unsafe_allow_html=True)
        c[3].write(item["Admissibility"])

    st.markdown("---")

    # --------------------------------------------------------------------------
    # FORENSIC FLIGHT RECORDER: SYNCHRONIZED MICRO-TIMELINE
    # --------------------------------------------------------------------------
    st.markdown("#### ⏱️ Contemporaneous Forensic Flight Recorder (Micro-Timeline)")
    st.caption("Millisecond-level synchronization of technical trip telemetry to commercial default milestones.")

    timeline_events = [
        {
            "time": "08:14:02.104 UTC",
            "event": "CRITICAL TELEMETRY TRIP: Inverter Bank 2 Harmonic Distortion",
            "actor": "Substation Relay R-04",
            "rule": "IEEE 2800 Breach",
            "detail": "THD spiked to 4.1% against 3.0% threshold. Hardware lockout triggered automatically.",
            "impact": "Generation halted. Interface trip recorded on COMTRADE bus.",
            "tag_color": "#ff4b4b"
        },
        {
            "time": "09:30:15.000 UTC",
            "event": "FORMAL NOTICE DISPATCHED: Schedule D § 3 Cure Demand",
            "actor": "Project Legal / Sarah Jenkins",
            "rule": "Turnkey EPC Clause 11.2",
            "detail": "Automated demand transmitted via EDI/Notice Gateway to Apex Power Systems. 90-minute cure window opened.",
            "impact": "Notice clock starts. Proof of receipt confirmed by carrier.",
            "tag_color": "#00d4ff"
        },
        {
            "time": "11:00:44.210 UTC",
            "event": "COUNTERPARTY DEFAULT: Apex PCS Refuses Site Dispatch",
            "actor": "Apex PCS OEM Dispatch",
            "rule": "Anticipatory Repudiation",
            "detail": "OEM asserts bad-faith Clause 14.b warranty voidance pretext. Refuses firmware patch or field engineer dispatch.",
            "impact": "Commercial deadlock confirmed. Demurrage accrual commences.",
            "tag_color": "#ff8080"
        },
        {
            "time": "11:01:00.000 UTC",
            "event": "LIQUIDATED CLAIM ACCRUAL: Unexcused Standby Demurrage",
            "actor": "Autonomous Telemetry Engine",
            "rule": "Schedule D § 3 Demurrage",
            "detail": f"Holding burn velocity locked at ${daily_burn / 24:,.2f}/hr (${daily_burn:,.2f}/day). Total escrow exposure actively compiling.",
            "impact": f"Accrual running. Current milestone balance: ${accrued_claim:,.2f} USD.",
            "tag_color": "#ffa500"
        },
        {
            "time": "14:45:00.000 UTC",
            "event": "STATUTORY PE BYPASS: Corporate Covenant #COV-8821 Activated",
            "actor": "Marcus Vance, PE (TXLIC114902)",
            "rule": "Delaware DGCL § 141(e)",
            "detail": "Physical engineering bypass of OEM lockouts under corporate board indemnity. Fluke 1775 logs sealed.",
            "impact": "Field recovery initiated. Chain of custody secured for arbitration.",
            "tag_color": "#00ff88"
        }
    ]

    event_options = [f"{ev['time']} — {ev['event']}" for ev in timeline_events]
    selected_idx = st.selectbox(
        "Scrub Flight Recorder Events (Inspect Cryptographic Event Payload):",
        range(len(timeline_events)),
        format_func=lambda x: event_options[x]
    )

    ev = timeline_events[selected_idx]

    st.markdown(f"""
        <div style="background: #131d2e; border: 2px solid {ev['tag_color']}; border-left: 8px solid {ev['tag_color']}; padding: 18px 20px; border-radius: 8px; margin-top: 10px; margin-bottom: 20px;">
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 10px; margin-bottom: 12px;">
                <span style="color: {ev['tag_color']}; font-weight: 900; font-size: 1.1rem;">RECORDED TIMESTAMP: {ev['time']}</span>
                <span style="background: rgba(255,255,255,0.1); color: #ffffff; padding: 4px 10px; border-radius: 4px; font-weight: 700; font-size: 0.85rem;">{ev['rule']}</span>
            </div>
            <div style="font-size: 1.2rem; font-weight: 800; color: #ffffff; margin-bottom: 8px;">{ev['event']}</div>
            <div style="color: #cbd5e0; font-size: 0.95rem; line-height: 1.5; margin-bottom: 12px;">{ev['detail']}</div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; font-size: 0.85rem; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 10px;">
                <div><strong style="color: #a0aec0;">Originating Entity / Relay:</strong> <span style="color: #ffffff;">{ev['actor']}</span></div>
                <div><strong style="color: #a0aec0;">Legal / Financial Consequence:</strong> <span style="color: #00ff88;">{ev['impact']}</span></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("#### Master Evidentiary Custodian Package")
    master_dossier_text = f"""MASTER FORENSIC FLIGHT RECORDER & PRE-LITIGATION DOSSIER
Docket: ERCOT IA § 4.2 Interconnection Docket #54219
Claim Amount: ${accrued_claim:,.2f} USD
Holding Velocity: ${daily_burn:,.2f} / Day
Merkle Root: {merkle_root}
Lead PE: Marcus Vance, PE (TXLIC114902)
Status: {status_label}
"""

    st.download_button(
        label="📥 Download Complete Master Forensic Flight Recorder Dossier (Full Job)",
        data=master_dossier_text,
        file_name="Master_Forensic_Dossier_Docket_54219_Full.txt",
        mime="text/plain",
        use_container_width=True,
        type="primary"
    )

    st.markdown("---")

    ex1, ex2 = st.columns(2)
    with ex1:
        st.markdown("**Surgical Exhibit Extracts**")
        st.download_button("Exhibit A: Board Safe-Harbor Bundle (PDF)", "CERTIFIED EXHIBIT A - DGCL 141 RESOLUTION", "Exhibit_A_Governance_Shield.pdf", use_container_width=True)
        st.download_button("Exhibit B: PE Waveform Binary (CSV)", "COMTRADE_TIMESTAMP,FREQ_HZ,THD_PERCENT\n08:14:02.104,59.98,4.12", "Exhibit_B_IEEE2800_Waveform.csv", use_container_width=True)
    with ex2:
        st.markdown("**Standby Letter of Credit Protocol (ISP98 / UCP 600)**")
        st.caption("Strict-compliance statutory demand served upon Issuing Escrow Bank.")

        lc_reference = "LC-TX-9011-APEX-DEMURRAGE"
        issuing_bank = "JPMorgan Chase Bank, N.A. / Global Infrastructure Escrow"
        applicant = "Apex Power Conversion Systems Corp"
        beneficiary = "Pactum Sovereign Escrow Holdings LLC"

        lc_demand_payload = f"""================================================================================
FORMAL DEMAND FOR PAYMENT UNDER STANDBY LETTER OF CREDIT
GOVERNING RULES: INTERNATIONAL STANDBY PRACTICES 1998 (ICC PUBLICATION NO. 590 - ISP98)
SUBJECT TO UNIFORM CUSTOMS AND PRACTICE FOR DOCUMENTARY CREDITS (UCP 600)
================================================================================

TO:      {issuing_bank}
         Global Trade & Escrow Services Desk
DATE:    18 September 2026
REF NO:  {lc_reference}

APPLICANT:   {applicant}
BENEFICIARY: {beneficiary}
AMOUNT:      ${accrued_claim:,.2f} USD

I. STATUTORY DEMAND STATEMENT
--------------------------------------------------------------------------------
The undersigned Authorized Officer of {beneficiary} ("Beneficiary")
hereby certifies under penalty of perjury that:

1. DEFAULT EVENT:
   The Applicant, {applicant}, has defaulted under Turnkey EPC
   Agreement #TX-9011, Schedule D § 3 (Unexcused Commercial Demurrage) by failing
   to cure harmonic compliance trips exceeding IEEE 2800 limits (THD 4.1%).

2. UNPAID LIQUIDATED DAMAGES:
   The sum of ${accrued_claim:,.2f} USD represents accrued, certified, and
   unpaid liquidated delay damages due from Applicant as confirmed by contemporaneous
   relational flight recorder telemetry Docket #54219.

3. NOTICE COMPLIANCE:
   Beneficiary has served formal notice of default and cure demand pursuant to
   Clause 11.2 of the Turnkey Agreement. All contractual cure periods have lapsed
   without remediation or engineer site dispatch by Applicant.

4. DRAW CONDITION SATISFACTION:
   Beneficiary demands payment in full within three (3) banking days of receipt
   of this presentation pursuant to ISP98 Rule 5.01.

II. SETTLEMENT WIRE INSTRUCTIONS
--------------------------------------------------------------------------------
Bank:          Pactum Commercial Escrow Trust
Routing / ABA: 021000021
Swift Code:    CHASUS33XXX
Account No:    9011-ERCOT-54219-CAPDEF
Special Inst:  Hold for Settlement of Docket #54219 Demurrage Burn

III. STATUTORY DIGITAL ATTESTATION
--------------------------------------------------------------------------------
Seal Hash:      {merkle_root}
Signatory:      Marcus Vance, PE (TXLIC114902) — Chief Attestation Engineer
Authentication: Delaware DGCL § 141(e) Corporate Safe-Harbor Conveyance
================================================================================
"""

        st.download_button(
            label=f"🏛️ Dispatch & Download ISP98 Demand Certificate ({'SEALED' if effective_seal else 'DRAFT'})",
            data=lc_demand_payload,
            file_name=f"Standby_LC_Drawdown_Demand_{lc_reference}_{'SEALED' if effective_seal else 'DRAFT'}.txt",
            mime="text/plain",
            type="primary",
            use_container_width=True,
            key="lc_btn_active"
        )
        st.caption("● Available for discovery testing; certified banking presentation requires the active seal state.")

    # --------------------------------------------------------------------------
    # ADVERSARIAL PREEMPTION & JUDICIAL STRESS-TEST MATRIX
    # --------------------------------------------------------------------------
    st.markdown("---")
    st.markdown("#### 🛡️ Adversarial Preemption & Judicial Defense Matrix")
    st.caption("Anticipatory defense vectors, evidentiary sufficiency scoring, and counter-briefs for Chancery Court / AAA-ICDR Arbitration.")

    defense_vectors = {
        "Vector 1: Warranty Spoliation Pretext (Clause 14.b)": {
            "risk_level": "CRITICAL OPPOSING DEFENSE",
            "risk_color": "#ff4b4b",
            "opposing_claim": "Apex litigation counsel will argue Marcus Vance, PE's physical interlock override constituted unauthorized equipment tampering, nullifying OEM warranty covenants and barring liquidated delay damages.",
            "statutory_shield": "Delaware DGCL § 141(e) Corporate Mitigation Defense",
            "evidentiary_proof": "Relay R-04 oscillography binary confirms inverter harmonic failure (THD 4.1%) occurred at 08:14 UTC, 6 hours PRIOR to site intervention. Physical bypass was legally required to mitigate grid disassociation damages under emergency duty of care.",
            "precedent": "In re Caremark Int'l Inc. Derivative Litig., 698 A.2d 959 (Del. Ch. 1996) / Restatement (Second) of Contracts § 350 (Avoidable Consequences).",
            "admissibility_confidence": "96.4% Evidentiary Preemption",
            "brief_code": "MOT-REBUTTAL-14B"
        },
        "Vector 2: Digital Hearsay & Spoiled Telemetry (FRE 802 / 901)": {
            "risk_level": "EVIDENTIARY CHALLENGE",
            "risk_color": "#ffa500",
            "opposing_claim": "Apex will file motions in limine asserting COMTRADE digital capture files are proprietary, unverified hearsay prone to digital modification or software artifacts.",
            "statutory_shield": "FRE 902(13) & 902(14) Self-Authenticating Digital Records",
            "evidentiary_proof": "Fluke 1775 Power Quality Analyzer certified under ISO/IEC 17025 calibration (Cert #ISO-8821). Data secured by SHA-256 Merkle root and accompanied by certified custodial affidavit from Marcus Vance, PE under criminal perjury penalties.",
            "precedent": "United States v. Lizarraga-Tirado, 789 F.3d 1107 (9th Cir. 2015) (Machine-generated data is not hearsay); FRE 902(14) Certification Process.",
            "admissibility_confidence": "99.1% Evidentiary Preemption",
            "brief_code": "MOT-LIMINE-FRE902"
        },
        "Vector 3: Notice Precondition & Cure Period Laches (Clause 11.2)": {
            "risk_level": "PROCEDURAL ATTRITION",
            "risk_color": "#00d4ff",
            "opposing_claim": "Apex will assert formal contractual cure notice was procedurally defective or untimely, claiming the 90-minute remedy window never commenced.",
            "statutory_shield": "Turnkey EPC Agreement § 11.2 Notice Verification",
            "evidentiary_proof": "Automated EDI carrier dispatch stamped 09:30:15 UTC with cryptographic delivery acknowledgement from Apex enterprise mail gateway. Commercial deadlock verified after 90-minute cure expiry at 11:00 UTC.",
            "precedent": "Restatement (Second) of Contracts § 251 (Failure to Give Adequate Assurance as Breach).",
            "admissibility_confidence": "98.7% Evidentiary Preemption",
            "brief_code": "MOT-SUMMARY-CURE-11.2"
        }
    }

    vec_keys = list(defense_vectors.keys())
    if "active_defense_vector" not in st.session_state or st.session_state.active_defense_vector not in vec_keys:
        st.session_state.active_defense_vector = vec_keys[0]

    st.markdown("""
        <div style="font-size: 0.9rem; font-weight: 800; color: #ffb703; margin-top: 15px; margin-bottom: 10px; text-transform: uppercase;">
            ⚠️ TACTICAL INJECT: Tap an adversarial attack vector below to load the statutory counter-measure
        </div>
    """, unsafe_allow_html=True)

    v_col1, v_col2, v_col3 = st.columns(3)
    with v_col1:
        if st.button(
            "1️⃣ Warranty Spoliation",
            type="primary" if st.session_state.active_defense_vector == vec_keys[0] else "secondary",
            use_container_width=True,
            key="defense_vector_1"
        ):
            st.session_state.active_defense_vector = vec_keys[0]
            st.rerun()
    with v_col2:
        if st.button(
            "2️⃣ Digital Hearsay (FRE 802)",
            type="primary" if st.session_state.active_defense_vector == vec_keys[1] else "secondary",
            use_container_width=True,
            key="defense_vector_2"
        ):
            st.session_state.active_defense_vector = vec_keys[1]
            st.rerun()
    with v_col3:
        if st.button(
            "3️⃣ Notice Precondition",
            type="primary" if st.session_state.active_defense_vector == vec_keys[2] else "secondary",
            use_container_width=True,
            key="defense_vector_3"
        ):
            st.session_state.active_defense_vector = vec_keys[2]
            st.rerun()

    selected_vector_name = st.session_state.active_defense_vector
    vec = defense_vectors[selected_vector_name]

    st.markdown(f"""
        <div style="background: #111a2e; border: 2px solid {vec['risk_color']}; border-left: 8px solid {vec['risk_color']}; padding: 18px 20px; border-radius: 8px; margin-top: 10px; margin-bottom: 20px;">
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 10px; margin-bottom: 12px;">
                <span style="background: {vec['risk_color']}; color: #000000; padding: 4px 8px; border-radius: 4px; font-weight: 900; font-size: 0.8rem;">{vec['risk_level']}</span>
                <span style="color: #00ff88; font-weight: 800; font-size: 0.95rem;">🛡️ {vec['admissibility_confidence']}</span>
            </div>
            <div style="margin-bottom: 12px;"><span style="color: #94a3b8; font-size: 0.78rem; font-weight: 700; text-transform: uppercase;">Opposing Litigation Counsel Assertions</span>
                <div style="color: #ffffff; font-size: 0.95rem; line-height: 1.4; margin-top: 4px;">{vec['opposing_claim']}</div>
            </div>
            <div style="margin-bottom: 12px;"><span style="color: #00d4ff; font-size: 0.78rem; font-weight: 700; text-transform: uppercase;">Statutory Rebuttal & Preemptive Shield</span>
                <div style="color: #ffffff; font-weight: 700; font-size: 1.05rem; margin-top: 2px;">{vec['statutory_shield']}</div>
                <div style="color: #cbd5e0; font-size: 0.9rem; line-height: 1.4; margin-top: 4px;">{vec['evidentiary_proof']}</div>
            </div>
            <div style="border-top: 1px solid rgba(255,255,255,0.05); padding-top: 10px; font-size: 0.82rem;"><strong style="color: #94a3b8;">Controlling Case Precedent:</strong> <span style="color: #e2e8f0; font-style: italic;">{vec['precedent']}</span></div>
        </div>
    """, unsafe_allow_html=True)

    rebuttal_payload = f"""================================================================================
IN THE DELAWARE COURT OF CHANCERY / AAA ARBITRATION PANEL
DOCKET NO. {st.session_state.get('active_docket', '54219')}
================================================================================
CLAIMANT:    PACTUM SOVEREIGN ASSET DEFENSE TRUST
RESPONDENT:  APEX POWER CONVERSION SYSTEMS CORP

PREEMPTIVE EMERGENCY REBUTTAL BRIEF: {vec['brief_code']}
SUBJECT: REBUTTAL OF RESPONDENT DEFENSE REGARDING {selected_vector_name.upper()}
================================================================================

I. COUNTERPARTY CONTENTION
--------------------------------------------------------------------------------
{vec['opposing_claim']}

II. STATUTORY PREEMPTION & CONTROLLING AUTHORITY
--------------------------------------------------------------------------------
{vec['statutory_shield']}
Authority: {vec['precedent']}

III. CONTEMPORANEOUS EVIDENTIARY RECORD (FRE 902)
--------------------------------------------------------------------------------
{vec['evidentiary_proof']}

Accrued Delay Demurrage Demanded: ${accrued_claim:,.2f} USD
Cryptographic Flight Recorder Root: {merkle_root}
Attesting Engineer: Marcus Vance, PE (TXLIC114902)

IV. CONCLUSION & PRAYER FOR RELIEF
--------------------------------------------------------------------------------
Claimant requests an immediate order striking Respondent's pretextual defense
and ordering the immediate drawdown of Standby Escrow Collateral under ISP98.

SUBMITTED UNDER RULE 11 CERTIFICATION.
================================================================================
"""

    st.download_button(
        label=f"📄 Generate Preemptive Rebuttal Motion Brief ({vec['brief_code']})",
        data=rebuttal_payload,
        file_name=f"Emergency_Rebuttal_Brief_{vec['brief_code']}.txt",
        mime="text/plain",
        key="btn_rebuttal_download",
        use_container_width=True
    )

else:
    # Failsafe: Prevent blank screens on any state mismatch.
    st.session_state.active_desk = DESK_OPTIONS[0]
    st.rerun()

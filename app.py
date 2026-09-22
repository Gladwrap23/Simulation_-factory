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
    "Tier 1A | Chairman Tactical Command Post",
    "Tier 1B | General Counsel Legal Chambers",
    "Tier 2A | Chairman Directorate Governance",
    "Tier 2B | Legal Counsel Governance Desk",
    "Tier 3A | Engineering Operations Command",
    "Tier 3B | Site Execution Desk",
    "Tier 4 | Forensic Recovery Vault"
]

if "active_desk" not in st.session_state:
    st.session_state.active_desk = DESK_OPTIONS[0]

# --- DUAL-TRACK GROUPING (COMMERCIAL/OPS vs LEGAL/STATUTORY) ---
TRACK_COMMERCIAL = "👔 Commercial & Operations Track"
TRACK_LEGAL = "⚖️ Legal & Statutory Track"
COMMERCIAL_DESKS = [DESK_OPTIONS[0], DESK_OPTIONS[2], DESK_OPTIONS[4], DESK_OPTIONS[5], DESK_OPTIONS[6]]
LEGAL_TIER3_LABEL = "Tier 3 | Regulatory & Interconnection Audit"
LEGAL_TIER4_LABEL = "Tier 4 | Legal Evidence & Collateral Vault"
LEGAL_DESKS = [DESK_OPTIONS[1], DESK_OPTIONS[3], LEGAL_TIER3_LABEL, LEGAL_TIER4_LABEL]

# --- DUAL-KEY INCEPTION INTERLOCK STATE ---
if "key_chairman_armed" not in st.session_state:
    st.session_state.key_chairman_armed = False
if "key_counsel_armed" not in st.session_state:
    st.session_state.key_counsel_armed = False
if "docket_inception_sealed" not in st.session_state:
    st.session_state.docket_inception_sealed = False
if "inception_timestamp" not in st.session_state:
    st.session_state.inception_timestamp = None
if "inception_hash" not in st.session_state:
    st.session_state.inception_hash = None
if "gate_2a_cleared" not in st.session_state:
    st.session_state.gate_2a_cleared = False
if "gate_2b_cleared" not in st.session_state:
    st.session_state.gate_2b_cleared = False
if "legal_identity" not in st.session_state:
    st.session_state.legal_identity = "General Counsel & CLO"

def toggle_chairman_key():
    st.session_state.key_chairman_armed = not st.session_state.key_chairman_armed
    _evaluate_dual_seal()

def toggle_counsel_key():
    st.session_state.key_counsel_armed = not st.session_state.key_counsel_armed
    _evaluate_dual_seal()

def _evaluate_dual_seal():
    if st.session_state.key_chairman_armed and st.session_state.key_counsel_armed:
        st.session_state.docket_inception_sealed = True
        st.session_state.inception_timestamp = "21 Sept 2026 14:45:00 UTC"
        st.session_state.inception_hash = "sha256:7a9e8841c30f4d89a2b1011894cf9983de092bbfca31998e104928fe88102abc"
    else:
        st.session_state.docket_inception_sealed = False

def render_inception_guard():
    if not st.session_state.get("docket_inception_sealed", False):
        st.markdown("""
            <div style="background: #1c1408; border: 1px solid #ffa500; padding: 12px 16px; border-radius: 6px; margin-bottom: 16px;">
                <strong style="color: #ffa500;">⚠️ SIMULATION / READ-ONLY NOTICE:</strong>
                <span style="color: #cbd5e0; font-size: 0.88rem;">
                    The active docket has not been formally instated under the Dual-Key Protocol.
                    Actions taken here remain non-binding simulations.
                </span>
            </div>
        """, unsafe_allow_html=True)

# --- SAFE NAVIGATION HANDLER ---
def navigate_to(target_desk):
    st.session_state.active_desk = target_desk
    if "nav_radio" in st.session_state:
        st.session_state.nav_radio = target_desk
    # Keep the dual-track sidebar radios in lockstep with cross-track jumps.
    if target_desk in LEGAL_DESKS:
        st.session_state.active_track_selector = TRACK_LEGAL
        if "radio_legal_desks" in st.session_state:
            st.session_state.radio_legal_desks = target_desk
    else:
        st.session_state.active_track_selector = TRACK_COMMERCIAL
        if "radio_commercial_desks" in st.session_state:
            st.session_state.radio_commercial_desks = target_desk

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


def render_top_action_bar():
    """Render executive print and dossier actions beneath the active breadcrumb."""
    top_col1, top_col2, top_col3 = st.columns([3, 1, 1])
    with top_col1:
        st.caption("Active Telemetry Engine: **Pactum Sovereign OS Build v6.8** | Real-Time Docket Audit")
    with top_col2:
        if st.button("🖨️ Print / PDF", key="top_quick_print", use_container_width=True):
            components.html("""<script>window.parent.print();</script>""", height=0)
    with top_col3:
        st.download_button(
            label="📑 Case File",
            data=unified_executive_bundle,
            file_name=f"Master_Case_File_{active_cfg['docket'].replace(' ', '_').replace('#', '')}.txt",
            mime="text/plain",
            key="top_quick_docket",
            use_container_width=True
        )
    st.markdown("---")

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

nav_options = DESK_OPTIONS + [LEGAL_TIER3_LABEL, LEGAL_TIER4_LABEL]

if "active_desk" not in st.session_state or st.session_state.active_desk not in nav_options:
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

    # ==============================================================================
    # SIDEBAR: DUAL-TRACK NAVIGATION ENGINE
    # ==============================================================================
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🎛️ Command Desk")

    # Top-level Track Selector
    track_selection = st.sidebar.radio(
        "Select Operating Track:",
        [TRACK_COMMERCIAL, TRACK_LEGAL],
        key="active_track_selector"
    )

    if track_selection == TRACK_COMMERCIAL:
        if st.session_state.get("active_desk") not in COMMERCIAL_DESKS:
            st.session_state.active_desk = COMMERCIAL_DESKS[0]

        selected_desk = st.sidebar.radio(
            "Commercial Hierarchy:",
            COMMERCIAL_DESKS,
            index=COMMERCIAL_DESKS.index(st.session_state.active_desk),
            key="radio_commercial_desks"
        )
        st.session_state.active_desk = selected_desk

    else:
        if st.session_state.get("active_desk") not in LEGAL_DESKS:
            st.session_state.active_desk = LEGAL_DESKS[0]

        selected_desk = st.sidebar.radio(
            "Legal Hierarchy:",
            LEGAL_DESKS,
            index=LEGAL_DESKS.index(st.session_state.active_desk),
            key="radio_legal_desks"
        )
        st.session_state.active_desk = selected_desk

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
            request_navigation(DESK_OPTIONS[0])

if st.session_state.selected_incident_id not in sector["incidents"]:
    st.session_state.selected_incident_id = next(iter(sector["incidents"]))
active_inc = sector["incidents"][st.session_state.selected_incident_id]
is_resolved = active_inc.get("status") == "RESOLVED"
is_dir_signed = active_inc.get("director_signed", False) or is_resolved
is_bypassed = active_inc.get("manual_pe_bypass", False) or is_resolved
if st.session_state.trigger_print:
    st.session_state.trigger_print = False
    components.html("<script>window.parent.print();</script>", height=0, width=0)

# ==============================================================================
# TIER 1A: CHAIRMAN TACTICAL COMMAND POST (COMMERCIAL PREROGATIVE)
# ==============================================================================
if st.session_state.active_desk == DESK_OPTIONS[0]:
    cfg = book_config
    # 1. State Synchronization Callbacks
    if "capex_baseline" not in st.session_state:
        st.session_state.capex_baseline = float(cfg["default_capex"])
    if "slider_chair_capex" not in st.session_state:
        st.session_state.slider_chair_capex = float(st.session_state.capex_baseline)
    if "burn_halted" not in st.session_state:
        st.session_state.burn_halted = False

    def set_capex_preset(target_amount):
        """Forces both the baseline state and slider state to update simultaneously."""
        st.session_state.capex_baseline = float(target_amount)
        st.session_state.slider_chair_capex = float(target_amount)

    def on_slider_move():
        """Updates baseline whenever the slider is manually dragged."""
        st.session_state.capex_baseline = float(st.session_state.slider_chair_capex)

    is_sealed = st.session_state.get("docket_inception_sealed", False)
    k1 = st.session_state.get("key_chairman_armed", False)
    k2 = st.session_state.get("key_counsel_armed", False)
    current_capex = float(st.session_state.capex_baseline)

    # 2. STATUS BANNER
    if is_sealed:
        st.markdown(f"""
            <div style="background: #062b19; border: 2px solid #00ff88; border-left: 8px solid #00ff88; padding: 16px 20px; border-radius: 8px; margin-bottom: 20px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-size: 1.1rem; font-weight: 900; color: #00ff88;">🔒 DOCKET INCEPTION CHARTER SEALED // COMMERCIALLY BOUND</span>
                    <span style="background: #00ff88; color: #04101e; font-size: 0.75rem; font-weight: 900; padding: 2px 8px; border-radius: 4px;">ARMED & BOUND</span>
                </div>
                <div style="color: #cbd5e0; font-size: 0.85rem; margin-top: 4px;">
                    Dual-Key satisfied. Balance sheet committed at <strong>${current_capex:,.0f} USD</strong>.
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div style="background: #1c1408; border: 2px solid #ffa500; border-left: 8px solid #ffa500; padding: 16px 20px; border-radius: 8px; margin-bottom: 20px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-size: 1.1rem; font-weight: 900; color: #ffa500;">⚠️ STRATEGIC SANDBOX MODE // NON-BINDING SCENARIO MODELING</span>
                    <span style="background: #ffa500; color: #000; font-size: 0.75rem; font-weight: 900; padding: 2px 8px; border-radius: 4px;">SANDBOX</span>
                </div>
                <div style="color: #cbd5e0; font-size: 0.85rem; margin-top: 4px;">
                    Recalibrate capital exposure below. Turning Key 1 binds this balance-sheet floor to the court docket.
                </div>
                <div style="display: flex; gap: 20px; margin-top: 8px; font-size: 0.82rem; font-weight: 800;">
                    <span style="color: {'#00ff88' if k1 else '#ff4b4b'};">{'✓' if k1 else '○'} KEY 1 (CHAIRMAN): {'ARMED & COMMITTED' if k1 else 'PENDING AUTHORIZATION'}</span>
                    <span style="color: {'#00ff88' if k2 else '#ffa500'};">{'✓' if k2 else '○'} KEY 2 (GENERAL COUNSEL): {'ARMED' if k2 else 'PENDING LEGAL CHAMBERS'}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # 3. CAPEX PRESETS WITH DIRECT ON_CLICK CALLBACKS
    st.markdown("#### 🎛️ Command Gateway: Project CapEx at Risk (Recalibrate)")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        base_val = float(cfg["default_capex"])
        st.button(f"⭐ Reset Base (${base_val/1e6:,.1f}M)", key="btn_px_base", on_click=set_capex_preset, args=(base_val,), use_container_width=True)
    with c2:
        st.button("$50M Mini-Build", key="btn_px_50m", on_click=set_capex_preset, args=(50_000_000.0,), use_container_width=True)
    with c3:
        st.button("$150M Utility-Scale", key="btn_px_150m", on_click=set_capex_preset, args=(150_000_000.0,), use_container_width=True)
    with c4:
        st.button("$300M Giga-Facility", key="btn_px_300m", on_click=set_capex_preset, args=(300_000_000.0,), use_container_width=True, type="primary" if current_capex == 300_000_000.0 else "secondary")

    # 4. SLIDER BOUND DIRECTLY TO ON_CHANGE
    st.slider(
        "Fine CapEx Recalibration ($ USD):",
        min_value=25_000_000.0,
        max_value=500_000_000.0,
        step=5_000_000.0,
        format="$%d",
        key="slider_chair_capex",
        on_change=on_slider_move
    )

    # --- METRICS & STANDSTILL CONTROL (COMPACT UTILITY) ---
    scale_factor = current_capex / float(cfg["default_capex"])
    daily_burn = float(cfg["daily_burn_base"]) * scale_factor
    accrued_7day = daily_burn * 7.0

    st.write("")
    m1, m2, m3 = st.columns(3)
    m1.metric("Balance Sheet CapEx", f"${current_capex:,.0f}")

    if st.session_state.burn_halted:
        m2.metric("Daily Holding Burn", "$0.00 / day", delta="STANDSTILL ACTIVE", delta_color="inverse")
        m3.metric("Accrued Demurrage (7-Day)", f"${accrued_7day:,.2f}", delta="FROZEN", delta_color="off")
    else:
        m2.metric("Daily Holding Burn", f"${daily_burn:,.2f} / day")
        m3.metric("Accrued Demurrage (7-Day)", f"${accrued_7day:,.2f}")

    # Compact Standstill Toggle (Tucked neatly under metrics)
    def toggle_standstill_on():
        st.session_state.burn_halted = True

    def toggle_standstill_off():
        st.session_state.burn_halted = False

    col_standstill, _ = st.columns([2, 1])
    with col_standstill:
        if not st.session_state.burn_halted:
            st.button("⏸️ Freeze Demurrage (Commercial Standstill)",
                      key="btn_halt_burn", on_click=toggle_standstill_on)
        else:
            st.button("▶️ Resume Demurrage Accrual",
                      key="btn_run_burn", on_click=toggle_standstill_off, type="primary")

    # --- KEY 1: SINGLE-ACTION COMMIT & ADVANCE ---
    st.markdown("---")
    st.markdown("#### 🔑 Key 1: Executive Chairman Commercial Release")
    st.caption(f"Authorizes formal liquidated damages demand against {cfg['counterparty']} and commits ${current_capex:,.0f} USD baseline to docket.")

    def commit_and_advance_to_t2a():
        st.session_state.key_chairman_armed = True
        _evaluate_dual_seal()
        st.session_state.active_desk = COMMERCIAL_DESKS[1]  # Instantly advance to Tier 2A

    # ONE CLEAN ACTION: No duplicate buttons, no locked placeholders
    st.button(
        "⚡ ENGAGE KEY 1: COMMIT BALANCE SHEET & PROCEED TO TIER 2A ➔",
        key="btn_arm_and_advance_k1",
        on_click=commit_and_advance_to_t2a,
        type="primary",
        use_container_width=True
    )

# =========================================================
# 5. VIEW: TIER 1B — GENERAL COUNSEL LEGAL CHAMBERS
# =========================================================
elif st.session_state.active_desk == DESK_OPTIONS[1]:
    is_sealed = st.session_state.docket_inception_sealed
    st.markdown("""
        <div style="background:linear-gradient(90deg,#130f26 0%,#1e1b4b 100%);border-left:8px solid #a855f7;padding:18px 24px;border-radius:8px;margin-bottom:20px;">
            <div style="font-size:1.6rem;font-weight:900;color:#fff;">TIER 1B | GENERAL COUNSEL LEGAL CHAMBERS</div>
            <div style="color:#c084fc;font-size:.9rem;font-weight:700;margin-top:2px;">PRIVILEGE QUARANTINE, STATUTORY PROOF AUDIT & LITIGATION INCEPTION</div>
        </div>
    """, unsafe_allow_html=True)

    legal_roles = [
        "General Counsel & CLO",
        "Lead External Litigation Counsel",
        "Regulatory & Grid Counsel",
        "Forensic Evidence Custodian",
    ]
    st.session_state.legal_identity = st.selectbox(
        "Active Legal Seat:",
        legal_roles,
        index=legal_roles.index(st.session_state.legal_identity),
        key="sel_legal_role",
    )
    st.markdown("#### Statutory-to-Evidence Sufficiency Ledger")
    st.markdown("""
    | Statutory pillar | Required artifact | Custodial status |
    | --- | --- | --- |
    | DGCL Section 141(e) | Board technical reliance and safe-harbor minute | Verified and ready |
    | FRE 803(6) | Work Order WO-8821-HARMONIC | Stamped |
    | FRE 902(13) and (14) | COMTRADE binary and Fluke calibration certificate | Pending field PE seal |
    | Turnkey Clause 11.2 | EDI gateway and 90-minute cure receipt | Pre-staged |
    """)
    st.markdown("#### Key 2: General Counsel Statutory & Privilege Release")
    st.button(
        "DISARM KEY 2" if st.session_state.key_counsel_armed else "ENGAGE KEY 2: ISSUE LITIGATION HOLD",
        key="t1b_counsel_key",
        on_click=toggle_counsel_key,
        type="primary",
        use_container_width=True,
    )
    if st.session_state.key_counsel_armed:
        st.success("KEY 2 ARMED: Enterprise litigation hold active and discovery wall sealed.")
    st.write("")
    nav_col1, nav_col2 = st.columns(2)
    with nav_col1:
        st.button("Return to Chairman Command Post (Tier 1A)", key="t1b_to_t1a", on_click=navigate_to, args=(DESK_OPTIONS[0],), use_container_width=True)
    with nav_col2:
        if is_sealed:
            st.button("Proceed to Legal Governance Desk (Tier 2B)", key="t1b_to_t2b", on_click=navigate_to, args=(DESK_OPTIONS[3],), use_container_width=True, type="primary")
        else:
            st.button("Tier 2B Locked (Requires Dual-Key Inception)", key="t1b_locked", disabled=True, use_container_width=True)

# ==============================================================================
# TIER 2A: CHAIRMAN DIRECTORATE GOVERNANCE (UNIFIED NO-LOOP COCKPIT)
# ==============================================================================
elif st.session_state.active_desk == COMMERCIAL_DESKS[1]:
    g2a = st.session_state.get("gate_2a_cleared", False)
    g2b = st.session_state.get("gate_2b_cleared", False)

    st.markdown("""
        <div style="background: linear-gradient(90deg, #0f172a 0%, #1e293b 100%); border-left: 8px solid #00d4ff; padding: 18px 24px; border-radius: 8px; margin-bottom: 20px;">
            <div style="font-size: 1.5rem; font-weight: 900; color: #ffffff;">TIER 2A | CHAIRMAN DIRECTORATE GOVERNANCE</div>
            <div style="font-size: 0.9rem; font-weight: 700; color: #00d4ff; margin-top: 2px;">
                BOARD OF DIRECTORS RATIFICATION & TECHNICAL RELIANCE REPOSITORY
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 1. STATUS HEADER
    if not g2a:
        st.markdown(f"""
            <div style="background: #1e1114; border: 2px solid #ef4444; border-left: 8px solid #ef4444; padding: 16px 20px; border-radius: 8px; margin-bottom: 20px;">
                <div style="font-size: 0.8rem; font-weight: 800; color: #f87171;">STATUTORY FIDUCIARY STATUS</div>
                <div style="font-size: 1.3rem; font-weight: 900; color: #ffffff; margin-top: 2px;">
                    🔴 GOVERNANCE DEADLOCK: TECHNICAL RELIANCE REQUIRED
                </div>
                <div style="color: #cbd5e0; font-size: 0.85rem; margin-top: 6px;">
                    Marcus Vance, PE cannot perform the hardware bypass until Dr. Arthur Pendleton executes the DGCL § 141(e) reliance resolution.
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style="background: #062b19; border: 2px solid #00ff88; border-left: 8px solid #00ff88; padding: 16px 20px; border-radius: 8px; margin-bottom: 20px;">
                <div style="font-size: 0.8rem; font-weight: 800; color: #00ff88;">STATUTORY FIDUCIARY STATUS</div>
                <div style="font-size: 1.3rem; font-weight: 900; color: #ffffff; margin-top: 2px;">
                    🟢 FIDUCIARY CONSENSUS RATIFIED // DGCL § 141(a) ACTIVE
                </div>
                <div style="color: #cbd5e0; font-size: 0.85rem; margin-top: 6px;">
                    Dr. Arthur Pendleton has executed technical reliance. Business Judgment Rule shield is active.
                </div>
            </div>
        """, unsafe_allow_html=True)

    # 2. DR. PENDLETON ACTION CARD
    if not g2a:
        st.markdown("""
            <div style="background: #141c2e; border: 2px solid #ef4444; border-radius: 8px; padding: 18px 20px; margin-bottom: 12px;">
                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                    <div>
                        <div style="font-size: 1.15rem; font-weight: 900; color: #ffffff;">Dr. Arthur Pendleton</div>
                        <div style="color: #60a5fa; font-size: 0.85rem; font-weight: 700;">Chair, Grid Risk & Technical Integrity Committee</div>
                        <div style="color: #94a3b8; font-size: 0.78rem;">Delaware DGCL § 141(e) Technical Reliance Authority</div>
                    </div>
                    <span style="background: #ef4444; color: #ffffff; font-size: 0.75rem; font-weight: 900; padding: 3px 8px; border-radius: 4px;">
                        🔴 ACTIVE BOTTLENECK
                    </span>
                </div>
                <div style="margin-top: 12px; font-size: 0.85rem; color: #cbd5e0;">
                    <strong>Action Required:</strong> Formally attest to the 4.1% THD harmonic breach from Work Order WO-8821 to absorb personal liability onto the corporate balance sheet.
                </div>
            </div>
        """, unsafe_allow_html=True)

        if st.button("✍️ EXECUTE DR. PENDLETON DGCL SECTION 141(e) RELIANCE RESOLUTION", key="btn_exec_pendleton_final", type="primary", use_container_width=True):
            st.session_state.gate_2a_cleared = True
            st.rerun()
    else:
        st.markdown("""
            <div style="background: #0b1c18; border: 1px solid #00ff88; border-radius: 8px; padding: 16px 20px; margin-bottom: 16px;">
                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                    <div>
                        <div style="font-size: 1.15rem; font-weight: 900; color: #ffffff;">Dr. Arthur Pendleton</div>
                        <div style="color: #00ff88; font-size: 0.85rem; font-weight: 700;">Chair, Grid Risk & Technical Integrity Committee</div>
                    </div>
                    <span style="background: #00ff88; color: #04101e; font-size: 0.75rem; font-weight: 900; padding: 3px 8px; border-radius: 4px;">
                        ✓ SIGNED & RATIFIED
                    </span>
                </div>
                <div style="margin-top: 8px; color: #cbd5e0; font-size: 0.82rem;">
                    Resolution entered into Minute Book. Fiduciary shield fully established.
                </div>
            </div>
        """, unsafe_allow_html=True)

    # 3. DIRECT LINEAR DESCENT GATEWAY
    st.write("")
    st.markdown("---")

    if g2a:
        st.button("🟢 PROCEED TO TIER 3A: OPERATIONS DISPATCH ➔",
                  key="btn_t2a_advance_clean",
                  on_click=navigate_to,
                  args=(COMMERCIAL_DESKS[2],),
                  type="primary",
                  use_container_width=True)
    else:
        st.button("🔴 TIER 3A LOCKED (Execute Pendleton Resolution Above to Proceed)",
                  key="btn_t2a_locked_clean",
                  disabled=True,
                  use_container_width=True)

# =========================================================
# 7. VIEW: TIER 2B — LEGAL COUNSEL GOVERNANCE & SECRETARIAL DESK
# =========================================================
elif st.session_state.active_desk == DESK_OPTIONS[3]:
    is_sealed = st.session_state.docket_inception_sealed
    g2a = st.session_state.gate_2a_cleared
    g2b = st.session_state.gate_2b_cleared
    st.markdown("""
        <div style="background:linear-gradient(90deg,#130f26 0%,#1e1b4b 100%);border-left:8px solid #a855f7;padding:18px 24px;border-radius:8px;margin-bottom:20px;">
            <div style="font-size:1.6rem;font-weight:900;color:#fff;">TIER 2B | LEGAL COUNSEL GOVERNANCE DESK</div>
            <div style="color:#c084fc;font-size:.9rem;font-weight:700;margin-top:2px;">CORPORATE MINUTE BOOK AUDIT, STATUTORY RELIANCE & DEED OF INDEMNIFICATION</div>
        </div>
    """, unsafe_allow_html=True)
    if not is_sealed:
        st.warning("SIMULATION NOTICE: Active docket is disarmed. Resolutions remain non-binding until Tier 1 dual-key inception is sealed.")
    st.markdown("#### Corporate Minute Registry & Statutory Fiduciary Audit")
    st.markdown(f"""
    | Committee / Seat | Statutory authority | Legal reliance defense | Minute book status |
    | --- | --- | --- | --- |
    | Dr. Arthur Pendleton | Delaware DGCL Section 141(e) | Technical expert reliance shield | {'CERTIFIED' if g2a else 'PENDING RATIFICATION'} |
    | David Chen (Proxy) | PUCT Protocol Section 4.2 | Regulatory standstill compliance | STANDBY AUDITED |
    | Eleanor Vance, CPA | ISP98 Rule 5.01 | Letter of credit default mechanics | STANDBY AUDITED |
    | Executive Chairman | Delaware DGCL Section 141(a) | Business Judgment Rule | COMMITTED |
    """)
    # --------------------------------------------------------------------------
    # LEGAL OFFICER: JONATHAN STERLING, ESQ. (CORPORATE SECRETARY)
    # --------------------------------------------------------------------------
    st.markdown("### ⚖️ Legal Officer Execution & Coporate Seal")

    if not g2b:
        st.markdown("""
            <div style="background: #141c2e; border: 2px solid #a855f7; border-radius: 8px; padding: 18px 20px; margin-bottom: 14px;">
                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                    <div>
                        <div style="font-size: 1.15rem; font-weight: 900; color: #ffffff;">Jonathan Sterling, Esq.</div>
                        <div style="color: #c084fc; font-size: 0.85rem; font-weight: 700;">Corporate Secretary & Governance Counsel</div>
                        <div style="color: #94a3b8; font-size: 0.78rem;">Statutory Authority: Delaware DGCL § 145 / Corporate Minute Custody (DE Bar #44109)</div>
                    </div>
                    <span style="background: #a855f7; color: #ffffff; font-size: 0.75rem; font-weight: 900; padding: 3px 8px; border-radius: 4px;">
                        🔴 PENDING CORPORATE SEAL
                    </span>
                </div>
                <div style="margin-top: 14px; background: #0b1120; border-left: 4px solid #3b82f6; padding: 10px 14px; border-radius: 4px;">
                    <strong style="color: #93c5fd; font-size: 0.82rem;">WHAT HAS BEEN DONE:</strong>
                    <div style="color: #cbd5e0; font-size: 0.82rem; margin-top: 2px;">
                        • Dr. Arthur Pendleton's DGCL § 141(e) Technical Reliance attested into minute book.<br>
                        • Binding corporate indemnification covenant drafted to absorb switchyard liabilities under DGCL § 145.
                    </div>
                </div>
                <div style="margin-top: 10px; background: #1c1114; border-left: 4px solid #ef4444; padding: 10px 14px; border-radius: 4px;">
                    <strong style="color: #fca5a5; font-size: 0.82rem;">WHAT NEEDS TO BE DONE:</strong>
                    <div style="color: #cbd5e0; font-size: 0.82rem; margin-top: 2px;">
                        • Affix Corporate Seal to execute the Deed of Indemnity, insulating Marcus Vance, PE before field dispatch.
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        if st.button("✍️ JONATHAN STERLING: EXECUTE & SEAL DEED OF INDEMNITY (DGCL § 145)", key="btn_seal_2b_sterling", type="primary", use_container_width=True):
            st.session_state.gate_2b_cleared = True
            st.session_state.gate_2_cleared = True
            st.rerun()
    else:
        st.markdown("""
            <div style="background: #0b1c18; border: 1px solid #00ff88; border-radius: 8px; padding: 16px 20px; margin-bottom: 14px;">
                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                    <div>
                        <div style="font-size: 1.15rem; font-weight: 900; color: #ffffff;">Jonathan Sterling, Esq.</div>
                        <div style="color: #00ff88; font-size: 0.85rem; font-weight: 700;">Corporate Secretary & Governance Counsel</div>
                        <div style="color: #94a3b8; font-size: 0.78rem;">Delaware Bar #44109 // Corporate Seal Affixed</div>
                    </div>
                    <span style="background: #00ff88; color: #04101e; font-size: 0.75rem; font-weight: 900; padding: 3px 8px; border-radius: 4px;">
                        ✓ DEED SEALED
                    </span>
                </div>
                <div style="margin-top: 10px; color: #cbd5e0; font-size: 0.82rem;">
                    <strong>COMPLETED:</strong> Deed of Indemnity executed under DGCL § 145 and entered into the Corporate Minute Registry. Corporate liability shield active for Marcus Vance, PE.
                </div>
                <div style="font-family: monospace; font-size: 0.75rem; color: #00d4ff; margin-top: 6px;">
                    Minute Seal: sha256:f48a901c22e987102ce094ab10e4a77e9921004ab12fedcba98765432
                </div>
            </div>
        """, unsafe_allow_html=True)

    nav_col1, nav_col2 = st.columns(2)
    with nav_col1:
        st.button("View Chairman Boardroom (Tier 2A)", key="t2b_to_t2a", on_click=navigate_to, args=(DESK_OPTIONS[2],), use_container_width=True)
    with nav_col2:
        if g2a and g2b:
            st.button("PROCEED TO TIER 3A: OPERATIONS DISPATCH", key="t2b_to_t3a", on_click=navigate_to, args=(DESK_OPTIONS[4],), use_container_width=True, type="primary")
        else:
            st.info("Both Board Ratification (2A) and Legal Indemnity Deed (2B) must be sealed before dispatch.")

# =========================================================
# 8. VIEW: TIER 3A — ENGINEERING OPERATIONS COMMAND
# =========================================================
elif st.session_state.active_desk == COMMERCIAL_DESKS[2]:
    render_inception_guard()
    render_breadcrumb(2)
    render_top_action_bar()
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

    # Inside Sarah Jenkins' Lead Status Column:
    with c2:
        st.markdown(f"""
            <div style="background: #0d1526; border: 1px solid #1e293b; padding: 14px; border-radius: 6px;">
                <div style="color: #94a3b8; font-size: 0.75rem; font-weight: 800; text-transform: uppercase;">Command Lead Status</div>
                <div style="color: #ffffff; font-weight: 900; font-size: 1rem; margin-top: 2px;">Officer: Sarah Jenkins</div>
                <div style="color: #60a5fa; font-size: 0.8rem; margin-top: 2px;">Role: VP, Engineering Operations</div>
                <div style="color: #94a3b8; font-size: 0.8rem;">Contractor: Permian HV Field Services</div>
                {"" if not st.session_state.gate_3a_cleared else '''
                <div style="background: #062b19; border: 1px solid #00ff88; color: #00ff88; font-size: 0.75rem; font-weight: 800; padding: 4px 8px; border-radius: 4px; margin-top: 8px; display: inline-block;">
                    ● 3A Gate Cleared: Dispatched to Field Lead
                </div>
                '''}
            </div>
        """, unsafe_allow_html=True)
        if not st.session_state.gate_3a_cleared:
            st.warning("○ Awaiting Corporate Handoff Completion")

    # Bottom Linear Descent Gateway (The Single Source of Truth)
    st.write("")
    st.markdown("---")

    col_back, col_fwd = st.columns([1, 2])
    with col_back:
        st.button("△ Return to Directorate (Tier 2A)",
                  key="btn_t3a_back",
                  on_click=navigate_to,
                  args=(COMMERCIAL_DESKS[1],),
                  use_container_width=True)
    with col_fwd:
        if st.session_state.gate_3a_cleared:
            st.button("🟢 PROCEED TO TIER 3B: SITE EXECUTION ➔",
                      key="btn_t3a_to_t3b",
                      on_click=navigate_to,
                      args=(COMMERCIAL_DESKS[3],),
                      type="primary",
                      use_container_width=True)
        else:
            st.button("🔴 TIER 3B LOCKED (Complete Steps 1-3 Above to Proceed)",
                      key="btn_t3a_locked",
                      disabled=True,
                      use_container_width=True)

# =========================================================
# 7. VIEW: TIER 3B — SITE EXECUTION & REMEDIATION DESK
# =========================================================
elif st.session_state.active_desk == DESK_OPTIONS[5]:
    render_inception_guard()
    render_breadcrumb(3)
    render_top_action_bar()
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
        st.button("← Return to Tier 3A", on_click=navigate_to, args=(DESK_OPTIONS[4],))
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
            st.button("➔ PROCEED TO TIER 4: FORENSIC RECOVERY VAULT", key="t3b_fwd_t4", on_click=navigate_to, args=(DESK_OPTIONS[6],), use_container_width=True, type="primary")
    else:
        st.button("⌂ Return to Command Post (Tier 1)", key="t3b_back_t1_idle", on_click=navigate_to, args=(DESK_OPTIONS[0],), use_container_width=True)

# =========================================================
# 7. VIEW: TIER 4 — FORENSIC VAULT
# =========================================================
elif st.session_state.active_desk == LEGAL_TIER3_LABEL:
    render_inception_guard()
    render_breadcrumb(3)
    render_top_action_bar()
    st.markdown("""
        <div style="background: linear-gradient(90deg, #130f26 0%, #1e1b4b 100%); border-left: 8px solid #a855f7; padding: 18px 24px; border-radius: 8px; margin-bottom: 20px;">
            <div style="font-size: 1.6rem; font-weight: 900; color: #fff;">TIER 3 | REGULATORY & INTERCONNECTION AUDIT</div>
            <div style="color: #c084fc; font-size: .9rem; font-weight: 700; margin-top: 2px;">GRID CODE COMPLIANCE, TARIFF FILING INTEGRITY & COUNTERPARTY NOTICE AUDIT</div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("#### Interconnection Docket & Notice Compliance Ledger")
    st.markdown(f"""
    | Regulatory instrument | Governing authority | Compliance status |
    | --- | --- | --- |
    | Interconnection Agreement | {book_config['docket']} | ACTIVE / UNDER AUDIT |
    | Grid Code Harmonics Filing | {book_config['tech_standard']} | 4.1% THD CERTIFIED COMPLIANT |
    | Cure Notice Dispatch | Turnkey EPC Clause 11.2 | TRANSMITTED & RECEIPT CONFIRMED |
    | Market Participant Attestation | {selected_jurisdiction} | STANDBY / DAVID CHEN PROXY |
    """)
    st.info("This desk audits the regulatory paper trail supporting the liquidated demurrage claim before it is escalated to the Forensic Recovery Vault.")
    nav_col1, nav_col2 = st.columns(2)
    with nav_col1:
        st.button("Return to Tier 2B Governance Desk", key="t3leg_to_t2b", on_click=navigate_to, args=(DESK_OPTIONS[3],), use_container_width=True)
    with nav_col2:
        st.button("PROCEED TO TIER 4: LEGAL EVIDENCE VAULT", key="t3leg_to_t4", on_click=navigate_to, args=(LEGAL_TIER4_LABEL,), use_container_width=True, type="primary")

elif st.session_state.active_desk in (DESK_OPTIONS[6], LEGAL_TIER4_LABEL):
    render_inception_guard()
    render_breadcrumb(4)
    render_top_action_bar()
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
    # TERMINAL EXPORT & COURT PRESENTATION RUNWAY
    # --------------------------------------------------------------------------
    st.markdown("""
        <div style="background: #1e293b; border: 2px solid #00d4ff; padding: 16px 20px; border-radius: 8px; margin-top: 20px; margin-bottom: 20px;">
            <div style="font-size: 1.15rem; font-weight: 900; color: #ffffff;">
                🏛️ FINAL DISPOSITION: EXPORT COURT & ARBITRATION PACKAGE
            </div>
            <div style="color: #94a3b8; font-size: 0.85rem; margin-top: 4px;">
                Produce court-admissible physical filings or generate AirPrint records for Delaware Chancery Court emergency hearings.
            </div>
        </div>
    """, unsafe_allow_html=True)

    c_exp1, c_exp2 = st.columns(2)
    with c_exp1:
        if st.button("🖨️ Print Full Docket View (AirPrint / Save PDF)", key="t4_print_btn", use_container_width=True):
            components.html("""<script>window.parent.print();</script>""", height=0)
    with c_exp2:
        st.download_button(
            label="📑 Download Complete Master Docket Bundle",
            data=unified_executive_bundle,
            file_name=f"Certified_Master_Docket_{active_cfg['docket'].replace(' ', '_').replace('#', '')}.txt",
            mime="text/plain",
            key="t4_docket_bundle_btn",
            use_container_width=True,
            type="primary"
        )

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

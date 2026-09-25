import datetime
import hashlib
import json
import os
import re
from copy import deepcopy
import streamlit as st
import streamlit.components.v1 as components

APP_BUILD_ID = "v6.10_german_language_toggle_sep24_2026"

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

# --- SCHEMA-DRIVEN SCENARIO PACKS (AutonomousCapitalDefenseScenario) ---
# Load modular scenarios from the sibling scenarios.json file
_SCENARIOS_JSON_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scenarios.json")
try:
    with open(_SCENARIOS_JSON_PATH, "r") as f:
        SCENARIOS_DATA = json.load(f)
except Exception:
    SCENARIOS_DATA = []

SCENARIO_PACKS = SCENARIOS_DATA

# Map scenarios by name for the dropdown
def _scenario_label(scenario):
    if "metadata" in scenario:
        meta = scenario["metadata"]
        return f"{meta['sector_name']} ({meta['country_code']})"
    return f"{scenario['asset_name']} ({scenario['jurisdiction_code']})"


SCENARIOS_MAP = {
    _scenario_label(scenario): scenario
    for scenario in SCENARIOS_DATA
}

def _scenario_to_operating_book(scenario):
    """Maps a schema-shaped scenario pack into the OPERATING_BOOKS entry shape.

    Uses the same label key as SCENARIOS_MAP so the two stay interchangeable.
    """
    if scenario.get("scenario_id") == "DE_OFFSHORE_WIND_001":
        roster = scenario["named_roster"]
        key = _scenario_label(scenario)
        return key, {
            "scenario_id": scenario["scenario_id"],
            "docket": f"{scenario['court_forum']} Docket #{scenario['scenario_id']}",
            "jurisdiction": scenario["statutory_safe_harbor"],
            "jurisdiction_options": [scenario["court_forum"]],
            "counterparty": scenario["counterparty_entity"],
            "contract": scenario["evidence_standard"],
            "capex_exposure": float(scenario["capex_exposure"]),
            "filing_date": scenario.get("filing_date", "2024 Semi-Annual Report"),
            "filing_source": scenario["filing_source"],
            "default_capex": float(scenario["capex_exposure"]),
            "daily_burn_base": float(scenario["daily_holding_burn"]),
            "lead_pe": roster["independent_engineer"],
            "lead_director": roster["supervisory_chair"],
            "tech_standard": scenario["technical_drift_metric"],
            "currency_symbol": scenario["currency_symbol"],
            "currency_code": scenario["currency_code"],
        }

    meta = scenario["metadata"]
    juris = scenario["jurisdiction"]
    fin = scenario["financials"]
    breach = scenario["technical_breach"]
    stake = scenario["stakeholders"]

    key = f"{meta['sector_name']} ({meta['country_code']})"
    jurisdiction_label = f"{juris['court_name']} ({juris['statute_board_reliance']})"

    return key, {
        "docket": f"{juris['court_name']} Docket #{scenario['scenario_id']}",
        "jurisdiction": jurisdiction_label,
        "jurisdiction_options": [jurisdiction_label],
        "counterparty": meta["client_name"],
        "contract": juris["default_notice_clause"],
        "capex_exposure": float(scenario.get("capex_exposure", fin["default_capex_usd"])),
        "filing_date": scenario.get("filing_date"),
        "filing_source": scenario.get("filing_source"),
        "default_capex": float(fin["default_capex_usd"]),
        "daily_burn_base": float(fin["daily_burn_base_usd"]),
        "lead_pe": stake["lead_pe_name"],
        "lead_director": stake["technical_director_name"],
        "tech_standard": f"{breach['standard_code']} {breach['metric_name']} Breach "
                         f"({breach['breach_value']}{breach['unit_of_measure']} vs "
                         f"{breach['threshold_limit']}{breach['unit_of_measure']} limit)"
    }

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

for _scenario in SCENARIO_PACKS:
    _book_key, _book_entry = _scenario_to_operating_book(_scenario)
    OPERATING_BOOKS[_book_key] = _book_entry

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
TRACK_COMMERCIAL = "🗂️ Commercial & Operations Track"
TRACK_LEGAL = "⚖️ Legal & Statutory Track"
TIER_1A = "Tier 1A | Chairman Tactical Command Post"
TIER_2A = "Tier 2A | Chairman Directorate Governance"
TIER_3A = "Tier 3A | Engineering Operations Command"
TIER_3B = "Tier 3B | Site Execution Desk"
TIER_4 = "Tier 4 | Forensic Recovery Vault"
COMMERCIAL_DESKS = [TIER_1A, TIER_2A, TIER_3A, TIER_3B, TIER_4]
COMMERCIAL_TIERS = COMMERCIAL_DESKS
LEGAL_TIER3_LABEL = "Tier 3 | Regulatory & Interconnection Audit"
LEGAL_TIER4_LABEL = "Tier 4 | Legal Evidence & Collateral Vault"
LEGAL_DESKS = [DESK_OPTIONS[1], DESK_OPTIONS[3], LEGAL_TIER3_LABEL, LEGAL_TIER4_LABEL]
LEGAL_TIERS = [
    "Tier 1B | General Counsel Litigation Command",
    "Tier 2B | Litigation Hold & Statutory Notice",
    "Tier 3C | Evidentiary Discovery & ISO Audit",
    "Tier 4 | Master Judicial Docket & Evidence Vault"
]

if "nav_tier_legal" not in st.session_state:
    st.session_state["nav_tier_legal"] = LEGAL_TIERS[0]

if "nav_track_selection" not in st.session_state:
    st.session_state["nav_track_selection"] = TRACK_COMMERCIAL
if "nav_tier_commercial" not in st.session_state:
    st.session_state["nav_tier_commercial"] = TIER_1A
if "mandate_executed" not in st.session_state:
    st.session_state["mandate_executed"] = False


def cb_goto_tier_1a():
    st.session_state["nav_tier_commercial"] = TIER_1A


def cb_goto_tier_3a():
    st.session_state["nav_tier_commercial"] = TIER_3A


def cb_goto_tier_3b():
    st.session_state["nav_tier_commercial"] = TIER_3B


def cb_goto_tier_4():
    st.session_state["nav_tier_commercial"] = TIER_4


def cb_goto_legal():
    st.session_state["nav_track_selection"] = TRACK_LEGAL

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

# ==============================================================================
# UNIFIED NAVIGATION ENGINE (SYNCHRONIZES SIDEBAR + IN-PAGE BUTTONS)
# ==============================================================================
def go_to_desk(target_desk):
    """Safely update the active desk and both sidebar navigation widgets."""
    st.session_state.active_desk = target_desk

    if target_desk in COMMERCIAL_DESKS:
        st.session_state.active_track_selector = TRACK_COMMERCIAL
        st.session_state.radio_commercial_desks = target_desk
        st.session_state.track_selector_widget = TRACK_COMMERCIAL
        st.session_state.radio_comm_desks = target_desk
    elif target_desk in LEGAL_DESKS:
        st.session_state.active_track_selector = TRACK_LEGAL
        st.session_state.radio_legal_desks = target_desk
        st.session_state.track_selector_widget = TRACK_LEGAL
        st.session_state.radio_leg_desks = target_desk


def reset_entire_incident():
    """Wipe gate progression back to an uncommitted, pristine state."""
    keys_to_clear = [
        "key_chairman_armed", "key_counsel_armed", "docket_inception_sealed",
        "gate_2a_cleared", "gate_2b_cleared", "gate_2_cleared",
        "gate_3a_cleared", "burn_halted"
    ]
    for key in keys_to_clear:
        st.session_state[key] = False

    selected_book = st.session_state.get("selected_book_name", next(iter(OPERATING_BOOKS)))
    default_capex = float(OPERATING_BOOKS[selected_book]["default_capex"])
    st.session_state.capex_baseline = default_capex
    st.session_state.slider_chair_capex = default_capex
    st.session_state.slider_capex = default_capex
    go_to_desk(COMMERCIAL_DESKS[0])


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
            st.button("⌂ Return to Command Post (Tier 1)", key=f"{gateway_key}_back", on_click=go_to_desk, args=(DESK_OPTIONS[0],), use_container_width=True)
        with nav_c2:
            st.button(f"➔ PROCEED TO {next_label}", key=f"{gateway_key}_forward", on_click=go_to_desk, args=(next_desk,), use_container_width=True, type="primary")
    else:
        st.info("ℹ️ Complete the required controls above to unlock the next operational tier.")
        st.button("⌂ Return to Command Post (Tier 1)", key=f"{gateway_key}_back_incomplete", on_click=go_to_desk, args=(DESK_OPTIONS[0],), use_container_width=True)


def render_executive_dual_signoff():
    st.markdown("""
        <div style="background: linear-gradient(90deg, #0b1728 0%, #1e1b4b 100%); border-left: 8px solid #00ff88; padding: 20px 24px; border-radius: 8px; margin-bottom: 24px;">
            <div style="font-size: 1.5rem; font-weight: 900; color: #ffffff;">STAGE 04 | EXECUTIVE DUAL SIGN-OFF DOCKET</div>
            <div style="font-size: 0.85rem; font-weight: 700; color: #00ff88; margin-top: 4px;">SYNTHESIS OF COMMERCIAL LIQUIDATION & STATUTORY CHANCERY FILING</div>
        </div>
    """, unsafe_allow_html=True)

    if "chair_final_signed" not in st.session_state:
        st.session_state.chair_final_signed = False
    if "clo_final_signed" not in st.session_state:
        st.session_state.clo_final_signed = False

    col_comm, col_legal = st.columns(2)
    with col_comm:
        st.markdown("""
            <div style="background: #0d1526; border: 1px solid #1e3a8a; border-radius: 8px; padding: 18px; margin-bottom: 16px;">
                <div style="font-size: 0.8rem; font-weight: 800; color: #60a5fa; text-transform: uppercase;">COMMERCIAL AUTHORITY</div>
                <div style="font-size: 1.15rem; font-weight: 900; color: #ffffff; margin-top: 2px;">Executive Chairman</div>
                <div style="color: #94a3b8; font-size: 0.78rem; margin-bottom: 12px;">Mandate: Capital Recovery & Collateral Call</div>
                <div style="background: #08101d; padding: 10px; border-radius: 4px; font-size: 0.8rem; color: #cbd5e0; line-height: 1.6;">
                    • CapEx Baseline: <strong>$300,000,000 USD</strong><br>
                    • Accrued Demurrage: <strong>$2,070,671.19 USD</strong><br>
                    • Field Execution: <strong>IEEE 2800 Bypass Certified (Marcus Vance, PE)</strong>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if not st.session_state.chair_final_signed:
            def sign_chair_final():
                st.session_state.chair_final_signed = True
            st.button("✍️ EXECUTIVE CHAIRMAN: SIGN COMMERCIAL DEMAND & LC DRAW", key="btn_sign_chair_final", on_click=sign_chair_final, type="primary", use_container_width=True)
        else:
            st.success("✓ EXECUTIVE CHAIRMAN SIGNATURE AFFIXED")

    with col_legal:
        st.markdown("""
            <div style="background: #14132b; border: 1px solid #7c3aed; border-radius: 8px; padding: 18px; margin-bottom: 16px;">
                <div style="font-size: 0.8rem; font-weight: 800; color: #c084fc; text-transform: uppercase;">STATUTORY AUTHORITY</div>
                <div style="font-size: 1.15rem; font-weight: 900; color: #ffffff; margin-top: 2px;">Katherine Ross, Esq. (CLO)</div>
                <div style="color: #94a3b8; font-size: 0.78rem; margin-bottom: 12px;">Mandate: Sovereign Court Injunction & Privilege Custody</div>
                <div style="background: #0d0c1c; padding: 10px; border-radius: 4px; font-size: 0.8rem; color: #cbd5e0; line-height: 1.6;">
                    • Fiduciary Attestation: <strong>DGCL § 141(e) Signed (Pendleton)</strong><br>
                    • Regulatory Default: <strong>ERCOT § 4.2 / Cl. 11.2 Notice Audited</strong><br>
                    • Admissibility: <strong>FRE 902(14) SHA-256 Binary Sealed</strong>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if not st.session_state.clo_final_signed:
            def sign_clo_final():
                st.session_state.clo_final_signed = True
            st.button("✍️ CHIEF LEGAL OFFICER: SIGN CHANCERY COMPLAINT & INJUNCTION", key="btn_sign_clo_final", on_click=sign_clo_final, type="primary", use_container_width=True)
        else:
            st.success("✓ CHIEF LEGAL OFFICER SIGNATURE AFFIXED")

    st.write("")
    st.markdown("---")
    if st.session_state.chair_final_signed and st.session_state.clo_final_signed:
        st.success("🏆 COLLECTIVE EXECUTIVE SOVEREIGN SEAL AFFIXED\n\nVerified complaint and emergency TRO served; ISP98 standby letter of credit draw presented; case docket permanently sealed.")
    else:
        st.info("🔒 **Collective Action Gate:** Both the Executive Chairman and Chief Legal Officer must independently affix their signatures above to instigate the formal filing and collateral drawdown.")

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


I18N.update({
    "EN": {
        "title": "TIER 1 | JUDICIAL EVIDENCE SEALING & EXECUTIVE COMMAND POST",
        "caption": "Fiduciary Airlock & Sovereign Asset Defense | Forum: ",
        "gateway_title": "Command Gateway: Exposure Target (Sensitivity Engine)",
        "btn_base": "⭐ Audited Base",
        "btn_base_src": "EnBW 2024 & BNetzA Filings",
        "btn_500_cap": "Hypothetical Sub-Array",
        "btn_1500_cap": "Hypothetical Grid Link",
        "btn_3000_cap": "Full Offshore Expansion",
        "slider_label": "Adjust Balance Sheet Exposure Floor:",
        "chair_seat": "Supervisory Board & Executive",
        "ops_lead": "Operational Leadership",
        "bottleneck_header": "⚠️ Acute Grid Synchronization Bottleneck (Capital Burn)",
        "drift_label": "Identified Drift",
        "lbl_base": "Active CapEx Baseline",
        "lbl_daily_burn": "Daily Holding Burn (8.5% p.a.)",
        "per_day": "/ day",
        "lbl_30d": "30-Day Standstill Accumulation",
        "lbl_ld_cap": "Liquidated Damages Ceiling (10% LD Cap)",
        "lbl_engineer": "Certifying Statutory Engineer",
        "scale_header": "📊 Bridging Scale: Total Capital Preserved",
        "scale_gross": "Gross Inaction Loss Prevented (30d + LD Cap)",
        "scale_fee": "Less Forensic Retainer Mandate (2.5%)",
        "scale_net": "NET CAPITAL PRESERVED TO BALANCE SHEET",
        "counsel_seat": "General Counsel",
        "counsel_role": "Chief Legal Officer / Corporate Legal Director",
        "shield_header": "🛡️ Statutory Fiduciary & Safe-Harbor Ledger",
        "forum_label": "Legal Forum",
        "safe_harbor_label": "Statutory Shield",
        "evidence_label": "Evidence Standard",
        "hold_status_label": "Litigation Hold Status",
        "hold_active": "🔴 ACTIVE & SEALED ON DOCKET",
        "hold_pending": "⚪ PREPARED (PENDING RATIFICATION)",
        "consortium_label": "Consortium Risk",
        "counterparty_label": "Default Counterparty",
        "provenance_title": "🔍 View Provenance Card & Statutory Anchor",
        "prov_source": "Public Data Ingestion",
        "prov_standard": "Methodological Standard",
        "prov_hash": "Cryptographic Hash",
        "prov_legal": "Statutory Reliance Instrument: Formally Certified under AktG § 93",
        "airlock_warning": "🔒 SYSTEM AIRLOCK: To release court-admissible ZPO dossiers, DIN ISO 17025 telemetry logs, and operational VDI work orders, a formal board resolution pursuant to AktG § 93 is required.",
        "airlock_btn": "🛡️ EXECUTE RESOLUTION: MANDATE STATUTORY EVIDENCE SEALING (2.5% RETAINER)",
        "airlock_success": "✅ BOARD RESOLUTION RATIFIED: AktG § 93 SAFE HARBOR ENGAGED | EVIDENCE CHAIN CERTIFIED UNDER ZPO § 371",
        "btn_ops": "➔ UNLOCK TECHNICAL OPERATIONS",
        "btn_legal": "➔ ENTER COURT DOCKET & LITIGATION CHAMBERS",
    },
    "DE": {
        "title": "TIER 1 | GERICHTLICHE BEWEISSICHERUNG & VORSTANDS-COMMAND POST",
        "caption": "Fiduciary Airlock & Sovereign Asset Defense | Forum: ",
        "gateway_title": "Command Gateway: Exposure Target (Sensitivity Engine)",
        "btn_base": "⭐ Audited Base",
        "btn_base_src": "EnBW 2024 & BNetzA Filings",
        "btn_500_cap": "Hypothetisches Teilfeld",
        "btn_1500_cap": "Hypothetische Netzanbindung",
        "btn_3000_cap": "Vollständige Offshore-Erweiterung",
        "slider_label": "Bilanzielle Bemessungsgrundlage anpassen:",
        "chair_seat": "Aufsichtsrat & Vorstand",
        "ops_lead": "Operative Leitung",
        "bottleneck_header": "⚠️ Akute Netzsynchronisations-Blockade (Liquiditätsabfluss)",
        "drift_label": "Identifizierte Abweichung",
        "lbl_base": "Aktive Bemessungsgrundlage",
        "lbl_daily_burn": "Täglicher Halteverlust (8.5% p.a.)",
        "per_day": "/ Tag",
        "lbl_30d": "30-Tage Stillstands-Akkumulation",
        "lbl_ld_cap": "Pönalen-Deckel (10% LD Cap)",
        "lbl_engineer": "Zertifizierender Gutachter",
        "scale_header": "📊 Bridging Scale: Gesamterhaltener Kapitalwert",
        "scale_gross": "Vermiedener Schadenseintritt (30d + Pönalen)",
        "scale_fee": "Abzüglich Forensik-Mandat (2.5%)",
        "scale_net": "NETTO-KAPITALERHALT AUF BILANZEBENE",
        "counsel_seat": "General Counsel",
        "counsel_role": "Syndikusrechtsanwalt / Leiter Konzernrechtsabteilung",
        "shield_header": "🛡️ Gesetzlicher Fiduciary & Safe-Harbor Ledger",
        "forum_label": "Rechtliches Forum",
        "safe_harbor_label": "Haftungsprivileg",
        "evidence_label": "Beweisstandard",
        "hold_status_label": "Status Beweissicherung",
        "hold_active": "🔴 RECHTSHÄNGIG EINGELEITET",
        "hold_pending": "⚪ VORBEREITET (ZUR ZEICHNUNG)",
        "consortium_label": "Konsortial-Risiko",
        "counterparty_label": "Verzugsgegner",
        "provenance_title": "🔍 Provenienz-Karte & Gesetzliche Verankerung einsehen",
        "prov_source": "Öffentliche Datenquelle",
        "prov_standard": "Methodischer Standard",
        "prov_hash": "Kryptographischer Hash",
        "prov_legal": "Freistellungs-Dokument: Freizeichnung gem. BGH II ZR 268/16",
        "airlock_warning": "🔒 SYSTEM-SPERRE: Zur Freigabe gerichtsfester ZPO-Dossiers, Messprotokolle nach DIN EN ISO 17025 und operativer VDI-Mängellisten ist die formelle Beschlussfassung gem. AktG § 93 erforderlich.",
        "airlock_btn": "🛡️ BESCHLUSS FASSEN: STATUTARISCHE BEWEISSICHERUNG MANDATIEREN (2.5% RETRO-RETAINER)",
        "airlock_success": "✅ VORSTANDSBESCHLUSS RATIFIZIERT: AktG § 93 ENTWOHNUNG AKTIVIERT | BEWEISKETTE NACH ZPO § 371 BEGLAUBIGT",
        "btn_ops": "➔ TECHNISCHE OPERATIVE FREISCHALTEN",
        "btn_legal": "➔ GERICHTSKAMMER & KLAGESCHRIFT BETRETEN",
    },
})

T1_I18N = {
    "EN": {
        **I18N["EN"],
        "top_title": "TIER 1 | JUDICIAL EVIDENCE SEALING & EXECUTIVE COMMAND POST",
        "top_caption": "Fiduciary Airlock & Sovereign Asset Defense | Forum: ",
        "matrix_title": "Fiduciary Sensitivity Matrix | IDW PS 340 Exposure Calibration",
        "matrix_sub": "Deterministic balance-sheet stress-testing across audited capital allocations:",
        "btn_base": "⭐ Base",
        "btn_base_sub": "EnBW 2024 & BNetzA Filings",
        "btn_500": "Stress Case: €500M",
        "btn_500_sub": "Isolated Converter Station Risk",
        "btn_1500": "Stress Case: €1.5B",
        "btn_1500_sub": "HVDC Grid Interconnect Risk",
        "btn_3000": "Full Scope: €3.0B",
        "btn_3000_sub": "Total Offshore Array Expansion",
        "slider_label": "Calibrate Balance Sheet Exposure (for AktG § 93 Fiduciary Determination):",
        "burn_banner": "🚨 UNMITIGATED INACTION HOLDING BURN",
        "hourly_label": "Hourly Bleed:",
        "bleed_30d_label": "30-Day Accumulation:",
        "daily_suffix": "/ day",
        "hourly_suffix": "/ hr",
        "btn_ops": "➔ DISPATCH OPERATIONS",
        "btn_legal": "➔ COURT DOCKET",
    },
    "DE": {
        **I18N["DE"],
        "top_title": "TIER 1 | GERICHTLICHE BEWEISSICHERUNG & VORSTANDS-COMMAND POST",
        "top_caption": "Treuhänderischer Fiduciary-Airlock & Schutzschirm | Gerichtsstand: ",
        "matrix_title": "Fiduciary-Sensitivitätsmatrix | IDW PS 340 Risikofrüherkennung",
        "matrix_sub": "Deterministische Bilanz-Stresstests auf Basis testierter Kapitalallokationen:",
        "btn_base": "⭐ Basis",
        "btn_base_sub": "EnBW 2024 & BNetzA Regulierungs-Filing",
        "btn_500": "Stresstest: €500 Mio.",
        "btn_500_sub": "Isoliertes Konverterstations-Risiko",
        "btn_1500": "Stresstest: €1,5 Mrd.",
        "btn_1500_sub": "HVDC-Netzanbindungs-Risiko",
        "btn_3000": "Vollumfang: €3,0 Mrd.",
        "btn_3000_sub": "Gesamtexpansion Offshore-Park",
        "slider_label": "Bilanzielle Bemessungsgrundlage kalibrieren (für AktG § 93 Ermessensentscheidung):",
        "burn_banner": "🚨 UNMITIGIERTER STILLSTANDS-HALTEVERLUST",
        "hourly_label": "Stündlicher Verlust:",
        "bleed_30d_label": "30-Tage Stillstands-Akkumulation:",
        "daily_suffix": "/ Tag",
        "hourly_suffix": "/ Std",
        "btn_ops": "➔ TECHNISCHE OPERATIVE FREISCHALTEN",
        "btn_legal": "➔ GERICHTSKAMMER & KLAGESCHRIFT BETRETEN",
        "scale_header": "📊 BRIDGING SCALE | BILANZIELLER KAPITALERHALT",
        "scale_gross": "Vermiedener Schadenseintritt (30d Verlust + 10% Pönale)",
        "scale_fee": "Abzüglich Statutarischer Forensik-Retainer (2,5%)",
        "counsel_seat": "General Counsel / Chefjurist",
        "hold_active": "🔴 RECHTSHÄNGIG EINGELEITET (ZPO § 371)",
        "prov_legal": "Freistellungs-Dokument: Freizeichnung gem. AktG § 93 / BGH II ZR 268/16",
    },
}


def render_german_command_post(scenario_data, is_de=False):
    t = T1_I18N["DE"] if is_de else T1_I18N["EN"]

    if "active_capex" not in st.session_state:
        st.session_state.active_capex = float(scenario_data["capex_exposure"])
    if "mandate_executed" not in st.session_state:
        st.session_state.mandate_executed = False

    def update_capex(val):
        st.session_state.active_capex = float(val)
        st.session_state.slider_german_capex = float(val)

    curr = scenario_data["currency_symbol"]
    roster = scenario_data["named_roster"]
    prov = scenario_data["provenance_data"]

    active_capex = float(st.session_state.active_capex)
    apr = scenario_data["cost_of_capital_apr"]
    daily_burn = (active_capex * apr) / 365.0
    thirty_day_bleed = daily_burn * 30.0
    ld_cap = active_capex * scenario_data["liquidated_damages_cap_percent"]
    forensic_fee = active_capex * scenario_data["forensic_retainer_percent"]
    net_preserved = (thirty_day_bleed + ld_cap) - forensic_fee

    st.markdown(f"## 🏛️ {t['top_title']}")
    st.caption(f"{t['top_caption']}{scenario_data['court_forum']}")
    st.markdown(f"### 🎛️ {t['matrix_title']}")
    st.caption(t["matrix_sub"])

    b1, b2, b3, b4 = st.columns(4)
    with b1:
        st.button(
            f"{t['btn_base']} ({curr}{scenario_data['capex_exposure'] / 1e9:.1f}B)",
            key="btn_base",
            on_click=update_capex,
            args=(scenario_data["capex_exposure"],),
            use_container_width=True,
        )
        st.caption(t["btn_base_sub"])
    with b2:
        st.button(t["btn_500"], key="btn_500", on_click=update_capex, args=(500000000.0,), use_container_width=True)
        st.caption(t["btn_500_sub"])
    with b3:
        st.button(t["btn_1500"], key="btn_1500", on_click=update_capex, args=(1500000000.0,), use_container_width=True)
        st.caption(t["btn_1500_sub"])
    with b4:
        st.button(t["btn_3000"], key="btn_3000", on_click=update_capex, args=(3000000000.0,), use_container_width=True)
        st.caption(t["btn_3000_sub"])

    slider_val = st.slider(
        t["slider_label"],
        min_value=100000000.0,
        max_value=3500000000.0,
        value=float(active_capex),
        step=50000000.0,
        format=f"{curr}%,d",
        key="slider_german_capex",
    )
    if slider_val != active_capex:
        st.session_state.active_capex = float(slider_val)
        st.rerun()

    st.markdown("---")
    col_comm, col_legal = st.columns(2)

    with col_comm:
        st.markdown(f"""
        <div style="margin-bottom: 12px;">
            <div style="font-size: 1.35rem; font-weight: 800; color: #ffffff;">
                💼 {t['chair_seat']}: <span style="color: #60a5fa;">{roster['supervisory_chair']}</span>
            </div>
            <div style="font-size: 1.1rem; color: #94a3b8; margin-top: 4px;">
                {t['ops_lead']}: <span style="color: #e2e8f0; font-weight: 600;">{roster['executive_ceo']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="font-size: 1.15rem; color: #f87171; font-weight: 900; letter-spacing: 0.05em; text-transform: uppercase; margin: 14px 0 6px 0;">
            {t['bottleneck_header']}
        </div>
        """, unsafe_allow_html=True)

        st.error(f"**{t['drift_label']}:** {scenario_data['technical_drift_metric']}")

        hourly_burn = daily_burn / 24.0
        st.markdown(f"""
        <div style="background: rgba(220, 38, 38, 0.15); border: 2px solid #ef4444; border-radius: 10px; padding: 18px; margin: 14px 0;">
            <div style="font-size: 0.95rem; color: #fca5a5; font-weight: 800; text-transform: uppercase; letter-spacing: 0.1em;">
                {t['burn_banner']}
            </div>
            <div style="font-size: 2.6rem; font-weight: 900; color: #ffffff; margin: 6px 0; text-shadow: 0 0 14px rgba(239, 68, 68, 0.5);">
                {curr}{daily_burn:,.0f} <span style="font-size: 1.3rem; color: #fca5a5; font-weight: 800;">{t['daily_suffix']}</span>
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 1.15rem; color: #ffffff; margin-top: 10px; border-top: 1px solid rgba(239,68,68,0.4); padding-top: 10px;">
                <span>⏱️ {t['hourly_label']} <b style="color: #fca5a5;">{curr}{hourly_burn:,.0f}</b> {t['hourly_suffix']}</span>
                <span>📅 {t['bleed_30d_label']} <b style="color: #fca5a5;">{curr}{thirty_day_bleed:,.0f}</b></span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background: #111827; border: 1px solid #374151; border-radius: 8px; padding: 14px 18px; margin: 12px 0; font-size: 1.15rem; line-height: 1.8;">
            <div>• <span style="color: #94a3b8;">{t['lbl_base']}:</span> <b style="color: #ffffff;">{curr}{active_capex:,.2f}</b></div>
            <div>• <span style="color: #94a3b8;">{t['lbl_ld_cap']}:</span> <b style="color: #f87171;">{curr}{ld_cap:,.2f}</b></div>
            <div>• <span style="color: #94a3b8;">{t['lbl_engineer']}:</span> <b style="color: #60a5fa;">{roster['independent_engineer']}</b></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background: rgba(16, 185, 129, 0.15); border: 2px solid #10b981; border-radius: 10px; padding: 18px; margin: 14px 0;">
            <div style="font-size: 1.05rem; color: #6ee7b7; font-weight: 800; text-transform: uppercase; letter-spacing: 0.08em;">
                {t['scale_header']}
            </div>
            <div style="font-size: 1.2rem; color: #ffffff; margin-top: 10px;">
                {t['scale_gross']}: <b style="color: #a7f3d0;">{curr}{(thirty_day_bleed + ld_cap):,.2f}</b>
            </div>
            <div style="font-size: 1.2rem; color: #fca5a5; margin-top: 6px;">
                {t['scale_fee']}: <b style="color: #f87171;">-{curr}{forensic_fee:,.2f}</b>
            </div>
            <div style="border-top: 1px solid rgba(16, 185, 129, 0.5); margin-top: 12px; padding-top: 10px;">
                <div style="font-size: 0.95rem; color: #a7f3d0; text-transform: uppercase; font-weight: 800; letter-spacing: 0.05em;">
                    {t['scale_net']}
                </div>
                <div style="font-size: 2.5rem; font-weight: 900; color: #34d399; text-shadow: 0 0 14px rgba(16, 185, 129, 0.4);">
                    {curr}{net_preserved:,.2f}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_legal:
        st.markdown(f"""
        <div style="margin-bottom: 12px;">
            <div style="font-size: 1.35rem; font-weight: 800; color: #ffffff;">
                ⚖️ {t['counsel_seat']}: <span style="color: #60a5fa;">{roster['general_counsel']}</span>
            </div>
            <div style="font-size: 1.1rem; color: #94a3b8; margin-top: 4px;">
                {t['counsel_role']}
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="font-size: 1.15rem; color: #34d399; font-weight: 900; letter-spacing: 0.05em; text-transform: uppercase; margin: 14px 0 6px 0;">
            🛡️ {t['shield_header']}
        </div>
        """, unsafe_allow_html=True)

        st.success(f"**{t['forum_label']}:** {scenario_data['court_forum']}")

        hold_badge_color = "#ef4444" if st.session_state.mandate_executed else "#94a3b8"
        hold_text = t['hold_active'] if st.session_state.mandate_executed else t['hold_pending']

        st.markdown(f"""
        <div style="background: #111827; border: 1px solid #374151; border-radius: 8px; padding: 14px 18px; margin: 14px 0; font-size: 1.15rem; line-height: 1.9;">
            <div>• <span style="color: #94a3b8;">{t['safe_harbor_label']}:</span> <b style="color: #34d399;">{scenario_data['statutory_safe_harbor']}</b></div>
            <div>• <span style="color: #94a3b8;">{t['evidence_label']}:</span> <b style="color: #ffffff;">{scenario_data['evidence_standard']}</b></div>
            <div>• <span style="color: #94a3b8;">{t['hold_status_label']}:</span> <b style="color: {hold_badge_color};">{hold_text}</b></div>
            <div>• <span style="color: #94a3b8;">{t['consortium_label']}:</span> <b style="color: #e2e8f0;">{prov['co_investors']}</b></div>
            <div>• <span style="color: #94a3b8;">{t['counterparty_label']}:</span> <b style="color: #f87171;">{scenario_data['counterparty_entity']}</b></div>
        </div>
        """, unsafe_allow_html=True)

        with st.expander(t['provenance_title'], expanded=True):
            st.markdown(f"""
            <div style="font-size: 1.1rem; line-height: 1.8; color: #e2e8f0;">
                <div>• <span style="color: #94a3b8;">{t['prov_source']}:</span> <b style="color: #ffffff;">{prov['ingestion_doc_id']}</b></div>
                <div>• <span style="color: #94a3b8;">{t['prov_standard']}:</span> <b style="color: #ffffff;">{prov['derivation_standard']}</b></div>
                <div>• <span style="color: #94a3b8;">{t['prov_hash']}:</span> <code style="font-size: 0.95rem; color: #34d399;">{prov['sha256_root']}</code></div>
                <div style="margin-top: 8px; color: #38bdf8; font-weight: 600;">• {t['prov_legal']}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    if not st.session_state.mandate_executed:
        st.warning(t["airlock_warning"])
        if st.button(t["airlock_btn"], type="primary", use_container_width=True):
            st.session_state.mandate_executed = True
            st.rerun()
    else:
        st.success(t["airlock_success"])
        st.markdown("""
        <style>
        div.stButton > button[key="btn_go_de_ops"] {
            background-color: #f59e0b !important;
            color: #000000 !important;
            font-weight: 900 !important;
            font-size: 1.05rem !important;
            border: 2px solid #d97706 !important;
            border-radius: 8px !important;
            padding: 12px 16px !important;
            box-shadow: 0 0 12px rgba(245, 158, 11, 0.4) !important;
        }
        div.stButton > button[key="btn_go_de_legal"] {
            background-color: #38bdf8 !important;
            color: #000000 !important;
            font-weight: 900 !important;
            font-size: 1.05rem !important;
            border: 2px solid #0284c7 !important;
            border-radius: 8px !important;
            padding: 12px 16px !important;
            box-shadow: 0 0 12px rgba(56, 189, 248, 0.4) !important;
        }
        </style>
        """, unsafe_allow_html=True)
        o1, o2 = st.columns(2)
        with o1:
            st.button(
                f"{t['btn_ops']} ({roster['independent_engineer'].split(',')[0]})",
                key="btn_go_de_ops",
                on_click=cb_goto_tier_3a,
                use_container_width=True
            )
        with o2:
            st.button(
                f"{t['btn_legal']} ({roster['general_counsel'].split('(')[0].strip()})",
                key="btn_go_de_legal",
                on_click=cb_goto_legal,
                use_container_width=True
            )


def render_tier_2a_governance(scenario_data, is_de=False):
    roster = scenario_data["named_roster"]

    st.markdown("## 🏛️ TIER 2A | CHAIRMAN DIRECTORATE GOVERNANCE")
    st.info("Direct Board Oversight & Statutory Resolution Registry Active.")

    st.markdown(f"""
    * **Supervisory Chair:** `{roster['supervisory_chair']}`
    * **Executive CEO:** `{roster['executive_ceo']}`
    * **Safe Harbor:** {scenario_data['statutory_safe_harbor']}
    * **Forum:** {scenario_data['court_forum']}
    """)

    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        st.button("⬅️ Return to Command Post (Tier 1A)", on_click=cb_goto_tier_1a, use_container_width=True)
    with c2:
        st.button("➔ Advance to Engineering Operations (Tier 3A)", type="primary", on_click=cb_goto_tier_3a, use_container_width=True)


def render_tier_3a_engineering(scenario_data, is_de=False):
    roster = scenario_data["named_roster"]
    prov = scenario_data["provenance_data"]

    st.markdown("## ⚡ TIER 3A | ENGINEERING OPERATIONS COMMAND")
    st.caption(f"Lead Certifying Engineer: **{roster['independent_engineer']}** | Standards: DIN EN ISO/IEC 17025")

    st.success("🔓 **STATUTORY ACCESS GRANTED:** Full telemetry bus logs, calibration certificates, and contractor default notices unsealed.")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🔌 Inter-Array 66kV Phase Distortion Log")
        st.error(f"**Critical Breach:** {scenario_data['technical_drift_metric']}")
        st.markdown(f"""
        * **Governing Grid Code:** VDE-AR-N 4130 § 8.3 / TenneT BorWin epsilon
        * **Recorded Current Harmonic Distortion:** `3.82% THD_I` (Statutory Cap: `2.50%`)
        * **Root Mechanism:** Sub-synchronous resonance on converter filter banks
        * **VDI Work Order:** `WO-2024-DE-0941` issued for physical dampening recalibration
        """)

    with col2:
        st.markdown("### 📋 Statutory Field Directives")
        st.markdown(f"""
        * **Field Notice Target:** `{scenario_data['counterparty_entity']}`
        * **Engineering Sign-off Authority:** `{roster['independent_engineer']}`
        * **Cryptographic Telemetry Seal:** `{prov['sha256_root'][:32]}...`
        * **Status:** Site standstill active; demurrage freeze legally confirmed
        """)

    st.markdown("---")
    nav_c1, nav_c2 = st.columns(2)
    with nav_c1:
        st.button("⬅️ Return to Command Post", on_click=cb_goto_tier_1a, use_container_width=True)
    with nav_c2:
        st.button("➔ Advance to Site Execution Desk", on_click=cb_goto_tier_3b, type="primary", use_container_width=True)


T3B_I18N = {
    "EN": {
        "title": "TIER 3B | SITE EXECUTION DESK",
        "caption": "Substation Field Telemetry, Physical Inspection & SCADA Directives | Target: ",
        "alert_title": "⚠️ ACTIVE PHYSICAL FIELD INTERVENTION | VDI / DIN EN ISO 17025 ACCREDITED",
        "alert_desc": "Raw sensory inputs, high-resolution inspection media, and hardware calibration traces captured live from the 66kV inter-array substation bus.",
        "telemetry_header": "🎛️ Substation Bus Telemetry",
        "array_arch": "Array Architecture: 64 x SG 14-236 DD Turbines (960 MW Array)",
        "rec_volt": "Recorded Voltage: 66.12 kV RMS | Frequency: 49.98 Hz",
        "harmonic_slip": "Current Harmonic Slip: 3.82% THD_I (VDE-AR-N 4130 Limit: 2.50%)",
        "osc_rig": "Oscilloscope Rig: Fluke 1777 Power Quality Analyzer (Cal ID: DE-2024-9912)",
        "directives_header": "📋 Physical Inspection Directives",
        "intervention_stat": "Intervention Status: Damping filter banks isolated for firmware recalibration",
        "lead_eng": "Lead Field Engineer: ",
        "demurrage_notice": "Demurrage Freezing Notice: Ref #LG-STGT-2024-882 served to TenneT",
        "telemetry_hash": "Telemetry Hash: ",
        "hub_header": "📥 Physical Evidence Extraction Hub",
        "hub_desc": "Direct extraction of raw telemetry logs, engineering single-line diagrams, and marine inspection video footage:",
        "card1_title": "Raw Telemetry Stream",
        "card1_sub": "Fluke 1777 66kV FFT Waveforms (.CSV)",
        "card1_btn": "⬇️ Download Telemetry (.CSV)",
        "card2_title": "Single-Line Diagrams",
        "card2_sub": "VDI 2024 Electrical CAD Plans (.PDF)",
        "card2_btn": "⬇️ Download SLD Plans (.PDF)",
        "card3_title": "ROV Inspection Media",
        "card3_sub": "Subsea J-Tube & Cable Video Logs",
        "card3_btn": "⬇️ Download Media Package",
        "btn_back": "⬅️ Back to Operations Command (Tier 3A)",
        "btn_next": "➔ Advance to Forensic Recovery Vault (Tier 4)",
    },
    "DE": {
        "title": "TIER 3B | OPERATIVER STANDORT-LEITSTAND",
        "caption": "Umspannwerk-Feldtelemetrie, physische Inspektion & SCADA-Direktiven | Ziel: ",
        "alert_title": "⚠️ AKTIVE PHYSISCHE INTERVENTION | VDI / DIN EN ISO 17025 AKKREDITIERT",
        "alert_desc": "Echtzeit-Sensordaten, hochauflösende Inspektionsmedien und Hardware-Kalibrierungsspuren direkt von der 66-kV-Park-Sammelschiene erfasst.",
        "telemetry_header": "🎛️ Sammelschienen-Telemetrie (66 kV)",
        "array_arch": "Park-Konfiguration: 64 x SG 14-236 DD Turbinen (960-MW-Gesamtfeld)",
        "rec_volt": "Gemessene Betriebsspannung: 66,12 kV RMS | Netzfrequenz: 49,98 Hz",
        "harmonic_slip": "Oberschwingungsdrift: 3,82% THD_I (VDE-AR-N 4130 Grenzwert: 2,50%)",
        "osc_rig": "Mess-Oszilloskop: Fluke 1777 Netzanalysator (Kalibrier-ID: DE-2024-9912)",
        "directives_header": "📋 Physische Inspektions-Direktiven",
        "intervention_stat": "Interventions-Status: Dämpfungsfilterkreise zur Firmware-Rekalibrierung isoliert",
        "lead_eng": "Leitender Sachverständiger: ",
        "demurrage_notice": "Stillstandsmeldung & Pönalenstopp: Az. LG Stuttgart 24-OH-882 an TenneT zugestellt",
        "telemetry_hash": "Kryptographischer Telemetrie-Hash: ",
        "hub_header": "📥 Beweismittel-Extraktionszentrum",
        "hub_desc": "Direkter Abruf gerichtsfester Roh-Telemetriedaten, elektrotechnischer Übersichts-Schaltpläne und ROV-Unterwasser-Videobeweise:",
        "card1_title": "Roh-Telemetriedatenstrom",
        "card1_sub": "Fluke 1777 66-kV FFT-Wellenformen (.CSV)",
        "card1_btn": "⬇️ Telemetriedaten herunterladen (.CSV)",
        "card2_title": "Übersichts-Schaltpläne",
        "card2_sub": "VDI 2024 CAD-Elektro-Bestandspläne (.PDF)",
        "card2_btn": "⬇️ Schaltpläne herunterladen (.PDF)",
        "card3_title": "ROV-Inspektionsmedien",
        "card3_sub": "Unterwasser-J-Tube- und Seekabel-Videoprotokolle",
        "card3_btn": "⬇️ Medienpaket herunterladen",
        "btn_back": "⬅️ Zurück zu Operations Command (Tier 3A)",
        "btn_next": "➔ Weiter zum Beweismittel-Tresor (Tier 4)",
    },
}


def render_tier_3b_site_execution(scenario_data, is_de=False):
    t = T3B_I18N["DE"] if is_de else T3B_I18N["EN"]
    roster = scenario_data["named_roster"]
    prov = scenario_data["provenance_data"]

    st.markdown(f"## ⚙️ {t['title']}")
    st.caption(f"{t['caption']}{scenario_data['counterparty_entity']}")

    st.markdown(f"""
    <div style="background: rgba(245, 158, 11, 0.12); border: 2px solid #f59e0b; border-radius: 8px; padding: 14px 18px; margin: 12px 0;">
        <div style="font-size: 1.1rem; font-weight: 800; color: #fbbf24; text-transform: uppercase;">{t['alert_title']}</div>
        <div style="font-size: 0.95rem; color: #fef3c7; margin-top: 4px;">{t['alert_desc']}</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"### {t['telemetry_header']}")
        st.markdown(f"""
        * **{t['array_arch']}**
        * **{t['rec_volt']}**
        * **{t['harmonic_slip']}**
        * **{t['osc_rig']}**
        """)
    with c2:
        st.markdown(f"### {t['directives_header']}")
        st.markdown(f"""
        * **{t['intervention_stat']}**
        * **{t['lead_eng']}** `{roster['independent_engineer']}`
        * **{t['demurrage_notice']}**
        * **{t['telemetry_hash']}** `{prov['sha256_root'][:32]}...`
        """)

    st.markdown("---")
    st.markdown(f"### {t['hub_header']}")
    st.caption(t["hub_desc"])

    d1, d2, d3 = st.columns(3)
    with d1:
        st.markdown(f"""
        <div style="background: #111827; border: 1px solid #374151; border-radius: 8px; padding: 14px; text-align: center;">
            <div style="font-size: 2.0rem;">📊</div>
            <div style="font-weight: 800; color: #ffffff; margin-top: 6px;">{t['card1_title']}</div>
            <div style="font-size: 0.8rem; color: #94a3b8; margin: 4px 0 12px 0;">{t['card1_sub']}</div>
        </div>
        """, unsafe_allow_html=True)
        raw_csv = "zeitstempel,spannung_kv,frequenz_hz,thd_i_prozent,subsynchrone_resonanz_hz\n2026-09-24T14:00:00Z,66.12,49.98,3.82,14.2\n2026-09-24T14:05:00Z,66.10,49.99,3.81,14.3"
        st.download_button(label=t["card1_btn"], data=raw_csv, file_name=f"Telemetrie_66kV_{scenario_data['scenario_id']}.csv", mime="text/csv", key="btn_dl_telemetry_t3b", use_container_width=True)

    with d2:
        st.markdown(f"""
        <div style="background: #111827; border: 1px solid #374151; border-radius: 8px; padding: 14px; text-align: center;">
            <div style="font-size: 2.0rem;">📐</div>
            <div style="font-weight: 800; color: #ffffff; margin-top: 6px;">{t['card2_title']}</div>
            <div style="font-size: 0.8rem; color: #94a3b8; margin: 4px 0 12px 0;">{t['card2_sub']}</div>
        </div>
        """, unsafe_allow_html=True)
        plan_manifest = f"ENBW HE DREIHT - 66KV SCHALTPLAN\nSachverstaendiger: {roster['independent_engineer']}\nNorm: DIN EN 61400-21 / VDE-AR-N 4130\nPruefsumme SHA-256: {prov['sha256_root']}"
        st.download_button(label=t["card2_btn"], data=plan_manifest, file_name=f"Schaltplan_66kV_{scenario_data['scenario_id']}.pdf", mime="application/pdf", key="btn_dl_cad_t3b", use_container_width=True)

    with d3:
        st.markdown(f"""
        <div style="background: #111827; border: 1px solid #374151; border-radius: 8px; padding: 14px; text-align: center;">
            <div style="font-size: 2.0rem;">🎥</div>
            <div style="font-weight: 800; color: #ffffff; margin-top: 6px;">{t['card3_title']}</div>
            <div style="font-size: 0.8rem; color: #94a3b8; margin: 4px 0 12px 0;">{t['card3_sub']}</div>
        </div>
        """, unsafe_allow_html=True)
        video_metadata = "ROV UNTERWASSER-INSPEKTIONS-PROTOKOLL (4K UHD)\nObjekt: BorWin epsilon J-Tube Kabeleinfuehrung\nKamera: Kongsberg OE14-502 Marine HD\nBeglaubigter Hash: SHA-256: 4f8a91c0e3b1285091cd"
        st.download_button(label=t["card3_btn"], data=video_metadata, file_name=f"ROV_Inspektionsprotokoll_{scenario_data['scenario_id']}.txt", mime="text/plain", key="btn_dl_media_t3b", use_container_width=True)

    st.markdown("---")
    b1, b2 = st.columns(2)
    with b1:
        st.button(t["btn_back"], on_click=cb_goto_tier_3a, use_container_width=True)
    with b2:
        st.button(t["btn_next"], type="primary", on_click=cb_goto_tier_4, use_container_width=True)


def render_tier_4_forensic_vault(scenario_data, is_de=False):
    curr = scenario_data["currency_symbol"]
    roster = scenario_data["named_roster"]
    prov = scenario_data["provenance_data"]
    active_capex = st.session_state.get("active_capex", scenario_data["capex_exposure"])

    # Header & Status
    st.markdown("## 🔐 TIER 4 | FORENSIC RECOVERY VAULT & JUDICIAL DOCKET")
    st.caption(f"Immutable Statutory Evidence Repository | Forum: {scenario_data['court_forum']}")

    st.markdown("""
    <div style="background: rgba(16, 185, 129, 0.15); border: 2px solid #10b981; border-radius: 8px; padding: 14px 18px; margin: 12px 0;">
        <div style="font-size: 1.15rem; font-weight: 800; color: #34d399; text-transform: uppercase;">
            🏛️ STATUTORY CHAIN OF CUSTODY SEALED | ZPO § 371 & FRE 902(14) READY
        </div>
        <div style="font-size: 0.95rem; color: #d1fae5; margin-top: 4px;">
            Every action, telemetry ingest, and legal notice below is immutably anchored to the master Merkle root. Tamper-evident and admissible as primary direct evidence.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Master Root & Custody Metrics
    st.markdown("### 🔏 Cryptographic Integrity & Legal Custody")
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f"""
        <div style="background: #111827; border: 1px solid #374151; border-radius: 8px; padding: 12px 16px;">
            <div style="font-size: 0.8rem; color: #94a3b8; text-transform: uppercase; font-weight: 700;">Legal Custodian</div>
            <div style="font-size: 1.15rem; color: #60a5fa; font-weight: 800; margin-top: 2px;">{roster['general_counsel'].split('(')[0].strip()}</div>
            <div style="font-size: 0.8rem; color: #e2e8f0;">Syndikusrechtsanwalt (DE Bar)</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div style="background: #111827; border: 1px solid #374151; border-radius: 8px; padding: 12px 16px;">
            <div style="font-size: 0.8rem; color: #94a3b8; text-transform: uppercase; font-weight: 700;">Forensic Engineer</div>
            <div style="font-size: 1.15rem; color: #60a5fa; font-weight: 800; margin-top: 2px;">{roster['independent_engineer'].split(',')[0].strip()}</div>
            <div style="font-size: 0.8rem; color: #e2e8f0;">Ö.b.u.v. Sachverständiger (VDI)</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
        <div style="background: #111827; border: 1px solid #374151; border-radius: 8px; padding: 12px 16px;">
            <div style="font-size: 0.8rem; color: #94a3b8; text-transform: uppercase; font-weight: 700;">Statutory Reliance Shield</div>
            <div style="font-size: 1.15rem; color: #34d399; font-weight: 800; margin-top: 2px;">AktG § 93 (BJR)</div>
            <div style="font-size: 0.8rem; color: #e2e8f0;">DIN EN ISO/IEC 17025 Accredited</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="background: #0f172a; border: 1px solid #1e293b; border-radius: 6px; padding: 10px 14px; margin: 12px 0; font-family: monospace; font-size: 0.85rem; color: #38bdf8;">
        <b>MASTER MERKLE ROOT:</b> SHA-256: {prov['sha256_root']}
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Granular Forensic Interaction Ledger
    st.markdown("### ⏱️ Sequential Forensic Chain-of-Custody Ledger")
    st.caption("Chronological, second-by-second interaction record showing all statutory actors and verified actions:")

    audit_events = [
        {
            "time": "2026-09-24 14:12:08 UTC",
            "actor": "System Automation Engine",
            "role": "Public Data Ingest",
            "action": f"Ingested audited filings ({prov['ingestion_doc_id']}). Identified 3.82% THD harmonic drift against VDE-AR-N 4130.",
            "hash": "4f8a91c0e3b1...81a0",
            "status": "INGESTED"
        },
        {
            "time": "2026-09-24 15:30:22 UTC",
            "actor": roster['independent_engineer'],
            "role": "Statutory Certifying Engineer",
            "action": "Completed independent DIN EN 61000-4-30 Class A FFT calibration sweep. Executed sworn engineering affidavit attesting to converter sub-synchronous resonance.",
            "hash": "8c7d31f99a02...41bc",
            "status": "SWORN & SIGNED"
        },
        {
            "time": "2026-09-24 16:45:10 UTC",
            "actor": f"{roster['supervisory_chair']} / {roster['executive_ceo']}",
            "role": "Supervisory & Management Board",
            "action": "Constructive notice formally served. Unmitigated inaction holding burn calculated at €558,904/day. Fiduciary exposure entered on corporate risk ledger.",
            "hash": "19b4e602f7aa...9921",
            "status": "NOTICE SERVED"
        },
        {
            "time": "2026-09-24 17:05:44 UTC",
            "actor": roster['general_counsel'],
            "role": "General Counsel / Syndikus",
            "action": "Issued formal Litigation Hold Notice to TenneT TSO GmbH (BorWin epsilon platform). Standstill standstill period invoked under EnWG § 17.",
            "hash": "d281ac49e108...77e4",
            "status": "HOLD ACTIVE"
        },
        {
            "time": "2026-09-24 18:20:00 UTC",
            "actor": "Joint Supervisory & Legal Directorate",
            "role": "Board Directive Execution",
            "action": "2.5% Statutory Forensic Retainer ratified under AktG § 93 Business Judgment Rule. Full demurrage freeze and court bundle generation authorized.",
            "hash": "e3b0c44298fc...b855",
            "status": "RATIFIED"
        }
    ]

    for ev in audit_events:
        st.markdown(f"""
        <div style="background: #111827; border-left: 4px solid #38bdf8; border-radius: 4px; padding: 12px 16px; margin: 10px 0;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-family: monospace; font-size: 0.85rem; color: #94a3b8;">📅 {ev['time']}</span>
                <span style="background: #0369a1; color: #ffffff; font-size: 0.75rem; font-weight: 800; padding: 2px 8px; border-radius: 4px;">{ev['status']}</span>
            </div>
            <div style="font-size: 1.05rem; font-weight: 700; color: #ffffff; margin-top: 4px;">
                👤 {ev['actor']} <span style="font-size: 0.85rem; font-weight: 400; color: #94a3b8;">({ev['role']})</span>
            </div>
            <div style="font-size: 0.95rem; color: #cbd5e1; margin-top: 4px;">
                {ev['action']}
            </div>
            <div style="font-family: monospace; font-size: 0.8rem; color: #64748b; margin-top: 6px;">
                SHA-256 HASH: {ev['hash']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Exportable Multi-Modal Judicial Artifacts
    st.markdown("### 📦 Certified Judicial Evidence Exhibits (ZPO § 371 / FRE 902)")
    st.caption("All artifacts are cryptographically signed, timestamped, and exportable for court submission:")

    with st.expander("📄 EXHIBIT A: Statutory Ingestion Root & Grid Restudy Record", expanded=False):
        st.markdown(f"""
        * **Document Identifier:** `{prov['ingestion_doc_id']}`
        * **Sovereign Source:** Bundesnetzagentur (BNetzA) & EnBW 2024 Semi-Annual Filing
        * **Finding:** Synchronization halted at 66kV bus bar due to 3.82% THD harmonic drift.
        """)
        st.download_button(
            "⬇️ Download Exhibit A (.PDF)",
            data=f"EXHIBIT A: Sovereign Ingestion Filing {prov['ingestion_doc_id']}",
            file_name="Exhibit_A_Sovereign_Ingest.pdf",
            mime="application/pdf",
            key="dl_ex_a"
        )

    with st.expander("🎥 EXHIBIT B: Sworn Expert Deposition & Video Testimony", expanded=False):
        st.markdown(f"""
        * **Deponent:** `{roster['independent_engineer']}` (Ö.b.u.v. Sachverständiger)
        * **Format:** Recorded Sworn Video Deposition (4K / H.264) + Certified Transcript
        * **Attestation:** Confirms under penalty of perjury that harmonic instability originates inside the TenneT BorWin epsilon converter controls, fully exonerating EnBW turbine hardware.
        * **Admissibility:** Sworn under ZPO § 371 and FRE 902(14) self-authenticating standard.
        """)
        st.download_button(
            "⬇️ Download Deposition Transcript & Video Hash (.PDF)",
            data=f"CERTIFIED TESTIMONY & VIDEO TRANSCRIPT\nDeponent: {roster['independent_engineer']}\nVerified Hash: 19b4e602f7aa119b...",
            file_name="Exhibit_B_Expert_Deposition_Transcript.pdf",
            mime="application/pdf",
            key="dl_ex_b"
        )

    with st.expander("📐 EXHIBIT C: Substation Single-Line Diagrams & Telemetry Logs", expanded=False):
        st.markdown("""
        * **Contents:** 66kV Substation SLD, Harmonic Filter Calibration Data, and Oscilloscope Traces.
        * **Calibration Rig:** Fluke 1777 (Calibration ID: `DE-CAL-2024-9912`)
        * **Standard:** DIN EN 61000-4-30 Class A Compliance
        """)
        st.download_button(
            "⬇️ Download Engineering Evidence Package (.ZIP)",
            data=f"ENGINEERING PACKAGE: SLD + FLUKE LOGS\nAsset: {scenario_data['asset_name']}",
            file_name="Exhibit_C_Engineering_Package.zip",
            mime="application/zip",
            key="dl_ex_c"
        )

    with st.expander("⚖️ EXHIBIT D: AktG § 93 / § 116 Supervisory Board Fiduciary Shield", expanded=False):
        st.markdown(f"""
        * **Addressed To:** {roster['supervisory_chair']} & {roster['general_counsel']}
        * **Legal Weight:** Primary reliance instrument insulating directors from joint-venture liability claims by Allianz, AIP, and Norges Bank.
        """)
        st.download_button(
            "⬇️ Download Certified Fiduciary Shield Directive (.PDF)",
            data=f"AKTG § 93 FIDUCIARY SHIELD DIRECTIVE\nAuthorized for: {roster['supervisory_chair']}",
            file_name="Exhibit_D_AktG93_Fiduciary_Shield.pdf",
            mime="application/pdf",
            key="dl_ex_d"
        )

    st.markdown("---")

    # Master Court Export Button
    docket_text = f"""================================================================================
GERICHTLICHE BEWEISSICHERUNGSDOSSIER GEM. ZPO § 371 / FRE 902(14)
LANDGERICHT STUTTGART / OLG FRANKFURT
================================================================================
ASSET: {scenario_data['asset_name']}
OPERATING ENTITY: {scenario_data['corporate_entity']}
COUNTERPARTY: {scenario_data['counterparty_entity']}
ACTIVE CAPEX: {curr}{active_capex:,.2f}
MASTER MERKLE ROOT: {prov['sha256_root']}
CUSTODIAN: {roster['general_counsel']}
INDEPENDENT ENGINEER: {roster['independent_engineer']}

CHRONOLOGICAL EVENT LOG:
- 2026-09-24 14:12:08 UTC | Public Ingestion Verified | BNetzA Doc: {prov['ingestion_doc_id']}
- 2026-09-24 15:30:22 UTC | DIN EN 61000-4-30 Calibration Executed | 3.82% THD Breach Confirmed
- 2026-09-24 16:45:10 UTC | Board Constructive Notice Served | Carrying Cost Burn Logged
- 2026-09-24 17:05:44 UTC | Litigation Hold Served on TenneT TSO GmbH
- 2026-09-24 18:20:00 UTC | AktG § 93 Mandate Formally Ratified

CERTIFICATION:
This electronic record constitutes primary judicial evidence under German ZPO § 371.
All SHA-256 hashes are mathematically verified against original hardware telemetry.
================================================================================
"""

    st.download_button(
        label="📥 EXPORT SEALED MASTER JUDICIAL DOSSIER (.TXT / COURT DOCKET)",
        data=docket_text,
        file_name=f"Forensic_Judicial_Docket_{scenario_data['scenario_id']}.txt",
        mime="text/plain",
        use_container_width=True
    )

    st.markdown("---")
    st.button("⬅️ Return to Chairman Tactical Command Post (Tier 1A)", on_click=cb_goto_tier_1a, use_container_width=True)


def render_legal_statutory_track(scenario_data, is_de=False):
    roster = scenario_data["named_roster"]
    prov = scenario_data["provenance_data"]

    st.markdown("## ⚖️ LEGAL & STATUTORY TRACK")
    st.caption(f"General Counsel: **{roster['general_counsel']}** | Forum: {scenario_data['court_forum']}")
    st.success("Legal statutory track active. Litigation hold and ZPO evidence custody are available for review.")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Statutory Ledger")
        st.markdown(f"""
        * **Safe Harbor:** {scenario_data['statutory_safe_harbor']}
        * **Evidence Standard:** {scenario_data['evidence_standard']}
        * **Counterparty:** `{scenario_data['counterparty_entity']}`
        """)
    with col2:
        st.markdown("### Evidence Provenance")
        st.markdown(f"""
        * **Ingestion:** `{prov['ingestion_doc_id']}`
        * **Standard:** `{prov['derivation_standard']}`
        * **Hash:** `{prov['sha256_root']}`
        """)


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
    st.session_state.selected_book_name = st.session_state.get(
        "selected_book", next(iter(SCENARIOS_MAP)) if SCENARIOS_MAP else next(iter(OPERATING_BOOKS))
    )
if st.session_state.selected_book_name not in OPERATING_BOOKS:
    st.session_state.selected_book_name = next(iter(SCENARIOS_MAP)) if SCENARIOS_MAP else next(iter(OPERATING_BOOKS))

# ==============================================================================
# GLOBAL LOCKDOWN STATE EVALUATION (DUAL EXECUTIVE FINAL SIGN-OFF)
# ==============================================================================
is_master_sealed = st.session_state.get("chair_final_signed", False) and st.session_state.get("clo_final_signed", False)

SIDEBAR_I18N = {
    "EN": {
        "book": "OPERATING BOOK (GLOBAL DISPUTED ASSETS)",
        "currency": "OPERATING CURRENCY",
        "baseline": "Baseline Exposure",
        "lang_label": "🌐 JURISDICTION LANGUAGE / SPRACHE",
        "jurisdiction": "SOVEREIGN LEGAL JURISDICTION",
        "docket": "Docket",
        "law": "Governing Law",
        "counterparty": "Counterparty",
        "desk": "Command Desk",
        "track_label": "Select Operating Track:",
        "track_comm": "🗂️ Commercial & Operations Track",
        "track_legal": "⚖️ Legal & Statutory Track",
        "comm_hierarchy": "Commercial Hierarchy:",
        "legal_hierarchy": "Legal & Statutory Hierarchy:",
    },
    "DE": {
        "book": "PORTFOLIO (GLOBAL STRITTIGE ANLAGEN)",
        "currency": "BETRIEBSWÄHRUNG",
        "baseline": "Ausgangs-Bemessungsgrundlage",
        "lang_label": "🌐 SPRACHE / JURISDICTION LANGUAGE",
        "jurisdiction": "HOHEITLICHER GERICHTSSTAND",
        "docket": "Aktenzeichen",
        "law": "Anwendbares Recht",
        "counterparty": "Verzugsgegner",
        "desk": "Leitstand",
        "track_label": "Betriebspfad wählen:",
        "track_comm": "🗂️ Operativer & Kaufmännischer Pfad",
        "track_legal": "⚖️ Rechtlicher & Statutarischer Pfad",
        "comm_hierarchy": "Operative Hierarchie:",
        "legal_hierarchy": "Rechtliche Hierarchie:",
    },
}

with st.sidebar:
    st.markdown("""
        <div style="padding: 6px 0 16px 0;">
            <div style="font-size: 1.1rem; font-weight: 900; color: #ffffff; letter-spacing: 0.05em;">
                ⚡ AUTONOMOUS CAPITAL DEFENSE
            </div>
            <div style="font-size: 0.75rem; color: #94a3b8; font-weight: 600; text-transform: uppercase;">
                Forensic Claims Engine • Build v6.8
            </div>
        </div>
    """, unsafe_allow_html=True)

    selected_book_default = st.session_state.selected_book_name
    selected_scenario_default = SCENARIOS_MAP.get(selected_book_default, {})
    language_default = "Deutsch (DE)" if "DE" in selected_scenario_default.get("jurisdiction_code", "") else "English (EN)"
    selected_language_state = st.session_state.get("app_language_toggle", language_default)
    language_strings = SIDEBAR_I18N["DE"] if "Deutsch" in selected_language_state else SIDEBAR_I18N["EN"]
    selected_lang = st.selectbox(
        language_strings["lang_label"],
        options=["English (EN)", "Deutsch (DE)"],
        index=1 if language_default == "Deutsch (DE)" else 0,
        key="app_language_toggle",
    )
    is_de = "Deutsch" in selected_lang
    sb = SIDEBAR_I18N["DE"] if is_de else SIDEBAR_I18N["EN"]

    st.markdown(f"""
        <div style="font-size: 0.85rem; font-weight: 800; color: #94a3b8; text-transform: uppercase; margin-bottom: 6px; letter-spacing: 0.5px;">
            📁 {sb['book']}
        </div>
    """, unsafe_allow_html=True)
    
    selected_book = st.selectbox(
        sb["book"],
        options=list(SCENARIOS_MAP.keys()) if SCENARIOS_MAP else list(OPERATING_BOOKS.keys()),
        key="selected_book_name",
        label_visibility="collapsed"
    )
    active_cfg = OPERATING_BOOKS[selected_book]
    scenario_data = SCENARIOS_MAP.get(selected_book, {})

    # --- SIDEBAR ASSET & CURRENCY BADGE ---
    cfg = active_cfg
    curr_sym = scenario_data.get("currency_symbol", scenario_data.get("financials", {}).get("currency_symbol", cfg.get("currency_symbol", "$")))
    curr_code = scenario_data.get("currency_code", cfg.get("currency_code", "GBP" if curr_sym == "£" else "USD"))
    base_capex_val = cfg.get("capex_exposure", cfg.get("default_capex", 180000000 if curr_sym == "£" else 30000000))

    st.markdown(f"""
        <div style="background: #0f172a; border: 1px solid #1e293b; border-left: 3px solid #38bdf8; padding: 6px 10px; border-radius: 4px; margin-top: -8px; margin-bottom: 14px;">
            <span style="font-size: 0.7rem; color: #94a3b8; font-weight: 700; text-transform: uppercase;">{sb['currency']}:</span>
            <span style="font-size: 0.75rem; color: #38bdf8; font-weight: 800; margin-left: 4px;">{curr_code} ({curr_sym})</span>
            <div style="font-size: 0.68rem; color: #64748b;">{sb['baseline']}: {curr_sym}{base_capex_val:,.0f}</div>
        </div>
    """, unsafe_allow_html=True)

    if st.session_state.get("last_loaded_book") != selected_book:
        st.session_state.capex_baseline = active_cfg["default_capex"]
        st.session_state.slider_capex = float(active_cfg["default_capex"])
        st.session_state.active_docket = active_cfg["docket"]
        st.session_state.active_counterparty = active_cfg["counterparty"]
        st.session_state.selected_incident_id = "INC-001"
        st.session_state.selected_director = active_cfg["lead_director"]
        st.session_state.last_loaded_book = selected_book

    st.markdown(f"""
        <div style="font-size: 0.85rem; font-weight: 800; color: #94a3b8; text-transform: uppercase; margin-top: 14px; margin-bottom: 6px; letter-spacing: 0.5px;">
            ⚖️ {sb['jurisdiction']}
        </div>
    """, unsafe_allow_html=True)
    selected_jurisdiction = st.selectbox(
        sb["law"],
        options=active_cfg["jurisdiction_options"],
        key=f"jurisdiction_{selected_book}",
        label_visibility="collapsed"
    )
    st.session_state.active_jurisdiction = selected_jurisdiction

    active_sector = selected_book
    sector = build_operating_book(active_sector)
    sector["statute"] = selected_jurisdiction
    book_config = sector["operating_book"]
    curr_sym = book_config.get("currency_symbol", sector["currency"])
    st.caption(f"{sb['docket']}: {book_config['docket']}")
    st.caption(f"{sb['law']}: {selected_jurisdiction}")
    st.caption(f"{sb['counterparty']}: {book_config['counterparty']}")
    
    calib_key = f"capex_override_{active_sector}"
    if calib_key not in st.session_state:
        st.session_state[calib_key] = int(sector["asset_cap"])
    current_calib_capex = st.session_state[calib_key]
    scale_factor = current_calib_capex / sector["asset_cap"]

    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

    # ==============================================================================
    # 3. SIDEBAR WITH VISUAL LOCKS
    # ==============================================================================
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"### 🎛️ {sb['desk']}")

    track_labels = {sb["track_comm"]: TRACK_COMMERCIAL, sb["track_legal"]: TRACK_LEGAL}
    selected_track_label = st.sidebar.radio(
        sb["track_label"],
        options=list(track_labels),
        key="nav_track_selection"
    )
    selected_track = track_labels[selected_track_label]

    is_retained = st.session_state.get("mandate_executed", False)

    if selected_track == TRACK_COMMERCIAL:
        selected_tier = st.sidebar.radio(
            sb["comm_hierarchy"],
            options=COMMERCIAL_TIERS,
            key="nav_tier_commercial"
        )
        st.session_state.active_desk = selected_tier
    else:
        selected_tier = st.sidebar.radio(
            sb["legal_hierarchy"],
            options=LEGAL_TIERS,
            key="nav_tier_legal"
        )
        st.session_state.active_desk = LEGAL_DESKS[0]

    st.sidebar.markdown("---")
    st.sidebar.markdown("🖨️ **MASTER DOCKET LOCKDOWN EXPORT**")

    if is_master_sealed:
        active_capex_seal = st.session_state.get("capex_baseline", active_cfg["default_capex"])
        docket_text = f"""
======================================================================
SOVEREIGN DISPUTE SYNTHESIS & MASTER DOCKET
======================================================================
STATUS: SEALED & FILED // READ-ONLY MODE
JURISDICTION: {selected_jurisdiction}
DOCKET: {active_cfg['docket']}
CAPEX BASELINE: ${active_capex_seal:,.2f} USD
======================================================================

[X] EXECUTIVE CHAIRMAN FINAL SIGNATURE AFFIXED
[X] CHIEF LEGAL OFFICER FINAL SIGNATURE AFFIXED

======================================================================
ALL MODIFICATIONS LOCKED. SPOLIATION RISK: ZERO.
======================================================================
"""
        st.sidebar.download_button(
            label="📄 DOWNLOAD MASTER DOCKET (TXT)",
            data=docket_text,
            file_name="Master_Docket_Sealed.txt",
            mime="text/plain",
            type="primary",
            use_container_width=True
        )
        st.sidebar.success("🔒 Docket Sealed. App is in Read-Only Mode.")
    else:
        st.sidebar.button("📄 DOWNLOAD MASTER DOCKET (TXT)", disabled=True, help="Complete Dual Executive Sign-off on Tier 4 to unlock.", use_container_width=True)

    st.sidebar.markdown("---")
    if st.sidebar.button("🔄 Reset Incident / Clean Run", use_container_width=True):
        reset_entire_incident()
        st.session_state.chair_final_signed = False
        st.session_state.clo_final_signed = False
        st.session_state.capex_baseline = float(active_cfg["default_capex"])
        st.session_state.slider_chair_capex = float(active_cfg["default_capex"])
        st.session_state.slider_capex = float(active_cfg["default_capex"])
        st.rerun()

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

if active_cfg.get("scenario_id") == "DE_OFFSHORE_WIND_001":
    if selected_track == TRACK_COMMERCIAL:
        if selected_tier == TIER_1A:
            render_german_command_post(scenario_data, is_de)

        elif selected_tier == TIER_2A:
            render_tier_2a_governance(scenario_data, is_de)

        elif selected_tier == TIER_3A:
            render_tier_3a_engineering(scenario_data, is_de)

        elif selected_tier == TIER_3B:
            render_tier_3b_site_execution(scenario_data, is_de)

        elif selected_tier == TIER_4:
            render_tier_4_forensic_vault(scenario_data, is_de)

    elif selected_track == TRACK_LEGAL:
        render_legal_statutory_track(scenario_data, is_de)
    st.stop()

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
# MASTER RENDER LOOP: GLOBAL LOCKDOWN BANNER
# ==============================================================================
if is_master_sealed and st.session_state.active_desk not in [COMMERCIAL_DESKS[4], LEGAL_DESKS[3]]:
    st.markdown("""
        <div style="background: #1e1114; border: 2px solid #ef4444; border-left: 8px solid #ef4444; padding: 14px 18px; border-radius: 8px; margin-bottom: 24px; text-align: center;">
            <div style="font-size: 1.2rem; font-weight: 900; color: #f87171;">🔒 READ-ONLY MODE: DOCKET SEALED</div>
            <div style="color: #cbd5e0; font-size: 0.85rem; margin-top: 4px;">
                The Executive Chairman and CLO have instigated collective action. All prior state inputs, sliders, and gates are permanently locked to preserve evidentiary integrity under FRE 902.
            </div>
        </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# TIER 1A: CHAIRMAN TACTICAL COMMAND POST (COMMERCIAL PREROGATIVE)
# ==============================================================================
if st.session_state.active_desk == DESK_OPTIONS[0]:
    cfg = book_config
    if "capex_baseline" not in st.session_state:
        st.session_state.capex_baseline = float(cfg["default_capex"])
    if "slider_capex" in st.session_state:
        st.session_state.capex_baseline = float(st.session_state.slider_capex)
    if "burn_halted" not in st.session_state:
        st.session_state.burn_halted = False

    is_sealed = st.session_state.get("docket_inception_sealed", False)
    k1 = st.session_state.get("key_chairman_armed", False)
    k2 = st.session_state.get("key_counsel_armed", False)
    current_capex = float(st.session_state.capex_baseline)

    forum = scenario_data.get(
        "court_forum",
        scenario_data.get("jurisdiction", {}).get("court_name", selected_jurisdiction),
    )
    st.markdown("## 🏛️ TIER 1 | JUDICIAL EVIDENCE SEALING & EXECUTIVE COMMAND POST")
    st.caption(f"Fiduciary Airlock & Sovereign Asset Defense | Forum: {forum}")

    # --- COMMAND GATEWAY: SENSITIVITY & AUDITED BASELINE ---
    curr_sym = scenario_data.get(
        "currency_symbol",
        scenario_data.get("financials", {}).get(
            "currency_symbol",
            "£" if ("GBR" in str(cfg) or "Subsea" in str(cfg) or "Caledonia" in str(cfg)) else "$",
        ),
    )
    curr_code = "GBP" if curr_sym == "£" else "USD"
    base_floor = float(cfg.get("capex_exposure", 180000000 if curr_sym == "£" else 300000000))
    matrix_cfg = scenario_data.get("sensitivity_matrix", {
        "framework_title": "Fiduciary Sensitivity Matrix | Capital Exposure Calibration",
        "framework_subtitle": "Deterministic balance-sheet stress-testing across audited capital allocations:",
        "slider_caption": "Calibrate Balance Sheet Exposure Baseline:",
        "base_btn_caption": "Audited Sovereign Filings",
        "presets": [
            {"label": "Stress Case 1", "val": base_floor * 0.25, "desc": "Sub-Component Risk"},
            {"label": "Stress Case 2", "val": base_floor * 0.60, "desc": "Transmission / Tie-In Risk"},
            {"label": "Full Scope", "val": base_floor * 1.25, "desc": "Full Program Exposure"},
        ],
    })

    # Initialize slider key if not present
    if "slider_capex" not in st.session_state:
        st.session_state.slider_capex = base_floor

    # Callback helper to ensure buttons override the slider instantly
    def update_capex_target(target_amount):
        st.session_state.slider_capex = float(target_amount)
        st.session_state.capex_baseline = float(target_amount)

    st.markdown(f"### 🎛️ {matrix_cfg['framework_title']}")
    st.caption(matrix_cfg["framework_subtitle"])

    base_label = (
        f"{curr_sym}{base_floor / 1e9:.1f}B"
        if base_floor >= 1e9
        else f"{curr_sym}{base_floor / 1e6:.0f}M"
    )

    # 4 Preset Buttons with Contextual Metadata
    b_col1, b_col2, b_col3, b_col4 = st.columns(4)

    with b_col1:
        st.button(
            f"⭐ Base ({base_label})",
            key="btn_preset_base",
            on_click=update_capex_target,
            args=(base_floor,),
            use_container_width=True
        )
        st.caption(matrix_cfg["base_btn_caption"])

    for index, preset in enumerate(matrix_cfg["presets"]):
        with (b_col2, b_col3, b_col4)[index]:
            st.button(
                preset["label"],
                key=f"btn_preset_{index}",
                on_click=update_capex_target,
                args=(preset["val"],),
                use_container_width=True,
            )
            st.caption(preset["desc"])

    # Synchronized CapEx Slider
    active_capex = st.slider(
        matrix_cfg["slider_caption"],
        min_value=float(base_floor * 0.1),
        max_value=float(base_floor * 1.5),
        step=float(base_floor * 0.02),
        key="slider_capex"
    )
    st.session_state.capex_baseline = float(active_capex)
    current_capex = float(active_capex)

    # Financial Calculations
    daily_holding_burn = (active_capex * 0.12) / 365.0
    accrued_demurrage = daily_holding_burn * 7.0
    fee_percentage = 0.025  # 2.5% Sovereign Recovery Success Fee
    platform_recovery_fee = active_capex * fee_percentage

    # 4-Column KPI Grid with Restored Recovery Fee
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)

    with m_col1:
        st.markdown(f"""
            <div style="background: #0f172a; border: 1px solid #1e293b; padding: 12px; border-radius: 6px;">
                <div style="font-size: 0.7rem; color: #94a3b8; font-weight: 700; text-transform: uppercase;">Balance Sheet CapEx</div>
                <div style="font-size: 1.1rem; font-weight: 900; color: #ffffff; margin-top: 4px;">{curr_sym}{active_capex:,.0f}</div>
            </div>
        """, unsafe_allow_html=True)

    with m_col2:
        st.markdown(f"""
            <div style="background: #0f172a; border: 1px solid #1e293b; padding: 12px; border-radius: 6px;">
                <div style="font-size: 0.7rem; color: #94a3b8; font-weight: 700; text-transform: uppercase;">Daily Holding Burn</div>
                <div style="font-size: 1.1rem; font-weight: 900; color: #ffffff; margin-top: 4px;">{curr_sym}{daily_holding_burn:,.2f} / day</div>
            </div>
        """, unsafe_allow_html=True)

    with m_col3:
        st.markdown(f"""
            <div style="background: #0f172a; border: 1px solid #1e293b; padding: 12px; border-radius: 6px;">
                <div style="font-size: 0.7rem; color: #94a3b8; font-weight: 700; text-transform: uppercase;">Accrued Demurrage (7-Day)</div>
                <div style="font-size: 1.1rem; font-weight: 900; color: #ffffff; margin-top: 4px;">{curr_sym}{accrued_demurrage:,.2f}</div>
            </div>
        """, unsafe_allow_html=True)

    with m_col4:
        st.markdown(f"""
            <div style="background: #141c2e; border: 1px solid #3b82f6; padding: 12px; border-radius: 6px;">
                <div style="font-size: 0.7rem; color: #60a5fa; font-weight: 700; text-transform: uppercase;">Forensic Fee (2.5% Retainer)</div>
                <div style="font-size: 1.1rem; font-weight: 900; color: #38bdf8; margin-top: 4px;">{curr_sym}{platform_recovery_fee:,.0f}</div>
            </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.button("⏸ Freeze Demurrage (Commercial Standstill)", key="btn_freeze_demurrage")

    # --- KEY 1: COMMIT BALANCE SHEET AND ADVANCE DIRECTLY ---
    st.markdown("---")
    st.markdown("#### 🔑 Key 1: Executive Chairman Commercial Release")
    st.caption(f"Authorizes formal liquidated damages demand against {cfg['counterparty']} and commits ${current_capex:,.0f} USD baseline to docket.")

    if st.button(
        "⚡ ENGAGE KEY 1: COMMIT BALANCE SHEET & PROCEED TO TIER 2A ➔",
        key="btn_arm_and_advance_k1",
        type="primary",
        use_container_width=True
    ):
        st.session_state.key_chairman_armed = True
        _evaluate_dual_seal()
        go_to_desk(COMMERCIAL_DESKS[1])
        st.rerun()

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
        st.button("Return to Chairman Command Post (Tier 1A)", key="t1b_to_t1a", on_click=go_to_desk, args=(DESK_OPTIONS[0],), use_container_width=True)
    with nav_col2:
        if is_sealed:
            st.button("Proceed to Legal Governance Desk (Tier 2B)", key="t1b_to_t2b", on_click=go_to_desk, args=(DESK_OPTIONS[3],), use_container_width=True, type="primary")
        else:
            st.button("Tier 2B Locked (Requires Dual-Key Inception)", key="t1b_locked", disabled=True, use_container_width=True)

# ==============================================================================
# TIER 2A: DIRECTORATE GOVERNANCE & STATUTORY RELIANCE
# ==============================================================================
elif st.session_state.active_desk == COMMERCIAL_DESKS[1]:
    cfg = book_config
    
    # 1. Safe dynamic variables from active scenario config
    is_uk = "GBR" in str(cfg) or "Subsea" in str(cfg) or "Caledonia" in str(cfg)

    tech_lead = (
        cfg.get("stakeholders", {}).get("technical_director_name") if isinstance(cfg.get("stakeholders"), dict) else None
    ) or cfg.get("technical_director") or ("Dr. Ewan Campbell" if is_uk else "Dr. Arthur Pendleton")

    reliance_statute = (
        cfg.get("jurisdiction", {}).get("statute_board_reliance") if isinstance(cfg.get("jurisdiction"), dict) else None
    ) or cfg.get("statute_board_reliance") or ("UK Companies Act 2006 s.172" if is_uk else "Delaware DGCL § 141(e)")

    pe_lead = (
        cfg.get("stakeholders", {}).get("lead_pe_name") if isinstance(cfg.get("stakeholders"), dict) else None
    ) or cfg.get("lead_pe") or ("Nigel Stewart, CEng" if is_uk else "Marcus Vance, PE")

    breach_dict = cfg.get("technical_breach") if isinstance(cfg.get("technical_breach"), dict) else {}
    breach_val = breach_dict.get("breach_value", 0.28 if is_uk else 4.1)
    breach_unit = breach_dict.get("unit_of_measure", "dB/km" if is_uk else "% THD")
    breach_metric = breach_dict.get("metric_name", "Optical Fiber Attenuation" if is_uk else "Total Harmonic Distortion (THD)")
    wo_code = breach_dict.get("hardware_work_order", "WO-9904-OPTIC-SPLICE" if is_uk else "WO-8821")
    breach_phrase = f"{breach_val} {breach_unit} {breach_metric}"

    # 2. Header Status Banner
    st.markdown(f"""
        <div style="background: #1e1114; border: 2px solid #ef4444; border-left: 8px solid #ef4444; padding: 14px 18px; border-radius: 8px; margin-bottom: 20px;">
            <div style="font-size: 0.75rem; font-weight: 800; color: #f87171; text-transform: uppercase;">STATUTORY FIDUCIARY STATUS</div>
            <div style="font-size: 1.15rem; font-weight: 900; color: #ffffff; margin-top: 2px;">GOVERNANCE DEADLOCK: TECHNICAL RELIANCE REQUIRED</div>
            <div style="color: #cbd5e0; font-size: 0.8rem; margin-top: 4px;">
                {pe_lead} cannot perform the hardware bypass until {tech_lead} executes the {reliance_statute} reliance resolution.
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 3. Dynamic Technical Director Card
    st.markdown(f"""
        <div style="background: #141c2e; border: 2px solid #3b82f6; border-radius: 8px; padding: 16px 18px; margin-bottom: 16px;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div>
                    <div style="font-size: 1.2rem; font-weight: 900; color: #ffffff;">{tech_lead}</div>
                    <div style="color: #60a5fa; font-size: 0.82rem; font-weight: 700;">Chair, Technical Integrity & Risk Committee</div>
                    <div style="color: #94a3b8; font-size: 0.75rem;">{reliance_statute} Statutory Reliance Authority</div>
                </div>
                <span style="background: #ef4444; color: #ffffff; font-size: 0.72rem; font-weight: 900; padding: 3px 8px; border-radius: 4px;">
                    ACTIVE BOTTLENECK
                </span>
            </div>
            <div style="margin-top: 12px; background: #0b1120; border-left: 3px solid #f59e0b; padding: 8px 12px; border-radius: 4px;">
                <div style="color: #cbd5e0; font-size: 0.8rem;">
                    <strong>Action Required:</strong> Formally attest to the <strong>{breach_phrase}</strong> breach from Work Order <strong>{wo_code}</strong> to absorb personal liability onto the corporate balance sheet.
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 4. Single-Action Execution Button
    def execute_director_reliance():
        st.session_state.gate_2a_cleared = True
        go_to_desk(COMMERCIAL_DESKS[2])
        st.rerun()

    if not st.session_state.get("gate_2a_cleared", False):
        st.button(
            f"⚡ EXECUTE {tech_lead.upper()} {reliance_statute.upper()} RELIANCE RESOLUTION ➔",
            key="btn_exec_reliance_dyn",
            on_click=execute_director_reliance,
            type="primary",
            use_container_width=True
        )
    else:
        st.success(f"✓ {reliance_statute} Reliance Attestation sealed by {tech_lead}.")
        st.button("🟢 PROCEED TO TIER 3A: ENGINEERING OPERATIONS COMMAND ➔", 
                  key="btn_t2a_to_t3a", on_click=go_to_desk, args=(COMMERCIAL_DESKS[2],), type="primary", use_container_width=True)

    # Return Navigation
    st.write("")
    st.markdown("---")
    st.button("△ Return to Tactical Command Post (Tier 1A)", key="btn_t2a_back", on_click=go_to_desk, args=(COMMERCIAL_DESKS[0],), use_container_width=True)

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
    # --------------------------------------------------------------------------
    # CORPORATE MINUTE REGISTRY TABLE (DYNAMIC REAL-TIME BINDING)
    # --------------------------------------------------------------------------
    st.markdown("### Corporate Minute Registry & Statutory Fiduciary Audit")
    pendleton_status = "CERTIFIED / RATIFIED" if st.session_state.get("gate_2a_cleared", False) else "PENDING RATIFICATION"
    pendleton_color = "#00ff88" if st.session_state.get("gate_2a_cleared", False) else "#f59e0b"
    table_html = f"""
    <table style="width: 100%; border-collapse: collapse; font-size: 0.85rem; margin-bottom: 20px; background: #0e1726; border-radius: 6px; overflow: hidden;">
        <thead>
            <tr style="background: #1e293b; color: #94a3b8; text-align: left;">
                <th style="padding: 10px 14px;">Committee / Seat</th>
                <th style="padding: 10px 14px;">Statutory Authority</th>
                <th style="padding: 10px 14px;">Legal Reliance Defense</th>
                <th style="padding: 10px 14px;">Minute Book Status</th>
            </tr>
        </thead>
        <tbody>
            <tr style="border-bottom: 1px solid #1e293b;"><td style="padding: 10px 14px; font-weight: 700; color: #ffffff;">Dr. Arthur Pendleton</td><td style="padding: 10px 14px; color: #cbd5e0;">Delaware DGCL Section 141(e)</td><td style="padding: 10px 14px; color: #cbd5e0;">Technical expert reliance shield</td><td style="padding: 10px 14px; font-weight: 800; color: {pendleton_color};">{pendleton_status}</td></tr>
            <tr style="border-bottom: 1px solid #1e293b;"><td style="padding: 10px 14px; font-weight: 700; color: #ffffff;">David Chen (Proxy)</td><td style="padding: 10px 14px; color: #cbd5e0;">PUCT Protocol Section 4.2</td><td style="padding: 10px 14px; color: #cbd5e0;">Regulatory standstill compliance</td><td style="padding: 10px 14px; font-weight: 800; color: #60a5fa;">STANDBY AUDITED</td></tr>
            <tr style="border-bottom: 1px solid #1e293b;"><td style="padding: 10px 14px; font-weight: 700; color: #ffffff;">Eleanor Vance, CPA</td><td style="padding: 10px 14px; color: #cbd5e0;">ISP98 Rule 5.01</td><td style="padding: 10px 14px; color: #cbd5e0;">Letter of credit default mechanics</td><td style="padding: 10px 14px; font-weight: 800; color: #60a5fa;">STANDBY AUDITED</td></tr>
            <tr><td style="padding: 10px 14px; font-weight: 700; color: #ffffff;">Executive Chairman</td><td style="padding: 10px 14px; color: #cbd5e0;">Delaware DGCL Section 141(a)</td><td style="padding: 10px 14px; color: #cbd5e0;">Business Judgment Rule</td><td style="padding: 10px 14px; font-weight: 800; color: #00ff88;">COMMITTED</td></tr>
        </tbody>
    </table>
    """
    st.markdown(table_html, unsafe_allow_html=True)
    # --------------------------------------------------------------------------
    # LEGAL OFFICER: JONATHAN STERLING, ESQ. (CORPORATE SECRETARY)
    # --------------------------------------------------------------------------
    st.markdown("### ⚖️ Legal Officer Execution & Corporate Seal")

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

    # LINEAR DESCENT GATEWAY (LEGAL TRACK)
    st.markdown("---")
    c_back2, c_next2 = st.columns([1, 2])
    with c_back2:
        st.button("△ Return to Legal Chambers (Tier 1B)",
                  key="btn_t2b_back_t1",
                  on_click=go_to_desk,
                  args=(LEGAL_DESKS[0],),
                  use_container_width=True)
    with c_next2:
        if g2b:
            st.button("🟢 PROCEED TO TIER 3: REGULATORY & INTERCONNECTION AUDIT ➔",
                      key="btn_t2b_to_leg3_ready",
                      on_click=go_to_desk,
                      args=(LEGAL_DESKS[2],),
                      type="primary",
                      use_container_width=True)
        else:
            st.button("🔴 TIER 3 LOCKED (Execute Sterling Deed Above)",
                      key="btn_t2b_locked",
                      disabled=True,
                      use_container_width=True)

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
                  on_click=go_to_desk,
                  args=(COMMERCIAL_DESKS[1],),
                  use_container_width=True)
    with col_fwd:
        if st.session_state.gate_3a_cleared:
            st.button("🟢 PROCEED TO TIER 3B: SITE EXECUTION ➔",
                      key="btn_t3a_to_t3b",
                      on_click=go_to_desk,
                      args=(COMMERCIAL_DESKS[3],),
                      type="primary",
                      use_container_width=True)
        else:
            st.button("🔴 TIER 3B LOCKED (Complete Steps 1-3 Above to Proceed)",
                      key="btn_t3a_locked",
                      disabled=True,
                      use_container_width=True)

# ==============================================================================
# TIER 3B: SITE EXECUTION DESK (DYNAMIC JURISDICTION BINDING)
# ==============================================================================
elif st.session_state.active_desk == COMMERCIAL_DESKS[3]:
    cfg = book_config
    is_uk = "GBR" in str(cfg) or "Subsea" in str(cfg) or "Caledonia" in str(cfg)

    # 1. Dynamic Stakeholder & License Extraction
    pe_name = (
        cfg.get("stakeholders", {}).get("lead_pe_name") if isinstance(cfg.get("stakeholders"), dict) else None
    ) or cfg.get("lead_pe") or ("Nigel Stewart, CEng" if is_uk else "Marcus Vance, PE")
    
    pe_reg = "ECUK Reg #884920" if is_uk else "TXLIC114902"
    
    # 2. Dynamic Breach & Work Order Metadata
    breach_dict = cfg.get("technical_breach") if isinstance(cfg.get("technical_breach"), dict) else {}
    wo_code = breach_dict.get("hardware_work_order", "WO-9904-OPTIC-SPLICE" if is_uk else "WO-8821-HARMONIC")
    breach_val = breach_dict.get("breach_value", 0.28 if is_uk else 4.1)
    breach_unit = breach_dict.get("unit_of_measure", "dB/km" if is_uk else "%")
    breach_metric = breach_dict.get("metric_name", "Optical Fiber Attenuation" if is_uk else "THD Harmonics")
    threshold_limit = breach_dict.get("threshold_limit", "< 0.16 dB/km (ITU-T G.654.E)" if is_uk else "< 3.0% (IEEE 2800)")

    # 3. Dynamic Regulatory Body & Docket
    target_gate = "Check #4 (Marine Landing COD)" if is_uk else "Check #6 (COD Attestation)"
    reg_docket = cfg.get("docket_number", "#UK_NORTHSEA_FIBER_02" if is_uk else "ERCOT Docket #54219")
    statute_board = "STATUTORY ECUK STATUS" if is_uk else "STATUTORY TBPE STATUS"
    statute_shield = "UK Companies Act 2006 s.172/232 Active" if is_uk else "Delaware DGCL § 141 Shield Active"

    # Header Banner
    st.markdown(f"""
        <div style="background: #0f172a; border-left: 6px solid #10b981; padding: 14px 18px; border-radius: 6px; margin-bottom: 20px;">
            <div style="font-size: 1.3rem; font-weight: 900; color: #ffffff;">TIER 3B | SITE EXECUTION DESK</div>
            <div style="font-size: 0.8rem; font-weight: 700; color: #34d399; letter-spacing: 0.5px; text-transform: uppercase;">
                SPECIALIZED PHYSICAL ENGINEERING & STATUTORY ATTESTATION | {pe_name} ({pe_reg})
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 3 KPI Metadata Cards
    col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
    with col_kpi1:
        st.markdown(f"""
            <div style="background: #1e293b; border: 1px solid #334155; padding: 12px; border-radius: 6px;">
                <div style="font-size: 0.7rem; color: #94a3b8; font-weight: 800; text-transform: uppercase;">Active Work Order</div>
                <div style="font-size: 1.05rem; font-weight: 900; color: #ffffff; margin: 3px 0;">{wo_code}</div>
                <div style="font-size: 0.72rem; color: #ef4444; font-weight: 700;">● P1 - CRITICAL BYPASS</div>
            </div>
        """, unsafe_allow_html=True)

    with col_kpi2:
        st.markdown(f"""
            <div style="background: #1e293b; border: 1px solid #334155; padding: 12px; border-radius: 6px;">
                <div style="font-size: 0.7rem; color: #94a3b8; font-weight: 800; text-transform: uppercase;">Target Regulatory Gate</div>
                <div style="font-size: 1.05rem; font-weight: 900; color: #ffffff; margin: 3px 0;">{target_gate}</div>
                <div style="font-size: 0.72rem; color: #38bdf8; font-weight: 600;">{reg_docket}</div>
            </div>
        """, unsafe_allow_html=True)

    with col_kpi3:
        st.markdown(f"""
            <div style="background: #1e293b; border: 1px solid #334155; padding: 12px; border-radius: 6px;">
                <div style="font-size: 0.7rem; color: #94a3b8; font-weight: 800; text-transform: uppercase;">{statute_board}</div>
                <div style="font-size: 1.05rem; font-weight: 900; color: #f59e0b; margin: 3px 0;">PENDING ATTESTATION</div>
                <div style="font-size: 0.72rem; color: #10b981; font-weight: 600;">{statute_shield}</div>
            </div>
        """, unsafe_allow_html=True)

    st.write("")

    # Execution Punch List & Live Telemetry Columns
    col_punch, col_telem = st.columns([1.1, 0.9])

    with col_punch:
        st.markdown("### Execution Punch List & Statutory Sign-Off")
        if is_uk:
            s1 = st.checkbox("Step 1: Subsea Repeater Station 3 OTDR Reflectometry Sweep", key="uk_step1")
            s2 = st.checkbox(f"Step 2: Optical Core Splice Attenuation Profile ({breach_val} {breach_unit})", key="uk_step2")
            s3 = st.checkbox("Step 3: Subsea PFE Power Feed Interlock Bypass (Covenant #COV-9904)", key="uk_step3")
            s4 = st.checkbox("Step 4: Affix Statutory CEng Digital Seal & Formally Lock Evidence", key="uk_step4")
        else:
            s1 = st.checkbox("Step 1: Rack 4 PE Calibration & Neutral Grounding Sweep", key="us_step1")
            s2 = st.checkbox(f"Step 2: Inverter Bank 1–4 Sub-Cycle Injection Sweep (THD {breach_val}%)", key="us_step2")
            s3 = st.checkbox("Step 3: Hardware PE Key Interlock Bypass (Covenant #COV-8821)", key="us_step3")
            s4 = st.checkbox("Step 4: Affix Statutory PE Digital Seal & Formally Lock Evidence", key="us_step4")

    with col_telem:
        if is_uk:
            st.markdown("### Live Telemetry (EXFO FTB-1 OTDR)")
            st.markdown(f"""
                <div style="background: #020617; border: 1px solid #1e293b; border-radius: 8px; padding: 14px 18px; font-family: monospace;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                        <span style="color: #94a3b8; font-weight: 700;">OPTICAL ATTENUATION:</span>
                        <span style="color: #ef4444; font-weight: 900;">{breach_val} {breach_unit}</span>
                    </div>
                    <div style="font-size: 0.75rem; color: #ef4444; margin-bottom: 12px;">Threshold: {threshold_limit} Breach</div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                        <span style="color: #94a3b8;">CHROMATIC DISPERSION:</span>
                        <span style="color: #38bdf8; font-weight: 800;">20.4 ps/(nm·km)</span>
                    </div>
                    <div style="display: flex; justify-content: space-between;">
                        <span style="color: #94a3b8;">OPTICAL RETURN LOSS:</span>
                        <span style="color: #34d399; font-weight: 800;">SYNCED (> 45 dB)</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("### Live Telemetry (Fluke 1775)")
            st.markdown(f"""
                <div style="background: #020617; border: 1px solid #1e293b; border-radius: 8px; padding: 14px 18px; font-family: monospace;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                        <span style="color: #94a3b8; font-weight: 700;">THD HARMONICS:</span>
                        <span style="color: #ef4444; font-weight: 900;">{breach_val}%</span>
                    </div>
                    <div style="font-size: 0.75rem; color: #ef4444; margin-bottom: 12px;">Threshold: {threshold_limit} Breach</div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                        <span style="color: #94a3b8;">INRUSH DAMPING:</span>
                        <span style="color: #38bdf8; font-weight: 800;">1.18 pu</span>
                    </div>
                    <div style="display: flex; justify-content: space-between;">
                        <span style="color: #94a3b8;">RELAY COMTRADE:</span>
                        <span style="color: #34d399; font-weight: 800;">SYNCED (10 kHz)</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

    st.write("")
    st.markdown("---")

    # --- TIER 4 TRANSITION GATE ---
    def proceed_to_tier4():
        st.session_state.gate_3b_cleared = True
        go_to_desk(COMMERCIAL_DESKS[4])  # Routes directly to Tier 4 | Forensic Recovery Vault
        st.rerun()

    all_signed = s1 and s2 and s3 and s4

    if all_signed:
        st.success(f"✓ All statutory protocols certified by {pe_name}. Evidence chain locked.")
        st.button(
            "🟢 SEAL STATUTORY EVIDENCE & PROCEED TO TIER 4 (FORENSIC VAULT) ➔",
            key="btn_t3b_to_t4",
            on_click=proceed_to_tier4,
            type="primary",
            use_container_width=True
        )
    else:
        st.button(
            "🔒 TIER 4 LOCKED (Complete all 4 sign-off steps above to proceed)",
            key="btn_t3b_locked",
            disabled=True,
            use_container_width=True
        )

    # Secondary Navigation
    st.write("")
    st.button("△ Return to Tactical Command Post (Tier 1A)", key="btn_t3b_back", on_click=go_to_desk, args=(COMMERCIAL_DESKS[0],), use_container_width=True)

# ==============================================================================
# LEGAL TIER 3: REGULATORY & INTERCONNECTION AUDIT (DYNAMIC BINDING)
# ==============================================================================
elif st.session_state.active_desk == LEGAL_DESKS[2]:
    cfg = book_config
    is_uk = "GBR" in str(cfg) or "Subsea" in str(cfg) or "Caledonia" in str(cfg)

    # 1. Dynamic Legal & Regulatory Persona
    counsel_name = "Alistair Vance, Solicitor" if is_uk else "Rachel Ramos, Esq."
    counsel_role = "Subsea Telecom & Maritime Regulatory Counsel" if is_uk else "Regulatory & Interconnection Counsel"
    statute_cite = (
        "Ofcom General Conditions of Entitlement // UK Communications Act 2003"
        if is_uk else
        "PUCT Substantive Rules § 25.101 // ERCOT Protocol § 4.2 Lead"
    )
    reg_title = "OFCOM PROTOCOL AUDIT & STATUTORY DEFAULT NOTICE" if is_uk else "PUCT PROTOCOL AUDIT & CONTRACTUAL DEFAULT NOTICE"

    # 2. Dynamic Conditions Precedent
    if is_uk:
        cond_1 = "Subsea Turnkey EPC Clause 18.4 default notice served via London Maritime EDI."
        cond_2 = "48-hour subsea core remediation window elapsed without Consortium cure."
        cond_3 = "Cable landing bypass logged as emergency maritime asset preservation under Ofcom § 12."
    else:
        cond_1 = "Turnkey EPC Clause 11.2 default notice served via certified EDI/SMTP."
        cond_2 = "90-minute cure clock logged without OEM cure response."
        cond_3 = "Substation bypass logged as emergency grid reliability event under ERCOT § 4.2."

    # Header Banner
    st.markdown(f"""
        <div style="background: #1e112a; border-left: 6px solid #a855f7; padding: 14px 18px; border-radius: 6px; margin-bottom: 20px;">
            <div style="font-size: 1.3rem; font-weight: 900; color: #ffffff;">LEGAL TIER 3 | REGULATORY & INTERCONNECTION AUDIT</div>
            <div style="font-size: 0.8rem; font-weight: 700; color: #c084fc; letter-spacing: 0.5px; text-transform: uppercase;">
                {reg_title} // {counsel_name.upper()}
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Dynamic Legal Counsel Card
    st.markdown(f"""
        <div style="background: #141324; border: 2px solid #7c3aed; border-radius: 8px; padding: 16px 18px; margin-bottom: 20px;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div>
                    <div style="font-size: 1.2rem; font-weight: 900; color: #ffffff;">{counsel_name}</div>
                    <div style="color: #a78bfa; font-size: 0.82rem; font-weight: 700;">{counsel_role}</div>
                    <div style="color: #94a3b8; font-size: 0.75rem;">{statute_cite}</div>
                </div>
                <span style="background: #7c3aed; color: #ffffff; font-size: 0.72rem; font-weight: 900; padding: 3px 8px; border-radius: 4px;">
                    STATUTORY AUDIT
                </span>
            </div>
            <div style="margin-top: 14px; background: #0c0a1a; border-left: 3px solid #38bdf8; padding: 12px 14px; border-radius: 4px;">
                <div style="color: #38bdf8; font-size: 0.75rem; font-weight: 800; text-transform: uppercase; margin-bottom: 6px;">
                    Conditions Precedent Verified:
                </div>
                <div style="color: #cbd5e0; font-size: 0.8rem; line-height: 1.5;">
                    • {cond_1}<br>
                    • {cond_2}<br>
                    • {cond_3}
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Gateway Execution Button
    def certify_legal_default():
        st.session_state.gate_legal_3_cleared = True
        go_to_desk(LEGAL_DESKS[3])
        st.rerun()

    st.button(
        "📄 CERTIFY CONTRACTUAL DEFAULT & PROCEED TO LEGAL TIER 4 (VAULT) ➔",
        key="btn_certify_default_dyn",
        on_click=certify_legal_default,
        type="primary",
        use_container_width=True
    )

    st.write("")
    st.markdown("---")
    st.button("△ Return to Governance Desk (Tier 2B)", key="btn_l3_back", on_click=go_to_desk, args=(LEGAL_DESKS[1],), use_container_width=True)

# ==============================================================================
# LEGAL TIER 4: LEGAL EVIDENCE & COLLATERAL VAULT (TARIQ AL-MANSOOR)
# ==============================================================================
elif st.session_state.active_desk == LEGAL_DESKS[3]:
    render_executive_dual_signoff()

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
        st.button("Return to Tier 2B Governance Desk", key="t3leg_to_t2b", on_click=go_to_desk, args=(DESK_OPTIONS[3],), use_container_width=True)
    with nav_col2:
        st.button("PROCEED TO TIER 4: LEGAL EVIDENCE VAULT", key="t3leg_to_t4", on_click=go_to_desk, args=(LEGAL_TIER4_LABEL,), use_container_width=True, type="primary")

elif st.session_state.active_desk in [COMMERCIAL_DESKS[4], LEGAL_DESKS[3]]:
    # 1. State Initializations
    if "chair_final_signed" not in st.session_state:
        st.session_state.chair_final_signed = False
    if "clo_final_signed" not in st.session_state:
        st.session_state.clo_final_signed = False

    # 2. Dynamic Values
    cfg = book_config
    current_capex = float(st.session_state.get("capex_baseline", cfg["default_capex"]))
    scale_factor = current_capex / float(cfg["default_capex"])
    daily_burn = float(cfg["daily_burn_base"]) * scale_factor
    accrued_demurrage = daily_burn * 7.0

    # 3. Header Banner
    st.markdown("""
        <div style="background: linear-gradient(90deg, #091e3a 0%, #102a45 100%); border-left: 8px solid #00ff88; padding: 18px 24px; border-radius: 8px; margin-bottom: 20px;">
            <div style="font-size: 1.5rem; font-weight: 900; color: #ffffff;">STAGE 04 | EXECUTIVE DUAL SIGN-OFF DOCKET</div>
            <div style="font-size: 0.85rem; font-weight: 700; color: #00ff88; margin-top: 4px;">FORENSIC EVIDENCE VAULT & SOVEREIGN COLLATERAL RECOVERY</div>
        </div>
    """, unsafe_allow_html=True)

    # 4. Two Independent Executive Sign-Off Columns
    col_chair, col_clo = st.columns(2)
    with col_chair:
        st.markdown(f"""
            <div style="background: #0d1526; border: 2px solid #1e3a8a; border-radius: 8px; padding: 18px; margin-bottom: 14px;">
                <div style="font-size: 0.75rem; font-weight: 800; color: #60a5fa; text-transform: uppercase;">COMMERCIAL AUTHORITY</div>
                <div style="font-size: 1.2rem; font-weight: 900; color: #ffffff; margin-top: 2px;">Executive Chairman</div>
                <div style="color: #94a3b8; font-size: 0.78rem; margin-bottom: 12px;">Mandate: Capital Recovery & Bank Guarantee Enforcement</div>
                <div style="background: #08101d; padding: 10px; border-radius: 4px; font-size: 0.8rem; color: #cbd5e0; line-height: 1.6;">
                    • CapEx Baseline: <strong>${current_capex:,.0f} USD</strong><br>
                    • Accrued Demurrage: <strong>${accrued_demurrage:,.2f} USD</strong><br>
                    • Substation Status: <strong>WO-8821 Executed & Verified</strong>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if not st.session_state.chair_final_signed:
            def sign_chair_final():
                st.session_state.chair_final_signed = True
            st.button("✍️ CHAIRMAN: SIGN DEMURRAGE DEMAND & LC CALL", key="btn_sign_chair_final", on_click=sign_chair_final, type="primary", use_container_width=True)
        else:
            st.success("✓ EXECUTIVE CHAIRMAN SIGNATURE AFFIXED")

    with col_clo:
        st.markdown("""
            <div style="background: #14132b; border: 2px solid #7c3aed; border-radius: 8px; padding: 18px; margin-bottom: 14px;">
                <div style="font-size: 0.75rem; font-weight: 800; color: #c084fc; text-transform: uppercase;">STATUTORY AUTHORITY</div>
                <div style="font-size: 1.2rem; font-weight: 900; color: #ffffff; margin-top: 2px;">Katherine Ross, Esq. (CLO)</div>
                <div style="color: #94a3b8; font-size: 0.78rem; margin-bottom: 12px;">Mandate: Chancery Injunction & Evidentiary Admissibility</div>
                <div style="background: #0d0c1c; padding: 10px; border-radius: 4px; font-size: 0.8rem; color: #cbd5e0; line-height: 1.6;">
                    • Fiduciary Reliance: <strong>DGCL § 141(e) Affirmed</strong><br>
                    • Regulatory Compliance: <strong>ERCOT § 4.2 / Cl. 11.2 Notice Filed</strong><br>
                    • Admissibility: <strong>FRE 902(14) Forensic Hash Sealed</strong>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if not st.session_state.clo_final_signed:
            def sign_clo_final():
                st.session_state.clo_final_signed = True
            st.button("✍️ CLO: SIGN EMERGENCY CHANCERY COMPLAINT", key="btn_sign_clo_final", on_click=sign_clo_final, type="primary", use_container_width=True)
        else:
            st.success("✓ CHIEF LEGAL OFFICER SIGNATURE AFFIXED")

    # 5. Collective Instigation Trigger
    st.write("")
    st.markdown("---")
    if st.session_state.chair_final_signed and st.session_state.clo_final_signed:
        st.markdown(f"""
            <div style="background: #062b19; border: 2px solid #00ff88; border-radius: 8px; padding: 22px; text-align: center;">
                <div style="font-size: 1.4rem; font-weight: 900; color: #00ff88;">🏆 COLLECTIVE ACTION INSTIGATED: DISPUTE DOCKET SEALED</div>
                <div style="color: #cbd5e0; font-size: 0.9rem; margin-top: 8px; line-height: 1.6;">
                    1. Emergency Injunction & TRO electronically served on Delaware Court of Chancery.<br>
                    2. ISP98 Standby Letter of Credit Draw (${accrued_demurrage:,.2f} USD) transmitted to JPMorgan Chase.<br>
                    3. FRE 902(14) chain-of-custody archive permanently sealed. Zero spoliation exposure.
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.info("🔒 **Collective Action Gate:** Both department heads must independently affix their signatures above to instigate the simultaneous court filing and bank collateral drawdown.")

    # 6. Return Navigation
    st.write("")
    c_ret1, c_ret2 = st.columns(2)
    with c_ret1:
        st.button("△ Return to Chairman Command Post (Tier 1A)", key="btn_t4_ret_comm", on_click=go_to_desk, args=(COMMERCIAL_DESKS[0],), use_container_width=True)
    with c_ret2:
        st.button("△ Return to Legal Chambers (Tier 1B)", key="btn_t4_ret_legal", on_click=go_to_desk, args=(LEGAL_DESKS[0],), use_container_width=True)

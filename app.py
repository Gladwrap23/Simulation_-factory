import streamlit as st

# -----------------------------------------------------------------------------
# 1. PAGE SETUP & EXECUTIVE PROJECTION STYLES
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="ACC Command Surface",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
    /* 🔒 HIDE TOP TOOLBAR & PREVENT HEADING CLIPPING */
    [data-testid="stHeader"] {
        display: none !important;
    }
    .block-container {
        padding-top: 2.5rem !important;
    }
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    
    /* SCOPE HEADER BOX */
    .scope-box {
        background-color: #062313;
        border: 1.5px solid #00e676;
        border-radius: 8px;
        padding: 16px 20px;
        margin-bottom: 25px;
    }
    .scope-title {
        color: #00e676;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 1.2px;
        text-transform: uppercase;
    }
    .scope-role {
        color: #ffffff;
        font-size: 1.6rem;
        font-weight: 700;
        margin-top: 4px;
    }

    /* DUAL CHANNEL BOARDROOM PROJECTION PANELS */
    .projection-target-panel {
        background-color: #0f172a;
        border: 1.5px solid #3b82f6;
        border-radius: 10px;
        padding: 22px;
        margin-bottom: 15px;
    }
    .projection-live-panel {
        background-color: #1f1315;
        border: 1.5px solid #ef4444;
        border-radius: 10px;
        padding: 22px;
        margin-bottom: 15px;
    }
    .panel-header-target {
        color: #60a5fa;
        font-size: 0.85rem;
        font-weight: 800;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 15px;
        border-bottom: 1px solid #1e3a8a;
        padding-bottom: 8px;
    }
    .panel-header-live {
        color: #f87171;
        font-size: 0.85rem;
        font-weight: 800;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 15px;
        border-bottom: 1px solid #7f1d1d;
        padding-bottom: 8px;
    }
    
    /* HIGH-PROMINENCE ATTRIBUTION CALLOUT BOX */
    .attribution-box-prominent {
        background: linear-gradient(135deg, #1e1b4b 0%, #31101d 100%);
        border: 2px solid #ff4d4d;
        box-shadow: 0 0 15px rgba(255, 77, 77, 0.25);
        border-radius: 10px;
        padding: 20px 24px;
        margin-bottom: 22px;
    }
    .attribution-title-prominent {
        color: #f87171;
        font-size: 0.85rem;
        font-weight: 900;
        letter-spacing: 1.5px;
        text-transform: uppercase;
    }
    .attribution-body-prominent {
        color: #ffffff;
        font-size: 1.22rem;
        font-weight: 700;
        margin-top: 8px;
        line-height: 1.4;
    }
</style>
""",
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# 2. STRUCTURED MONETARY DATA MAP WITH PROVENANCE TAGS
# -----------------------------------------------------------------------------
ROLE_MAP = {
    "minister": {
        "label": "🏛️ Minister for ACC & Board Chair",
        "title": "NATIONAL SCHEME FINANCIAL DRIFT",
        "data_basis": "ACC Financial Condition Report ($63.6B OCL Baseline)",
        "scenario_type": "Directional Scenario Estimate (Non-Guidance)",
        "location_val": "National Scheme",
        "location_sub": "(All 4 Operational Regions)",
        "target_metric_val": "$14.20M / week",
        "target_metric_sub": "(Allocated Comp Budget)",
        "live_metric_val": "$14.62M / week",
        "live_metric_sub": "(Actual Comp Outflow)",
        "delta": "+$420,000 / week Financial Drift",
        "target_dwell_val": "$0 / claim",
        "target_dwell_sub": "(Mandated Policy Baseline)",
        "live_dwell_val": "+$1.68M",
        "live_dwell_sub": "(Cumulative Dwell Exposure)",
        "action_badge": "STEWARDSHIP INTERVENTION REQUIRED",
        "drift_origin": "📍 Northern Region (Auckland / Whangārei Hubs) accounts for $320,000/wk (76%) of National Drift due to Orthopedic Assessment Backlog.",
        "root_cause": "Orthopedic Assessment Capacity Backlog Driving Extended Weekly Compensation Outflows Across Northern Network",
        "options": [
            "Authorize Allied Health Assessment Delegation",
            "Reallocate $2.5M Emergency Capacity Burst Fund",
        ],
    },
    "ce": {
        "label": "⚡ Chief Executive (Wellington HQ)",
        "title": "PRIMARY CAPACITY & FINANCIAL DRIFT",
        "data_basis": "ACC Weekly Comp & Clinical Assessment Expenditure Data",
        "scenario_type": "Directional Scenario Estimate",
        "location_val": "Auckland Central & Waitematā",
        "location_sub": "(Clinical Assessment Hubs)",
        "target_metric_val": "$2.10M / week",
        "target_metric_sub": "(IME & Clinical Budget)",
        "live_metric_val": "$2.82M / week",
        "live_metric_sub": "(Actual Clinical Spend)",
        "delta": "+$720,000 / week Panel Overrun",
        "target_dwell_val": "$0",
        "target_dwell_sub": "(Stagnant Claim Target)",
        "live_dwell_val": "+$3.12M",
        "live_dwell_sub": "(Unbudgeted Dwell Exposure)",
        "action_badge": "CAPACITY RE-ROUTING REQUIRED",
        "root_cause": "1,240 Stagnant IME Claims Driving Extended Income Replacement Outflows",
        "options": [
            "Re-route 300 Cases to Waikato/Bay of Plenty Panel",
            "Trigger Fast-Track Telehealth Assessment Protocol",
        ],
    },
    "rgm_north": {
        "label": "📍 RGM - Northern Region (Auckland / Northland)",
        "title": "NORTHERN REGION FINANCIAL DRIFT",
        "data_basis": "Northern Regional Operations Baseline",
        "scenario_type": "Operational Drift Model",
        "location_val": "Waitematā & Whangārei",
        "location_sub": "(Regional Clinical Hubs)",
        "target_metric_val": "$4.50M / week",
        "target_metric_sub": "(Regional Target)",
        "live_metric_val": "$4.98M / week",
        "live_metric_sub": "(Actual Regional Spend)",
        "delta": "+$480,000 / week Regional Breach",
        "target_dwell_val": "$0 / claim",
        "target_dwell_sub": "(14-Day Baseline)",
        "live_dwell_val": "+$1.15M",
        "live_dwell_sub": "(Local Bottleneck Cost)",
        "action_badge": "REGIONAL MOBILIZATION REQUIRED",
        "root_cause": "512 Blocked Orthopedic Claims in Metro Auckland & Whangārei",
        "options": [
            "Deploy Mobile Specialist Assessment Unit to Whangārei",
            "Authorize Private Hospital Panel Overflow Contract",
        ],
    },
    "rgm_midland": {
        "label": "📍 RGM - Midland Region (Waikato / Bay of Plenty)",
        "title": "MIDLAND TRIAGE & CAPACITY FINANCIAL DRIFT",
        "data_basis": "Midland Triage & Provider Allocation Data",
        "scenario_type": "Operational Drift Model",
        "location_val": "Hamilton Central & Tauranga",
        "location_sub": "(Regional Branches)",
        "target_metric_val": "$2.80M / week",
        "target_metric_sub": "(Midland Budget Target)",
        "live_metric_val": "$3.04M / week",
        "live_metric_sub": "(Actual Spend Outflow)",
        "delta": "+$240,000 / week Triage Drift",
        "target_dwell_val": "$0 / claim",
        "target_dwell_sub": "(48-Hour Standard)",
        "live_dwell_val": "+$410,000",
        "live_dwell_sub": "(Delayed Triage Exposure)",
        "action_badge": "TRIAGE CONTRACT OVERFLOW REQUIRED",
        "root_cause": "184 Cases Awaiting Clinical Triage Due to Local Provider Deficit",
        "options": [
            "Issue Overflow Capacity Contract to Local Private Network",
            "Approve Regional Case Manager Overtime Allowance",
        ],
    },
    "rgm_central": {
        "label": "📍 RGM - Central Region (Wellington / Lower NI)",
        "title": "CENTRAL REGION SURGICAL DELAY COSTS",
        "data_basis": "Central Region Surgical Panel Sign-off Registry",
        "scenario_type": "Operational Drift Model",
        "location_val": "Wellington HQ & Palmerston North",
        "location_sub": "(Regional Hubs)",
        "target_metric_val": "$3.20M / week",
        "target_metric_sub": "(Central Regional Budget)",
        "live_metric_val": "$3.48M / week",
        "live_metric_sub": "(Actual Outflow)",
        "delta": "+$280,000 / week Panel Lag Drift",
        "target_dwell_val": "$0 / claim",
        "target_dwell_sub": "(10-Day Baseline)",
        "live_dwell_val": "+$620,000",
        "live_dwell_sub": "(Delayed Surgical Exposure)",
        "action_badge": "FAST-TRACK SIGN-OFF REQUIRED",
        "root_cause": "120 Claims Stalled on Surgical Panel Approval Signatures Exceeding 30 Days",
        "options": [
            "Delegate Fast-Track Sign-off Authority to Regional Lead",
            "Re-route Claims to Hawke's Bay Assessment Panel",
        ],
    },
    "rgm_south": {
        "label": "📍 RGM - South Island (Canterbury / Otago / Southland)",
        "title": "SOUTH ISLAND REHABILITATION SERVICE COSTS",
        "data_basis": "South Island Allied Health Provider Network Records",
        "scenario_type": "Operational Drift Model",
        "location_val": "Christchurch & Dunedin",
        "location_sub": "(Service Centres)",
        "target_metric_val": "$3.70M / week",
        "target_metric_sub": "(South Island Budget)",
        "live_metric_val": "$4.05M / week",
        "live_metric_sub": "(Actual Spend)",
        "delta": "+$350,000 / week Service Deficit",
        "target_dwell_val": "$0 / claim",
        "target_dwell_sub": "(5-Day Standard)",
        "live_dwell_val": "+$890,000",
        "live_dwell_sub": "(Unplaced Client Exposure)",
        "action_badge": "ALLIED HEALTH NETWORK ACTIVATION",
        "root_cause": "290 Clients Awaiting Allied Health & Vocational Provider Placement",
        "options": [
            "Activate Emergency Allied Health Preferred Provider Network",
            "Authorize Direct Vocational Grant Streamlining",
        ],
    },
    "cm": {
        "label": "💼 Case Manager / Frontline Operator",
        "title": "INDIVIDUAL CLAIM FINANCIAL DRIFT (#ACC-2026-89421)",
        "data_basis": "Claim Registry File #ACC-2026-89421 Baseline",
        "scenario_type": "Frontline Operational Sample",
        "location_val": "Claim #ACC-2026-89421",
        "location_sub": "(Northern Hub Queue)",
        "target_metric_val": "$850 / week",
        "target_metric_sub": "(Standard Comp Baseline)",
        "live_metric_val": "$2,100 / week",
        "live_metric_sub": "(Extended Comp + Stagnant Fees)",
        "delta": "+$1,250 / week Claim Drift",
        "target_dwell_val": "$0",
        "target_dwell_sub": "(5-Day Target Baseline)",
        "live_dwell_val": "+$6,800",
        "live_dwell_sub": "(Accumulated Idle Dwell Liability)",
        "action_badge": "DELEGATION OVERRIDE REQUIRED",
        "root_cause": "Governance Stoppage: Treatment Plan Exceeds $5,000 Authority Threshold, Stalled 38 Days Awaiting Surgical Panel Sign-off",
        "options": [
            "Execute Delegated Authority Override ($5,000 Band)",
            "Escalate Directly to Regional Clinical Lead",
        ],
    },
    "support": {
        "label": "📋 Support Staff & Intake Entry Point",
        "title": "NATIONAL INTAKE GATEWAY LAG COSTS",
        "data_basis": "National Digital Intake System Log",
        "scenario_type": "Frontline Operational Sample",
        "location_val": "National Intake Gateway",
        "location_sub": "(Digital Verification)",
        "target_metric_val": "$120,000 / week",
        "target_metric_sub": "(Processing Baseline)",
        "live_metric_val": "$210,000 / week",
        "live_metric_sub": "(Actual Processing + Lag Cost)",
        "delta": "+$90,000 / week Intake Lag",
        "target_dwell_val": "$0",
        "target_dwell_sub": "(Verification Standard)",
        "live_dwell_val": "+$340,000",
        "live_dwell_sub": "(Downstream Delay Liability)",
        "action_badge": "AUTOMATED EXTRACTION REQUIRED",
        "root_cause": "Upstream Provider Data Defect: Unstructured GP Submissions Forcing Manual ICD-10 Extraction Across 430 Intake Claims",
        "options": [
            "Trigger Automated Provider Document Request",
            "Apply Fast-Track Automated Coding Validation",
        ],
    },
}

# -----------------------------------------------------------------------------
# 3. HELPER: CUSTOM EXECUTIVE METRIC CARD RENDERER WITH PROVENANCE
# -----------------------------------------------------------------------------
def render_executive_card(label, main_val, subtext="", delta="", basis_tag="", is_live=False):
    badge_html = ""
    if delta:
        badge_bg = "#3a1518" if is_live else "#1e293b"
        badge_color = "#ff4d4d" if is_live else "#60a5fa"
        badge_border = "#7f1d1d" if is_live else "#2563eb"
        badge_html = f"""
        <div style="margin-top: 6px;">
            <span style="background-color: {badge_bg}; color: {badge_color}; border: 1px solid {badge_border}; font-size: 0.78rem; font-weight: 700; padding: 3px 8px; border-radius: 4px; display: inline-block;">
                ▲ {delta}
            </span>
        </div>
        """
    
    basis_html = ""
    if basis_tag:
        basis_html = f"""
        <div style="color: #64748b; font-size: 0.70rem; font-weight: 600; margin-top: 4px; letter-spacing: 0.5px;">
            📊 Basis: {basis_tag}
        </div>
        """

    st.markdown(
        f"""
        <div style="margin-bottom: 20px;">
            <div style="color: #94a3b8; font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 3px;">
                {label}
            </div>
            <div style="font-size: 1.55rem; font-weight: 800; color: #ffffff; line-height: 1.25;">
                {main_val} 
                <span style="font-size: 0.88rem; font-weight: 400; color: #94a3b8; margin-left: 3px;">
                    {subtext}
                </span>
            </div>
            {badge_html}
            {basis_html}
        </div>
        """,
        unsafe_allow_html=True,
    )

# -----------------------------------------------------------------------------
-----------------------------------------------------------------------------# -----------------------------------------------------------------------------
# 4. SIDEBAR CONTROLS & SESSION STATE INITIALIZATION
# -----------------------------------------------------------------------------
st.sidebar.title("AAT SCHEME GOVERNANCE")

role_keys = list(ROLE_MAP.keys())

# Ensure default role exists if launching fresh
if "sb_role_matrix_select" not in st.session_state:
    st.session_state["sb_role_matrix_select"] = "minister"

# Query parameter override (for direct URL links)
query_role = str(st.query_params.get("role", "")).lower()
if query_role == "gm":
    query_role = "rgm_north"
if query_role in ROLE_MAP:
    st.session_state["sb_role_matrix_select"] = query_role

selected_key = st.sidebar.selectbox(
    "Active User Role Matrix",
    role_keys,
    format_func=lambda k: ROLE_MAP[k]["label"],
    key="sb_role_matrix_select",
)

st.sidebar.markdown("---")

if selected_key == "minister":
    st.sidebar.info("📽️ **Boardroom Governance Surface Active**\n\nDual-channel comparative matrix enabled for Minister & Board Chair.")
else:
    st.sidebar.info("⚡ **Operational Execution Glass Active**\n\nDirect capacity re-routing & intervention surface enabled.")

# 5. DYNAMIC TITLE & MAIN COMMAND SURFACE RENDERER
# -----------------------------------------------------------------------------
if selected_key == "minister":
    st.title("🏛️ ACC Board & Ministerial Command Surface")
elif selected_key == "ce":
    st.title("⚡ ACC Executive Operational Command Glass")
elif "rgm" in selected_key:
    st.title("📍 ACC Regional Operational Command Glass")
else:
    st.title("💼 ACC Frontline Operational Command Glass")

current_data = ROLE_MAP[selected_key]

st.markdown(
    f"""
    <div class="scope-box">
        <div class="scope-title">ACTIVE COMMAND SCOPE</div>
        <div class="scope-role">{current_data['label']}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

if selected_key == "minister":
    st.markdown(f"### 🎯 SYNCHRONIZED BOARDROOM MATRIX: {current_data['title']}")

    if "drift_origin" in current_data:
        st.markdown(
            f"""
            <div class="attribution-box-prominent">
                <div class="attribution-title-prominent">⚡ AUTOMATIC REGIONAL DRIFT ATTRIBUTION</div>
                <div class="attribution-body-prominent">{current_data['drift_origin']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("📍 DRILL DOWN: Focus Command Glass on Northern Region (Auckland / Whangārei)", key="btn_drilldown_north"):
            st.query_params["role"] = "rgm_north"
            st.rerun()

    col_target, col_live = st.columns(2)

    with col_target:
        st.markdown(
            """
            <div class="projection-target-panel">
                <div class="panel-header-target">🎯 TARGET BASELINE PERFORMANCE (POLICY STANDARD)</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        render_executive_card(
            "Target Network Bounds",
            current_data["location_val"],
            current_data["location_sub"],
            basis_tag=current_data["data_basis"],
        )
        
        render_executive_card(
            "Mandated Performance Metric",
            current_data["target_metric_val"],
            current_data["target_metric_sub"],
            basis_tag="Statutory Allocation Target",
        )
        
        render_executive_card(
            "Target Dwell Standard",
            current_data["target_dwell_val"],
            current_data["target_dwell_sub"],
            basis_tag="Policy Baseline Standard",
        )
        
        st.info("System operating within mandated stewardship bands.")

    with col_live:
        st.markdown(
            """
            <div class="projection-live-panel">
                <div class="panel-header-live">⚠️ LIVE OPERATING STATE (REAL-TIME ENGINE FEED)</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        render_executive_card(
            "Active Operational Location",
            current_data["location_val"],
            current_data["location_sub"],
            basis_tag=current_data["location_sub"],
        )
        
        render_executive_card(
            "Live Drift Rate",
            current_data["live_metric_val"],
            current_data["live_metric_sub"],
            delta=current_data["delta"],
            basis_tag="Live Engine Feed",
            is_live=True,
        )
        
        render_executive_card(
            "Live Dwell Bottleneck",
            current_data["live_dwell_val"],
            current_data["live_dwell_sub"],
            delta="DRIFT BREACH",
            basis_tag="Accumulated Dwell Liability",
            is_live=True,
        )
        
        st.error(f"**Identified Root Cause:** {current_data['root_cause']}")

else:
    st.subheader(f"🎯 {current_data['title']}")

    col1, col2, col3 = st.columns(3)
    with col1:
        render_executive_card(
            "📍 Target Location / Network",
            current_data["location_val"],
            current_data["location_sub"],
            basis_tag=current_data["data_basis"],
        )
    with col2:
        render_executive_card(
            "⚠️ Impact Drift Rate",
            current_data["live_metric_val"],
            current_data["live_metric_sub"],
            delta=current_data["delta"],
            basis_tag="Live Financial Drift",
            is_live=True,
        )
    with col3:
        render_executive_card(
            "🛡️ Operational Status",
            "ACTIVE DRIFT",
            "(Unmitigated Baseline)",
            delta=current_data.get("action_badge", "ACTION REQUIRED"),
            basis_tag="System Status",
            is_live=True,
        )

    st.error(f"**Root Cause:** {current_data['root_cause']}")

# -----------------------------------------------------------------------------
# 6. STRATEGIC INTERVENTIONS EXECUTION LAYER
# -----------------------------------------------------------------------------
st.markdown("---")
st.markdown("### ⚡ Strategic Interventions")

for idx, option in enumerate(current_data["options"]):
    if st.button(f"Execute: {option}", key=f"btn_app_{selected_key}_{idx}"):
        st.success(f"Command Executed: {option}")

# -----------------------------------------------------------------------------
# 7. GOVERNANCE & RISK DISCLAIMER ANCHOR
# -----------------------------------------------------------------------------
st.markdown("---")
st.caption(
    "📌 **Risk & Compliance Notice:** Figures and parameters referenced across this command surface are anchored in public statutory disclosures "
    "(including the ACC Financial Condition Report and Annual Performance Disclosures). Where scenario inputs deviate from real-time empirical engine calculations, "
    "figures are explicitly classified as **Directional Scenario Estimates** for strategic evaluation, not official company guidance or actuarial commitments."
)

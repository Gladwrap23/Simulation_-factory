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
        font-size: 1.15rem;
        font-weight: 700;
        margin-top: 8px;
        line-height: 1.4;
    }
</style>
""",
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# 2. STRUCTURED DATA MAP WITH REFINED FRONTLINE TEXT
# -----------------------------------------------------------------------------
ROLE_MAP = {
    "minister": {
        "label": "🏛️ Minister for ACC & Board Chair",
        "title": "NATIONAL SCHEME FINANCIAL DRIFT",
        "data_basis": "ACC Financial Condition Report ($63.6B OCL Baseline)",
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
        "drift_origin": "📍 100% Drift Reconciled: Northern $320k/wk (76.2%) | Midland $40k/wk (9.5%) | Central $30k/wk (7.1%) | South Island (incl. Nelson) $30k/wk (7.1%).",
        "root_cause": "Systemic Clinical Assessment & Triage Bottlenecks Driving Extended Weekly Compensation Liabilities Across Regional Networks",
        "options": [
            "Authorize Allied Health Assessment Delegation Mandate",
            "Reallocate $2.5M Emergency Capacity Burst Fund",
        ],
    },
    "rgm_north": {
        "label": "📍 RGM - Northern Region (Auckland / Northland)",
        "title": "NORTHERN REGION FINANCIAL DRIFT",
        "data_basis": "Northern Regional Operations Baseline",
        "location_val": "Waitematā & Whangārei",
        "location_sub": "(Regional Clinical Hubs)",
        "target_metric_val": "$4.50M / week",
        "target_metric_sub": "(Regional Target)",
        "live_metric_val": "$4.82M / week",
        "live_metric_sub": "(Actual Regional Spend)",
        "delta": "+$320,000 / week Regional Share (76.2%)",
        "target_dwell_val": "$0 / claim",
        "target_dwell_sub": "(14-Day Baseline)",
        "live_dwell_val": "+$1.15M",
        "live_dwell_sub": "(Local Bottleneck Cost)",
        "root_cause": "512 Blocked Orthopedic Claims in Metro Auckland & Whangārei",
        "options": [
            "Deploy Mobile Specialist Assessment Unit to Whangārei",
            "Authorize Private Hospital Panel Overflow Contract",
        ],
    },
    "rgm_south": {
        "label": "📍 RGM - South Island (Canterbury / Otago / Southland / Nelson-Marlborough)",
        "title": "SOUTH ISLAND REHABILITATION SERVICE COSTS",
        "data_basis": "South Island & Te Tau Ihu Provider Records",
        "location_val": "Christchurch, Dunedin, Nelson & Blenheim",
        "location_sub": "(Service Centres)",
        "target_metric_val": "$3.70M / week",
        "target_metric_sub": "(South Island Target)",
        "live_metric_val": "$3.73M / week",
        "live_metric_sub": "(Actual Spend)",
        "delta": "+$30,000 / week Regional Share (7.1%)",
        "target_dwell_val": "$0 / claim",
        "target_dwell_sub": "(5-Day Standard)",
        "live_dwell_val": "+$180,000",
        "live_dwell_sub": "(Nelson/Canterbury Provider Lag)",
        "root_cause": "290 Clients Awaiting Allied Health & Vocational Provider Placement across Nelson, Blenheim, and Christchurch",
        "options": [
            "Activate Emergency Allied Health Preferred Provider Network",
            "Authorize Direct Vocational Grant Streamlining in Nelson/Tasman",
        ],
    },
    "cm": {
        "label": "💼 Case Manager / Frontline Operator",
        "title": "FRONTLINE CLAIM DRIFT REGISTRY",
        "data_basis": "Active Claim Registry Files",
        "claims": {
            "Claim #ACC-2026-89421 (Auckland Central)": {
                "location_val": "Claim #ACC-2026-89421",
                "location_sub": "(Auckland Central Hub)",
                "live_metric_val": "$2,100 / week",
                "delta": "+$1,250 / week Claim Drift",
                "live_dwell_val": "+$6,800",
                "root_cause": "Governance Stoppage: Treatment Plan Exceeds $5,000 Authority Threshold, Stalled 38 Days Awaiting Surgical Panel Sign-off",
            },
            "Claim #ACC-2026-91044 (Nelson Hub)": {
                "location_val": "Claim #ACC-2026-91044",
                "location_sub": "(Nelson Service Centre)",
                "live_metric_val": "$1,720 / week",
                "delta": "+$920 / week Claim Drift",
                "live_dwell_val": "+$3,400",
                "root_cause": "Provider Bottleneck: Vocational Rehab Assessment Delay Exceeding 24 Days in Top of the South",
            },
        },
        "options": [
            "Execute Delegated Authority Override ($5,000 Band)",
            "Escalate Directly to Regional Clinical Lead",
        ],
    },
    "support": {
        "label": "📋 Support Staff & Intake Entry Point",
        "title": "NATIONAL INTAKE GATEWAY LAG COSTS",
        "data_basis": "National Digital Intake Gateway Logs",
        "location_val": "National Digital Gateway",
        "location_sub": "(Verification & Extraction)",
        "target_metric_val": "$120,000 / week",
        "target_metric_sub": "(Standard Processing)",
        "live_metric_val": "$210,000 / week",
        "live_metric_sub": "(Actual Processing + Lag Cost)",
        "delta": "+$90,000 / week Intake Lag Drift",
        "target_dwell_val": "0 Days",
        "target_dwell_sub": "(Verification Standard)",
        "live_dwell_val": "+4.2 Days Avg Lag",
        "live_dwell_sub": "(Downstream Delay Cost)",
        "root_cause": "Upstream Provider Defect: 430 Unstructured GP Submissions + 180 Document Mismatches (Nelson & Metro Intake)",
        "options": [
            "Trigger Automated Provider Document Request",
            "Apply Fast-Track Automated Coding Validation",
        ],
    },
}

# -----------------------------------------------------------------------------
# 3. HELPER METRIC CARD RENDERER WITH PROVENANCE
# -----------------------------------------------------------------------------
def render_executive_card(label, main_val, subtext="", delta="", basis_tag="", is_live=False):
    badge_html = f"""<div style="margin-top: 6px;"><span style="background-color: {'#3a1518' if is_live else '#1e293b'}; color: {'#ff4d4d' if is_live else '#60a5fa'}; border: 1px solid {'#7f1d1d' if is_live else '#2563eb'}; font-size: 0.78rem; font-weight: 700; padding: 3px 8px; border-radius: 4px; display: inline-block;">▲ {delta}</span></div>""" if delta else ""
    basis_html = f"""<div style="color: #64748b; font-size: 0.70rem; font-weight: 600; margin-top: 4px;">📊 Basis: {basis_tag}</div>""" if basis_tag else ""

    st.markdown(
        f"""
        <div style="margin-bottom: 20px;">
            <div style="color: #94a3b8; font-size: 0.72rem; font-weight: 700; text-transform: uppercase; margin-bottom: 3px;">{label}</div>
            <div style="font-size: 1.55rem; font-weight: 800; color: #ffffff;">{main_val} <span style="font-size: 0.88rem; font-weight: 400; color: #94a3b8;">{subtext}</span></div>
            {badge_html}{basis_html}
        </div>
        """,
        unsafe_allow_html=True,
    )

# -----------------------------------------------------------------------------
# 4. SIDEBAR CONTROLS & SAFE CALLBACK STATE SYNC
# -----------------------------------------------------------------------------
st.sidebar.title("AAT SCHEME GOVERNANCE")
role_keys = list(ROLE_MAP.keys())

# Safe Callback Handler to avoid StreamlitAPIException
def set_role(target_role):
    st.session_state["sb_role_matrix_select"] = target_role

if "sb_role_matrix_select" not in st.session_state:
    st.session_state["sb_role_matrix_select"] = "minister"

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

# -----------------------------------------------------------------------------
# 5. DYNAMIC TITLE & MAIN COMMAND SURFACE RENDERER
# -----------------------------------------------------------------------------
if selected_key == "minister":
    st.title("🏛️ ACC Board & Ministerial Command Surface")
elif "rgm" in selected_key:
    st.title("📍 ACC Regional Operational Command Glass")
elif selected_key == "cm":
    st.title("💼 ACC Frontline Case Management Glass")
else:
    st.title("📋 ACC Intake & Support Operational Glass")

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

# MINISTER BOARDROOM VIEW
if selected_key == "minister":
    st.markdown(
        f"""
        <div class="attribution-box-prominent">
            <div class="attribution-title-prominent">⚡ FULL 100% RECONCILED REGIONAL DRIFT ALLOCATION</div>
            <div class="attribution-body-prominent">{current_data['drift_origin']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.button(
        "📍 DRILL DOWN: Focus Command Glass on Northern Region (Auckland / Whangārei)",
        key="btn_drilldown_north",
        on_click=set_role,
        args=("rgm_north",),
    )

    col_t, col_l = st.columns(2)
    with col_t:
        st.markdown('<div class="projection-target-panel"><div class="panel-header-target">🎯 TARGET BASELINE PERFORMANCE</div></div>', unsafe_allow_html=True)
        render_executive_card("Target Bounds", current_data["location_val"], current_data["location_sub"], basis_tag=current_data["data_basis"])
        render_executive_card("Mandated Allocation", current_data["target_metric_val"], current_data["target_metric_sub"], basis_tag="Statutory Allocation Target")
        render_executive_card("Target Dwell Standard", current_data["target_dwell_val"], current_data["target_dwell_sub"], basis_tag="Policy Baseline Standard")
    with col_l:
        st.markdown('<div class="projection-live-panel"><div class="panel-header-live">⚠️ LIVE OPERATING STATE (REAL-TIME FEED)</div></div>', unsafe_allow_html=True)
        render_executive_card("Active Scope", current_data["location_val"], current_data["location_sub"], basis_tag="All 4 Regions")
        render_executive_card("Live National Drift", current_data["live_metric_val"], current_data["live_metric_sub"], delta=current_data["delta"], basis_tag="Live Engine Feed", is_live=True)
        render_executive_card("Live Dwell Bottleneck", current_data["live_dwell_val"], current_data["live_dwell_sub"], delta="DRIFT BREACH", basis_tag="Accumulated Dwell Liability", is_live=True)

# CASE MANAGER (FRONTLINE MULTI-CLAIM VIEW)
elif selected_key == "cm":
    selected_claim = st.selectbox("Select Active Frontline Claim Registry File", list(current_data["claims"].keys()))
    claim_info = current_data["claims"][selected_claim]
    
    col1, col2 = st.columns(2)
    with col1:
        render_executive_card("📍 Claim Identification", claim_info["location_val"], claim_info["location_sub"], basis_tag="Claim Registry File")
        render_executive_card("⚠️ Weekly Outflow Drift", claim_info["live_metric_val"], "(Comp Payout)", delta=claim_info["delta"], basis_tag="Live Claim Outflow", is_live=True)
    with col2:
        render_executive_card("⏳ Accumulated Dwell Liability", claim_info["live_dwell_val"], "(Idle Time Cost)", delta="GOVERNANCE STOPPAGE", basis_tag="Idle Claim Liability", is_live=True)
    
    st.error(f"**Identified Claim Bottleneck:** {claim_info['root_cause']}")

    # 🧠 SEND STOPPAGE DIRECTLY TO NOTEBOOK LM FOR ACTION PLAN
    st.markdown("---")
    st.subheader("💡 Automated AI Resolution Pathway")
    if st.button("🧠 Send Stoppage Context to NotebookLM for Action Plan", key="btn_cm_notebooklm", use_container_width=True):
        st.session_state["pending_ai_query"] = f"Action plan for {selected_claim}: {claim_info['root_cause']}"
        st.switch_page("pages/2_AI_Assistant.py")

# SUPPORT STAFF VIEW
elif selected_key == "support":
    col1, col2, col3 = st.columns(3)
    with col1:
        render_executive_card("📍 Target Location / Network", current_data["location_val"], current_data["location_sub"], basis_tag=current_data["data_basis"])
    with col2:
        render_executive_card("⚠️ Impact Drift Rate", current_data["live_metric_val"], current_data["live_metric_sub"], delta=current_data["delta"], is_live=True)
    with col3:
        render_executive_card("🛡️ Operational Status", "ACTIVE DRIFT", "(Unmitigated Baseline)", delta="ACTION REQUIRED", basis_tag="System Status", is_live=True)

    st.error(f"**Identified Systemic Root Cause:** {current_data['root_cause']}")

    # 🧠 SEND UNSTRUCTURED INTAKE DEFECTS TO NOTEBOOK LM FOR ACTION PLAN
    st.markdown("---")
    st.subheader("💡 Automated AI Intake Resolution Pathway")
    if st.button("🧠 Send Intake Defect Log to NotebookLM for Parsing Action Plan", key="btn_support_notebooklm", use_container_width=True):
        st.session_state["pending_ai_query"] = "Action plan for 430 Unstructured GP Submissions + 180 Document Mismatches causing $90k/wk intake lag drift."
        st.switch_page("pages/2_AI_Assistant.py")

# STANDARD REGIONAL VIEWS (RGMs)
else:
    col1, col2, col3 = st.columns(3)
    with col1:
        render_executive_card("📍 Target Location / Network", current_data["location_val"], current_data["location_sub"], basis_tag=current_data["data_basis"])
    with col2:
        render_executive_card("⚠️ Impact Drift Rate", current_data["live_metric_val"], current_data["live_metric_sub"], delta=current_data["delta"], is_live=True)
    with col3:
        render_executive_card("🛡️ Operational Status", "ACTIVE DRIFT", "(Unmitigated Baseline)", delta="ACTION REQUIRED", basis_tag="System Status", is_live=True)

    st.error(f"**Identified Systemic Root Cause:** {current_data['root_cause']}")

# INTERVENTIONS
st.markdown("---")
st.markdown("### ⚡ Strategic Interventions")
for idx, option in enumerate(current_data["options"]):
    if st.button(f"Execute: {option}", key=f"btn_{selected_key}_{idx}"):
        st.success(f"Command Executed: {option}")

# FOOTER DISCLAIMER
st.markdown("---")
st.caption(
    "📌 **Risk & Compliance Notice:** Figures referenced are anchored in public statutory disclosures (ACC Financial Condition Report). "
    "Operational scenario inputs are classified as Directional Scenario Estimates for strategic evaluation, not official company guidance."
)


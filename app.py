"""Standalone single-page dark cockpit for board, management, and site command."""

from datetime import datetime, timezone
from hashlib import sha256
from html import escape

import streamlit as st


st.set_page_config(
    page_title="Kinetic Dark Cockpit",
    page_icon="K",
    layout="wide",
    initial_sidebar_state="expanded",
)


def money(value):
    return f"${value:,.0f}"


def now_label():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def add_audit_record(event, detail, actor):
    previous_hash = st.session_state.audit_ledger[-1]["hash"] if st.session_state.audit_ledger else "GENESIS"
    timestamp = now_label()
    content = f"{previous_hash}|{timestamp}|{event}|{detail}|{actor}"
    record_hash = sha256(content.encode("utf-8")).hexdigest()
    st.session_state.audit_ledger.append(
        {
            "timestamp": timestamp,
            "event": event,
            "detail": detail,
            "actor": actor,
            "previous_hash": previous_hash,
            "hash": record_hash,
        }
    )


def initialize_state():
    defaults = {
        "chairman_override": False,
        "committee_investment": True,
        "committee_risk": True,
        "committee_remuneration": False,
        "committee_sustainability": True,
        "burn_resolved": False,
        "directive_issued": False,
        "directive": {},
        "audit_ledger": [],
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)
    if not st.session_state.audit_ledger:
        add_audit_record(
            "CHAIN INITIALIZED",
            "Exposure ledger sealed at $88.5M; weekly holding burn opened at $610k.",
            "System Attestation",
        )


def metric_card(label, value, note, accent="cyan"):
    st.markdown(
        f'<div class="metric-card {accent}"><div class="metric-label">{escape(label)}</div>'
        f'<div class="metric-value">{escape(value)}</div><div class="metric-note">{escape(note)}</div></div>',
        unsafe_allow_html=True,
    )


def section_heading(kicker, title, description):
    st.markdown(f'<div class="eyebrow">{escape(kicker)}</div>', unsafe_allow_html=True)
    st.header(title)
    st.caption(description)


initialize_state()

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Space+Grotesk:wght@400;500;600;700&display=swap');
    :root { --bg:#0d1117; --panel:#161b22; --panel-2:#1c242d; --line:#303945; --text:#e6edf3; --muted:#8b98a5; --cyan:#00E5FF; --green:#39d353; --amber:#f2cc60; }
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] { background:var(--bg) !important; color:var(--text) !important; }
    [data-testid="stSidebar"] { background:var(--panel) !important; border-right:1px solid var(--line); }
    [data-testid="stSidebar"] * { color:var(--text) !important; }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { color:var(--muted) !important; }
    h1,h2,h3,h4,p,span,label,div { font-family:'Space Grotesk',sans-serif; letter-spacing:0; }
    h1,h2,h3,h4 { color:var(--text) !important; }
    h1 { font-size:2.4rem; }
    h2 { margin-top:1.4rem; }
    [data-testid="stCaptionContainer"], .stCaption { color:var(--muted) !important; }
    .eyebrow { color:var(--cyan); font:500 .72rem 'DM Mono',monospace; letter-spacing:.1em; text-transform:uppercase; }
    .mono { font-family:'DM Mono',monospace; }
    .hero-line { color:var(--muted); font-size:1rem; margin-top:-.7rem; }
    .metric-card { background:var(--panel) !important; border:1px solid var(--line); border-top:2px solid var(--cyan); border-radius:4px; padding:1rem 1.1rem; min-height:124px; }
    .metric-card.green { border-top-color:var(--green); }
    .metric-card.amber { border-top-color:var(--amber); }
    .metric-label { color:var(--muted); font-size:.78rem; text-transform:uppercase; letter-spacing:.05em; }
    .metric-value { color:var(--text); font-size:1.85rem; font-weight:700; margin:.45rem 0; }
    .metric-note { color:var(--cyan); font:500 .72rem 'DM Mono',monospace; }
    .badge { background:#12343a; border:1px solid var(--cyan); border-radius:3px; color:var(--cyan); display:inline-block; font:500 .7rem 'DM Mono',monospace; margin:.15rem .3rem .15rem 0; padding:.32rem .5rem; }
    .badge.green { background:#12311d; border-color:var(--green); color:var(--green); }
    .artifact { background:var(--panel); border-left:3px solid var(--cyan); margin:.5rem 0; padding:.8rem; }
    .artifact strong { color:var(--text); display:block; }
    .artifact small { color:var(--muted); font:400 .7rem 'DM Mono',monospace; }
    .audit-row { border-bottom:1px solid var(--line); padding:.8rem 0; }
    .audit-time, .hash { color:var(--cyan); font:400 .68rem 'DM Mono',monospace; overflow-wrap:anywhere; }
    .audit-event { color:var(--text); font-weight:700; margin:.2rem 0; }
    .audit-detail { color:var(--muted); font-size:.8rem; }
    .stButton button { background:var(--panel-2); border:1px solid var(--cyan); border-radius:3px; color:var(--cyan); font-weight:700; }
    .stButton button:hover { background:#12343a; border-color:var(--cyan); color:#fff; }
    .stButton button[kind="primary"] { background:#174d29; border-color:var(--green); color:#fff; }
    div[data-baseweb="select"] > div, div[data-baseweb="input"] > div, input { background:var(--panel-2) !important; border-color:var(--line) !important; color:var(--text) !important; }
    [data-testid="stDataFrame"] { border:1px solid var(--line); }
    [data-testid="stMetric"] { background:var(--panel); border:1px solid var(--line); padding:.8rem; }
    [data-testid="stMetricValue"], [data-testid="stMetricLabel"] { color:var(--text) !important; }
    [data-testid="stProgressBar"] > div > div { background:var(--cyan); }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown('<div class="eyebrow">KINETIC ASSET MANAGEMENT</div>', unsafe_allow_html=True)
    st.title("DARK\nCOCKPIT")
    st.markdown('<div class="mono">COMMAND PLANE / 26.08</div>', unsafe_allow_html=True)
    st.divider()
    view = st.sidebar.radio(
        "Command view",
        [
            "Tier 1 | Chairman Directorate",
            "Tier 2 | General Management",
            "Tier 3 | Site Operations",
            "Forensic Audit Ledger",
        ],
    )
    st.divider()
    st.markdown("**COMMAND STATUS**")
    st.markdown('<span class="badge green">● ATTESTED / LIVE</span>', unsafe_allow_html=True)
    st.markdown("**OPERATOR**")
    st.markdown('<span class="mono">M. SERRANO / L2</span>', unsafe_allow_html=True)
    if st.session_state.directive_issued:
        st.markdown('<span class="badge">DIRECTIVE ACTIVE</span>', unsafe_allow_html=True)

st.markdown('<div class="eyebrow">EXECUTIVE OPERATING LAYER / ERCOT RECOVERY</div>', unsafe_allow_html=True)
st.title("Decision velocity, with a paper trail.")
st.markdown('<p class="hero-line">A high-contrast command surface for capital exposure, frontline execution, and accountable override.</p>', unsafe_allow_html=True)

top_one, top_two, top_three, top_four = st.columns(4)
with top_one:
    metric_card("Total exposure", "$88.5M", "board ceiling / 12 assets")
with top_two:
    burn_value = "$0 / wk" if st.session_state.burn_resolved else "$610k / wk"
    burn_note = "RESOLVED" if st.session_state.burn_resolved else "ACTIVE HOLDING BURN"
    metric_card("Weekly holding burn", burn_value, burn_note, "green" if st.session_state.burn_resolved else "amber")
with top_three:
    metric_card("Client realization", "$549k", "90% protected value")
with top_four:
    metric_card("Phoenix fee", "$61k", "10% accrued fee", "amber")

if view == "Tier 1 | Chairman Directorate":
    section_heading("TIER 1 / CHAIRMAN DIRECTORATE", "Authorization perimeter", "Board authority, capital posture, and the deconstructed realization position.")
    left, right = st.columns([1, 1.5])
    with left:
        override = st.toggle("Chairman Override", key="chairman_override")
        if override:
            st.warning("OVERRIDE ARMED / downstream actions carry chairman attestation")
        else:
            st.success("STANDARD DELEGATED AUTHORITY")
    with right:
        st.markdown("**BOARD SUB-COMMITTEE AUTHORIZATIONS**")
        committees = [
            ("committee_investment", "Investment Committee", "Capital deployment and exposure"),
            ("committee_risk", "Risk & Audit Committee", "Controls, evidence, and exceptions"),
            ("committee_remuneration", "Remuneration Committee", "People and incentive impacts"),
            ("committee_sustainability", "Sustainability Committee", "Grid resilience and impact"),
        ]
        for key, label, description in committees:
            st.toggle(label, key=key, help=description)
        authorized = sum(st.session_state[key] for key, _, _ in committees)
        st.markdown(f'<span class="badge green">{authorized}/4 AUTHORIZED</span>', unsafe_allow_html=True)
    st.divider()
    st.markdown("**90 / 10 DECONSTRUCTED REALIZATION TABLE**")
    st.dataframe(
        [
            {"Realization leg": "Client realization", "Share": "90%", "Amount": "$549,000", "Status": "PROTECTED"},
            {"Realization leg": "Phoenix fee", "Share": "10%", "Amount": "$61,000", "Status": "ACCRUED"},
            {"Realization leg": "Total decomposed value", "Share": "100%", "Amount": "$610,000", "Status": "RECONCILED"},
        ],
        use_container_width=True,
        hide_index=True,
    )

elif view == "Tier 2 | General Management":
    section_heading("TIER 2 / GENERAL MANAGEMENT", "Directive translation register", "Translate board intent into bounded surge budgets and response commitments.")
    st.markdown("**SURGE BUDGET (%)**")
    budget_cols = st.columns(3)
    for column, label, key, value in zip(
        budget_cols,
        ["Grid stabilization", "Claims response", "Evidence preservation"],
        ["grid_budget", "claims_budget", "evidence_budget"],
        [18, 12, 8],
    ):
        with column:
            st.number_input(label, min_value=0, max_value=100, value=value, step=1, format="%d", key=key)
    st.markdown("**SLA ROUTING**")
    sla_one, sla_two, sla_three = st.columns(3)
    with sla_one:
        st.selectbox("Critical incident", ["15 minutes", "30 minutes", "1 hour"], key="critical_sla")
    with sla_two:
        st.selectbox("Material exception", ["4 hours", "Same business day", "48 hours"], key="material_sla")
    with sla_three:
        st.selectbox("Routine evidence request", ["1 business day", "3 business days", "5 business days"], key="routine_sla")
    st.divider()
    if st.button("⚡ Issue Translated Directive", type="primary", use_container_width=True):
        st.session_state.directive = {
            "grid_budget": st.session_state.grid_budget,
            "claims_budget": st.session_state.claims_budget,
            "evidence_budget": st.session_state.evidence_budget,
            "critical_sla": st.session_state.critical_sla,
            "material_sla": st.session_state.material_sla,
            "routine_sla": st.session_state.routine_sla,
        }
        st.session_state.directive_issued = True
        add_audit_record("DIRECTIVE ISSUED", "Tier 2 parameters translated and published to Site Operations.", "General Management")
        st.success("TRANSLATED DIRECTIVE ISSUED TO COMMAND")
    if st.session_state.directive_issued:
        directive = st.session_state.directive
        st.markdown("**ACTIVE REGISTER**")
        st.dataframe(
            [
                {"Directive": "Grid stabilization", "Parameter": f"{directive['grid_budget']}% surge", "SLA": directive["critical_sla"], "Status": "ACTIVE"},
                {"Directive": "Claims response", "Parameter": f"{directive['claims_budget']}% surge", "SLA": directive["material_sla"], "Status": "ACTIVE"},
                {"Directive": "Evidence preservation", "Parameter": f"{directive['evidence_budget']}% surge", "SLA": directive["routine_sla"], "Status": "ACTIVE"},
            ],
            use_container_width=True,
            hide_index=True,
        )

elif view == "Tier 3 | Site Operations":
    section_heading("TIER 3 / SITE OPERATIONS", "Frontline command center", "Verify upstream governance, authenticate ERCOT artifacts, and clear the SOP gate.")
    if st.session_state.directive_issued:
        directive = st.session_state.directive
        st.markdown(
            f'<span class="badge green">UPSTREAM / TIER 2 DIRECTIVE ACTIVE</span>'
            f'<span class="badge">GRID SURGE {directive["grid_budget"]}%</span>'
            f'<span class="badge">CLAIMS SURGE {directive["claims_budget"]}%</span>'
            f'<span class="badge">CRITICAL SLA {escape(directive["critical_sla"])}</span>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown('<span class="badge">UPSTREAM / AWAITING TIER 2 DIRECTIVE</span>', unsafe_allow_html=True)
    st.markdown("**ERCOT SECTOR-PURE AUTHENTIC ARTIFACTS**")
    artifact_cols = st.columns(4)
    for column, name, detail in zip(
        artifact_cols,
        ["ICCP", "PSCAD", "IEEE 2800", "COD"],
        [
            "Inter-Control Center Communications Protocol / dispatch link",
            "Power Systems Computer Aided Design / transient model",
            "Interconnection and Interoperability Requirements / standard",
            "Commercial Operation Date / commissioning record",
        ],
    ):
        with column:
            st.markdown(f'<div class="artifact"><strong>{escape(name)}</strong><small>{escape(detail)}<br>ERCOT / VERIFIED</small></div>', unsafe_allow_html=True)
    st.markdown("**8 / 8 SOP CHECKLIST**")
    checklist = [
        "Isolation boundaries confirmed",
        "Control-room handoff logged",
        "Dispatch instruction acknowledged",
        "Protection settings cross-checked",
        "Communications path tested",
        "Contingency route rehearsed",
        "Evidence artifacts attached",
        "Supervisor review completed",
    ]
    check_cols = st.columns(2)
    for index, item in enumerate(checklist):
        with check_cols[index % 2]:
            st.checkbox(item, key=f"sop_{index}")
    all_checked = all(st.session_state.get(f"sop_{index}", False) for index in range(8))
    if all_checked and not st.session_state.burn_resolved:
        if st.button("⚡ Submit Frontline SOP Sign-off & Notify Command", type="primary", use_container_width=True):
            st.session_state.burn_resolved = True
            add_audit_record(
                "FRONTLINE SOP CLEARED",
                "8/8 checks accepted; weekly holding burn resolved from $610k / wk to $0 / wk.",
                "Site Operations",
            )
            st.rerun()
    elif all_checked:
        st.success("FRONTLINE CLEARED / COMMAND NOTIFIED / $0 PER WEEK")
    else:
        completed = sum(st.session_state.get(f"sop_{index}", False) for index in range(8))
        st.info(f"{completed}/8 checks complete. All checks are required before sign-off.")

else:
    section_heading("FORENSIC AUDIT LEDGER", "Cryptographic chain of custody", "Append-only event records link every command action to its predecessor hash.")
    audit_one, audit_two, audit_three = st.columns(3)
    with audit_one:
        st.metric("Chain state", "SEALED")
    with audit_two:
        st.metric("Weekly burn", "$0 / wk" if st.session_state.burn_resolved else "$610k / wk")
    with audit_three:
        st.metric("Records", len(st.session_state.audit_ledger))
    st.divider()
    for record in reversed(st.session_state.audit_ledger):
        st.markdown(
            f'<div class="audit-row"><div class="audit-time">{escape(record["timestamp"])} / {escape(record["actor"])}</div>'
            f'<div class="audit-event">{escape(record["event"])}</div><div class="audit-detail">{escape(record["detail"])}</div>'
            f'<div class="hash">HASH {escape(record["hash"])}<br>PREV {escape(record["previous_hash"])}</div></div>',
            unsafe_allow_html=True,
        )

st.divider()
st.caption(f"Last console render: {now_label()} | Evidence policy: source-bound, operator-attested, board-visible")

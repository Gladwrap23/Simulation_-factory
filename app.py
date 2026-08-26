import hashlib
from datetime import datetime, timezone

import streamlit as st


st.set_page_config(
    page_title="Factory Command Post",
    page_icon="FC",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        :root { --ink:#ffffff; --muted:#c9d1d9; --paper:#0d1117; --panel:#161b22;
            --line:#30363d; --teal:#00E5FF; --amber:#ffb454; --red:#ff7b72; }
        .stApp { background:var(--paper); color:var(--ink); }
    [data-testid="stHeader"] { background:transparent; }
    footer, #MainMenu { visibility:hidden; }
        h1, h2, h3 { font-family:Georgia, serif; letter-spacing:0; color:#ffffff; }
    h1 { font-size:2.5rem; line-height:1.05; }
    h2 { border-bottom:1px solid var(--line); padding-bottom:.45rem; }
    [data-testid="stMetric"] { background:var(--panel); border:1px solid var(--line);
      border-top:4px solid var(--teal); padding:1rem; }
    [data-testid="stMetricValue"] { color:#00E5FF !important; }
    .eyebrow { color:var(--teal); font:700 .75rem/1.2 monospace; letter-spacing:.12em;
      text-transform:uppercase; }
    .mast { border-bottom:5px solid var(--ink); padding:1rem 0 1.25rem; margin-bottom:1.2rem; }
    .status { background:#161b22; color:#ffffff; padding:.65rem .85rem; font:700 .8rem monospace; }
    .status span { color:#00E5FF; }
    .callout { background:#161b22; border-left:5px solid var(--teal); padding:1rem 1.1rem; }
    .artifact { background:var(--panel); border:1px solid var(--line); padding:.8rem 1rem; min-height:120px; }
    .artifact strong { color:var(--teal); font:700 .8rem monospace; }
    .lock { color:var(--red); font:700 .78rem monospace; }
        .governance-badge { display:inline-block; background:#161b22; border:1px solid #30363d;
            border-radius:4px; color:#ffffff; margin:0 .35rem .45rem 0; padding:.45rem .65rem; }
        .governance-badge strong { color:#00E5FF; }
        .governance-badge.paused { border-color:#ff7b72; color:#ff7b72; }
    section[data-testid="stSidebar"] { background:#161b22; }
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] h4,
    section[data-testid="stSidebar"] h5,
    section[data-testid="stSidebar"] h6,
    section[data-testid="stSidebar"] .stRadio label,
    section[data-testid="stSidebar"] .stCheckbox label,
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stToggle label,
    section[data-testid="stSidebar"] .stSlider label,
    section[data-testid="stSidebar"] [data-testid="stWidgetLabel"],
    section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p,
    section[data-testid="stSidebar"] [data-testid="stCaptionContainer"],
    section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p,
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] [data-baseweb="select"] *,
    section[data-testid="stSidebar"] [data-baseweb="menu"] * { opacity:1 !important; color:#ffffff !important; font-weight:600 !important; }
    section[data-testid="stSidebar"] h2 { font-size:1.35rem; }
    [data-testid="stWidgetLabel"],
    [data-testid="stWidgetLabel"] p,
    [data-testid="stMetricLabel"],
    [data-testid="stMetricLabel"] p,
    [data-testid="stCaptionContainer"],
    [data-testid="stCaptionContainer"] p,
    .callout, .callout b,
    [data-testid="stAlert"],
    [data-testid="stAlert"] * { color:#ffffff !important; font-weight:600; }
    [data-testid="stMetric"], .artifact { background:#161b22; border-color:#30363d; }
    [data-baseweb="menu"], [data-baseweb="popover"] { background:#161b22; color:#ffffff; }
    [data-baseweb="menu"] *, [data-baseweb="popover"] * { opacity:1 !important; color:#ffffff !important; font-weight:600 !important; }
    </style>
    """,
    unsafe_allow_html=True,
)


BOOKS = {
    "ERCOT_BESS": {
        "name": "ERCOT BESS / storage operations",
        "exposure": 88.5,
        "drift": 12.3,
        "burn": 610000,
        "nodes": ["BESS Storage Hub 01", "Solar Substation Beta", "ERCOT Control Centre"],
        "bottleneck": "Telemetry validation and inverter testing",
    },
    "GRID_TRANSMISSION": {
        "name": "Grid & transmission infrastructure",
        "exposure": 126.0,
        "drift": 15.7,
        "burn": 740000,
        "nodes": ["BESS Storage Hub 01", "Solar Substation Beta", "Regional Control Centre"],
        "bottleneck": "Interconnection testing and construction clearance",
    },
    "ACC_NZ": {
        "name": "ACC NZ Scheme / claims governance",
        "exposure": 210.0,
        "drift": 31.5,
        "burn": 1150000,
        "nodes": ["Northern Hub 01", "Midland Hub 02", "Central Operations Hub"],
        "bottleneck": "Entitlement audit and clinical verification",
    },
    "PORT_LOGISTICS": {
        "name": "Port logistics / container flow",
        "exposure": 64.0,
        "drift": 8.2,
        "burn": 410000,
        "nodes": ["Container Terminal 01", "Freight Rail Hub North", "Gate Complex 4"],
        "bottleneck": "Manifest audit and intermodal handoff",
    },
}

ARTIFACTS = [
    ("ICCP 4-sec", "Inter-Control Centre Protocol", "Telemetry heartbeat: 04.0 sec | checksum: 9F-A2 | state: nominal"),
    ("ASTM D877", "Dielectric breakdown test", "Oil sample: TX-204 | 11.8 kV | 5-run mean: 48.2 kV | pass"),
    ("ACC45", "Asset condition certificate", "Asset: STK-04 | inspection window: 2026-08-25 | sign-off: pending"),
    ("BAPLIE", "Bay plan / loading exchange", "Voyage: NZ-118 | berth: P4 | reefer plugs: 38/40 | reconciled"),
]


def money(value):
    return f"${value:,.0f}"


def append_audit(event, authority, node, total_recovered):
    previous = st.session_state.get("audit_head", "GENESIS")
    client_retained = total_recovered * 0.90
    phoenix_fee = total_recovered * 0.10
    payload = f"{previous}|{event}|{authority}|{node}|{total_recovered:.2f}"
    proof = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    st.session_state.audit_head = proof
    st.session_state.setdefault("audit_ledger", []).insert(0, {
        "Timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "Node": node,
        "Authority": authority,
        "Total Recovered": money(total_recovered),
        "Client Retained (90%)": money(client_retained),
        "Phoenix Fee (10%)": money(phoenix_fee),
    })


st.sidebar.markdown("## FACTORY COMMAND POST")
st.sidebar.caption("Live operating book | control plane online")


book_options = list(BOOKS)
if st.session_state.get("active_book") not in book_options:
    st.session_state["active_book"] = book_options[0]


def switch_book():
    st.rerun()


st.sidebar.selectbox(
    "Operating book",
    book_options,
    format_func=lambda key: BOOKS[key]["name"],
    key="active_book",
    on_change=switch_book,
)
book_key = st.session_state["active_book"]
book = BOOKS[book_key]

st.sidebar.markdown("### Authority routing")
tier = st.sidebar.radio(
    "Command view",
    ["Tier 1 | Chairman Directorate", "Tier 2 | General Management", "Tier 3 | Site Operations"],
)
chairman_override = st.sidebar.toggle("Chairman Directorate Override", value=False)
domains = {
    "Operations": st.sidebar.checkbox("Operations domain", value=True, disabled=chairman_override),
    "Capital": st.sidebar.checkbox("Capital domain", value=True, disabled=chairman_override),
    "Compliance": st.sidebar.checkbox("Compliance domain", value=True, disabled=chairman_override),
    "Systems": st.sidebar.checkbox("Systems domain", value=True, disabled=chairman_override),
}
if chairman_override:
    domains = {domain: True for domain in domains}

st.sidebar.markdown("### Stress controls")
stress_locked = not chairman_override
if stress_locked:
    st.sidebar.caption("LOCKED: Chairman Directorate Override required")
stress_lag = st.sidebar.slider("Queue lag surge (weeks)", 0, 8, 0, disabled=stress_locked)
surge_budget = st.sidebar.slider("Surge budget (%)", 0, 40, 10, 5, disabled=stress_locked)

is_chairman_view = tier.startswith("Tier 1")
multiplier = 1 + stress_lag * 0.12
weekly_burn = book["burn"] * multiplier
sla_days = max(1, 7 - stress_lag)

st.markdown(
    f"<div class='mast'><div class='eyebrow'>AAT / command register / {book_key}</div>"
    f"<h1>{book['name']}</h1><div class='status'>AUTHORITY: <span>{'CHAIRMAN OVERRIDE' if chairman_override else tier.split('|')[1].strip().upper()}</span> &nbsp;|&nbsp; TELEMETRY: LIVE &nbsp;|&nbsp; SLA CLOCK: {sla_days} DAYS</div></div>",
    unsafe_allow_html=True,
)

if is_chairman_view:
    st.markdown("<div class='eyebrow'>Tier 1 / apex decision surface</div>", unsafe_allow_html=True)
    st.header("Chairman Directorate Override")
    if chairman_override:
        st.success("Override active. All directorates are translated into one accountable command chain.")
    else:
        st.warning("Chairman gate is closed. Activate the override in the sidebar to authorize macro stress and audit-ledger visibility.")
    metric_cols = st.columns(4)
    metric_cols[0].metric("Enterprise exposure", f"${book['exposure'] * multiplier:.1f}M")
    metric_cols[1].metric("Velocity drift", f"${book['drift'] * multiplier:.1f}M")
    metric_cols[2].metric("Weekly holding burn", money(weekly_burn))
    metric_cols[3].metric("Active domains", f"{sum(domains.values())}/4")
    idle_labour = weekly_burn * 0.55
    wacc_carry = weekly_burn * 0.25
    statutory_penalties = weekly_burn * 0.20
    total_holding_loss = idle_labour + wacc_carry + statutory_penalties
    client_realization = total_holding_loss * 0.90
    phoenix_realization_fee = total_holding_loss * 0.10
    realization_ledger = [
        {"Component": "Idle Labour", "Amount": money(idle_labour)},
        {"Component": "WACC Carry", "Amount": money(wacc_carry)},
        {"Component": "Statutory Penalties", "Amount": money(statutory_penalties)},
        {"Component": "Total Holding Loss", "Amount": money(total_holding_loss)},
        {"Component": "Client Realization (90%)", "Amount": money(client_realization)},
        {"Component": "Phoenix Realization Fee (10%)", "Amount": money(phoenix_realization_fee)},
    ]
    st.subheader("Deconstructed Holding Loss & Realization Ledger")
    st.dataframe(realization_ledger, use_container_width=True, hide_index=True)
    st.markdown(f"<div class='callout'><b>Chairman decision brief:</b> {book['bottleneck']}. A {stress_lag}-week lag creates {money(weekly_burn * max(stress_lag, 1))} of controllable holding burn. Release the Tier 2 surge plan and keep the Tier 3 evidence chain attached.</div>", unsafe_allow_html=True)
    st.subheader("Chairman-gated audit ledger")
    if chairman_override:
        if st.button("Record Chairman directive", type="primary"):
            append_audit(
                "Directorate override reviewed",
                "Chairman",
                book["nodes"][0],
                total_holding_loss,
            )
            st.toast("Directive appended to the chained ledger")
        st.dataframe(st.session_state.get("audit_ledger", []), use_container_width=True, hide_index=True)
    else:
        st.markdown("<p class='lock'>LOCKED / NO LEDGER DISCLOSURE WITHOUT CHAIRMAN AUTHORITY</p>", unsafe_allow_html=True)

elif tier.startswith("Tier 2"):
    st.markdown("<div class='eyebrow'>Tier 2 / translation and allocation</div>", unsafe_allow_html=True)
    st.header("General Management Directive & Domain Translation Console")
    st.info("Convert the Chairman outcome into accountable domain instructions, surge budgets, and time-bound service levels.")
    directive = st.text_area(
        "Management directive",
        value=f"Stabilise {book['bottleneck']} and restore the {sla_days}-day release SLA.",
        height=90,
        key=f"directive_{book_key}",
    )
    domain_cols = st.columns(4)
    domain_rows = []
    for index, domain in enumerate(domains):
        with domain_cols[index]:
            allocation = st.number_input(
                f"{domain} surge budget (%)",
                0,
                40,
                10 if domains[domain] else 0,
                5,
                key=f"budget_{book_key}_{domain}",
            )
            service_level = st.selectbox(
                f"{domain} SLA",
                ["4 hours", "1 business day", "3 business days", "7 days"],
                index=1,
                key=f"sla_{book_key}_{domain}",
            )
            domain_rows.append({"Book": book_key, "Domain": domain, "State": "ACTIVE" if domains[domain] else "PAUSED", "Surge": f"{allocation}%", "SLA": service_level})
    st.subheader("Directive translation register")
    st.dataframe(domain_rows, use_container_width=True, hide_index=True)
    if st.button("Issue translated directive", type="primary"):
        st.session_state.setdefault("active_directives", {})[book_key] = {
            "issued_by": "General Management",
            "domains": {
                row["Domain"]: {
                    "state": row["State"],
                    "surge": row["Surge"],
                    "sla": row["SLA"],
                }
                for row in domain_rows
            },
        }
        append_audit(
            "General management directive issued",
            "General Management",
            book["nodes"][0],
            total_recovered=weekly_burn,
        )
        st.success("Directive issued to active domains. Site operators now receive the latest SLA clock.")

else:
    st.markdown("<div class='eyebrow'>Tier 3 / evidence-led execution</div>", unsafe_allow_html=True)
    st.header("Site Operations Hub")
    st.caption(f"Operating nodes: {' | '.join(book['nodes'])}  |  Live bottleneck: {book['bottleneck']}")
    issued_directive = st.session_state.get("active_directives", {}).get(book_key)
    st.subheader("Upstream Governance")
    if issued_directive:
        governance_badges = []
        for domain, directive in issued_directive["domains"].items():
            if directive["state"] == "PAUSED":
                governance_badges.append(
                    f"<span class='governance-badge paused'><strong>{domain}</strong> 🔴 PAUSED | Surge {directive['surge']} | SLA {directive['sla']}</span>"
                )
            else:
                governance_badges.append(
                    f"<span class='governance-badge'><strong>{domain}</strong> | ACTIVE | Surge {directive['surge']} | SLA {directive['sla']}</span>"
                )
        st.markdown("".join(governance_badges), unsafe_allow_html=True)
    else:
        st.warning("No Tier 2 directive has been issued for this operating book.")
    required_domains = list(domains)
    required_domains_active = bool(issued_directive) and all(
        issued_directive["domains"].get(domain, {}).get("state") == "ACTIVE"
        for domain in required_domains
    )
    st.subheader("Authentic control artifacts")
    artifact_cols = st.columns(4)
    for index, (code, title, detail) in enumerate(ARTIFACTS):
        with artifact_cols[index]:
            st.markdown(f"<div class='artifact'><strong>{code}</strong><br><b>{title}</b><br><small>{detail}</small></div>", unsafe_allow_html=True)
    st.subheader("SOP release checklist")
    checks = [
        "ICCP heartbeat verified against edge timestamp",
        "ASTM D877 sample and instrument serial attached",
        "ACC45 condition certificate countersigned",
        "BAPLIE plan reconciled with berth and reefer manifest",
        "Exception owner and next review time assigned",
    ]
    completed = sum(st.checkbox(item, key=f"sop_{book_key}_{index}") for index, item in enumerate(checks))
    st.progress(completed / len(checks), text=f"SOP evidence complete: {completed}/{len(checks)}")
    if not required_domains_active:
        st.error("Full field SOP execution is locked until every required domain is ACTIVE in Tier 2.")
    st.subheader("Locked stress envelope")
    st.caption("Stress sliders are visible for situational awareness but require Chairman Directorate Override to move.")
    st.slider("Queue lag surge (weeks)", 0, 8, stress_lag, disabled=True, key="site_lag")
    st.slider("Surge budget (%)", 0, 40, surge_budget, 5, disabled=True, key="site_budget")
    if st.button("Submit site evidence", type="primary", disabled=not required_domains_active):
        append_audit(
            "Site evidence submitted",
            "Site Operations",
            book["nodes"][0],
            total_recovered=weekly_burn,
        )
        st.success("Evidence package queued for General Management review.")

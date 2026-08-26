from pathlib import Path

"""Standalone executive governance console for the simulation factory."""

from datetime import datetime, timezone
from html import escape

import streamlit as st


st.set_page_config(
	page_title="Kinetic Governance Console",
	page_icon="K",
	layout="wide",
	initial_sidebar_state="expanded",
)


def money(value):
	return f"${value:,.0f}"


def now_label():
	return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def record_event(event, detail, actor="Frontline Operations"):
	st.session_state.audit_events.insert(
		0,
		{"time": now_label(), "event": event, "detail": detail, "actor": actor},
	)


def initialize_state():
	defaults = {
		"chairman_override": False,
		"committee_investment": True,
		"committee_risk": True,
		"committee_remuneration": False,
		"committee_sustainability": True,
		"active_burn": 610000,
		"sop_submitted": False,
		"audit_events": [
			{
				"time": "2026-08-26 09:12 UTC",
				"event": "CHAIN INITIALIZED",
				"detail": "Exposure ledger sealed at $88.5M; holding burn opened at $610k.",
				"actor": "System Attestation",
			},
			{
				"time": "2026-08-26 09:15 UTC",
				"event": "UPSTREAM VERIFIED",
				"detail": "ERCOT dispatch evidence linked through ICCP and PSCAD artifacts.",
				"actor": "Grid Controls",
			},
		],
	}
	for key, value in defaults.items():
		st.session_state.setdefault(key, value)


initialize_state()

st.markdown(
	"""
	<style>
	@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Space+Grotesk:wght@400;500;600;700&display=swap');
	:root { --ink:#15222a; --muted:#65757a; --line:#d8e1dd; --paper:#f4f7f2; --teal:#0b6e69; --lime:#d4ee9a; --amber:#f5bc53; --red:#c44b3c; }
	.stApp { background: var(--paper); color:var(--ink); }
	[data-testid="stSidebar"] { background:#17383a; border-right:0; }
	[data-testid="stSidebar"] * { color:#edf6e7 !important; }
	h1,h2,h3,h4,p,span,label,div { font-family:'Space Grotesk', sans-serif; }
	h1 { letter-spacing:0; font-size:2.35rem; color:var(--ink); }
	h2 { margin-top:1.5rem; color:var(--ink); }
	.mono { font-family:'DM Mono', monospace; letter-spacing:0; }
	.eyebrow { color:var(--teal); font-family:'DM Mono',monospace; font-size:.72rem; font-weight:500; letter-spacing:.08em; text-transform:uppercase; }
	.subhead { color:var(--muted); margin-top:-.8rem; }
	.metric-card { background:#fff; border:1px solid var(--line); border-radius:6px; padding:1rem 1.1rem; min-height:125px; }
	.metric-value { font-size:1.85rem; font-weight:700; line-height:1.15; margin:.45rem 0; }
	.metric-label { color:var(--muted); font-size:.82rem; }
	.metric-note { color:var(--teal); font-size:.75rem; }
	.section-rule { border-top:1px solid var(--line); margin:1.6rem 0 1rem; }
	.badge { display:inline-block; padding:.3rem .55rem; margin:.15rem .25rem .15rem 0; border-radius:3px; background:#dff0bf; color:#31551c; font:500 .72rem 'DM Mono',monospace; }
	.badge.teal { background:#d8efeb; color:#0b5d59; }
	.badge.amber { background:#fff0cf; color:#875a13; }
	.artifact { border-left:3px solid var(--teal); background:#fff; padding:.75rem .9rem; margin:.5rem 0; }
	.artifact strong { display:block; font-size:.9rem; }
	.artifact small { color:var(--muted); font-family:'DM Mono',monospace; }
	.audit-row { border-bottom:1px solid var(--line); padding:.7rem 0; }
	.audit-time { color:var(--teal); font:500 .7rem 'DM Mono',monospace; }
	.audit-event { font-weight:700; font-size:.82rem; }
	.audit-detail { color:var(--muted); font-size:.78rem; }
	.stButton button { border-radius:4px; font-family:'Space Grotesk',sans-serif; font-weight:600; }
	.stTabs [data-baseweb="tab-list"] { gap:1.4rem; border-bottom:1px solid var(--line); }
	.stTabs [data-baseweb="tab"] { font-weight:600; }
	</style>
	""",
	unsafe_allow_html=True,
)

with st.sidebar:
	st.markdown('<div class="eyebrow">Kinetic Asset Management</div>', unsafe_allow_html=True)
	st.title("Governance\nConsole")
	st.caption("CONTROL PLANE / 26.08")
	st.divider()
	st.markdown("**Active command**")
	st.info("ERCOT reliability recovery")
	st.markdown("**Operator**")
	st.markdown('<span class="mono">M. SERRANO / L2</span>', unsafe_allow_html=True)
	st.divider()
	st.markdown("**Chain status**")
	st.success("ATTESTED / LIVE")

st.markdown('<div class="eyebrow">Board pack 07 / executive operating layer</div>', unsafe_allow_html=True)
st.title("Decision velocity, with a paper trail.")
st.markdown('<p class="subhead">A single control surface for capital exposure, frontline execution, and accountable override.</p>', unsafe_allow_html=True)

top_one, top_two, top_three, top_four = st.columns(4)
for column, label, value, note in [
	(top_one, "Total exposure", "$88.5M", "within board ceiling"),
	(top_two, "Holding burn", money(st.session_state.active_burn), "active operating reserve"),
	(top_three, "Realization split", "90 / 10", "client / Phoenix fee"),
	(top_four, "SOP readiness", "8 / 8", "awaiting sign-off" if not st.session_state.sop_submitted else "frontline cleared"),
]:
	with column:
		st.markdown(
			f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value">{value}</div><div class="metric-note">{note}</div></div>',
			unsafe_allow_html=True,
		)

governance, telemetry, management, operations, audit = st.tabs(
	["Apex Board Governance", "Executive Telemetry", "General Management Console", "Site Operations Hub", "Forensic Audit Ledger"]
)

with governance:
	st.markdown('<div class="eyebrow">01 / apex board governance</div>', unsafe_allow_html=True)
	st.header("Authorization perimeter")
	st.caption("Every elevated action requires a visible board posture and committee quorum.")
	left, right = st.columns([1, 1.4])
	with left:
		override = st.toggle("Chairman Override", key="chairman_override")
		if override:
			st.warning("Override armed. All downstream actions will carry chairman attestation.")
		else:
			st.success("Standard delegated authority")
	with right:
		st.markdown("**Board sub-committee authorizations**")
		committees = [
			("committee_investment", "Investment Committee", "Capital deployment and exposure"),
			("committee_risk", "Risk & Audit Committee", "Controls, evidence, and exceptions"),
			("committee_remuneration", "Remuneration Committee", "People and incentive impacts"),
			("committee_sustainability", "Sustainability Committee", "Grid resilience and impact"),
		]
		for key, label, description in committees:
			st.toggle(label, key=key, help=description)
	st.markdown('<div class="section-rule"></div>', unsafe_allow_html=True)
	authorized = sum(st.session_state[key] for key, _, _ in committees)
	st.markdown(f'<span class="badge teal">{authorized}/4 COMMITTEES AUTHORIZED</span>', unsafe_allow_html=True)
	st.markdown('<span class="badge">ATTESTATION REQUIRED</span>', unsafe_allow_html=True)

with telemetry:
	st.markdown('<div class="eyebrow">02 / executive telemetry</div>', unsafe_allow_html=True)
	st.header("Exposure and realization")
	st.caption("Current position translated into an auditable client-versus-fee realization view.")
	t1, t2 = st.columns([1, 1.6])
	with t1:
		st.markdown('<div class="metric-card"><div class="metric-label">Gross exposure</div><div class="metric-value">$88.5M</div><div class="metric-note">12 assets / 4 sectors / ERCOT weighted</div></div>', unsafe_allow_html=True)
		st.markdown('<div class="metric-card" style="margin-top:1rem"><div class="metric-label">Holding burn</div><div class="metric-value">' + money(st.session_state.active_burn) + '</div><div class="metric-note">resets on frontline clearance</div></div>', unsafe_allow_html=True)
	with t2:
		st.markdown("**90 / 10 Deconstructed Realization Table**")
		st.dataframe(
			[
				{"Realization leg": "Client realization", "Share": "90%", "Amount": "$549,000", "Status": "Protected"},
				{"Realization leg": "Phoenix fee", "Share": "10%", "Amount": "$61,000", "Status": "Accrued"},
				{"Realization leg": "Total decomposed value", "Share": "100%", "Amount": "$610,000", "Status": "Reconciled"},
			],
			use_container_width=True,
			hide_index=True,
		)
		st.progress(0.9, text="Client value capture / 90%")

with management:
	st.markdown('<div class="eyebrow">03 / general management console</div>', unsafe_allow_html=True)
	st.header("Directive translation register")
	st.caption("Translate board language into bounded operating instructions with an explicit SLA.")
	budgets = st.columns(3)
	for column, label, key, value in zip(
		budgets,
		["Grid stabilization surge", "Claims response surge", "Evidence preservation surge"],
		["grid_budget", "claims_budget", "evidence_budget"],
		[18, 12, 8],
	):
		with column:
			st.number_input(label, min_value=0, max_value=100, value=value, step=1, format="%d", key=key)
	st.markdown('<div class="section-rule"></div>', unsafe_allow_html=True)
	st.markdown("**SLA routing")
	r1, r2, r3 = st.columns(3)
	with r1:
		st.selectbox("Critical incident", ["15 minutes", "30 minutes", "1 hour"], key="critical_sla")
	with r2:
		st.selectbox("Material exception", ["4 hours", "Same business day", "48 hours"], key="material_sla")
	with r3:
		st.selectbox("Routine evidence request", ["1 business day", "3 business days", "5 business days"], key="routine_sla")
	st.markdown("**Directive register**")
	st.dataframe(
		[
			{"Board directive": "Protect reliability while releasing liquidity", "Translated action": "Prioritize ERCOT recovery queue; cap surge at 18%", "Owner": "Asset Control", "SLA": st.session_state.critical_sla},
			{"Board directive": "No undocumented exception", "Translated action": "Attach source artifact before every status transition", "Owner": "Risk & Audit", "SLA": st.session_state.material_sla},
			{"Board directive": "Clear the frontline queue", "Translated action": "Complete 8/8 SOP and submit attestation", "Owner": "Site Operations", "SLA": st.session_state.routine_sla},
		],
		use_container_width=True,
		hide_index=True,
	)

with operations:
	st.markdown('<div class="eyebrow">04 / site operations hub</div>', unsafe_allow_html=True)
	st.header("Frontline command center")
	sector = st.selectbox("Operating sector", ["ERCOT", "PJM", "CAISO"], key="sector")
	artifact_map = {
		"ERCOT": [("ICCP", "Inter-Control Center Communications Protocol", "dispatch link / live"), ("PSCAD", "Power Systems Computer Aided Design", "transient model / sealed")],
		"PJM": [("ICCP", "Inter-Control Center Communications Protocol", "dispatch link / live"), ("PSS/E", "Power System Simulator for Engineering", "stability model / sealed")],
		"CAISO": [("ICCP", "Inter-Control Center Communications Protocol", "dispatch link / live"), ("WECC", "Western Electricity Coordinating Council model", "regional model / sealed")],
	}
	badges = "".join(f'<span class="badge teal">UPSTREAM {escape(label)} / VERIFIED</span>' for label, _, _ in artifact_map[sector])
	st.markdown(f"**Dynamic Upstream Governance**  {badges}", unsafe_allow_html=True)
	st.markdown("**Sector-pure authentic artifacts**")
	artifact_cols = st.columns(len(artifact_map[sector]))
	for column, (name, detail, status) in zip(artifact_cols, artifact_map[sector]):
		with column:
			st.markdown(f'<div class="artifact"><strong>{escape(name)}</strong><small>{escape(detail)}<br>{escape(status)}</small></div>', unsafe_allow_html=True)
	st.markdown("**8 / 8 SOP checklist**")
	checklist = ["Isolation boundaries confirmed", "Control-room handoff logged", "Dispatch instruction acknowledged", "Protection settings cross-checked", "Communications path tested", "Contingency route rehearsed", "Evidence artifacts attached", "Supervisor review completed"]
	checklist_cols = st.columns(2)
	for index, item in enumerate(checklist):
		with checklist_cols[index % 2]:
			st.checkbox(item, value=True, disabled=True, key=f"sop_{index}")
	if st.session_state.sop_submitted:
		st.success("Frontline SOP signed off. Active burn has been cleared to $0.")
	elif st.button("Submit Frontline SOP Sign-off", type="primary", use_container_width=True):
		st.session_state.sop_submitted = True
		st.session_state.active_burn = 0
		record_event("FRONTLINE CLEARED", "8/8 SOP sign-off accepted; active burn reset from $610,000 to $0.")
		st.rerun()

with audit:
	st.markdown('<div class="eyebrow">05 / forensic audit ledger</div>', unsafe_allow_html=True)
	st.header("Cryptographic chain of custody")
	st.caption("Immutable-style event presentation for operator review and post-clearance reconciliation.")
	a1, a2, a3 = st.columns(3)
	with a1:
		st.metric("Chain state", "SEALED")
	with a2:
		st.metric("Active burn", money(st.session_state.active_burn))
	with a3:
		st.metric("Events", len(st.session_state.audit_events))
	st.markdown('<div class="section-rule"></div>', unsafe_allow_html=True)
	for event in st.session_state.audit_events:
		st.markdown(
			f'<div class="audit-row"><div class="audit-time">{escape(event["time"])} / {escape(event["actor"])}</div><div class="audit-event">{escape(event["event"])}</div><div class="audit-detail">{escape(event["detail"])}</div></div>',
			unsafe_allow_html=True,
		)

st.markdown('<div class="section-rule"></div>', unsafe_allow_html=True)
st.caption(f"Last console render: {now_label()} | Evidence policy: source-bound, operator-attested, board-visible")

import datetime

import streamlit as st

import ledger_store


TOTAL_ASSET_EXPOSURE = 88_500_000
BOARD_EXPOSURE_LIMIT = 95_000_000
WEEKLY_HOLDING_BURN = 610_000
CLIENT_REALIZATION_TARGET = 549_000
PHOENIX_ADVISORY_FEE = 61_000
CARRY_BURN_PER_SEC = 1.01

GM_DOMAINS = {
    "Marcus Vance": {
        "domain": "Grid Interconnection & Telemetry",
        "short_label": "Grid & Telemetry | SLA 45m",
        "sla_seconds": 45 * 60,
        "sla_label": "45 min",
        "stance": (
            "Holding telemetry attestation open. ICCP scan is drifting against the 4-second ERCOT "
            "polling requirement and will not certify a point-map he cannot reproduce twice."
        ),
        "contract_risk": (
            "Telemetry non-conformance under ERCOT Nodal Protocol § 6.5.5.2 exposes the asset to "
            "resource-status suspension and forfeiture of dispatch revenue."
        ),
        "escalation": "Escalate to Grid Risk & Technical Integrity Committee for a 4-hour re-scan window.",
        "suggested_query": "Can we proceed if ICCP telemetry has 4-second drift?",
        "synthesis": (
            "4-second ICCP drift sits at the outer edge of ERCOT tolerance, not outside it. Proceeding is "
            "defensible with a logged re-scan commitment; the telemetry defect is administrative, not "
            "electrical, and does not justify continued standby carry."
        ),
    },
    "Elena Rostova": {
        "domain": "Field Substation & High-Voltage",
        "short_label": "Field Substation | SLA 3.0h",
        "sla_seconds": 3 * 3600,
        "sla_label": "3.0 hrs",
        "stance": (
            "Withholding signature. Refuses to energize without EPC warranty indemnity waiver."
        ),
        "contract_risk": (
            "Energization prior to IEEE 2800 packet closure voids the OEM high-voltage transformer "
            "warranty — $1.2M unhedged equipment exposure carried at the operating company."
        ),
        "escalation": "Issue Directorate Indemnity Carve-Out and fund $1.2M Asset Defense Escrow.",
        "suggested_query": "What happens if we grant Elena an emergency warranty indemnification?",
        "synthesis": (
            "An emergency indemnification transfers $1.2M of warranty exposure to the directorate reserve "
            "and clears the energization hold immediately. Idle carry overtakes the equipment risk in "
            "roughly 13.8 days, so the carve-out is net capital-accretive today."
        ),
    },
    "David Chen": {
        "domain": "Regulatory & Market Operations",
        "short_label": "Regulatory Operations | SLA 90m",
        "sla_seconds": 90 * 60,
        "sla_label": "90 min",
        "stance": (
            "Demanding immediate Part 2 COD attestation filing. Queue position drops within 48 hours "
            "and he will not absorb the restudy liability created by frontline delay."
        ),
        "contract_risk": (
            "Missing the ERCOT IA § 4.2 filing window triggers queue cancellation, a $4.5M restudy "
            "forfeiture, and a 14-month COD slip."
        ),
        "escalation": "Authorize provisional filing under statutory safe harbor with counsel attestation.",
        "suggested_query": "What is the penalty under ERCOT IA § 4.2 if we force provisional filing?",
        "synthesis": (
            "Provisional filing under § 4.2 carries a curable deficiency notice and potential administrative "
            "penalty, materially cheaper than queue cancellation. Filing now preserves the interconnect "
            "window and halts the standby clock."
        ),
    },
}

SOP_CHECKS = [
    {"key": "check_1", "name": "ICCP 4-Sec Telemetry Handshake", "owner": "Marcus Vance", "default": True},
    {"key": "check_2", "name": "PSCAD EMT Model Validation", "owner": "Marcus Vance", "default": True},
    {"key": "check_3", "name": "RTU Point-Map Certification", "owner": "Marcus Vance", "default": True},
    {"key": "check_4", "name": "IEEE 2800 Ride-Through Test Packet", "owner": "Elena Rostova", "default": True},
    {"key": "check_5", "name": "HV Transformer Relay Coordination Study", "owner": "Elena Rostova", "default": True},
    {"key": "check_6", "name": "Substation Grounding & Safety Clearance", "owner": "Elena Rostova", "default": False},
    {"key": "check_7", "name": "ERCOT Part 2 COD Attestation Filing", "owner": "David Chen", "default": False},
    {"key": "check_8", "name": "NERC Registration & Settlement Enablement", "owner": "David Chen", "default": False},
]


INCIDENTS = {
    "INC-001": {
        "title": "ERCOT IA Section 4.2 Part 2 COD Attestation",
        "priority": "P1 - CRITICAL",
        "burn_rate_sec": 1.01,
        "start_time": datetime.datetime.now() - datetime.timedelta(days=1),
        "schedule_drift": "+9 Days COD Drift",
        "status": "DEADLOCKED",
        "cognizant_director": {
            "name": "Dr. Arthur Pendleton",
            "role": "Chair, Grid Risk & Technical Integrity",
            "status": "Concurrence Pending",
        },
        "gms": {
            "Elena Rostova": {
                "role": "GM - Field Operations & Contractor Mobilization",
                "domain": "High-Voltage Crews & Permian Substation",
                "stance": "Withholding signature: Energization without IEEE 2800 test packet invalidates OEM high-voltage transformer warranty ($1.2M exposure).",
                "checks": [
                    {"id": "Check #1", "name": "ICCP 4-sec Telemetry", "status": "CLEARED", "evidence": "Locked to Ledger"},
                    {"id": "Check #3", "name": "PSCAD EMT Model", "status": "CLEARED", "evidence": "Evidence Verified"},
                    {"id": "Check #5", "name": "IEEE 2800 Test Packet", "status": "CLEARED", "evidence": "Packet Transmitted"},
                ],
            },
            "David Chen": {
                "role": "GM - Regulatory & Market Operations",
                "domain": "ERCOT Protocol & Queue Adjudication",
                "stance": "Demanding immediate Part 2 COD Attestation filing: ERCOT interconnection queue position drops in 48 hours without filing.",
                "checks": [
                    {"id": "Check #2", "name": "ICCP Telemetry Record", "status": "CLEARED", "evidence": "Record Attached"},
                    {"id": "Check #4", "name": "PSCAD EMT Model Record", "status": "CLEARED", "evidence": "Record Attached"},
                    {"id": "Check #6", "name": "Part 2 COD Attestation", "status": "BLOCKED", "evidence": "Awaiting Frontline Sign-Off"},
                ],
            },
        },
        "audit_log": [
            "[T-24h] Deadlock flagged: Elena Rostova withheld sign-off on Part 2 COD Attestation.",
            "[T-18h] Contractor idle carry clock activated at $1.01/sec.",
        ],
    },
    "INC-002": {
        "title": "Substation Main Step-Up Inrush Trip",
        "priority": "P2 - HIGH",
        "burn_rate_sec": 0.46,
        "start_time": datetime.datetime.now() - datetime.timedelta(hours=14),
        "schedule_drift": "+4 Days Commissioning",
        "status": "ACTIVE",
        "cognizant_director": {"name": "Sarah Jenkins", "role": "Chair, Operations & Asset Safety", "status": "Reviewing Relay Logs"},
        "gms": {},
        "audit_log": [],
    },
    "INC-003": {
        "title": "SCADA Protocol IEC 61850 Mapping Mismatch",
        "priority": "P3 - MODERATE",
        "burn_rate_sec": 0.25,
        "start_time": datetime.datetime.now() - datetime.timedelta(hours=8),
        "schedule_drift": "+2 Days Witness Test",
        "status": "ACTIVE",
        "cognizant_director": {"name": "Arthur Pendleton", "role": "Chair, Grid Risk", "status": "Nominal"},
        "gms": {},
        "audit_log": [],
    },
    "INC-004": {
        "title": "BESS Inverter Firmware Security Patch Rollback",
        "priority": "P4 - MONITORED",
        "burn_rate_sec": 0.07,
        "start_time": datetime.datetime.now() - datetime.timedelta(hours=4),
        "schedule_drift": "+0 Days (Float Available)",
        "status": "ACTIVE",
        "cognizant_director": {"name": "Marcus Vance", "role": "Executive Sponsor", "status": "Nominal"},
        "gms": {},
        "audit_log": [],
    },
}


if "incident_store" not in st.session_state:
    st.session_state.incident_store = INCIDENTS
if "active_incident_id" not in st.session_state:
    st.session_state.active_incident_id = "INC-001"
if "selected_gm_branch" not in st.session_state:
    st.session_state.selected_gm_branch = "Elena Rostova"
if "selected_book" not in st.session_state:
    st.session_state["selected_book"] = "ERCOT_INTERCONNECT"
if "checklist_db" not in st.session_state:
    st.session_state["checklist_db"] = {}
if "standby_frozen" not in st.session_state:
    st.session_state["standby_frozen"] = {}
if "ledger_ready" not in st.session_state:
    try:
        ledger_store.init_db()
        st.session_state["ledger_ready"] = True
    except Exception:  # ledger persistence is best-effort; UI must stay live
        st.session_state["ledger_ready"] = False


def ensure_checklist(book: str) -> dict:
    """Idempotent per-book SOP state so checks survive view navigation."""
    checklist_db = st.session_state["checklist_db"]
    book_state = checklist_db.setdefault(book, {})
    for check in SOP_CHECKS:
        book_state.setdefault(check["key"], check["default"])
    return book_state


def readiness_count(book: str) -> int:
    book_state = ensure_checklist(book)
    return sum(1 for check in SOP_CHECKS if book_state.get(check["key"]))


def gm_open_checks(book: str, gm_name: str) -> list:
    book_state = ensure_checklist(book)
    return [check for check in SOP_CHECKS if check["owner"] == gm_name and not book_state.get(check["key"])]


def gm_checks(gm_name: str) -> list:
    return [check for check in SOP_CHECKS if check["owner"] == gm_name]


def identify_bottleneck(book: str, elapsed_seconds: float):
    """Pacing GM = worst SLA overrun with open checks; falls back to first GM still holding checks."""
    candidates = [
        (name, meta, gm_open_checks(book, name), elapsed_seconds - meta["sla_seconds"])
        for name, meta in GM_DOMAINS.items()
        if gm_open_checks(book, name)
    ]
    if not candidates:
        return None
    return max(candidates, key=lambda item: item[3])


def fetch_gm_ledger_events(book: str, gm_name: str, limit: int = 3) -> list:
    if not st.session_state.get("ledger_ready"):
        return []
    try:
        with ledger_store.get_db() as conn:
            rows = conn.execute(
                """
                SELECT actor_id, official_title, action_type, t1_resolution, hesitation_cost,
                       blocker_notes, sha256_hash
                FROM forensic_ledger
                WHERE operating_book = ?
                  AND (actor_id LIKE ? OR official_title LIKE ? OR blocker_notes LIKE ?
                       OR actor_id = 'CHAIRMAN')
                ORDER BY entry_id DESC
                LIMIT ?
                """,
                (book, f"%{gm_name}%", f"%{gm_name}%", f"%{gm_name}%", limit),
            ).fetchall()
        return [dict(row) for row in rows]
    except Exception:
        return []


def write_ledger_event(book: str, action: str, rationale: str, work_order_id: str, t0) -> str:
    if not st.session_state.get("ledger_ready"):
        return "LEDGER OFFLINE - EVENT HELD IN SESSION CHAIN"
    try:
        ledger_store.record_ledger_entry(
            book=book,
            tier=1,
            actor_id="CHAIRMAN",
            title="Chairman of the Board",
            action=action,
            work_order_id=work_order_id,
            t0=t0,
            blocker="GOVERNANCE_DEADLOCK",
            notes=rationale,
        )
        return "COMMITTED TO SQLITE FORENSIC LEDGER (SHA-256 CHAINED)"
    except Exception as exc:
        return f"LEDGER WRITE FAILED: {exc}"


def _kpi_card(label: str, value: str, basis: str, accent: str) -> str:
    return (
        f"<div style='background:#0B0F19;border:1px solid {accent};border-left:6px solid {accent};"
        "border-radius:8px;padding:14px 16px;height:132px;'>"
        f"<div style='color:#9AA4B2;font-size:0.72rem;letter-spacing:0.09em;text-transform:uppercase;'>{label}</div>"
        f"<div style='color:#FFFFFF;font-size:1.55rem;font-weight:800;margin-top:6px;'>{value}</div>"
        f"<div style='color:{accent};font-size:0.75rem;margin-top:6px;font-weight:600;'>{basis}</div>"
        "</div>"
    )


def render_gm_dossier(
    incident: dict,
    selected_book: str,
    gm_name: str,
    elapsed: float,
    live_carry: float,
    readiness: int,
) -> None:
    """Cross-tier drawer uniting Tier 2 stance, Tier 3 SOP state, and Tier 4 ledger for one GM."""
    gm_meta = GM_DOMAINS[gm_name]
    book_state = ensure_checklist(selected_book)
    open_checks = gm_open_checks(selected_book, gm_name)

    st.markdown(f"### 🔍 Unified Domain Dossier: {gm_name} — {gm_meta['domain']}")
    tier2_col, tier3_col, tier4_col = st.columns(3)

    with tier2_col:
        st.markdown("**TIER 2 · MANAGEMENT STANCE**")
        st.warning(gm_meta["stance"])
        st.markdown(f"**Contractual Risk:** {gm_meta['contract_risk']}")
        st.markdown(f"**Escalation Directive:** {gm_meta['escalation']}")
        st.caption(
            f"SLA {gm_meta['sla_label']} · elapsed {elapsed/3600:,.1f} hrs · "
            f"{len(open_checks)} gate(s) withheld"
        )

    with tier3_col:
        st.markdown("**TIER 3 · SITE SOP VERIFICATION**")
        for check in gm_checks(gm_name):
            widget_key = f"sop_{selected_book}_{check['key']}"
            st.session_state.setdefault(widget_key, bool(book_state.get(check["key"])))
            verified = st.checkbox(
                f"{check['name']}: {'Cleared' if book_state.get(check['key']) else 'PENDING'}",
                key=widget_key,
            )
            if verified != bool(book_state.get(check["key"])):
                st.session_state["checklist_db"][selected_book][check["key"]] = verified
                st.rerun()
        heartbeat = datetime.datetime.utcnow().strftime("%H:%M:%S UTC")
        st.caption(
            f"Telemetry heartbeat {heartbeat} · link {'DEGRADED' if open_checks else 'NOMINAL'} · "
            f"book readiness {readiness}/8"
        )

    with tier4_col:
        st.markdown("**TIER 4 · FORENSIC AUDIT LEDGER**")
        events = fetch_gm_ledger_events(selected_book, gm_name)
        if not events:
            st.info("No chained ledger blocks recorded for this domain yet.")
        for event in events:
            st.markdown(
                f"`{event['action_type']}` · {event['t1_resolution']}\n\n"
                f"**Actor:** {event['actor_id']} ({event['official_title']}) · "
                f"**Hesitation Cost:** ${event['hesitation_cost']:,.2f}"
            )
            st.caption(f"Counsel rationale: {event['blocker_notes'] or 'n/a'}")
            st.code(f"SHA-256: {event['sha256_hash']}", language="text")

    st.markdown("#### Chairman Command Interrogation")
    suggested = gm_meta["suggested_query"]
    if st.button(
        f"Load suggested interrogation: “{suggested}”",
        key=f"suggest_query_{selected_book}_{gm_name}",
        use_container_width=True,
    ):
        st.session_state[f"chairman_query_{selected_book}_{gm_name}"] = suggested
        st.rerun()

    user_query = st.text_input(
        "Ask Command Intelligence about this deadlock, GM stances, or financial exposure...",
        placeholder=suggested,
        key=f"chairman_query_{selected_book}_{gm_name}",
    )
    if user_query:
        with st.chat_message("assistant"):
            st.write(
                f"**Executive Synthesis for Chairman — {gm_name} domain:** Evaluating '{user_query}' against "
                f"live standby carry (${CARRY_BURN_PER_SEC:.2f}/sec, ${live_carry:,.0f} accrued) and "
                f"SOP readiness {readiness}/8."
            )
            st.info(
                f"**Structural Analysis:** {gm_meta['synthesis']}\n\n"
                f"**Burn vs. Legal Exposure:** every additional hour of deadlock costs "
                f"${CARRY_BURN_PER_SEC * 3600:,.0f} in contractor carry "
                f"(${WEEKLY_HOLDING_BURN:,.0f}/wk). Measured against {gm_meta['contract_risk'].rstrip('.')}, "
                f"continued inaction is the more expensive fiduciary path.\n\n"
                f"**Directive:** {gm_meta['escalation']}"
            )


def render_tier_1(incident: dict, selected_book: str) -> None:
    """Chairman Directorate Command Center (fiduciary ribbon, SLA clocks, override console)."""
    book_state = ensure_checklist(selected_book)
    readiness = readiness_count(selected_book)
    frozen = st.session_state["standby_frozen"].get(selected_book, False)

    elapsed = (datetime.datetime.now() - incident["start_time"]).total_seconds()
    live_carry = 0.0 if frozen else elapsed * CARRY_BURN_PER_SEC

    st.subheader("Tier 1 | Chairman Directorate Command Center")

    ribbon = st.columns(5)
    ribbon[0].markdown(
        _kpi_card(
            "Total Asset Exposure",
            f"${TOTAL_ASSET_EXPOSURE/1_000_000:,.1f}M",
            f"Board Limit ${BOARD_EXPOSURE_LIMIT/1_000_000:,.1f}M",
            "#F5A623",
        ),
        unsafe_allow_html=True,
    )
    ribbon[1].markdown(
        _kpi_card(
            "Holding Burn",
            "$0 / wk (FROZEN)" if frozen else f"${WEEKLY_HOLDING_BURN:,.0f} / wk",
            f"Live ticker ${0.00 if frozen else CARRY_BURN_PER_SEC:.2f}/sec · accrued ${live_carry:,.0f}",
            "#00FFA3" if frozen else "#FF4B4B",
        ),
        unsafe_allow_html=True,
    )
    ribbon[2].markdown(
        _kpi_card(
            "Client Realization",
            f"${CLIENT_REALIZATION_TARGET:,.0f}",
            "Target preservation",
            "#4DA3FF",
        ),
        unsafe_allow_html=True,
    )
    ribbon[3].markdown(
        _kpi_card(
            "Phoenix Advisory Fee",
            f"${PHOENIX_ADVISORY_FEE:,.0f}",
            "10% accrual on realization",
            "#B388FF",
        ),
        unsafe_allow_html=True,
    )
    ribbon[4].markdown(
        _kpi_card(
            "SOP Readiness",
            f"{readiness} / 8",
            "GATE CLEARED" if readiness == 8 else f"{8 - readiness} CHECKS UNVERIFIED",
            "#00FFA3" if readiness == 8 else "#FF4B4B",
        ),
        unsafe_allow_html=True,
    )

    bottleneck = identify_bottleneck(selected_book, elapsed)
    if st.session_state.get("inspected_gm") not in GM_DOMAINS:
        st.session_state["inspected_gm"] = bottleneck[0] if bottleneck else "Elena Rostova"

    st.markdown("#### Domain Critical-Path Chronometer (SLA Heat Map)")
    chrono_cols = st.columns(3)
    for column, (gm_name, gm_meta) in zip(chrono_cols, GM_DOMAINS.items()):
        open_checks = gm_open_checks(selected_book, gm_name)
        over_sla = elapsed > gm_meta["sla_seconds"]
        if not open_checks:
            status, accent = "CLEARED", "#00FFA3"
        elif over_sla:
            status, accent = "BREACHED / ACCRUING BURN", "#FF4B4B"
        else:
            status, accent = "ON SCHEDULE", "#F5A623"

        is_inspected = st.session_state["inspected_gm"] == gm_name
        overrun = max(0.0, elapsed - gm_meta["sla_seconds"])
        column.markdown(
            f"<div style='background:#0B0F19;border:{'2px' if is_inspected else '1px'} solid {accent};"
            f"border-radius:8px;padding:14px 16px;"
            f"box-shadow:{'0 0 18px ' + accent + '55' if is_inspected else 'none'};'>"
            f"<div style='color:#FFFFFF;font-size:1.05rem;font-weight:800;'>{gm_name}</div>"
            f"<div style='color:#9AA4B2;font-size:0.8rem;margin-top:2px;'>{gm_meta['short_label']}</div>"
            f"<div style='color:#9AA4B2;font-size:0.78rem;margin-top:8px;'>{gm_meta['domain']} · "
            f"Elapsed: {elapsed/3600:,.1f} hrs</div>"
            f"<div style='color:{accent};font-size:0.95rem;font-weight:800;margin-top:8px;'>{status}</div>"
            f"<div style='color:#9AA4B2;font-size:0.75rem;margin-top:4px;'>Open checks: {len(open_checks)} · "
            f"Overrun: {overrun/3600:,.1f} hrs</div>"
            "</div>",
            unsafe_allow_html=True,
        )
        if column.button(
            "🔎 INSPECTING DOMAIN" if is_inspected else "🔍 INSPECT DOMAIN",
            key=f"inspect_gm_{selected_book}_{gm_name}",
            use_container_width=True,
            type="primary" if is_inspected else "secondary",
        ):
            st.session_state["inspected_gm"] = gm_name
            st.rerun()

    with st.container():
        render_gm_dossier(
            incident,
            selected_book,
            st.session_state["inspected_gm"],
            elapsed,
            live_carry,
            readiness,
        )

    st.markdown("")
    if readiness < 8:
        if bottleneck is None:
            bottleneck_gm, bottleneck_meta, bottleneck_checks = (
                "Unassigned",
                {"domain": "n/a", "sla_label": "n/a"},
                [],
            )
        else:
            bottleneck_gm, bottleneck_meta, bottleneck_checks, _ = bottleneck

        unverified = "".join(
            f"<li style='color:#FFD5D5;'>{check['name']} <span style='color:#9AA4B2;'>"
            f"({check['owner']})</span></li>"
            for check in SOP_CHECKS
            if not book_state.get(check["key"])
        )
        st.markdown(
            "<div style='border:2px solid #FF4B4B;border-radius:10px;padding:20px 22px;"
            "background:rgba(255,75,75,0.07);box-shadow:0 0 22px rgba(255,75,75,0.35);'>"
            "<div style='color:#FF4B4B;font-size:1.25rem;font-weight:900;letter-spacing:0.04em;'>"
            "🚨 CRITICAL PIPELINE STALL: ACTIVE FIDUCIARY EXPOSURE</div>"
            f"<p style='color:#FFFFFF;margin-top:10px;margin-bottom:6px;'><b>Pacing Bottleneck:</b> "
            f"{bottleneck_gm} — {bottleneck_meta['domain']} (SLA {bottleneck_meta['sla_label']}, "
            f"{len(bottleneck_checks)} check(s) unresolved)</p>"
            f"<p style='color:#FFFFFF;margin:0 0 4px 0;'><b>Unverified Check Items ({8 - readiness}):</b></p>"
            f"<ul style='margin-top:0;'>{unverified}</ul>"
            f"<p style='color:#FFFFFF;margin:6px 0;'><b>Accrued Idle Carry:</b> ${live_carry:,.0f} "
            f"(${WEEKLY_HOLDING_BURN:,.0f}/wk contractor standby at ${CARRY_BURN_PER_SEC:.2f}/sec)</p>"
            "<p style='color:#FF9C9C;margin:10px 0 0 0;font-style:italic;'><b>Legal Directive:</b> "
            "Actual knowledge established under DGCL Caremark doctrine. Inaction constitutes documented "
            "governance drift.</p>"
            "</div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            "<div style='border:2px solid #00FFA3;border-radius:10px;padding:20px 22px;"
            "background:rgba(0,255,163,0.07);box-shadow:0 0 22px rgba(0,255,163,0.32);'>"
            "<div style='color:#00FFA3;font-size:1.25rem;font-weight:900;letter-spacing:0.04em;'>"
            "🟢 ACTIVE REMEDIATION CONFIRMED — GATE CLEARED &amp; AUDITED</div>"
            "<p style='color:#FFFFFF;margin-top:10px;'><b>Root-Cause Rectification:</b> All 8 frontline SOP "
            "gates verified across Grid Interconnection & Telemetry, Field Substation & High-Voltage, and "
            "Regulatory & Market Operations. Sequential sign-off deadlock replaced by directorate-attested "
            "parallel clearance.</p>"
            f"<p style='color:#FFFFFF;margin:6px 0;'><b>Capital Preserved:</b> ${WEEKLY_HOLDING_BURN:,.0f}/wk "
            f"standby carry arrested; ${CLIENT_REALIZATION_TARGET:,.0f} client realization target defended; "
            f"${PHOENIX_ADVISORY_FEE:,.0f} Phoenix advisory fee accrual secured.</p>"
            "<p style='color:#FFFFFF;margin:6px 0;'><b>Downstream Commercialization:</b> "
            "(1) Transmit Part 2 COD attestation to ERCOT; (2) enable market settlement &amp; NERC registration; "
            "(3) demobilize standby crews; (4) release audited gate packet to the Board minute book.</p>"
            "</div>",
            unsafe_allow_html=True,
        )

    st.markdown(
        "<div style='border:2px solid #F5A623;border-radius:10px;padding:18px 20px;margin-top:14px;"
        "background:rgba(245,166,35,0.06);'>"
        "<div style='color:#F5A623;font-size:1.2rem;font-weight:900;letter-spacing:0.05em;'>"
        "⚡ CHAIRMAN DIRECTORATE STATUTORY OVERRIDE CONSOLE</div>"
        "<div style='color:#E6C48A;font-size:0.88rem;margin-top:4px;'>"
        "Exercise DGCL § 141 Safe-Harbor Authority &amp; Unilateral Gate Clearance</div>"
        "</div>",
        unsafe_allow_html=True,
    )
    counsel_rationale = st.text_input(
        "Statutory Counsel Justification / Fiduciary Filing Basis",
        value=(
            "Board-authorized unilateral safe-harbor override to arrest $610k/wk contractor carry burn; "
            "executing expedited regulatory attestation."
        ),
        key=f"counsel_rationale_{selected_book}",
    )

    override_col_a, override_col_b = st.columns(2)
    with override_col_a:
        if st.button(
            "🚨 UNILATERAL GATE CLEARANCE (FORCE COD ATTESTATION)",
            key=f"unilateral_gate_clearance_{selected_book}",
            use_container_width=True,
        ):
            for check in SOP_CHECKS:
                st.session_state["checklist_db"][selected_book][check["key"]] = True
                # drop stale checkbox widget state so Tier 3 re-seeds from checklist_db
                st.session_state.pop(f"sop_{selected_book}_{check['key']}", None)
            ledger_status = write_ledger_event(
                book=selected_book,
                action="CHAIRMAN_UNILATERAL_OVERRIDE",
                rationale=counsel_rationale,
                work_order_id=st.session_state.active_incident_id,
                t0=incident["start_time"],
            )
            stamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
            incident["audit_log"].append(
                f"[{stamp}] CHAIRMAN_UNILATERAL_OVERRIDE: All 8 SOP gates force-cleared under DGCL § 141 "
                f"safe harbor. Rationale: {counsel_rationale} | {ledger_status}"
            )
            st.rerun()
    with override_col_b:
        if st.button(
            "🛑 EMERGENCY STANDBY FREEZE (TRIP CIRCUIT BREAKER)",
            key=f"emergency_standby_freeze_{selected_book}",
            use_container_width=True,
        ):
            st.session_state["standby_frozen"][selected_book] = True
            incident["burn_rate_sec"] = 0.0
            ledger_status = write_ledger_event(
                book=selected_book,
                action="CHAIRMAN_STANDBY_FREEZE",
                rationale=counsel_rationale,
                work_order_id=st.session_state.active_incident_id,
                t0=incident["start_time"],
            )
            stamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
            incident["audit_log"].append(
                f"[{stamp}] CHAIRMAN_STANDBY_FREEZE: Standby carry billing tripped to $0/sec. "
                f"Rationale: {counsel_rationale} | {ledger_status}"
            )
            st.rerun()


st.set_page_config(
    page_title="Factory Command Post | Incident Control",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.sidebar.title("FACTORY COMMAND POST")
st.sidebar.caption("Autonomous Capital Defense Control Plane")
total_fleet_burn = sum(
    incident["burn_rate_sec"] * 604800
    for incident in st.session_state.incident_store.values()
    if incident["status"] != "RESOLVED"
)
st.sidebar.metric("Portfolio Holding Burn", f"${total_fleet_burn:,.0f} / wk")
st.sidebar.divider()
st.sidebar.subheader("Active Blockage Queue")

for incident_id, incident_data in st.session_state.incident_store.items():
    button_label = f"{incident_data['priority']}: {incident_id}\n{incident_data['title'][:26]}..."
    if st.sidebar.button(button_label, key=f"incident_nav_{incident_id}", use_container_width=True):
        st.session_state.active_incident_id = incident_id
        if incident_data["gms"]:
            st.session_state.selected_gm_branch = next(iter(incident_data["gms"]))
        st.rerun()

incident = st.session_state.incident_store[st.session_state.active_incident_id]
elapsed_seconds = (datetime.datetime.now() - incident["start_time"]).total_seconds()
accumulated_burn = elapsed_seconds * incident["burn_rate_sec"] if incident["status"] != "RESOLVED" else 0.0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Incident Status", incident["status"], delta=incident["priority"])
col2.metric(
    "Active Holding Burn",
    f"${incident['burn_rate_sec'] * 604800:,.0f} / wk" if incident["status"] != "RESOLVED" else "$0 / wk",
    f"${incident['burn_rate_sec']:.2f}/sec",
    delta_color="inverse",
)
col3.metric("Sunk Accrual (Since Lock)", f"${accumulated_burn:,.0f}", incident["schedule_drift"], delta_color="inverse")
col4.metric(
    "Operational Readiness",
    f"{readiness_count(st.session_state['selected_book'])} / 8 Frontline SOP",
    "GOV DEADLOCKED" if incident["status"] == "DEADLOCKED" else "CLEARED",
    delta_color="inverse" if incident["status"] == "DEADLOCKED" else "normal",
)

st.divider()
st.header(f"{incident['priority']}: {incident['title']}")
render_tier_1(incident, st.session_state["selected_book"])

st.markdown(
    "**Blockage:** Grid Interconnection Agreement Section 4.2 Part 2 COD Filing Gate &nbsp;|&nbsp; "
    f"**Cognizant Director:** `{incident['cognizant_director']['name']}` "
    f"({incident['cognizant_director']['role']}) &nbsp;|&nbsp; "
    f"**Directorate Status:** `{incident['cognizant_director']['status']}`"
)
if incident["status"] == "DEADLOCKED" and st.button(
    "Concur with Chairman Carve-Out", key="directorate_concurrence"
):
    incident["cognizant_director"]["status"] = "DIRECTORATE CONCURRENCE GRANTED"
    st.rerun()

with st.expander(
    f"Command Intelligence Briefing | {incident['cognizant_director']['name']}",
    expanded=False,
):
    st.markdown(
        f"*Domain Context Injected: {incident['cognizant_director']['role']} | "
        f"Current Burn: ${incident['burn_rate_sec']:.2f}/sec*"
    )
    intel_query = st.selectbox(
        "Select Directorate Assessment Prompt:",
        [
            "Assess OEM Warranty Forfeiture ($1.2M) vs. ERCOT Queue Drop Risk",
            "Draft Binding Directorate Indemnification Waiver for Elena Rostova",
            "Synthesize IEEE 2800 Test Packet Gaps for Board Minutes",
        ],
        key=f"intel_query_{st.session_state.active_incident_id}",
    )
    intelligence_key = f"intelligence_result_{st.session_state.active_incident_id}"

    if st.button(
        "Run Command Intelligence Synthesis",
        key=f"run_intelligence_{st.session_state.active_incident_id}",
        use_container_width=True,
    ):
        st.session_state[intelligence_key] = intel_query

    generated_query = st.session_state.get(intelligence_key)
    if generated_query == "Assess OEM Warranty Forfeiture ($1.2M) vs. ERCOT Queue Drop Risk":
        st.info(
            "**Executive Trade-Off Synthesis:**\n"
            "- **Regulatory Risk (David Chen):** Queue position cancellation triggers immediate $4.5M interconnection study forfeiture and a 14-month COD delay.\n"
            "- **Asset Integrity Risk (Elena Rostova):** Energizing without IEEE 2800 verified logs risks OEM voiding warranty on the $1.2M high-voltage transformer.\n"
            "- **Financial Crossover:** Idle contractor carry ($610k/wk) exceeds the total unhedged equipment risk in exactly **13.8 days**.\n"
            "- **Director Recommendation:** Concur with Conditional Indemnity Carve-Out. Absorbing equipment warranty at directorate level saves ~$2.4M in idle burn and queue penalties."
        )
    elif generated_query == "Draft Binding Directorate Indemnification Waiver for Elena Rostova":
        st.code(
            "DIRECTORATE INDEMNITY RESOLUTION (ERCOT IA Section 4.2)\n"
            "Pursuant to delegated authority under the Grid Risk & Technical Integrity Committee:\n"
            "1. Elena Rostova (GM - Field Operations) is granted full fiduciary and operational indemnification against manufacturer warranty forfeiture arising from energization prior to final IEEE 2800 packet completion.\n"
            "2. Direct David Chen (GM - Regulatory) to execute and transmit Part 2 COD Attestation forthwith.\n"
            "3. Contingency reserve of $1,200,000 is allocated to Asset Defense Escrow.",
            language="text",
        )
    elif generated_query:
        st.info(
            "**Board Minute Addendum:**\n"
            "Telemetry verification completed on 5 of 6 gates (ICCP 4-sec, EMT PSCAD cleared). "
            "Check #6 (IEEE 2800 packet transmission) is functionally complete on site but withheld "
            "due to administrative sign-off protocols. Operational risk is deemed administrative, not electrical."
        )

    if generated_query:
        if st.button(
            "Stamp Assessment to Tier 4 Forensic Ledger",
            key=f"stamp_intelligence_{st.session_state.active_incident_id}",
        ):
            timestamp = datetime.datetime.utcnow().strftime("%H:%M:%S UTC")
            director = incident["cognizant_director"]
            incident["audit_log"].append(
                f"[{timestamp}] COMMAND INTELLIGENCE: Generated & concurred by "
                f"{director['name']} ({director['role']}) - Query: {generated_query}"
            )
            st.success("Stamped to Forensic Audit Ledger.")
            st.rerun()

st.subheader("Tier 2 | General Management Workspaces")
if incident["gms"]:
    gm_names = list(incident["gms"])
    if st.session_state.selected_gm_branch not in gm_names:
        st.session_state.selected_gm_branch = gm_names[0]
    selected_gm = st.radio(
        "Isolate General Manager Workstream:",
        gm_names,
        index=gm_names.index(st.session_state.selected_gm_branch),
        horizontal=True,
        key="incident_gm_selector",
    )
    st.session_state.selected_gm_branch = selected_gm
    active_gm = incident["gms"][selected_gm]
    st.markdown(f"**Lead GM:** {selected_gm} - `{active_gm['role']}`")
    st.markdown(f"**Domain Responsibility:** {active_gm['domain']}")
    st.info(f"**Operational Position:** {active_gm['stance']}")

    st.subheader(f"Tier 3 | Site Operations Telemetry ({selected_gm})")
    for check in active_gm["checks"]:
        check_col1, check_col2, check_col3 = st.columns([1, 3, 2])
        check_col1.write(f"**{check['id']}**")
        check_col2.write(check["name"])
        if check["status"] == "CLEARED":
            check_col3.success(f"CLEARED: {check['evidence']}")
        else:
            check_col3.error(f"HELD: {check['evidence']}")
else:
    st.write("Telemetry routing nominal.")

st.subheader("Tier 4 | Forensic Audit Ledger & Remedial Action Engine")
if incident["status"] == "DEADLOCKED":
    st.markdown("### Authorize Executive Remedial Action")
    action_col1, action_col2, action_col3 = st.columns(3)
    with action_col1:
        st.markdown("**Option A: Indemnity Carve-Out**")
        st.caption("Filing proceeds. Directorate absorbs OEM warranty forfeiture risk.")
        if st.button("Authorize Carve-Out & File COD", key="authorize_carveout", use_container_width=True):
            incident["status"] = "RESOLVED"
            incident["burn_rate_sec"] = 0.0
            incident["audit_log"].append(
                f"[{datetime.datetime.utcnow().strftime('%H:%M:%S UTC')}] CHAIRMAN DIRECTIVE EXECUTED: Issued Executive Indemnification Carve-Out. Warranty exposure retained at Directorate level. David Chen authorized to submit Part 2 COD immediately."
            )
            for gm_data in incident["gms"].values():
                for check in gm_data["checks"]:
                    check["status"] = "CLEARED"
                    check["evidence"] = "Directorate Override"
            st.rerun()
    with action_col2:
        st.markdown("**Option B: Dispatch Test Team**")
        st.caption("Authorize $35k draw to rush IEEE 2800 field crew in 6 hours.")
        if st.button("Draw Capital & Expedite", key="expedite_test_team", use_container_width=True):
            incident["audit_log"].append(
                f"[{datetime.datetime.utcnow().strftime('%H:%M:%S UTC')}] EMERGENCY CAPITAL DRAW: $35,000 drawn for expedited IEEE 2800 field crew. Expected clear in 6 hours."
            )
            st.rerun()
    with action_col3:
        st.markdown("**Option C: Stand-Down Order**")
        st.caption("Demobilize idle high-voltage contractor crews to stop burn.")
        if st.button("Demobilize Crews", key="demobilize_crews", use_container_width=True):
            incident["burn_rate_sec"] = 0.0
            incident["audit_log"].append(
                f"[{datetime.datetime.utcnow().strftime('%H:%M:%S UTC')}] CONTRACTOR STAND-DOWN: Permian high-voltage crews demobilized. Carry cost halted to $0/sec pending queue outcome."
            )
            st.rerun()

st.markdown("### Ledger Entries (Cryptographic Chain)")
for log_entry in reversed(incident["audit_log"]):
    st.code(log_entry, language="yaml")

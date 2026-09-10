import datetime
import hashlib
import json

import streamlit as st

import ledger_store


VIEW_TIER_1 = "🏛️ Tier 1 | Chairman Directorate"
VIEW_TIER_2 = "📋 Tier 2 | Executive Management Overview"
VIEW_DOCKET_VANCE = "⚡ Docket: Marcus Vance (Grid & Telemetry)"
VIEW_DOCKET_ROSTOVA = "🔧 Docket: Elena Rostova (Field Substation)"
VIEW_DOCKET_CHEN = "⚖️ Docket: David Chen (Regulatory & Market Ops)"
VIEW_TIER_3 = "⚡ Tier 3 | Site Operations Tactical Command"
VIEW_TIER_4 = "📜 Tier 4 | Master Forensic Ledger"

NAV_OPTIONS = [
    VIEW_TIER_1,
    VIEW_TIER_2,
    VIEW_DOCKET_VANCE,
    VIEW_DOCKET_ROSTOVA,
    VIEW_DOCKET_CHEN,
    VIEW_TIER_3,
    VIEW_TIER_4,
]

DOCKET_ROUTES = {
    "Marcus Vance": VIEW_DOCKET_VANCE,
    "Elena Rostova": VIEW_DOCKET_ROSTOVA,
    "David Chen": VIEW_DOCKET_CHEN,
}
ROUTE_TO_GM = {route: gm for gm, route in DOCKET_ROUTES.items()}


TOTAL_ASSET_EXPOSURE = 88_500_000
BOARD_EXPOSURE_LIMIT = 95_000_000
WEEKLY_HOLDING_BURN = 610_000
CLIENT_REALIZATION_TARGET = 549_000
PHOENIX_ADVISORY_FEE = 61_000
CARRY_BURN_PER_SEC = 1.01
SITE_LOCATION = "Wharton 345kV Substation / Inverter Yard"
WORK_ORDER_ID = "WO-BESS-345KV-09"
LOTO_STATUS = "LOTO ACTIVE: BUS GROUNDED"
TELEMETRY_HEARTBEAT = "SCADA PING: 24ms | IEEE 2800 NORMAL"

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
        "role": "GM - Grid Interconnection & Telemetry",
        "authority": "Signature authority over ICCP/RTU point-maps, EMT model attestation, and TSP handshake.",
        "upstream": [
            "ERCOT-approved resource ID and NOIE registration packet (David Chen)",
            "Energized substation bay with terminated fiber path (Elena Rostova)",
        ],
        "downstream": [
            "Certified telemetry point-map required before Elena can complete relay coordination",
            "Validated PSCAD EMT model required before David can file Part 2 COD attestation",
        ],
        "waiver_terms": (
            "The Corporation shall indemnify and hold harmless Marcus Vance against any third-party claim, "
            "protocol penalty, or telemetry non-conformance action arising from certification of the ICCP "
            "point-map at 4-second scan tolerance, pursuant to DGCL § 141(e) reliance on expert reports."
        ),
        "ai_specialty": "IEEE 2800 / ICCP TASE.2 grid telemetry protocol counsel",
        "frontline": {
            "name": "Priya Raghunathan",
            "role": "SCADA & Telemetry Field Engineer",
            "mandate": "ERCOT Nodal Protocol § 6.5.5.2 telemetry conformance and RTU point-map integrity.",
            "liability": "Resource-status suspension and dispatch revenue forfeiture on sustained scan drift.",
            "telemetry": [
                ("ICCP scan interval", "4.1 s", "DRIFT"),
                ("RTU point-map parity", "1,842 / 1,842", "NOMINAL"),
                ("EMT model residual", "0.6%", "NOMINAL"),
            ],
            "field_status": "Scan interval holding at 4.1s on the primary path; failover circuit staged for re-scan.",
            "directive": "Execute a 30-minute dual-path re-scan and log point-map evidence to the ledger.",
        },
        "ai_brief": (
            "Protocol read: ICCP TASE.2 scan tolerance is a performance obligation, not a safety interlock. "
            "A logged re-scan commitment with time-stamped point-map evidence satisfies ERCOT Nodal § 6.5.5.2 "
            "good-faith compliance while the asset energizes."
        ),
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
        "role": "GM - Field Operations & Contractor Mobilization",
        "authority": "Signature authority over high-voltage energization, EPC crews, and substation safety clearance.",
        "upstream": [
            "Certified telemetry point-map and relay setpoints (Marcus Vance)",
            "Executed EPC warranty position and regulatory energization window (David Chen)",
        ],
        "downstream": [
            "Energization clearance required before Marcus can close live telemetry verification",
            "IEEE 2800 packet and grounding certificate required before David files COD attestation",
        ],
        "waiver_terms": (
            "The Corporation shall indemnify and hold harmless Elena Rostova, in her individual and official "
            "capacity, against OEM warranty forfeiture, EPC contractor claims, and third-party equipment "
            "damage claims arising from energization prior to final IEEE 2800 packet closure. A $1,200,000 "
            "Asset Defense Escrow is allocated as the exclusive source of recovery."
        ),
        "ai_specialty": "EPC warranty & high-voltage equipment contract counsel",
        "frontline": {
            "name": "Hector Alvarez",
            "role": "High-Voltage Commissioning Superintendent",
            "mandate": "IEEE 2800 ride-through packet closure, grounding certification, and crew safety clearance.",
            "liability": "OEM transformer warranty forfeiture ($1.2M) and EPC contractor claim exposure.",
            "telemetry": [
                ("Transformer oil temp", "58 °C", "NOMINAL"),
                ("Grounding grid resistance", "0.42 Ω", "PENDING WITNESS"),
                ("Ride-through packet", "7 / 9 cases", "IN TEST"),
            ],
            "field_status": "Crews mobilized and idle at the Permian bay awaiting written indemnity before energizing.",
            "directive": "Hold energization until board indemnity lands, then close grounding witness test same shift.",
        },
        "ai_brief": (
            "Contract read: OEM warranty forfeiture is a bounded $1.2M liability transferable to the "
            "directorate reserve. Continued standby carry overtakes that ceiling in roughly 13.8 days, so "
            "the indemnity is the cheaper instrument."
        ),
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
        "role": "GM - Regulatory & Market Operations",
        "authority": "Signature authority over ERCOT filings, queue position, NERC registration, and settlement enablement.",
        "upstream": [
            "Validated PSCAD EMT model and certified point-map (Marcus Vance)",
            "IEEE 2800 test packet and grounding/safety clearance (Elena Rostova)",
        ],
        "downstream": [
            "Filed Part 2 COD attestation unlocks commercial dispatch and settlement revenue",
            "NERC registration closes the interconnection docket and releases standby crews",
        ],
        "waiver_terms": (
            "The Corporation shall indemnify and hold harmless David Chen against regulatory penalty, "
            "deficiency assessment, or third-party claim arising from provisional Part 2 COD attestation "
            "filed under ERCOT IA § 4.2 on the basis of board-authorized safe-harbor direction."
        ),
        "ai_specialty": "ERCOT tariff, nodal protocol & interconnection agreement counsel",
        "frontline": {
            "name": "Dana Whitfield",
            "role": "Interconnection Compliance Field Liaison",
            "mandate": "ERCOT IA § 4.2 filing-window compliance, NERC registration, and settlement enablement.",
            "liability": "Queue cancellation, $4.5M restudy forfeiture, and 14-month COD slip.",
            "telemetry": [
                ("Queue position", "#14 (48 h to drop)", "AT RISK"),
                ("Part 2 COD packet", "Drafted, unsigned", "PENDING"),
                ("NERC registration", "Awaiting COD", "BLOCKED"),
            ],
            "field_status": "Filing packet staged in the ERCOT portal; submission blocked pending frontline attestations.",
            "directive": "File provisional Part 2 COD under safe harbor the moment attestations clear.",
        },
        "ai_brief": (
            "Tariff read: a provisional § 4.2 filing draws a curable deficiency notice and administrative "
            "penalty exposure, materially below the $4.5M restudy forfeiture and 14-month slip triggered by "
            "queue cancellation."
        ),
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
if "domain_frozen" not in st.session_state:
    st.session_state["domain_frozen"] = {}
if "field_escalations" not in st.session_state:
    st.session_state["field_escalations"] = {}
if "escalation_form_open" not in st.session_state:
    st.session_state["escalation_form_open"] = False
if "technician_handle" not in st.session_state:
    st.session_state["technician_handle"] = "T3-FIELD-LEAD / H. Alvarez"
if "field_evidence" not in st.session_state:
    st.session_state["field_evidence"] = {}
if "nav_selection" not in st.session_state:
    st.session_state["nav_selection"] = NAV_OPTIONS[0]
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


def fetch_gm_ledger_events(book: str, gm_name: str, limit: int = 200) -> list:
    """Blocks signed by, or expressly naming, this GM — strict domain-scoped chain."""
    if not st.session_state.get("ledger_ready"):
        return []
    try:
        with ledger_store.get_db() as conn:
            rows = conn.execute(
                """
                SELECT * FROM forensic_ledger
                WHERE operating_book = ?
                  AND (actor_id = ? OR official_title LIKE ? OR blocker_notes LIKE ?)
                ORDER BY entry_id DESC
                LIMIT ?
                """,
                (book, gm_name, f"%{gm_name}%", f"%{gm_name}%", limit),
            ).fetchall()
        return [dict(row) for row in rows]
    except Exception:
        return []


def commit_to_ledger(
    event_type: str,
    actor: str,
    domain: str,
    rationale: str,
    payload: str = "",
    tier: int = 1,
    title: str | None = None,
    book: str | None = None,
    work_order_id: str | None = None,
    t0=None,
) -> str:
    """Single writer for every governance event: SHA-256 block hash + committed SQLite insert."""
    if not st.session_state.get("ledger_ready"):
        return "LEDGER OFFLINE - EVENT HELD IN SESSION CHAIN"

    book = book or st.session_state["selected_book"]
    work_order_id = work_order_id or st.session_state.active_incident_id
    t1 = datetime.datetime.utcnow()
    t0_dt = t0 if isinstance(t0, datetime.datetime) else t1
    lag = max(0.0, (t1 - t0_dt).total_seconds())
    cost = ledger_store.calculate_hesitation_cost(lag)
    stamp = t1.strftime("%Y-%m-%d %H:%M:%S UTC")
    notes = rationale if not payload else f"{rationale} || PAYLOAD: {payload}"
    block_hash = hashlib.sha256(f"{stamp}|{actor}|{event_type}|{rationale}".encode()).hexdigest()

    try:
        conn = ledger_store.get_db()
        try:
            conn.execute(
                """
                INSERT INTO forensic_ledger (
                    operating_book, tier_level, actor_id, official_title, action_type,
                    work_order_id, t0_detection, t1_resolution, governance_lag_sec,
                    hesitation_cost, blocker_category, blocker_notes, sha256_hash
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    book,
                    tier,
                    actor,
                    title or actor,
                    event_type,
                    work_order_id,
                    t0_dt.strftime("%Y-%m-%d %H:%M:%S UTC"),
                    stamp,
                    lag,
                    cost,
                    domain,
                    notes,
                    block_hash,
                ),
            )
            conn.commit()
        finally:
            conn.close()
        return f"COMMITTED TO SQLITE LEDGER · SHA-256 {block_hash[:16]}…"
    except Exception as exc:
        return f"LEDGER WRITE FAILED: {exc}"


def fetch_ledger_chain(book: str | None = None, limit: int = 1000) -> list:
    """Uncached read of the master ledger; book=None returns every block, newest first."""
    if not st.session_state.get("ledger_ready"):
        return []
    try:
        with ledger_store.get_db() as conn:
            if book is None:
                rows = conn.execute(
                    "SELECT * FROM forensic_ledger ORDER BY entry_id DESC LIMIT ?", (limit,)
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT * FROM forensic_ledger WHERE operating_book = ? ORDER BY entry_id DESC LIMIT ?",
                    (book, limit),
                ).fetchall()
        return [dict(row) for row in rows]
    except Exception:
        return []


def route_to(view: str) -> None:
    st.session_state["nav_selection"] = view
    st.rerun()


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
        events = fetch_gm_ledger_events(selected_book, gm_name, limit=3)
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


def render_gm_docket(incident: dict, selected_book: str, gm_name: str) -> None:
    """Isolated single-page command post for one GM domain."""
    gm_meta = GM_DOMAINS[gm_name]
    frontline = gm_meta["frontline"]
    book_state = ensure_checklist(selected_book)
    owned_checks = gm_checks(gm_name)
    open_checks = gm_open_checks(selected_book, gm_name)
    freeze_key = f"{selected_book}|{gm_name}"
    domain_frozen = st.session_state["domain_frozen"].get(freeze_key, False)

    elapsed = (datetime.datetime.now() - incident["start_time"]).total_seconds()
    domain_rate = CARRY_BURN_PER_SEC * (len(owned_checks) / len(SOP_CHECKS))
    domain_burn = 0.0 if domain_frozen or not open_checks else elapsed * domain_rate
    sla_state = (
        "CLEARED"
        if not open_checks
        else ("BREACHED / ACCRUING BURN" if elapsed > gm_meta["sla_seconds"] else "ON SCHEDULE")
    )
    accent = "#00FFA3" if not open_checks else ("#FF4B4B" if elapsed > gm_meta["sla_seconds"] else "#F5A623")

    if st.button("← Return to Chairman Directorate", key=f"breadcrumb_{gm_name}"):
        route_to(VIEW_TIER_1)

    st.markdown(
        f"<div style='border:2px solid {accent};border-radius:10px;padding:18px 22px;"
        "background:#0B0F19;'>"
        f"<div style='color:#FFFFFF;font-size:1.5rem;font-weight:900;'>🔒 DOMAIN DOCKET LOCKED: "
        f"{gm_name} — {gm_meta['role']}</div>"
        f"<div style='color:{accent};font-size:0.92rem;font-weight:700;margin-top:6px;'>"
        f"Mandate: {gm_meta['domain']} | SLA Target: {gm_meta['sla_label']} | "
        f"Accrued Carry: ${domain_burn:,.0f}</div>"
        f"<div style='color:#9AA4B2;font-size:0.85rem;margin-top:8px;'><b>Domain Authority:</b> "
        f"{gm_meta['authority']}</div>"
        f"<div style='color:#9AA4B2;font-size:0.85rem;margin-top:6px;'><b>Paired Tier 3 Site Lead:</b> "
        f"{frontline['name']} — {frontline['role']}</div>"
        f"<div style='color:{accent};font-size:0.95rem;font-weight:800;margin-top:10px;'>"
        f"Chronometer: elapsed {elapsed/3600:,.1f} hrs · {sla_state} · "
        f"${domain_rate:.2f}/sec{' · BILLING HALTED' if domain_frozen else ''}</div>"
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown("### Section A — Tier 2 Executive Stance & Legal Directives")

    st.markdown("#### 🎩 Tier 2 Executive Stance")
    stance_col, mandate_col = st.columns(2)
    with stance_col:
        st.warning(gm_meta["stance"])
        st.markdown(f"**Domain Accountability:** {gm_meta['authority']}")
    with mandate_col:
        st.markdown(f"**Regulatory Mandate:** {frontline['mandate']}")
        st.markdown(f"**Liability Posture:** {gm_meta['contract_risk']}")
        st.caption(
            f"SLA chronometer: {gm_meta['sla_label']} · elapsed {elapsed/3600:,.1f} hrs · "
            f"overrun {max(0.0, elapsed - gm_meta['sla_seconds'])/3600:,.1f} hrs · "
            f"carry ${domain_burn:,.0f} at ${domain_rate:.2f}/sec"
        )

    st.markdown("#### 🔗 Domain Interface Handshake")
    upstream_col, downstream_col = st.columns(2)
    with upstream_col:
        st.markdown("**Prerequisite inputs required from peer GMs**")
        for item in gm_meta["upstream"]:
            st.markdown(f"- {item}")
    with downstream_col:
        st.markdown("**Downstream deliverables passed to the next domain**")
        for item in gm_meta["downstream"]:
            st.markdown(f"- {item}")

    st.markdown(
        "<div style='border:2px solid #4DA3FF;border-radius:10px;padding:16px 20px;margin-top:12px;"
        "background:rgba(77,163,255,0.06);'>"
        "<div style='color:#4DA3FF;font-size:1.1rem;font-weight:900;'>"
        "🛡️ DGCL § 141 BILATERAL SAFE-HARBOR &amp; INDEMNIFICATION RESOLUTION</div>"
        "</div>",
        unsafe_allow_html=True,
    )
    waiver_rationale = st.text_input(
        "Indemnity Terms / Bilateral Waiver Basis",
        value=gm_meta["waiver_terms"],
        key=f"waiver_rationale_{selected_book}_{gm_name}",
    )
    if st.button(
        "Grant Board Indemnification & Authorize Sign-Off",
        key=f"grant_indemnity_{selected_book}_{gm_name}",
        use_container_width=True,
    ):
        for check in owned_checks:
            st.session_state["checklist_db"][selected_book][check["key"]] = True
            st.session_state.pop(f"docket_sop_{selected_book}_{check['key']}", None)
            st.session_state.pop(f"sop_{selected_book}_{check['key']}", None)
        st.session_state["domain_frozen"][freeze_key] = True
        ledger_status = commit_to_ledger(
            event_type="BILATERAL_INDEMNIFICATION_ISSUED",
            actor=gm_name,
            domain=gm_meta["domain"],
            rationale=waiver_rationale,
            payload=json.dumps({"checks_cleared": [c["key"] for c in owned_checks], "standby": "HALTED"}),
            tier=2,
            title=gm_meta["role"],
            book=selected_book,
            t0=incident["start_time"],
        )
        stamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        incident["audit_log"].append(
            f"[{stamp}] BILATERAL_INDEMNIFICATION_ISSUED ({gm_name}): {waiver_rationale} | {ledger_status}"
        )
        st.rerun()

    st.markdown("#### 🤝 Forensic Executive Meeting & AI Chamber")
    st.caption(f"Domain counsel engaged: {gm_meta['ai_specialty']}")
    meeting_notes = st.text_area(
        "Executive Meeting Notes / Oral Stipulations",
        placeholder=f"Record bilateral stipulations agreed with {gm_name}...",
        key=f"meeting_notes_{selected_book}_{gm_name}",
    )
    domain_query = st.text_input(
        f"Interrogate {gm_meta['ai_specialty']}",
        placeholder=gm_meta["suggested_query"],
        key=f"domain_query_{selected_book}_{gm_name}",
    )
    if domain_query:
        with st.chat_message("assistant"):
            st.write(f"**{gm_meta['ai_specialty']} — response to '{domain_query}'**")
            st.info(
                f"{gm_meta['ai_brief']}\n\n"
                f"**Structural Analysis:** {gm_meta['synthesis']}\n\n"
                f"**Burn vs. Exposure:** domain standby accrues ${domain_rate * 3600:,.0f}/hr "
                f"(${domain_burn:,.0f} to date) against {gm_meta['contract_risk'].rstrip('.')}.\n\n"
                f"**Directive:** {gm_meta['escalation']}"
            )

    if st.button(
        "🔒 Stipulate & Seal Meeting Minutes to Ledger",
        key=f"seal_minutes_{selected_book}_{gm_name}",
        use_container_width=True,
    ):
        stamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        minute_hash = hashlib.sha256(
            f"{selected_book}|{gm_name}|{stamp}|{meeting_notes}".encode()
        ).hexdigest()
        ledger_status = commit_to_ledger(
            event_type="FORENSIC_MEETING_RECORD",
            actor=gm_name,
            domain=gm_meta["domain"],
            rationale=meeting_notes,
            payload=json.dumps({"minutes_sha256": minute_hash, "sealed_at": stamp}),
            tier=2,
            title=gm_meta["role"],
            book=selected_book,
            t0=incident["start_time"],
        )
        incident["audit_log"].append(
            f"[{stamp}] FORENSIC_MEETING_RECORD ({gm_name}): sealed minutes {minute_hash[:16]}… | {ledger_status}"
        )
        st.success(f"Minutes sealed. SHA-256: {minute_hash}")
        st.rerun()

    st.markdown(f"### Section B — Tier 3 Dedicated Frontline Operations ({frontline['role']})")
    st.markdown(
        f"#### 📡 Dedicated Direct Line — {gm_name} (Tier 2) ⇄ {frontline['name']} (Tier 3)"
    )
    st.caption(f"Frontline site lead: {frontline['name']} · {frontline['role']}")
    field_col, order_col = st.columns(2)
    with field_col:
        field_status = st.text_area(
            f"Field status from {frontline['name']}",
            value=frontline["field_status"],
            key=f"field_status_{selected_book}_{gm_name}",
            height=110,
        )
    with order_col:
        gm_directive = st.text_area(
            f"{gm_name} operational directive",
            value=frontline["directive"],
            key=f"gm_directive_{selected_book}_{gm_name}",
            height=110,
        )
    if st.button(
        "⚡ Dispatch Executive Field Order",
        key=f"dispatch_field_order_{selected_book}_{gm_name}",
        use_container_width=True,
    ):
        stamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        ledger_status = commit_to_ledger(
            event_type="EXECUTIVE_FIELD_ORDER",
            actor=gm_name,
            domain=gm_meta["domain"],
            rationale=f"DIRECTIVE to {frontline['name']} ({frontline['role']}): {gm_directive}",
            payload=json.dumps({"field_status": field_status, "dispatched_at": stamp}),
            tier=2,
            title=gm_meta["role"],
            book=selected_book,
            t0=incident["start_time"],
        )
        incident["audit_log"].append(
            f"[{stamp}] EXECUTIVE_FIELD_ORDER ({gm_name} → {frontline['name']}): {gm_directive} | {ledger_status}"
        )
        st.success(f"Field order dispatched to {frontline['name']}. {ledger_status}")
        st.rerun()

    st.markdown(f"#### ✅ Tier 3 Active Frontline Execution — {frontline['role']}")
    telemetry_cols = st.columns(len(frontline["telemetry"]))
    for telemetry_col, (label, reading, badge) in zip(telemetry_cols, frontline["telemetry"]):
        telemetry_col.metric(label, reading, badge, delta_color="off")
    for check in owned_checks:
        widget_key = f"docket_sop_{selected_book}_{check['key']}"
        st.session_state.setdefault(widget_key, bool(book_state.get(check["key"])))
        verified = st.checkbox(
            f"{check['name']} — {'CLEARED' if book_state.get(check['key']) else 'PENDING'}",
            key=widget_key,
        )
        if verified != bool(book_state.get(check["key"])):
            st.session_state["checklist_db"][selected_book][check["key"]] = verified
            st.session_state.pop(f"sop_{selected_book}_{check['key']}", None)
            if verified:
                commit_to_ledger(
                    event_type="CHECK_VERIFIED",
                    actor=gm_name,
                    domain=gm_meta["domain"],
                    rationale=(
                        f"{check['name']} executed by {frontline['name']} ({frontline['role']}) and "
                        f"countersigned by {gm_name} ({gm_meta['role']})."
                    ),
                    payload=json.dumps({"check": check["key"], "source": "GM_DOCKET"}),
                    tier=3,
                    title=gm_meta["role"],
                    book=selected_book,
                    t0=incident["start_time"],
                )
            st.rerun()
    st.caption(
        f"Domain readiness {len(owned_checks) - len(open_checks)}/{len(owned_checks)} · "
        f"heartbeat {datetime.datetime.utcnow().strftime('%H:%M:%S UTC')} · "
        f"book readiness {readiness_count(selected_book)}/8 (synced to Tier 1 & Tier 2)"
    )

    st.markdown(f"### Section C — 📜 Forensic Ledger Trail: {gm_name}")
    domain_chain = fetch_gm_ledger_events(selected_book, gm_name)
    if not domain_chain:
        st.info(f"No ledger blocks signed by {gm_name} on operating book `{selected_book}` yet.")
    else:
        st.dataframe(
            [
                {
                    "Entry": row["entry_id"],
                    "UTC Timestamp": row["t1_resolution"],
                    "Event": row["action_type"],
                    "Signed By": f"{row['actor_id']} ({row['official_title']})",
                    "Tier": row["tier_level"],
                    "Counsel Rationale": row["blocker_notes"] or "n/a",
                    "SHA-256": row["sha256_hash"],
                }
                for row in domain_chain
            ],
            use_container_width=True,
            hide_index=True,
        )
        for row in domain_chain:
            with st.expander(f"Block {row['entry_id']} · {row['action_type']} · {row['t1_resolution']}"):
                st.code(json.dumps(row, indent=2, default=str), language="json")
                st.code(f"SHA-256: {row['sha256_hash']}", language="text")


def render_tier_4(incident: dict, selected_book: str) -> None:
    """Master forensic ledger: every block from every tier, newest first, hashes and payloads visible."""
    st.subheader("📜 Tier 4 | Master Forensic Ledger")
    chain = fetch_ledger_chain()
    if not chain:
        st.info("No SQLite ledger blocks recorded yet.")
    else:
        st.caption(f"{len(chain)} immutable blocks · newest first · live read, no caching.")
        st.dataframe(
            [
                {
                    "Entry": row["entry_id"],
                    "UTC Timestamp": row["t1_resolution"],
                    "Event": row["action_type"],
                    "Actor": row["actor_id"],
                    "Title": row["official_title"],
                    "Tier": row["tier_level"],
                    "Domain": row["blocker_category"],
                    "Book": row["operating_book"],
                    "Lag (s)": round(row["governance_lag_sec"] or 0.0, 1),
                    "Hesitation Cost": f"${row['hesitation_cost']:,.2f}",
                    "SHA-256": row["sha256_hash"],
                }
                for row in chain
            ],
            use_container_width=True,
            hide_index=True,
        )
        for row in chain:
            with st.expander(
                f"Block {row['entry_id']} · {row['action_type']} · {row['t1_resolution']}"
            ):
                st.code(json.dumps(row, indent=2, default=str), language="json")
                st.code(f"SHA-256: {row['sha256_hash']}", language="text")

    st.markdown("### Session Chain (Incident Narrative)")
    for log_entry in reversed(incident["audit_log"]):
        st.code(log_entry, language="yaml")


def active_field_block(book: str):
    """Most recent unresolved Tier 3 escalation for the book, if any."""
    escalations = st.session_state["field_escalations"].get(book, [])
    return escalations[-1] if escalations else None


def field_diagnostic(query: str) -> str:
    """Procedural field response keyed off equipment/protocol terms in the technician's query."""
    text = query.lower()
    if "dnp3" in text or "sel-751" in text or "relay" in text:
        return (
            "**SEL-751 / DNP3 communication timeout — field procedure**\n"
            "1. Open the relay HMI and confirm Port 3 settings: PROTO=DNP3, baud 19200, parity NONE.\n"
            "2. Verify the DNP3 outstation address matches the SCADA master map (ADDR mismatch is the "
            "most common timeout cause after a firmware load).\n"
            "3. Issue `SER` and `STA` at the relay prompt; capture the last 20 sequential events for evidence.\n"
            "4. Loop-test the fiber pair with an OTDR shot; margin below 3 dB requires re-termination.\n"
            "5. If the link recovers, hold a 10-minute soak with 4-second polling before stamping the gate.\n"
            "6. Safety: no relay setting group change while the breaker is in service — take the element to "
            "test mode with the trip lockout applied first."
        )
    if "dielectric" in text or "oil" in text or "transformer" in text:
        return (
            "**Transformer dielectric / oil test — field procedure**\n"
            "1. De-energize, ground both HV and LV bushings, and apply the personal protective grounds.\n"
            "2. Draw the oil sample from the bottom valve into a clean amber syringe; log temperature.\n"
            "3. Run ASTM D877/D1816 breakdown voltage — five shots, discard the outlier, average the rest.\n"
            "4. Reject if the average is below 30 kV; requires filtration and a repeat run.\n"
            "5. Photograph the meter face and attach it as evidence before stamping the gate.\n"
            "6. Safety: hold the grounds in place until the test set is fully discharged and disconnected."
        )
    if "iccp" in text or "telemetry" in text or "scada" in text or "rtu" in text:
        return (
            "**ICCP / RTU telemetry drift — field procedure**\n"
            "1. Confirm the RTU clock is disciplined to GPS; a drifting clock reads as scan-interval drift.\n"
            "2. Run a dual-path scan for 30 minutes and log the interval histogram at both ends.\n"
            "3. Compare the point-map checksum against the ERCOT-approved list; correct any offset points.\n"
            "4. Fail the primary path to the backup circuit and repeat the scan to isolate the carrier.\n"
            "5. Export the point-map evidence file and attach it before stamping the gate."
        )
    if "ground" in text or "grid resistance" in text:
        return (
            "**Grounding grid verification — field procedure**\n"
            "1. Use the fall-of-potential method at 62% spacing; three traverses at 90° offsets.\n"
            "2. Target is under 1 Ω for a substation grid; log soil moisture and ambient temperature.\n"
            "3. Inspect every exothermic weld on the riser conductors for cracks or discoloration.\n"
            "4. Attach the meter readings and witness signature before stamping the gate."
        )
    if "firmware" in text or "patch" in text or "rollback" in text:
        return (
            "**Firmware fault / rollback — field procedure**\n"
            "1. Capture the current settings file and event buffer before touching the image.\n"
            "2. Verify the vendor image checksum against the OEM release note.\n"
            "3. Roll back on the redundant unit first; keep the in-service unit on the known-good image.\n"
            "4. Re-verify protection element pickup values after the load — settings do not always survive.\n"
            "5. Safety: place affected zones in test mode and notify the control room before the reboot."
        )
    return (
        "**General field procedure**\n"
        "1. Isolate the affected circuit, apply lockout/tagout, and verify zero energy with a proven meter.\n"
        "2. Reproduce the fault once and capture instrument readings, event logs, and photos as evidence.\n"
        "3. Check the OEM manual step against the approved SOP revision before deviating.\n"
        "4. If the resolution requires a commercial or contractual decision, raise the Field Blocker Beacon "
        "instead of holding the crew idle."
    )


def render_tier_3(incident: dict, selected_book: str) -> None:
    """Frontline tactical command post: no macro financials — work order, safety, telemetry, gates only."""
    book_state = ensure_checklist(selected_book)
    readiness = readiness_count(selected_book)
    blocker = active_field_block(selected_book)

    st.markdown(
        "<div class='command-header'>⚡ Tier 3 | Site Operations Tactical Command Post</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<div class='field-banner'>"
        f"<div><span class='field-label'>Active Work Order</span>"
        f"<span class='field-value'>{WORK_ORDER_ID}</span></div>"
        f"<div><span class='field-label'>Field Safety / Isolation</span>"
        f"<span class='field-value'>{LOTO_STATUS}</span></div>"
        f"<div><span class='field-label'>Site Telemetry Heartbeat</span>"
        f"<span class='field-value'>{TELEMETRY_HEARTBEAT}</span></div>"
        f"<div><span class='field-label'>SOP Execution Progress</span>"
        f"<span class='field-value'>{readiness} / {len(SOP_CHECKS)} Frontline Gates Cleared</span></div>"
        "</div>",
        unsafe_allow_html=True,
    )
    st.caption(f"Active site: {SITE_LOCATION}")
    st.progress(readiness / len(SOP_CHECKS), text=f"SOP readiness {readiness} / {len(SOP_CHECKS)} verified")

    technician = st.text_input(
        "Technician handle (signs every attestation)",
        key="technician_handle",
    )

    st.markdown(
        "#### 🛠️ Frontline Technical Co-Pilot: Query OEM Manuals, IEEE Standards & "
        "Step-by-Step Troubleshooting"
    )
    diagnostic_query = st.text_input(
        "Field diagnostic query",
        placeholder="e.g., How do we resolve DNP3 communication timeout on SEL-751 relay during step 3?",
        key=f"field_diagnostic_query_{selected_book}",
        label_visibility="collapsed",
    )
    if st.button("🔍 Run Field Diagnostic", key=f"run_field_diagnostic_{selected_book}", use_container_width=True):
        st.session_state[f"field_diagnostic_result_{selected_book}"] = diagnostic_query
    diagnostic_result = st.session_state.get(f"field_diagnostic_result_{selected_book}")
    if diagnostic_result:
        st.info(field_diagnostic(diagnostic_result))

    if blocker:
        remaining = (blocker["deadline"] - datetime.datetime.utcnow()).total_seconds()
        clock = (
            f"{remaining/60:,.0f} min remaining on management response clock"
            if remaining > 0
            else f"RESPONSE CLOCK EXPIRED {abs(remaining)/60:,.0f} min ago"
        )
        st.error(
            f"🚨 **CRITICAL FIELD BLOCK ACTIVE** — {blocker['detail']}\n\n"
            f"**Third party:** {blocker['vendor']} · **Requested of GM:** {blocker['requested_action']}\n\n"
            f"**Escalated:** {blocker['opened_at']} · {clock}"
        )
    else:
        st.markdown(
            "<div class='beacon-box'>🚨 FIELD BLOCKER BEACON — raise a stall to General Management "
            "and the Directorate rather than holding crews idle at the panel.</div>",
            unsafe_allow_html=True,
        )

    if st.button(
        "🚨 Escalate Field Blocker to General Management & Directorate",
        key=f"open_escalation_{selected_book}",
        use_container_width=True,
    ):
        st.session_state["escalation_form_open"] = True

    if st.session_state["escalation_form_open"]:
        with st.form(f"escalation_form_{selected_book}"):
            st.markdown("**Field Blocker Escalation**")
            root_cause = st.text_area(
                "Root Cause / Blocker Detail",
                placeholder=(
                    "e.g., EPC contractor refusing to certify transformer dielectric oil test "
                    "without a waiver"
                ),
            )
            third_party = st.text_input(
                "Third Party / Vendor Causing Stall",
                placeholder="e.g., Permian HV Services (EPC) / OEM warranty desk",
            )
            requested_action = st.text_area(
                "Requested Action from GM",
                placeholder="e.g., Issue executive indemnity waiver or invoke liquidated damages",
            )
            submitted = st.form_submit_button("Submit Escalation & Start 30-Minute Response Clock")
        if submitted:
            opened = datetime.datetime.utcnow()
            escalation = {
                "detail": root_cause or "Unspecified field blocker",
                "vendor": third_party or "Unspecified third party",
                "requested_action": requested_action or "Executive determination requested",
                "opened_at": opened.strftime("%Y-%m-%d %H:%M:%S UTC"),
                "deadline": opened + datetime.timedelta(minutes=30),
                "technician": technician,
            }
            st.session_state["field_escalations"].setdefault(selected_book, []).append(escalation)
            st.session_state["escalation_form_open"] = False
            incident["status"] = "CRITICAL FIELD BLOCK"
            ledger_status = commit_to_ledger(
                event_type="TACTICAL_BLOCKER_ESCALATED",
                actor=technician,
                domain="Site Operations (Tier 3)",
                rationale=f"ROOT CAUSE: {escalation['detail']}",
                payload=json.dumps(
                    {
                        "third_party": escalation["vendor"],
                        "requested_action": escalation["requested_action"],
                        "response_deadline": escalation["deadline"].strftime("%Y-%m-%d %H:%M:%S UTC"),
                    }
                ),
                tier=3,
                title="Tier 3 Frontline Site Lead",
                book=selected_book,
                t0=incident["start_time"],
            )
            incident["audit_log"].append(
                f"[{escalation['opened_at']}] TACTICAL_BLOCKER_ESCALATED ({technician}): "
                f"{escalation['detail']} | GM response due by "
                f"{escalation['deadline'].strftime('%H:%M:%S UTC')} | {ledger_status}"
            )
            st.rerun()

    st.markdown("#### ✅ Field Execution & Attestation (Checks #1 – #8)")
    for index, check in enumerate(SOP_CHECKS, start=1):
        widget_key = f"tier3_sop_{selected_book}_{check['key']}"
        st.session_state.setdefault(widget_key, bool(book_state.get(check["key"])))
        verified = st.checkbox(
            f"Check #{index} — {check['name']} ({check['owner']}) — "
            f"{'VERIFIED' if book_state.get(check['key']) else 'PENDING'}",
            key=widget_key,
        )
        evidence_key = f"{selected_book}|{check['key']}"
        evidence = st.session_state["field_evidence"].setdefault(
            evidence_key, {"note": "", "dictation": ""}
        )
        with st.expander(f"📝 Frontline Field Note & Evidence Attachment — Check #{index}"):
            evidence["note"] = st.text_area(
                "Witness test values, multimeter readings, instrument serials",
                value=evidence["note"],
                key=f"evidence_note_{evidence_key}",
            )
            evidence["dictation"] = st.text_area(
                "🎙️ Dictate Field Note (Voice-to-Evidence)",
                value=evidence["dictation"],
                key=f"evidence_dictation_{evidence_key}",
                placeholder="Spoken field note transcribed at the panel...",
            )
            uploaded = st.file_uploader(
                "Attach photo / instrument capture",
                key=f"evidence_photo_{evidence_key}",
                type=["png", "jpg", "jpeg", "pdf"],
            )
            if uploaded is not None:
                st.caption(f"Attached: {uploaded.name} ({uploaded.size:,} bytes)")
            if st.button("Commit field note to ledger", key=f"commit_note_{evidence_key}"):
                note_status = commit_to_ledger(
                    event_type="FIELD_NOTE_RECORDED",
                    actor=technician,
                    domain=check["owner"],
                    rationale=f"Field note for Check #{index} {check['name']}",
                    payload=json.dumps(
                        {
                            "check": check["key"],
                            "note": evidence["note"],
                            "dictation": evidence["dictation"],
                            "attachment": uploaded.name if uploaded is not None else None,
                        }
                    ),
                    tier=3,
                    title="Tier 3 Frontline Site Lead",
                    book=selected_book,
                    t0=incident["start_time"],
                )
                st.success(note_status)

        if verified != bool(book_state.get(check["key"])):
            st.session_state["checklist_db"][selected_book][check["key"]] = verified
            st.session_state.pop(f"sop_{selected_book}_{check['key']}", None)
            st.session_state.pop(f"docket_sop_{selected_book}_{check['key']}", None)
            commit_to_ledger(
                event_type="CHECK_VERIFIED" if verified else "CHECK_WITHDRAWN",
                actor=technician,
                domain=check["owner"],
                rationale=(
                    f"Check #{index} {check['name']} "
                    f"{'stamped' if verified else 'withdrawn'} by {technician} at the panel."
                ),
                payload=json.dumps(
                    {
                        "check": check["key"],
                        "evidence": evidence["note"],
                        "dictation": evidence["dictation"],
                        "source": "TIER_3",
                    }
                ),
                tier=3,
                title="Tier 3 Frontline Site Lead",
                book=selected_book,
                t0=incident["start_time"],
            )
            st.rerun()

    st.caption(
        f"Heartbeat {datetime.datetime.utcnow().strftime('%H:%M:%S UTC')} · readiness "
        f"{readiness}/8 synced live to Tier 1 Chairman metrics and Tier 2 GM dockets."
    )


def render_tier_2(incident: dict, selected_book: str) -> None:
    st.subheader("Tier 2 | General Management Overview")
    blocker = active_field_block(selected_book)
    if blocker:
        remaining = (blocker["deadline"] - datetime.datetime.utcnow()).total_seconds()
        st.error(
            f"🚨 CRITICAL FIELD BLOCK escalated from Tier 3 — {blocker['detail']}\n\n"
            f"**Third party:** {blocker['vendor']} · **Requested action:** {blocker['requested_action']} · "
            f"**Response clock:** {remaining/60:,.0f} min"
        )
    for gm_name, gm_meta in GM_DOMAINS.items():
        open_checks = gm_open_checks(selected_book, gm_name)
        owned = gm_checks(gm_name)
        cleared = len(owned) - len(open_checks)
        with st.container(border=True):
            st.markdown(f"**{gm_name}** — `{gm_meta['role']}`")
            st.markdown(f"**Domain Responsibility:** {gm_meta['domain']}")
            st.markdown(
                f"**Paired Tier 3 Site Lead:** {gm_meta['frontline']['name']} — "
                f"{gm_meta['frontline']['role']}"
            )
            st.progress(cleared / len(owned), text=f"Domain gates verified {cleared} / {len(owned)}")
            if open_checks:
                st.markdown("**Open checks:**")
                for check in open_checks:
                    st.markdown(f"- {check['name']}")
            else:
                st.success("All domain gates verified.")
            st.info(f"**Operational Position:** {gm_meta['stance']}")
            st.caption(
                f"SLA {gm_meta['sla_label']} · {len(open_checks)} gate(s) withheld · "
                f"{gm_meta['contract_risk']}"
            )
            directive_col, nav_col = st.columns([3, 1])
            domain_directive = directive_col.text_input(
                f"Directive to {gm_name}",
                key=f"tier2_directive_{selected_book}_{gm_name}",
                placeholder="Issue a domain directive or cross-domain escalation...",
                label_visibility="collapsed",
            )
            if directive_col.button(
                f"Issue directive to {gm_name}", key=f"tier2_directive_btn_{gm_name}"
            ):
                status = commit_to_ledger(
                    event_type="DOMAIN_DIRECTIVE_ISSUED",
                    actor="CHAIRMAN",
                    domain=gm_meta["domain"],
                    rationale=domain_directive or "Domain directive issued without written basis.",
                    payload=json.dumps({"target_gm": gm_name, "open_checks": len(open_checks)}),
                    tier=2,
                    title="Chairman of the Board",
                    book=selected_book,
                    t0=incident["start_time"],
                )
                incident["audit_log"].append(
                    f"[{datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}] "
                    f"DOMAIN_DIRECTIVE_ISSUED ({gm_name}): {domain_directive} | {status}"
                )
                st.success(status)
            if nav_col.button("Inspect Docket", key=f"tier2_open_{gm_name}", use_container_width=True):
                st.session_state["inspected_gm"] = gm_name
                route_to(DOCKET_ROUTES[gm_name])


def render_remedial_engine(incident: dict) -> None:
    if incident["status"] != "DEADLOCKED":
        return
    st.markdown("### Authorize Executive Remedial Action")
    action_col1, action_col2, action_col3 = st.columns(3)
    with action_col1:
        st.markdown("**Option A: Indemnity Carve-Out**")
        st.caption("Filing proceeds. Directorate absorbs OEM warranty forfeiture risk.")
        if st.button("Authorize Carve-Out & File COD", key="authorize_carveout", use_container_width=True):
            incident["status"] = "RESOLVED"
            incident["burn_rate_sec"] = 0.0
            incident["audit_log"].append(
                f"[{datetime.datetime.utcnow().strftime('%H:%M:%S UTC')}] CHAIRMAN DIRECTIVE EXECUTED: "
                "Issued Executive Indemnification Carve-Out. Warranty exposure retained at Directorate level."
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
                f"[{datetime.datetime.utcnow().strftime('%H:%M:%S UTC')}] EMERGENCY CAPITAL DRAW: $35,000 "
                "drawn for expedited IEEE 2800 field crew. Expected clear in 6 hours."
            )
            st.rerun()
    with action_col3:
        st.markdown("**Option C: Stand-Down Order**")
        st.caption("Demobilize idle high-voltage contractor crews to stop burn.")
        if st.button("Demobilize Crews", key="demobilize_crews", use_container_width=True):
            incident["burn_rate_sec"] = 0.0
            incident["audit_log"].append(
                f"[{datetime.datetime.utcnow().strftime('%H:%M:%S UTC')}] CONTRACTOR STAND-DOWN: Permian "
                "high-voltage crews demobilized. Carry cost halted to $0/sec pending queue outcome."
            )
            st.rerun()


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
    field_block = active_field_block(selected_book)
    if field_block:
        remaining = (field_block["deadline"] - datetime.datetime.utcnow()).total_seconds()
        st.error(
            f"🚨 CRITICAL FIELD BLOCK (Tier 3 escalation) — {field_block['detail']}\n\n"
            f"**Third party:** {field_block['vendor']} · **Requested action:** "
            f"{field_block['requested_action']} · **Management response clock:** {remaining/60:,.0f} min"
        )
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
            f"📂 OPEN {gm_name.upper()} DOCKET",
            key=f"inspect_gm_{selected_book}_{gm_name}",
            use_container_width=True,
            type="primary" if is_inspected else "secondary",
        ):
            st.session_state["inspected_gm"] = gm_name
            route_to(DOCKET_ROUTES[gm_name])

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
                # drop stale checkbox widget state so every tier re-seeds from checklist_db
                st.session_state.pop(f"sop_{selected_book}_{check['key']}", None)
                st.session_state.pop(f"docket_sop_{selected_book}_{check['key']}", None)
                st.session_state.pop(f"tier3_sop_{selected_book}_{check['key']}", None)
            ledger_status = commit_to_ledger(
                event_type="CHAIRMAN_UNILATERAL_OVERRIDE",
                actor="CHAIRMAN",
                domain="Board Directorate",
                rationale=counsel_rationale,
                payload=json.dumps({"gates_forced": [c["key"] for c in SOP_CHECKS], "authority": "DGCL 141"}),
                tier=1,
                title="Chairman of the Board",
                book=selected_book,
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
            ledger_status = commit_to_ledger(
                event_type="CHAIRMAN_STANDBY_FREEZE",
                actor="CHAIRMAN",
                domain="Board Directorate",
                rationale=counsel_rationale,
                payload=json.dumps({"burn_rate_sec": 0.0, "circuit_breaker": "TRIPPED"}),
                tier=1,
                title="Chairman of the Board",
                book=selected_book,
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

st.markdown(
    """
    <style>
    .command-header {
        background: linear-gradient(90deg, #101826 0%, #0B0F19 100%);
        border-left: 8px solid #F5A623;
        border-radius: 8px;
        color: #FFFFFF;
        font-size: 1.6rem;
        font-weight: 900;
        letter-spacing: 0.04em;
        padding: 16px 20px;
        margin-bottom: 12px;
    }
    .field-banner {
        display: flex;
        gap: 28px;
        flex-wrap: wrap;
        background: #0B0F19;
        border: 2px solid #00FFA3;
        border-radius: 8px;
        padding: 14px 20px;
        margin-bottom: 10px;
    }
    .field-label {
        display: block;
        color: #9AA4B2;
        font-size: 0.72rem;
        letter-spacing: 0.09em;
        text-transform: uppercase;
    }
    .field-value {
        display: block;
        color: #FFFFFF;
        font-size: 1.15rem;
        font-weight: 800;
    }
    .beacon-box {
        border: 2px solid #F5A623;
        border-radius: 8px;
        background: rgba(245, 166, 35, 0.10);
        color: #F5A623;
        font-weight: 700;
        padding: 12px 18px;
        margin: 10px 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
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

st.sidebar.divider()
selected_view = st.sidebar.radio("Command view", NAV_OPTIONS, key="nav_selection")

incident = st.session_state.incident_store[st.session_state.active_incident_id]
elapsed_seconds = (datetime.datetime.now() - incident["start_time"]).total_seconds()
accumulated_burn = elapsed_seconds * incident["burn_rate_sec"] if incident["status"] != "RESOLVED" else 0.0

if selected_view in ROUTE_TO_GM:
    render_gm_docket(incident, st.session_state["selected_book"], ROUTE_TO_GM[selected_view])
    st.stop()

if selected_view == NAV_OPTIONS[5]:
    render_tier_3(incident, st.session_state["selected_book"])
    st.stop()

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

if selected_view == NAV_OPTIONS[1]:
    render_tier_2(incident, st.session_state["selected_book"])
    st.stop()

if selected_view == NAV_OPTIONS[6]:
    render_tier_4(incident, st.session_state["selected_book"])
    render_remedial_engine(incident)
    st.stop()

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

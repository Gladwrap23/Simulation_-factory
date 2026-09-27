import datetime
import hashlib
import json

import streamlit as st

st.set_page_config(
    page_title="Sovereign Evidentiary Management System",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    /* Force iPad Safari momentum scrolling across sidebar and dropdowns */
    section[data-testid="stSidebar"] {
        overflow-y: scroll !important;
        -webkit-overflow-scrolling: touch !important;
        max-height: 100vh !important;
    }
    div[data-baseweb="select"] {
        max-height: 400px !important;
    }
    div[role="listbox"] {
        max-height: 320px !important;
        overflow-y: auto !important;
        -webkit-overflow-scrolling: touch !important;
    }

    /* Expand the popover menu height so all clients are visible */
    div[data-baseweb="popover"],
    div[data-baseweb="popover"] > div,
    ul[role="listbox"] {
        max-height: 650px !important;
        height: auto !important;
        overflow-y: auto !important;
        -webkit-overflow-scrolling: touch !important;
    }

    /* Make each client row taller and easier to tap with a finger */
    li[role="option"] {
        padding-top: 14px !important;
        padding-bottom: 14px !important;
        font-size: 15px !important;
        line-height: 1.4 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

CLIENT_PROFILES = {
    "🇺🇸 USA | Amazon Freight (I-45 Corridor)": {
        "sector": "Autonomous Class 8 Haulage",
        "docket_id": "US-FMCSA-AMZN-I45",
        "jurisdiction": "US_DE",
        "burn_rate_daily": 450_000.00,
        "currency": "USD",
        "target_entity": "NHTSA SGO / Commercial Van Carrier",
    },
    "🇩🇪 GER | TenneT / EnBW (North Sea Offshore)": {
        "sector": "Offshore HVDC Grid Transmission",
        "docket_id": "DE-BNetzA-TENNET-OW",
        "jurisdiction": "DE_BW",
        "burn_rate_daily": 454_000.00,
        "currency": "EUR",
        "target_entity": "TenneT TSO B.V. & Offshore Wind Syndicate",
    },
    "🇬🇧 GBR | Zenobē / National Grid (Scotland BESS)": {
        "sector": "Grid-Scale Transmission BESS",
        "docket_id": "UK-TCC-ZENOBE-BESS",
        "jurisdiction": "UK_ENG",
        "burn_rate_daily": 320_000.00,
        "currency": "GBP",
        "target_entity": "National Grid Electricity System Operator (ESO)",
    },
    "🇯🇵 JPN | Toyota / Japan Post (Tokyo Drone Hub)": {
        "sector": "Autonomous Postal Drone / Last-Mile",
        "docket_id": "JP-MLIT-TOYOTA-BVLOS",
        "jurisdiction": "JP_TYO",
        "burn_rate_daily": 58_000_000.00,
        "currency": "JPY",
        "target_entity": "MLIT Civil Aviation Bureau & East Japan Railway",
    },
    "🇨🇱 CHL | Enel Chile / SQM (Atacama BESS)": {
        "sector": "High-Altitude Lithium BESS Microgrid",
        "docket_id": "CL-SEC-ENEL-ATACAMA",
        "jurisdiction": "CL_STGO",
        "burn_rate_daily": 620_000.00,
        "currency": "USD",
        "target_entity": "Coordinador Eléctrico Nacional (CEN) & Interconnector",
    },
}

CURRENT_USER = {
    "name": "Marcus Vance",
    "role": "Field PE",
    "authorized_dockets": ["ALL"],
}

JURISDICTION_REGISTRY = {
    "US_DE": {
        "country": "United States (Delaware / Federal)",
        "court": "Delaware Court of Chancery / Federal District Court",
        "currency_code": "USD",
        "currency_symbol": "$",
        "language_name": "English (en-US)",
        "statutory_schema": "Delaware Uniform Rules of Evidence / FRE 902(14)",
        "metrology": "NIST (National Institute of Standards and Technology)",
        "statute_evidence": "FRE 902(14) / FRCP Rule 37(e) Litigation Hold",
        "fiduciary_shield": "DGCL § 141(e) Reliance Protection",
        "banking_cutoff": "14:00 EST (Fedwire / CHIPS)",
        "oath_text": "I declare under penalty of perjury under the laws of the United States of America that the foregoing is true and correct.",
    },
    "US_CA": {
        "country": "United States (California / 9th Cir.)",
        "court": "California Superior Court / N.D. Cal",
        "currency_code": "USD",
        "currency_symbol": "$",
        "language_name": "English (en-US)",
        "statutory_schema": "California Evidence Code §§ 1552, 1553",
        "metrology": "NIST Traceable / CAL FIRE Calibration Enclave",
        "statute_evidence": "CEC § 1552 / CPUC Fire Safety Order Rule 20",
        "fiduciary_shield": "Cal. Corp. Code § 309 Good Faith Reliance",
        "banking_cutoff": "14:00 PST (Fedwire Escrow Desk)",
        "oath_text": "I certify under penalty of perjury under the laws of the State of California that the foregoing is true and correct.",
    },
    "DE_BW": {
        "country": "Germany (Baden-Württemberg / Federal)",
        "court": "Landgericht Stuttgart (Commercial Chamber)",
        "currency_code": "EUR",
        "currency_symbol": "€",
        "language_name": "German (de-DE / Amtssprache)",
        "statutory_schema": "ZPO § 184 (Gerichtssprache Deutsch) / ZPO § 371",
        "metrology": "PTB (Physikalisch-Technische Bundesanstalt)",
        "statute_evidence": "ZPO §§ 371, 416a / ZPO § 485 Beweisverfahren",
        "fiduciary_shield": "AktG § 93 Business Judgment Rule",
        "banking_cutoff": "14:00 CET (TARGET2 / Bundesbank)",
        "oath_text": "Ich versichere an Eides statt unter Bezugnahme auf StGB § 156, dass die vorstehenden Messungen unverändert sind.",
    },
    "UK_ENG": {
        "country": "United Kingdom (England & Wales)",
        "court": "High Court of Justice (Technology & Construction Court)",
        "currency_code": "GBP",
        "currency_symbol": "£",
        "language_name": "English (en-GB)",
        "statutory_schema": "Civil Procedure Rules (CPR Part 22 & Part 35)",
        "metrology": "NPL (National Physical Laboratory)",
        "statute_evidence": "Civil Evidence Act 1995 (s. 8/9) / CPR Part 31",
        "fiduciary_shield": "Companies Act 2006 s. 172 Director Safe Harbor",
        "banking_cutoff": "16:00 GMT (CHAPS / Bank of England)",
        "oath_text": "I believe that the facts stated in this witness statement are true. I understand that proceedings for contempt of court may be brought against anyone who makes a false statement.",
    },
    "JP_TYO": {
        "country": "Japan (Tokyo / National)",
        "court": "Tokyo District Court",
        "currency_code": "JPY",
        "currency_symbol": "¥",
        "language_name": "Japanese (ja-JP)",
        "statutory_schema": "Code of Civil Procedure of Japan",
        "metrology": "National Metrology Institute of Japan (NMIJ)",
        "statute_evidence": "Code of Civil Procedure (documentary and expert evidence)",
        "fiduciary_shield": "Companies Act of Japan (directors' duties)",
        "banking_cutoff": "15:00 JST (BOJ-NET / Zengin)",
        "oath_text": "I certify that this record accurately reflects the technical observations captured.",
    },
    "CL_STGO": {
        "country": "Chile (Santiago / National)",
        "court": "Santiago Civil Courts",
        "currency_code": "CLP",
        "currency_symbol": "CLP $",
        "language_name": "Spanish (es-CL)",
        "statutory_schema": "Código de Procedimiento Civil de Chile",
        "metrology": "Instituto Nacional de Normalización (INN)",
        "statute_evidence": "Código de Procedimiento Civil (documentary and expert evidence)",
        "fiduciary_shield": "Ley de Sociedades Anónimas (directors' duties)",
        "banking_cutoff": "14:00 CLT (Sistema LBTR / Banco Central de Chile)",
        "oath_text": "Certifico que este registro refleja fielmente las observaciones técnicas capturadas.",
    },
}

CURRENCY_SYMBOLS = {
    "USD": "$",
    "EUR": "€",
    "GBP": "£",
    "JPY": "¥",
    "CLP": "CLP $",
}

authorized_client_name = next(
    iter(CLIENT_PROFILES)
) if "ALL" in CURRENT_USER["authorized_dockets"] else next(
    (
        client_name
        for client_name, client_profile in CLIENT_PROFILES.items()
        if client_profile["docket_id"] in CURRENT_USER["authorized_dockets"]
    ),
    None,
)
if authorized_client_name is None:
    raise ValueError("Configured user has no authorized client profile.")

requested_docket = st.query_params.get("docket")
if requested_docket and requested_docket != st.session_state.get("last_magic_link_docket"):
    matching_client = next(
        (
            client_name
            for client_name, client_profile in CLIENT_PROFILES.items()
            if client_profile["docket_id"] == requested_docket
        ),
        None,
    )
    if matching_client is not None:
        st.session_state.selected_client = matching_client
        st.session_state.last_magic_link_docket = requested_docket

if st.session_state.pop("return_to_authorized", False):
    st.session_state.selected_client = authorized_client_name

if st.session_state.get("selected_client") not in CLIENT_PROFILES:
    st.session_state.selected_client = next(iter(CLIENT_PROFILES))

st.sidebar.title("Sovereign Node Command")
selected_client_name = st.sidebar.selectbox(
    "Active Account / Sector Docket",
    list(CLIENT_PROFILES.keys()),
    key="selected_client",
)
profile = dict(CLIENT_PROFILES[selected_client_name])

if (
    "ALL" not in CURRENT_USER["authorized_dockets"]
    and profile["docket_id"] not in CURRENT_USER["authorized_dockets"]
):
    st.error("🛑 ACCESS RESTRICTED: SOVEREIGN JURISDICTIONAL ISOLATION")
    st.markdown(
        f"""
### Enclave Security Alert: Unauthorized Docket Access
**Authenticated Identity:** `{CURRENT_USER['name']}` ({CURRENT_USER['role']})  
**Authorized Partition:** `{CURRENT_USER['authorized_dockets'][0]}`  
**Target Requested Partition:** `{profile['docket_id']}` ({profile['sector']})

---

#### Statutory Safeguards Enacted:
* **Zero Decryption:** Telemetry feeds, trade secrets, and banking targets remain cryptographically sealed.
* **Protective Shield:** Access blocked pursuant to **FRE Rule 26(c)** protective orders and **GeschGehG § 4**.
* **Immutable Audit:** Event signature anchored to sovereign ledger and flagged for Vault Monitor.
"""
    )

    if st.button(
        f"➔ Return to Authorized Workstation ({CLIENT_PROFILES[authorized_client_name]['docket_id']})",
        type="primary",
    ):
        st.session_state.selected_client = authorized_client_name
        st.rerun()

    st.stop()

jurisdiction = JURISDICTION_REGISTRY[profile["jurisdiction"]]
profile.setdefault("standard", profile["sector"])
profile.setdefault("instrument", "Configured sector telemetry instrumentation")
profile.setdefault("work_order", f"WO-{profile['docket_id']}")
profile.setdefault("certifier_title", f"{CURRENT_USER['name']} ({CURRENT_USER['role']})")
currency_code = profile["currency"]
currency_symbol = CURRENCY_SYMBOLS[currency_code]

if "sector_dockets" not in st.session_state:
    st.session_state.sector_dockets = {}

active_docket_id = profile["docket_id"]
if active_docket_id not in st.session_state.sector_dockets:
    st.session_state.sector_dockets[active_docket_id] = {
        "stage": 1,
        "wo_scope": f"Statutory inspection and calibration for {profile['standard']}.",
        "field_telemetry_hash": None,
        "pe_signed_by": None,
        "ops_countersigned_by": None,
        "legal_cleared_by": None,
        "dual_key_chairman": False,
        "dual_key_clo": False,
    }

active_docket = st.session_state.sector_dockets[active_docket_id]
dossier_stage = active_docket["stage"]


def advance_active_stage(target_stage: int) -> None:
    if target_stage > active_docket["stage"]:
        active_docket["stage"] = target_stage

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Docket ID:** `{profile['docket_id']}`")
st.sidebar.markdown(f"**Jurisdiction:** {jurisdiction['country']}")
col_meta1, col_meta2 = st.sidebar.columns(2)
col_meta1.markdown(
    f"**Currency:**\n\n`{currency_code} ({currency_symbol})`"
)
col_meta2.markdown(f"**Court Language:**\n\n`{jurisdiction['language_name']}`")
st.sidebar.markdown(f"**Target Court:** {jurisdiction['court']}")
st.sidebar.markdown(f"**Metrology Body:** {jurisdiction['metrology']}")
st.sidebar.markdown(f"**Statutory Evidence:** `{jurisdiction['statute_evidence']}`")
st.sidebar.markdown(f"**Banking Cutoff:** :red[{jurisdiction['banking_cutoff']}]")
st.sidebar.markdown(
    f"**Daily Burn Rate:** :red[{currency_symbol}{profile['burn_rate_daily']:,.2f} / day]"
)

PAGES = [
    "Tier 1: Sovereign Executive Overview",
    "Tier 3A: Operations Dispatch Command",
    "Tier 3B: Work-Face Attestation Desk",
    "Tier 3A: Operations Verification Desk",
    "Legal Chambers: Evidentiary Audit",
    "Tier 4: Executive Vault & Filing (Always Active)",
]

target_page = st.session_state.get("target_page")
if target_page in PAGES:
    st.session_state.nav_radio = target_page
    st.session_state.target_page = None
elif "target_page" in st.session_state:
    st.session_state.target_page = None

if st.session_state.get("nav_radio") not in PAGES:
    st.session_state.nav_radio = PAGES[0]


def navigate_to(page_name: str) -> None:
    if page_name not in PAGES:
        raise ValueError(f"Unknown workstation page: {page_name}")
    st.session_state.target_page = page_name
    st.rerun()

nav_selection = st.sidebar.radio(
    "Workstation Navigation",
    PAGES,
    key="nav_radio",
)

if nav_selection == "Tier 1: Sovereign Executive Overview":
    st.title("Tier 1: Sovereign Executive Command")
    st.caption("Real-Time Liquidity Exposure, Burn Mitigation & Litigation Readiness")

    c1, c2, c3 = st.columns(3)
    c1.metric(
        f"Accrued Holding Burn ({currency_code})",
        f"{currency_symbol}{(profile['burn_rate_daily'] / 24 * 4.2):,.2f}",
        f"+{currency_symbol}48.20/sec",
    )
    c2.metric(
        f"Letter of Credit At Risk ({currency_code})",
        f"{currency_symbol}15,000,000.00",
        f"Freeze Deadline: {jurisdiction['banking_cutoff'].split()[0]}",
    )
    c3.metric("Dossier Lifecycle Status", f"Stage {dossier_stage} of 5")

    st.markdown("---")
    st.subheader("Adversarial Red Team Pre-Emption Briefing")
    st.info(
        f"**Target Counterparty:** {profile['target_entity']}\n\n"
        f"**Forum Precedent Risk:** Delaware Chancery & Landgericht commercial divisions dismiss monetary-only claims "
        f"unless irreparable system damage and continuous metric logging are demonstrated on Day 1. "
        f"Stage 2 (Field Attestation) must anchor telemetry to {jurisdiction['metrology']} calibration."
    )

    st.subheader("Evidentiary Pipeline Command (Tap to Navigate)")

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        if st.button("1. Ops Dispatch\n(Tier 3A)", use_container_width=True):
            navigate_to("Tier 3A: Operations Dispatch Command")

    with c2:
        if st.button("2. Field Attestation\n(Tier 3B)", use_container_width=True):
            navigate_to("Tier 3B: Work-Face Attestation Desk")

    with c3:
        if st.button("3. Ops Verification\n(Tier 3A)", use_container_width=True):
            navigate_to("Tier 3A: Operations Verification Desk")

    with c4:
        if st.button("4. Chambers Audit\n(Legal)", use_container_width=True):
            navigate_to("Legal Chambers: Evidentiary Audit")

    with c5:
        if st.button("5. Executive Vault\n(Tier 4)", use_container_width=True):
            navigate_to("Tier 4: Executive Vault & Filing (Always Active)")

elif nav_selection == "Tier 3A: Operations Dispatch Command":
    st.title("Tier 3A: Engineering Operations Dispatch")
    st.caption("Formal Issuance of Statutory Work Orders")

    st.markdown(f"**Work Order ID:** `{profile['work_order']}`")
    st.markdown(f"**Governing Metric:** `{profile['standard']}`")
    st.markdown(f"**Assigned Instrument:** `{profile['instrument']}`")

    wo_text = st.text_area(
        "Technical Scope & Statutory Directives",
        value=active_docket["wo_scope"],
        height=150,
    )

    if dossier_stage == 1:
        if st.button(
            "Transmit Work Order to Site Desk (Tier 3B)",
            type="primary",
            use_container_width=True,
        ):
            active_docket["wo_scope"] = wo_text
            advance_active_stage(2)
            navigate_to("Tier 3B: Work-Face Attestation Desk")
    else:
        st.success(f"Work Order dispatched. Current lifecycle is at Stage {dossier_stage}.")
        if st.button(
            "➔ Proceed to Tier 3B: Work-Face Attestation Desk",
            type="primary",
            use_container_width=True,
        ):
            navigate_to("Tier 3B: Work-Face Attestation Desk")

elif nav_selection == "Tier 3B: Work-Face Attestation Desk":
    st.title("Tier 3B: Work-Face Attestation Desk")
    st.caption("Physical Calibration, Telemetry Ingestion & PE Statutory Seal")

    st.markdown(f"**Active Work Order:** `{profile['work_order']}`")
    st.markdown(f"**Assigned Certifying Witness:** `{profile['certifier_title']}`")

    st.markdown("#### Step 1: Physical Zero-Drift & Sensor Calibration")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Metrology Calibration Token (NIST Traceable)**")
        st.code("NIST-CAL-99120-PASS", language="text")
    with c2:
        st.markdown("**Zero-Drift Variance (Pre-Test Audit)**")
        st.success("0.0002% — WITHIN STATUTORY TOLERANCE (< 0.01%)")

    st.markdown("#### Step 2: Telemetry Capture & Oscillography Stream")
    sample_payload = {
        "docket": profile["docket_id"],
        "standard": profile["standard"],
        "metric_violation": "4.12% Total Harmonic Distortion (Threshold 3.0%)",
        "hardware_sn": "FLK-1777-B9921",
        "sample_rate": "10 kHz continuous",
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }
    st.json(sample_payload)

    st.markdown("#### Step 3: Statutory Witness Oath")
    st.warning(f"**Statutory Oath:** {jurisdiction['oath_text']}")

    if dossier_stage < 2:
        st.error("Work Order pending dispatch from Tier 3A.")
        if st.button(
            "⚡ Fast-Track Dispatch & Unlock Signing Desk",
            type="primary",
            use_container_width=True,
        ):
            advance_active_stage(2)
            navigate_to("Tier 3B: Work-Face Attestation Desk")
    elif dossier_stage == 2:
        if st.button(
            f"Affix Statutory Seal ({profile['certifier_title']})",
            type="primary",
            use_container_width=True,
        ):
            raw_hash = hashlib.sha256(json.dumps(sample_payload).encode()).hexdigest()
            active_docket["field_telemetry_hash"] = raw_hash
            active_docket["pe_signed_by"] = profile["certifier_title"]
            advance_active_stage(3)
            navigate_to("Tier 3A: Operations Verification Desk")
    else:
        st.success(f"Attestation completed by {active_docket['pe_signed_by']}.")
        st.code(f"Hash: {active_docket['field_telemetry_hash']}")
        if st.button(
            "➔ Proceed to Tier 3A: Operations Verification",
            type="primary",
            use_container_width=True,
        ):
            navigate_to("Tier 3A: Operations Verification Desk")

elif nav_selection == "Tier 3A: Operations Verification Desk":
    st.title("Tier 3A: Operations Verification & Audit")
    st.caption("Verification of Methodological Integrity Prior to Legal Review")

    if dossier_stage < 3:
        st.info("Awaiting completion of Tier 3B physical field attestation.")
    else:
        st.markdown(f"**Verified Telemetry Hash:** `{active_docket['field_telemetry_hash']}`")
        st.markdown(f"**Field Witness:** `{active_docket['pe_signed_by']}`")

        c1, c2 = st.columns(2)
        c1.checkbox("Confirm 48-Hour Prior Notice of Test was Served", value=True, disabled=True)
        c2.checkbox("Confirm Calibration Certificate Traceable to " + jurisdiction["metrology"], value=True, disabled=True)

        if dossier_stage == 3:
            if st.button(
                "Countersign Manifest & Transmit to Legal Chambers",
                type="primary",
                use_container_width=True,
            ):
                active_docket["ops_countersigned_by"] = "VP Operations / Sarah Jenkins"
                advance_active_stage(4)
                navigate_to("Legal Chambers: Evidentiary Audit")
        else:
            st.success(f"Countersigned by {active_docket['ops_countersigned_by']}.")
            if st.button(
                "➔ Proceed to Legal Chambers Audit",
                type="primary",
                use_container_width=True,
            ):
                navigate_to("Legal Chambers: Evidentiary Audit")

elif nav_selection == "Legal Chambers: Evidentiary Audit":
    st.title("Legal Chambers: Trial Admissibility Clearance")
    st.caption("FRE / ZPO Gap Analysis, Anti-Spoliation Directive & Red-Team Audit")

    if dossier_stage < 4:
        st.info("Awaiting Operations verification before initiating legal chambers review.")
    else:
        st.subheader("Admissibility Gap Analysis")
        st.markdown(f"**Governing Rule:** `{jurisdiction['statute_evidence']}`")
        st.markdown(f"**Fiduciary Safe Harbor:** `{jurisdiction['fiduciary_shield']}`")

        st.success(
            "✓ Metrology chain of custody complete.\n\n"
            "✓ Self-authenticating electronic record meets FRE 902(14) / ZPO § 371 requirements.\n\n"
            "✓ Anti-spoliation litigation hold ready for simultaneous service."
        )

        if dossier_stage == 4:
            if st.button(
                "Clear Dossier & Issue Litigation Hold to Tier 4 Vault",
                type="primary",
                use_container_width=True,
            ):
                active_docket["legal_cleared_by"] = "Katherine Ross, Lead Trial Counsel"
                advance_active_stage(5)
                navigate_to("Tier 4: Executive Vault & Filing (Always Active)")
        else:
            st.success(f"Cleared for trial filing by {active_docket['legal_cleared_by']}.")
            if st.button(
                "➔ Open Tier 4 Executive Vault",
                type="primary",
                use_container_width=True,
            ):
                navigate_to("Tier 4: Executive Vault & Filing (Always Active)")

elif nav_selection == "Tier 4: Executive Vault & Filing (Always Active)":
    st.title("Tier 4: Executive Vault & Subpoena-Proof Filing")
    st.caption("Dual-Key Fiduciary Ratification & Global Banking Drawstop")

    st.subheader("Live Evidentiary Dossier Status")
    e1, e2, e3, e4 = st.columns(4)
    e1.markdown("**Exhibit A**\n\n*Incident Brief*")
    e1.success("READY")

    e2.markdown("**Exhibit B**\n\n*Telemetry Affidavit*")
    if active_docket["pe_signed_by"]:
        e2.success("SEALED")
        e2.caption(f"**Witness:** {active_docket['pe_signed_by']}")
    else:
        e2.warning("Awaiting Tier 3B")
        e2.caption("Pending Field PE/Chief")

    e3.markdown("**Exhibit C**\n\n*FRE/ZPO Certificate*")
    if active_docket["legal_cleared_by"]:
        e3.success("CERTIFIED")
    else:
        e3.warning("Awaiting Chambers")

    e4.markdown("**Exhibit D**\n\n*Fiduciary Memo*")
    if dossier_stage == 5:
        e4.success("COMPILED")
    else:
        e4.info("Drafting...")

    st.markdown("---")
    st.subheader("Dual-Key Release Authorization")
    st.markdown(f"**Target Issuing Bank / Clearing Agency:** `{jurisdiction['banking_cutoff']}`")

    c1, c2 = st.columns(2)
    key_chairman = c1.checkbox(
        "Key 1: Executive Chairman Ratification (DGCL § 141(e) Reliance)",
        value=active_docket["dual_key_chairman"],
        disabled=(dossier_stage < 5),
        key=f"{active_docket_id}_dual_key_chairman",
    )
    key_clo = c2.checkbox(
        "Key 2: Chief Legal Officer Filing Clearance",
        value=active_docket["dual_key_clo"],
        disabled=(dossier_stage < 5),
        key=f"{active_docket_id}_dual_key_clo",
    )

    active_docket["dual_key_chairman"] = key_chairman
    active_docket["dual_key_clo"] = key_clo

    if dossier_stage < 5:
        st.warning("Dual-key execution is locked until Stages 1 through 4 are certified.")
    else:
        if key_chairman and key_clo:
            st.success("DUAL KEYS VERIFIED: Sovereign Filing Authority Unlocked.")
            if st.button("EXECUTE EMERGENCY FILING & WIRE FREEZE NOTICE", type="primary"):
                st.balloons()
                st.success(
                    f"DOCKET FILED BEFORE LUNCHTIME.\n\n"
                    f"Notice of Claim served on {profile['target_entity']}.\n\n"
                    f"Letter of Credit drawstop transmitted to escrow bank prior to {jurisdiction['banking_cutoff']} cutoff."
                )
        else:
            st.info("Both Executive Chairman and Chief Legal Officer must turn their keys to execute filing.")

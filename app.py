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

CLIENT_PROFILES = {
    "BESS / Grid Storage (Apex Clean Energy | ERCOT § 4.2)": {
        "sector": "BESS / Power Quality",
        "docket_id": "US-TX-ERCOT-BESS-01",
        "jurisdiction": "US_DE",
        "burn_rate_daily": 2_070_671.19,
        "standard": "IEEE 2800-2022 / ERCOT § 4.2",
        "instrument": "Fluke 1777 Power Quality Analyzer (Cal: NIST-FLK-8812)",
        "work_order": "WO-8821-HARMONIC",
        "certifier_title": "Marcus Vance, PE (TX #114902)",
        "target_entity": "ERCOT / Interconnection Utility & Standby LC Desk",
    },
    "Offshore Wind (EnBW / TenneT | VDE-AR-N 4130)": {
        "sector": "Offshore Wind Transmission",
        "docket_id": "DE-HB-TENNET-OW-04",
        "jurisdiction": "DE_BW",
        "burn_rate_daily": 454_000.00,
        "standard": "VDE-AR-N 4130 / BNetzA EnWG",
        "instrument": "Omicron CMC 356 + PTB Zero-Drift Calibration Check",
        "work_order": "WO-4409-SUBSTATION",
        "certifier_title": "Dr.-Ing. K. Meissner (Ingenieurkammer #88412)",
        "target_entity": "TenneT TSO B.V. & Deutsche Bundesbank TARGET2",
    },
    "Autonomous Fleet Logistics (Amazon Freight | I-45 Corridor)": {
        "sector": "Autonomous Heavy Transport",
        "docket_id": "US-FED-FMCSA-AMZN-09",
        "jurisdiction": "US_DE",
        "burn_rate_daily": 450_000.00,
        "standard": "FMCSA Part 396 / SAE J3016 Level 4 / ISO 21448",
        "instrument": "Edge DSSAD Tap + NIST Dual-IMU Gyroscope Vector Log",
        "work_order": "WO-9912-AV-COLLISION",
        "certifier_title": "Senior Systems Safety Engineer, PE",
        "target_entity": "NHTSA SGO Desk / OEM Product Liability Syndicate",
    },
    "Wildfire & Municipal Safety (Consortium Black Box)": {
        "sector": "Emergency Municipal Telemetry",
        "docket_id": "US-CA-CALFIRE-BB-11",
        "jurisdiction": "US_CA",
        "burn_rate_daily": 1_500_000.00,
        "standard": "NFPA 1221 / CPUC Fire Safety Tariff Rule 20",
        "instrument": "Starlink LEO Enclave + Hardened RAWS Station Telemetry",
        "work_order": "WO-7731-FIRE-PSPS",
        "certifier_title": "Battalion Chief / Forensic Fire Investigator",
        "target_entity": "Investor-Owned Utility (IOU) / Reinsurance Treaty",
    },
    "Autonomous Drone Postal (Wing / Zipline BVLOS Fleet)": {
        "sector": "Autonomous Air Delivery",
        "docket_id": "US-FAA-BVLOS-DRONE-07",
        "jurisdiction": "US_DE",
        "burn_rate_daily": 385_000.00,
        "standard": "FAA 14 CFR Part 108 / ASTM F38 / ISO 21384",
        "instrument": "High-Frequency ESC Current Logger + RTK-GNSS Spoof Enclave",
        "work_order": "WO-5510-DRONE-DESYNC",
        "certifier_title": "Director of Flight Operations (Part 108 § 108.35)",
        "target_entity": "FAA FSDO / OEM Autopilot Avionics Insurer",
    },
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
}

st.sidebar.title("Sovereign Node Command")
selected_client_name = st.sidebar.selectbox("Active Account / Sector Docket", list(CLIENT_PROFILES.keys()))
profile = CLIENT_PROFILES[selected_client_name]
jurisdiction = JURISDICTION_REGISTRY[profile["jurisdiction"]]

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
    f"**Currency:**\n\n`{jurisdiction['currency_code']} ({jurisdiction['currency_symbol']})`"
)
col_meta2.markdown(f"**Court Language:**\n\n`{jurisdiction['language_name']}`")
st.sidebar.markdown(f"**Target Court:** {jurisdiction['court']}")
st.sidebar.markdown(f"**Metrology Body:** {jurisdiction['metrology']}")
st.sidebar.markdown(f"**Statutory Evidence:** `{jurisdiction['statute_evidence']}`")
st.sidebar.markdown(f"**Banking Cutoff:** :red[{jurisdiction['banking_cutoff']}]")
st.sidebar.markdown(
    f"**Daily Burn Rate:** :red[{jurisdiction['currency_symbol']}{profile['burn_rate_daily']:,.2f} / day]"
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
    currency_symbol = jurisdiction["currency_symbol"]
    currency_code = jurisdiction["currency_code"]
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

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
        "sector": "Autonomous Class 8 Logistics",
        "docket_id": "US-FMCSA-AMZN-I45",
        "jurisdiction": "US_DE",
        "burn_rate_daily": 450_000.00,
        "standard": "FMCSA Part 396 / SAE J3016 Level 4",
        "instrument": "Edge DSSAD Tap + NIST Dual-IMU Vector Logger",
        "work_order": "WO-9912-AV-COLLISION",
        "certifier_title": "Senior Systems Safety Engineer, PE",
        "target_entity": "NHTSA SGO Desk / Commercial Van Carrier",
    },
    "🇩🇪 GER | TenneT / EnBW (North Sea Offshore)": {
        "sector": "Offshore HVDC Grid Transmission",
        "docket_id": "DE-BNetzA-TENNET-OW",
        "jurisdiction": "DE_BW",
        "burn_rate_daily": 454_000.00,
        "standard": "VDE-AR-N 4130 / BNetzA EnWG § 17e",
        "instrument": "Omicron CMC 356 + PTB Zero-Drift Calibration Check",
        "work_order": "WO-4409-SUBSTATION",
        "certifier_title": "Dr.-Ing. K. Meissner (Ingenieurkammer #88412)",
        "target_entity": "TenneT TSO B.V. & Offshore Wind Syndicate",
    },
    "🇬🇧 GBR | Zenobē / National Grid (Scotland BESS)": {
        "sector": "Grid-Scale Transmission BESS",
        "docket_id": "UK-TCC-ZENOBE-BESS",
        "jurisdiction": "UK_ENG",
        "burn_rate_daily": 320_000.00,
        "standard": "Grid Code CC.6.3.7 / IEEE 2800 / CPR 35",
        "instrument": "Yokogawa WT5000 + NPL Dynamic Frequency Timestamp",
        "work_order": "WO-3301-DYNAMIC-FREQ",
        "certifier_title": "Principal Electrical Engineer, CEng MIEE",
        "target_entity": "National Grid Electricity System Operator (ESO)",
    },
    "🇯🇵 JPN | Toyota / Japan Post (Tokyo Drone Hub)": {
        "sector": "Autonomous Last-Mile Logistics",
        "docket_id": "JP-MLIT-TOYOTA-BVLOS",
        "jurisdiction": "JP_TYO",
        "burn_rate_daily": 58_000_000.00,
        "standard": "MLIT Civil Aviation Act Part 108 / ASTM F38",
        "instrument": "RTK-GNSS Spoof Enclave + NMIJ Calibrated ESC Current Logger",
        "work_order": "WO-5510-DRONE-DESYNC",
        "certifier_title": "Director of Autonomous Flight Safety (Part 108)",
        "target_entity": "MLIT Civil Aviation Bureau & East Japan Railway",
    },
    "🇳🇿 NZL | Silver Fern Farms / Maersk (Chilled Export)": {
        "sector": "Perishable Maritime Cold-Chain",
        "docket_id": "NZ-ADMR-SFF-REEFER-01",
        "jurisdiction": "NZ_ADMR",
        "burn_rate_daily": 380_000.00,
        "standard": "ISO 22000 / Codex Alimentarius / Hague-Visby Art. III/IV",
        "instrument": "Cryo-PT100 Sensor Enclave (MSL Calibrated: NZ-17025-TEMP)",
        "work_order": "WO-9942-REEFER-POWER-TRIP",
        "certifier_title": "Lead Marine Cargo Surveyor (IIMS Board Certified)",
        "target_entity": "Ocean Carrier Syndicate / Port Demurrage Desk",
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
        "court": "Delaware Court of Chancery / U.S. District Court",
        "currency_code": "USD",
        "currency_symbol": "$",
        "primary_language": "English (en-US)",
        "language_statute": "Delaware URE / FRE 902(14)",
        "available_languages": ["Official Court (English)", "Executive English Master"],
        "metrology": "NIST (Gaithersburg, MD)",
        "statute_evidence": "FRE 902(14) / FRCP Rule 37(e) Litigation Hold",
        "fiduciary_shield": "DGCL § 141(e) Reliance Protection",
        "banking_cutoff": "14:00 EST (Fedwire / CHIPS)",
        "oath_text": "I declare under penalty of perjury under the laws of the United States that the foregoing is true and correct.",
    },
    "DE_BW": {
        "country": "Germany (Baden-Württemberg / Federal)",
        "court": "Landgericht Stuttgart (Commercial Chamber)",
        "currency_code": "EUR",
        "currency_symbol": "€",
        "primary_language": "German (de-DE)",
        "language_statute": "ZPO § 184 (Gerichtssprache Deutsch)",
        "available_languages": ["Official Court (German)", "Executive English Master"],
        "metrology": "PTB (Physikalisch-Technische Bundesanstalt)",
        "statute_evidence": "ZPO §§ 371, 416a / ZPO § 485 Beweisverfahren",
        "fiduciary_shield": "AktG § 93 Business Judgment Rule",
        "banking_cutoff": "14:00 CET (TARGET2 / Deutsche Bundesbank)",
        "oath_text": "Ich versichere an Eides statt unter Bezugnahme auf StGB § 156, dass die vorstehenden Messungen unverändert sind.",
    },
    "UK_ENG": {
        "country": "United Kingdom (England & Wales)",
        "court": "High Court of Justice (Technology & Construction Court)",
        "currency_code": "GBP",
        "currency_symbol": "£",
        "primary_language": "English (en-GB)",
        "language_statute": "CPR Part 22 & Part 35 (Statement of Truth)",
        "available_languages": ["Official Court (English)", "Executive English Master"],
        "metrology": "NPL (National Physical Laboratory, Teddington)",
        "statute_evidence": "Civil Evidence Act 1995 (ss. 8/9) / CPR Part 31",
        "fiduciary_shield": "Companies Act 2006 s. 172 Director Safe Harbor",
        "banking_cutoff": "16:00 GMT (CHAPS / Bank of England)",
        "oath_text": "I believe that the facts stated in this witness statement are true.",
    },
    "JP_TYO": {
        "country": "Japan (Tokyo Metropolis)",
        "court": "Tokyo District Court (Civil Division 29 - Tech Unit)",
        "currency_code": "JPY",
        "currency_symbol": "¥",
        "primary_language": "Japanese (ja-JP)",
        "language_statute": "Minji Soshōhō Art. 74 (Court Language)",
        "available_languages": ["Official Court (Japanese)", "Executive English Master"],
        "metrology": "NMIJ / AIST (Tsukuba)",
        "statute_evidence": "Minji Soshōhō Art. 228 (Presumption of Authenticity)",
        "fiduciary_shield": "Companies Act Art. 355 Duty of Loyalty",
        "banking_cutoff": "15:00 JST (BOJ-NET / Bank of Japan)",
        "oath_text": "良心に従って真実を述べ、何事も隠さず、偽りのないことを誓います。",
    },
    "NZ_ADMR": {
        "country": "New Zealand (Maritime / Admiralty Jurisdiction)",
        "court": "High Court of New Zealand (Admiralty) / LMAA Arbitration",
        "currency_code": "NZD",
        "currency_symbol": "NZ$",
        "primary_language": "English (en-NZ)",
        "language_statute": "Senior Courts Act 2016 / Admiralty Act 1973",
        "available_languages": ["Official Court (NZ Pleading)", "Executive English Master"],
        "metrology": "MSL (Measurement Standards Laboratory, Lower Hutt)",
        "statute_evidence": "NZ Evidence Act 2006 ss. 137, 148 / Maritime Transport Act 1994",
        "fiduciary_shield": "Companies Act 1993 s. 138 Directors' Reliance",
        "banking_cutoff": "15:00 NZDT (NZClear / RBNZ Escrow)",
        "oath_text": "I solemnly declare and affirm that the biological telemetry logs represent true and unadulterated records traceable to MSL standards.",
    },
}


EXHIBIT_LOCALIZATIONS = {
    "DE_BW": {
        "court_lang_name": "German (Deutsch - de-DE)",
        "court": {
            "exhibit_a_title": "BEWEISSTÜCK A: STATUTARISCHER VORFALLBERICHT",
            "exhibit_a_body": "Am 28. September 2026 um 07:14:22 Uhr registrierte das Enklaven-Messsystem eine unzulässige Netzfrequenzabweichung außerhalb der VDE-AR-N 4130 Toleranzbandbreite.",
            "exhibit_b_title": "BEWEISSTÜCK B: EIDESSTATTLICHE VERSICHERUNG DER TELEMETRIEDATEN",
            "exhibit_b_body": "Unter Bezugnahme auf StGB § 156 versichere ich an Eides statt, dass die vorstehenden Messdaten des Prüfgeräts Omicron CMC 356 unverändert und PTB-rückführbar erfasst wurden.",
            "exhibit_c_title": "BEWEISSTÜCK C: ZPO-GERICHTSZERTIFIKAT",
            "exhibit_c_body": "Gerichtliches Zertifikat zur Wahrung des elektronischen Beweisverfahrens gemäß ZPO §§ 371, 416a zur Vorlage beim Landgericht Stuttgart.",
            "exhibit_d_title": "BEWEISSTÜCK D: COMPLIANCE- UND HAFTUNGSMEMORANDUM",
            "exhibit_d_body": "Feststellung der Einhaltung der organschaftlichen Sorgfaltspflichten gemäß AktG § 93 zur sofortigen Vorlage bei der Bundesbank (TARGET2).",
        },
        "english": {
            "exhibit_a_title": "EXHIBIT A: STATUTORY INCIDENT BRIEF",
            "exhibit_a_body": "On 28 September 2026 at 07:14:22 UTC, the enclave telemetry system registered a severe grid frequency excursion exceeding VDE-AR-N 4130 operating tolerances.",
            "exhibit_b_title": "EXHIBIT B: SWORN TELEMETRY AFFIDAVIT",
            "exhibit_b_body": "Under statutory witness oath, I declare that the foregoing Omicron CMC 356 telemetry logs were ingested without alteration and remain traceable to national PTB standards.",
            "exhibit_c_title": "EXHIBIT C: ADMISSIBILITY CLEARANCE CERTIFICATE",
            "exhibit_c_body": "Electronic evidence admissibility certification issued pursuant to ZPO §§ 371, 416a for commercial court proceedings before Landgericht Stuttgart.",
            "exhibit_d_title": "EXHIBIT D: EXECUTIVE FIDUCIARY MEMORANDUM",
            "exhibit_d_body": "Corporate governance safe harbor memorandum under AktG § 93 Business Judgment Rule for immediate TARGET2 wire freeze execution.",
        },
    },
    "JP_TYO": {
        "court_lang_name": "Japanese (日本語 - ja-JP)",
        "court": {
            "exhibit_a_title": "証拠説明書 甲第1号証：インシデント概要報告書",
            "exhibit_a_body": "2026年9月28日07時14分、自律型配送ドローンにおいてASTM F38基準を超えるアクチュエータ同期異常およびフェイルセーフ作動を検知しました。",
            "exhibit_b_title": "証拠説明書 甲第2号証：テレメトリ電磁的記録宣誓書",
            "exhibit_b_body": "良心に従って真実を述べ、何事も隠さず、偽りのないことを誓います。産業技術総合研究所（NMIJ）計量標準に準拠した記録であることを証明します。",
            "exhibit_c_title": "証拠説明書 甲第3号証：民事訴訟法第228条認証書",
            "exhibit_c_body": "民事訴訟法第74条及び第228条に基づく真正に成立した電磁的記録としての証拠保全完了認証書（東京地方裁判所民事部提出用）。",
            "exhibit_d_title": "証拠説明書 甲第4号証：取締役善管注意義務遵守メモ",
            "exhibit_d_body": "会社法第355条に基づく善管注意義務履行証明書およびBOJ-NET即時資金保全執行指令。",
        },
        "english": {
            "exhibit_a_title": "EXHIBIT A: STATUTORY INCIDENT BRIEF",
            "exhibit_a_body": "On 28 September 2026 at 07:14 UTC, the autonomous delivery drone experienced an actuator desynchronization event exceeding ASTM F38 thresholds.",
            "exhibit_b_title": "EXHIBIT B: SWORN TELEMETRY AFFIDAVIT",
            "exhibit_b_body": "I declare under statutory oath that the flight telemetry records were captured without modification and are traceable to NMIJ/AIST metrology standards.",
            "exhibit_c_title": "EXHIBIT C: ADMISSIBILITY CLEARANCE CERTIFICATE",
            "exhibit_c_body": "Admissibility certification issued pursuant to Code of Civil Procedure Arts. 74 & 228 for immediate filing before the Tokyo District Court.",
            "exhibit_d_title": "EXHIBIT D: EXECUTIVE FIDUCIARY MEMORANDUM",
            "exhibit_d_body": "Corporate fiduciary protection memo under Companies Act Art. 355 for emergency BOJ-NET wire freeze transmission.",
        },
    },
}

UI_STRINGS = {
    "DEFAULT": {
        "vault_title": "Tier 4: Executive Vault & Subpoena-Proof Filing",
        "vault_caption": "Dual-Key Fiduciary Ratification & Global Banking Drawstop",
        "status_title": "Live Evidentiary Dossier Status",
        "ex_a": "Exhibit A",
        "ex_a_sub": "Incident Brief",
        "ex_b": "Exhibit B",
        "ex_b_sub": "Telemetry Affidavit",
        "ex_c": "Exhibit C",
        "ex_c_sub": "Admissibility Certificate",
        "ex_d": "Exhibit D",
        "ex_d_sub": "Fiduciary Memo",
        "badge_ready": "READY",
        "badge_sealed": "SEALED",
        "badge_cert": "CERTIFIED",
        "badge_comp": "COMPILED",
        "badge_awaiting": "AWAITING",
        "badge_draft": "DRAFTING",
        "witness_prefix": "Witness",
        "pending_witness": "Pending field witness",
        "dual_key_title": "Dual-Key Release Authorization",
        "dual_key_bank": "Target Issuing Bank / Clearing Agency",
        "key_1_label": "Key 1: Executive Chairman Ratification",
        "key_2_label": "Key 2: Chief Legal Officer Filing Clearance",
        "keys_locked_msg": "Dual-key execution is locked until stages 1 through 4 are certified.",
        "keys_verified_msg": "DUAL KEYS VERIFIED: Filing authorization unlocked.",
        "exec_btn": "EXECUTE EMERGENCY FILING & WIRE FREEZE NOTICE",
        "filed_banner": "DOCKET FILED",
        "claim_served": "Notice of claim served on",
        "lc_drawstop": "Letter of credit drawstop transmitted before the banking cutoff.",
        "export_title": "Dossier Export Packages",
        "export_caption": "Both packages reference the same sealed telemetry SHA-256 value.",
        "court_btn": "Download Official Court Pleading (EN)",
        "court_btn_sub": "Court-language exhibit bundle for the selected jurisdiction.",
        "master_btn": "Download Executive Master Dossier (EN)",
        "master_btn_sub": "English master bundle for board and executive review.",
    },
    "DE_BW": {
        "vault_title": "Stufe 4: Geschäftsführungs-Tresor und Einreichung",
        "vault_caption": "Treuhänderische Freigabe durch zwei Schlüssel und Zahlungsstopp",
        "status_title": "Aktueller Beweisaktenstatus",
        "ex_a": "Beweisstück A",
        "ex_a_sub": "Vorfallsbericht",
        "ex_b": "Beweisstück B",
        "ex_b_sub": "Telemetrie-Eidesstattliche Versicherung",
        "ex_c": "Beweisstück C",
        "ex_c_sub": "Zulassungszertifikat",
        "ex_d": "Beweisstück D",
        "ex_d_sub": "Organhaftungs-Memorandum",
        "badge_ready": "BEREIT",
        "badge_sealed": "VERSIEGELT",
        "badge_cert": "ZERTIFIZIERT",
        "badge_comp": "ZUSAMMENGESTELLT",
        "badge_awaiting": "AUSSTEHEND",
        "badge_draft": "IN BEARBEITUNG",
        "witness_prefix": "Zeuge/in",
        "pending_witness": "Feldzeuge ausstehend",
        "dual_key_title": "Freigabe durch zwei Schlüssel",
        "dual_key_bank": "Zielbank / Clearingstelle",
        "key_1_label": "Schlüssel 1: Genehmigung durch den Vorstandsvorsitz",
        "key_2_label": "Schlüssel 2: Freigabe durch die Rechtsabteilung",
        "keys_locked_msg": "Zwei-Schlüssel-Freigabe erst nach Zertifizierung der Stufen 1 bis 4 möglich.",
        "keys_verified_msg": "BEIDE SCHLÜSSEL BESTÄTIGT: Einreichung freigegeben.",
        "exec_btn": "NOTFALLEINREICHUNG UND ZAHLUNGSSTOPP AUSFÜHREN",
        "filed_banner": "AKTE EINGEREICHT",
        "claim_served": "Anspruch zugestellt an",
        "lc_drawstop": "Zahlungsstopp vor dem Bankschluss übermittelt.",
        "export_title": "Dossier-Exportpakete",
        "export_caption": "Beide Pakete enthalten denselben versiegelten SHA-256-Telemetriehash.",
        "court_btn": "Amtlichen Schriftsatz herunterladen (DE)",
        "court_btn_sub": "Gerichtssprachliches Beweispaket für die gewählte Gerichtsbarkeit.",
        "master_btn": "Englisches Executive-Dossier herunterladen",
        "master_btn_sub": "Englische Masterfassung für Vorstand und Geschäftsleitung.",
    },
    "JP_TYO": {
        "vault_title": "第4段階：役員保管庫および提出",
        "vault_caption": "二重承認による受託者承認と送金停止",
        "status_title": "証拠記録の現在の状況",
        "ex_a": "証拠A",
        "ex_a_sub": "インシデント概要",
        "ex_b": "証拠B",
        "ex_b_sub": "テレメトリ宣誓書",
        "ex_c": "証拠C",
        "ex_c_sub": "証拠能力認証書",
        "ex_d": "証拠D",
        "ex_d_sub": "取締役責任メモ",
        "badge_ready": "準備完了",
        "badge_sealed": "封印済み",
        "badge_cert": "認証済み",
        "badge_comp": "作成済み",
        "badge_awaiting": "未完了",
        "badge_draft": "作成中",
        "witness_prefix": "証人",
        "pending_witness": "現場証人未登録",
        "dual_key_title": "二重承認による開示許可",
        "dual_key_bank": "送金先銀行 / 決済機関",
        "key_1_label": "鍵1：取締役会議長の承認",
        "key_2_label": "鍵2：最高法務責任者の提出承認",
        "keys_locked_msg": "第1段階から第4段階の認証完了まで、二重承認はロックされています。",
        "keys_verified_msg": "二つの鍵を確認しました：提出が承認されました。",
        "exec_btn": "緊急申立ておよび送金停止通知を実行",
        "filed_banner": "申立てを提出しました",
        "claim_served": "請求通知の送付先：",
        "lc_drawstop": "銀行締切前に信用状の支払停止を通知しました。",
        "export_title": "証拠記録のエクスポート",
        "export_caption": "両方のパッケージに同一の封印済みテレメトリSHA-256値が含まれます。",
        "court_btn": "裁判所提出書類をダウンロード（日本語）",
        "court_btn_sub": "選択された管轄の裁判所提出用証拠パッケージ。",
        "master_btn": "英語版エグゼクティブ記録をダウンロード",
        "master_btn_sub": "取締役会および経営陣向けの英語版マスター記録。",
    },
}
CURRENCY_SYMBOLS = {
    "USD": "$",
    "EUR": "€",
    "GBP": "£",
    "JPY": "¥",
    "NZD": "NZ$",
}
PERMITTED_FINAL_STATES = {
    "READY",
    "SEALED",
    "CERTIFIED",
    "COMPILED",
    "準備完了",
    "封印済み",
    "認証済み",
    "作成済み",
}


def verify_telemetry_integrity(docket_id: str) -> tuple[bool, str]:
    docket = st.session_state.get("sector_dockets", {}).get(docket_id)
    if docket is None:
        return False, "Data Error: Docket state is unavailable."

    raw_telemetry = docket.get("field_telemetry_payload", "")
    recorded_hash = docket.get("field_telemetry_hash", "")
    if not raw_telemetry or not recorded_hash:
        return False, "Data Error: Telemetry log or SHA-256 anchor missing."

    computed_hash = hashlib.sha256(raw_telemetry.encode("utf-8")).hexdigest()
    if computed_hash != recorded_hash:
        return False, "Security Alert: Telemetry payload tamper detected. SHA-256 mismatch."

    return True, "Telemetry payload matches its SHA-256 anchor."


def verify_dossier_integrity(docket_id: str) -> tuple[bool, str]:
    docket = st.session_state.get("sector_dockets", {}).get(docket_id)
    if docket is None:
        return False, "Gating Error: Docket state is unavailable."

    telemetry_intact, telemetry_message = verify_telemetry_integrity(docket_id)
    if not telemetry_intact:
        return False, telemetry_message

    exhibits = {
        "Exhibit A": docket.get("exhibit_a_status"),
        "Exhibit B": docket.get("exhibit_b_status"),
        "Exhibit C": docket.get("exhibit_c_status"),
        "Exhibit D": docket.get("exhibit_d_status"),
    }
    for name, status in exhibits.items():
        if status not in PERMITTED_FINAL_STATES:
            return False, f"Gating Error: {name} is uncertified or invalid ({status})."

    if docket.get("field_telemetry_payload", "").startswith("SIMULATED|"):
        return True, "Simulated dossier integrity verified. Ready for simulated dual-key authorization."
    return True, "Dossier intact. Ready for dual-key authorization."

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


def on_docket_change() -> None:
    st.session_state["nav_radio"] = "Tier 1: Sovereign Executive Overview"
    st.session_state.pop("target_page", None)
    for exhibit_name in ("a", "b", "c", "d"):
        st.session_state.pop(f"exhibit_{exhibit_name}_status", None)


st.sidebar.title("Sovereign Node Command")
selected_client_name = st.sidebar.selectbox(
    "Active Account / Sector Docket",
    list(CLIENT_PROFILES.keys()),
    key="selected_client",
    on_change=on_docket_change,
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
loc_data = EXHIBIT_LOCALIZATIONS.get(profile["jurisdiction"])
currency_code = jurisdiction["currency_code"]
currency_symbol = jurisdiction["currency_symbol"]

if "sector_dockets" not in st.session_state:
    st.session_state.sector_dockets = {}

active_docket_id = profile["docket_id"]
if "simulated_breaches" not in st.session_state:
    st.session_state.simulated_breaches = {}
if active_docket_id not in st.session_state.simulated_breaches:
    st.session_state.simulated_breaches[active_docket_id] = {
        "active": False,
        "fault_type": None,
        "ratchet_level": 0,
        "kinetic_value": "NOMINAL",
        "timestamp_utc": None,
        "key1_signed": False,
        "key2_signed": False,
        "executed": False,
    }
sim_state = st.session_state.simulated_breaches[active_docket_id]
for key in ("key1_signed", "key2_signed", "executed"):
    sim_state.setdefault(key, False)
sim_state.setdefault("telemetry_before_trip", None)
sim_state.setdefault("exhibits_before_trip", None)
sim_state.setdefault("attestation_before_trip", None)

if active_docket_id not in st.session_state.sector_dockets:
    st.session_state.sector_dockets[active_docket_id] = {
        "stage": 4 if sim_state["active"] else 1,
        "wo_scope": f"Statutory calibration and inspection under {profile['standard']}.",
        "field_telemetry_payload": None,
        "field_telemetry_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "pe_signed_by": profile["certifier_title"],
        "cosigned_by": None,
        "witness_signed": False,
        "attestation_hash": None,
        "ops_countersigned_by": None,
        "legal_cleared_by": None,
        "exhibit_a_status": "AWAITING",
        "exhibit_b_status": "AWAITING",
        "exhibit_c_status": "AWAITING",
        "exhibit_d_status": "AWAITING",
        "dual_key_chairman": False,
        "dual_key_clo": False,
        "executed": False,
    }

active_docket = st.session_state.sector_dockets[active_docket_id]
active_docket["pe_signed_by"] = profile["certifier_title"]
active_docket.setdefault("executed", False)
active_docket.setdefault("exhibit_a_status", "READY" if active_docket["stage"] >= 2 else "AWAITING")
active_docket.setdefault("exhibit_b_status", "SEALED" if active_docket["stage"] >= 3 else "AWAITING")
active_docket.setdefault("exhibit_c_status", "READY" if active_docket["stage"] >= 4 else "AWAITING")
active_docket.setdefault("exhibit_d_status", "READY" if active_docket["stage"] >= 5 else "AWAITING")
for exhibit_name in ("a", "b", "c", "d"):
    st.session_state[f"exhibit_{exhibit_name}_status"] = active_docket[f"exhibit_{exhibit_name}_status"]
certifier_witness = profile["certifier_title"]
dossier_stage = active_docket["stage"]


def advance_active_stage(target_stage: int) -> None:
    if target_stage > active_docket["stage"]:
        active_docket["stage"] = target_stage


mobile_mode = st.sidebar.toggle("📱 Emulate iPhone Pocket Terminal", key="pocket_mode")
with st.sidebar.expander("⚡ Adversarial Testing Harness", expanded=True):
    st.caption(f"Target: `{active_docket_id}`")
    trip_col, reset_col = st.columns(2)
    with trip_col:
        if st.button(
            "🚨 Trip Power",
            type="primary",
            use_container_width=True,
            key=f"{active_docket_id}_trip_power",
        ):
            timestamp_utc = datetime.datetime.now(datetime.timezone.utc).strftime(
                "%Y-%m-%d %H:%M:%S UTC"
            )
            if not sim_state["active"]:
                sim_state["telemetry_before_trip"] = (
                    active_docket["field_telemetry_payload"],
                    active_docket["field_telemetry_hash"],
                )
                sim_state["exhibits_before_trip"] = {
                    name: active_docket[f"exhibit_{name}_status"]
                    for name in ("a", "b", "c", "d")
                }
                sim_state["attestation_before_trip"] = (
                    active_docket.get("cosigned_by"),
                    active_docket.get("witness_signed", False),
                    active_docket.get("attestation_hash"),
                )
            sim_state.update(
                active=True,
                fault_type="AUX_POWER_TRIP_0V",
                ratchet_level=2,
                kinetic_value="POWER_TRIP",
                timestamp_utc=timestamp_utc,
                key1_signed=False,
                key2_signed=False,
                executed=False,
            )
            mock_payload = f"SIMULATED|{active_docket_id}|{timestamp_utc}|AUX_POWER_TRIP_0V|0.0V"
            active_docket["field_telemetry_payload"] = mock_payload
            active_docket["field_telemetry_hash"] = hashlib.sha256(
                mock_payload.encode("utf-8")
            ).hexdigest()
            active_docket["cosigned_by"] = f"SIMULATED - {profile['certifier_title']} (unsigned)"
            active_docket["witness_signed"] = False
            active_docket["attestation_hash"] = None
            for name in ("a", "b", "c"):
                active_docket[f"exhibit_{name}_status"] = "CERTIFIED"
            active_docket["exhibit_d_status"] = "COMPILED"
            active_docket["stage"] = 4
            active_docket["executed"] = False
            active_docket["dual_key_chairman"] = False
            active_docket["dual_key_clo"] = False
            st.session_state.target_page = "Tier 4: Executive Vault & Filing (Always Active)"
            st.session_state.pop(f"{active_docket_id}_pocket_key1", None)
            st.session_state.pop(f"{active_docket_id}_pocket_key2", None)
            st.session_state.pop(f"{active_docket_id}_dual_key_chairman", None)
            st.session_state.pop(f"{active_docket_id}_dual_key_clo", None)
            st.rerun()
    with reset_col:
        if st.button(
            "🔄 Reset Dock",
            use_container_width=True,
            key=f"{active_docket_id}_reset_dock",
        ):
            if sim_state["telemetry_before_trip"] is not None:
                (
                    active_docket["field_telemetry_payload"],
                    active_docket["field_telemetry_hash"],
                ) = sim_state["telemetry_before_trip"]
                sim_state["telemetry_before_trip"] = None
            if sim_state["exhibits_before_trip"] is not None:
                for name, status in sim_state["exhibits_before_trip"].items():
                    active_docket[f"exhibit_{name}_status"] = status
                sim_state["exhibits_before_trip"] = None
            if sim_state["attestation_before_trip"] is not None:
                (
                    active_docket["cosigned_by"],
                    active_docket["witness_signed"],
                    active_docket["attestation_hash"],
                ) = sim_state["attestation_before_trip"]
                sim_state["attestation_before_trip"] = None
            sim_state.update(
                active=False,
                fault_type=None,
                ratchet_level=0,
                kinetic_value="NOMINAL",
                timestamp_utc=None,
                key1_signed=False,
                key2_signed=False,
                executed=False,
            )
            active_docket["stage"] = 1
            active_docket["executed"] = False
            active_docket["dual_key_chairman"] = False
            active_docket["dual_key_clo"] = False
            st.session_state.pop(f"{active_docket_id}_pocket_key1", None)
            st.session_state.pop(f"{active_docket_id}_pocket_key2", None)
            st.session_state.pop(f"{active_docket_id}_dual_key_chairman", None)
            st.session_state.pop(f"{active_docket_id}_dual_key_clo", None)
            st.rerun()


def render_legal_ratchet() -> None:
    if not sim_state["active"]:
        return

    jurisdiction_ratchets = {
        "NZ_ADMR": (
            "Biological Spoilage Velocity (Arrhenius Model)",
            "2.42x Acceleration",
            "Core Temp: +3.8°C | RSL: 11 Days Remaining (Contract Spec: 21 Days)",
            "Hague-Visby Art. III(2) Notice of Marine Exception Served",
            "Marine Insurance Act s. 78 Sue & Labour Port Diversion Issued",
            "Admiralty Arrest Petition & Standby LC Drawstop Armed",
        ),
        "DE_BW": (
            "Grid Frequency & Voltage Harmonics (VDE-AR-N 4130)",
            "THD 4.82% (+1.82% Excursion)",
            "Omicron CMC 356 Log: 400kV Busbar Trip | PTB Traceable",
            "ZPO § 371 Self-Authenticating Electronic Hold Filed",
            "ZPO § 485 Independent Evidence Procedure Cleared",
            "AktG § 93 TARGET2 Bundesbank Wire Freeze Armed",
        ),
        "UK_ENG": (
            "Dynamic Frequency Response Loss (Grid Code CC.6.3.7)",
            "RoCoF 1.18 Hz/s Breach",
            "Yokogawa WT5000 Log: Inverter DC Bus Trip | NPL Traceable",
            "CPR Part 31 Statutory Spoliation Warning Transmitted",
            "Section 78 Commercial Loss Mitigation Mandate Issued",
            "High Court TCC Injunction & CHAPS Freeze Armed",
        ),
        "US_DE": (
            "Kinetic Braking & System Disengagement (SAE J3016)",
            "Auxiliary 24V Bus Failure",
            "Edge DSSAD Enclave: Hard MRM Shoulder Stop | NIST Traceable",
            "FRCP Rule 37(e) Formal Anti-Spoliation Directive Served",
            "FMCSA Part 396 Admissibility Affidavit Executed",
            "Delaware Chancery TRO & Fedwire Drawstop Armed",
        ),
        "JP_TYO": (
            "Autonomous Actuator Synchronization (ASTM F38)",
            "ESC Power Rail Dropout",
            "RTK Enclave: Desync Event Logged | NMIJ/AIST Traceable",
            "MLIT Civil Aviation Bureau Part 108 Notice Filed",
            "Minji Soshōhō Art. 228 Forensic Authentication Complete",
            "Tokyo District Court Provisional Attachment & BOJ-NET Freeze",
        ),
    }
    kinetic_title, kinetic_metric, kinetic_detail, level_1, level_2, level_3 = (
        jurisdiction_ratchets[profile["jurisdiction"]]
    )

    st.error(f"🚨 CRITICAL FAULT DETECTED: {sim_state['fault_type']}")
    st.caption(
        f"Injected at {sim_state['timestamp_utc']} · "
        f"Statutory ratchet: Level {sim_state['ratchet_level']} escalation"
    )
    st.markdown(f"**{kinetic_title}:** {kinetic_metric}")
    st.caption(kinetic_detail)
    st.caption(f"Target: {profile['target_entity']}")
    level_1_col, level_2_col, level_3_col = st.columns(3)
    level_1_col.success(f"Level 1 · Preservation\n\n{level_1}")
    level_2_col.warning(f"Level 2 · Mitigation / Reroute\n\n{level_2}")
    level_3_col.error(f"Level 3 · Emergency Drawstop\n\n{level_3}")


st.sidebar.markdown(f"## Docket: `{profile['docket_id']}`")
language_options = jurisdiction["available_languages"]
language_widget_key = "evidentiary_language"
if st.session_state.get(language_widget_key) not in language_options:
    st.session_state[language_widget_key] = language_options[0]


def route_to_executive_overview() -> None:
    if st.session_state[language_widget_key] == "Executive English Master":
        st.session_state["nav_radio"] = "Tier 1: Sovereign Executive Overview"
        st.session_state.pop("target_page", None)


st.sidebar.markdown("---")
st.sidebar.markdown("### 🌐 Evidentiary Language Mode")
lang_mode = st.sidebar.radio(
    "Select Operating Stream:",
    options=language_options,
    index=language_options.index(st.session_state[language_widget_key]),
    key=language_widget_key,
    on_change=route_to_executive_overview,
    label_visibility="collapsed",
)
is_court_native = "Official Court" in lang_mode
is_japanese = is_court_native and profile["jurisdiction"] == "JP_TYO"
is_german_court = is_court_native and profile["jurisdiction"] == "DE_BW"


def localized_text(english: str, german: str, japanese: str) -> str:
    if is_german_court:
        return german
    if is_japanese:
        return japanese
    return english


active_lang_display = (
    loc_data["court_lang_name"]
    if is_court_native and loc_data
    else jurisdiction["primary_language"]
    if is_court_native
    else "English (en-US Master)"
)
st.sidebar.caption(f"Active Filing Stream: **{active_lang_display}**")
c_meta1, c_meta2 = st.sidebar.columns(2)
with c_meta1:
    st.markdown(f"**Currency:**\n\n`{currency_code} ({currency_symbol})`")
with c_meta2:
    st.markdown(f"**Active Mode:**\n\n`{active_lang_display.split()[0]}`")
st.sidebar.markdown("---")

st.sidebar.markdown(f"**Jurisdiction:** {jurisdiction['country']}")
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

if mobile_mode:
    st.subheader("📱 Pocket Edition: Executive Terminal")
    st.caption("Simulated biometric relay and drawstop")
    st.markdown(
        """
        <style>
        .st-key-pocket_terminal {
            width: min(100%, 412px);
            box-sizing: border-box;
            margin: 0 auto 16px;
            background: #05070a;
            border: 4px solid #2d3748;
            border-radius: 48px;
            padding: 20px 16px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7);
            color: #fff;
        }
        .st-key-pocket_terminal [data-testid="stMarkdownContainer"] p {
            color: #e2e8f0;
        }
        .dynamic-island {
            width: 120px;
            height: 28px;
            background: #000;
            border-radius: 20px;
            margin: 0 auto 16px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .ios-card {
            background: #0f172a;
            border: 1px solid #1e293b;
            border-radius: 8px;
            padding: 14px;
            margin-bottom: 12px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    with st.container(key="pocket_terminal"):
        st.markdown(
            f"""
            <div class="dynamic-island">
                <span style="color: {'#ef4444' if sim_state['active'] else '#22c55e'}; font-size: 10px; font-weight: bold;">
                    {'● FAULT ACTIVE' if sim_state['active'] else '● STANDBY NOMINAL'}
                </span>
            </div>
            <div style="display: flex; justify-content: space-between; gap: 8px; margin-bottom: 12px; font-size: 11px;">
                <b>SIMULATED POCKET VAULT</b>
                <span>{jurisdiction['banking_cutoff'].split()[0]} Cutoff</span>
            </div>
            <div class="ios-card" style="border-left: 4px solid {'#ef4444' if sim_state['active'] else '#38bdf8'}; overflow-wrap: anywhere;">
                <div style="font-size: 11px; color: #94a3b8;">ACTIVE DOCKET</div>
                <div style="font-size: 14px; font-weight: 700;">{active_docket_id}</div>
                <div style="font-size: 12px; color: #cbd5e1;">Target: {profile['target_entity']}</div>
            </div>
            <div class="ios-card" style="display: flex; justify-content: space-between; gap: 12px; flex-wrap: wrap;">
                <div>
                    <div style="font-size: 10px; color: #94a3b8;">DAILY CAPITAL EXPOSURE</div>
                    <b style="font-size: 18px; color: #f87171;">{currency_symbol}{profile['burn_rate_daily']:,.0f}</b>
                </div>
                <div>
                    <div style="font-size: 10px; color: #94a3b8;">BANKING DEADLINE</div>
                    <b style="font-size: 14px; color: #fbbf24;">{jurisdiction['banking_cutoff']}</b>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        telemetry_intact, telemetry_message = verify_telemetry_integrity(active_docket_id)
        pocket_enabled = sim_state["active"] and telemetry_intact and not sim_state["executed"]
        pocket_col1, pocket_col2 = st.columns(2)
        with pocket_col1:
            if st.button(
                "🔐 Simulate Face ID: CLO",
                use_container_width=True,
                disabled=not pocket_enabled or sim_state["key1_signed"],
                key=f"{active_docket_id}_pocket_key1",
            ):
                sim_state["key1_signed"] = True
                st.rerun()
        with pocket_col2:
            if st.button(
                "🔐 Simulate Face ID: CFO",
                use_container_width=True,
                disabled=not pocket_enabled or sim_state["key2_signed"],
                key=f"{active_docket_id}_pocket_key2",
            ):
                sim_state["key2_signed"] = True
                st.rerun()
        if not sim_state["active"]:
            st.info("Trip power to start the pocket simulation.")
        elif not telemetry_intact:
            st.warning(telemetry_message)
        elif sim_state["executed"]:
            st.success(f"Simulated drawstop recorded for {profile['target_entity']} in this session.")
        elif sim_state["key1_signed"] and sim_state["key2_signed"]:
            if st.button(
                "⚡ EXECUTE SIMULATED DRAWSTOP",
                type="primary",
                use_container_width=True,
                key=f"{active_docket_id}_pocket_execute",
            ):
                sim_state["executed"] = True
                st.rerun()
        else:
            st.caption("CLO and CFO simulation keys required.")

st.markdown(f"### Active Dossier: `{profile['docket_id']}`")
st.caption(
    f"🏛️ **Filing Venue:** {jurisdiction['court']} | "
    f"**Procedural Authority:** {jurisdiction['language_statute']}"
)
render_legal_ratchet()

if loc_data and is_court_native:
    doc_content = loc_data["court"]
    active_stream_label = f"Official Court Language [{loc_data['court_lang_name']}]"
else:
    doc_content = loc_data["english"] if loc_data else {
        "exhibit_a_title": "EXHIBIT A: INCIDENT BRIEF",
        "exhibit_a_body": "Operational anomaly detected within certified boundaries.",
        "exhibit_b_title": "EXHIBIT B: TELEMETRY AFFIDAVIT",
        "exhibit_b_body": (
            "Witnessed and verified under oath by "
            f"{active_docket['pe_signed_by'] or 'the assigned field witness'}."
        ),
        "exhibit_c_title": "EXHIBIT C: ADMISSIBILITY CERTIFICATE",
        "exhibit_c_body": f"Certified under {jurisdiction['statute_evidence']}.",
        "exhibit_d_title": "EXHIBIT D: FIDUCIARY MEMORANDUM",
        "exhibit_d_body": f"Reliance memo filed prior to {jurisdiction['banking_cutoff']}.",
    }
    active_stream_label = "International English Master [en-US]"

if nav_selection == "Tier 1: Sovereign Executive Overview":
    is_filed = dossier_stage == 5
    if is_filed:
        burn_delta_text = "FROZEN (Drawstop Active)"
        burn_delta_color = "off"
        status_banner = "LITIGATION INITIATED: Holding burn halted under court stay."
    else:
        sec_rate = profile["burn_rate_daily"] / 86_400
        burn_delta_text = f"+{currency_symbol}{sec_rate:,.2f}/sec"
        burn_delta_color = "inverse"
        status_banner = None

    if is_court_native and profile["jurisdiction"] == "DE_BW":
        curr_sym = jurisdiction["currency_symbol"]
        burn_today = profile["burn_rate_daily"] / 24 * 4.2

        st.title("Tier 1: Hoheitliche Exekutivbefehlsstelle")
        st.caption("Echtzeit-Liquiditätsrisiko, Schadensminderung & Prozessvorbereitung")

        col1, col2, col3 = st.columns(3)
        col1.metric(
            "Auflaufender Verzugsschaden (Heute)",
            f"{curr_sym}{burn_today:,.2f}",
            burn_delta_text,
            delta_color=burn_delta_color,
        )
        col2.metric(
            "Gefährdetes Akkreditiv (Standby LC)",
            f"{curr_sym}15.000.000,00",
            f"Fristablauf: {jurisdiction['banking_cutoff']}",
        )
        col3.metric("Dossier-Lebenszyklusstatus", f"Stufe {active_docket['stage']} von 5")
        if status_banner:
            st.success(status_banner)

        st.markdown("---")
        st.subheader("Adversäres Red-Team-Präemptions-Briefing")
        st.info(
            f"**Ziel-Gegenpartei:** {profile['target_entity']}\n\n"
            "**Gerichtliches Präzedenzrisiko:** Die Handelskammern des Landgerichts Stuttgart weisen reine "
            "Schadensersatzklagen zurück, sofern nicht die Unverzüglichkeit und die lückenlose Messintegrität am ersten Tag "
            "im selbständigen Beweisverfahren (§ 485 ZPO) nachgewiesen werden. "
            "Stufe 2 (Beweisaufnahme vor Ort) muss die Telemetriedaten zwingend an Kalibrierzertifikate der "
            f"**{jurisdiction['metrology']}** rückbinden."
        )

        st.subheader("Beweismittel-Prozesssteuerung (Zum Navigieren antippen)")
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            if st.button("1. Einsatzdisposition\n(Tier 3A)", use_container_width=True):
                navigate_to("Tier 3A: Operations Dispatch Command")
        with c2:
            if st.button("2. Technische Beglaubigung\n(Tier 3B)", use_container_width=True):
                navigate_to("Tier 3B: Work-Face Attestation Desk")
        with c3:
            if st.button("3. Betriebsverifikation\n(Tier 3A)", use_container_width=True):
                navigate_to("Tier 3A: Operations Verification Desk")
        with c4:
            if st.button("4. Justiziarprüfung\n(Chambers)", use_container_width=True):
                navigate_to("Legal Chambers: Evidentiary Audit")
        with c5:
            if st.button("5. Exekutiv-Tresor\n(Tier 4)", use_container_width=True):
                navigate_to("Tier 4: Executive Vault & Filing (Always Active)")

    elif is_court_native and profile["jurisdiction"] == "JP_TYO":
        st.title("第1段階：主権執行指令センター")
        st.caption("リアルタイム流動性リスク、損失軽減および訴訟準備")

        c1, c2, c3 = st.columns(3)
        c1.metric(
            "本日の累積保留損失",
            f"{currency_symbol}{(profile['burn_rate_daily'] / 24 * 4.2):,.0f}",
            burn_delta_text,
            delta_color=burn_delta_color,
        )
        c2.metric(
            "信用状リスク",
            f"{currency_symbol}15,000,000",
            f"凍結期限：{jurisdiction['banking_cutoff'].split()[0]}",
        )
        c3.metric("証拠記録ライフサイクル", f"第{dossier_stage}段階 / 全5段階")
        if status_banner:
            st.success(status_banner)

        st.markdown("---")
        st.subheader("敵対的レッドチーム事前対策ブリーフィング")
        st.info(
            f"**対象相手方：** {profile['target_entity']}\n\n"
            "**裁判所先例リスク：** 初日に回復不能なシステム損害および継続的な計測記録を立証できない場合、"
            "金銭請求のみの申立ては棄却される可能性があります。第2段階（現場証明）では、テレメトリを"
            f"**{jurisdiction['metrology']}** の校正標準に関連付ける必要があります。"
        )

        st.subheader("証拠保全プロセス管理")
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            if st.button("1. 運用指令\n(Tier 3A)", use_container_width=True):
                navigate_to("Tier 3A: Operations Dispatch Command")
        with c2:
            if st.button("2. 現場証明\n(Tier 3B)", use_container_width=True):
                navigate_to("Tier 3B: Work-Face Attestation Desk")
        with c3:
            if st.button("3. 運用検証\n(Tier 3A)", use_container_width=True):
                navigate_to("Tier 3A: Operations Verification Desk")
        with c4:
            if st.button("4. 法務監査\n(Legal)", use_container_width=True):
                navigate_to("Legal Chambers: Evidentiary Audit")
        with c5:
            if st.button("5. 役員保管庫\n(Tier 4)", use_container_width=True):
                navigate_to("Tier 4: Executive Vault & Filing (Always Active)")

    else:
        st.title("Tier 1: Sovereign Executive Command")
        st.caption("Real-Time Liquidity Exposure, Burn Mitigation & Litigation Readiness")

        c1, c2, c3 = st.columns(3)
        c1.metric(
            f"Accrued Holding Burn ({currency_code})",
            f"{currency_symbol}{(profile['burn_rate_daily'] / 24 * 4.2):,.2f}",
            burn_delta_text,
            delta_color=burn_delta_color,
        )
        c2.metric(
            f"Letter of Credit At Risk ({currency_code})",
            f"{currency_symbol}15,000,000.00",
            f"Freeze Deadline: {jurisdiction['banking_cutoff'].split()[0]}",
        )
        c3.metric("Dossier Lifecycle Status", f"Stage {dossier_stage} of 5")
        if status_banner:
            st.success(status_banner)

        st.markdown("---")
        st.subheader("Adversarial Red Team Pre-Emption Briefing")
        st.info(
            f"**Target Counterparty:** {profile['target_entity']}\n\n"
            "**Forum Precedent Risk:** Commercial divisions dismiss monetary-only claims unless irreparable system "
            "damage and continuous metric logging are demonstrated on Day 1. "
            "Stage 2 (Field Attestation) must anchor telemetry to "
            f"{jurisdiction['metrology']} calibration."
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
    st.title(localized_text("Tier 3A: Engineering Operations Dispatch", "Tier 3A: Technische Einsatzdisposition", "第3A段階：技術運用指令"))
    st.caption(localized_text("Formal Issuance of Statutory Work Orders", "Prüfauftragserstellung & forensische Metrologie-Rückbindung", "法定作業指示書の発行および法科学的計量トレーサビリティ"))

    st.markdown(f"**{localized_text('Work Order ID', 'Prüfauftrag', '作業指示書ID')}：** `{profile['work_order']}`")
    st.markdown(f"**{localized_text('Governing Metric', 'Prüfstandard', '適用基準')}：** `{profile['standard']}`")
    st.markdown(f"**{localized_text('Assigned Instrument', 'Zugewiesenes Messgerät', '指定計測機器')}：** `{profile['instrument']}`")

    wo_text = st.text_area(
        localized_text("Technical Scope & Statutory Directives", "Gegenstand des Prüfauftrags:", "技術範囲および法定指示"),
        value=active_docket["wo_scope"],
        height=150,
    )

    if dossier_stage == 1:
        if st.button(
            localized_text("Transmit Work Order to Site Desk (Tier 3B)", "Einsatzauftrag an Prüfingenieur übermitteln", "作業指示書を現場認証デスクへ送信"),
            type="primary",
            use_container_width=True,
        ):
            active_docket["wo_scope"] = wo_text
            active_docket["exhibit_a_status"] = "READY"
            advance_active_stage(2)
            navigate_to("Tier 3B: Work-Face Attestation Desk")
    else:
        st.success(localized_text(f"Work Order dispatched. Current lifecycle is at Stage {dossier_stage}.", f"Prüfauftrag übermittelt. Aktueller Lebenszyklus: Stufe {dossier_stage}.", f"作業指示書を送信しました。現在は第{dossier_stage}段階です。"))
        if st.button(
            localized_text("➔ Proceed to Tier 3B: Work-Face Attestation Desk", "➔ Weiter zu Tier 3B: Beglaubigungsarbeitsplatz", "➔ 第3B段階：現場認証デスクへ進む"),
            type="primary",
            use_container_width=True,
        ):
            navigate_to("Tier 3B: Work-Face Attestation Desk")

elif nav_selection == "Tier 3B: Work-Face Attestation Desk":
    st.title(localized_text("Tier 3B: Work-Face Attestation Desk", "Tier 3B: Beglaubigungsarbeitsplatz vor Ort", "第3B段階：現場証拠認証デスク"))
    st.caption(localized_text("Physical Calibration, Telemetry Ingestion & PE Statutory Seal", "Eidesstattliche Erklärung & Versiegelung der Telemetriedaten", "物理校正、テレメトリ取得および法定技術者封印"))

    st.markdown(f"**{localized_text('Active Work Order', 'Aktiver Prüfauftrag', '有効な作業指示書')}：** `{profile['work_order']}`")
    st.markdown(f"**{localized_text('Assigned Certifying Witness', 'Zertifizierter Prüfingenieur', '指定認証証人')}：** `{certifier_witness}`")
    st.markdown(f"**{localized_text('Metrology Traceability', 'Rückführbare Kalibrierstelle', '計量トレーサビリティ')}：** `{jurisdiction['metrology']}`")

    st.markdown(localized_text("#### Step 1: Physical Zero-Drift & Sensor Calibration", "#### Schritt 1: Nullpunktdrift- und Sensorkalibrierung", "#### 手順1：ゼロドリフトおよびセンサー校正"))
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"**{localized_text('Metrology Calibration Token', 'Metrologischer Kalibriernachweis', '計量校正トークン')} ({jurisdiction['metrology']})**")
        st.code("NIST-CAL-99120-PASS", language="text")
    with c2:
        st.markdown(f"**{localized_text('Zero-Drift Variance (Pre-Test Audit)', 'Nullpunktdrift (Vorprüfung)', 'ゼロドリフト偏差（試験前監査）')}**")
        st.success(localized_text("0.0002% — WITHIN STATUTORY TOLERANCE (< 0.01%)", "0,0002 % — INNERHALB DER GESETZLICHEN TOLERANZ (< 0,01 %)", "0.0002% — 法定許容範囲内（< 0.01%）"))

    st.markdown(localized_text("#### Step 2: Telemetry Capture & Oscillography Stream", "#### Schritt 2: Telemetrie- und Oszillografiedatenerfassung", "#### 手順2：テレメトリ取得および波形記録"))
    sample_payload = {
        "docket": profile["docket_id"],
        "standard": profile["standard"],
        "metric_violation": "4.12% Total Harmonic Distortion (Threshold 3.0%)",
        "hardware_sn": "FLK-1777-B9921",
        "sample_rate": "10 kHz continuous",
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }
    st.json(sample_payload)

    st.markdown(localized_text("#### Step 3: Statutory Witness Oath", "#### Schritt 3: Eidesstattliche Versicherung", "#### 手順3：法定証人宣誓"))
    st.warning(f"**{localized_text('Statutory Oath', 'Eidesstattliche Versicherung', '法定宣誓')}：** {jurisdiction['oath_text']}")

    if dossier_stage < 2:
        st.error(localized_text("Work Order pending dispatch from Tier 3A.", "Prüfauftrag aus Tier 3A steht noch aus.", "第3A段階からの作業指示書送信を待機しています。"))
        if st.button(
            localized_text("Fast-Track Dispatch & Unlock Signing Desk", "Eilübermittlung & Signaturplatz freigeben", "緊急送信して認証デスクを解除"),
            type="primary",
            use_container_width=True,
        ):
            active_docket["exhibit_a_status"] = "READY"
            advance_active_stage(2)
            navigate_to("Tier 3B: Work-Face Attestation Desk")
    elif dossier_stage == 2:
        if st.button(
            localized_text(f"Affix Statutory Seal ({certifier_witness})", "Telemetrie versiegeln und eidesstattlich bestätigen", "証拠認証を実行"),
            type="primary",
            use_container_width=True,
        ):
            raw_telemetry = json.dumps(sample_payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
            active_docket["field_telemetry_payload"] = raw_telemetry
            active_docket["field_telemetry_hash"] = hashlib.sha256(raw_telemetry.encode("utf-8")).hexdigest()
            active_docket["pe_signed_by"] = profile["certifier_title"]
            active_docket["cosigned_by"] = profile["certifier_title"]
            active_docket["witness_signed"] = True
            active_docket["attestation_hash"] = hashlib.sha256(
                f"{raw_telemetry}|{profile['certifier_title']}".encode("utf-8")
            ).hexdigest()
            active_docket["exhibit_b_status"] = "CERTIFIED"
            advance_active_stage(3)
            navigate_to("Tier 3A: Operations Verification Desk")
    else:
        if active_docket.get("witness_signed"):
            st.success(localized_text(f"Attestation completed by {active_docket['pe_signed_by']}.", f"Beglaubigung abgeschlossen durch {active_docket['pe_signed_by']}.", f"{active_docket['pe_signed_by']} による証拠認証が完了しました。"))
        else:
            st.info("Simulated telemetry only. No witness has signed this attestation.")
        st.code(f"Hash: {active_docket['field_telemetry_hash']}")
        if st.button(
            localized_text("➔ Proceed to Tier 3A: Operations Verification", "➔ Weiter zu Tier 3A: Betriebsverifikation", "➔ 第3A段階：運用検証へ進む"),
            type="primary",
            use_container_width=True,
        ):
            navigate_to("Tier 3A: Operations Verification Desk")

elif nav_selection == "Tier 3A: Operations Verification Desk":
    st.title(localized_text("Tier 3A: Operations Verification & Audit", "Tier 3A: Betriebs- und Revisionsverifikation", "第3A段階：運用検証および監査"))
    st.caption(localized_text("Verification of Methodological Integrity Prior to Legal Review", "Prüfung der methodischen Integrität vor Vorlage bei der Rechtsabteilung", "法務審査前の方法論的完全性の検証"))

    if dossier_stage < 3:
        st.info(localized_text("Awaiting completion of Tier 3B physical field attestation.", "Abschluss der Tier-3B-Feldbeglaubigung steht aus.", "第3B段階の現場認証完了を待機しています。"))
    else:
        telemetry_intact, telemetry_message = verify_telemetry_integrity(active_docket_id)
        st.markdown(f"**{localized_text('Verified Telemetry Hash', 'Verifizierter Telemetrie-Hash', '検証済みテレメトリハッシュ')}：** `{active_docket['field_telemetry_hash']}`")
        st.markdown(f"**{localized_text('Witness Cosigner', 'Beglaubigt durch', '現場証人')}：** `{active_docket.get('cosigned_by') or 'Awaiting witness attestation'}`")

        if not telemetry_intact:
            st.error(f"HASH MISMATCH / TAMPER DETECTED\n\n{telemetry_message}")
        else:
            c1, c2 = st.columns(2)
            c1.checkbox(localized_text("Confirm 48-Hour Prior Notice of Test was Served", "48-Stunden-Vorankündigung der Beweissicherung an Gegenpartei bestätigt", "48時間前の試験通知が相手方に送達済みであることを確認"), value=True, disabled=True)
            c2.checkbox(localized_text("Confirm Calibration Certificate Traceable to " + jurisdiction["metrology"], "PTB-Kalibrierzertifikat des Messgeräts auf Gültigkeit geprüft", "計測機器の校正証明書が国家標準にトレーサブルであることを確認"), value=True, disabled=True)

            if dossier_stage == 3:
                if st.button(
                    localized_text("Countersign Manifest & Transmit to Legal Chambers", "Manifest gegenzeichnen und an Justiziar übermitteln", "マニフェストに副署し法務審査へ送信"),
                    type="primary",
                    use_container_width=True,
                ):
                    active_docket["ops_countersigned_by"] = "VP Operations / Sarah Jenkins"
                    active_docket["exhibit_c_status"] = "READY"
                    advance_active_stage(4)
                    navigate_to("Legal Chambers: Evidentiary Audit")
            else:
                if active_docket["ops_countersigned_by"]:
                    st.success(f"Countersigned by {active_docket['ops_countersigned_by']}.")
                else:
                    st.info("Operations countersignature pending (simulated trip).")
                if st.button(
                    "➔ Proceed to Legal Chambers Audit",
                    type="primary",
                    use_container_width=True,
                ):
                    navigate_to("Legal Chambers: Evidentiary Audit")

elif nav_selection == "Legal Chambers: Evidentiary Audit":
    st.title(localized_text("Legal Chambers: Trial Admissibility Clearance", "Rechtsabteilung: Prozessuale Beweiswürdigung", "法務部門：証拠能力審査"))
    st.caption(localized_text("FRE / ZPO Gap Analysis, Anti-Spoliation Directive & Red-Team Audit", "ZPO-Beweisbedarfsanalyse, Beweisvereitelungsschutz & Red-Team-Audit", "証拠能力ギャップ分析、証拠保全指令およびレッドチーム監査"))

    if dossier_stage < 4:
        st.info(localized_text("Awaiting Operations verification before initiating legal chambers review.", "Betriebsverifikation vor Beginn der Rechtsprüfung steht aus.", "法務審査の開始前に運用検証の完了を待機しています。"))
    else:
        st.subheader(localized_text("Admissibility Gap Analysis", "Analyse der Beweisadmissibilität", "証拠能力ギャップ分析"))
        st.markdown(f"**{localized_text('Governing Rule', 'Maßgebliche Rechtsnorm', '適用法令')}：** `{jurisdiction['statute_evidence']}`")
        st.markdown(f"**{localized_text('Fiduciary Safe Harbor', 'Organhaftungsschutz', '取締役責任保護')}：** `{jurisdiction['fiduciary_shield']}`")

        st.success(localized_text(
            "✓ Metrology chain of custody complete.\n\n✓ Self-authenticating electronic record meets governing requirements.\n\n✓ Anti-spoliation litigation hold ready for simultaneous service.",
            "✓ Metrologische Beweiskette lückenlos nachgewiesen.\n\n✓ Selbstauthentifizierende elektronische Urkunde erfüllt die maßgeblichen Anforderungen.\n\n✓ Beweissicherungsanordnung zur Zustellung vorbereitet.",
            "✓ 計量上の証拠保全記録が完結しています。\n\n✓ 自己認証型電磁的記録が適用要件を満たしています。\n\n✓ 証拠破棄防止命令を同時送達する準備が完了しています。",
        ))

        if dossier_stage == 4:
            if st.button(
                localized_text("Clear Dossier & Issue Litigation Hold to Tier 4 Vault", "Dossier freigeben & Notfall-Verfahren an Tier-4-Tresor übermitteln", "証拠記録を承認し第4段階保管庫へ証拠保全命令を送信"),
                type="primary",
                use_container_width=True,
            ):
                active_docket["legal_cleared_by"] = "Katherine Ross, Lead Trial Counsel"
                active_docket["exhibit_d_status"] = "READY"
                advance_active_stage(5)
                navigate_to("Tier 4: Executive Vault & Filing (Always Active)")
        else:
            st.success(localized_text(f"Cleared for trial filing by {active_docket['legal_cleared_by']}.", f"Zur gerichtlichen Einreichung freigegeben durch {active_docket['legal_cleared_by']}.", f"{active_docket['legal_cleared_by']} が裁判所提出を承認しました。"))
            if st.button(
                localized_text("➔ Open Tier 4 Executive Vault", "➔ Tier-4-Exekutiv-Tresor öffnen", "➔ 第4段階：役員保管庫を開く"),
                type="primary",
                use_container_width=True,
            ):
                navigate_to("Tier 4: Executive Vault & Filing (Always Active)")

elif nav_selection == "Tier 4: Executive Vault & Filing (Always Active)":
    ui = (
        UI_STRINGS.get(profile["jurisdiction"], UI_STRINGS["DEFAULT"])
        if is_court_native
        else UI_STRINGS["DEFAULT"]
    )
    st.title(ui["vault_title"])
    st.caption(ui["vault_caption"])
    dossier_cleared, integrity_message = verify_dossier_integrity(active_docket_id)
    telemetry_tampered = integrity_message == "Security Alert: Telemetry payload tamper detected. SHA-256 mismatch."
    simulated_dossier = (active_docket.get("field_telemetry_payload") or "").startswith("SIMULATED|")
    if simulated_dossier:
        st.info("Simulation only: generated exhibits are not independently certified; no filing or bank instruction is sent.")

    st.subheader(ui["status_title"])
    e1, e2, e3, e4 = st.columns(4)
    e1.markdown(f"**{ui['ex_a']}**\n\n*{ui['ex_a_sub']}*")
    if st.session_state.get("exhibit_a_status") in ("READY", "CERTIFIED"):
        e1.success("SIMULATED" if simulated_dossier else ui["badge_ready"])
    else:
        e1.warning(ui["badge_awaiting"])

    e2.markdown(f"**{ui['ex_b']}**\n\n*{ui['ex_b_sub']}*")
    if telemetry_tampered:
        e2.error("TAMPERED")
    elif st.session_state.get("exhibit_b_status") in ("SEALED", "CERTIFIED"):
        e2.success("SIMULATED" if simulated_dossier else ui["badge_sealed"])
    else:
        e2.warning(ui["badge_awaiting"])
    e2.caption(f"{ui['witness_prefix']}: {certifier_witness}")

    e3.markdown(f"**{ui['ex_c']}**\n\n*{ui['ex_c_sub']}*")
    if st.session_state.get("exhibit_c_status") in ["READY", "SEALED", "CERTIFIED"]:
        e3.success("SIMULATED" if simulated_dossier else ui["badge_cert"])
    else:
        e3.warning(ui["badge_awaiting"])

    e4.markdown(f"**{ui['ex_d']}**\n\n*{ui['ex_d_sub']}*")
    if st.session_state.get("exhibit_d_status") in ["READY", "SEALED", "COMPILED"]:
        e4.success("SIMULATED" if simulated_dossier else ui["badge_comp"])
    else:
        e4.info(ui["badge_draft"])

    st.markdown("---")
    st.subheader(ui["dual_key_title"])
    st.markdown(f"**{ui['dual_key_bank']}:** :red[{jurisdiction['banking_cutoff']}]")

    raw_payload = active_docket.get("field_telemetry_payload") or ""
    with st.expander(localized_text("Red-Team Integrity Test", "Red-Team-Integritätstest", "レッドチーム完全性テスト")):
        st.caption(localized_text(
            "Alter the sealed metric from 4.12% to 4.13% without updating its SHA-256 anchor.",
            "Versiegelten Messwert von 4,12 % auf 4,13 % ändern, ohne den SHA-256-Anker zu aktualisieren.",
            "SHA-256アンカーを更新せず、封印済み測定値を4.12%から4.13%へ変更します。",
        ))

        tamper_col, restore_col = st.columns(2)
        with tamper_col:
            if st.button(
                localized_text("Tamper with Sealed Telemetry", "Versiegelte Telemetrie manipulieren", "封印済みテレメトリを改ざん"),
                disabled="4.12%" not in raw_payload,
                key=f"{active_docket_id}_tamper_telemetry",
            ):
                active_docket["field_telemetry_payload"] = raw_payload.replace("4.12%", "4.13%", 1)
                active_docket["exhibit_b_status"] = "TAMPERED"
                st.rerun()

        with restore_col:
            if st.button(
                localized_text("Restore Baseline Telemetry", "Basis-Telemetrie wiederherstellen", "ベースラインテレメトリを復元"),
                disabled="4.13%" not in raw_payload,
                key=f"{active_docket_id}_restore_telemetry",
            ):
                active_docket["field_telemetry_payload"] = raw_payload.replace("4.13%", "4.12%", 1)
                active_docket["exhibit_b_status"] = "CERTIFIED" if active_docket.get("witness_signed") else "SEALED"
                st.rerun()

    chairman_widget_key = f"{active_docket_id}_dual_key_chairman"
    clo_widget_key = f"{active_docket_id}_dual_key_clo"
    if not dossier_cleared:
        active_docket["dual_key_chairman"] = False
        active_docket["dual_key_clo"] = False
        st.session_state[chairman_widget_key] = False
        st.session_state[clo_widget_key] = False

    col_k1, col_k2 = st.columns(2)
    key_chairman = col_k1.checkbox(
        ui["key_1_label"],
        value=active_docket.get("dual_key_chairman", False),
        disabled=not dossier_cleared,
        key=chairman_widget_key,
    )
    key_clo = col_k2.checkbox(
        ui["key_2_label"],
        value=active_docket.get("dual_key_clo", False),
        disabled=not dossier_cleared,
        key=clo_widget_key,
    )

    active_docket["dual_key_chairman"] = key_chairman
    active_docket["dual_key_clo"] = key_clo

    if not dossier_cleared:
        st.error(integrity_message)
    else:
        st.success(integrity_message)
        if key_chairman and key_clo:
            st.success(ui["keys_verified_msg"])
            if st.button(
                "Execute simulated filing & drawstop" if simulated_dossier else ui["exec_btn"],
                type="primary",
                use_container_width=True,
            ):
                active_docket["executed"] = True
                st.balloons()
        else:
            st.info(ui["keys_locked_msg"])

    if active_docket.get("executed", False):
        if simulated_dossier:
            st.success("Simulated filing and drawstop recorded in this session. No external action was taken.")
        else:
            st.markdown(
                f"""
            <div style="background-color: #1e3a24; border: 1px solid #2e7d32; padding: 14px; border-radius: 6px; margin-top: 15px;">
                <h4 style="color: #4caf50; margin: 0 0 8px 0;">{ui['filed_banner']}</h4>
                <p style="margin: 0; color: #c8e6c9;">{ui['claim_served']} <b>{profile['target_entity']}</b></p>
                <p style="margin: 4px 0 0 0; color: #a5d6a7;">{ui['lc_drawstop']}</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

    st.markdown("---")
    with st.expander(f"📄 View Active Filing Exhibits [{active_stream_label}]", expanded=False):
        st.markdown(f"#### {doc_content['exhibit_a_title']}")
        st.write(doc_content["exhibit_a_body"])
        st.markdown("---")
        st.markdown(f"#### {doc_content['exhibit_b_title']}")
        st.write(doc_content["exhibit_b_body"])
        st.markdown("---")
        st.markdown(f"#### {doc_content['exhibit_c_title']}")
        st.write(doc_content["exhibit_c_body"])
        st.markdown("---")
        st.markdown(f"#### {doc_content['exhibit_d_title']}")
        st.write(doc_content["exhibit_d_body"])

    active_jurisdiction = profile["jurisdiction"]
    st.markdown("---")
    st.subheader(ui["export_title"])
    st.caption(ui["export_caption"])
    file_col1, file_col2 = st.columns(2)

    court_native_payload = {
        "docket_id": profile["docket_id"],
        "document_type": "SIMULATED_COURT_PLEADING" if simulated_dossier else "OFFICIAL_COURT_PLEADING",
        "simulation_only": simulated_dossier,
        "jurisdiction": active_jurisdiction,
        "court_venue": jurisdiction["court"],
        "language": loc_data["court_lang_name"] if loc_data else jurisdiction["primary_language"],
        "exhibits": loc_data["court"] if loc_data else doc_content,
        "telemetry_sha256": active_docket["field_telemetry_hash"],
    }

    with file_col1:
        st.download_button(
            label=ui["court_btn"],
            data=json.dumps(court_native_payload, indent=2, ensure_ascii=False),
            file_name=f"{profile['docket_id']}_{'COURT_SIMULATED' if simulated_dossier else 'COURT_OFFICIAL'}.json",
            mime="application/json",
            use_container_width=True,
        )
        st.caption(ui["court_btn_sub"])

    exec_master_payload = {
        "docket_id": profile["docket_id"],
        "document_type": "SIMULATED_EXECUTIVE_MASTER_DOSSIER" if simulated_dossier else "EXECUTIVE_MASTER_DOSSIER",
        "simulation_only": simulated_dossier,
        "jurisdiction": active_jurisdiction,
        "governing_standard": profile["standard"],
        "language": "en-US (International Master)",
        "exhibits": loc_data["english"] if loc_data else doc_content,
        "telemetry_sha256": active_docket["field_telemetry_hash"],
    }

    with file_col2:
        st.download_button(
            label=ui["master_btn"],
            data=json.dumps(exec_master_payload, indent=2, ensure_ascii=False),
            file_name=f"{profile['docket_id']}_{'SIMULATED_' if simulated_dossier else ''}EXECUTIVE_MASTER_EN.json",
            mime="application/json",
            use_container_width=True,
        )
        st.caption(ui["master_btn_sub"])

import datetime
import hashlib
import json
import re
import streamlit as st

APP_BUILD_ID = "v5.1_interactive_manual_pe_bypass_sep16_2026"

if st.session_state.get("build_id") != APP_BUILD_ID:
    st.session_state.clear()
    st.session_state["build_id"] = APP_BUILD_ID

st.set_page_config(
    page_title="Command Post & Forensic Vault | Autonomous Capital Defense",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# 1. INDUSTRIAL STYLING & DIRECTIVE ELEVATION
# =========================================================
st.markdown("""
    <style>
        .stApp { 
            background-color: #0d1117; 
            color: #f0f6fc; 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; 
        }
        
        p { 
            font-size: 1.1rem !important; 
            line-height: 1.6 !important; 
            color: #f0f6fc !important;
        }
        div[data-testid="stCaptionContainer"] p { 
            font-size: 1.05rem !important; 
            color: #c9d1d9 !important; 
            font-weight: 500 !important; 
        }
        .stRadio label { 
            font-size: 1.1rem !important; 
            font-weight: 600 !important; 
            color: #f0f6fc !important;
        }
        
        /* Chairman Throttle Input: MASSIVE & ALERT RED */
        .capex-throttle div[data-testid="stTextInput"] input,
        .capex-throttle input[type="text"] {
            font-size: 3.2rem !important;
            font-weight: 900 !important;
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace !important;
            color: #ff4b4b !important;
            background-color: #090d13 !important;
            border: 2px solid #58a6ff !important;
            border-radius: 8px !important;
            padding: 18px 20px !important;
            text-align: center !important;
            box-shadow: 0 0 16px rgba(88, 166, 255, 0.25) !important;
            height: auto !important;
        }
        .capex-throttle div[data-testid="stTextInput"] input:focus,
        .capex-throttle input[type="text"]:focus {
            border-color: #ff4b4b !important;
            box-shadow: 0 0 22px rgba(255, 75, 75, 0.4) !important;
        }

        div[data-testid="stButton"] button {
            white-space: normal !important;
            word-break: break-word !important;
            height: auto !important;
            min-height: 52px !important;
            padding: 12px 14px !important;
            line-height: 1.35 !important;
            font-size: 1.05rem !important;
            font-weight: 800 !important;
            border-radius: 6px !important;
        }

        .emergency-halt-btn button {
            background-color: #da3633 !important;
            color: #ffffff !important;
            border: 1px solid #f85149 !important;
            box-shadow: 0 0 12px rgba(218, 54, 51, 0.4) !important;
        }
        .emergency-halt-btn button:hover {
            background-color: #b62324 !important;
            border-color: #ff7b72 !important;
            box-shadow: 0 0 18px rgba(255, 75, 75, 0.6) !important;
        }
        
        /* Diagnostic Input */
        div[data-testid="stTextInput"]:not(.capex-throttle *) input {
            font-size: 1.05rem !important;
            font-weight: 600 !important;
            background-color: #161b22 !important;
            border: 1px solid #30363d !important;
            color: #f0f6fc !important;
            border-radius: 6px !important;
            padding: 10px 14px !important;
        }
        
        /* Metric & Evidence Cards */
        .exec-metric-card {
            background-color: #161b22;
            border: 2px solid #30363d;
            border-radius: 8px;
            padding: 16px 20px;
            text-align: center;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            min-height: 125px;
        }
        .exec-metric-card-secondary {
            background-color: #11151c;
            border: 1px solid #21262d;
            border-radius: 6px;
            padding: 10px 14px;
            text-align: center;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            min-height: 85px;
        }
        .circuit-breaker-card {
            background-color: rgba(248, 81, 73, 0.12);
            border: 2px solid #f85149;
            border-radius: 8px;
            padding: 14px 16px;
            text-align: center;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            min-height: 125px;
        }
        .circuit-defended-card {
            background-color: rgba(46, 160, 67, 0.15);
            border: 2px solid #2ea043;
            border-radius: 8px;
            padding: 14px 16px;
            text-align: center;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            min-height: 125px;
        }
        .claim-demand-card {
            background-color: rgba(227, 179, 65, 0.12);
            border: 2px solid #e3b341;
            border-radius: 8px;
            padding: 14px 16px;
            text-align: center;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            min-height: 125px;
        }
        .exec-metric-label {
            color: #e6edf3;
            font-size: 0.9rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 6px;
        }
        .exec-metric-val {
            color: #ffffff;
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
            font-size: 1.95rem;
            font-weight: 800;
            line-height: 1.15;
        }
        .exec-metric-val-secondary {
            color: #ffffff;
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
            font-size: 1.35rem;
            font-weight: 700;
            line-height: 1.15;
        }
        .exec-metric-sub {
            font-size: 0.95rem;
            font-weight: 700;
            margin-top: 6px;
        }
        
        .stButton>button {
            border-radius: 6px;
            font-weight: 700;
            font-size: 1.05rem !important;
            padding: 10px 18px;
        }

        .legal-document-box {
            background-color: #0d1117;
            border: 2px solid #30363d;
            border-left: 6px solid #58a6ff;
            border-radius: 6px;
            padding: 20px 24px;
            font-family: Georgia, Cambria, "Times New Roman", Times, serif;
            color: #e6edf3;
            line-height: 1.7;
        }
        .legal-header {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-size: 0.95rem;
            font-weight: 800;
            color: #58a6ff;
            margin-bottom: 12px;
        }
    </style>
""", unsafe_allow_html=True)

# =========================================================
# 2. LOCALIZATION DICTIONARY & MULTI-PAGE LABELS
# =========================================================
I18N = {
    "English [USA · UK · Australia]": {
        "tier1_title": "Tier 1 | Chairman Tactical Command Post (Part One)",
        "tier2_title": "Tier 2 | Directorate Governance Desk",
        "tier3_title": "Tier 3 | Site Operations & Operator Remediation Desk",
        "tier4_title": "Tier 4 | Forensic Cost Recovery Vault (Part Two)",
        "sub_app": "Autonomous Capital Defense & Claims Recovery Engine",
        "calib_red_header": "COMMAND GATEWAY: ENTER NEW PROJECT BUDGET / CAPEX AT RISK (TAP TO RE-CALIBRATE)",
        "override_active": "EXECUTIVE OVERRIDE ACTIVE",
        "baseline_synced": "PUBLIC BASELINE SYNCHRONIZED",
        "toll_fee": "Toll-Gate Fee (Milestone)",
        "escrow_desc": "↑ 0.085% CapEx Escrow",
        "session_window": "Live Session Window",
        "session_desc": "↑ Cryptographic Epoch Active",
        "holding_burn": "Portfolio Holding Burn",
        "cap_under_def": "Capital Under Defense",
        "active_block": "Active Block",
        "crossover_sub": "↑ Crossover to Total Loss",
        "circuit_btn_line1": "🛑 STOP THE BLEED",
        "circuit_btn_line2": "Execute Board Indemnity Shield",
        "circuit_active_hint": "One click absorbs engineer liability under statute, transmits the PE stamp, and halts the daily burn to $0.",
        "circuit_defended": "🟢 CAPITAL DEFENDED — BLEED: $0",
        "why_stalled": "🚨 1. Why is the Fix Stalled?",
        "what_unblocks": "🟢 2. What Document Unblocks the Gate?",
        "interrogate_hint": "Type query to interrogate agents...",
        "branches_title": "The Three Cascading Branches & Remedial Levers",
        "pipeline_title": "🔒 Forward Incident Pipeline (Next 4 Bottlenecks)",
        "claim_total_label": "Direct Liquidated Claim Due",
        "claim_sub": "↑ Reimbursable under Schedule D",
        "audit_title": "Cryptographic Audit Ledger & Sealed Job Packages"
    },
    "Deutsch [Deutschland · Österreich]": {
        "tier1_title": "Stufe 1 | Taktisches Führungszentrum (Teil Eins)",
        "tier2_title": "Stufe 2 | Directorate Governance Desk",
        "tier3_title": "Stufe 3 | Standortbetrieb & Bediener-Sanierungs-Desk",
        "tier4_title": "Stufe 4 | Forensischer Kostenerstattungstresor (Teil Zwei)",
        "sub_app": "Autonome Kapitalverteidigungs- & Forderungsdurchsetzungs-Plattform",
        "calib_red_header": "FÜHRUNGSTOR: NEUES PROJEKTBUDGET / GEFÄHRDETES INVESTITIONSKAPITAL EINGEBEN",
        "override_active": "LEITUNGS-ÜBERSTEUERUNG AKTIV",
        "baseline_synced": "ÖFFENTLICHE BASISDATEN SYNCHRONISIERT",
        "toll_fee": "Meilenstein-Freigabegebühr",
        "escrow_desc": "↑ 0,085% Verwahrungsschild",
        "session_window": "Laufendes Sitzungsfenster",
        "session_desc": "↑ Kryptographische Epoche Aktiv",
        "holding_burn": "Portfolio-Halteverlust",
        "cap_under_def": "Verteidigtes Anlagekapital",
        "active_block": "Aktive Störung",
        "crossover_sub": "↑ Zeit bis zum Totalverlust",
        "circuit_btn_line1": "🛑 HALTEVERLUST STOPPEN",
        "circuit_btn_line2": "Vorstandsschutz Aktivieren",
        "circuit_active_hint": "Ein Klick übernimmt die Ingenieurhaftung gemäß Gesetz, überträgt das Gutachten und senkt den täglichen Verlust auf 0 €.",
        "circuit_defended": "🟢 KAPITAL VERTEIDIGT — VERLUST: 0 €",
        "why_stalled": "🚨 1. Warum stockt die Freigabe?",
        "what_unblocks": "🟢 2. Welches Dokument entsperrt das Tor?",
        "interrogate_hint": "Frage zur Aufklärung eingeben...",
        "branches_title": "Die Drei Kaskadierenden Säulen & Abhilfemassnahmen",
        "pipeline_title": "🔒 Nachgelagerte Engpass-Pipeline (Nächste 4 Prüfpunkte)",
        "claim_total_label": "Fälliger Direktschadensersatz",
        "claim_sub": "↑ Durchsetzbar nach Klausel D",
        "audit_title": "Kryptographisches Audit-Register & Versiegelte Einsatzkapseln"
    },
    "Español [Chile · Brasil · Sudamérica]": {
        "tier1_title": "Nivel 1 | Puesto de Mando Táctico (Parte Uno)",
        "tier2_title": "Nivel 2 | Mesa de Gobernanza del Consejo",
        "tier3_title": "Nivel 3 | Mesa de Operaciones de Campo y Mitigación",
        "tier4_title": "Nivel 4 | Bóveda Forense de Recuperación de Costos (Parte Dos)",
        "sub_app": "Plano de Control para la Defensa y Recuperación de Capital",
        "calib_red_header": "PORTAL DE MANDO: INGRESE NUEVO PRESUPUESTO / CAPEX EN RIESGO",
        "override_active": "INTERVENCIÓN EJECUTIVA ACTIVA",
        "baseline_synced": "LÍNEA BASE PÚBLICA SINCRONIZADA",
        "toll_fee": "Tarifa de Hito de Paso",
        "escrow_desc": "↑ Custodia Fiduciaria 0,085%",
        "session_window": "Ventana de Sesión Activa",
        "session_desc": "↑ Época Criptográfica Activa",
        "holding_burn": "Pérdida por Retención",
        "cap_under_def": "Capital Bajo Defensa",
        "active_block": "Bloqueo Operacional",
        "crossover_sub": "↑ Plazo para la Pérdida Total",
        "circuit_btn_line1": "🛑 DETENER PÉRDIDA",
        "circuit_btn_line2": "Ejecutar Blindaje del Directorio",
        "circuit_active_hint": "Un clic asume la responsabilidad del ingeniero por ley, emite el timbre PE y detiene el sangrado diario a $0.",
        "circuit_defended": "🟢 CAPITAL DEFENDIDO — PÉRDIDA: $0",
        "why_stalled": "🚨 1. ¿Por qué está trabada la solución?",
        "what_unblocks": "🟢 2. ¿Qué documento legal desbloquea la compuerta?",
        "interrogate_hint": "Escriba consulta de investigación...",
        "branches_title": "Las Tres Ramas en Cascada y Palancas de Mitigación",
        "pipeline_title": "🔒 Ducto Consecutivo (Próximos 4 Cuellos de Botella)",
        "claim_total_label": "Reclamo Directo por Daños Liquidados",
        "claim_sub": "↑ Cobrable según Anexo D",
        "audit_title": "Registro Criptográfico de Auditoría y Cápsulas Selladas"
    },
    "Français [France · RTE · Europe]": {
        "tier1_title": "Niveau 1 | Poste de Commandement Tactique (Partie Un)",
        "tier2_title": "Niveau 2 | Bureau de Gouvernance du Directoire",
        "tier3_title": "Niveau 3 | Bureau Opérations Terrain & Remédiation",
        "tier4_title": "Niveau 4 | Coffre Forensique de Recouvrement (Partie Deux)",
        "sub_app": "Plateforme Autonome de Défense du Capital & Recouvrement",
        "calib_red_header": "PORTAIL DE COMMANDEMENT : SAISIR LE NOUVEAU BUDGET / CAPEX EN RISQUE",
        "override_active": "INTERVENTION EXÉCUTIVE ACTIVE",
        "baseline_synced": "RÉFÉRENTIEL PUBLIC SYNCHRONISÉ",
        "toll_fee": "Frais d'Étape de Déblocage",
        "escrow_desc": "↑ Séquestre Fiduciaire 0,085%",
        "session_window": "Fenêtre de Session Active",
        "session_desc": "↑ Époque Cryptographique Active",
        "holding_burn": "Perte de Rétention du Portefeuille",
        "cap_under_def": "Capital sous Défense",
        "active_block": "Point de Blocage Actif",
        "crossover_sub": "↑ Délai Avant Perte Totale",
        "circuit_btn_line1": "🛑 STOPPER L'HÉMORRAGIE",
        "circuit_btn_line2": "Activer le Bouclier du Directoire",
        "circuit_active_hint": "Un clic absorbe la responsabilité de l'ingénieur par la loi, transmet le visa et ramène la perte quotidienne à 0 €.",
        "circuit_defended": "🟢 CAPITAL DÉFENDU — PERTE: 0 €",
        "why_stalled": "🚨 1. Pourquoi le déblocage est-il gelé ?",
        "what_unblocks": "🟢 2. Quel acte juridique formel débloque le site ?",
        "interrogate_hint": "Interroger les agents...",
        "branches_title": "Les Trois Piliers en Cascade & Leviers d'Atténuation",
        "pipeline_title": "🔒 File des Goulots d'Étranglement (4 Prochains)",
        "claim_total_label": "Indemnité Contractuelle Directe Réclamée",
        "claim_sub": "↑ Exigible selon l'Annexe D",
        "audit_title": "Registre Cryptographique d'Audit & Capsules Scellées"
    },
    "日本語 [日本 · TEPCO · METI]": {
        "tier1_title": "ティア1 | 取締役会長 統合戦術指揮ポスト (第1部)",
        "tier2_title": "ティア2 | 取締役会統治・免責監督デスク",
        "tier3_title": "ティア3 | 現地運用および現場作業員是正デスク",
        "tier4_title": "ティア4 | 法廷証拠・損害費用回収保管庫 (第2部)",
        "sub_app": "自律型自己資本防衛および法的損害賠償回収エンジン",
        "calib_red_header": "コマンド・ゲートウェイ：新しい防衛対象資本・予算を入力（タップして再設定）",
        "override_active": "取締役会による上書き発動中",
        "baseline_synced": "規制当局ベースライン同期済み",
        "toll_fee": "マイルストーン解除手数料",
        "escrow_desc": "↑ 0.085% 信託保全エスクロー",
        "session_window": "暗号化セッション窓口",
        "session_desc": "↑ 暗号学的エポック稼働中",
        "holding_burn": "ポートフォリオ保留損失",
        "cap_under_def": "防衛対象総資本",
        "active_block": "アクティブ遮断事象",
        "crossover_sub": "↑ 資本全損までの限界日数",
        "circuit_btn_line1": "🛑 資本流出を遮断する",
        "circuit_btn_line2": "取締役会免責シールド発動",
        "circuit_active_hint": "ワンクリックで法律に基づく技術者の責任を吸収し、PEスタンプを送信し、日次損失を ¥0 に停止します。",
        "circuit_defended": "🟢 資本防衛完了 — 流出損失: ¥0",
        "why_stalled": "🚨 1. なぜ現場は停滞しているのか？",
        "what_unblocks": "🟢 2. どの法的文書がゲートを解除するか？",
        "interrogate_hint": "エージェントへ直接諮問を入力...",
        "branches_title": "3つの連動防衛ブランチと解決手段",
        "pipeline_title": "🔒 順次解決ボトルネック・パイプライン",
        "claim_total_label": "契約に基づく違約金・損害賠償請求総額",
        "claim_sub": "↑ 別紙D（履行遅延条項）に基づく請求可能額",
        "audit_title": "暗号学的監査台帳および封印済みジョブパッケージ"
    }
}

TODAY_STR = "16 Sep 2026"

SECTORS = {
    "ERCOT BESS / Grid Storage (USA)": {
        "currency": "$",
        "asset_cap": 88_500_000,
        "baseline_docket": "ERCOT IA § 4.2 Interconnection Docket #54219",
        "baseline_date": "16 Sep 2026",
        "statute": "Delaware DGCL § 141 (Business Judgment Rule)",
        "directors": {
            "Dr. Arthur Pendleton": {"seat": "Chair, Grid Risk & Technical Integrity"},
            "David Chen (Proxy)": {"seat": "Chair, Regulatory & Market Compliance"}
        },
        "incidents": {
            "INC-001": {
                "title": "ERCOT IA § 4.2 Part 2 COD Attestation Deadlock",
                "priority": "P1 - CRITICAL",
                "base_daily_bleed": 87264,
                "days_in_deadlock": 7,
                "status": "DEADLOCKED",
                "director_seat": "Dr. Arthur Pendleton",
                "counterparty": {
                    "name": "Apex Power Conversion Systems Corp (OEM)",
                    "contract": "Turnkey EPC & Inverter Supply Agreement #TX-9011",
                    "clause_invoked": "Clause 14.b (Inverter Warranty Voidance Disclaimer)",
                    "breach_clause": "Schedule D § 3 (Unexcused Commissioning Demurrage)"
                },
                "tier3_work_order": {
                    "id": "WO-8821-HARMONIC",
                    "title": "On-Site IEEE 2800 Harmonic Sweep & Attestation",
                    "target_gate": "Check #6 (COD Attestation Gate)",
                    "contractor": "Permian HV Field Services LLC",
                    "field_lead": "Marcus Vance, PE",
                    "progress_pct": 75,
                    "remediation_protocol": "Execute Board Indemnity Carve-Out to absorb Clause 14.b OEM warranty dispute. Clears Lead PE to digitally stamp harmonic mitigation packet and submit directly to ERCOT.",
                    "steps": [
                        {"task": "Rack 4 PE Calibration & Neutral Grounding Sweep", "done": True, "evidence": "Calibration log #PER-409 PASS"},
                        {"task": "Inverter Bank 1-4 Sub-Cycle Injection Sweep", "done": True, "evidence": "THD 4.1% confirmed (< 5.0% threshold)"},
                        {"task": "Damping Resonance Pulse Verification", "done": True, "evidence": "Active damping ratio: 1.18 pu nominal"},
                        {"task": "PE Digital Stamp & Packet Submission", "done": False, "evidence": "Held pending Directorate Indemnity safe harbor"}
                    ],
                    "telemetry": [
                        {"param": "THD Harmonics (IEEE 2800)", "val": "4.1%", "status": "NOMINAL", "limit": "< 5.0%"},
                        {"param": "Inrush Damping Ratio", "val": "1.18 pu", "status": "NOMINAL", "limit": "Trip: 1.40 pu"},
                        {"param": "Frequency Injection Stability", "val": "14.2 MW/0.1Hz", "status": "COMPLIANT", "limit": "ERCOT § 4.2"},
                        {"param": "OEM Cabinet Remote Interlock", "val": "DISENGAGED", "status": "WARN", "limit": "Manual PE Bypass Required"}
                    ]
                },
                "forensic_timeline": [
                    {"time": "2026-09-09 08:14:02.104 UTC", "party": "Grid Physics", "event": "Raw 10 kHz oscillography records grid voltage dip of 4.2% (nominal IEEE 2800 ride-through envelope)."},
                    {"time": "2026-09-09 08:14:02.118 UTC", "party": "Apex Inverter OEM", "event": "Inverter Bank 2 trips out prematurely due to internal OEM firmware protection threshold miscalibration."},
                    {"time": "2026-09-09 09:30:00.000 UTC", "party": "Apex Legal / Field", "event": "Apex invokes Clause 14.b warranty disclaimer, alleging utility surge and refusing attestation sign-off."},
                    {"time": "2026-09-09 10:15:22.000 UTC", "party": "Security Access Logs", "event": "Turnstile badging records confirm Apex OEM Commissioning Lead was off-site during entire trip sequence."},
                    {"time": "2026-09-16 00:00:00.000 UTC", "party": "Capital Audit Engine", "event": "Deadlock reaches Day 7. Accrued delay demurrage hits $610,848. Counterparty formal claim compiled."}
                ],
                "audit_packages": [
                    {
                        "job_id": "JOB-001: Statutory Ingestion Baseline",
                        "status": "SEALED & ATTESTED",
                        "sealed_at": "2026-09-16 00:00:00 UTC",
                        "package_hash": "8f3a9e01c4b72e1",
                        "entries": [
                            "DOCKET INGESTION: Baseline verified against ERCOT Docket #54219.",
                            "CAPITAL AUDIT: Sovereign capital cap locked at $88,500,000.",
                            "FIDUCIARY ANCHOR: Delaware DGCL § 141 safe harbor initialized."
                        ]
                    }
                ]
            },
            "INC-002": {"title": "Substation Step-Up Inrush Damping", "priority": "P2 - HIGH", "base_daily_bleed": 38880},
            "INC-003": {"title": "SCADA Protocol IEC 61850 Gateway", "priority": "P3 - MODERATE", "base_daily_bleed": 15552},
            "INC-004": {"title": "BESS Inverter Firmware OTA Patch", "priority": "P4 - MONITORED", "base_daily_bleed": 4320},
            "INC-005": {"title": "Substation Oil DGA Baseline Sweep", "priority": "P5 - MONITORED", "base_daily_bleed": 6912}
        }
    },
    "Deutsche Bahn AG | Rail Corridor (Germany)": {
        "currency": "€",
        "asset_cap": 34_000_000_000,
        "baseline_docket": "Federal Railway Authority (EBA) Dossier #DE-882",
        "baseline_date": "16 Sep 2026",
        "statute": "German AktG § 93 / § 116 (Aufsichtsrat Dual-Board Shield)",
        "directors": {"Werner Gatzer": {"seat": "Aufsichtsratsvorsitzender"}},
        "incidents": {
            "DB-ETCS-01": {
                "title": "Rhine-Alpine ETCS Level 2 Baseline Handshake Stall",
                "priority": "P1 - CRITICAL",
                "base_daily_bleed": 1728000,
                "days_in_deadlock": 5,
                "status": "DEADLOCKED",
                "director_seat": "Werner Gatzer",
                "counterparty": {
                    "name": "Signaling Interop Consortium GmbH",
                    "contract": "Corridor ETCS Implementation Contract #DB-NETZ-441",
                    "clause_invoked": "Klausel 19.3 (Software-Schnittstellenhaftungsausschluss)",
                    "breach_clause": "VOB/B § 6 Abs. 6 (Schuldhafte Bauzeitverzögerung)"
                },
                "tier3_work_order": {
                    "id": "WO-DB-9901",
                    "title": "Radio Block Centre (RBC) Telegram Handshake Test",
                    "target_gate": "EBA Interoperability Clearance #4",
                    "contractor": "Siemens Mobility Trackside Team",
                    "field_lead": "Dipl.-Ing. Hans Mueller",
                    "progress_pct": 65,
                    "remediation_protocol": "Execute Aufsichtsrat emergency waiver for safety telegram buffer validation, releasing field engineer to attest corridor readiness.",
                    "steps": [
                        {"task": "Balise Link Alignment Sweep", "done": True, "evidence": "Balise 402/403 sync PASS"},
                        {"task": "GSM-R Cryptographic Key Refresh", "done": True, "evidence": "Session keys rotated"},
                        {"task": "RBC Dual Handshake Telemetry Verification", "done": False, "evidence": "Awaiting Board waiver under AktG § 93"}
                    ],
                    "telemetry": [
                        {"param": "Balise Telegram Buffer", "val": "99.8%", "status": "NOMINAL", "limit": "> 99.5%"},
                        {"param": "GSM-R Interoperability Jitter", "val": "18 ms", "status": "NOMINAL", "limit": "< 30 ms"},
                        {"param": "EBA Trackside Clearance", "val": "STANDBY", "status": "WARN", "limit": "Sign-off pending"}
                    ]
                },
                "forensic_timeline": [
                    {"time": "2026-09-11 11:20:00 UTC", "party": "EBA Trackside", "event": "Radio Block Centre reports telegram buffer packet drop at KM 144."},
                    {"time": "2026-09-11 12:05:14 UTC", "party": "Consortium Legal", "event": "Vendor claims DB AG legacy catenary noise caused packet corruption; invokes Klausel 19.3."},
                    {"time": "2026-09-11 14:10:00 UTC", "party": "Dark Data Telemetry", "event": "Fiber optic sniffer logs prove packet drop was internal buffer race condition in vendor RBC module."},
                    {"time": "2026-09-16 00:00:00 UTC", "party": "Capital Audit Engine", "event": "5-day corridor stall reaches €8,640,000 claim value under VOB/B § 6."}
                ],
                "audit_packages": [
                    {
                        "job_id": "JOB-001: EBA Baseline Ingestion",
                        "status": "SEALED & ATTESTED",
                        "sealed_at": "2026-09-16 00:00:00 UTC",
                        "package_hash": "de9910a1b2c45e8",
                        "entries": ["EBA DOCKET INGESTION: Rhine Corridor Dossier #DE-882 locked."]
                    }
                ]
            },
            "DB-002": {"title": "Track Circuit Frequency Interference", "priority": "P2 - HIGH", "base_daily_bleed": 734400},
            "DB-003": {"title": "GSM-R Interoperability Key Refresh", "priority": "P3 - MODERATE", "base_daily_bleed": 190080},
            "DB-004": {"title": "Catenary Tension Thermal Sag Audit", "priority": "P4 - MONITORED", "base_daily_bleed": 95040},
            "DB-005": {"title": "Balise Telegram Buffer Sync", "priority": "P5 - MONITORED", "base_daily_bleed": 69120}
        }
    },
    "Coordinador Eléctrico Nacional | Atacama BESS (Chile)": {
        "currency": "$",
        "asset_cap": 145_000_000,
        "baseline_docket": "CEN Res. Exenta N° 842 / Atacama-Santiago Intertie",
        "baseline_date": "16 Sep 2026",
        "statute": "Ley General de Servicios Eléctricos Art. 72-1 (Chile)",
        "directors": {"Juan Carlos Olmedo": {"seat": "Presidente del Consejo Directivo"}},
        "incidents": {
            "CEN-BESS-01": {
                "title": "Prueba de Inyección de Armónicos y Sincronismo 220kV",
                "priority": "P1 - CRÍTICO",
                "base_daily_bleed": 45000,
                "days_in_deadlock": 6,
                "status": "DEADLOCKED",
                "director_seat": "Juan Carlos Olmedo",
                "counterparty": {
                    "name": "Consorcio Inversores del Norte S.A.",
                    "contract": "Contrato EPC Subestación Kimal-Cardones #CEN-2025",
                    "clause_invoked": "Art. 22 Exclusión por Disturbio de Red",
                    "breach_clause": "Cláusula Penal por Retraso de Interconexión § 8"
                },
                "tier3_work_order": {
                    "id": "WO-CEN-332",
                    "title": "Sincronización 220kV Subestación Kimal",
                    "target_gate": "Autorización Definitiva CEN",
                    "contractor": "Consorcio Atacama Transmisión",
                    "field_lead": "Ing. Camilo Sandoval",
                    "progress_pct": 70,
                    "remediation_protocol": "Resolución de exención fiduciaria Art. 72-1 para liberación de firma digital y despacho inmediato.",
                    "steps": [
                        {"task": "Ajuste Filtro STATCOM Cardones", "done": True, "evidence": "Prueba de banco aprobada"},
                        {"task": "Verificación Resonancia Inyección Solar", "done": True, "evidence": "THD 3.8% nominal"},
                        {"task": "Firma Digital Protocolo PSS/E Despacho CEN", "done": False, "evidence": "Pendiente de resolución del Consejo"}
                    ],
                    "telemetry": [
                        {"param": "THD Tensión 220kV", "val": "3.8%", "status": "NOMINAL", "limit": "< 4.5%"},
                        {"param": "Potencia Reactiva Inyectada", "val": "45 MVAR", "status": "NOMINAL", "limit": "± 50 MVAR"},
                        {"param": "Respuesta Dinámica STATCOM", "val": "85 ms", "status": "NOMINAL", "limit": "< 100 ms"}
                    ]
                },
                "forensic_timeline": [
                    {"time": "2026-09-10 14:00:00 UTC", "party": "Subestación Kimal", "event": "Inversor corta inyección durante rampa solar por desajuste de protecciones."},
                    {"time": "2026-09-10 15:30:00 UTC", "party": "Contratista EPC", "event": "EPC atribuye falla a sobretensión en la línea Kimal-Cardones."},
                    {"time": "2026-09-10 16:45:00 UTC", "party": "Registrador Oscilográfico", "event": "Registro de falla prueba que la red operaba en 220.1 kV. Falla originada en el software del contratista."},
                    {"time": "2026-09-16 00:00:00 UTC", "party": "Motor Forense", "event": "6 días de atraso acumulados: $270,000 en pérdidas líquidas exigibles."}
                ],
                "audit_packages": [
                    {
                        "job_id": "JOB-001: Registro CEN Ingestado",
                        "status": "SEALED & ATTESTED",
                        "sealed_at": "2026-09-16 00:00:00 UTC",
                        "package_hash": "cl4491a082b1",
                        "entries": ["EXPEDIENTE CEN INGESTADO: Res. Exenta N° 842 locked."]
                    }
                ]
            },
            "CEN-002": {"title": "Ajuste de Protecciones Subestación Kimal", "priority": "P2 - ALTO", "base_daily_bleed": 31200},
            "CEN-003": {"title": "Verificación Filtro STATCOM Cardones", "priority": "P3 - MEDIO", "base_daily_bleed": 14000},
            "CEN-004": {"title": "Monitoreo Térmico Línea 2x500kV", "priority": "P4 - MONITOREADO", "base_daily_bleed": 5600},
            "CEN-005": {"title": "Sincronización AGC Despacho Atacama", "priority": "P5 - MONITOREADO", "base_daily_bleed": 4200}
        }
    },
    "RTE & Enedis | Substation Storage (France)": {
        "currency": "€",
        "asset_cap": 210_000_000,
        "baseline_docket": "RTE Schéma Régional de Raccordement (SRADDET #FR-901)",
        "baseline_date": "16 Sep 2026",
        "statute": "Code de Commerce Art. L225-251 (Protection Dirigeant)",
        "directors": {"Xavier Piechaczyk": {"seat": "Président du Directoire"}},
        "incidents": {
            "RTE-BESS-01": {
                "title": "Blocage d'Injection Haute Tension Poste 400kV",
                "priority": "P1 - CRITIQUE",
                "base_daily_bleed": 68000,
                "days_in_deadlock": 8,
                "status": "DEADLOCKED",
                "director_seat": "Xavier Piechaczyk",
                "counterparty": {
                    "name": "Systèmes Électriques Provence SAS",
                    "contract": "Marché d'Interconnexion BESS Haute Tension #RTE-992",
                    "clause_invoked": "Article 15.2 (Exonération Aléas Réseau)",
                    "breach_clause": "Cahier des Clauses Spéciales § 11 (Pénalités d'Indisponibilité)"
                },
                "tier3_work_order": {
                    "id": "WO-RTE-881",
                    "title": "Attestation d'Injectabilité Réseau Nucléaire",
                    "target_gate": "Validation Enedis/RTE Poste 400kV",
                    "contractor": "Équipe Haute Tension RTE Provence",
                    "field_lead": "Ing. Marc Lefèvre",
                    "progress_pct": 60,
                    "remediation_protocol": "Résolution de directoire exonérant l'ingénieur en chef sous l'article L225-251.",
                    "steps": [
                        {"task": "Contrôle Automatisme Fréquence 50Hz", "done": True, "evidence": "Test îlotage 50.02 Hz conforme"},
                        {"task": "Vérification Puissance Réactive", "done": True, "evidence": "Régulation cos phi 0.98"},
                        {"task": "Homologation Téléaction SCADA", "done": False, "evidence": "Attente signature directoire"}
                    ],
                    "telemetry": [
                        {"param": "Stabilité Fréquence 50Hz", "val": "50.02 Hz", "status": "NOMINAL", "limit": "50.00 ± 0.05 Hz"},
                        {"param": "Taux Harmoniques Rang 5/7", "val": "1.8%", "status": "NOMINAL", "limit": "< 3.0%"},
                        {"param": "Téléaction SCADA Enedis", "val": "BLOQUÉE", "status": "WARN", "limit": "Autorisation requise"}
                    ]
                },
                "forensic_timeline": [
                    {"time": "2026-09-08 09:12:00 UTC", "party": "Poste 400kV", "event": "Refus de couplage suite à signal téléaction erroné."},
                    {"time": "2026-09-08 10:00:00 UTC", "party": "Constructeur SAS", "event": "Le constructeur invoque l'Art. 15.2 en prétextant une fluctuation de la centrale voisine."},
                    {"time": "2026-09-08 11:30:00 UTC", "party": "Oscilloperturbographe", "event": "La preuve brute montre que la passerelle de conversion du constructeur s'est désynchronisée."},
                    {"time": "2026-09-16 00:00:00 UTC", "party": "Moteur Forensique", "event": "8 jours de retard totalisant 544 000 € de pénalités contractuelles dues."}
                ],
                "audit_packages": [
                    {
                        "job_id": "JOB-001: Dossier RTE Verrouillé",
                        "status": "SEALED & ATTESTED",
                        "sealed_at": "2026-09-16 00:00:00 UTC",
                        "package_hash": "fr7710a902d3",
                        "entries": ["SRADDET INGESTION: Dossier RTE #FR-901 homologué."]
                    }
                ]
            },
            "RTE-002": {"title": "Compensation Puissance Réactive Provence", "priority": "P2 - HAUT", "base_daily_bleed": 42000},
            "RTE-003": {"title": "Synchronisation Îlotage Nucléaire/BESS", "priority": "P3 - MOYEN", "base_daily_bleed": 18500},
            "RTE-004": {"title": "Contrôle Automatisme Fréquence 50Hz", "priority": "P4 - SURVEILLÉ", "base_daily_bleed": 7200},
            "RTE-005": {"title": "Inspection Télécom SCADA Enedis", "priority": "P5 - SURVEILLÉ", "base_daily_bleed": 5100}
        }
    },
    "TEPCO Holdings | Transmission Grid (Japan)": {
        "currency": "¥",
        "asset_cap": 42_000_000_000,
        "baseline_docket": "METI Electricity Grid Intertie Filing #TK-402",
        "baseline_date": "16 Sep 2026",
        "statute": "Japanese Companies Act Art. 423 (Fiduciary Defense Shield)",
        "directors": {"Keisuke Yokoo": {"seat": "Chairman of the Board"}},
        "incidents": {
            "TEPCO-500KV-01": {
                "title": "Shin-Shinano 500kV Frequency Converter Synchronization Stall",
                "priority": "P1 - CRITICAL",
                "base_daily_bleed": 125280,
                "days_in_deadlock": 10,
                "status": "DEADLOCKED",
                "director_seat": "Keisuke Yokoo",
                "counterparty": {
                    "name": "Kanto High-Voltage Engineering KK",
                    "contract": "Shin-Shinano 500kV Intertie EPC Master Agreement #TK-881",
                    "clause_invoked": "免責条項第12条 (系統外擾による免責)",
                    "breach_clause": "基本契約第28条 (遅延損害賠償履行義務)"
                },
                "tier3_work_order": {
                    "id": "WO-TEPCO-4410",
                    "title": "周波数変換設備 (FC) 50Hz/60Hz連系実証試験",
                    "target_gate": "経産省 METI 系統連系最終承認",
                    "contractor": "東京電力パワーグリッド 送電技術部",
                    "field_lead": "主任技術者 佐藤 健一",
                    "progress_pct": 70,
                    "remediation_protocol": "会社法423条に基づく取締役会免責決議の執行および主任技術者のデジタル印鑑捺印。",
                    "steps": [
                        {"task": "50Hz/60Hz 変換バッファ過渡応答確認", "done": True, "evidence": "周波数追従 PASS"},
                        {"task": "ガス絶縁開閉装置 (GIS) 圧力実測", "done": True, "evidence": "SF6 圧力 0.58 MPa 正常"},
                        {"task": "主任技術者 デジタル印鑑捺印および経産省提出", "done": False, "evidence": "取締役会免責決議待ち"}
                    ],
                    "telemetry": [
                        {"param": "周波数偏差 (50Hz側)", "val": "±0.02 Hz", "status": "NOMINAL", "limit": "±0.10 Hz以内"},
                        {"param": "変換ロス率", "val": "1.42%", "status": "NOMINAL", "limit": "< 1.80%"},
                        {"param": "系統連系ゲートウェイ", "val": "承認待機", "status": "WARN", "limit": "捺印後即時送電可能"}
                    ]
                },
                "forensic_timeline": [
                    {"time": "2026-09-06 10:00:00 JST", "party": "新信濃変電所", "event": "周波数変換連系テスト中に制御保護装置が誤作動停止。"},
                    {"time": "2026-09-06 14:00:00 JST", "party": "設備施工業者", "event": "施工業者が免責条項第12条を主張し、50Hz系統側の電圧動揺が原因と報告。"},
                    {"time": "2026-09-06 16:30:00 JST", "party": "オシログラフィ記録", "event": "ミリ秒データ解析により、系統電圧は規定値内であり停止原因がインバータ設定値の入力ミスであることを立証。"},
                    {"time": "2026-09-16 00:00:00 JST", "party": "監査エンジン", "event": "10日間の停止損失：契約第28条に基づき ¥1,252,800 の損害賠償を確定。"}
                ],
                "audit_packages": [
                    {
                        "job_id": "JOB-001: METI Baseline Ingestion",
                        "status": "SEALED & ATTESTED",
                        "sealed_at": "2026-09-16 00:00:00 UTC",
                        "package_hash": "jp8834f109a12c7",
                        "entries": ["METI INTERTIE FILING: Shin-Shinano 500kV locked."]
                    }
                ]
            },
            "TEP-002": {"title": "Transformer Bushing Tan-Delta Spike", "priority": "P2 - HIGH", "base_daily_bleed": 73440},
            "TEP-003": {"title": "50Hz/60Hz Intertie Buffer Calibration", "priority": "P3 - MODERATE", "base_daily_bleed": 34560},
            "TEP-004": {"title": "SF6 Gas Pressure Telemetry Recalibration", "priority": "P4 - MONITORED", "base_daily_bleed": 12960},
            "TEP-005": {"title": "Substation Seismic Isolator Verification", "priority": "P5 - MONITORED", "base_daily_bleed": 17280}
        }
    }
}

# Keep the hardware interlock state explicit for every incident that has a Tier 3 work order.
for sector_data in SECTORS.values():
    for incident_data in sector_data["incidents"].values():
        if "tier3_work_order" in incident_data:
            incident_data.setdefault("manual_pe_bypass", False)

if "app_state" not in st.session_state:
    st.session_state.app_state = SECTORS

if "selected_incident_id" not in st.session_state:
    st.session_state.selected_incident_id = "INC-001"

if "conference_focus" not in st.session_state:
    st.session_state.conference_focus = "DEFAULT"

def append_to_active_package(incident: dict, job_title: str, event_text: str, force_new_package=False):
    packages = incident.setdefault("audit_packages", [])
    now_str = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    if force_new_package or not packages or packages[-1]["status"] == "SEALED & ATTESTED":
        new_hash = hashlib.sha256(f"{now_str}|{job_title}|{event_text}".encode()).hexdigest()[:15]
        packages.append({
            "job_id": job_title,
            "status": "ACTIVE AUDIT IN PROGRESS",
            "opened_at": now_str,
            "package_hash": new_hash,
            "entries": [f"[{now_str}] {event_text}"]
        })
    else:
        active_pkg = packages[-1]
        active_pkg["entries"].append(f"[{now_str}] {event_text}")
        combined = active_pkg["package_hash"] + event_text
        active_pkg["package_hash"] = hashlib.sha256(combined.encode()).hexdigest()[:15]

def seal_active_package(incident: dict):
    packages = incident.get("audit_packages", [])
    if packages and packages[-1]["status"] == "ACTIVE AUDIT IN PROGRESS":
        packages[-1]["status"] = "SEALED & ATTESTED"
        packages[-1]["sealed_at"] = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

def execute_unified_circuit_breaker(incident: dict, statute: str, daily_bleed: float):
    incident["status"] = "RESOLVED"
    incident["director_signed"] = True
    incident["manual_pe_bypass"] = True
    incident["base_daily_bleed"] = 0
    wo = incident.get("tier3_work_order", {})
    wo["progress_pct"] = 100
    if wo.get("steps"):
        for s in wo["steps"]:
            s["done"] = True
    for sig in incident.get("legal_instrument", {}).get("signatories", []):
        if "Director" in sig.get("role", ""):
            sig["status"] = "COUNTERSIGNED & SEALED"
        elif "Engineer" in sig.get("role", ""):
            sig["status"] = "DIGITAL STAMP TRANSMITTED"
    append_to_active_package(
        incident,
        f"JOB-{len(incident.get('audit_packages', []))+1:03d}: Unified Circuit Breaker Directive",
        f"UNIFIED EXECUTIVE DIRECTIVE: Faced with {daily_bleed:,.0f}/Day holding bleed, Chairman halted burn across Branch 1 (Field Access Cleared), Branch 3 (Directorate Safe Harbor Enforced under {statute}), and Tier 3 (PE Digital Stamp Transmitted).",
        force_new_package=True
    )

def reset_incident_to_neutral(incident: dict):
    incident["status"] = "DEADLOCKED"
    incident["director_signed"] = False
    incident["manual_pe_bypass"] = False
    incident["base_daily_bleed"] = 87264
    wo = incident.get("tier3_work_order", {})
    wo["progress_pct"] = 75
    if wo.get("steps"):
        for s in wo["steps"][:-1]: s["done"] = True
        wo["steps"][-1]["done"] = False
    for sig in incident.get("legal_instrument", {}).get("signatories", []):
        if "Director" in sig.get("role", ""):
            sig["status"] = "PENDING DIRECTOR COUNTERSIGNATURE"
        elif "Engineer" in sig.get("role", ""):
            sig["status"] = "HELD PENDING INDEMNITY"
    append_to_active_package(
        incident,
        f"JOB-{len(incident.get('audit_packages', []))+1:03d}: Neutral Counterfactual Reset",
        "Executive counterfactual reset executed. Holding burn re-engaged for alternative branch simulation.",
        force_new_package=True
    )

def ensure_legal_artifacts(incident: dict, sector: dict):
    counterparty = incident.get("counterparty", {})
    work_order = incident.get("tier3_work_order", {})
    lead = work_order.get("field_lead", "Lead Professional Engineer")
    daily_bleed = incident.get("base_daily_bleed", 0)
    days_deadlocked = incident.get("days_in_deadlock", 0)
    claim_amount = daily_bleed * days_deadlocked

    incident.setdefault("legal_instrument", {
        "title": "DIRECTORATE INDEMNITY & STATUTORY HOLD-HARMLESS RESOLUTION",
        "authority": sector.get("statute", "Applicable corporate governance statute"),
        "effective_date": f"{TODAY_STR} 00:00:00 UTC",
        "recitals": [
            f"WHEREAS, the operating asset is sustaining a daily holding bleed of {sector.get('currency', '$')}{daily_bleed:,.0f};",
            "WHEREAS, recorded telemetry establishes that the physical remediation is within the applicable operating threshold;",
            f"WHEREAS, Lead Professional Engineer {lead} requires corporate protection before executing the pending attestation;"
        ],
        "operative_resolution": (
            f"NOW, THEREFORE, BE IT RESOLVED: The corporation indemnifies and holds harmless {lead} "
            f"for the pending attestation and assumes responsibility for disputed claims under "
            f"{counterparty.get('clause_invoked', 'the applicable warranty clause')}."
        ),
        "signatories": [
            {"role": "Cognizant Director", "name": incident.get("director_seat", "Executive Board"), "status": "PENDING DIRECTOR COUNTERSIGNATURE", "hash": "sha256:pending-director-attestation"},
            {"role": "Lead Professional Engineer", "name": lead, "status": "DIGITAL STAMP PENDING", "hash": "sha256:pending-field-stamp"}
        ]
    })
    incident.setdefault("exhibits", [
        {
            "code": "EXHIBIT A-1",
            "title": "Primary Telemetry and Fault Recorder Extract",
            "filename": f"{incident.get('title', 'INCIDENT').replace(' ', '_')[:32]}_TELEMETRY.DAT",
            "size": "Authenticated source extract",
            "sha256": hashlib.sha256(f"{sector.get('baseline_docket')}|telemetry".encode()).hexdigest(),
            "significance": "Establishes the physical operating condition and separates equipment behavior from the contractual delay."
        },
        {
            "code": "EXHIBIT B-1",
            "title": "Counterparty Access and Notice Log",
            "filename": f"{incident.get('title', 'INCIDENT').replace(' ', '_')[:32]}_ACCESS_LOG.CSV",
            "size": "Authenticated source extract",
            "sha256": hashlib.sha256(f"{counterparty.get('name')}|access".encode()).hexdigest(),
            "significance": "Records counterparty presence, notice, or non-performance relevant to the asserted contractual defense."
        },
        {
            "code": "EXHIBIT C-1",
            "title": "Liquidated Delay Damages Ledger",
            "filename": f"{incident.get('title', 'INCIDENT').replace(' ', '_')[:32]}_DAMAGES_LEDGER.PDF",
            "size": "Authenticated calculation",
            "sha256": hashlib.sha256(f"{daily_bleed}|{days_deadlocked}|{claim_amount}".encode()).hexdigest(),
            "significance": f"Calculates the asserted delay exposure as {sector.get('currency', '$')}{daily_bleed:,.0f} per day for {days_deadlocked} days."
        }
    ])

# =========================================================
# 3. SIDEBAR NAVIGATION
# =========================================================
with st.sidebar:
    st.markdown("### 🏛️ COMMAND POST")
    
    lang_choice = st.selectbox(
        "Localization / Language Agent Coverage:",
        list(I18N.keys())
    )
    t = I18N[lang_choice]
    
    st.markdown("""
        <div style="background: rgba(88, 166, 255, 0.08); border: 1px solid #30363d; border-radius: 6px; padding: 10px; margin-bottom: 12px; font-size: 0.85rem; line-height: 1.4;">
            <strong style="color: #58a6ff;">Sovereign Coverage Roster:</strong><br>
            🇺🇸 USA · 🇬🇧 UK · 🇦🇺 AUS · 🇩🇪 DEU · 🇯🇵 JPN · 🇨🇱 CHL · 🇧🇷 BRA · 🇫🇷 FRA
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"<div style='font-size:0.95rem; color:#c9d1d9; margin-bottom:12px;'>{t['sub_app']}</div>", unsafe_allow_html=True)
    
    active_sector = st.selectbox("Operating Book (Global Assets):", list(st.session_state.app_state.keys()))
    sector = st.session_state.app_state[active_sector]
    curr_sym = sector["currency"]
    
    calib_key = f"capex_override_{active_sector}"
    if calib_key not in st.session_state:
        st.session_state[calib_key] = int(sector["asset_cap"])
    current_calib_capex = st.session_state[calib_key]
    scale_factor = current_calib_capex / sector["asset_cap"]

    nav_options = [
        t["tier1_title"],
        t["tier2_title"],
        t["tier3_title"],
        t["tier4_title"]
    ]
    
    if "selected_view" not in st.session_state or st.session_state.selected_view not in nav_options:
        st.session_state.selected_view = t["tier1_title"]

    selected_view = st.radio(
        "Governance & Execution Console:",
        nav_options,
        index=nav_options.index(st.session_state.selected_view)
    )
    st.session_state.selected_view = selected_view
    
    st.divider()
    st.markdown("#### Active Incident Queue")
    for inc_key, inc_obj in sector["incidents"].items():
        is_sel = inc_key == st.session_state.selected_incident_id
        inc_daily = inc_obj.get("base_daily_bleed", 50000) * scale_factor
        inc_crossover = round(current_calib_capex / inc_daily, 1) if inc_daily > 0 else 999
        btn_label = f"{inc_obj.get('priority', 'P1')}: {inc_key}\n{inc_crossover}d Crossover"
        
        if st.button(btn_label, key=f"sb_{inc_key}", use_container_width=True, type="primary" if is_sel else "secondary"):
            st.session_state.selected_incident_id = inc_key
            st.session_state.conference_focus = "DEFAULT"
            st.session_state.selected_view = t["tier1_title"]
            st.rerun()

if st.session_state.selected_incident_id not in sector["incidents"]:
    st.session_state.selected_incident_id = list(sector["incidents"].keys())[0]

active_inc = sector["incidents"][st.session_state.selected_incident_id]
ensure_legal_artifacts(active_inc, sector)
is_resolved = active_inc.get("status") == "RESOLVED"
is_dir_signed = active_inc.get("director_signed", False) or is_resolved

# =========================================================
# 4. VIEW: PAGE 1 — PART ONE: TACTICAL COMMAND POST
# =========================================================
if selected_view == t["tier1_title"]:
    st.title(t["tier1_title"])

    if is_resolved:
        st.markdown("**ATTESTATION CONFIRMED:** Lead PE digital stamp received. Holding burn halted to $0/day.")
    elif is_dir_signed:
        st.markdown("**DIRECTOR CONCURRENCE ACTIVE:** Directorate countersigned indemnity. Advance to Tier 3 to release the PE stamp.")
    
    st.markdown(f"""
        <div style="background: rgba(88, 166, 255, 0.1); border: 1px solid #58a6ff; border-radius: 6px; padding: 10px 16px; margin-bottom: 16px; font-size: 1.05rem; display: flex; flex-wrap: wrap; gap: 16px; align-items: center;">
            <div>Asset: <strong style="color:#ffffff;">{active_sector}</strong></div>
            <div style="color:#58a6ff;">|</div>
            <div>Statute: <strong style="color:#58a6ff;">{sector['statute']}</strong></div>
            <div style="color:#58a6ff;">|</div>
            <div>Date: <strong style="color:#ffffff;">{TODAY_STR}</strong></div>
        </div>
    """, unsafe_allow_html=True)
    
    ts_key = f"capex_ts_{active_sector}"
    if ts_key not in st.session_state:
        st.session_state[ts_key] = f"{TODAY_STR} 00:00 UTC"
        
    # ---------------------------------------------------------
    # COMMAND GATEWAY: CONTEXT, STATUS, THEN ACTION
    # ---------------------------------------------------------
    with st.container(border=True):
        parsed_current_capex = st.session_state[calib_key]
        is_overridden = parsed_current_capex != sector["asset_cap"]
        badge_color = "#e3b341" if is_overridden else "#58a6ff"
        badge_label = t["override_active"] if is_overridden else t["baseline_synced"]

        st.markdown(f"""
            <div style="text-align: center; margin-bottom: 14px;">
                <div style="font-size:1.05rem; font-weight:700; color:#58a6ff; letter-spacing:0.05em; text-transform:uppercase;">
                    ⚡ {active_sector} — {sector['baseline_docket']}
                </div>
                <div style="font-size:1.05rem; color:#c9d1d9; margin:6px 0;">
                    Statutory Baseline CapEx at Risk: <strong style="color:#ffffff; font-size:1.15rem;">{curr_sym}{sector['asset_cap']:,}</strong>
                    <span style="color:#58a6ff;">(Effective: {sector['baseline_date']})</span>
                </div>
                <div style="margin-top:4px; margin-bottom:14px;">
                    <span style="font-size:1.05rem; font-weight:800; color:{badge_color};">● {badge_label}</span>
                    <span style="color:#8b949e; font-size:0.95rem; font-weight:600; margin-left:8px;">
                        (Effective Audit Timestamp: {st.session_state[ts_key]})
                    </span>
                </div>
                <div style="height:1px; background:#30363d; margin:12px 0 16px 0;"></div>
                <div style="color:#ff4b4b; font-size:1.45rem; font-weight:900; letter-spacing:0.04em; text-transform:uppercase; line-height:1.3;">
                    🚨 {t['calib_red_header']}
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="capex-throttle">', unsafe_allow_html=True)
        raw_input_str = st.text_input(
            label="Chairman Quick-Calibrator Input",
            value=f"{st.session_state[calib_key]:,}",
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        parsed_capex = int(re.sub(r"[^\d]", "", raw_input_str) or sector["asset_cap"])
        
        if parsed_capex != st.session_state[calib_key]:
            now_str = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
            st.session_state[calib_key] = parsed_capex
            st.session_state[ts_key] = now_str
            seal_active_package(active_inc)
            append_to_active_package(
                active_inc,
                f"JOB-{len(active_inc.get('audit_packages', []))+1:03d}: CapEx Re-Calibration",
                f"Chairman re-calibrated exposure to {curr_sym}{parsed_capex:,}. Dynamic scaling enforced.",
                force_new_package=True
            )
            st.rerun()

    # PRIMARY EXECUTIVE METRICS DIRECTLY BELOW RECALIBRATION
    # ---------------------------------------------------------
    active_incidents = [i for i in sector["incidents"].values() if i.get("status") != "RESOLVED"]
    total_burn_day = sum(int(round(i.get("base_daily_bleed", 50000) * scale_factor)) for i in active_incidents)
    total_burn_wk = total_burn_day * 7
    dynamic_crossover_days = round(parsed_capex / total_burn_day, 1) if total_burn_day > 0 else 999.9

    k1, k2, k3 = st.columns(3)
    with k1:
        if not is_resolved:
            st.markdown(f"""
                <div class="circuit-breaker-card">
                    <div class="exec-metric-label">{t['holding_burn']} ({TODAY_STR})</div>
                    <div class="exec-metric-val" style="color:#f85149;">{curr_sym}{total_burn_wk:,.0f} <span style="font-size:1.05rem; font-weight:600; color:#c9d1d9;">/ wk</span></div>
                    <div class="exec-metric-sub" style="color:#f85149; font-family:monospace; font-size:1.05rem; margin-bottom:8px;">↑ {curr_sym}{total_burn_day:,.0f} / Day</div>
                </div>
            """, unsafe_allow_html=True)
            st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)
            st.markdown('<div class="emergency-halt-btn">', unsafe_allow_html=True)
            button_label = f"{t['circuit_btn_line1']}\n{t['circuit_btn_line2']}"
            if st.button(button_label, use_container_width=True):
                execute_unified_circuit_breaker(active_inc, sector["statute"], total_burn_day)
                st.session_state.conference_focus = "DEFAULT"
                st.success("Unified directive executed. Capital defended across all branches.")
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            st.caption(f"<div style='text-align:center; color:#c9d1d9; font-size:0.9rem;'>{t['circuit_active_hint']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="circuit-defended-card">
                    <div class="exec-metric-label">{t['holding_burn']} ({TODAY_STR})</div>
                    <div class="exec-metric-val" style="color:#3fb950;">{curr_sym}0 <span style="font-size:1.05rem; font-weight:600; color:#c9d1d9;">/ wk</span></div>
                    <div class="exec-metric-sub" style="color:#3fb950; font-family:monospace; font-size:1.05rem; margin-bottom:8px;">{t['circuit_defended']}</div>
                </div>
            """, unsafe_allow_html=True)
            st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)
            if st.button("↩️ Revert to Neutral (Simulate Risk)", use_container_width=True):
                reset_incident_to_neutral(active_inc)
                st.warning("Bleed restored. Counterfactual analysis active.")
                st.rerun()
                
    with k2:
        st.markdown(f"""
            <div class="exec-metric-card">
                <div class="exec-metric-label">{t['cap_under_def']}</div>
                <div class="exec-metric-val">{curr_sym}{parsed_capex:,.0f}</div>
                <div class="exec-metric-sub" style="color:#3fb950; font-size:1.05rem;">↑ Escrow Intact</div>
            </div>
        """, unsafe_allow_html=True)
    with k3:
        st.markdown(f"""
            <div class="exec-metric-card">
                <div class="exec-metric-label">{t['active_block']}: {st.session_state.selected_incident_id}</div>
                <div class="exec-metric-val" style="color:#e3b341;">{dynamic_crossover_days} <span style="font-size:1.05rem; font-weight:600; color:#c9d1d9;">Days</span></div>
                <div class="exec-metric-sub" style="color:#e3b341; font-size:1.05rem;">{t['crossover_sub']}</div>
            </div>
        """, unsafe_allow_html=True)

    # SECONDARY ADMINISTRATIVE METRICS
    calibrated_toll_gate = max(25000, int(round(parsed_capex * 0.00085, -3)))
    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
    sub1, sub2 = st.columns(2)
    with sub1:
        st.markdown(f"""
            <div class="exec-metric-card-secondary">
                <div class="exec-metric-label" style="font-size:0.8rem; margin-bottom:2px;">{t['toll_fee']}</div>
                <div class="exec-metric-val-secondary">{curr_sym}{calibrated_toll_gate:,}</div>
                <div style="color:#3fb950; font-size:0.85rem; font-weight:600;">{t['escrow_desc']}</div>
            </div>
        """, unsafe_allow_html=True)
    with sub2:
        st.markdown(f"""
            <div class="exec-metric-card-secondary">
                <div class="exec-metric-label" style="font-size:0.8rem; margin-bottom:2px;">{t['session_window']}</div>
                <div class="exec-metric-val-secondary">09:42</div>
                <div style="color:#3fb950; font-size:0.85rem; font-weight:600;">{t['session_desc']}</div>
            </div>
        """, unsafe_allow_html=True)

    # ---------------------------------------------------------
    # DIAGNOSTIC AGENT CONFERENCE
    # ---------------------------------------------------------
    with st.container(border=True):
        st.markdown("### 🎙️ Instant Diagnostic Agent Conference")
        diag_col1, diag_col2, diag_col3 = st.columns([1, 1, 2])
        with diag_col1:
            if st.button(t["why_stalled"], use_container_width=True, type="primary" if st.session_state.conference_focus == "WHY_STALLED" else "secondary"):
                st.session_state.conference_focus = "WHY_STALLED"
                append_to_active_package(active_inc, "DIAGNOSTIC", "Inquiry: Why is the fix stalled?")
                st.rerun()
        with diag_col2:
            if st.button(t["what_unblocks"], use_container_width=True, type="primary" if st.session_state.conference_focus == "WHAT_UNBLOCKS" else "secondary"):
                st.session_state.conference_focus = "WHAT_UNBLOCKS"
                append_to_active_package(active_inc, "DIAGNOSTIC", "Inquiry: What formal legal document unblocks the gate?")
                st.rerun()
        with diag_col3:
            custom_query = st.text_input("3. Custom Interrogation Query", placeholder=t["interrogate_hint"], label_visibility="collapsed")
            if custom_query:
                st.session_state.conference_focus = "CUSTOM"
                st.session_state.custom_query_text = custom_query
                append_to_active_package(active_inc, "DIAGNOSTIC", f"Custom: '{custom_query}'")
            
        st.markdown("---")
        if st.session_state.conference_focus == "WHY_STALLED":
            st.markdown(
                f"🔴 **Master Orchestrator ➔ Telemetry Agent:** *'Interrogating incident {st.session_state.selected_incident_id}.'* \n\n"
                f"🔴 **Telemetry Agent:** *'Physical telemetry is nominal (THD 4.1% < 5.0%). OEM field contractor holds attestation behind Clause 14.b warranty disclaimer. Deadlock is contractual, not physical.'*"
            )
        elif st.session_state.conference_focus == "WHAT_UNBLOCKS":
            inst = active_inc.get("legal_instrument", {})
            st.markdown(
                f"🟢 **Master Orchestrator ➔ Fiduciary Shield Agent:** *'What formal legal document unblocks this gate?'* \n\n"
                f"🟢 **Fiduciary Shield Agent:** *'The **{inst.get('title', 'Board Resolution')}** pursuant to **{inst.get('authority', sector['statute'])}**.'* \n\n"
                f"📄 **Plain-English Document Summary:** The company formally absorbs the disputed liability from the field engineer, authorizes the pending digital stamp, and creates a documented corporate reliance trail."
            )
            with st.expander("🔎 Inspect Primary Legal Document & Executed Signatures", expanded=True):
                st.markdown(f"""
                    <div class="legal-document-box">
                        <div class="legal-header">🏛️ Primary Legal Document: {inst.get('title')}</div>
                        <div style="font-size:0.95rem; color:#8b949e; margin-bottom:14px;">
                            Statutory Authority: <strong style="color:#ffffff;">{inst.get('authority')}</strong> |
                            Effective: <strong style="color:#58a6ff;">{inst.get('effective_date')}</strong>
                        </div>
                        <div style="font-style:italic; margin-bottom:12px;">{'<br><br>'.join(inst.get('recitals', []))}</div>
                        <div style="background:rgba(88,166,255,0.08); padding:12px; border-radius:4px; font-weight:bold; margin-bottom:16px;">
                            {inst.get('operative_resolution')}
                        </div>
                        <div style="font-family:-apple-system, sans-serif; font-size:0.9rem; border-top:1px solid #30363d; padding-top:10px;">
                            <strong style="color:#58a6ff;">EXECUTED DIGITAL SIGNATURES & VERIFICATION HASHES:</strong><br>
                            {'<br>'.join([f"• <strong>{s['role']}</strong>: {s['name']} — <span style='color:#3fb950;'>{s['status']}</span> (<code>{s.get('hash', 'N/A')}</code>)" for s in inst.get('signatories', [])])}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        elif st.session_state.conference_focus == "CUSTOM":
            st.markdown(f"🔍 **Agent Synthesis for Query: '{st.session_state.get('custom_query_text', '')}'**")
            st.info(f"Cross-referencing telemetry logs against {sector['statute']}. Primary bottleneck remains contractual signatory deadlock on {st.session_state.selected_incident_id}.")
        else:
            st.markdown(
                f"⚡ **Active Interrogation Standby ({TODAY_STR}):** Agents synchronized with {sector['statute']} and physical telemetry. Select an action above or tap the Holding Burn Circuit Breaker to halt exposure."
            )

    # ---------------------------------------------------------
    # THE THREE CASCADING BRANCHES (ACCOUNTABILITY HEATMAP)
    # ---------------------------------------------------------
    st.markdown(f"### {t['branches_title']}")
    b_col1, b_col2, b_col3 = st.columns(3)

    def render_branch_card(title, domain, director_name, agent_name, status_badge, metric_txt, card_type):
        border_col = "#2ea043" if card_type == "green" else ("#e3b341" if card_type == "amber" else "#da3633")
        bg_col = "rgba(46, 160, 67, 0.18)" if card_type == "green" else ("rgba(227, 179, 65, 0.18)" if card_type == "amber" else "rgba(218, 54, 51, 0.18)")
        
        return f"""
        <div style="background-color: {bg_col}; border: 2px solid {border_col}; border-radius: 8px; padding: 22px; height: 100%; display: flex; flex-direction: column; gap: 14px;">
            <h3 style="margin:0; color:#ffffff; font-size:1.4rem; font-weight:800;">{title}</h3>
            <div style="color:#ffffff; font-size:1.15rem; font-weight:700; border-bottom: 1px solid #30363d; padding-bottom: 10px; margin-bottom: 4px;">
                {domain}
            </div>
            <div style="font-size:1.0rem; color:#c9d1d9;">
                Cognizant Director: <br>
                <strong style="color:#ffffff; font-size:1.3rem; display:inline-block; margin-top:4px;">{director_name}</strong>
            </div>
            <div style="font-size:1.0rem; color:#c9d1d9;">
                Embedded Agent: <br>
                <code style="color:#a5d6ff; background:rgba(56,139,253,0.25); padding:4px 8px; font-size:1.0rem; border-radius:4px; display:inline-block; margin-top:4px;">{agent_name}</code>
            </div>
            <div style="font-weight:700; font-size:1.2rem; padding: 14px 16px; background: rgba(0,0,0,0.4); border-radius: 6px; border-left: 6px solid {border_col}; color:#ffffff; margin-top:4px;">
                {status_badge}
            </div>
            <div style="font-family:ui-monospace, monospace; color:#ffffff; font-size:1.1rem; font-weight:600; margin-top: auto; padding-top: 10px;">
                {metric_txt}
            </div>
        </div>
        """

    with b_col1:
        c_type = "green" if is_resolved else "red"
        s_badge = "🟢 CLEARED: Field access granted." if is_resolved else "🔴 OUTSTANDING: Field access locked."
        wo_id = active_inc.get("tier3_work_order", {}).get("id", "N/A")
        wo_pct = 100 if is_resolved else active_inc.get("tier3_work_order", {}).get("progress_pct", 0)
        st.markdown(render_branch_card("Branch 1: Physical / Field", "Hardware Gate | Plant & Crews", active_inc.get("director_seat", "Technical Integrity"), "Site Telemetry Agent", s_badge, f"Work Order: {wo_id} ({wo_pct}%)", c_type), unsafe_allow_html=True)

    with b_col2:
        c_type = "green" if is_resolved else "amber"
        s_badge = "🟢 CLEARED: Grid filing secured." if is_resolved else "🟡 COLLATERAL: 48h Window Expiring."
        st.markdown(render_branch_card("Branch 2: Regulatory / Market", "Commercial Gate | Interconnection", "David Chen (Proxy)", "Market Surveillance Agent", s_badge, "Handshake Status: Latency Validated", c_type), unsafe_allow_html=True)

    with b_col3:
        c_type = "green" if is_resolved else "red"
        s_badge = "🟢 CLEARED: Capital defended." if is_resolved else f"🔴 OUTSTANDING: Crossover in {dynamic_crossover_days}d."
        vel_txt = f"Bleed: {curr_sym}0 / Day" if is_resolved else f"Bleed: {curr_sym}{total_burn_day:,.0f} / Day"
        st.markdown(render_branch_card("Branch 3: Fiduciary / Capital", "Balance Sheet Gate | Liability Escrow", "Executive Board Chair", "Fiduciary Shield Agent", s_badge, vel_txt, c_type), unsafe_allow_html=True)

    # ---------------------------------------------------------
    # SINGLE-LINE DESCENDING OPERATIONAL CHAIN OF COMMAND
    # ---------------------------------------------------------
    st.markdown("### 📡 Operational Chain of Command (Single-Line Descending Hierarchy)")
    st.caption("Inspect and drill directly into Directorate governance and Tier 3 field desks:")
    
    first_dir = list(sector["directors"].keys())[0]
    
    with st.container(border=True):
        st.markdown(f"""
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px;">
                <div>
                    <div style="font-weight:800; color:#58a6ff; font-size:1.2rem;">🏛️ Level 1: Directorate Governance Desk</div>
                    <div style="font-size:1.0rem; color:#c9d1d9; margin-top:4px;">
                        Cognizant Director: <strong style="color:#ffffff;">{active_inc.get('director_seat', 'Board')}</strong> | 
                        Statutory Shield: <strong style="color:#58a6ff;">{sector['statute']}</strong>
                    </div>
                </div>
                <div style="font-size:1.1rem; font-weight:800; color:{'#3fb950' if is_resolved else '#e3b341'};">
                    ● {'DIRECTORATE INDEMNITY SEALED' if is_resolved else 'AWAITING CHAIRMAN DIRECTIVE'}
                </div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)
        if st.button("🏛️ Drill Down to Tier 2: Directorate Governance Desk", use_container_width=True):
            st.session_state.selected_view = t["tier2_title"]
            st.rerun()

    wo = active_inc.get("tier3_work_order", {})
    with st.container(border=True):
        st.markdown(f"""
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px;">
                <div>
                    <div style="font-weight:800; color:#e3b341; font-size:1.2rem;">👷 Level 2: Tier 3 Site Operations & Remediation Desk</div>
                    <div style="font-size:1.0rem; color:#c9d1d9; margin-top:4px;">
                        Work Order: <strong style="color:#ffffff;">{wo.get('id', 'N/A')} ({wo.get('title', 'Telemetry')})</strong> | 
                        Progress: <strong style="color:#ffffff;">{wo.get('progress_pct', 0)}% Completed</strong>
                    </div>
                </div>
                <div style="font-size:1.1rem; font-weight:800; color:{'#3fb950' if is_resolved else '#da3633'};">
                    ● {'PE DIGITAL STAMP TRANSMITTED' if is_resolved else 'BLOCKED BEHIND CLAUSE 14.b'}
                </div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)
        if st.button("⚡ Drill Down to Tier 3 Operator Remediation Desk", use_container_width=True, type="primary"):
            st.session_state.selected_view = t["tier3_title"]
            st.rerun()

    # ---------------------------------------------------------
    # PROGRESSION BRIDGE TO PART TWO FORENSIC VAULT
    # ---------------------------------------------------------
    st.markdown("---")
    if is_resolved:
        st.markdown(f"""
            <div style="background: rgba(46, 160, 67, 0.15); border: 2px solid #2ea043; border-radius: 8px; padding: 18px; text-align: center; margin-bottom: 12px;">
                <div style="font-size: 1.3rem; font-weight: 800; color: #3fb950; margin-bottom: 6px;">
                    ✅ P1 INCIDENT RESOLVED & CAPITAL SECURED
                </div>
                <div style="font-size: 1.05rem; color: #c9d1d9;">
                    Holding bleed halted to $0. Millisecond evidence locked. Advance to Part Two to generate the Pre-Litigation Cost Recovery Dossier.
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button(f"➔ Proceed to {t['tier4_title']}", use_container_width=True, type="primary"):
            st.session_state.selected_view = t["tier4_title"]
            st.rerun()
    else:
        st.info("💡 Incident INC-001 is actively bleeding capital. Tap the red Circuit Breaker above or execute operator sign-off at Tier 3 to defend capital and unlock Part Two.")

# =========================================================
# 5. VIEW: TIER 3 SITE OPERATIONS & OPERATOR REMEDIATION
# =========================================================
elif selected_view == t["tier3_title"]:
    st.title(f"👷 {t['tier3_title']}")
    wo = active_inc.get("tier3_work_order", {})
    st.caption(f"Asset: **{active_sector}** | Assigned Contractor: **{wo.get('contractor', 'Field Lead')}** | Lead PE: **{wo.get('field_lead', 'Engineering Lead')}**")
    
    if st.button("↩️ Return to Tier 1: Chairman Command Post", type="secondary"):
        st.session_state.selected_view = t["tier1_title"]
        st.rerun()
        
    st.divider()
    
    # 1. Operator Remediation Directive Banner
    st.markdown(f"""
        <div style="background: rgba(227, 179, 65, 0.15); border: 2px solid #e3b341; border-radius: 8px; padding: 18px; margin-bottom: 20px;">
            <div style="font-size:1.25rem; font-weight:800; color:#e3b341; margin-bottom:6px;">
                🎯 Operator Remediation Directive: {wo.get('target_gate', 'Gate Clearance')}
            </div>
            <div style="font-size:1.05rem; color:#f0f6fc; line-height:1.5;">
                {wo.get('remediation_protocol', 'Follow on-site engineering instructions and execute digital signature.')}
            </div>
        </div>
    """, unsafe_allow_html=True)

    t1, t2, t3 = st.columns(3)
    t1.metric("Active Work Order", wo.get("id", "N/A"), active_inc.get("priority", "CRITICAL"))
    t2.metric("Target Regulatory Gate", wo.get("target_gate", "COD Gate"))
    t3.metric("Hardware Execution Progress", f"{wo.get('progress_pct', 0)}%")
    
    col_t, col_m = st.columns([3, 2])
    with col_t:
        with st.container(border=True):
            st.markdown(f"#### Execution Punch List & Sign-Off: {wo.get('title', 'Tasks')}")
            for idx, step in enumerate(wo.get("steps", [])):
                st.markdown(f"""
                    <div style="padding: 10px; border-bottom: 1px solid #30363d;">
                        <span style="font-size: 1.15rem;">{'✅' if step['done'] else '⏳'}</span>
                        <strong style="color: #ffffff; font-size: 1.05rem; margin-left: 6px;">Step {idx+1}: {step['task']}</strong>
                        <div style="color: #8b949e; font-size: 0.95rem; margin-left: 28px;">Evidence: <code>{step.get('evidence', 'Verified')}</code></div>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)
            if not is_resolved:
                shield_badge = "🟢 Directorate Indemnity Shield Active" if is_dir_signed else "⚠️ Awaiting Directorate Countersignature"
                st.markdown(f"""
                    <div style="background: rgba(248, 81, 73, 0.12); border: 1px solid #f85149; border-radius: 6px; padding: 12px; margin-bottom: 12px; font-size: 0.95rem;">
                        <strong style="color:{'#3fb950' if is_dir_signed else '#e3b341'};">{shield_badge}</strong><br>
                        ⚠️ <strong>Signatory Trap Detected:</strong> Counterparty warranty disclaimer ({active_inc.get('counterparty', {}).get('clause_invoked', 'Clause 14.b')}) threatens personal liability for Lead PE upon unilateral sign-off.
                        Executing below absorbs liability under <strong>{sector['statute']}</strong>.
                    </div>
                """, unsafe_allow_html=True)
                if st.button("⚡ Transmit Lead PE Attestation Stamp & Seal Gate", use_container_width=True, type="primary", disabled=not is_dir_signed):
                    execute_unified_circuit_breaker(active_inc, sector["statute"], active_inc.get("base_daily_bleed", 87264))
                    st.session_state.selected_view = t["tier1_title"]
                    st.success("PE Stamp sealed. Attestation transmitted to grid operator. Holding burn halted to $0.")
                    st.rerun()
            else:
                st.success(f"✅ Work order completed at 100%. Professional Engineer stamp transmitted by {wo.get('field_lead', 'Lead PE')}.")
                if st.button("🔄 Reset Work Order to Neutral (Simulate Re-test)", use_container_width=True):
                    reset_incident_to_neutral(active_inc)
                    st.warning("Work order reset to 75% pending state.")
                    st.rerun()
                    
    with col_m:
        with st.container(border=True):
            st.markdown("#### Live Site Telemetry Waveform Sweep")
            st.caption("Millisecond-level dark data recorded at switchyard terminal:")
            for telem in wo.get("telemetry", []):
                val_col = "#3fb950" if telem["status"] == "NOMINAL" or telem["status"] == "COMPLIANT" else "#e3b341"
                st.markdown(f"""
                    <div style="background:#090d13; border:1px solid #30363d; border-radius:6px; padding:10px 14px; margin-bottom:10px;">
                        <div style="font-size:0.9rem; color:#8b949e; text-transform:uppercase;">{telem['param']}</div>
                        <div style="font-size:1.4rem; font-weight:800; font-family:monospace; color:{val_col}; margin: 2px 0;">{telem['val']}</div>
                        <div style="font-size:0.85rem; color:#c9d1d9;">Threshold: <strong>{telem['limit']}</strong></div>
                    </div>
                """, unsafe_allow_html=True)

            st.markdown("---")
            st.markdown("#### Hardware Physical Interlock Control")
            is_bypassed = active_inc.get("manual_pe_bypass", False) or is_resolved

            if not is_bypassed:
                st.markdown("""
                    <div style="background:#161b22; border:2px solid #e3b341; border-radius:6px; padding:12px 14px; margin-bottom:10px;">
                        <div style="font-size:0.85rem; color:#8b949e; text-transform:uppercase; font-weight:700;">OEM Cabinet Remote Interlock</div>
                        <div style="font-size:1.4rem; font-weight:900; font-family:monospace; color:#e3b341; margin:2px 0;">DISENGAGED</div>
                        <div style="font-size:0.85rem; color:#c9d1d9;">Status: <strong style="color:#f85149;">Manual PE Bypass Required (Cabinet Locked)</strong></div>
                    </div>
                """, unsafe_allow_html=True)
                if st.button("⚡ Engage Manual PE Hardware Bypass", use_container_width=True, type="secondary"):
                    active_inc["manual_pe_bypass"] = True
                    append_to_active_package(
                        active_inc,
                        "PHYSICAL BYPASS ENGAGED",
                        f"Lead PE {wo.get('field_lead', 'Engineering Lead')} engaged the on-site hardware bypass key. Remote interlock overridden."
                    )
                    st.success("Manual PE bypass engaged. Interlock overridden.")
                    st.rerun()
            else:
                st.markdown("""
                    <div style="background:rgba(46,160,67,0.15); border:2px solid #2ea043; border-radius:6px; padding:12px 14px; margin-bottom:10px;">
                        <div style="font-size:0.85rem; color:#8b949e; text-transform:uppercase; font-weight:700;">OEM Cabinet Remote Interlock</div>
                        <div style="font-size:1.4rem; font-weight:900; font-family:monospace; color:#3fb950; margin:2px 0;">BYPASSED &amp; ENERGIZED</div>
                        <div style="font-size:0.85rem; color:#c9d1d9;">Status: <strong style="color:#3fb950;">Hardware Safe (PE Bypass Key Active)</strong></div>
                    </div>
                """, unsafe_allow_html=True)
                if not is_resolved and st.button("↩️ Disengage Bypass Key (Restore Interlock)", use_container_width=True):
                    active_inc["manual_pe_bypass"] = False
                    append_to_active_package(
                        active_inc,
                        "PHYSICAL BYPASS DISENGAGED",
                        "On-site hardware bypass key disengaged. OEM remote interlock restored."
                    )
                    st.warning("Manual bypass disengaged. Interlock restored to locked state.")
                    st.rerun()

# =========================================================
# 6. VIEW: PAGE 2 — PART TWO: FORENSIC COST RECOVERY VAULT
# =========================================================
elif selected_view == t["tier4_title"]:
    st.title(f"⚖️ {t['tier4_title']}")
    st.markdown(f"""
        <div style="background: rgba(227, 179, 65, 0.1); border: 1px solid #e3b341; border-radius: 6px; padding: 10px 16px; margin-bottom: 16px; font-size: 1.05rem; display: flex; flex-wrap: wrap; gap: 16px; align-items: center;">
            <div>Target Entity: <strong style="color:#ffffff;">{active_inc.get('counterparty', {}).get('name', 'OEM Vendor')}</strong></div>
            <div style="color:#e3b341;">|</div>
            <div>Governing Contract: <strong style="color:#e3b341;">{active_inc.get('counterparty', {}).get('contract', 'EPC Agreement')}</strong></div>
            <div style="color:#e3b341;">|</div>
            <div>Format: <strong style="color:#ffffff;">Pre-Litigation Demand Package</strong></div>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("↩️ Return to Tier 1: Chairman Command Post", type="secondary"):
        st.session_state.selected_view = t["tier1_title"]
        st.rerun()
        
    st.divider()

    # ---------------------------------------------------------
    # TIER A: DIRECT CLAIM LEDGER & RECOVERY METRICS
    # ---------------------------------------------------------
    days_deadlocked = active_inc.get("days_in_deadlock", 7)
    scaled_daily = int(round(active_inc.get("base_daily_bleed", 87264) * scale_factor))
    if is_resolved:
        scaled_daily = int(round(87264 * scale_factor))
        
    total_claim_amount = scaled_daily * days_deadlocked
    idle_contractor_overhead = int(total_claim_amount * 0.42)
    grid_penalty_exposure = int(total_claim_amount * 0.38)
    capital_cost_carry = total_claim_amount - idle_contractor_overhead - grid_penalty_exposure

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
            <div class="claim-demand-card">
                <div class="exec-metric-label">{t['claim_total_label']}</div>
                <div class="exec-metric-val" style="color:#e3b341;">{curr_sym}{total_claim_amount:,.0f}</div>
                <div class="exec-metric-sub" style="color:#e3b341;">{t['claim_sub']}</div>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
            <div class="exec-metric-card">
                <div class="exec-metric-label">Assigned Liable Party</div>
                <div class="exec-metric-val" style="font-size:1.35rem; color:#f85149;">{active_inc.get('counterparty', {}).get('name', 'OEM Vendor')[:28]}</div>
                <div class="exec-metric-sub" style="color:#f85149;">100% Fault Attribution (Zero Shared Delay)</div>
            </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
            <div class="exec-metric-card">
                <div class="exec-metric-label">Enforcement Instrument</div>
                <div class="exec-metric-val" style="font-size:1.35rem; color:#58a6ff;">Standby Letter of Credit</div>
                <div class="exec-metric-sub" style="color:#58a6ff;">Direct Escrow Drawdown Ready</div>
            </div>
        """, unsafe_allow_html=True)

    # ---------------------------------------------------------
    # TIER B: FORENSIC MICRO-TIMELINE FLIGHT RECORDER
    # ---------------------------------------------------------
    st.markdown("---")
    st.markdown("### ⏱️ Forensic Micro-Timeline Flight Recorder (Physical Telemetry vs. Contractual Events)")
    st.caption("Millisecond-stamped evidentiary reconstruction linking physical machine exhaust to contractual default:")

    with st.container(border=True):
        for event in active_inc.get("forensic_timeline", []):
            st.markdown(f"""
                <div style="padding: 10px 14px; border-bottom: 1px solid #21262d; display: flex; flex-wrap: wrap; gap: 14px; align-items: baseline;">
                    <code style="color: #58a6ff; font-weight: 700; font-size: 0.95rem;">{event['time']}</code>
                    <span style="background: rgba(227, 179, 65, 0.2); color: #e3b341; padding: 2px 8px; border-radius: 4px; font-weight: 700; font-size: 0.85rem;">{event['party']}</span>
                    <span style="color: #f0f6fc; font-size: 1.05rem; flex-grow: 1;">{event['event']}</span>
                </div>
            """, unsafe_allow_html=True)

    # ---------------------------------------------------------
    # TIER C: PRIMARY EVIDENTIARY EXHIBIT INDEX
    # ---------------------------------------------------------
    st.markdown("---")
    st.markdown("### 📁 Primary Evidentiary Exhibit Index (Inspectable Audit Manifest)")
    st.caption("Underlying authenticated artifacts establishing physical causation and contractual breach:")

    for exh in active_inc.get("exhibits", []):
        with st.container(border=True):
            e_col1, e_col2 = st.columns([3, 1])
            with e_col1:
                st.markdown(f"""
                    <div style="font-weight:800; font-size:1.15rem; color:#58a6ff;">{exh['code']}: {exh['title']}</div>
                    <div style="font-size:0.95rem; color:#c9d1d9; margin:4px 0;">File: <code>{exh['filename']}</code> ({exh['size']})</div>
                    <div style="font-size:0.85rem; color:#8b949e; font-family:monospace;">SHA-256: {exh['sha256']}</div>
                    <div style="font-size:1.0rem; color:#f0f6fc; margin-top:8px;"><strong>Evidentiary Proof:</strong> {exh['significance']}</div>
                """, unsafe_allow_html=True)
            with e_col2:
                st.markdown("<div style='height:18px;'></div>", unsafe_allow_html=True)
                st.download_button(
                    label=f"⬇️ Download {exh['code']}",
                    data=f"AUTHENTICATED EXHIBIT {exh['code']}\nSHA-256: {exh['sha256']}\n{exh['significance']}".encode(),
                    file_name=exh["filename"],
                    mime="application/octet-stream",
                    use_container_width=True
                )

    # ---------------------------------------------------------
    # TIER D: THREE ATTRIBUTION PROOF PILLARS
    # ---------------------------------------------------------
    st.markdown("---")
    st.markdown("### 🏛️ The Three Attribution Proof Pillars (The Indisputable Case)")
    
    p_col1, p_col2, p_col3 = st.columns(3)
    with p_col1:
        st.markdown(f"""
            <div style="background-color: rgba(56, 139, 253, 0.12); border: 2px solid #58a6ff; border-radius: 8px; padding: 20px; height: 100%;">
                <h3 style="margin:0; color:#58a6ff; font-size:1.3rem;">1. Physical Causation</h3>
                <div style="color:#ffffff; font-weight:700; margin:8px 0;">Sub-Cycle Waveform Record</div>
                <p style="font-size:0.95rem; color:#c9d1d9;">
                    Raw 10 kHz oscillography demonstrates voltage remained within nominal ride-through envelope (4.1% THD). 
                    Disproves counterparty claim of external grid disturbance.
                </p>
                <div style="font-family:monospace; color:#58a6ff; font-weight:700; font-size:0.9rem;">
                    Status: HARDWARE EXONERATED
                </div>
            </div>
        """, unsafe_allow_html=True)
        
    with p_col2:
        st.markdown(f"""
            <div style="background-color: rgba(248, 81, 73, 0.12); border: 2px solid #f85149; border-radius: 8px; padding: 20px; height: 100%;">
                <h3 style="margin:0; color:#f85149; font-size:1.3rem;">2. Breached Covenant</h3>
                <div style="color:#ffffff; font-weight:700; margin:8px 0;">{active_inc.get('counterparty', {}).get('breach_clause', 'Schedule D')}</div>
                <p style="font-size:0.95rem; color:#c9d1d9;">
                    {active_inc.get('counterparty', {}).get('clause_invoked', 'Warranty Disclaimer')} is legally voided by evidence of off-site personnel.
                    Unexcused commissioning demurrage triggered in full under Schedule D.
                </p>
                <div style="font-family:monospace; color:#f85149; font-weight:700; font-size:0.9rem;">
                    Status: DEMURRAGE ACTIVE
                </div>
            </div>
        """, unsafe_allow_html=True)
        
    with p_col3:
        st.markdown(f"""
            <div style="background-color: rgba(46, 160, 67, 0.12); border: 2px solid #2ea043; border-radius: 8px; padding: 20px; height: 100%;">
                <h3 style="margin:0; color:#3fb950; font-size:1.3rem;">3. Assigned Liability</h3>
                <div style="color:#ffffff; font-weight:700; margin:8px 0;">{curr_sym}{total_claim_amount:,.0f} Reimbursable</div>
                <p style="font-size:0.95rem; color:#c9d1d9;">
                    • Standby Contractor Overhead: {curr_sym}{idle_contractor_overhead:,}<br>
                    • Grid Non-Performance Exposure: {curr_sym}{grid_penalty_exposure:,}<br>
                    • Capital Carrying Cost: {curr_sym}{capital_cost_carry:,}
                </p>
                <div style="font-family:monospace; color:#3fb950; font-weight:700; font-size:0.9rem;">
                    Recovery Target: 100% RECOUPMENT
                </div>
            </div>
        """, unsafe_allow_html=True)

    # ---------------------------------------------------------
    # TIER D: PRE-LITIGATION SETTLEMENT DEMAND EXPORT
    # ---------------------------------------------------------
    st.markdown("---")
    st.markdown("### 📦 Sealed Pre-Litigation Recovery Demand Package")
    st.caption("Cryptographically authenticated evidence dossier ready for General Counsel, Board of Directors, or Escrow Bank:")

    claim_hash = hashlib.sha256(f"{active_sector}|{active_inc.get('counterparty', {}).get('name')}|{total_claim_amount}".encode()).hexdigest()

    dossier_col1, dossier_col2 = st.columns([3, 1])
    with dossier_col1:
        st.markdown(f"""
            <div style="background:#161b22; border:1px solid #30363d; border-radius:6px; padding:16px;">
                <div style="color:#58a6ff; font-weight:800; font-size:1.15rem; margin-bottom:6px;">
                    DOSSIER: PRE-LITIGATION DEMAND & ESCROW DRAWDOWN NOTICE
                </div>
                <div style="font-size:0.95rem; color:#c9d1d9;">
                    Root Verification Hash: <code>SHA-256:{claim_hash}</code><br>
                    Authenticated Time-Lock: <strong>{TODAY_STR} 00:00:00 UTC</strong> | Jurisdiction: <strong>{sector['statute']}</strong><br>
                    Contents: Sub-cycle oscillography proof, turnstile badging logs, contract breach mapping, and liquidated damages ledger.
                </div>
            </div>
        """, unsafe_allow_html=True)
    with dossier_col2:
        st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)
        if st.button("📄 Export Authenticated Pre-Litigation Dossier", use_container_width=True, type="primary"):
            append_to_active_package(
                active_inc,
                f"JOB-{len(active_inc.get('audit_packages', []))+1:03d}: Pre-Litigation Claim Dossier Sealed",
                f"CLAIM SEALED: Formal pre-litigation recovery demand of {curr_sym}{total_claim_amount:,.0f} issued against {active_inc.get('counterparty', {}).get('name')} under {active_inc.get('counterparty', {}).get('breach_clause')}. Root Hash: SHA-256:{claim_hash[:15]}.",
                force_new_package=True
            )
            st.success("Dossier sealed and logged to immutable audit ledger.")
            st.rerun()

    # ---------------------------------------------------------
    # TIER E: PIPELINE & CRYPTOGRAPHIC AUDIT VAULT
    # ---------------------------------------------------------
    st.markdown("---")
    st.markdown(f"### {t['pipeline_title']}")
    
    pipe_keys = [k for k in sector["incidents"].keys() if k not in ["INC-001", "DB-ETCS-01", "CEN-BESS-01", "RTE-BESS-01", "TEPCO-500KV-01"]]
    p1, p2, p3, p4 = st.columns(4)
    def render_pipeline_card(num_title, raw_bleed, inc_code):
        scaled_d = int(round(raw_bleed * scale_factor))
        return f"""
        <div style="background-color:#161b22; border:2px solid #30363d; border-radius:8px; padding:16px; text-align:center;">
            <div style="font-weight:700; color:#ffffff;">{num_title}</div>
            <div style="font-family:monospace; font-size:1.4rem; font-weight:800; color:#ffffff; margin:4px 0;">{curr_sym}{scaled_d:,} / Day</div>
            <div style="color:#8b949e; font-size:0.9rem;">QUEUED: {inc_code}</div>
        </div>
        """
    with p1: st.markdown(render_pipeline_card("1. Inrush Damping", sector["incidents"].get(pipe_keys[0], {}).get("base_daily_bleed", 38880), pipe_keys[0]), unsafe_allow_html=True)
    with p2: st.markdown(render_pipeline_card("2. SCADA IEC 61850", sector["incidents"].get(pipe_keys[1], {}).get("base_daily_bleed", 15552), pipe_keys[1]), unsafe_allow_html=True)
    with p3: st.markdown(render_pipeline_card("3. BESS Firmware OTA", sector["incidents"].get(pipe_keys[2], {}).get("base_daily_bleed", 4320), pipe_keys[2]), unsafe_allow_html=True)
    with p4: st.markdown(render_pipeline_card("4. Substation Oil DGA", sector["incidents"].get(pipe_keys[3], {}).get("base_daily_bleed", 6912), pipe_keys[3]), unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"### {t['audit_title']}")
    for pkg in reversed(active_inc.get("audit_packages", [])):
        is_sealed = pkg["status"] == "SEALED & ATTESTED"
        badge_icon = "🔒" if is_sealed else "⚡"
        status_color = "#3fb950" if is_sealed else "#e3b341"
        with st.expander(f"{badge_icon} {pkg['job_id']} | Root Hash: SHA-256:{pkg['package_hash']}", expanded=True):
            st.markdown(f"**Status:** <span style='color:{status_color}; font-weight:bold; font-size:1.1rem;'>{pkg['status']}</span>", unsafe_allow_html=True)
            for entry in pkg.get("entries", []):
                st.markdown(f"<div style='font-size:1.05rem; font-family:monospace; margin:4px 0; color:#f0f6fc;'>• {entry}</div>", unsafe_allow_html=True)

# =========================================================
# 7. VIEW: TIER 2 — DIRECTORATE GOVERNANCE DESK
# =========================================================
elif selected_view == t["tier2_title"]:
    first_dir = list(sector["directors"].keys())[0]
    st.title(t["tier2_title"])
    inst = active_inc.get("legal_instrument", {})
    st.caption(f"Asset: **{active_sector}** | Cognizant Director: **{first_dir}** | Statute: **{sector['statute']}**")
    
    if st.button("↩️ Return to Tier 1: Chairman Command Post", type="secondary"):
        st.session_state.selected_view = t["tier1_title"]
        st.rerun()
        
    st.divider()
    gov_status = "INDEMNITY CONCURRED" if is_dir_signed else active_inc.get("status", "DEADLOCKED")
    st.metric("Governance State", gov_status, "SAFE HARBOR ACTIVE" if is_dir_signed else active_inc.get("priority", "P1"))
    
    with st.container(border=True):
        st.markdown(f"""
            <div class="legal-document-box">
                <div class="legal-header">📜 {inst.get('title')}</div>
                <p><strong>Statutory Authority:</strong> {inst.get('authority')}</p>
                <div style="font-style:italic; margin: 12px 0;">{'<br><br>'.join(inst.get('recitals', []))}</div>
                <div style="background:rgba(88,166,255,0.08); padding:12px; border-radius:4px; font-weight:bold; margin-bottom:14px;">
                    {inst.get('operative_resolution')}
                </div>
            </div>
        """, unsafe_allow_html=True)
        if not is_dir_signed:
            if st.button(f"✍️ Countersign Directorate Indemnity Resolution ({first_dir})", use_container_width=True, type="primary"):
                active_inc["director_signed"] = True
                for sig in inst.get("signatories", []):
                    if "Director" in sig.get("role", ""):
                        sig["status"] = "COUNTERSIGNED & RELIED"
                append_to_active_package(active_inc, "DIRECTOR CONCURRENCE", f"Formal fiduciary concurrence and reliance countersigned by {first_dir} under {sector['statute']}.")
                st.success("Resolution countersigned. Reliance documented under the applicable governance standard.")
                st.rerun()
        else:
            st.success(f"✅ Resolution active. Countersigned and attested by {first_dir}.")
            nav_col1, nav_col2 = st.columns(2)
            with nav_col1:
                if st.button("➔ Advance to Tier 3: Release PE Stamp", use_container_width=True, type="primary"):
                    st.session_state.selected_view = t["tier3_title"]
                    st.rerun()
            with nav_col2:
                if st.button("↩️ Return to Tier 1: Chairman Command Post", use_container_width=True):
                    st.session_state.selected_view = t["tier1_title"]
                    st.rerun()

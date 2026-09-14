import datetime
import hashlib
import json
import re
import streamlit as st

APP_BUILD_ID = "v3.5_red_command_gateway_sep15_2026"

if st.session_state.get("build_id") != APP_BUILD_ID:
    st.session_state.clear()
    st.session_state["build_id"] = APP_BUILD_ID

st.set_page_config(
    page_title="Command Post | Autonomous Capital Defense",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# 1. INDUSTRIAL HIGH-CONTRAST TYPOGRAPHY & THROTTLE INPUT
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
        
        /* Chairman Throttle Input: Oversized, Centered, High-Contrast */
        div[data-testid="stTextInput"] input {
            font-size: 2.5rem !important;
            font-weight: 800 !important;
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace !important;
            color: #ffffff !important;
            background-color: #090d13 !important;
            border: 2px solid #58a6ff !important;
            border-radius: 8px !important;
            padding: 14px 20px !important;
            text-align: center !important;
            box-shadow: 0 0 16px rgba(88, 166, 255, 0.25) !important;
        }
        div[data-testid="stTextInput"] input:focus {
            border-color: #ff4b4b !important;
            box-shadow: 0 0 22px rgba(255, 75, 75, 0.4) !important;
        }
        
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
    </style>
""", unsafe_allow_html=True)

# =========================================================
# 2. LOCALIZATION DICTIONARY & SOVEREIGN ROSTER
# =========================================================
I18N = {
    "English [USA · UK · Australia]": {
        "title": "Executive Chairman Command Post",
        "sub_app": "Autonomous Capital Defense Control Plane",
        "calib_red_header": "COMMAND GATEWAY: ENTER PROJECT BUDGET / CAPEX AT RISK (TAP TO RE-CALIBRATE)",
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
        "why_stalled": "🚨 1. Why is the Fix Stalled?",
        "what_unblocks": "🟢 2. What Unblocks the Gate?",
        "interrogate_hint": "3. Type query to interrogate agent engine...",
        "branches_title": "The Three Cascading Branches & Remedial Levers",
        "opt_a": "Execute Option A Directive",
        "pipeline_title": "🔒 Gated Incident Pipeline (Next 4 Bottlenecks)",
        "active_threat": "🟡 ACTIVE THREAT",
        "queued": "🔒 QUEUED",
        "audit_title": "Tier 4 | Sealed Cryptographic Job Capsules"
    },
    "Deutsch [Deutschland · Österreich]": {
        "title": "Aufsichtsratsvorsitzender Lagezentrum",
        "sub_app": "Autonome Kontrollplattform zur Kapitalverteidigung",
        "calib_red_header": "FÜHRUNGSTOR: PROJEKTBUDGET / GEFÄHRDETES INVESTITIONSKAPITAL (ANTIPPEN ZUM KALIBRIEREN)",
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
        "why_stalled": "🚨 1. Warum stockt die Freigabe?",
        "what_unblocks": "🟢 2. Wie wird das Tor entsperrt?",
        "interrogate_hint": "3. Frage zur Sachverhaltsaufklärung eingeben...",
        "branches_title": "Die Drei Kaskadierenden Säulen & Abhilfemassnahmen",
        "opt_a": "Weisung Option A Vollstrecken",
        "pipeline_title": "🔒 Nachgelagerte Engpass-Pipeline (Nächste 4 Prüfpunkte)",
        "active_threat": "🟡 AKUTE BEDROHUNG",
        "queued": "🔒 WARTESCHLANGE",
        "audit_title": "Stufe 4 | Versiegelte Kryptographische Einsatzkapseln"
    },
    "Español [Chile · Brasil · Sudamérica]": {
        "title": "Puesto de Mando del Presidente Ejecutivo",
        "sub_app": "Plano de Control para la Defensa Autónoma del Capital",
        "calib_red_header": "PORTAL DE MANDO: INGRESE PRESUPUESTO / CAPEX EN RIESGO (TOQUE PARA RECALIBRAR)",
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
        "why_stalled": "🚨 1. ¿Por qué está trabada la solución?",
        "what_unblocks": "🟢 2. ¿Qué desbloquea la compuerta?",
        "interrogate_hint": "3. Escriba consulta para interrogar a los agentes...",
        "branches_title": "Las Tres Ramas en Cascada y Palancas de Mitigación",
        "opt_a": "Ejecutar Directiva Opción A",
        "pipeline_title": "🔒 Ducto de Incidentes Consecutivos (Próximos 4 Cuellos de Botella)",
        "active_threat": "🟡 AMENAZA ACTIVA",
        "queued": "🔒 EN ESPERA",
        "audit_title": "Nivel 4 | Cápsulas Criptográficas de Auditoría Selladas"
    },
    "Français [France · RTE · Europe]": {
        "title": "Poste de Commandement du Président Exécutif",
        "sub_app": "Plateforme Autonome de Défense du Capital Fédéral",
        "calib_red_header": "PORTAIL DE COMMANDEMENT : SAISIR LE BUDGET / CAPEX EN RISQUE (TOUCHER POUR RECALIBRER)",
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
        "why_stalled": "🚨 1. Pourquoi le déblocage est-il gelé ?",
        "what_unblocks": "🟢 2. Quel acte juridique libère le site ?",
        "interrogate_hint": "3. Interroger les agents de gouvernance...",
        "branches_title": "Les Trois Piliers en Cascade & Leviers d'Atténuation",
        "opt_a": "Exécuter la Directive Option A",
        "pipeline_title": "🔒 File Gérée des Goulots d'Étranglement (4 Prochains)",
        "active_threat": "🟡 MENACE ACTIVE",
        "queued": "🔒 EN ATTENTE",
        "audit_title": "Niveau 4 | Capsules d'Audit Cryptographiques Scellées"
    },
    "日本語 [日本 · TEPCO · METI]": {
        "title": "取締役会長 統合指令ポスト (Command Post)",
        "sub_app": "自律型自己資本防衛コントロールプレーン",
        "calib_red_header": "コマンド・ゲートウェイ：防衛対象資本・予算を入力（タップして再設定）",
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
        "why_stalled": "🚨 1. なぜ現場は停滞しているのか？",
        "what_unblocks": "🟢 2. どの決議がゲートを解除するか？",
        "interrogate_hint": "3. エージェントへ直接諮問を入力...",
        "branches_title": "3つの連動防衛ブランチと解決手段",
        "opt_a": "選択肢A 取締役会免責決議を実行",
        "pipeline_title": "🔒 順次解決ボトルネック・パイプライン",
        "active_threat": "🟡 進行中の危機",
        "queued": "🔒 保留中",
        "audit_title": "ティア4 | 封印済み暗号監査カプセル"
    }
}

TODAY_STR = "15 Sep 2026"

SECTORS = {
    "ERCOT BESS / Grid Storage (USA)": {
        "currency": "$",
        "asset_cap": 88_500_000,
        "baseline_docket": "ERCOT IA § 4.2 Interconnection Docket #54219",
        "baseline_date": "15 Sep 2026",
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
                "status": "DEADLOCKED",
                "director_seat": "Dr. Arthur Pendleton",
                "tier3_work_order": {
                    "id": "WO-8821-HARMONIC",
                    "title": "On-Site IEEE 2800 Harmonic Sweep",
                    "progress_pct": 75,
                    "steps": [
                        {"task": "Rack 4 PE Calibration", "done": True},
                        {"task": "Inverter Bank 1-4 Frequency Injection", "done": True},
                        {"task": "Damping Resonance Verification", "done": True},
                        {"task": "PE Digital Stamp & Packet Sign-off", "done": False}
                    ]
                },
                "audit_packages": [
                    {
                        "job_id": "JOB-001: Statutory Ingestion Baseline",
                        "status": "SEALED & ATTESTED",
                        "sealed_at": "2026-09-15 00:00:00 UTC",
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
        "baseline_date": "15 Sep 2026",
        "statute": "German AktG § 93 / § 116 (Aufsichtsrat Dual-Board Shield)",
        "directors": {"Werner Gatzer": {"seat": "Aufsichtsratsvorsitzender"}},
        "incidents": {
            "DB-ETCS-01": {
                "title": "Rhine-Alpine ETCS Level 2 Baseline Handshake Stall",
                "priority": "P1 - CRITICAL",
                "base_daily_bleed": 1728000,
                "status": "DEADLOCKED",
                "director_seat": "Werner Gatzer",
                "tier3_work_order": {"id": "WO-DB-9901", "progress_pct": 65, "steps": []},
                "audit_packages": [
                    {
                        "job_id": "JOB-001: EBA Baseline Ingestion",
                        "status": "SEALED & ATTESTED",
                        "sealed_at": "2026-09-15 00:00:00 UTC",
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
        "baseline_date": "15 Sep 2026",
        "statute": "Ley General de Servicios Eléctricos Art. 72-1 (Chile)",
        "directors": {"Juan Carlos Olmedo": {"seat": "Presidente del Consejo Directivo"}},
        "incidents": {
            "CEN-BESS-01": {
                "title": "Prueba de Inyección de Armónicos y Sincronismo 220kV",
                "priority": "P1 - CRÍTICO",
                "base_daily_bleed": 45000,
                "status": "DEADLOCKED",
                "director_seat": "Juan Carlos Olmedo",
                "tier3_work_order": {"id": "WO-CEN-332", "progress_pct": 70, "steps": []},
                "audit_packages": [
                    {
                        "job_id": "JOB-001: Registro CEN Ingestado",
                        "status": "SEALED & ATTESTED",
                        "sealed_at": "2026-09-15 00:00:00 UTC",
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
        "baseline_date": "15 Sep 2026",
        "statute": "Code de Commerce Art. L225-251 (Protection Dirigeant)",
        "directors": {"Xavier Piechaczyk": {"seat": "Président du Directoire"}},
        "incidents": {
            "RTE-BESS-01": {
                "title": "Blocage d'Injection Haute Tension Poste 400kV",
                "priority": "P1 - CRITIQUE",
                "base_daily_bleed": 68000,
                "status": "DEADLOCKED",
                "director_seat": "Xavier Piechaczyk",
                "tier3_work_order": {"id": "WO-RTE-881", "progress_pct": 60, "steps": []},
                "audit_packages": [
                    {
                        "job_id": "JOB-001: Dossier RTE Verrouillé",
                        "status": "SEALED & ATTESTED",
                        "sealed_at": "2026-09-15 00:00:00 UTC",
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
        "baseline_date": "15 Sep 2026",
        "statute": "Japanese Companies Act Art. 423 (Fiduciary Defense Shield)",
        "directors": {"Keisuke Yokoo": {"seat": "Chairman of the Board"}},
        "incidents": {
            "TEPCO-500KV-01": {
                "title": "Shin-Shinano 500kV Frequency Converter Synchronization Stall",
                "priority": "P1 - CRITICAL",
                "base_daily_bleed": 125280,
                "status": "DEADLOCKED",
                "director_seat": "Keisuke Yokoo",
                "tier3_work_order": {"id": "WO-TEPCO-4410", "progress_pct": 70, "steps": []},
                "audit_packages": [
                    {
                        "job_id": "JOB-001: METI Baseline Ingestion",
                        "status": "SEALED & ATTESTED",
                        "sealed_at": "2026-09-15 00:00:00 UTC",
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

if "app_state" not in st.session_state:
    st.session_state.app_state = SECTORS

if "selected_incident_id" not in st.session_state:
    st.session_state.selected_incident_id = "INC-001"

if "conference_focus" not in st.session_state:
    st.session_state.conference_focus = "DEFAULT"

if "remedial_simulation" not in st.session_state:
    st.session_state.remedial_simulation = "Option A: Directorate Carve-Out (Dominant Path)"

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

# =========================================================
# 3. SIDEBAR WITH EXPANDED SOVEREIGN ROSTER
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

    selected_role = st.radio(
        "Governance Profile:",
        [t["title"], "Tier 3: Site Operations / Field Lead"] +
        [f"Director: {d}" for d in sector["directors"].keys()]
    )
    
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
            st.rerun()

if st.session_state.selected_incident_id not in sector["incidents"]:
    st.session_state.selected_incident_id = list(sector["incidents"].keys())[0]

active_inc = sector["incidents"][st.session_state.selected_incident_id]
is_resolved = active_inc.get("status") == "RESOLVED"

# =========================================================
# 4. EXECUTIVE CHAIRMAN VIEW (RED-HEADER COMMAND GATEWAY)
# =========================================================
if selected_role == t["title"]:
    st.title(t["title"])
    
    # Statutory Defense Banner
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
    # UNIFIED CHAIRMAN QUICK-CALIBRATOR TERMINAL (BOLD RED GATE)
    # ---------------------------------------------------------
    with st.container(border=True):
        st.markdown(f"""
            <div style="text-align: center; margin-bottom: 14px;">
                <div style="font-size:0.95rem; font-weight:700; color:#58a6ff; letter-spacing:0.08em; text-transform:uppercase;">
                    ⚡ {active_sector} — {sector['baseline_docket']}
                </div>
                <div style="color: #ff4b4b; font-size: 1.5rem; font-weight: 900; letter-spacing: 0.05em; text-transform: uppercase; margin: 10px 0 6px 0; line-height: 1.3;">
                    🚨 {t['calib_red_header']}
                </div>
                <div style="font-size:0.95rem; color:#8b949e;">
                    Statutory Baseline Docket: <strong style="color:#ffffff;">{curr_sym}{sector['asset_cap']:,}</strong> 
                    <span style="color:#58a6ff;">(Effective: {sector['baseline_date']})</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Centerpiece Throttle Input Box
        raw_input_str = st.text_input(
            label="Chairman Quick-Calibrator Input",
            value=f"{st.session_state[calib_key]:,}",
            label_visibility="collapsed"
        )
        parsed_capex = int(re.sub(r"[^\d]", "", raw_input_str) or sector["asset_cap"])
        
        # Trigger Job Package & Seal on Change
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

        is_overridden = parsed_capex != sector["asset_cap"]
        badge_color = "#e3b341" if is_overridden else "#58a6ff"
        badge_label = t["override_active"] if is_overridden else t["baseline_synced"]
        
        st.markdown(f"""
            <div style="text-align:center; margin-top:10px; margin-bottom:4px;">
                <span style="font-size:1.15rem; font-weight:800; color:{badge_color};">
                    ● {badge_label}: {curr_sym}{parsed_capex:,}
                </span>
                <span style="color:#ffffff; font-size:0.95rem; font-weight:600; margin-left:8px;">
                    (Effective Audit Timestamp: {st.session_state[ts_key]})
                </span>
            </div>
        """, unsafe_allow_html=True)

    # ---------------------------------------------------------
    # SECONDARY METRICS: TOLL-GATE & EPOCH
    # ---------------------------------------------------------
    calibrated_toll_gate = max(25000, int(round(parsed_capex * 0.00085, -3)))
    
    sub1, sub2 = st.columns(2)
    with sub1:
        st.markdown(f"""
            <div class="exec-metric-card">
                <div class="exec-metric-label">{t['toll_fee']}</div>
                <div class="exec-metric-val">{curr_sym}{calibrated_toll_gate:,}</div>
                <div class="exec-metric-sub" style="color:#3fb950;">{t['escrow_desc']}</div>
            </div>
        """, unsafe_allow_html=True)
    with sub2:
        st.markdown(f"""
            <div class="exec-metric-card">
                <div class="exec-metric-label">{t['session_window']}</div>
                <div class="exec-metric-val">09:42</div>
                <div class="exec-metric-sub" style="color:#3fb950;">{t['session_desc']}</div>
            </div>
        """, unsafe_allow_html=True)

    # ---------------------------------------------------------
    # MAIN TRUNK: FINANCIAL READOUT
    # ---------------------------------------------------------
    active_incidents = [i for i in sector["incidents"].values() if i.get("status") != "RESOLVED"]
    total_burn_day = sum(int(round(i.get("base_daily_bleed", 50000) * scale_factor)) for i in active_incidents)
    total_burn_wk = total_burn_day * 7
    dynamic_crossover_days = round(parsed_capex / total_burn_day, 1) if total_burn_day > 0 else 999.9

    k1, k2, k3 = st.columns(3)
    with k1:
        st.markdown(f"""
            <div class="exec-metric-card">
                <div class="exec-metric-label">{t['holding_burn']} ({TODAY_STR})</div>
                <div class="exec-metric-val" style="color:#f85149;">{curr_sym}{total_burn_wk:,.0f} <span style="font-size:1.05rem; font-weight:600; color:#c9d1d9;">/ wk</span></div>
                <div class="exec-metric-sub" style="color:#f85149; font-family:monospace; font-size:1.05rem;">↑ {curr_sym}{total_burn_day:,.0f} / Day</div>
            </div>
        """, unsafe_allow_html=True)
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
                append_to_active_package(active_inc, "DIAGNOSTIC", "Inquiry: What unblocks the gate?")
                st.rerun()
        with diag_col3:
            custom_query = st.text_input("Interrogate", placeholder=t["interrogate_hint"], label_visibility="collapsed")
            if custom_query:
                st.session_state.conference_focus = "CUSTOM"
                st.session_state.custom_query_text = custom_query
                append_to_active_package(active_inc, "DIAGNOSTIC", f"Custom: '{custom_query}'")
            
        st.markdown("---")
        if st.session_state.conference_focus == "WHY_STALLED":
            st.markdown(
                f"🔴 **Master Orchestrator ➔ Telemetry Agent:** *'Interrogating incident {st.session_state.selected_incident_id}.'* \n\n"
                f"🔴 **Telemetry Agent:** *'Field hardware tests completed at 75%. OEM supervisor holds sign-off pending indemnification against Clause 14.b. Physical telemetry is nominal; signatory deadlock active.'*"
            )
        elif st.session_state.conference_focus == "WHAT_UNBLOCKS":
            st.markdown(
                f"🟢 **Master Orchestrator ➔ Fiduciary Shield Agent:** *'What instrument unblocks this gate?'* \n\n"
                f"🟢 **Fiduciary Shield Agent:** *'Board Resolution (Option A) executing a Directorate Indemnity Carve-Out shields the site lead under {sector['statute']}, releasing the attestation within 5 minutes.'*"
            )
        else:
            st.markdown(
                f"⚡ **Active Interrogation Standby ({TODAY_STR}):** Agents synchronized with {sector['statute']} and physical telemetry. Select an action above to execute diagnostic."
            )

    # ---------------------------------------------------------
    # REMEDIAL LEVERS & BRANCHES
    # ---------------------------------------------------------
    st.markdown(f"### {t['branches_title']}")
    with st.container(border=True):
        r1, r2 = st.columns([3, 1])
        with r1:
            st.session_state.remedial_simulation = st.radio(
                "Simulate Remedial Action:",
                [
                    "Option A: Directorate Carve-Out (Dominant Path)",
                    "Option B: Mobilize Secondary Field Crew ($35k Draw)",
                    "Option C: Demobilize Site Contractors (Standby)"
                ],
                horizontal=True
            )
        with r2:
            st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
            if not is_resolved:
                if "Option A" in st.session_state.remedial_simulation:
                    if st.button(t["opt_a"], use_container_width=True, type="primary"):
                        active_inc["status"] = "RESOLVED"
                        active_inc["base_daily_bleed"] = 0
                        wo = active_inc.get("tier3_work_order", {})
                        wo["progress_pct"] = 100
                        for s in wo.get("steps", []): s["done"] = True
                        append_to_active_package(active_inc, "REMEDIAL EXECUTION", "Option A executed. Burn halted to 0.")
                        st.session_state.conference_focus = "DEFAULT"
                        st.success("Option A Executed.")
                        st.rerun()
            else:
                if st.button(f"⚡ Settle Milestone Fee ({curr_sym}{calibrated_toll_gate:,})", use_container_width=True, type="primary"):
                    seal_active_package(active_inc)
                    st.success("Milestone Settled. Audit Capsule Sealed.")

    # ---------------------------------------------------------
    # PIPELINE (DYNAMIC TRANSLATION)
    # ---------------------------------------------------------
    with st.container(border=True):
        st.markdown(f"### {t['pipeline_title']}")
        p1, p2, p3, p4 = st.columns(4)

        def render_pipeline_card(num_title, raw_bleed, inc_code, is_threat):
            border = "#e3b341" if is_threat else "#30363d"
            bg = "rgba(227, 179, 65, 0.16)" if is_threat else "#161b22"
            status_txt = t["active_threat"] if is_threat else t["queued"]
            status_color = "#e3b341" if is_threat else "#c9d1d9"
            
            scaled_daily = int(round(raw_bleed * scale_factor))
            scaled_weekly = scaled_daily * 7
            crossover_days = round(parsed_capex / scaled_daily, 1) if scaled_daily > 0 else 999.9
            
            return f"""
            <div style="background-color:{bg}; border:2px solid {border}; border-radius:8px; padding:18px; height:100%; display:flex; flex-direction:column; text-align:center;">
                <div style="font-weight:700; font-size:1.15rem; color:#ffffff; margin-bottom:8px;">{num_title}</div>
                <div style="font-family:ui-monospace, monospace; font-size:1.7rem; font-weight:800; color:#ffffff; margin: 4px 0;">
                    {curr_sym}{scaled_daily:,} <span style="font-size:1.0rem; font-weight:600; color:#c9d1d9;">/ Day</span>
                </div>
                <div style="font-size:0.95rem; font-weight:600; color:#c9d1d9; margin-bottom:6px;">
                    {curr_sym}{scaled_weekly:,} / Wk
                </div>
                <div style="font-size:1.05rem; font-weight:700; color:#e3b341; margin-bottom:14px;">
                    Horizon: {crossover_days} Days
                </div>
                <div style="font-size:1.0rem; font-weight:700; color:{status_color}; margin-top:auto;">
                    {status_txt}: {inc_code}
                </div>
            </div>
            """

        pipe_keys = [k for k in sector["incidents"].keys() if k not in ["INC-001", "DB-ETCS-01", "CEN-BESS-01", "RTE-BESS-01"]]
        with p1:
            inc_p1 = sector["incidents"].get(pipe_keys[0], {})
            st.markdown(render_pipeline_card("1. Inrush Damping", inc_p1.get("base_daily_bleed", 38880), pipe_keys[0], is_resolved), unsafe_allow_html=True)
        with p2:
            inc_p2 = sector["incidents"].get(pipe_keys[1], {})
            st.markdown(render_pipeline_card("2. SCADA IEC 61850", inc_p2.get("base_daily_bleed", 15552), pipe_keys[1], False), unsafe_allow_html=True)
        with p3:
            inc_p3 = sector["incidents"].get(pipe_keys[2], {})
            st.markdown(render_pipeline_card("3. BESS Firmware OTA", inc_p3.get("base_daily_bleed", 4320), pipe_keys[2], False), unsafe_allow_html=True)
        with p4:
            inc_p4 = sector["incidents"].get(pipe_keys[3], {})
            st.markdown(render_pipeline_card("4. Substation Oil DGA", inc_p4.get("base_daily_bleed", 6912), pipe_keys[3], False), unsafe_allow_html=True)

    # ---------------------------------------------------------
    # TIER 4 AUDIT LEDGER
    # ---------------------------------------------------------
    with st.container(border=True):
        st.markdown(f"### {t['audit_title']}")
        for pkg in reversed(active_inc.get("audit_packages", [])):
            is_sealed = pkg["status"] == "SEALED & ATTESTED"
            badge_icon = "🔒" if is_sealed else "⚡"
            status_color = "#3fb950" if is_sealed else "#e3b341"
            
            with st.expander(f"{badge_icon} {pkg['job_id']} | Root Hash: SHA-256:{pkg['package_hash']}", expanded=not is_sealed):
                st.markdown(f"**Status:** <span style='color:{status_color}; font-weight:bold; font-size:1.1rem;'>{pkg['status']}</span>", unsafe_allow_html=True)
                for entry in pkg.get("entries", []):
                    st.markdown(f"<div style='font-size:1.05rem; font-family:monospace; margin:4px 0; color:#f0f6fc;'>• {entry}</div>", unsafe_allow_html=True)

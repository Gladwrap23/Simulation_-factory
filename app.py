import datetime
import hashlib
import json
import streamlit as st

# =========================================================
# 1. APPLICATION SETUP & INDUSTRIAL OBSIDIAN STYLING
# =========================================================
st.set_page_config(
    page_title="Factory Command Post | Autonomous Capital Defense",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        .stApp { background-color: #0d1117; color: #c9d1d9; }
        div[data-testid="stMetric"] {
            background-color: #161b22;
            border: 1px solid #30363d;
            padding: 10px 14px;
            border-radius: 6px;
            min-height: 85px;
        }
        div[data-testid="stMetricLabel"] { color: #8b949e; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; }
        div[data-testid="stMetricValue"] { color: #f0f6fc; font-family: monospace; font-size: 1.45rem; }
        .stButton>button {
            border-radius: 4px;
            font-weight: 600;
            letter-spacing: 0.02em;
        }
        .main-card {
            background-color: #161b22;
            border: 1px solid #30363d;
            border-radius: 6px;
            padding: 16px;
            margin-bottom: 12px;
        }
    </style>
""",
    unsafe_allow_html=True,
)

# =========================================================
# 2. STATE MANAGEMENT & SOVEREIGN CORPORATE PORTFOLIO
# =========================================================
if "micro_drift_active" not in st.session_state:
    st.session_state.micro_drift_active = False
if "drift_minutes" not in st.session_state:
    st.session_state.drift_minutes = 0
if "conference_focus" not in st.session_state:
    st.session_state.conference_focus = "NONE"
if "remedial_simulation" not in st.session_state:
    st.session_state.remedial_simulation = "Option A: Directorate Carve-Out (Dominant Path)"
if "custom_capex" not in st.session_state:
    st.session_state.custom_capex = 0
if "session_authenticated" not in st.session_state:
    st.session_state.session_authenticated = True

SECTORS = {
    "ERCOT BESS / Grid Storage (USA)": {
        "currency": "$",
        "asset_cap": 88_500_000,
        "statute": "Delaware DGCL § 141 (Business Judgment Rule)",
        "directors": {
            "Dr. Arthur Pendleton": {
                "seat": "Chair, Grid Risk & Technical Integrity",
                "focus": "OEM Warranties, IEEE 2800 Compliance, Transformer Covenants",
                "assigned_gm": "Elena Rostova",
            },
            "David Chen (Proxy)": {
                "seat": "Chair, Regulatory & Market Compliance",
                "focus": "ERCOT Standard IA § 4.2, Interconnection Queue Defense",
                "assigned_gm": "David Chen",
            },
        },
        "incidents": {
            "INC-001": {
                "title": "ERCOT IA § 4.2 Part 2 COD Attestation Deadlock",
                "priority": "P1 - CRITICAL",
                "base_burn_rate_sec": 1.01,
                "start_time": datetime.datetime.now() - datetime.timedelta(days=1),
                "schedule_drift": "+9 Days COD Drift",
                "status": "DEADLOCKED",
                "director_seat": "Dr. Arthur Pendleton",
                "deadlock_summary": "Elena Rostova (protecting $1.2M warranty) vs. David Chen (protecting $4.5M queue deposit).",
                "crossover_days": 13.8,
                "tier3_work_order": {
                    "id": "WO-8821-HARMONIC",
                    "title": "On-Site IEEE 2800 Harmonic Sweep",
                    "assigned_crew": "Permian HV Crew 3 (Lead: Mark Henderson)",
                    "target_gate": "Check #6 (Part 2 COD Attestation)",
                    "progress_pct": 75,
                    "steps": [
                        {"task": "Rack 4 PE Calibration", "done": True},
                        {"task": "Inverter Bank 1-4 Frequency Injection", "done": True},
                        {"task": "Damping Resonance Verification", "done": True},
                        {"task": "PE Digital Stamp & Packet Sign-off", "done": False},
                    ],
                    "telemetry_metrics": {
                        "THD Harmonics": ("4.1%", "Limit: 5.0% [NOMINAL]"),
                        "Inrush Damping": ("1.18 pu", "Trip: 1.40 pu"),
                        "Frequency Response": ("14.2 MW/0.1Hz", "Compliant"),
                        "ICCP Latency": ("240 ms", "Max Allowed: 1000 ms"),
                    },
                },
                "gms": {
                    "Elena Rostova": {
                        "title": "GM - Field Operations & High-Voltage Crews",
                        "domain": "Permian Substation, 138kV Step-Up Transformer",
                        "position": "Withholding sign-off: Energizing without completed sweeps voids $1.2M warranty under Clause 14.b.",
                        "checks": [
                            {"id": "Check #1", "name": "ICCP 4-sec Telemetry", "status": "CLEARED", "evidence": "240ms Heartbeat"},
                            {"id": "Check #3", "name": "PSCAD EMT Model", "status": "CLEARED", "evidence": "Waveform Cleared"},
                            {"id": "Check #5", "name": "Relay Inrush Testing", "status": "CLEARED", "evidence": "1.18 pu Damping"},
                        ],
                    },
                    "David Chen": {
                        "title": "GM - Regulatory & Interconnection",
                        "domain": "ERCOT Gateway & IA § 4.2 COD Filing",
                        "position": "Demanding filing: Window lapses in 48 hours. Forfeiture triggers $4.5M restudy penalty.",
                        "checks": [
                            {"id": "Check #2", "name": "ICCP Attestation Record", "status": "CLEARED", "evidence": "Record Locked"},
                            {"id": "Check #4", "name": "PSCAD Study Submittal", "status": "CLEARED", "evidence": "Submitted"},
                            {"id": "Check #6", "name": "Part 2 COD Attestation Gate", "status": "BLOCKED", "evidence": "Withheld by Field Ops (WO-8821)"},
                        ],
                    },
                },
                "audit_log": [
                    {
                        "ts": "2026-09-13 08:00:12 UTC",
                        "hash": "8f3a9e01c4",
                        "event": "INCIDENT INITIALIZED: Elena Rostova withheld sign-off on Check #6.",
                        "snapshot": {"burn_sec": 1.01, "crossover": 13.8, "bjr": "ENFORCED"},
                    }
                ],
            },
            "INC-002": {
                "title": "Substation Step-Up Inrush Damping Validation",
                "priority": "P2 - HIGH",
                "base_burn_rate_sec": 0.45,
                "start_time": datetime.datetime.now() - datetime.timedelta(days=2),
                "schedule_drift": "+3 Days Drift",
                "status": "QUEUED",
                "director_seat": "Dr. Arthur Pendleton",
                "deadlock_summary": "Breaker actuation damping curves require secondary OEM calibration.",
                "crossover_days": 28.4,
                "tier3_work_order": {"id": "WO-8824-INRUSH", "title": "Resistor Cycle Check", "progress_pct": 50, "steps": [], "telemetry_metrics": {}},
                "gms": {},
                "audit_log": [],
            },
            "INC-003": {
                "title": "SCADA Protocol IEC 61850 Gateway",
                "priority": "P3 - MODERATE",
                "base_burn_rate_sec": 0.18,
                "start_time": datetime.datetime.now() - datetime.timedelta(days=3),
                "schedule_drift": "+1 Day Drift",
                "status": "QUEUED",
                "director_seat": "David Chen (Proxy)",
                "deadlock_summary": "Telemetry gateway polling buffer delay between RTU and ERCOT node.",
                "crossover_days": 45.0,
                "tier3_work_order": {"id": "WO-8830-SCADA", "title": "GOOSE Buffer Clear", "progress_pct": 90, "steps": [], "telemetry_metrics": {}},
                "gms": {},
                "audit_log": [],
            },
            "INC-004": {
                "title": "BESS Inverter Firmware OTA Security Patch",
                "priority": "P4 - MONITORED",
                "base_burn_rate_sec": 0.05,
                "start_time": datetime.datetime.now() - datetime.timedelta(days=4),
                "schedule_drift": "On Schedule",
                "status": "QUEUED",
                "director_seat": "Dr. Arthur Pendleton",
                "deadlock_summary": "Staged firmware flashing across 48 inverter skids.",
                "crossover_days": 90.0,
                "tier3_work_order": {"id": "WO-8845-OTA", "title": "SHA-256 Flashing", "progress_pct": 75, "steps": [], "telemetry_metrics": {}},
                "gms": {},
                "audit_log": [],
            },
        },
    },
    "Deutsche Bahn AG | Rail Corridor (Germany)": {
        "currency": "€",
        "asset_cap": 34_000_000_000,
        "statute": "German AktG § 93 / § 116 (Aufsichtsrat Dual-Board Shield)",
        "directors": {
            "Werner Gatzer": {
                "seat": "Aufsichtsratsvorsitzender (Supervisory Board Chair)",
                "focus": "Federal Infrastructure Allocation, EBA Statutory Compliance, Capital Defense",
                "assigned_gm": "Signaling Operations Lead",
            }
        },
        "incidents": {
            "DB-ETCS-01": {
                "title": "Rhine-Alpine ETCS Level 2 Baseline Handshake Stall",
                "priority": "P1 - CRITICAL",
                "base_burn_rate_sec": 20.00,
                "start_time": datetime.datetime.now() - datetime.timedelta(hours=14),
                "schedule_drift": "+14h Track Possession Slip",
                "status": "DEADLOCKED",
                "director_seat": "Werner Gatzer",
                "deadlock_summary": "Signaling GM (holding for balise safety telegrams) vs. Network Operations (facing international rail closure).",
                "crossover_days": 4.2,
                "tier3_work_order": {
                    "id": "WO-DB-9901-ETCS",
                    "title": "Radio Block Center Handshake Certification",
                    "assigned_crew": "Frankfurt Rail Engineering Taskforce",
                    "target_gate": "Federal Railway Authority (EBA) Release",
                    "progress_pct": 65,
                    "steps": [
                        {"task": "Balise Telegram Frequency Sweep", "done": True},
                        {"task": "GSM-R Interoperability Verification", "done": True},
                        {"task": "EBA Safety Case Digital Stamp", "done": False},
                    ],
                    "telemetry_metrics": {
                        "RBC Latency": ("82 ms", "Limit: 120 ms [NOMINAL]"),
                        "Packet Loss Rate": ("0.001%", "Max: 0.01%"),
                    },
                },
                "gms": {
                    "Signaling Operations Lead": {
                        "title": "GM - Train Control & Safety Engineering",
                        "domain": "Rhine Corridor Signaling & RBC Nodes",
                        "position": "Withholding sign-off: Commissioning track without certified EBA telegram logs triggers strict personal derailment liability under AEG § 4.",
                        "checks": [
                            {"id": "Check #1", "name": "Balise Telegram Ingestion", "status": "CLEARED", "evidence": "Verified"},
                            {"id": "Check #2", "name": "EBA Statutory Safety Stamp", "status": "BLOCKED", "evidence": "Withheld by Signaling GM"},
                        ],
                    }
                },
                "audit_log": [
                    {
                        "ts": "2026-09-13 04:00:00 UTC",
                        "hash": "de9910a1b2",
                        "event": "INCIDENT INITIALIZED: ETCS Level 2 commissioning halted over safety cert.",
                        "snapshot": {"burn_sec": 20.00, "statute": "AktG § 93", "gate": "EBA Release"},
                    }
                ],
            }
        },
    },
    "TEPCO Holdings | Transmission Grid (Japan)": {
        "currency": "¥",
        "asset_cap": 42_000_000_000,
        "statute": "Japanese Companies Act Art. 423 (Fiduciary Defense Shield)",
        "directors": {
            "Keisuke Yokoo": {
                "seat": "Chairman of the Board (取締役会長)",
                "focus": "Capital Defense, METI Reliability Compliance, Fiduciary Risk",
                "assigned_gm": "Grid Operations Lead",
            }
        },
        "incidents": {
            "TEPCO-500KV-01": {
                "title": "Shin-Shinano 500kV Frequency Converter Synchronization Stall",
                "priority": "P1 - CRITICAL",
                "base_burn_rate_sec": 1.45,
                "start_time": datetime.datetime.now() - datetime.timedelta(days=1),
                "schedule_drift": "+24h Grid Sync Slip",
                "status": "DEADLOCKED",
                "director_seat": "Keisuke Yokoo",
                "deadlock_summary": "Substation Chief (holding for harmonic filter dampening) vs. Power Grid GM (facing METI reserve fines).",
                "crossover_days": 9.5,
                "tier3_work_order": {
                    "id": "WO-TEPCO-4410",
                    "title": "50-to-60Hz Converter Waveform Verification",
                    "assigned_crew": "Tokyo Substation Engineering Group",
                    "target_gate": "METI Intertie Clearance",
                    "progress_pct": 70,
                    "steps": [
                        {"task": "Filter Capacitor Bank Step-Test", "done": True},
                        {"task": "Frequency Inversion Damping", "done": True},
                        {"task": "Final Synchronization Signature", "done": False},
                    ],
                    "telemetry_metrics": {
                        "Harmonic Distortion": ("2.1%", "METI Limit: 3.0%"),
                        "Phase Sync Delta": ("0.4 deg", "Max: 1.0 deg"),
                    },
                },
                "gms": {
                    "Grid Operations Lead": {
                        "title": "GM - High-Voltage Transmission",
                        "domain": "Shin-Shinano Frequency Converter Substation",
                        "position": "Awaiting formal board liability indemnity before energizing intertie under unverified dampening data.",
                        "checks": [
                            {"id": "Check #1", "name": "Converter Waveform Test", "status": "CLEARED", "evidence": "2.1% THD"},
                            {"id": "Check #2", "name": "METI Grid Intertie Gate", "status": "BLOCKED", "evidence": "Withheld by Substation Lead"},
                        ],
                    }
                },
                "audit_log": [
                    {
                        "ts": "2026-09-13 06:00:00 UTC",
                        "hash": "jp8834f109",
                        "event": "INCIDENT INITIALIZED: 500kV converter sync held pending indemnity.",
                        "snapshot": {"burn_sec": 1.45, "statute": "Companies Act Art. 423", "gate": "METI Sync"},
                    }
                ],
            }
        },
    },
    "Thyssenkrupp AG | Industrial Plant (Germany)": {
        "currency": "€",
        "asset_cap": 8_200_000_000,
        "statute": "German AktG § 93 & BImSchG (Environmental & Plant Shield)",
        "directors": {
            "Miguel Ángel López Borrego": {
                "seat": "Vorstandsvorsitzender (Executive Board CEO)",
                "focus": "Direct Reduction Iron (DRI) Hydrogen Integrity, Plant Liability",
                "assigned_gm": "Duisburg Works Plant GM",
            }
        },
        "incidents": {
            "TK-DRI-01": {
                "title": "Duisburg Blast Furnace Hydrogen Conversion Pressure Stall",
                "priority": "P1 - CRITICAL",
                "base_burn_rate_sec": 14.50,
                "start_time": datetime.datetime.now() - datetime.timedelta(hours=8),
                "schedule_drift": "+8h Blast Injection Slip",
                "status": "DEADLOCKED",
                "director_seat": "Miguel Ángel López Borrego",
                "deadlock_summary": "Plant GM (holding seal sign-off) vs. Steel Trading (facing €3.8M molten iron freeze loss).",
                "crossover_days": 3.1,
                "tier3_work_order": {
                    "id": "WO-TK-502-H2",
                    "title": "Hydrogen Injection Valve Pressure Recalibration",
                    "assigned_crew": "Duisburg Maintenance Engineering",
                    "target_gate": "Safety Seal Verification",
                    "progress_pct": 60,
                    "steps": [
                        {"task": "Seal Integrity Pressure Leak Check", "done": True},
                        {"task": "H2 Flow Ratio Ingestion", "done": True},
                        {"task": "Works Council Sign-off Stamp", "done": False},
                    ],
                    "telemetry_metrics": {
                        "Line Pressure": ("4.2 bar", "Max: 5.0 bar [NOMINAL]"),
                        "H2 Purity": ("99.98%", "Min: 99.95%"),
                    },
                },
                "gms": {
                    "Duisburg Works Plant GM": {
                        "title": "GM - Primary Metallurgy Operations",
                        "domain": "Duisburg Blast Furnace Injection Skid",
                        "position": "Withholding seal clearance: High-pressure hydrogen injection without ratified Works Council waiver exposes plant management to personal criminal liability under BImSchG.",
                        "checks": [
                            {"id": "Check #1", "name": "Valve Seal Testing", "status": "CLEARED", "evidence": "4.2 bar Validated"},
                            {"id": "Check #2", "name": "BImSchG Operating Release", "status": "BLOCKED", "evidence": "Held pending Board Indemnity"},
                        ],
                    }
                },
                "audit_log": [
                    {
                        "ts": "2026-09-13 10:00:00 UTC",
                        "hash": "tk7721cc34",
                        "event": "INCIDENT INITIALIZED: H2 injection line held over BImSchG clearance.",
                        "snapshot": {"burn_sec": 14.50, "statute": "AktG § 93", "gate": "BImSchG Release"},
                    }
                ],
            }
        },
    },
    "Aurizon Holdings | Freight Rail (Australia)": {
        "currency": "A$",
        "asset_cap": 5_400_000_000,
        "statute": "Corporations Act 2001 § 180 (Australian BJR Defense)",
        "directors": {
            "Tim Longstaff": {
                "seat": "Chairman of the Board",
                "focus": "CQCN Heavy Haul Integrity, Rail Safety National Law Compliance",
                "assigned_gm": "Network Operations GM",
            }
        },
        "incidents": {
            "AZ-CQCN-01": {
                "title": "Central Queensland Coal Network 25kV Traction Feeder Stall",
                "priority": "P1 - CRITICAL",
                "base_burn_rate_sec": 5.05,
                "start_time": datetime.datetime.now() - datetime.timedelta(hours=18),
                "schedule_drift": "+18h Train Path Slip",
                "status": "DEADLOCKED",
                "director_seat": "Tim Longstaff",
                "deadlock_summary": "Traction Engineering (holding for harmonic arcing) vs. Haulage Scheduling (facing demurrage penalties).",
                "crossover_days": 6.8,
                "tier3_work_order": {
                    "id": "WO-AZ-771-HV",
                    "title": "Blackwater Feeder Autotransformer Harmonic Sweep",
                    "assigned_crew": "Rockhampton Traction Unit",
                    "target_gate": "Rail Safety National Law Sign-off",
                    "progress_pct": 80,
                    "steps": [
                        {"task": "Feeder Bus Impedance Test", "done": True},
                        {"task": "Catenary Resonance Sweep", "done": True},
                        {"task": "Sign-off Packet Transmission", "done": False},
                    ],
                    "telemetry_metrics": {
                        "Feeder THD": ("3.4%", "Limit: 4.5%"),
                        "Autotransformer Temp": ("62°C", "Max: 85°C"),
                    },
                },
                "gms": {
                    "Network Operations GM": {
                        "title": "GM - Central Queensland Network Infrastructure",
                        "domain": "Blackwater 25kV Traction Substation",
                        "position": "Awaiting executive board waiver: Closing feeder breaker without stamped acoustic tests risks multi-locomotive inverter blowouts under RSNL § 52.",
                        "checks": [
                            {"id": "Check #1", "name": "Traction Bus Telemetry", "status": "CLEARED", "evidence": "Nominal"},
                            {"id": "Check #2", "name": "RSNL Statutory Safety Gate", "status": "BLOCKED", "evidence": "Withheld by Traction Lead"},
                        ],
                    }
                },
                "audit_log": [
                    {
                        "ts": "2026-09-13 11:30:00 UTC",
                        "hash": "az5512bb99",
                        "event": "INCIDENT INITIALIZED: 25kV Feeder re-energization held pending indemnity.",
                        "snapshot": {"burn_sec": 5.05, "statute": "Corps Act § 180", "gate": "RSNL Gate"},
                    }
                ],
            }
        },
    },
}

if "app_state" not in st.session_state:
    st.session_state.app_state = SECTORS

if "selected_incident_id" not in st.session_state:
    st.session_state.selected_incident_id = "INC-001"


def record_ledger_entry(incident: dict, event_text: str, custom_snapshot=None):
    ts = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    prev_hash = incident["audit_log"][-1]["hash"] if incident["audit_log"] else "000000"
    point_in_time_snapshot = (
        custom_snapshot
        if custom_snapshot
        else {
            "holding_burn_sec": incident.get("base_burn_rate_sec", 0.0),
            "financial_crossover_days": incident.get("crossover_days", 0.0),
            "bjr_shield_status": "SATISFIED (Business Judgment Rule Preserved)",
            "counterfactual_tested": st.session_state.remedial_simulation,
        }
    )
    raw_payload = f"{ts}|{prev_hash}|{event_text}|{json.dumps(point_in_time_snapshot, sort_keys=True)}"
    entry_hash = hashlib.sha256(raw_payload.encode()).hexdigest()[:10]
    incident["audit_log"].append(
        {"ts": ts, "hash": entry_hash, "event": event_text, "snapshot": point_in_time_snapshot}
    )


# =========================================================
# 3. SIDEBAR: OPERATING BOOK, LOCALIZATION & QUEUE
# =========================================================
with st.sidebar:
    st.markdown("### 🏛️ COMMAND POST")
    st.caption("Autonomous Capital Defense Control Plane")

    lang_choice = st.selectbox(
        "Localization / 言語 / Sprache:",
        ["English (US / UK / AU)", "日本語 (Japanese)", "Deutsch (German)"],
    )

    active_sector = st.selectbox(
        "Operating Book (Global Assets):",
        list(st.session_state.app_state.keys()),
    )
    sector = st.session_state.app_state[active_sector]
    curr_sym = sector["currency"]

    director_seats = list(sector["directors"].keys())
    selected_role = st.radio(
        "Active Governance Profile:",
        [
            "Executive Chairman (Panoramic Tree)",
            "Tier 3: Site Operations / Field Lead",
        ]
        + [f"Director: {d}" for d in director_seats],
    )

    st.divider()
    st.markdown("#### Active Incident Queue")
    for inc_key, inc_obj in sector["incidents"].items():
        is_selected = inc_key == st.session_state.selected_incident_id
        btn_label = f"{inc_obj['priority']}: {inc_key}\n{inc_obj['title'][:26]}..."
        if st.button(
            btn_label,
            key=f"sb_{inc_key}",
            use_container_width=True,
            type="primary" if is_selected else "secondary",
        ):
            st.session_state.selected_incident_id = inc_key
            st.session_state.conference_focus = "NONE"
            st.rerun()

    st.divider()
    st.markdown("#### ⚡ Autonomous Tripwire")
    if not st.session_state.micro_drift_active:
        if st.button("Simulate +45m Field Slip", use_container_width=True):
            st.session_state.micro_drift_active = True
            st.session_state.drift_minutes = 45
            p_inc = list(sector["incidents"].values())[0]
            p_inc["crossover_days"] = max(1.0, round(p_inc["crossover_days"] * 0.85, 1))
            record_ledger_entry(
                p_inc,
                "MICRO-DRIFT DETECTED: Physical injection delayed +45m. Crossover horizon tightened.",
            )
            st.rerun()
    else:
        if st.button("Reset Field Slip", use_container_width=True):
            st.session_state.micro_drift_active = False
            st.session_state.drift_minutes = 0
            p_inc = list(sector["incidents"].values())[0]
            p_inc["crossover_days"] = 13.8
            record_ledger_entry(p_inc, "DRIFT RECOVERY: Field operations nominal.")
            st.rerun()

if st.session_state.selected_incident_id not in sector["incidents"]:
    st.session_state.selected_incident_id = list(sector["incidents"].keys())[0]

active_inc = sector["incidents"][st.session_state.selected_incident_id]
current_burn_rate = (
    active_inc["base_burn_rate_sec"] if active_inc["status"] != "RESOLVED" else 0.0
)


# =========================================================
# 4. VIEW A: TIER 3 SITE OPERATIONS / FIELD LEAD
# =========================================================
if selected_role == "Tier 3: Site Operations / Field Lead":
    st.title("Tier 3 | Site Operations & Field Execution Desk")
    st.caption(f"Asset: **{active_sector}** | Branch: **{st.session_state.selected_incident_id}**")

    wo = active_inc.get("tier3_work_order", {})
    t1, t2, t3 = st.columns(3)
    t1.metric("Active Work Order", wo.get("id", "N/A"), active_inc["priority"])
    t2.metric("Target Gate", wo.get("target_gate", "N/A"))
    t3.metric("Execution Progress", f"{wo.get('progress_pct', 0)}%")

    st.divider()
    col_tasks, col_metrics = st.columns([3, 2])
    with col_tasks:
        with st.container(border=True):
            st.markdown(f"#### Operational Punch List: {wo.get('title', 'Tasks')}")
            for idx, step in enumerate(wo.get("steps", [])):
                s_icon = "✅" if step["done"] else "⏳"
                st.write(f"{s_icon} **Step {idx+1}:** {step['task']}")

            if active_inc["status"] == "DEADLOCKED":
                st.divider()
                if st.button(
                    "⚡ Complete Final Step: Digital PE Stamp & Upload",
                    use_container_width=True,
                    type="primary",
                ):
                    wo["progress_pct"] = 100
                    if wo.get("steps"):
                        wo["steps"][-1]["done"] = True
                    for gm in active_inc["gms"].values():
                        for c in gm.get("checks", []):
                            if "Gate" in c["name"] or "Release" in c["name"]:
                                c["status"] = "CLEARED"
                                c["evidence"] = "Verified On-Site"
                    active_inc["status"] = "RESOLVED"
                    active_inc["base_burn_rate_sec"] = 0.0
                    record_ledger_entry(
                        active_inc,
                        f"TIER 3 FIELD RESOLUTION: {wo.get('id')} stamped on site. Burn halted to 0.",
                    )
                    st.success("Field packet verified and transmitted!")
                    st.rerun()

    with col_metrics:
        with st.container(border=True):
            st.markdown("#### Live Telemetry & Engineering Tolerances")
            for m_name, (m_val, m_tol) in wo.get("telemetry_metrics", {}).items():
                st.metric(label=m_name, value=m_val, delta=m_tol)

    with st.container(border=True):
        st.subheader("Field Execution Hash Trail")
        for item in reversed(active_inc["audit_log"]):
            st.code(f"[{item['ts']}] SHA:{item['hash']} | {item['event']}", language="yaml")


# =========================================================
# 5. VIEW B: COGNIZANT DIRECTOR (SINGLE VERTICAL PILLAR)
# =========================================================
elif selected_role.startswith("Director:"):
    director_name = selected_role.replace("Director: ", "")
    d_meta = sector["directors"].get(director_name, {})

    st.title(f"{d_meta.get('seat', director_name)}")
    st.caption(f"Charter: **{d_meta.get('focus', 'Fiduciary Oversight')}**")

    m1, m2, m3 = st.columns(3)
    m1.metric("Jurisdiction Status", active_inc["status"], delta=active_inc["priority"])
    m2.metric(
        "Holding Burn Velocity",
        f"{curr_sym}{current_burn_rate*604800:,.0f} / wk",
        f"{curr_sym}{current_burn_rate:.2f}/sec",
        delta_color="inverse",
    )
    m3.metric("Statutory Shield", sector["statute"][:24] + "...")

    st.divider()
    with st.container(border=True):
        st.subheader("Directorate Mandate & Concurrence Desk")
        st.markdown(
            f"**Branch Under Inspection:** `{active_inc['title']}`\n\n"
            f"**Stalemate Summary:** {active_inc['deadlock_summary']}"
        )
        if active_inc["status"] == "DEADLOCKED":
            if st.button("Issue Director Formal Concurrence", use_container_width=True):
                record_ledger_entry(
                    active_inc,
                    f"COGNIZANT CONCURRENCE: {director_name} concurred for {st.session_state.selected_incident_id}.",
                )
                st.success("Concurrence sealed to ledger.")
                st.rerun()


# =========================================================
# 6. VIEW C: EXECUTIVE CHAIRMAN (MASTER COMMAND POST)
# =========================================================
else:
    st.title("Executive Chairman Command Post")
    st.caption(
        f"Operating Sector: **{active_sector}** | Statutory Defense: **{sector['statute']}**"
    )

    # ---------------------------------------------------------
    # ONE-NUMBER QUICK-CALIBRATOR & COUNTDOWN TIMER
    # ---------------------------------------------------------
    with st.container(border=True):
        qc1, qc2, qc3 = st.columns([2, 1, 1])
        with qc1:
            input_capex = st.number_input(
                "Chairman Quick-Calibrator: Enter Project Budget / CapEx at Risk:",
                value=int(sector["asset_cap"]),
                step=5_000_000,
                format="%d",
            )
        with qc2:
            st.metric("Toll-Gate Fee (1 Milestone)", f"{curr_sym}75,000", "BJR Escrow Protected")
        with qc3:
            st.metric("Live Session Window", "09:42", "Zero-Retention Enforced")

    # ---------------------------------------------------------
    # MAIN TRUNK: CAPITAL DEFENSE TICKER
    # ---------------------------------------------------------
    active_incidents = [i for i in sector["incidents"].values() if i["status"] != "RESOLVED"]
    tot_burn_sec = sum(i["base_burn_rate_sec"] for i in active_incidents)
    tot_burn_wk = tot_burn_sec * 604800

    k1, k2, k3 = st.columns(3)
    k1.metric(
        "Portfolio Holding Burn",
        f"{curr_sym}{tot_burn_wk:,.0f} / wk",
        f"{curr_sym}{tot_burn_sec:.2f}/sec",
        delta_color="inverse",
    )
    k2.metric(
        "Capital Under Defense",
        f"{curr_sym}{input_capex:,.0f}",
        "Asset Defense Escrow Intact",
    )
    k3.metric(
        "Active Operational Block",
        f"{st.session_state.selected_incident_id}",
        f"Crossover: {active_inc['crossover_days']} Days",
        delta_color="inverse",
    )

    if st.session_state.micro_drift_active:
        st.error(
            f"🚨 **AUTONOMOUS TRIPWIRE ALERT (+{st.session_state.drift_minutes}m):** Secondary testing delayed. "
            f"Crossover threshold tightened to **{active_inc['crossover_days']} days**. Immediate board override recommended."
        )

    # ---------------------------------------------------------
    # INSTANT AGENT DIAGNOSTIC CONFERENCE
    # ---------------------------------------------------------
    with st.container(border=True):
        st.markdown("### 🎙️ Instant Diagnostic Agent Conference")
        st.caption("Interrogate domain agents to diagnose root friction without micromanaging field physics.")

        cq1, cq2, cq3 = st.columns([2, 1, 1])
        cq1.text_input("Conference Query:", placeholder="Type query...", label_visibility="collapsed")
        if cq2.button("Why is the Fix Stalled?", use_container_width=True):
            st.session_state.conference_focus = "WHY_STALLED"
        if cq3.button("What Unblocks the GM?", use_container_width=True):
            st.session_state.conference_focus = "WHAT_UNBLOCKS"

        if st.session_state.conference_focus == "WHY_STALLED":
            st.markdown("---")
            if "日本語" in lang_choice:
                st.markdown(
                    "🔴 **統括エージェント ➔ 現場テレメトリ:** 「Check #6が未確認の理由は何か？」\n\n"
                    "🔴 **現場テレメトリ:** 「現場チームは待機完了していますが、企業免責の確認書がないため、OEMエンジニアが盤への物理アクセスを拒否しています。機械的故障ではなく法的ロックです。」"
                )
            elif "Deutsch" in lang_choice:
                st.markdown(
                    "🔴 **Haupt-Orchestrator ➔ Standort-Agent:** 'Warum ist Gate #6 blockiert?'\n\n"
                    "🔴 **Standort-Agent:** 'Das Prüfteam ist vor Ort. Der Hersteller-Ingenieur verweigert jedoch den Schaltschrankzugang ohne Vorstandserklärung nach AktG § 93. Rein juristische Blockade.'"
                )
            else:
                st.markdown(
                    "🔴 **Master Orchestrator ➔ Site Telemetry Agent:** *'Inquire status on active work order. Why is the gate blocked?'*\n\n"
                    "🔴 **Site Telemetry Agent:** *'Emergency crew is staged on site. However, the OEM field supervisor is withholding physical access to the relay cabinet pending written corporate indemnity. Mechanical physics are nominal; access is legally blocked.'*"
                )
        elif st.session_state.conference_focus == "WHAT_UNBLOCKS":
            st.markdown("---")
            if "日本語" in lang_choice:
                st.markdown(
                    "🟢 **統括エージェント ➔ 司法シールド:** 「責任を回避し現場GMの署名を得るための法的手段は？」\n\n"
                    "🟢 **司法シールド:** 「会社法第423条に基づく取締役会免責決議（Option A）を発行することで、GM個人の賠償責任が解除され、5分以内に送電合意が成立します。」"
                )
            elif "Deutsch" in lang_choice:
                st.markdown(
                    "🟢 **Haupt-Orchestrator ➔ Fiduciary Shield:** 'Welches Rechtsinstrument entlastet den Standort-Leiter?'\n\n"
                    "🟢 **Fiduciary Shield:** 'Ein Vorstandsbeschluss zur Haftungsfreistellung nach AktG § 93. Entlastet die Geschäftsführung vollständig und hebt den Stillstand sofort auf.'"
                )
            else:
                st.markdown(
                    "🟢 **Master Orchestrator ➔ Fiduciary Shield Agent:** *'What specific legal instrument unblocks the GM without personal liability exposure?'*\n\n"
                    "🟢 **Fiduciary Shield Agent:** *'A Board Resolution (Option A) executing a Directorate Indemnity Carve-Out from the corporate Asset Defense Escrow absorbs all liability at the board level, clearing the GM to sign within 5 minutes.'*"
                )

    # ---------------------------------------------------------
    # THE THREE CASCADING BRANCHES & REMEDIAL LEVERS
    # ---------------------------------------------------------
    st.markdown("### The Three Cascading Branches & Remedial Levers")
    st.caption("Simulate executive levers to project immediate consequences across Physical, Market, and Fiduciary pillars:")

    with st.container(border=True):
        rem_col1, rem_col2 = st.columns([3, 1])
        with rem_col1:
            st.session_state.remedial_simulation = st.radio(
                "Select Executive Action to Simulate:",
                [
                    "Option A: Directorate Carve-Out (Dominant Path)",
                    "Option B: Mobilize Secondary Field Crew ($35k Draw)",
                    "Option C: Demobilize Site Contractors (Standby)",
                ],
                horizontal=True,
            )
        with rem_col2:
            st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
            if active_inc["status"] == "DEADLOCKED":
                if "Option A" in st.session_state.remedial_simulation:
                    if st.button("Execute Option A Directive", use_container_width=True, type="primary"):
                        active_inc["status"] = "RESOLVED"
                        active_inc["base_burn_rate_sec"] = 0.0
                        wo = active_inc.get("tier3_work_order", {})
                        wo["progress_pct"] = 100
                        for s in wo.get("steps", []):
                            s["done"] = True
                        for gm in active_inc.get("gms", {}).values():
                            for c in gm.get("checks", []):
                                c["status"] = "CLEARED"
                                c["evidence"] = "Directorate Override"
                        record_ledger_entry(
                            active_inc,
                            f"CHAIRMAN DIRECTIVE: Option A executed on {st.session_state.selected_incident_id}. Burn halted to 0.",
                        )
                        st.session_state.conference_focus = "NONE"
                        st.success("Option A Executed. Holding burn halted to 0.")
                        st.rerun()
                elif "Option B" in st.session_state.remedial_simulation:
                    if st.button("Authorize $35k Capital Draw", use_container_width=True):
                        record_ledger_entry(
                            active_inc,
                            f"CAPITAL DRAW: $35,000 authorized on {st.session_state.selected_incident_id}.",
                        )
                        st.success("Capital Released.")
                        st.rerun()
                else:
                    st.button("Option Inadmissible", use_container_width=True, disabled=True)

    b_col1, b_col2, b_col3 = st.columns(3)
    conf = st.session_state.conference_focus
    sim = st.session_state.remedial_simulation

    with b_col1:
        with st.container(border=True):
            st.markdown("#### Branch 1: Physical / Field")
            st.caption("Hardware Gate | Plant & Crews")
            st.markdown(f"**Cognizant Director:** {active_inc.get('director_seat', 'Board Seat')}")
            st.markdown("**Embedded Agent:** `Site Telemetry Agent`")

            if active_inc["status"] == "RESOLVED":
                st.success("✅ **Gate Cleared:** Field verification approved under board escrow.")
            elif conf == "WHY_STALLED":
                st.error("🚨 **Friction Point (CRIMSON):** Physical cabinet access held by OEM engineer pending indemnity.")
            elif conf == "WHAT_UNBLOCKS":
                st.success("🟢 **Friction Point (RESOLVED):** Cleared to grant access upon Option A execution.")
            elif "Option B" in sim:
                st.warning("⚠️ **Simulated State:** Secondary crew staged; adds 6-hour delay.")
            else:
                st.error("🚨 **Friction Point:** Testing held; OEM warranty at risk.")

            wo = active_inc.get("tier3_work_order", {})
            st.write(f"**Work Order:** `{wo.get('id', 'N/A')}` ({wo.get('progress_pct', 0)}%)")

    with b_col2:
        with st.container(border=True):
            st.markdown("#### Branch 2: Regulatory / Market")
            st.caption("Commercial Gate | Interconnection")
            st.markdown("**Cognizant Director:** Regulatory Lead")
            st.markdown("**Embedded Agent:** `Market Surveillance Agent`")

            if active_inc["status"] == "RESOLVED":
                st.success("✅ **Filing Complete:** Commercial grid gate verified.")
            elif conf == "WHY_STALLED":
                st.warning("⏳ **Friction Point (AMBER):** Statutory filing countdown running ($4.5M deposit at risk).")
            elif conf == "WHAT_UNBLOCKS":
                st.success("🟢 **Friction Point (READY):** Filing packet staged for instant transmission.")
            elif "Option C" in sim:
                st.error("🚫 **BREACH:** Regulatory queue forfeited!")
            else:
                st.warning("⏳ **Friction Point:** Interconnection gate countdown running.")

            st.write("**Handshake Status:** Latency Validated")

    with b_col3:
        with st.container(border=True):
            st.markdown("#### Branch 3: Fiduciary / Capital")
            st.caption("Balance Sheet Gate | Liability Escrow")
            st.markdown("**Cognizant Director:** Executive Board Chair")
            st.markdown("**Embedded Agent:** `Fiduciary Shield Agent`")

            if active_inc["status"] == "RESOLVED":
                st.success("✅ **Capital Defended:** Holding burn halted to 0.")
            elif conf == "WHAT_UNBLOCKS":
                st.success("🟢 **Remedial Key (EMERALD):** Directorate Carve-Out transfers liability to escrow.")
            elif "Option C" in sim:
                st.error("⚠️ **LOCKED:** Violates board duty of care.")
            else:
                st.error(f"⚠️ **Friction Point:** Holding burn crosses asset value in {active_inc['crossover_days']} days.")

            st.write(f"**Velocity:** {curr_sym}{current_burn_rate:.2f}/sec")

    # ---------------------------------------------------------
    # PIPELINE MONITOR: SUBSEQUENT 4 BOTTLENECKS
    # ---------------------------------------------------------
    with st.container(border=True):
        st.markdown("### 🔒 Gated Incident Pipeline (Next 4 Bottlenecks)")
        st.caption("Sequential project bottlenecks locked behind Milestone 1 fee settlement:")

        p1, p2, p3, p4 = st.columns(4)
        with p1:
            st.markdown("**1. Inrush Damping Curve**")
            st.caption(f"Bleed: {curr_sym}0.45/sec ({curr_sym}38.8k/day)")
            st.warning("🔒 Queued: INC-002")
        with p2:
            st.markdown("**2. SCADA IEC 61850 Gateway**")
            st.caption(f"Bleed: {curr_sym}0.18/sec ({curr_sym}15.5k/day)")
            st.warning("🔒 Queued: INC-003")
        with p3:
            st.markdown("**3. BESS Skid Firmware OTA**")
            st.caption(f"Bleed: {curr_sym}0.05/sec ({curr_sym}4.3k/day)")
            st.warning("🔒 Queued: INC-004")
        with p4:
            st.markdown("**4. Substation Oil DGA Baseline**")
            st.caption(f"Bleed: {curr_sym}0.08/sec ({curr_sym}6.9k/day)")
            st.warning("🔒 Queued: INC-005")

    # ---------------------------------------------------------
    # TIER 4: DEDICATED FORENSIC LEDGER & BJR SHIELD
    # ---------------------------------------------------------
    with st.container(border=True):
        st.markdown("### Tier 4 | Zero-Hindsight Cryptographic Audit Ledger")
        st.caption("Deterministic point-in-time flight recorder. Verifiable shield under the Business Judgment Rule.")

        for item in reversed(active_inc["audit_log"]):
            with st.expander(f"🔒 [{item['ts']}] SHA-256:{item['hash']} — {item['event']}", expanded=False):
                st.json(item.get("snapshot", {}))


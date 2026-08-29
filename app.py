import hashlib
import re
import sqlite3
from datetime import datetime, timezone
import numpy as np
import streamlit as st

st.set_page_config(
    page_title="Factory Command Post | Autonomous Capital Defense",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-Contrast Cockpit CSS with Touch-Optimized Targets
st.markdown('''
<style>
    :root {
        --bg-base: #0d1117;
        --bg-panel: #161b22;
        --line: #30363d;
        --teal: #00E5FF;
        --green: #3fb950;
        --red: #ff7b72;
        --amber: #d29922;
        --purple: #bc8cff;
        --text-main: #f0f6fc;
        --text-muted: #8b949e;
    }
    .stApp { background-color: var(--bg-base); color: var(--text-main); }
    section[data-testid="stSidebar"] { background-color: var(--bg-panel); border-right: 1px solid var(--line); }
    
    /* Top Metrics Styling */
    div[data-testid="stMetric"] { 
        background-color: var(--bg-panel); 
        border: 1px solid var(--line); 
        border-top: 3px solid var(--teal); 
        border-radius: 8px; 
        padding: 12px; 
    }
    div[data-testid="stMetricValue"] { 
        color: var(--teal) !important; 
        font-family: monospace; 
        font-size: 1.25rem !important;
        overflow: visible !important;
        white-space: normal !important;
    }
    
    /* Mobile / iPad Touch Optimization */
    .stButton > button { 
        min-height: 52px !important; 
        font-size: 1.05rem !important; 
        font-weight: 600 !important; 
        border-radius: 8px !important;
        width: 100% !important;
    }
    div[role="radiogroup"] > label { 
        min-height: 48px !important; 
        display: flex !important; 
        align-items: center !important; 
        font-size: 1.05rem !important;
        padding: 6px 12px !important;
        margin-bottom: 4px !important;
        border-radius: 6px !important;
    }
    .stSelectbox, .stNumberInput { font-size: 1.05rem !important; }
    
    /* Cards & Banners */
    .card { background-color: var(--bg-panel); border: 1px solid var(--line); border-radius: 8px; padding: 14px; margin-bottom: 12px; }
    .agent-card { background: rgba(22, 27, 34, 0.95); border: 1px solid var(--purple); border-radius: 8px; padding: 14px; margin-bottom: 12px; }
    .blueprint-card { background: rgba(22, 27, 34, 0.85); border: 1px solid #ff7b72; border-radius: 8px; padding: 16px; margin: 12px 0 20px 0; }
    .forecast-card { background: rgba(22, 27, 34, 0.85); border: 1px solid var(--amber); border-radius: 8px; padding: 16px; margin-bottom: 16px; }
    .critical-forecast-card { background: rgba(255, 77, 79, 0.08); border: 2px solid #ff4d4f; border-radius: 8px; padding: 16px; margin-bottom: 16px; box-shadow: 0 0 0 1px rgba(255,77,79,0.35), 0 0 20px rgba(255,77,79,0.7); animation: pulseCritical 1.6s ease-in-out infinite alternate; }
    @keyframes pulseCritical {
        0% { box-shadow: 0 0 0 1px rgba(255,77,79,0.2), 0 0 12px rgba(255,77,79,0.35); }
        100% { box-shadow: 0 0 0 1px rgba(255,77,79,0.7), 0 0 24px rgba(255,77,79,0.9); }
    }
    .critical-agent-card { border: 2px solid rgba(255, 122, 78, 0.95) !important; background: rgba(210,153,34,0.12) !important; box-shadow: 0 0 18px rgba(255,77,79,0.5); }
    .secondary-agent-card { opacity: 0.5; }
    .pipeline-card { background-color: #0b0e14; border: 1px solid var(--teal); border-radius: 8px; padding: 12px; margin-top: 14px; }
    .badge { display: inline-block; padding: 3px 8px; border-radius: 4px; font-size: 0.75rem; font-family: monospace; font-weight: bold; }
    .badge-active { background: rgba(0,229,255,0.15); color: var(--teal); border: 1px solid var(--teal); }
    .badge-pending { background: rgba(210,153,34,0.15); color: var(--amber); border: 1px solid var(--amber); }
    .badge-success { background: rgba(63,185,80,0.15); color: var(--green); border: 1px solid var(--green); }
    .badge-danger { background: rgba(255,123,114,0.15); color: var(--red); border: 1px solid var(--red); }
    .badge-agent { background: rgba(188,140,255,0.15); color: var(--purple); border: 1px solid var(--purple); }
    .badge-safe-harbor { background: rgba(88,166,255,0.15); color: #58a6ff; border: 1px solid #58a6ff; }

    /* Frontline Blocker Radar & Critical Checklist Item */
    .radar-card { background: rgba(255, 77, 79, 0.08); border: 2px solid #ff4d4f; border-radius: 8px; padding: 14px; margin-bottom: 16px; box-shadow: 0 0 0 1px rgba(255,77,79,0.35), 0 0 20px rgba(255,77,79,0.7); animation: pulseCritical 1.6s ease-in-out infinite alternate; }
    .radar-card-cleared { background: rgba(63,185,80,0.08); border: 2px solid var(--green); border-radius: 8px; padding: 14px; margin-bottom: 16px; }
</style>
''', unsafe_allow_html=True)

# Master Data Matrix: Complete 12 Industrial & Public Infrastructure Books
DATA_MATRIX = {
    "ERCOT BESS / storage operations": {
        "exposure": "$88.5M", "base_burn": 610000,
        "region": "West Texas — Permian Substation POI 345kV",
        "bottleneck": "PSCAD Inverter EMT Validation & 4-sec ICCP Telemetry Lag",
        "drift_metrics": {"sla_drift": "+2.5 Days", "telemetry_drift": "+8.4s (Lagging)", "cost_drift": "+$183k Carry"},
        "regime": "UPSTREAM DEPENDENCY BLOCK",
        "regime_detail": "High-voltage crews idle ($220k/wk). Blocked by inverter firmware DNP3 telemetry lag and ERCOT review queue, not field headcount.",
        "recommended_surge": 0,
        "circuit_breaker": "LOCKED: Surge funding will subsidize idle contractor carry. Inject synthetic telemetry packet to clear gate.",
        "agents": {
            "COO": {"status": "STANDBY DETECTED", "memo": "Field contractor headcount 100% mobilized but idle at POI. Zero additional labor spend recommended until telemetry clears."},
            "AFIC": {"status": "CARRYING DRAG", "memo": "Holding burn: $610k/wk. 30-day projected terminal impairment: $2.44M if uncorrected."},
            "CLO": {"status": "STATUTORY NOTICE", "memo": "ERCOT IA Section 4.2 allows filing an expedited 24-hr Provisional Part 2 COD Waiver packet."},
            "CTO": {"status": "PARAMETER MISMATCH", "memo": "Inverter firmware 2.41 dropping DNP3 heartbeat packets. Synthetic packet injection rig can clear IEEE 2800 in 4 hours."}
        },
        "critical_lead": "CTO",
        "artifacts": [("ICCP 4-sec Telemetry", "Heartbeat: 04.0s / Verified"), ("PSCAD EMT Model", "Inverter: BESS-01 / Verified"), ("IEEE 2800 Test Packet", "Ride-through: Verified"), ("Part 2 COD Attestation", "Commercial ops declaration / Assembled")],
        "checks": ["ICCP telemetry evidence verified", "ICCP telemetry record attached", "PSCAD EMT model evidence verified", "PSCAD EMT model record attached", "IEEE 2800 test packet verified", "IEEE 2800 test record attached", "COD attestation evidence verified", "COD attestation record attached"],
        "critical_check_idx": 7
    },
    "Grid Infrastructure / PJM Cluster": {
        "exposure": "$142.0M", "base_burn": 940000,
        "region": "Mid-Atlantic — 500kV Substation Transmission Intertie",
        "bottleneck": "ASTM D877 Dielectric Testing & Schedule 12 Facility Study Review",
        "drift_metrics": {"sla_drift": "+3.8 Days", "telemetry_drift": "Nominal", "cost_drift": "+$320k Carry"},
        "regime": "CAPACITY DEFICIT",
        "regime_detail": "Regional transformer oil testing lab backlog. True capacity deficit in certified high-voltage testing personnel.",
        "recommended_surge": 35,
        "circuit_breaker": "UNLOCKED: Surge funding approved to fly in 3rd-party certified ASTM testing engineers.",
        "agents": {
            "COO": {"status": "LABOR SHORTAGE", "memo": "Regional transformer oil labs at 3-week backlog. Emergency surge to mobilize mobile dielectric testing lab required."},
            "AFIC": {"status": "HIGH WACC DRAG", "memo": "$940k/wk carrying burn across $142M asset. $120k surge yields immediate 90% capital preservation ($846k/wk)."},
            "CLO": {"status": "SCHEDULE 12 RISK", "memo": "PJM tariff clause triggers daily standby demurrage starting Day 14. Statutory cure notice ready."},
            "CTO": {"status": "PERIMETER SECURE", "memo": "NERC CIP-005 Electronic Security Perimeter validated and pre-energization interlock telemetry certified."}
        },
        "critical_lead": "COO",
        "artifacts": [("ASTM D877 Dielectric Log", "Breakdown Voltage: >35kV / Verified"), ("Schedule 12 Agreement", "Facility Study Review: Complete"), ("NERC CIP-005 Perimeter", "Electronic Perimeter: Certified"), ("HV Energization Sign-off", "Safety Protocol: Assembled")],
        "checks": ["Dielectric log evidence verified", "Dielectric log record attached", "Schedule 12 agreement verified", "Schedule 12 record attached", "NERC CIP perimeter verified", "NERC CIP perimeter record attached", "HV energization sign-off verified", "HV energization record attached"],
        "critical_check_idx": 0
    },
    "ACC NZ Scheme / Claims Review": {
        "exposure": "$210.0M", "base_burn": 480000,
        "region": "Northern Hub 01 — Auckland Clinical Claims Queue",
        "bottleneck": "Manual Medical Paper Verification & Sequential Delegation Review",
        "drift_metrics": {"sla_drift": "+4.2 Days", "telemetry_drift": "Queue Lag +420", "cost_drift": "+$140k Dwell"},
        "regime": "UPSTREAM DEPENDENCY BLOCK",
        "regime_detail": "Assessor capacity adequate; blocked by sequential physical paper routing between Northern Hub and Wellington.",
        "recommended_surge": 0,
        "circuit_breaker": "LOCKED: Overtime will not resolve paper queue bottlenecks. Deploy digital triage triage workflow.",
        "agents": {
            "COO": {"status": "QUEUE SATURATION", "memo": "68% of delay caused by sequential paper routing. Deploying digital ACC45 intake eliminates queue dwell."},
            "AFIC": {"status": "EXTENDED DWELL", "memo": "Weekly dwell expense $480k. Triaging complex claims digitally collapses weekly carrying cost by $380k."},
            "CLO": {"status": "DELEGATION COMPLIANCE", "memo": "Crown Ministerial Delegation Schedule allows automated digital fast-track triage under ACC45 statutory framework."},
            "CTO": {"status": "INTAKE AUTOMATION", "memo": "Digital ACC45 triage gateway configured; ready for immediate deployment to replace paper routing."}
        },
        "critical_lead": "CLO",
        "artifacts": [("ACC45 Lodgement Log", "Digital Intake: Verified"), ("Clinical Triage Matrix", "Complex Claim Review: Cleared"), ("Vocational Assessment", "Independence Evaluation: Certified"), ("Crown Delegation Cert", "Statutory Sign-off: Assembled")],
        "checks": ["ACC45 intake evidence verified", "ACC45 intake record attached", "Clinical triage evidence verified", "Clinical triage record attached", "Vocational evaluation verified", "Vocational evaluation record attached", "Crown delegation evidence verified", "Crown delegation record attached"],
        "critical_check_idx": 6
    },
    "Port Logistics / Container Flow": {
        "exposure": "$64.0M", "base_burn": 320000,
        "region": "MetroPort — Quay Crane Terminal Node 04",
        "bottleneck": "EDIFACT BAPLIE 2.2 Deserialization Mismatch & Stevedore Demurrage",
        "drift_metrics": {"sla_drift": "+1.8 Days", "telemetry_drift": "Berth Lag +6 hrs", "cost_drift": "+$95k Demurrage"},
        "regime": "UPSTREAM DEPENDENCY BLOCK",
        "regime_detail": "Stevedore crane crews standing by. Blocked by container stowage EDI deserialization mismatch with Port Authority TOS.",
        "recommended_surge": 0,
        "circuit_breaker": "LOCKED: Stevedore overtime unnecessary. Correct TOS EDI schema parser to release container flow.",
        "agents": {
            "COO": {"status": "CRANE IDLE", "memo": "Quay cranes 03 and 04 standing down due to manifest parse errors. Twin-lift load cell safety systems fully calibrated."},
            "AFIC": {"status": "VESSEL DEMURRAGE", "memo": "Vessel dwell penalties compounding at $45k/day. Total weekly holding drag: $320k."},
            "CLO": {"status": "CUSTOMS CLEARANCE", "memo": "Customs electronic holds cleared; sole remaining blocker is EDIFACT BAPLIE data schema certification."},
            "CTO": {"status": "SCHEMA PATCH READY", "memo": "BAPLIE 2.2 parser translation mapping hotfix prepared; restores automated crane sequence planning instantly."}
        },
        "critical_lead": "CTO",
        "artifacts": [("BAPLIE 2.2 EDI Log", "Container Manifest: Verified"), ("TOS Berth Sequence", "Berth Allocation Plan: Active"), ("Crane Load Cell Cert", "Calibration: Approved"), ("Quay Release Authority", "Port Authority Gate: Assembled")],
        "checks": ["BAPLIE manifest verified", "BAPLIE manifest attached", "TOS sequence plan verified", "TOS sequence plan attached", "Load cell calibration verified", "Load cell calibration attached", "Quay release authority verified", "Quay release authority attached"],
        "critical_check_idx": 1
    },
    "Hyperscale Data Center / Power Intertie": {
        "exposure": "$310.0M", "base_burn": 1450000,
        "region": "Northern Virginia — 200MW Substation Primary Feeder",
        "bottleneck": "Medium-Voltage Gas-Insulated Switchgear (GIS) SF6 Gas Leak Attestation",
        "drift_metrics": {"sla_drift": "+5.0 Days", "telemetry_drift": "Pressure Delta -0.4 bar", "cost_drift": "+$580k WACC"},
        "regime": "CAPACITY DEFICIT",
        "regime_detail": "Certified high-voltage GIS pressure technicians unavailable locally. Server racks energized on diesel backup at $210k/day.",
        "recommended_surge": 40,
        "circuit_breaker": "UNLOCKED: Surge funding approved for emergency OEM field service flight teams.",
        "agents": {
            "COO": {"status": "SPECIALIST DEFICIT", "memo": "Certified OEM GIS switchgear technicians require emergency mobilization from Zurich headquarters."},
            "AFIC": {"status": "DIESEL BURN", "memo": "Backup diesel generation costing $210k/day + $1.45M weekly WACC drag. Rapid grid energization critical."},
            "CLO": {"status": "EPA COMPLIANCE", "memo": "EPA Section 608 attestation required for SF6 gas handling before closing breaker onto utility feeder."},
            "CTO": {"status": "TELEMETRY READY", "memo": "Substation RTU fiber loop and backup power transfer switch logic validated."}
        },
        "critical_lead": "COO",
        "artifacts": [("SF6 Pressure Attestation", "Gas Density: Nominal / Sealed"), ("GIS Dielectric Cert", "HV Pressure Test: Passed"), ("EPA 608 Environmental Sign-off", "Emissions Compliance: Certified"), ("Utility Intertie Release", "Breaker Sync: Assembled")],
        "checks": ["SF6 density log verified", "SF6 density record attached", "GIS dielectric cert verified", "GIS dielectric cert attached", "EPA compliance verified", "EPA compliance attached", "Breaker sync verified", "Breaker sync attached"],
        "critical_check_idx": 1
    },
    "Offshore Wind / North Sea Subsea HVDC": {
        "exposure": "$520.0M", "base_burn": 2100000,
        "region": "Dogger Bank — 1.2GW Offshore Converter Platform POI",
        "bottleneck": "Subsea HVDC Cable Fiber-Optic DTS Temperature Anomaly & Joint Cert",
        "drift_metrics": {"sla_drift": "+6.2 Days", "telemetry_drift": "DTS Loop +4.1°C", "cost_drift": "+$890k Demurrage"},
        "regime": "UPSTREAM DEPENDENCY BLOCK",
        "regime_detail": "Cable-laying vessel costing $180k/day on weather standby. Blocked by optical time-domain reflectometer (OTDR) calibration mismatch.",
        "recommended_surge": 0,
        "circuit_breaker": "LOCKED: Vessel demurrage is software-blocked. Recalibrate DTS optical threshold before ordering re-pull.",
        "agents": {
            "COO": {"status": "VESSEL STANDBY", "memo": "DP2 installation vessel idle at offshore coordinates. Sensor threshold recalibration needed, not subsea re-lay."},
            "AFIC": {"status": "MASSIVE DEMURRAGE", "memo": "Platform carrying drag: $2.1M/week. Total exposure $520M. Fast OTDR recalibration saves $1.89M."},
            "CLO": {"status": "MARITIME PERMIT", "memo": "UK Crown Estate seabed lease work window expires in 11 days. Regulatory extension drafted."},
            "CTO": {"status": "DTS CALIBRATION", "memo": "Subsea fiber distributed temperature sensing (DTS) optical splice recalibration script ready."}
        },
        "critical_lead": "CTO",
        "artifacts": [("OTDR Optical Splice Log", "Reflectometry: 0.02dB / Verified"), ("HVDC Joint Pressure Attestation", "Hydrostatic Seal: Passed"), ("Crown Estate Seabed Cert", "Work Permit: Active"), ("Platform COD Protocol", "Energization: Assembled")],
        "checks": ["OTDR splice log verified", "OTDR splice log attached", "Joint pressure cert verified", "Joint pressure cert attached", "Seabed permit verified", "Seabed permit attached", "Platform COD verified", "Platform COD attached"],
        "critical_check_idx": 1
    },
    "Semiconductor Fab / Cleanroom Commissioning": {
        "exposure": "$440.0M", "base_burn": 1850000,
        "region": "Phoenix East — 3nm Lithography Bay Node 02",
        "bottleneck": "ISO Class 1 Airborne Particle Count Spikes & Ultra-Pure Water TOC Drift",
        "drift_metrics": {"sla_drift": "+3.1 Days", "telemetry_drift": "TOC +12 ppb Drift", "cost_drift": "+$620k Carry"},
        "regime": "UPSTREAM DEPENDENCY BLOCK",
        "regime_detail": "EUV tool installation engineers idle on site. Blocked by sensor baseline drift in UPW TOC analyzer.",
        "recommended_surge": 0,
        "circuit_breaker": "LOCKED: Cleanroom trades are fully staffed. Recalibrate TOC analyzer sensor baseline.",
        "agents": {
            "COO": {"status": "TRADES ON STANDBY", "memo": "ASML EUV installation specialists waiting on bay air cert. Physical particle scrubbing complete."},
            "AFIC": {"status": "DEPRECIATION DRAG", "memo": "Fab facility depreciation and carrying cost: $1.85M/wk. Quick sensor zero-point fix unblocks $396k/wk fee."},
            "CLO": {"status": "CHIPS ACT AUDIT", "memo": "Federal grant milestone compliance verification protocol ready for submission upon cleanroom sign-off."},
            "CTO": {"status": "ANALYZER RECAL", "memo": "Ultra-Pure Water TOC sensor zero-point baseline firmware recalibration code compiled."}
        },
        "critical_lead": "CTO",
        "artifacts": [("ISO Class 1 Particle Log", "0.1μm Count: <10 / Verified"), ("UPW TOC Analysis", "Total Organic Carbon: <0.5ppb"), ("Cleanroom Pressure Cert", "Positive Pressure: 45Pa"), ("EUV Bay Handover", "Tool Delivery Clearance: Ready")],
        "checks": ["Particle log evidence verified", "Particle log record attached", "UPW TOC log verified", "UPW TOC log record attached", "Pressure cert verified", "Pressure cert attached", "Bay handover verified", "Bay handover attached"],
        "critical_check_idx": 3
    },
    "Critical Minerals / Lithium Refining Facility": {
        "exposure": "$175.0M", "base_burn": 720000,
        "region": "Pilbara — Battery-Grade Hydroxide Calcination Train 01",
        "bottleneck": "Rotary Kiln Refractory Temperature Gradient & Environmental Water Discharge",
        "drift_metrics": {"sla_drift": "+4.0 Days", "telemetry_drift": "Kiln Delta +35°C", "cost_drift": "+$240k Carry"},
        "regime": "CAPACITY DEFICIT",
        "regime_detail": "Refractory brick masons and pyrometallurgical specialists unavailable in remote zone.",
        "recommended_surge": 30,
        "circuit_breaker": "UNLOCKED: Surge budget approved to air-charter specialized kiln refractory repair crew.",
        "agents": {
            "COO": {"status": "CREW DEFICIT", "memo": "Kiln refractory hot-spot requires certified rotary kiln refractory masons via FIFO charter."},
            "AFIC": {"status": "OEM OFFTAKE RISK", "memo": "$720k/wk burn. OEM battery offtake agreement delivery penalty window triggers in 14 days."},
            "CLO": {"status": "EPA DISCHARGE PERMIT", "memo": "Western Australia DWER discharge license conditions verified and water treatment logs cleared."},
            "CTO": {"status": "PYROMETRY TELEMETRY", "memo": "Thermal imaging pyrometry array operational and ready for post-repair kiln light-up."}
        },
        "critical_lead": "COO",
        "artifacts": [("Kiln Thermal Attestation", "Temperature Gradient: Nominal"), ("Refractory Masonry Cert", "High-Alumina Brick: Certified"), ("DWER Environmental Permit", "Water Discharge: Approved"), ("Calcination Commissioning", "First Spodumene Feed: Ready")],
        "checks": ["Kiln thermal log verified", "Kiln thermal log attached", "Masonry cert verified", "Masonry cert attached", "DWER permit verified", "DWER permit attached", "Calcination log verified", "Calcination log attached"],
        "critical_check_idx": 2
    },
    "Rail Freight & Intermodal Corridor": {
        "exposure": "$95.0M", "base_burn": 390000,
        "region": "Chicago Intermodal — Automated Switching Yard Track 12",
        "bottleneck": "Positive Train Control (PTC) Interlocking Transponder Sync Failure",
        "drift_metrics": {"sla_drift": "+2.0 Days", "telemetry_drift": "PTC Sync -140ms", "cost_drift": "+$110k Delay"},
        "regime": "UPSTREAM DEPENDENCY BLOCK",
        "regime_detail": "Locomotives and manifest trains held on siding. Blocked by wayside interface unit (WIU) encryption key sync.",
        "recommended_surge": 0,
        "circuit_breaker": "LOCKED: Train crews standing by. Re-push WIU cryptographic security certificate to wayside units.",
        "agents": {
            "COO": {"status": "YARD GRIDLOCK", "memo": "Classification track blocked. Dispatch crews waiting on wayside clear signal; mechanicals ready."},
            "AFIC": {"status": "CARRIER PENALTIES", "memo": "Class 1 railroad dwell penalties: $390k/week. Encryption cert push resolves blockage immediately."},
            "CLO": {"status": "FRA MANDATE", "memo": "Federal Railroad Administration 49 CFR Part 236 safety compliance sign-off prepared."},
            "CTO": {"status": "PTC KEY ROTATION", "memo": "Wayside Interface Unit PKI encryption certificate re-push payload ready for transmission."}
        },
        "critical_lead": "CTO",
        "artifacts": [("PTC Transponder Telemetry", "Sync Heartbeat: <10ms / Verified"), ("Wayside PKI Security Cert", "Encryption Key: Active"), ("FRA Part 236 Attestation", "Safety Appliance: Certified"), ("Yard Dispatch Release", "Interlocking Sequence: Active")],
        "checks": ["PTC telemetry verified", "PTC telemetry attached", "PKI security cert verified", "PKI security cert attached", "FRA attestation verified", "FRA attestation attached", "Yard release verified", "Yard release attached"],
        "critical_check_idx": 3
    },
    "Defense Manufacturing / Naval Shipyard": {
        "exposure": "$680.0M", "base_burn": 2800000,
        "region": "Groton — Submarine Drydock Hull Section Hydrostatic Pressure Gate",
        "bottleneck": "HY-80 High-Yield Steel Ultrasonic NDT Weld Defect Verification",
        "drift_metrics": {"sla_drift": "+7.5 Days", "telemetry_drift": "NDT Queue +18 Welds", "cost_drift": "+$1.1M Labor Drag"},
        "regime": "CAPACITY DEFICIT",
        "regime_detail": "Shortage of Level III Ultrasonic NDT certified radiographers with active security clearances.",
        "recommended_surge": 50,
        "circuit_breaker": "UNLOCKED: Surge authorized for cleared Level III NDT radiographers from secondary naval facility.",
        "agents": {
            "COO": {"status": "CLEARANCE BOTTLENECK", "memo": "Hull assembly blocked. Emergency travel surge for Top Secret-cleared Level III NDT radiographers approved."},
            "AFIC": {"status": "DRYDOCK CARRY", "memo": "Drydock occupancy carrying cost: $2.8M/week. Total capital recovery potential: $2.52M client retention."},
            "CLO": {"status": "NAVSEA COMPLIANCE", "memo": "NAVSEA Technical Publication 248 welding attestation and MIL-STD compliance packet assembled."},
            "CTO": {"status": "PHASED ARRAY DATA", "memo": "Phased Array Ultrasonic Testing (PAUT) digital radiography imaging database operational."}
        },
        "critical_lead": "COO",
        "artifacts": [("PAUT NDT Weld Map", "Volumetric Scan: 100% / Passed"), ("Level III Radiographer Cert", "NAVSEA Qualified: Verified"), ("NAVSEA 248 Compliance", "Hull Integrity: Approved"), ("Drydock Flooding Authority", "Submersion Gate: Assembled")],
        "checks": ["NDT weld map verified", "NDT weld map attached", "Radiographer cert verified", "Radiographer cert attached", "NAVSEA attestation verified", "NAVSEA attestation attached", "Flooding authority verified", "Flooding authority attached"],
        "critical_check_idx": 2
    },
    "Municipal Water & Desalination Plant": {
        "exposure": "$115.0M", "base_burn": 450000,
        "region": "Carlsbad — 50MGD Seawater Reverse Osmosis Train 04",
        "bottleneck": "Polyamide RO Membrane Silt Density Index (SDI) & Boron Rejection Cert",
        "drift_metrics": {"sla_drift": "+3.4 Days", "telemetry_drift": "SDI Index 4.8 (High)", "cost_drift": "+$135k Chemical"},
        "regime": "UPSTREAM DEPENDENCY BLOCK",
        "regime_detail": "Plant operators waiting on coagulant dosing algorithm calibration from chemical dosing vendor.",
        "recommended_surge": 0,
        "circuit_breaker": "LOCKED: Membrane flush crews ready. Update chemical feed dosing profile in SCADA system.",
        "agents": {
            "COO": {"status": "MEMBRANES IDLE", "memo": "High-pressure pump trains in recirc mode. Coagulant dosing software fix will bring SDI under 3.0."},
            "AFIC": {"status": "CHEMICAL BLEED", "memo": "Holding drag: $450k/week in idle power and pretreatment chemicals. Rapid gate clear preserves $405k."},
            "CLO": {"status": "POTABLE WATER STD", "memo": "Title 22 California Drinking Water Standards compliance testing certification ready."},
            "CTO": {"status": "SCADA DOSING PROFILE", "memo": "PLC chemical feed PID loop tuning parameter payload ready for deployment."}
        },
        "critical_lead": "CTO",
        "artifacts": [("SDI Membrane Permeate Log", "SDI15: 2.8 / Passed"), ("Boron Rejection Analysis", "Boron: <0.5mg/L / Verified"), ("Title 22 Potable Water Cert", "Health Standard: Approved"), ("Municipal Distribution Gate", "Water Delivery Release: Active")],
        "checks": ["SDI permeate log verified", "SDI permeate log attached", "Boron analysis verified", "Boron analysis attached", "Title 22 cert verified", "Title 22 cert attached", "Distribution gate verified", "Distribution gate attached"],
        "critical_check_idx": 1
    },
    "Commercial Aviation / Fleet AOG Turnaround": {
        "exposure": "$160.0M", "base_burn": 850000,
        "region": "Dallas MRO Hub — Widebody CFM LEAP-1B Engine Mount Replacement",
        "bottleneck": "FAA Form 8130-3 Dual-Release Airworthiness Tag Missing Serial Match",
        "drift_metrics": {"sla_drift": "+2.2 Days", "telemetry_drift": "Gate Hold +48 hrs", "cost_drift": "+$340k AOG"},
        "regime": "UPSTREAM DEPENDENCY BLOCK",
        "regime_detail": "A&P mechanics on floor with tools in hand. Aircraft on Ground (AOG) due to digital certificate serial mismatch.",
        "recommended_surge": 0,
        "circuit_breaker": "LOCKED: Mechanics are standing by. OEM digital signature API re-transmission clears tail release.",
        "agents": {
            "COO": {"status": "MECHANICS IDLE", "memo": "Airframe mechanics complete; aircraft cannot be signed into service without dual-release airworthiness tag."},
            "AFIC": {"status": "AOG BLEED", "memo": "AOG revenue loss + leased engine carry: $850k/week ($121k/day). Direct 90% client recovery: $765k."},
            "CLO": {"status": "FAA 14 CFR 43.9", "memo": "FAA airworthiness conformity and maintenance log entry ready for Chief Inspector release."},
            "CTO": {"status": "SPEC2000 API PATCH", "memo": "ATA Spec 2000 digital certificate XML exchange gateway re-push configured and ready."}
        },
        "critical_lead": "CTO",
        "artifacts": [("FAA 8130-3 Airworthiness Tag", "Dual Release: Verified"), ("Spec 2000 Digital Trace", "Engine Mount Serial: Matched"), ("Chief Inspector Release", "Airworthiness: Signed"), ("Flight Operations Handover", "Tail In-Service: Ready")],
        "checks": ["FAA 8130-3 evidence verified", "FAA 8130-3 record attached", "Spec 2000 trace verified", "Spec 2000 trace attached", "Inspector release verified", "Inspector release attached", "Flight ops handover verified", "Flight ops handover attached"],
        "critical_check_idx": 3
    }
}

DEFAULT_SURGICAL_BUDGET = {
    "blunt_spend_warning": "🛑 Blunt Spend Trap: Adding 14 electrician headcounts costs $220,000/wk but cannot resolve firmware communication errors.",
    "surgical_line_items": [
        {"item": "Inverter OEM Senior Firmware Specialist (On-Site)", "cost": 15000, "vendor": "PowerGrid Dynamics"},
        {"item": "Synthetic DNP3 Packet Injection Test Rig Lease (48-hr)", "cost": 20000, "vendor": "Substation Systems Corp"},
    ],
    "total_surgical_cost": 35000,
    "capital_efficiency_ratio": "15.7x Value Preserved vs. Surgical Spend",
}

for book_name, book_data in DATA_MATRIX.items():
    book_data.setdefault("critical_lead", None)
    book_data.setdefault("critical_check_idx", None)
    book_data.setdefault("checklist", book_data["checks"])
    book_data.setdefault("surgical_budget", {
        **DEFAULT_SURGICAL_BUDGET,
        "surgical_line_items": [item.copy() for item in DEFAULT_SURGICAL_BUDGET["surgical_line_items"]],
    })
    book_data.setdefault("phase_2", {
        "bottleneck": "Phase 2: Secondary Recovery Queue Awaiting Director Approval",
        "target_director": "CTO",
        "focus": "Systems Revalidation",
        "failure_mode": "Secondary queue gate remains unresolved after Phase 1 release.",
        "recommended_resolution": "Stage the follow-on technical remediation and route the issue to the designated executive director for approval.",
        "regime": "SECONDARY QUEUE HOLD",
        "regime_detail": "Sensing layer detected a phase-two process gate beyond initial commissioning. The site team has cleared the first wave but a second dependency remains in the queue.",
        "checks": ["Secondary queue gate evidence verified", "Secondary queue gate record attached", "Director-approved remediation deployed", "Systems revalidation test passed", "Field engineer secondary sign-off verified", "Field engineer secondary sign-off attached", "Secondary compliance attestation verified", "Secondary compliance attestation attached"],
    })

BLOCKER_DIAGNOSTICS = {
    "ERCOT BESS / storage operations": {"technical_root_cause": "Inverter firmware v2.41 drops DNP3 heartbeat telemetry packets during the 4-second polling cycle.", "missing_artifact_name": "Signed Part 2 COD Commercial Operation Attestation and 4-hour clean packet trace.", "standby_impact": "High-voltage switchgear crew idle at the Permian POI; $220,000/week idle carry.", "gm_remediation_request": "Authorize dispatch of the Synthetic Packet Injection Rig or file the expedited 24-hour Provisional Part 2 COD Waiver under ERCOT IA Section 4.2."},
    "Grid Infrastructure / PJM Cluster": {"technical_root_cause": "ASTM D877 dielectric validation is stalled in the regional transformer-oil laboratory backlog.", "missing_artifact_name": "Certified ASTM D877 dielectric breakdown log and executed Schedule 12 Facility Study Review.", "standby_impact": "Energization contractor pool remains idle at the 500kV intertie; daily standby demurrage begins on Day 14.", "gm_remediation_request": "Authorize emergency mobilization of a mobile ASTM testing laboratory with third-party certified high-voltage engineers."},
    "ACC NZ Scheme / Claims Review": {"technical_root_cause": "Sequential physical-paper routing between Northern Hub and Wellington is holding the statutory delegation chain.", "missing_artifact_name": "Executed Crown delegation certificate and digitally lodged ACC45 evidence record.", "standby_impact": "Clinical assessors are idle behind the paper queue; claims dwell is carrying $480,000/week.", "gm_remediation_request": "Authorize the digital ACC45 fast-track triage workflow and obtain the delegated ministerial approval for complex cases."},
    "Port Logistics / Container Flow": {"technical_root_cause": "The Port Authority TOS rejects the EDIFACT BAPLIE 2.2 stowage manifest because of a deserialization schema mismatch.", "missing_artifact_name": "Certified BAPLIE translation trace and Port Authority quay release authority.", "standby_impact": "Quay cranes 03 and 04 and stevedore crews are standing down; vessel demurrage is $45,000/day.", "gm_remediation_request": "Authorize deployment of the BAPLIE 2.2 parser translation hotfix and obtain Port Authority schema certification."},
    "Hyperscale Data Center / Power Intertie": {"technical_root_cause": "GIS SF6 pressure validation cannot close because no certified OEM technician is available to attest the gas-leak remediation.", "missing_artifact_name": "Signed SF6 pressure attestation and EPA Section 608 environmental handling sign-off.", "standby_impact": "Server racks remain on diesel backup at $210,000/day while the primary feeder crew awaits breaker close.", "gm_remediation_request": "Authorize an emergency OEM GIS field-service flight team to complete the pressure test and issue the SF6 attestation."},
    "Offshore Wind / North Sea Subsea HVDC": {"technical_root_cause": "The subsea DTS optical splice calibration is misreading the temperature threshold during OTDR verification.", "missing_artifact_name": "Calibrated OTDR optical splice log and signed HVDC joint pressure attestation.", "standby_impact": "The DP2 cable-laying vessel is weather-standby offshore at $180,000/day.", "gm_remediation_request": "Authorize remote deployment of the DTS optical recalibration script and retain the vessel through the verification retest."},
    "Semiconductor Fab / Cleanroom Commissioning": {"technical_root_cause": "The ultra-pure-water TOC analyzer has a zero-point sensor baseline drift, invalidating cleanroom release evidence.", "missing_artifact_name": "Signed UPW TOC calibration trace and ISO Class 1 cleanroom handover record.", "standby_impact": "ASML EUV installation specialists are idle in Phoenix East while the 3nm bay remains uncertified.", "gm_remediation_request": "Authorize immediate TOC analyzer firmware recalibration and an expedited cleanroom recertification run."},
    "Critical Minerals / Lithium Refining Facility": {"technical_root_cause": "A rotary-kiln refractory hot spot exceeds the allowed thermal gradient and requires certified masonry repair.", "missing_artifact_name": "Post-repair kiln thermal attestation and certified refractory masonry record.", "standby_impact": "Calcination commissioning is held in Pilbara with FIFO maintenance crews awaiting a safe light-up window.", "gm_remediation_request": "Authorize a FIFO air charter for certified rotary-kiln refractory masons and release the post-repair pyrometry test."},
    "Rail Freight & Intermodal Corridor": {"technical_root_cause": "Wayside Interface Unit encryption keys are out of sync, preventing Positive Train Control interlocking confirmation.", "missing_artifact_name": "Reissued Wayside PKI security certificate and PTC transponder synchronization trace.", "standby_impact": "Locomotives and manifest trains are held on siding at Chicago Intermodal, carrying $390,000/week in dwell penalties.", "gm_remediation_request": "Authorize the WIU cryptographic certificate re-push and a supervised PTC interlocking retest."},
    "Defense Manufacturing / Naval Shipyard": {"technical_root_cause": "HY-80 weld disposition is waiting on a Top Secret-cleared Level III ultrasonic NDT radiographer.", "missing_artifact_name": "NAVSEA-qualified Level III radiographer certificate and signed PAUT weld-map disposition.", "standby_impact": "Drydock hull assembly is held with $2.8 million/week occupancy carry.", "gm_remediation_request": "Authorize emergency travel for a cleared Level III NDT radiographer from the secondary naval facility."},
    "Municipal Water & Desalination Plant": {"technical_root_cause": "The SCADA chemical-feed PID profile is overdosing coagulant, leaving the membrane SDI above the potable-water release threshold.", "missing_artifact_name": "Verified SDI permeate log and signed boron rejection analysis.", "standby_impact": "High-pressure pump trains remain in recirculation while pretreatment chemicals and idle power carry $450,000/week.", "gm_remediation_request": "Authorize deployment of the PLC chemical-feed tuning payload and an accelerated Title 22 confirmation sample."},
    "Commercial Aviation / Fleet AOG Turnaround": {"technical_root_cause": "The ATA Spec 2000 gateway cannot match the FAA Form 8130-3 dual-release serial to the replacement engine mount.", "missing_artifact_name": "Matched FAA Form 8130-3 dual-release tag and signed Spec 2000 digital trace.", "standby_impact": "A&P mechanics and the widebody aircraft remain AOG at Dallas MRO; revenue and lease carry is $850,000/week.", "gm_remediation_request": "Authorize an OEM digital-signature API retransmission and Chief Inspector priority review for tail release."},
}

for book_name, blocker_diagnostic in BLOCKER_DIAGNOSTICS.items():
    DATA_MATRIX[book_name]["blocker_diagnostic"] = blocker_diagnostic

DATA_MATRIX["ERCOT BESS / storage operations"]["critical_lead"] = "CTO"
DATA_MATRIX["ERCOT BESS / storage operations"]["phase_2"] = {
    "bottleneck": "Phase 2: 100-Hour Continuous C-Rate Thermal Run & Cell Balancing",
    "target_director": "CTO",
    "focus": "Thermal Firmware Patch",
    "failure_mode": "Thermal drift continues after Phase 1 release, leaving the battery in a continuous C-rate balancing loop.",
    "recommended_resolution": "Deploy the thermal firmware patch and re-run continuous balancing under the 100-hour validation window.",
    "regime": "SECONDARY QUEUE HOLD",
    "regime_detail": "Phase 1 telemetry locks are cleared, but cell balancing still fails under sustained C-rate stress and must be corrected before final release.",
    "checks": ["Pyrometry thermal sensor array calibrated", "Continuous C-rate load cell stable at 345kV", "Coolant flow delta within +/- 1.5 deg C bounds", "Cell balancing active equalization verified", "Thermal runaway mitigation circuit verified", "Inverter thermal log attached", "SCADA pyrometry stream attached", "100-Hour continuous run certificate attached"],
    "critical_check_idx": 7,
}
DATA_MATRIX["ERCOT BESS / storage operations"]["phase2_burn"] = "183k"
DATA_MATRIX["Grid Infrastructure / PJM Cluster"]["critical_lead"] = "COO"
DATA_MATRIX["Grid Infrastructure / PJM Cluster"]["phase_2"] = {
    "bottleneck": "Phase 2: Substation Interlock Logic & Relay Trip Calibration",
    "target_director": "COO",
    "focus": "Protection Crew Mobilization",
    "failure_mode": "Relay trip calibration remains misaligned after the initial energization gate and is creating a protection logic hold.",
    "recommended_resolution": "Mobilize the protection crew and complete interlock logic calibration before re-entering the dispatch sequence.",
    "regime": "SECONDARY QUEUE HOLD",
    "regime_detail": "The transmission study is resolved, but the live relay logic remains out of calibration and can short-circuit the next commissioning stage.",
    "checks": ["Protection crew mobilized on site", "Relay trip calibration evidence verified", "Relay trip calibration record attached", "Interlock logic sequence validated", "SCADA dispatch handshake confirmed", "Backup protection scheme armed", "Live relay test log evidence verified", "Live relay test log record attached"],
}
DATA_MATRIX["ACC NZ Scheme / Claims Review"]["critical_lead"] = "CLO"
DATA_MATRIX["ACC NZ Scheme / Claims Review"]["phase_2"] = {
    "bottleneck": "Phase 2: Complex Vocational Rehabilitation Delegation Gate",
    "target_director": "CLO",
    "focus": "Ministerial Waiver",
    "failure_mode": "Complex vocational rehabilitation approvals are still caught behind a ministerial delegation gate after intake triage is complete.",
    "recommended_resolution": "Secure the delegated ministerial waiver and release the complex case review workflow to the next action queue.",
    "regime": "SECONDARY QUEUE HOLD",
    "regime_detail": "The digital triage lane is active, but high-complexity vocational cases remain pending ministerial delegation and cannot advance without legal approval.",
    "checks": ["Ministerial waiver request filed", "Ministerial waiver evidence verified", "Ministerial waiver record attached", "Complex case review reassigned", "Vocational rehabilitation plan updated", "Independent medical review scheduled", "Delegated authority sign-off verified", "Delegated authority sign-off attached"],
}
DATA_MATRIX["Critical Minerals / Lithium Refining Facility"]["critical_lead"] = "COO"
DATA_MATRIX["Defense Manufacturing / Naval Shipyard"]["critical_lead"] = "COO"
DATA_MATRIX["Commercial Aviation / Fleet AOG Turnaround"]["critical_lead"] = "CTO"

# Defensive Session State Initialization
for key, default in [
    ('ledger', []), ('cleared_books', {}), ('directive_issued', {}),
    ('board_escalation', {}), ('board_quorum', {}), ('active_phase', {}), ('phase_2_authorized', {}),
    ('surgical_spend_authorized', {}), ('surgical_purchase_orders', {}),
    ('detection_time', {}), ('override_logged', {}),
    ('active_view', '1️⃣ Tier 1 | Chairman Directorate'),
    ('last_sync', datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")),
    ('override_active', False), ('master_surge', 0),
    ('auto_override_triggered', False), ('master_surge_cap', 0), ('safe_harbor_active', False),
    ('escalation_transmitted', False), ('sop_checklist', [False] * 8),
    ('pipeline_step_1', 'PENDING'), ('pipeline_step_2', 'PENDING'),
    ('pipeline_step_3', 'PENDING'), ('pipeline_step_4', 'PENDING'),
    ('chairman_override_active', False), ('quorum_votes', [False, False, False, False])
]:
    if key not in st.session_state or (isinstance(default, dict) and not isinstance(st.session_state[key], dict)) or (isinstance(default, list) and not isinstance(st.session_state[key], list)):
        st.session_state[key] = default

# Navigation Callbacks
def nav_to(target_view):
    st.session_state['active_view'] = target_view

def trigger_sync():
    st.session_state['last_sync'] = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    st.toast("Forensic State Sync Completed across all 12 Books & Agents", icon="🔄")

def reset_book(book_name):
    st.session_state['cleared_books'][book_name] = False
    st.session_state['directive_issued'][book_name] = False
    st.session_state['board_escalation'][book_name] = False
    st.session_state['board_quorum'][book_name] = False
    st.session_state['override_active'] = False
    st.session_state['master_surge'] = 0
    st.session_state['auto_override_triggered'] = False
    st.session_state['master_surge_cap'] = 0
    st.session_state['safe_harbor_active'] = False
    st.session_state['escalation_transmitted'] = False
    st.session_state['active_phase'][book_name] = 1
    st.session_state['phase_2_authorized'][book_name] = False
    st.session_state['surgical_spend_authorized'][book_name] = False
    st.session_state['surgical_purchase_orders'][book_name] = []
    st.session_state['detection_time'][book_name] = datetime.now(timezone.utc)
    st.session_state['override_logged'][book_name] = False
    st.session_state['active_view'] = '1️⃣ Tier 1 | Chairman Directorate'
    for i in range(8):
        st.session_state[f"chk_{book_name}_{i}"] = False
        st.session_state[f"chk2_{book_name}_{i}"] = False
    for c in ['ops', 'afic', 'risk', 'tech']:
        st.session_state[f"comm_{book_name}_{c}"] = False


def get_phase_context(book_name):
    active_phase = st.session_state['active_phase'].get(book_name, 1)
    phase_2 = DATA_MATRIX[book_name].get('phase_2', {
        'bottleneck': 'Phase 2: Secondary Recovery Queue Awaiting Director Approval',
        'target_director': 'CTO',
        'focus': 'Systems Revalidation',
        'failure_mode': 'Secondary queue gate remains unresolved after Phase 1 release.',
        'recommended_resolution': 'Deploy the follow-on technical remediation and route approval to the designated executive director.',
        'regime': 'SECONDARY QUEUE HOLD',
        'regime_detail': 'The site team has cleared Phase 1 but a second dependency remains pending executive approval.',
        'checks': ['Secondary queue gate evidence verified', 'Secondary queue gate record attached', 'Director-approved remediation deployed', 'Systems revalidation test passed', 'Field engineer secondary sign-off verified', 'Field engineer secondary sign-off attached', 'Secondary compliance attestation verified', 'Secondary compliance attestation attached'],
    })
    return active_phase, phase_2


AUDIT_DB_PATH = "audit_ledger.db"
LEGAL_PRIVILEGE_TAG = "PRIVILEGED — STATUTORY RISK MANAGEMENT WORK PRODUCT"


def init_db():
    conn = sqlite3.connect(AUDIT_DB_PATH)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS audit_ledger (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            book TEXT,
            t0_detection TEXT,
            t1_resolution TEXT,
            governance_lag TEXT,
            hesitation_cost REAL,
            authority TEXT,
            sha256_hash TEXT,
            legal_privilege_tag TEXT
        )
    ''')
    conn.commit()
    conn.close()


def log_audit_event(book, t0_detection, t1_resolution, governance_lag, hesitation_cost, authority, sha256_hash, legal_privilege_tag=LEGAL_PRIVILEGE_TAG):
    conn = sqlite3.connect(AUDIT_DB_PATH)
    conn.execute(
        "INSERT INTO audit_ledger (timestamp, book, t0_detection, t1_resolution, governance_lag, hesitation_cost, authority, sha256_hash, legal_privilege_tag) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
            book, t0_detection, t1_resolution, governance_lag, hesitation_cost, authority, sha256_hash, legal_privilege_tag
        )
    )
    conn.commit()
    conn.close()


def fetch_audit_events():
    conn = sqlite3.connect(AUDIT_DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM audit_ledger ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(row) for row in rows]


init_db()


def append_forensic_entry(book_name, authority, resolution_time=None):
    detection_time = st.session_state['detection_time'].get(book_name)
    if detection_time is None:
        detection_time = datetime.now(timezone.utc)
        st.session_state['detection_time'][book_name] = detection_time
    if resolution_time is None:
        resolution_time = datetime.now(timezone.utc)

    gov_lag = resolution_time - detection_time
    lag_seconds = max(gov_lag.total_seconds(), 0)
    hesitation_cost = (DATA_MATRIX[book_name]['base_burn'] / (7 * 86400)) * lag_seconds

    forensic_entry = {
        "Book": book_name,
        "T0 Agent Detection": detection_time.strftime("%Y-%m-%d %H:%M:%S UTC"),
        "T1 Action Resolved": resolution_time.strftime("%Y-%m-%d %H:%M:%S UTC"),
        "Governance Lag": f"{lag_seconds:.0f} seconds",
        "Hesitation Cost ($)": f"${hesitation_cost:,.2f}",
        "Authorizing Authority": authority,
    }
    signature_payload = "|".join([
        forensic_entry["Book"],
        forensic_entry["T0 Agent Detection"],
        forensic_entry["T1 Action Resolved"],
        forensic_entry["Governance Lag"],
        forensic_entry["Hesitation Cost ($)"],
        forensic_entry["Authorizing Authority"],
    ])
    forensic_entry["SHA-256 Signature"] = hashlib.sha256(signature_payload.encode()).hexdigest()
    st.session_state['ledger'].append(forensic_entry)
    log_audit_event(
        book=book_name,
        t0_detection=forensic_entry["T0 Agent Detection"],
        t1_resolution=forensic_entry["T1 Action Resolved"],
        governance_lag=forensic_entry["Governance Lag"],
        hesitation_cost=hesitation_cost,
        authority=authority,
        sha256_hash=forensic_entry["SHA-256 Signature"],
    )
    st.session_state['detection_time'][book_name] = datetime.now(timezone.utc)


def parse_cost_drift_dollars(cost_drift_str):
    match = re.search(r'\$([\d.]+)([kM]?)', cost_drift_str)
    if not match:
        return 0.0
    value, suffix = match.groups()
    value = float(value)
    if suffix == 'k':
        value *= 1_000
    elif suffix == 'M':
        value *= 1_000_000
    return value

# Sidebar Controls
st.sidebar.title("FACTORY COMMAND POST")
st.sidebar.caption("Autonomous Capital Defense Control Plane")

book = st.sidebar.selectbox("Operating book (Top 12 Sectors)", list(DATA_MATRIX.keys()), key="book_select")
book_data = DATA_MATRIX[book]

if 'active_phase' not in st.session_state:
    st.session_state['active_phase'] = {}
if 'phase_2_authorized' not in st.session_state:
    st.session_state['phase_2_authorized'] = {}
st.session_state['active_phase'].setdefault(book, 1)
st.session_state['phase_2_authorized'].setdefault(book, False)
active_phase, phase_2 = get_phase_context(book)

# Mathematical Algorithmic Override: fiduciary-ratio / hesitation-lag safe-harbor trigger
critical_lead = book_data.get('critical_lead')
is_critical = critical_lead is not None
weekly_burn = book_data['base_burn']
terminal_loss = (weekly_burn / 7.0) * 90
fiduciary_ratio = terminal_loss / (weekly_burn * 0.10)

if not st.session_state['cleared_books'].get(book, False) and not st.session_state['detection_time'].get(book):
    st.session_state['detection_time'][book] = datetime.now(timezone.utc)
detection_time = st.session_state['detection_time'].get(book, datetime.now(timezone.utc))
hesitation_seconds = max((datetime.now(timezone.utc) - detection_time).total_seconds(), 0)

sla_seconds_map = {"COO": 86400, "AFIC": 86400, "CLO": 259200, "CTO": 14400}
sla_seconds = sla_seconds_map.get(critical_lead, 86400)
cost_drift_dollars = parse_cost_drift_dollars(book_data['drift_metrics']['cost_drift'])

st.session_state['auto_override_triggered'] = False
if not st.session_state['cleared_books'].get(book, False) and (hesitation_seconds > sla_seconds or (is_critical and fiduciary_ratio > 10.0)):
    st.session_state['auto_override_triggered'] = True
    st.session_state['master_surge_cap'] = min(50, int(cost_drift_dollars / 5000))

sync_c1, sync_c2 = st.sidebar.columns(2)
sync_c1.button("🔄 Sync State", on_click=trigger_sync)
sync_c2.button("⚠️ Reset Book", on_click=reset_book, args=(book,))
st.sidebar.caption(f"Last Audited Sync: `{st.session_state['last_sync']}`")

st.sidebar.markdown("---")

view = st.sidebar.radio("Command view", [
    "1️⃣ Tier 1 | Chairman Directorate",
    "2️⃣ Tier 2 | General Management",
    "3️⃣ Tier 3 | Site Operations",
    "4️⃣ Forensic Audit Ledger"
], key="active_view")

st.sidebar.markdown("---")

# Chairman Directorate Override is available only for active Stage 1 execution.
override = st.session_state['override_active'] or st.session_state.get('safe_harbor_active', False)
master_surge = st.session_state['master_surge']

stage_key = f"inspected_stage_{book}"
is_stage_1_execution = "Tier 1" in view and st.session_state.get(stage_key, active_phase) == 1

if is_stage_1_execution:
    override_val = st.session_state.get('override_active', False) or st.session_state.get('safe_harbor_active', False)
    override = st.sidebar.toggle("Chairman Directorate Override", value=override_val, key="manual_override_toggle")
    st.session_state['override_active'] = override

    if st.session_state['auto_override_triggered'] and override:
        st.sidebar.markdown(f'''
        <span class="badge badge-safe-harbor">🛡️ ALGORITHMIC SAFE-HARBOR OVERRIDE (Fiduciary Ratio: {fiduciary_ratio:.1f}x | Auto-Authorized)</span>
        ''', unsafe_allow_html=True)

    if override:
        master_surge = st.sidebar.slider("Master Surge Cap Override (%)", 0, 100, st.session_state['master_surge'], step=5)
        st.session_state['master_surge'] = master_surge

if is_stage_1_execution and override and not st.session_state['override_logged'].get(book, False):
    append_forensic_entry(book, "Chairman Directorate Override", datetime.now(timezone.utc))
    st.session_state['override_logged'][book] = True
elif is_stage_1_execution and not override:
    st.session_state['override_logged'][book] = False

quorum_count = sum([st.session_state.get(f"comm_{book}_{c}", False) for c in ['ops', 'afic', 'risk', 'tech']])
is_quorum = (quorum_count == 4) or override
if is_stage_1_execution:
    st.session_state['board_quorum'][book] = is_quorum

# Operating Pipeline Sequence Widget
is_cleared = st.session_state['cleared_books'].get(book, False)
is_directed = st.session_state['directive_issued'].get(book, False)
frontline_check_prefix = f"chk2_{book}" if active_phase == 2 else f"chk_{book}"
frontline_checklist = phase_2["checks"] if active_phase == 2 else book_data["checklist"]
frontline_check_count = len(frontline_checklist)
frontline_checks_complete = all(
    st.session_state.get(f"{frontline_check_prefix}_{index}", False)
    for index in range(frontline_check_count)
)
gm_dispatch_complete = (
    st.session_state['pipeline_step_2'] == "DISPATCHED"
    or st.session_state['surgical_spend_authorized'].get(book, False)
)
agent_attestation_ready = gm_dispatch_complete and frontline_checks_complete

pipeline_step1_sub = f"Sub-Committee Gate ({book_data.get('critical_lead') or 'Full Board'} Oversight)"
pipeline_step2_sub = book_data.get("gm_action_title", "Dispatch Engineering Directive")
pipeline_step3_sub = book_data.get("site_action_title", "8-Point SOP Checklist Verification")
pipeline_step4_sub = f"Preserve ${book_data.get('preservation_amt', '549k')} Balance Sheet"
pipeline_statuses = (
    {
        1: st.session_state['pipeline_step_1'],
        2: st.session_state['pipeline_step_2'],
        3: st.session_state['pipeline_step_3'],
        4: st.session_state['pipeline_step_4'],
    }
    if active_phase == 2
    else {
        1: 'AUTHORIZED' if is_quorum else 'PENDING',
        2: 'DISPATCHED' if is_directed else 'PENDING',
        3: 'VERIFIED' if is_cleared else 'IN PROGRESS',
        4: 'COMMITTED' if is_cleared else 'PENDING',
    }
)

if "Tier 3" not in view:
    st.sidebar.markdown(f'''
    <div class="pipeline-card">
    <strong style="color: var(--teal); font-size: 0.85rem;">OPERATING PIPELINE SEQUENCE</strong><br><br>
    <div style="margin-bottom:8px;">
        <div style="display:flex; justify-content:space-between;">
            <span>1. Apex Board</span> <span class="badge {'badge-success' if pipeline_statuses[1] == 'AUTHORIZED' else 'badge-pending'}">{pipeline_statuses[1]}</span>
        </div>
        <small style="color: var(--text-muted);">{pipeline_step1_sub}</small>
    </div>
    <div style="margin-bottom:8px;">
        <div style="display:flex; justify-content:space-between;">
            <span>2. GM Directive</span> <span class="badge {'badge-success' if pipeline_statuses[2] == 'DISPATCHED' else 'badge-pending'}">{pipeline_statuses[2]}</span>
        </div>
        <small style="color: var(--text-muted);">{pipeline_step2_sub}</small>
    </div>
    <div style="margin-bottom:8px;">
        <div style="display:flex; justify-content:space-between;">
            <span>3. Site Operations</span> <span class="badge {'badge-success' if pipeline_statuses[3] == 'VERIFIED' else 'badge-pending'}">{pipeline_statuses[3]}</span>
        </div>
        <small style="color: var(--text-muted);">{pipeline_step3_sub}</small>
    </div>
    <div>
        <div style="display:flex; justify-content:space-between;">
            <span>4. Audit Settlement</span> <span class="badge {'badge-success' if pipeline_statuses[4] == 'COMMITTED' else 'badge-pending'}">{pipeline_statuses[4]}</span>
        </div>
        <small style="color: var(--text-muted);">{pipeline_step4_sub}</small>
    </div>
    </div>
    ''', unsafe_allow_html=True)

# Financial Computations
base_burn = book_data["base_burn"]
active_surge = master_surge if override else (book_data["recommended_surge"] if is_quorum else 0)

if active_phase == 2:
    burn_display = f"${book_data.get('phase2_burn', '183k')} / wk"
    burn_sub = "Active Carry Defense"
    client_realization = f"${base_burn * 0.9:,.0f}"
    phoenix_fee = f"${base_burn * 0.1:,.0f}"
    sop_badge = "0 / 8"
elif is_cleared:
    burn_display = "$0 / wk"
    burn_sub = "✅ Cleared & Resolved"
    client_realization = f"${base_burn * 0.9:,.0f}"
    phoenix_fee = f"${base_burn * 0.1:,.0f}"
    sop_badge = "8 / 8"
else:
    surge_dollars = base_burn * (active_surge / 100.0)
    net_burn = base_burn - surge_dollars
    burn_display = f"${net_burn:,.0f} / wk"
    burn_sub = f"⚠️ {active_surge}% Surge Active (${surge_dollars:,.0f})" if active_surge > 0 else "Active Carrying Drag"
    client_realization = f"${base_burn * 0.9:,.0f}"
    phoenix_fee = f"${base_burn * 0.1:,.0f}"
    completed_checks = sum([st.session_state.get(f"chk_{book}_{i}", False) for i in range(8)])
    sop_badge = f"{completed_checks} / 8"

if "Tier 3" not in view:
    # Top Metric Cards Bar
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Total Exposure", book_data["exposure"], "Board Limit")
    m2.metric("Holding Burn", burn_display, burn_sub)
    m3.metric("Client Realization", client_realization, "90% target" if not is_cleared else "Preserved")
    m4.metric("Phoenix Fee", phoenix_fee, "10% accrual" if not is_cleared else "Earned")
    m5.metric("SOP Readiness", sop_badge, "Field Gate")

# Regional Bottleneck Blueprint & Live Drift Radar
phase_context = phase_2 if active_phase == 2 else book_data
current_bottleneck = phase_context.get('bottleneck', book_data['bottleneck'])
current_regime = phase_context.get('regime', book_data['regime'])
current_regime_detail = phase_context.get('regime_detail', book_data['regime_detail'])
current_circuit_breaker = phase_context.get('circuit_breaker', book_data['circuit_breaker'])
phase_banner_title = "PHASE 2 SECONDARY BOTTLENECK & FORENSIC BLUEPRINT" if active_phase == 2 else "REGIONAL BOTTLENECK & FORENSIC BLUEPRINT"

# Interactive 3-Stage Bottleneck Inspector — exposes role-specific intelligence in Tier 1 and Tier 3.
if "Tier 1" in view or ("Tier 3" in view and is_directed):
    stage_key = f"inspected_stage_{book}"
    st.session_state.setdefault(stage_key, active_phase)

    def set_inspected_stage(stage_num):
        st.session_state[stage_key] = stage_num

    stage3_title = "Part 2 COD Attestation" if book == "ERCOT BESS / storage operations" else f"{book_data['artifacts'][-1][0]} Commercial Release"
    stage_pills = (
        {
            1: ("Stage 1: ✅ PSCAD/DNP3 Telemetry (CLEARED & AUDITED)", "Phase 1 technical gate settled"),
            2: ("Stage 2: 🚨 ACTIVE BLOCKER (100-Hr Thermal Run & Balancing)", phase_2['bottleneck']),
            3: ("Stage 3: 🔒 Commercial Gate (Part 2 COD Attestation)", stage3_title),
        }
        if book == "ERCOT BESS / storage operations" and active_phase == 2
        else {
            1: ("Stage 1: Active Blocker", book_data['bottleneck']),
            2: ("Stage 2: Secondary Queue", phase_2['bottleneck']),
            3: ("Stage 3: Commercial Gate", stage3_title),
        }
    )
    st.subheader("🔍 Interactive 3-Stage Bottleneck Inspector")
    p1, p2, p3 = st.columns(3)
    for col, stage_num in zip((p1, p2, p3), (1, 2, 3)):
        title, subtitle = stage_pills[stage_num]
        is_selected = st.session_state[stage_key] == stage_num
        col.button(
            f"{'🔴 ' if is_selected else ''}{title}\n{subtitle}",
            key=f"stage_pill_{book}_{stage_num}",
            on_click=set_inspected_stage,
            args=(stage_num,),
            type="primary" if is_selected else "secondary",
            use_container_width=True
        )

    inspected_stage = st.session_state[stage_key]
    if inspected_stage == 1:
        current_bottleneck = book_data['bottleneck']
        current_regime = book_data['regime']
        current_regime_detail = book_data['regime_detail']
        current_circuit_breaker = book_data['circuit_breaker']
        phase_banner_title = "STAGE 1 · ACTIVE BLOCKER FORENSIC BLUEPRINT"
    elif inspected_stage == 2:
        current_bottleneck = phase_2['bottleneck']
        current_regime = phase_2['regime']
        current_regime_detail = phase_2['regime_detail']
        current_circuit_breaker = phase_2['recommended_resolution']
        phase_banner_title = "STAGE 2 · SECONDARY QUEUE FORENSIC BLUEPRINT"
    else:
        current_bottleneck = f"Terminal COD & Offtake Gate — {stage3_title} Pending Final Settlement"
        current_regime = "TERMINAL SETTLEMENT GATE"
        current_regime_detail = "Commercial operations date and offtake agreement release require both Phase 1 and Phase 2 verification packets fully executed and Board-ratified before funds are released."
        current_circuit_breaker = "LOCKED: Submit the final Tier 3 Phase 2 SOP checklist and Board audit sign-off to trigger terminal settlement release."
        phase_banner_title = "STAGE 3 · COMMERCIAL GATE FORENSIC BLUEPRINT"

    if "Tier 1" in view:
        stage_intelligence = {
            1: {
                "risk": f"{book_data['bottleneck']}. {book_data['regime_detail']}",
                "loss": base_burn,
                "oversight": book_data['agents']['CLO']['memo'],
                "action": f"{book_data['circuit_breaker']} Pre-draft the governing waiver and queue the targeted capital authorization only after the technical gate is validated.",
            },
            2: {
                "risk": f"{phase_2['bottleneck']}. {phase_2['regime_detail']}",
                "loss": base_burn,
                "oversight": f"DGCL duty-of-care exposure rises if the Board does not document review of the Phase 2 {phase_2['target_director']} remediation path.",
                "action": f"Pre-clear a conditional {phase_2['target_director']} capital approval and preserve the Board record for the secondary gate cure.",
            },
            3: {
                "risk": f"Terminal settlement remains blocked until the final {stage3_title} packet is complete and ratified.",
                "loss": base_burn,
                "oversight": "DGCL fiduciary exposure arises from releasing commercial proceeds before documented completion of the required control packets.",
                "action": "Pre-draft conditional release resolutions and retain settlement authority pending verified Phase 1 and Phase 2 artifacts.",
            },
        }[inspected_stage]
        st.markdown(f'''
        <div class="agent-card">
            <span class="badge badge-agent">🤖 CHAIRMAN'S FIDUCIARY AGENT BRIEFING | STAGE {inspected_stage}</span><br><br>
            <strong>Stage Risk &amp; Technical Root Cause:</strong> {stage_intelligence['risk']}<br><br>
            <strong>Projected Holding Loss ($/wk):</strong> ${stage_intelligence['loss']:,.0f} if this stage stalls upon activation.<br><br>
            <strong>Statutory Oversight Vulnerability (DGCL / Fiduciary exposure):</strong> {stage_intelligence['oversight']}<br><br>
            <strong>Recommended Pre-emptive Board Action:</strong> {stage_intelligence['action']}
        </div>
        ''', unsafe_allow_html=True)
    else:
        stage_checks = book_data['checks'] if inspected_stage == 1 else phase_2['checks'] if inspected_stage == 2 else [artifact[0] for artifact in book_data['artifacts']]
        stage_artifacts = book_data['artifacts'] if inspected_stage != 2 else [(check, "Required Phase 2 verification") for check in phase_2['checks']]
        telemetry_threshold = book_data['drift_metrics']['telemetry_drift'] if inspected_stage == 1 else "Phase 2 verification packet complete" if inspected_stage == 2 else "All control artifacts verified before terminal release"
        safety_interlock = book_data['agents']['CTO']['memo'] if inspected_stage == 1 else phase_2['recommended_resolution'] if inspected_stage == 2 else f"Maintain terminal release lock until {stage3_title} verification is complete."
        st.markdown(f'''
        <div class="agent-card" style="border-color: var(--teal);">
            <span class="badge badge-active">🛠️ ENGINEERING FIELD COPILOT | STAGE {inspected_stage}</span><br><br>
            <strong>Raw Telemetry Threshold:</strong> {telemetry_threshold}<br><br>
            <strong>Required Tooling:</strong> {', '.join(artifact[0] for artifact in stage_artifacts[:4])}<br><br>
            <strong>Physical Safety Interlocks:</strong> {safety_interlock}<br><br>
            <strong>Frontline Verification Checklist:</strong> {'; '.join(stage_checks)}
        </div>
        ''', unsafe_allow_html=True)

if "Tier 3" not in view:
    st.markdown(f'''
    <div class="blueprint-card">
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
        <span style="font-size:0.8rem; font-family:monospace; color:#ff7b72; font-weight:bold; letter-spacing:1px;">{phase_banner_title}</span>
        <span class="badge {'badge-danger' if 'DEPENDENCY' in current_regime or 'QUEUE' in current_regime else 'badge-active'}">REGIME: {current_regime}</span>
    </div>
    <div style="display: grid; grid-template-columns: 1fr 1.3fr 1.3fr; gap: 14px;">
        <div>
            <span class="badge badge-active">ACTIVE NODE</span><br>
            <strong>{book_data['region']}</strong><br><br>
            <small style="color:var(--text-muted);">
                SLA Drift: <strong>{book_data['drift_metrics']['sla_drift']}</strong><br>
                Telemetry: <strong>{book_data['drift_metrics']['telemetry_drift']}</strong><br>
                Cost Drift: <strong>{book_data['drift_metrics']['cost_drift']}</strong>
            </small>
        </div>
        <div>
            <strong style="color: #ff7b72;">{current_bottleneck}</strong><br>
            <small>{current_regime_detail}</small>
        </div>
        <div>
            <span class="badge badge-agent">CAPITAL DEFENSE CIRCUIT BREAKER</span><br>
            <small><em>{current_circuit_breaker}</em></small>
        </div>
    </div>
    </div>
    ''', unsafe_allow_html=True)

# ----------------- TIER 1: CHAIRMAN DIRECTORATE -----------------
if "Tier 1" in view:
    st.header("Apex Board Governance & Oversight")
    st.write(f"Domain statutory envelopes, agent forensic research memos, and quorum gating for {book}.")

    if st.session_state['auto_override_triggered']:
        safe_harbor_engaged = st.session_state.get('override_active', False) or st.session_state.get('safe_harbor_active', False)
        if safe_harbor_engaged:
            st.markdown(f'''
            <span class="badge badge-safe-harbor">🛡️ ALGORITHMIC SAFE-HARBOR OVERRIDE (Fiduciary Ratio: {fiduciary_ratio:.1f}x | Auto-Authorized)</span>
            ''', unsafe_allow_html=True)
        else:
            st.markdown(f'''
            <div class="radar-card">
                <strong>🚨 STATUTORY EMERGENCY MITIGATION PROPOSED:</strong> Fiduciary Ratio: {fiduciary_ratio:.1f}x | Algorithmic Surge Cap: {st.session_state['master_surge_cap']}% | Click below to execute Chairman Binding Authorization under Statutory Safe-Harbor Rule.
            </div>
            ''', unsafe_allow_html=True)

            def activate_safe_harbor():
                cap = min(50, int(cost_drift_dollars / 5000)) if 'cost_drift_dollars' in globals() else 30
                st.session_state['safe_harbor_active'] = True
                st.session_state['override_active'] = True
                st.session_state['master_surge_cap'] = cap
                st.session_state['master_surge'] = max(st.session_state['master_surge'], cap)
                append_forensic_entry(book, "CHAIRMAN_STATUTORY_SAFEHARBOR", datetime.now(timezone.utc))
                st.session_state['override_logged'][book] = True

            st.button(
                "⚡ Confirm Chairman Binding Safe-Harbor Directive",
                on_click=activate_safe_harbor,
                key="btn_confirm_safe_harbor",
                type="primary"
            )

    if active_phase == 2:
        target_director = phase_2['target_director']
        failure_mode = phase_2['failure_mode']
        recommended_resolution = phase_2['recommended_resolution']
        st.markdown(f'''
        <div class="agent-card" style="border: 1px solid var(--amber); background: rgba(210,153,34,0.08);">
            <span class="badge badge-agent">📩 DIRECT AGENT NOTIFICATION | TO: {target_director} CHAIR</span><br>
            <strong>Failure mode:</strong> {failure_mode}<br>
            <strong>Resolution:</strong> {recommended_resolution}
            <div style="margin-top: 10px;">
                <button type="button" style="background: var(--amber); color: #111; border: none; border-radius: 6px; padding: 10px 14px; font-weight: 700; cursor: pointer;">⚡ Authorize Domain Fix</button>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        if st.button("⚡ Authorize Domain Fix", type="primary"):
            st.session_state['phase_2_authorized'][book] = True
            st.toast(f"Phase 2 directive authorized for {book} and routed to {target_director}.", icon="✅")
    
    if st.session_state['board_escalation'].get(book, False):
        st.error("🚨 **CRITICAL FRONTLINE ESCALATION:** Site team has encountered a blocking constraint requiring Board intervention.")
        c_lsp, c_rbtn = st.columns([1.5, 1])
        with c_rbtn:
            if st.button("⚡ Clear Escalation & Dispatch Emergency Mandate", type="primary"):
                st.session_state['board_escalation'][book] = False
                st.session_state['board_quorum'][book] = True
                st.rerun()
    
    # Actuarial Terminal Endpoint Forecaster
    st.subheader("Actuarial Terminal Endpoint Forecast (Monte Carlo Inaction Loss)")
    days = [30, 60, 90]
    unmitigated_loss = [(base_burn / 7.0) * d for d in days]
    mitigated_preservation = [u * 0.90 for u in unmitigated_loss]
    
    f1, f2, f3 = st.columns(3)
    f1.markdown(f'''
    <div class="forecast-card">
        <span class="badge badge-danger">30-DAY INACTION IMPAIRMENT</span><br>
        <h3 style="color:#ff7b72; margin:6px 0;">${unmitigated_loss[0]:,.0f}</h3>
        <small>Preserved via Targeted Cure: <strong>${mitigated_preservation[0]:,.0f}</strong></small>
    </div>
    ''', unsafe_allow_html=True)
    f2.markdown(f'''
    <div class="forecast-card">
        <span class="badge badge-danger">60-DAY INACTION IMPAIRMENT</span><br>
        <h3 style="color:#ff7b72; margin:6px 0;">${unmitigated_loss[1]:,.0f}</h3>
        <small>Preserved via Targeted Cure: <strong>${mitigated_preservation[1]:,.0f}</strong></small>
    </div>
    ''', unsafe_allow_html=True)
    terminal_critical = unmitigated_loss[2] >= 1_500_000
    f3_card_class = "critical-forecast-card" if terminal_critical else "forecast-card"
    f3_banner = "🚨 TERMINAL DEFAULT IMMINENT" if terminal_critical else "90-DAY TERMINAL RISK"
    f3.markdown(f'''
    <div class="{f3_card_class}">
        <span class="badge badge-danger">{f3_banner}</span><br>
        <h3 style="color:#ff7b72; margin:6px 0;">${unmitigated_loss[2]:,.0f}</h3>
        <small>PPA/Offtake Forfeiture Risk: <strong>CRITICAL</strong></small>
    </div>
    ''', unsafe_allow_html=True)

    critical_lead = book_data.get('critical_lead')
    agent_map = {
        "COO": ("COO AGENT | ASSET DELIVERY", "Operations & Asset Delivery Committee (Chair: COO Oversight)", book_data['agents']['COO']),
        "AFIC": ("CFO AGENT | AFIC CAPITAL DEFENSE", "Audit, Finance & Investment Committee / AFIC (Chair: CFO Oversight)", book_data['agents']['AFIC']),
        "CLO": ("CLO AGENT | RISK & REGULATORY", "Risk, Regulatory & Legal Committee (Chair: CLO Oversight)", book_data['agents']['CLO']),
        "CTO": ("CTO AGENT | SYSTEMS & TELEMETRY", "Technology & Infrastructure Committee (Chair: CTO Oversight)", book_data['agents']['CTO']),
    }

    st.subheader("Frontline Verification Hold Radar")
    critical_idx = book_data.get("critical_check_idx")
    if critical_idx is not None:
        item_number = critical_idx + 1
        item_text = book_data["checklist"][critical_idx]
        critical_check_label = f"Frontline SOP Check #{item_number}: [{item_text}]"
        item_cleared = st.session_state.get(f"chk_{book}_{critical_idx}", False)
        if item_cleared:
            st.markdown(f'''
            <div class="radar-card-cleared">
                <span class="badge badge-success">✅ FRONTLINE ARTIFACT CLEARED</span><br>
                <small>{critical_check_label} verified and cleared at Site Operations.</small>
            </div>
            ''', unsafe_allow_html=True)
        else:
            blocker_diagnostic = book_data["blocker_diagnostic"]
            docket_transmitted = st.session_state.get("escalation_transmitted", False) and st.session_state['board_escalation'].get(book, False)
            st.markdown(f'''
            <div class="radar-card">
                <span class="badge badge-danger">🚨 HOLDING GATE</span><br>
                <strong>HOLDING GATE: {critical_check_label} is unverified.</strong><br>
                <small>This is the exact physical artifact currently holding up the critical path in Tier 3 Site Operations.</small>
                {f'<br><br><span class="badge badge-agent">FORENSIC BLOCKER DOCKET TRANSMITTED</span><br><strong>Technical Root Cause:</strong> {blocker_diagnostic["technical_root_cause"]}<br><strong>Missing Artifact:</strong> {blocker_diagnostic["missing_artifact_name"]}<br><strong>Standby Field Impact:</strong> {blocker_diagnostic["standby_impact"]}<br><strong>GM Remediation Required:</strong> {blocker_diagnostic["gm_remediation_request"]}' if docket_transmitted else ''}
            </div>
            ''', unsafe_allow_html=True)
    else:
        st.info("No critical frontline checklist item mapped for this operating book.")

    if is_stage_1_execution:
        st.subheader("Sub-Committee Governance Matrix")
        committee_rows = [
            ("COO", "ops", 0),
            ("AFIC", "afic", 2),
            ("CLO", "risk", 4),
            ("CTO", "tech", 6),
        ]
        for role, state_key, artifact_index in committee_rows:
            title, committee_label, agent_info = agent_map[role]
            checkbox_key = f"comm_{book}_{state_key}"
            approved = st.session_state.get(checkbox_key, False)
            is_required = not approved or critical_lead == role
            card_class = "critical-agent-card" if is_required else "agent-card"
            signoff_label = (
                f"{committee_label} — ✅ READY FOR STATUTORY SIGN-OFF"
                if critical_lead == role and agent_attestation_ready
                else f"Statutory Sign-off: {committee_label}"
            )
            hold_reason = "Critical-path authorization remains outstanding." if critical_lead == role else "Committee review remains outstanding before the operating directive can proceed."
            chairman_action = book_data['circuit_breaker'] if critical_lead == role else "Confirm the committee record, preserve the decision basis, and maintain the targeted surge authorization in reserve."
            frontline_artifact = book_data['checklist'][artifact_index]
            with st.expander(f"{'🚨 ' if is_required else '✅ '}{committee_label}", expanded=is_required):
                st.markdown(f'''
                <div class="{card_class}">
                    <span class="badge {'badge-danger' if is_required else 'badge-success'}">{'🚨 REQUIRED CRITICAL PATH SIGN-OFF' if is_required else 'SIGN-OFF RECORDED'}</span>
                    <strong>{title}</strong><br><br>
                    <strong>🤖 Agent Telemetry Diagnosis:</strong> {agent_info['memo']}<br><br>
                    <strong>📋 GM Supervisory Brief:</strong> {agent_info['status']}. Field standby carry is ${base_burn:,.0f}/wk; {hold_reason}<br><br>
                    <strong>🛠️ Frontline Dependency:</strong> Tier 3 must verify “{frontline_artifact}” to clear this hold.<br><br>
                    <strong>⚖️ Fiduciary Recommendation:</strong> {chairman_action}
                </div>
                ''', unsafe_allow_html=True)
                if critical_lead == role:
                    if agent_attestation_ready:
                        st.markdown(f'''
                        <div class="radar-card-cleared" style="box-shadow: 0 0 20px rgba(63,185,80,0.65);">
                            <span class="badge badge-success">✅ AGENT ATTESTATION</span><br><br>
                            <strong>GM Surgical Work Order verified on site. Frontline telemetry artifact confirmed. {committee_label} Chair is fully authorized to execute statutory sign-off.</strong>
                        </div>
                        ''', unsafe_allow_html=True)
                    else:
                        st.markdown('''
                        <div class="card" style="border: 2px solid var(--amber); background: rgba(255, 77, 79, 0.08);">
                            <span class="badge badge-danger">⚠️ AGENT ADVISORY</span><br><br>
                            <strong>Sign-off held pending GM Reverse-Engineered Dispatch ($35,000 Surgical Cure) and Frontline SOP Verification.</strong>
                        </div>
                        ''', unsafe_allow_html=True)
                if role == "CTO":
                    surgical_budget = book_data["surgical_budget"]
                    st.markdown(
                        f"**Targeted Cure: ${surgical_budget['total_surgical_cost']:,.0f} Surgical Spend "
                        "(Inverter Rig & OEM Lead) clears $610,000/wk holding burn.**"
                    )
                    st.markdown(
                        f"**🎯 Direct Frontline Responsibility: {critical_check_label}**  \n"
                        "**Status: Unverified on site. Dispatched GM Synthetic Injection Rig required to clear.**"
                    )
                st.checkbox(signoff_label, value=approved, key=checkbox_key)
        
        st.divider()
        t1_sp, t1_btn = st.columns([1.5, 1])
        with t1_btn:
            if is_quorum:
                st.button("➡️ Advance to Tier 2 (General Management)", on_click=nav_to, args=("2️⃣ Tier 2 | General Management",), type="primary")
            else:
                st.warning(f"⚠️ Quorum Incomplete ({quorum_count}/4). Full committee quorum or Chairman Override required.")
    else:
        st.info("Stage 2 and Stage 3 are briefing-only Board reviews. Return to Stage 1 to change quorum or use the Chairman Override.")

# ----------------- TIER 2: GENERAL MANAGEMENT -----------------
elif "Tier 2" in view:
    st.header(f"📋 General Management Operational Command (Chair: {critical_lead} Oversight)")

    if active_phase == 2:
        target_director = phase_2['target_director']
        st.markdown(f'''
        <div class="card" style="border-left: 4px solid var(--amber);">
            <strong>ℹ️ GM ADVISORY:</strong> Sensing layer detected Phase 2 gate requirement. Staged pending {target_director} approval.
        </div>
        ''', unsafe_allow_html=True)
    
    if not is_quorum:
        st.error("🔒 **TIER 2 LOCKED:** Board Quorum has not been authorized in Tier 1. Return to Chairman Directorate to establish quorum.")
    else:
        directive = phase_2['recommended_resolution'] if active_phase == 2 else book_data['circuit_breaker']
        technical_instruction = phase_2['failure_mode'] if active_phase == 2 else book_data['agents']['CTO']['memo']
        vendor_sla_hours = max(1, int(sla_seconds / 3600))
        hourly_carry = base_burn / 168
        st.markdown(f'''
        <div class="card" style="border-left: 4px solid var(--teal);">
            <span class="badge badge-active">ACTIVE ENGINEERING DIRECTIVE</span><br><br>
            <strong>Work Order:</strong> {directive}<br>
            <strong>Technical Execution:</strong> {technical_instruction}<br>
            <strong>Frontline Release Target:</strong> Frontline SOP Check #{book_data['critical_check_idx'] + 1}: [{book_data['checklist'][book_data['critical_check_idx']]}]
        </div>
        ''', unsafe_allow_html=True)

        st.subheader("Vendor & Contractor Mobilization Status")
        v1, v2, v3 = st.columns(3)
        v1.markdown(f"<div class='card'><span class='badge badge-active'>FIELD CONTRACTOR POOL</span><br>Standby headcount: 12<br><small>Mobilized for {book_data['artifacts'][0][0]} execution.</small></div>", unsafe_allow_html=True)
        v2.markdown(f"<div class='card'><span class='badge badge-pending'>STANDBY CARRY</span><br>${hourly_carry:,.0f} / hour<br><small>Active contractor and test-equipment carry.</small></div>", unsafe_allow_html=True)
        v3.markdown(f"<div class='card'><span class='badge badge-active'>VENDOR SLA COUNTDOWN</span><br>{vendor_sla_hours} hours<br><small>Required response window for {critical_lead} escalation.</small></div>", unsafe_allow_html=True)
        
        st.divider()
        
        def dispatch_directive():
            st.session_state['directive_issued'][book] = True
            st.session_state['pipeline_step_2'] = "DISPATCHED"
            st.session_state['surgical_spend_authorized'][book] = True
            st.session_state['surgical_purchase_orders'][book] = [
                {
                    "po_number": f"PO-{book[:4].upper().replace(' ', '')}-{index + 1:02d}",
                    "vendor": line_item["vendor"],
                    "cost": line_item["cost"],
                }
                for index, line_item in enumerate(book_data["surgical_budget"]["surgical_line_items"])
            ]
            st.session_state['active_view'] = '3️⃣ Tier 3 | Site Operations'
            
        surgical_budget = book_data["surgical_budget"]
        surgical_rows = "".join(
            f"<tr><td>{line_item['item']}</td><td>{line_item['vendor']}</td><td>${line_item['cost']:,.0f}</td></tr>"
            for line_item in surgical_budget["surgical_line_items"]
        )
        st.markdown(f'''
        <div class="card" style="border: 2px solid var(--teal); background: #0b0e14;">
            <span class="badge badge-active">🛠️ REVERSE-ENGINEERED SURGICAL SPEND ALLOCATION</span><br><br>
            <div style="background: rgba(210,153,34,0.12); border-left: 4px solid var(--amber); color: var(--text-muted); padding: 10px; margin-bottom: 12px;">
                {surgical_budget['blunt_spend_warning']}
            </div>
            <table style="width:100%; border-collapse:collapse; font-size:0.9rem;">
                <thead><tr style="color:var(--teal); text-align:left;"><th style="padding:6px; border-bottom:1px solid var(--line);">Item</th><th style="padding:6px; border-bottom:1px solid var(--line);">Vendor</th><th style="padding:6px; border-bottom:1px solid var(--line);">Cost</th></tr></thead>
                <tbody>{surgical_rows}</tbody>
            </table>
            <div style="display:flex; justify-content:space-between; gap:12px; margin-top:14px; font-family:monospace;">
                <strong style="color:var(--red);">Blunt Weekly Carry: $220k/wk</strong>
                <strong style="color:var(--green);">Total Surgical Cure: ${surgical_budget['total_surgical_cost']:,.0f}</strong>
            </div>
            <small style="color:var(--text-muted);">{surgical_budget['capital_efficiency_ratio']}</small>
        </div>
        ''', unsafe_allow_html=True)
        t2_sp, t2_btn = st.columns([1.5, 1])
        with t2_btn:
            st.button(
                f"⚡ Authorize Ring-Fenced Surgical Spend (${surgical_budget['total_surgical_cost']:,.0f}) & Dispatch Work Order",
                on_click=dispatch_directive,
                type="primary"
            )

# ----------------- TIER 3: SITE OPERATIONS -----------------
elif "Tier 3" in view:
    st.header(f"Site Operations Hub / {book}")
    if not is_directed:
        st.warning("🔒 Frontline readiness is locked pending a binding operational directive from Tier 2.")
    else:
        remediation_dispatched = (
            st.session_state['pipeline_step_2'] == "DISPATCHED"
            or st.session_state['surgical_spend_authorized'].get(book, False)
        )

        def auto_verify_checklist():
            for index in range(8):
                st.session_state[f"{key_prefix}_{index}"] = True

        st.subheader(f"Physical Test Criteria ({book})")
        art = book_data["artifacts"]
        a1, a2, a3, a4 = st.columns(4)
        a1.markdown(f"<div class='card'><strong>{art[0][0]}</strong><br><small>{art[0][1]}</small></div>", unsafe_allow_html=True)
        a2.markdown(f"<div class='card'><strong>{art[1][0]}</strong><br><small>{art[1][1]}</small></div>", unsafe_allow_html=True)
        a3.markdown(f"<div class='card'><strong>{art[2][0]}</strong><br><small>{art[2][1]}</small></div>", unsafe_allow_html=True)
        a4.markdown(f"<div class='card'><strong>{art[3][0]}</strong><br><small>{art[3][1]}</small></div>", unsafe_allow_html=True)

        st.subheader("Phase 2 Secondary Gate Verification Checklist" if active_phase == 2 else "Frontline SOP Release Checklist")
        if active_phase == 2:
            checks_raw = phase_2["checks"]
            key_prefix = f"chk2_{book}"
            critical_idx = phase_2.get("critical_check_idx")
        else:
            checks_raw = book_data["checklist"]
            key_prefix = f"chk_{book}"
            critical_idx = book_data.get("critical_check_idx")

        if remediation_dispatched:
            st.markdown('''
            <div class="radar-card-cleared">
                <span class="badge badge-success">✅ REMEDIATION DISPATCHED</span><br><br>
                <strong>Inverter OEM Specialist &amp; Synthetic DNP3 Rig active on site. Frontline verification unlocked.</strong>
            </div>
            ''', unsafe_allow_html=True)
            st.button(
                "⚡ Run Synthetic Telemetry Stream & Auto-Verify Checklist (8/8)",
                on_click=auto_verify_checklist,
                type="primary"
            )
        c_col1, c_col2 = st.columns(2)

        check_states = []
        for i, chk_text in enumerate(checks_raw):
            col_target = c_col1 if i % 2 == 0 else c_col2
            k = f"{key_prefix}_{i}"
            item_number = i + 1
            chk_label = f"Frontline SOP Check #{item_number}: [{chk_text}]"
            if i == critical_idx:
                chk_label = f"🔴 **{chk_label}** — *(🚨 CRITICAL PATH BLOCKER)*"
            v = col_target.checkbox(chk_label, value=st.session_state.get(k, False), key=k)
            check_states.append(v)

        completed_count = sum(check_states)
        st.divider()
    
    def signoff_and_settle():
        st.session_state['cleared_books'][book] = True
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        entry_hash = hashlib.sha256(f"{book}{timestamp}CLEARED".encode()).hexdigest()[:16]
        st.session_state['ledger'].append({
            "Timestamp": timestamp,
            "Operating Book": book,
            "Action": "Frontline SOP Sign-off & Interconnection Cleared",
            "Capital Recovered": f"${base_burn:,.0f} / wk",
            "Client Preserved (90%)": f"${base_burn*0.9:,.0f}",
            "Phoenix Fee (10%)": f"${base_burn*0.1:,.0f}",
            "Cryptographic Hash": entry_hash
        })
        append_forensic_entry(book, "Tier 3 SOP Sign-off", datetime.now(timezone.utc))
        st.session_state['active_phase'][book] = 2
        st.session_state['sop_checklist'] = [False] * 8
        st.session_state['pipeline_step_1'] = "PENDING"
        st.session_state['pipeline_step_2'] = "QUEUED"
        st.session_state['pipeline_step_3'] = "PENDING"
        st.session_state['pipeline_step_4'] = "PENDING"
        st.session_state['chairman_override_active'] = False
        st.session_state['override_active'] = False
        st.session_state['safe_harbor_active'] = False
        st.session_state['quorum_votes'] = [False, False, False, False]
        st.session_state['board_quorum'][book] = False
        st.session_state[f"inspected_stage_{book}"] = 2
        for i in range(8):
            st.session_state[f"chk2_{book}_{i}"] = False
        for committee in ['ops', 'afic', 'risk', 'tech']:
            st.session_state[f"comm_{book}_{committee}"] = False
        st.session_state['phase_2_authorized'][book] = False
        st.session_state['active_view'] = '4️⃣ Forensic Audit Ledger'

    def transmit_forensic_blocker_docket():
        st.session_state['escalation_transmitted'] = True
        st.session_state['board_escalation'][book] = True
        append_forensic_entry(book, "Tier 3 Forensic Blocker Docket Transmitted to Tier 2 GM and Tier 1 Chairman", datetime.now(timezone.utc))
        st.session_state['active_view'] = '1️⃣ Tier 1 | Chairman Directorate'

    if is_directed:
        if completed_count == 8:
            t3_sp, t3_act = st.columns([1.5, 1])
            with t3_act:
                st.button("⚡ Submit Frontline SOP Sign-off & Settle", on_click=signoff_and_settle, type="primary")
        else:
            st.info(f"{completed_count}/8 checks complete. All 8 verification checks required for physical sign-off.")
            critical_item_unchecked = critical_idx is not None and not st.session_state.get(f"{key_prefix}_{critical_idx}", False)
            if critical_item_unchecked and not remediation_dispatched:
                blocker_diagnostic = book_data["blocker_diagnostic"]
                st.markdown(f'''
                <div class="radar-card">
                    <span class="badge badge-danger">🚨 FRONTLINE BOTTLENECK FORENSIC DIAGNOSIS</span><br><br>
                    <strong>Technical Root Cause:</strong> {blocker_diagnostic["technical_root_cause"]}<br><br>
                    <strong>Missing Artifact:</strong> {blocker_diagnostic["missing_artifact_name"]}<br><br>
                    <strong>Standby Field Impact:</strong> {blocker_diagnostic["standby_impact"]}<br><br>
                    <strong>GM Remediation Required:</strong> {blocker_diagnostic["gm_remediation_request"]}
                </div>
                ''', unsafe_allow_html=True)
                esc_sp, esc_btn = st.columns([1.5, 1])
                with esc_btn:
                    st.button("⚡ Transmit Forensic Blocker Docket to Tier 2 (GM) & Tier 1 (Chairman)", on_click=transmit_forensic_blocker_docket, type="primary")
            elif critical_item_unchecked:
                st.info("Remediation is active on site. Verify the remaining frontline checklist items or run the synthetic telemetry stream.")
            else:
                st.info("The critical-path item is verified. Complete the remaining checklist items to submit frontline sign-off.")

# ----------------- TIER 4: FORENSIC AUDIT LEDGER -----------------
elif "Ledger" in view:
    st.header("Immutable Governance & Forensic Audit Ledger")
    st.write("Cryptographically verifiable chain of custody across all 12 operating books.")

    st.markdown(f'''
    <div class="card" style="border: 2px solid var(--red); background: rgba(255,123,114,0.08);">
        🔒 <strong>CONFIDENTIAL FIDUCIARY WORK PRODUCT</strong> — PROTECTED BY STATUTORY RISK MANAGEMENT PRIVILEGE (DO NOT DISCLOSE WITHOUT GENERAL COUNSEL AUTHORIZATION).
    </div>
    ''', unsafe_allow_html=True)

    st.subheader("Session Forensic Ledger")
    ledger_rows = [
        row for row in st.session_state['ledger']
        if str(row.get("Book") or row.get("Operating Book") or "").strip() not in ("", "None")
    ]
    if ledger_rows:
        st.dataframe(ledger_rows, use_container_width=True)
    else:
        st.info("No frontline sign-offs recorded in this session. Complete Tier 3 SOP verification to generate an entry.")

    st.subheader("Persistent Audit Ledger (SQLite — Survives Server Reboots)")
    audit_rows = [
        row for row in fetch_audit_events()
        if str(row.get("book") or "").strip() not in ("", "None")
    ]
    if audit_rows:
        st.dataframe(audit_rows, use_container_width=True)
    else:
        st.info("No persisted audit events recorded yet in audit_ledger.db.")

st.caption(f"Factory Command Post | Autonomous Capital Defense Control Plane | Audited Sync: {st.session_state['last_sync']}")

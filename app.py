import hashlib
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

for book_name, book_data in DATA_MATRIX.items():
    book_data.setdefault("critical_lead", None)
    book_data.setdefault("critical_check_idx", None)
    book_data.setdefault("phase_2", {
        "bottleneck": "Phase 2: Secondary Recovery Queue Awaiting Director Approval",
        "target_director": "CTO",
        "focus": "Systems Revalidation",
        "failure_mode": "Secondary queue gate remains unresolved after Phase 1 release.",
        "recommended_resolution": "Stage the follow-on technical remediation and route the issue to the designated executive director for approval.",
        "regime": "SECONDARY QUEUE HOLD",
        "regime_detail": "Sensing layer detected a phase-two process gate beyond initial commissioning. The site team has cleared the first wave but a second dependency remains in the queue.",
    })

DATA_MATRIX["ERCOT BESS / storage operations"]["critical_lead"] = "CTO"
DATA_MATRIX["ERCOT BESS / storage operations"]["phase_2"] = {
    "bottleneck": "Phase 2: 100-Hour Continuous C-Rate Thermal Run & Cell Balancing",
    "target_director": "CTO",
    "focus": "Thermal Firmware Patch",
    "failure_mode": "Thermal drift continues after Phase 1 release, leaving the battery in a continuous C-rate balancing loop.",
    "recommended_resolution": "Deploy the thermal firmware patch and re-run continuous balancing under the 100-hour validation window.",
    "regime": "SECONDARY QUEUE HOLD",
    "regime_detail": "Phase 1 telemetry locks are cleared, but cell balancing still fails under sustained C-rate stress and must be corrected before final release.",
}
DATA_MATRIX["Grid Infrastructure / PJM Cluster"]["critical_lead"] = "COO"
DATA_MATRIX["Grid Infrastructure / PJM Cluster"]["phase_2"] = {
    "bottleneck": "Phase 2: Substation Interlock Logic & Relay Trip Calibration",
    "target_director": "COO",
    "focus": "Protection Crew Mobilization",
    "failure_mode": "Relay trip calibration remains misaligned after the initial energization gate and is creating a protection logic hold.",
    "recommended_resolution": "Mobilize the protection crew and complete interlock logic calibration before re-entering the dispatch sequence.",
    "regime": "SECONDARY QUEUE HOLD",
    "regime_detail": "The transmission study is resolved, but the live relay logic remains out of calibration and can short-circuit the next commissioning stage.",
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
}
DATA_MATRIX["Critical Minerals / Lithium Refining Facility"]["critical_lead"] = "COO"
DATA_MATRIX["Defense Manufacturing / Naval Shipyard"]["critical_lead"] = "COO"
DATA_MATRIX["Commercial Aviation / Fleet AOG Turnaround"]["critical_lead"] = "CTO"

# Defensive Session State Initialization
for key, default in [
    ('ledger', []), ('cleared_books', {}), ('directive_issued', {}),
    ('board_escalation', {}), ('board_quorum', {}), ('active_phase', {}), ('phase_2_authorized', {}),
    ('detection_time', {}), ('override_logged', {}),
    ('active_view', '1️⃣ Tier 1 | Chairman Directorate'),
    ('last_sync', datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")),
    ('override_active', False), ('master_surge', 0)
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
    st.session_state['active_phase'][book_name] = 1
    st.session_state['phase_2_authorized'][book_name] = False
    st.session_state['detection_time'][book_name] = datetime.now(timezone.utc)
    st.session_state['override_logged'][book_name] = False
    st.session_state['active_view'] = '1️⃣ Tier 1 | Chairman Directorate'
    for i in range(8):
        st.session_state[f"chk_{book_name}_{i}"] = False
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
        'regime_detail': 'The site team has cleared Phase 1 but a second dependency remains pending executive approval.'
    })
    return active_phase, phase_2


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
    st.session_state['detection_time'][book_name] = datetime.now(timezone.utc)

# Sidebar Controls
st.sidebar.title("FACTORY COMMAND POST")
st.sidebar.caption("Autonomous Capital Defense Control Plane")

book = st.sidebar.selectbox("Operating book (Top 12 Sectors)", list(DATA_MATRIX.keys()))
book_data = DATA_MATRIX[book]

if 'active_phase' not in st.session_state:
    st.session_state['active_phase'] = {}
if 'phase_2_authorized' not in st.session_state:
    st.session_state['phase_2_authorized'] = {}
st.session_state['active_phase'].setdefault(book, 1)
st.session_state['phase_2_authorized'].setdefault(book, False)
active_phase, phase_2 = get_phase_context(book)

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

# Chairman Directorate Override
override = st.sidebar.toggle("Chairman Directorate Override", value=st.session_state['override_active'], key="override_toggle")
st.session_state['override_active'] = override

if override and not st.session_state['override_logged'].get(book, False):
    append_forensic_entry(book, "Chairman Directorate Override", datetime.now(timezone.utc))
    st.session_state['override_logged'][book] = True
elif not override:
    st.session_state['override_logged'][book] = False

master_surge = 0
if override:
    master_surge = st.sidebar.slider("Master Surge Cap Override (%)", 0, 100, st.session_state['master_surge'], step=5)
    st.session_state['master_surge'] = master_surge

quorum_count = sum([st.session_state.get(f"comm_{book}_{c}", False) for c in ['ops', 'afic', 'risk', 'tech']])
is_quorum = (quorum_count == 4) or override
if is_quorum:
    st.session_state['board_quorum'][book] = True
else:
    st.session_state['board_quorum'][book] = False

if not st.session_state['cleared_books'].get(book, False) and not st.session_state['detection_time'].get(book):
    st.session_state['detection_time'][book] = datetime.now(timezone.utc)

# Operating Pipeline Sequence Widget
is_cleared = st.session_state['cleared_books'].get(book, False)
is_directed = st.session_state['directive_issued'].get(book, False)

st.sidebar.markdown(f'''
<div class="pipeline-card">
    <strong style="color: var(--teal); font-size: 0.85rem;">OPERATING PIPELINE SEQUENCE</strong><br><br>
    <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
        <span>1. Apex Board</span> <span class="badge {'badge-success' if is_quorum else 'badge-pending'}">{'AUTHORIZED' if is_quorum else 'PENDING'}</span>
    </div>
    <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
        <span>2. GM Directive</span> <span class="badge {'badge-success' if is_directed else 'badge-pending'}">{'DISPATCHED' if is_directed else 'PENDING'}</span>
    </div>
    <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
        <span>3. Site Operations</span> <span class="badge {'badge-success' if is_cleared else 'badge-pending'}">{'VERIFIED' if is_cleared else 'IN PROGRESS'}</span>
    </div>
    <div style="display:flex; justify-content:space-between;">
        <span>4. Audit Settlement</span> <span class="badge {'badge-success' if is_cleared else 'badge-pending'}">{'COMMITTED' if is_cleared else 'PENDING'}</span>
    </div>
</div>
''', unsafe_allow_html=True)

# Financial Computations
base_burn = book_data["base_burn"]
active_surge = master_surge if override else (book_data["recommended_surge"] if is_quorum else 0)

if is_cleared:
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

    st.subheader("Autonomous Board Committee Research Dossiers")
    critical_lead = book_data.get('critical_lead')
    agent_map = {
        "COO": ("COO AGENT | ASSET DELIVERY", "Operations & Asset Delivery Committee (Chair: COO Oversight)", book_data['agents']['COO']),
        "AFIC": ("CFO AGENT | AFIC CAPITAL DEFENSE", "Audit, Finance & Investment Committee / AFIC (Chair: CFO Oversight)", book_data['agents']['AFIC']),
        "CLO": ("CLO AGENT | RISK & REGULATORY", "Risk, Regulatory & Legal Committee (Chair: CLO Oversight)", book_data['agents']['CLO']),
        "CTO": ("CTO AGENT | SYSTEMS & TELEMETRY", "Technology & Infrastructure Committee (Chair: CTO Oversight)", book_data['agents']['CTO']),
    }
    ag_col1, ag_col2 = st.columns(2)
    with ag_col1:
        for role, (title, _, agent_info) in [
            ("COO", agent_map["COO"]),
            ("CLO", agent_map["CLO"]),
        ]:
            card_style = "critical-agent-card" if critical_lead == role else "secondary-agent-card" if critical_lead is not None and critical_lead != role else "agent-card"
            badge = "🚨 CRITICAL PATH LEAD BOTTLENECK" if critical_lead == role else "AGENT"
            st.markdown(f'''
            <div class="{card_style}" style="padding: 14px; border-radius: 8px;">
                <span class="badge badge-agent">{badge} | {title}</span> <strong>Status: {agent_info['status']}</strong><br>
                <small>{agent_info['memo']}</small>
            </div>
            ''', unsafe_allow_html=True)
    with ag_col2:
        for role, (title, _, agent_info) in [
            ("AFIC", agent_map["AFIC"]),
            ("CTO", agent_map["CTO"]),
        ]:
            card_style = "critical-agent-card" if critical_lead == role else "secondary-agent-card" if critical_lead is not None and critical_lead != role else "agent-card"
            badge = "🚨 CRITICAL PATH LEAD BOTTLENECK" if critical_lead == role else "AGENT"
            st.markdown(f'''
            <div class="{card_style}" style="padding: 14px; border-radius: 8px;">
                <span class="badge badge-agent">{badge} | {title}</span> <strong>Status: {agent_info['status']}</strong><br>
                <small>{agent_info['memo']}</small>
            </div>
            ''', unsafe_allow_html=True)

    st.subheader("Frontline Verification Hold Radar")
    critical_idx = book_data.get("critical_check_idx")
    if critical_idx is not None:
        item_text = book_data["checks"][critical_idx]
        item_cleared = st.session_state.get(f"chk_{book}_{critical_idx}", False)
        if item_cleared:
            st.markdown(f'''
            <div class="radar-card-cleared">
                <span class="badge badge-success">✅ FRONTLINE ARTIFACT CLEARED</span><br>
                <small>Frontline Item #{critical_idx + 1} [{item_text}] verified and cleared at Site Operations.</small>
            </div>
            ''', unsafe_allow_html=True)
        else:
            st.markdown(f'''
            <div class="radar-card">
                <span class="badge badge-danger">🚨 HOLDING GATE</span><br>
                <strong>HOLDING GATE: Frontline Item #{critical_idx + 1} [{item_text}] is unverified.</strong><br>
                <small>This is the exact physical artifact currently holding up the critical path in Tier 3 Site Operations.</small>
            </div>
            ''', unsafe_allow_html=True)
    else:
        st.info("No critical frontline checklist item mapped for this operating book.")

    st.subheader("Board Sub-Committee Statutory Quorum")
    q1, q2 = st.columns(2)
    with q1:
        critical_key_order = [
            ("COO", "Operations & Asset Delivery Committee (Chair: COO Oversight)"),
            ("AFIC", "Audit, Finance & Investment Committee / AFIC (Chair: CFO Oversight)"),
            ("CLO", "Risk, Regulatory & Legal Committee (Chair: CLO Oversight)"),
            ("CTO", "Technology & Infrastructure Committee (Chair: CTO Oversight)"),
        ]
        for role, label in critical_key_order:
            checkbox_key = f"comm_{book}_{'ops' if role == 'COO' else 'afic' if role == 'AFIC' else 'risk' if role == 'CLO' else 'tech'}"
            is_required = critical_lead == role
            checkbox_label = f"{label} — 🚨 **REQUIRED CRITICAL PATH SIGN-OFF**" if is_required else label
            st.checkbox(checkbox_label, value=st.session_state.get(checkbox_key, False), key=checkbox_key)
    with q2:
        st.subheader("Holding Loss Recovery Allocation")
        st.table({
            "Category": ["Primary Operating Standby", "WACC Carrying Demurrage", "Regulatory Delay Penalty", "Total Weekly Exposure"],
            "Weekly Amount": [f"${base_burn*0.35:,.0f}", f"${base_burn*0.40:,.0f}", f"${base_burn*0.25:,.0f}", f"${base_burn:,.0f}"],
            "Client Retained (90%)": [f"${base_burn*0.35*0.9:,.0f}", f"${base_burn*0.40*0.9:,.0f}", f"${base_burn*0.25*0.9:,.0f}", f"${base_burn*0.9:,.0f}"],
            "Phoenix Accrual (10%)": [f"${base_burn*0.35*0.1:,.0f}", f"${base_burn*0.40*0.1:,.0f}", f"${base_burn*0.25*0.1:,.0f}", f"${base_burn*0.1:,.0f}"]
        })
    
    st.divider()
    t1_sp, t1_btn = st.columns([1.5, 1])
    with t1_btn:
        if is_quorum:
            st.button("➡️ Advance to Tier 2 (General Management)", on_click=nav_to, args=("2️⃣ Tier 2 | General Management",), type="primary")
        else:
            st.warning(f"⚠️ Quorum Incomplete ({quorum_count}/4). Full committee quorum or Chairman Override required.")

# ----------------- TIER 2: GENERAL MANAGEMENT -----------------
elif "Tier 2" in view:
    st.header("General Management Directive & Domain Translation")
    st.write(f"Operational translation of Boardroom mandates for {book}.")

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
        st.markdown(f'''
        <div class="card" style="border-left: 4px solid var(--teal);">
            <strong>Statutory Mandate Active:</strong> {active_surge}% Surge Capital Envelope Authorized | 
            <strong>Regime:</strong> {book_data['regime']} | 
            <strong>Action:</strong> Domain Work Orders Ready for Site Dispatch
        </div>
        ''', unsafe_allow_html=True)
        
        g1, g2, g3, g4 = st.columns(4)
        g1.markdown(f"<div class='card'><span class='badge badge-active'>OPERATIONS (COO)</span><br>Surge: {active_surge}%<br>SLA: 1 business day<br><small>Deploy dedicated 24/7 testing crew and clear standby logs.</small></div>", unsafe_allow_html=True)
        g2.markdown(f"<div class='card'><span class='badge badge-active'>CAPITAL (CFO)</span><br>Surge: {active_surge}%<br>SLA: 1 business day<br><small>Release milestone payment upon certified artifact verification.</small></div>", unsafe_allow_html=True)
        g3.markdown(f"<div class='card'><span class='badge badge-active'>COMPLIANCE (CLO)</span><br>Surge: {active_surge}%<br>SLA: 3 business days<br><small>Transmit compliance attestation to governing authority.</small></div>", unsafe_allow_html=True)
        g4.markdown(f"<div class='card'><span class='badge badge-active'>SYSTEMS (CTO)</span><br>Surge: {active_surge}%<br>SLA: 4 hours<br><small>Deploy synthetic calibration scripts and clear telemetry lock.</small></div>", unsafe_allow_html=True)
        
        st.divider()
        
        def dispatch_directive():
            st.session_state['directive_issued'][book] = True
            st.session_state['active_view'] = '3️⃣ Tier 3 | Site Operations'
            
        t2_sp, t2_btn = st.columns([1.5, 1])
        with t2_btn:
            st.button("⚡ Dispatch Translated Directive to Frontline", on_click=dispatch_directive, type="primary")

# ----------------- TIER 3: SITE OPERATIONS -----------------
elif "Tier 3" in view:
    st.header(f"Site Operations Hub / {book}")
    
    st.subheader("Upstream Governance Status")
    ug1, ug2, ug3, ug4 = st.columns(4)
    ug1.markdown(f"<div class='card'><span class='badge badge-active'>OPERATIONS</span><br>Surge: {active_surge}%<br>SLA: 1 business day</div>", unsafe_allow_html=True)
    ug2.markdown(f"<div class='card'><span class='badge badge-active'>CAPITAL</span><br>Surge: {active_surge}%<br>SLA: 1 business day</div>", unsafe_allow_html=True)
    ug3.markdown(f"<div class='card'><span class='badge badge-active'>COMPLIANCE</span><br>Surge: {active_surge}%<br>SLA: 3 business days</div>", unsafe_allow_html=True)
    ug4.markdown(f"<div class='card'><span class='badge badge-active'>SYSTEMS</span><br>Surge: {active_surge}%<br>SLA: 4 hours</div>", unsafe_allow_html=True)
    
    st.subheader(f"Authentic Control Artifacts ({book})")
    art = book_data["artifacts"]
    a1, a2, a3, a4 = st.columns(4)
    a1.markdown(f"<div class='card'><strong>{art[0][0]}</strong><br><small>{art[0][1]}</small></div>", unsafe_allow_html=True)
    a2.markdown(f"<div class='card'><strong>{art[1][0]}</strong><br><small>{art[1][1]}</small></div>", unsafe_allow_html=True)
    a3.markdown(f"<div class='card'><strong>{art[2][0]}</strong><br><small>{art[2][1]}</small></div>", unsafe_allow_html=True)
    a4.markdown(f"<div class='card'><strong>{art[3][0]}</strong><br><small>{art[3][1]}</small></div>", unsafe_allow_html=True)
    
    st.subheader("Frontline SOP Release Checklist")
    checks_raw = book_data["checks"]
    critical_idx = book_data.get("critical_check_idx")
    c_col1, c_col2 = st.columns(2)
    
    check_states = []
    for i, chk_text in enumerate(checks_raw):
        col_target = c_col1 if i % 2 == 0 else c_col2
        k = f"chk_{book}_{i}"
        chk_label = f"🔴 **{chk_text}** — *(🚨 CRITICAL PATH BLOCKER)*" if i == critical_idx else chk_text
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
        st.session_state['phase_2_authorized'][book] = False
        st.session_state['active_view'] = '4️⃣ Forensic Audit Ledger'

    def escalate_to_board():
        st.session_state['board_escalation'][book] = True
        st.session_state['active_view'] = '1️⃣ Tier 1 | Chairman Directorate'

    if completed_count == 8:
        t3_sp, t3_act = st.columns([1.5, 1])
        with t3_act:
            st.button("⚡ Submit Frontline SOP Sign-off & Settle", on_click=signoff_and_settle, type="primary")
    else:
        st.info(f"{completed_count}/8 checks complete. All 8 verification checks required for physical sign-off.")
        with st.expander("🚨 Transmit Critical Impediment to Chairman"):
            st.selectbox("Impediment Category", ["Specialist Labor Shortage", "Critical Hardware/Testing Delay", "Regulatory Compliance Hold"])
            st.text_input("Field Context", "Frontline blocked on compliance gate; requires emergency Board intervention.")
            esc_sp, esc_btn = st.columns([1.5, 1])
            with esc_btn:
                st.button("🚨 Dispatch Emergency Ticket to Chairman", on_click=escalate_to_board, type="primary")

# ----------------- TIER 4: FORENSIC AUDIT LEDGER -----------------
elif "Ledger" in view:
    st.header("Immutable Governance & Forensic Audit Ledger")
    st.write("Cryptographically verifiable chain of custody across all 12 operating books.")
    
    if st.session_state['ledger']:
        st.dataframe(st.session_state['ledger'], use_container_width=True)
    else:
        st.info("No frontline sign-offs recorded in this session. Complete Tier 3 SOP verification to generate an entry.")

st.caption(f"Factory Command Post | Autonomous Capital Defense Control Plane | Audited Sync: {st.session_state['last_sync']}")

# config.py - Top 12 Sector Master Strategy Engine & Governance Surface

SECTORS = {
    "ACC_BASELINE": {
        "title": "🧠 ACC Executive Synthesis & Knowledge Engine",
        "bridge_text": "Synthesis reconciles 100% of National Drift ($420k/wk): Northern $320k/wk (76.2%), Midland $40k/wk (9.5%), Central $30k/wk (7.1%), South Island $30k/wk (7.1%).",
        "metrics": [
            {"label": "Macro Valuation at Risk", "value": "$63.6 Billion", "basis": "Total OCL Disclosures"},
            {"label": "Annual Velocity Drift Cost", "value": "$2.556 Billion", "basis": "Annual Scheme Underwriting Gap"},
            {"label": "Actionable Controllable Loss", "value": "$1.209 Billion", "basis": "Preventable Administrative Drag (65%)"}
        ],
        "active_directive": {
            "title": "Mandate Standardized Case Triage & Direct Telemetry Ingestion",
            "completion_pct": 74,
            "compliant_units": "18 of 24 Regional Health Hubs",
            "burn_reclaimed": "$236,800 / wk",
            "days_active": 5
        },
        "layer2_operations": [
            {"site": "Northern Hub 01", "drift": "+4.2 Wks", "burn": "$180k/wk", "bottleneck": "Manual Medical Paper Verification"},
            {"site": "Midland Hub 02", "drift": "+1.8 Wks", "burn": "$40k/wk", "bottleneck": "Sequential Legal Approval Queue"},
            {"site": "Central Hub 03", "drift": "+1.1 Wks", "burn": "$30k/wk", "bottleneck": "Batch Reconciliation Delay"}
        ],
        "footer": "💡 Ground-Truth Source: Ingested 2025 ACC Financial Condition Report & Live Telemetry Feed."
    },
    "GRID_PJM": {
        "title": "⚡ PJM Infrastructure Capital & Interconnection Surface",
        "bridge_text": "Synthesis reconciles 100% of Active Interconnection Drift ($340k/wk): Regional Re-Study Backlogs (72%), Substation Lags (18%), Environmental Clearance (10%).",
        "metrics": [
            {"label": "Macro Valuation at Risk", "value": "$35.3 Million", "basis": "24-Month Long-Tail Exposure"},
            {"label": "Annual Velocity Drift Cost", "value": "$17.68 Million", "basis": "Interconnection Queue Dwell Drag"},
            {"label": "Actionable Controllable Loss", "value": "$340,000 / wk", "basis": "Redundant Manual Study Re-Keying"}
        ],
        "active_directive": {
            "title": "Bypass Manual Re-Studies via Pre-Validated Capacity Automation",
            "completion_pct": 62,
            "compliant_units": "31 of 50 Substation Clusters",
            "burn_reclaimed": "$210,800 / wk",
            "days_active": 6
        },
        "layer2_operations": [
            {"site": "Substation Alpha (Zone 4)", "drift": "+6.1 Wks", "burn": "$150k/wk", "bottleneck": "Manual FERC Re-Study Queue"},
            {"site": "Substation Beta (Zone 2)", "drift": "+3.4 Wks", "burn": "$110k/wk", "bottleneck": "Paper Land Retainer Audit"},
            {"site": "Substation Gamma (Zone 1)", "drift": "+2.0 Wks", "burn": "$80k/wk", "bottleneck": "Sequential Environmental Sign-off"}
        ],
        "footer": "💡 Ground-Truth Source: Ingested PJM FERC Filings, GIS Queue Feeds & PUCT Dockets."
    },
    "BIOPHARMA_CLARITY": {
        "title": "☢️ Radiopharmaceutical Clinical Governance Surface",
        "bridge_text": "Synthesis reconciles 100% of Trial Onboarding Drift ($280k/wk): Hospital Ethics (65%), Dosimetry Sign-offs (20%), Legal SLA (15%).",
        "metrics": [
            {"label": "Macro Valuation at Risk", "value": "$4.1 Billion", "basis": "Patented Monopoly Baseline"},
            {"label": "Annual Velocity Drift Cost", "value": "$14.56 Million", "basis": "Trial Completion Delay Drag"},
            {"label": "Actionable Controllable Loss", "value": "$25.7 Million", "basis": "Manual SDV Paper Cross-Checking (65%)"}
        ],
        "active_directive": {
            "title": "Freeze 100% Manual SDV; Deploy FDA Risk-Based Monitoring",
            "completion_pct": 68,
            "compliant_units": "17 of 25 Trial Sites",
            "burn_reclaimed": "$190,400 / wk",
            "days_active": 4
        },
        "layer2_operations": [
            {"site": "Site 04 (Johns Hopkins)", "drift": "+4.5 Wks", "burn": "$120k/wk", "bottleneck": "Manual Paper SDV Cross-Check"},
            {"site": "Site 12 (Mayo Clinic)", "drift": "+3.1 Wks", "burn": "$90k/wk", "bottleneck": "Sequential Ethics Committee Sign-off"},
            {"site": "Site 09 (Peter Mac)", "drift": "+2.3 Wks", "burn": "$70k/wk", "bottleneck": "Dosimetry Calibration Audit"}
        ],
        "footer": "💡 Ground-Truth Source: Ingested ASX Audited Regulatory Filings & Clinical Site Registries."
    },
    "DEFENSE_AEROSPACE": {
        "title": "🛡️ Sovereign Defense & Aerospace Acquisition Engine",
        "bridge_text": "Synthesis reconciles 100% of Program Drift ($650k/wk): Tier-2 Supplier Lags (55%), Security Vetting (30%), Testing Clearance (15%).",
        "metrics": [
            {"label": "Macro Valuation at Risk", "value": "$12.8 Billion", "basis": "Sovereign Program Capital Baseline"},
            {"label": "Annual Velocity Drift Cost", "value": "$33.80 Million", "basis": "Milestone Schedule Siphon"},
            {"label": "Actionable Controllable Loss", "value": "$21.97 Million", "basis": "Manual Supply Chain Quality Audits"}
        ],
        "active_directive": {
            "title": "Automate Tier-2 Supplier Security Verification via Digital Twin",
            "completion_pct": 55,
            "compliant_units": "11 of 20 Defense Contractors",
            "burn_reclaimed": "$357,500 / wk",
            "days_active": 7
        },
        "layer2_operations": [
            {"site": "Avionics Sub-Assembly Plant A", "drift": "+8.0 Wks", "burn": "$300k/wk", "bottleneck": "Manual Paper Component Audit"},
            {"site": "Propulsion Testing Rig B", "drift": "+5.2 Wks", "burn": "$200k/wk", "bottleneck": "Sequential Defense Security Clearance"}
        ],
        "footer": "💡 Ground-Truth Source: Ingested Department of Defense Telemetry & Contracting Dockets."
    },
    "ENERGY_ERCOT": {
        "title": "🔋 Texas ERCOT Storage & Dispatch Surface",
        "bridge_text": "Synthesis reconciles 100% of Battery Dispatch Drift ($210k/wk): Interconnection Testing (60%), Telemetry Linkage (40%).",
        "metrics": [
            {"label": "Macro Valuation at Risk", "value": "$1.8 Billion", "basis": "Storage Asset Capital Baseline"},
            {"label": "Annual Velocity Drift Cost", "value": "$10.92 Million", "basis": "Missed Peak Arbitrage Revenue"},
            {"label": "Actionable Controllable Loss", "value": "$7.10 Million", "basis": "Manual Grid Model Verification"}
        ],
        "active_directive": {
            "title": "Deploy Direct Telemetry Automated Grid Model Ingestion",
            "completion_pct": 80,
            "compliant_units": "16 of 20 Battery Sites",
            "burn_reclaimed": "$168,000 / wk",
            "days_active": 3
        },
        "layer2_operations": [
            {"site": "West Texas Storage Facility 1", "drift": "+3.2 Wks", "burn": "$120k/wk", "bottleneck": "Manual SCADA Calibration Check"}
        ],
        "footer": "💡 Ground-Truth Source: Ingested ERCOT Nodal Market Telemetry."
    },
    "BANKING_APRA": {
        "title": "🏛️ APRA Prudential Capital & Liquidity Surface",
        "bridge_text": "Synthesis reconciles 100% of RWA Calculation Drift ($520k/wk): Legacy Database Re-keying (80%), Manual Audit Sign-off (20%).",
        "metrics": [
            {"label": "Macro Valuation at Risk", "value": "$42.0 Billion", "basis": "Risk-Weighted Asset Baseline"},
            {"label": "Annual Velocity Drift Cost", "value": "$27.04 Million", "basis": "Excess Tier-1 Capital Holdback"},
            {"label": "Actionable Controllable Loss", "value": "$17.58 Million", "basis": "Manual Data Reconciliation Drag"}
        ],
        "active_directive": {
            "title": "Automate RWA Reporting Pipeline directly from Source Ledger",
            "completion_pct": 70,
            "compliant_units": "7 of 10 Capital Divisions",
            "burn_reclaimed": "$364,000 / wk",
            "days_active": 8
        },
        "layer2_operations": [
            {"site": "Commercial Mortgage Division", "drift": "+5.0 Wks", "burn": "$300k/wk", "bottleneck": "Manual Spread-sheet Cross-Checking"}
        ],
        "footer": "💡 Ground-Truth Source: Ingested APRA Regulatory Disclosures & Internal Ledgers."
    },
    "SUPPLY_CHAIN_PORT": {
        "title": "⚓ Deepwater Port Logistics & Intermodal Engine",
        "bridge_text": "Synthesis reconciles 100% of Berth Dwell Drift ($410k/wk): Customs Inspection Backlogs (65%), Paper Manifest Verification (35%).",
        "metrics": [
            {"label": "Macro Valuation at Risk", "value": "$2.9 Billion", "basis": "Annual Freight Throughput Baseline"},
            {"label": "Annual Velocity Drift Cost", "value": "$21.32 Million", "basis": "Demurrage & Container Dwell Penalties"},
            {"label": "Actionable Controllable Loss", "value": "$13.86 Million", "basis": "Manual Paper Customs Audit"}
        ],
        "active_directive": {
            "title": "Mandate Automated Manifest Ingestion & OCR Clearance",
            "completion_pct": 60,
            "compliant_units": "12 of 20 Container Terminals",
            "burn_reclaimed": "$246,000 / wk",
            "days_active": 5
        },
        "layer2_operations": [
            {"site": "Terminal 3 Gate Queue", "drift": "+4.1 Wks", "burn": "$250k/wk", "bottleneck": "Manual Paper Bill-of-Lading Audit"}
        ],
        "footer": "💡 Ground-Truth Source: Ingested Port Authority AIS & Customs Feeds."
    },
    "HEALTH_NHS": {
        "title": "🏥 NHS Elective Care Recovery & Surgical Surface",
        "bridge_text": "Synthesis reconciles 100% of Surgical Queue Drift ($380k/wk): Pre-Op Admin Clearance (70%), Bed Allocation Delay (30%).",
        "metrics": [
            {"label": "Macro Valuation at Risk", "value": "£1.4 Billion", "basis": "Elective Care Backlog Funding"},
            {"label": "Annual Velocity Drift Cost", "value": "£19.76 Million", "basis": "Unused Theatre Time & Cancellations"},
            {"label": "Actionable Controllable Loss", "value": "£12.84 Million", "basis": "Manual Paper Patient Onboarding"}
        ],
        "active_directive": {
            "title": "Deploy Automated Pre-Op Screening & Digital Consent Protocols",
            "completion_pct": 75,
            "compliant_units": "15 of 20 NHS Trust Hospitals",
            "burn_reclaimed": "£285,000 / wk",
            "days_active": 6
        },
        "layer2_operations": [
            {"site": "Royal Infirmary Theatre Suite B", "drift": "+3.8 Wks", "burn": "£200k/wk", "bottleneck": "Paper Pre-Op Nurse Sign-off"}
        ],
        "footer": "💡 Ground-Truth Source: Ingested NHS Digital Waiting List Telemetry."
    },
    "MINING_COPPER": {
        "title": "⛏️ Tier-1 Copper Smelting & Haulage Surface",
        "bridge_text": "Synthesis reconciles 100% of Ore Dispatch Drift ($490k/wk): Haulage Fleet Maintenance Lags (60%), Assay Lab Delays (40%).",
        "metrics": [
            {"label": "Macro Valuation at Risk", "value": "$3.4 Billion", "basis": "Annual Concentrate Output Value"},
            {"label": "Annual Velocity Drift Cost", "value": "$25.48 Million", "basis": "Smelter Bottleneck Idle Drag"},
            {"label": "Actionable Controllable Loss", "value": "$16.56 Million", "basis": "Manual Assay Sample Logging"}
        ],
        "active_directive": {
            "title": "Deploy Automated Automated Assay Testing & Fleet Telemetry",
            "completion_pct": 65,
            "compliant_units": "13 of 20 Mine Pits",
            "burn_reclaimed": "$318,500 / wk",
            "days_active": 4
        },
        "layer2_operations": [
            {"site": "Pit North Haulage Loop", "drift": "+4.9 Wks", "burn": "$290k/wk", "bottleneck": "Manual Paper Driver Shift Re-keying"}
        ],
        "footer": "💡 Ground-Truth Source: Ingested SCADA & Ore Transport Feeds."
    },
    "TELCO_5G": {
        "title": "📡 5G C-Band Infrastructure Surface",
        "bridge_text": "Synthesis reconciles 100% of Cell Site Activation Drift ($290k/wk): Council Permitting (70%), Fiber Backhaul SLA (30%).",
        "metrics": [
            {"label": "Macro Valuation at Risk", "value": "$1.2 Billion", "basis": "C-Band Spectrum License Baseline"},
            {"label": "Annual Velocity Drift Cost", "value": "$15.08 Million", "basis": "Delayed Subscriber Revenue"},
            {"label": "Actionable Controllable Loss", "value": "$9.80 Million", "basis": "Manual Municipal Permit Paperwork"}
        ],
        "active_directive": {
            "title": "Bypass Manual Council Permitting via State Fast-Track API",
            "completion_pct": 82,
            "compliant_units": "164 of 200 Cell Towers",
            "burn_reclaimed": "$237,800 / wk",
            "days_active": 9
        },
        "layer2_operations": [
            {"site": "Metro Sector Grid 09", "drift": "+2.9 Wks", "burn": "$140k/wk", "bottleneck": "Manual Local Board Approval"}
        ],
        "footer": "💡 Ground-Truth Source: Ingested FCC Dockets & Carrier Build Telemetry."
    },
    "INSURANCE_PROPERTY": {
        "title": "🏢 Global Commercial Property Reinsurance Engine",
        "bridge_text": "Synthesis reconciles 100% of Claim Resolution Drift ($580k/wk): Paper Adjuster Audits (75%), Legal Disagreements (25%).",
        "metrics": [
            {"label": "Macro Valuation at Risk", "value": "$8.5 Billion", "basis": "Underwritten Treaty Exposure"},
            {"label": "Annual Velocity Drift Cost", "value": "$30.16 Million", "basis": "Dwell Penalty Interest & Legal Friction"},
            {"label": "Actionable Controllable Loss", "value": "$19.60 Million", "basis": "Manual Claim File Cross-Checking"}
        ],
        "active_directive": {
            "title": "Automate Property Loss Assessment via Drone GIS & AI Claims Rule",
            "completion_pct": 58,
            "compliant_units": "29 of 50 Major Losses",
            "burn_reclaimed": "$336,400 / wk",
            "days_active": 5
        },
        "layer2_operations": [
            {"site": "Commercial Complex Portfolio B", "drift": "+5.8 Wks", "burn": "$320k/wk", "bottleneck": "Manual Paper Adjuster Verification"}
        ],
        "footer": "💡 Ground-Truth Source: Ingested Lloyd's Syndicate Claims Feed."
    },
    "RAIL_FREIGHT": {
        "title": "🚂 National Class-1 Rail Logistics Engine",
        "bridge_text": "Synthesis reconciles 100% of Yard Dwell Drift ($440k/wk): Locomotive Maintenance Backlog (65%), Crew Scheduling Lags (35%).",
        "metrics": [
            {"label": "Macro Valuation at Risk", "value": "$5.6 Billion", "basis": "Network Asset Capital Baseline"},
            {"label": "Annual Velocity Drift Cost", "value": "$22.88 Million", "basis": "Railcar Dwell & Network Congestion"},
            {"label": "Actionable Controllable Loss", "value": "$14.87 Million", "basis": "Manual Crew Callboard Paperwork"}
        ],
        "active_directive": {
            "title": "Deploy Automated Locomotive Telemetry & Crew Dispatch Rules",
            "completion_pct": 71,
            "compliant_units": "14 of 20 Switching Yards",
            "burn_reclaimed": "$312,400 / wk",
            "days_active": 6
        },
        "layer2_operations": [
            {"site": "Central Sorting Yard Gamma", "drift": "+4.0 Wks", "burn": "$260k/wk", "bottleneck": "Paper Crew Shift Log Cross-Checking"}
        ],
        "footer": "💡 Ground-Truth Source: Ingested FRA Telemetry & Class-1 Dispatch Systems."
    }
}

# -----------------------------------------------------------------------------
# Update 4 — Four-Stage Clearance Tracker & Cost of Inaction (COI) Schema
# Stages: Intake → Evidence Validation → Authority Sign-off → Operational Clearance
# -----------------------------------------------------------------------------
CLEARANCE_STAGE_LABELS = (
    "Stage 1 · Intake Queue",
    "Stage 2 · Evidence Validation",
    "Stage 3 · Authority Sign-off",
    "Stage 4 · Operational Clearance",
)

# Per-sector clearance pipeline counts + COI metric cards (Label / Big Value / Ground-Truth Basis)
SECTOR_CLEARANCE_COI = {
    "ACC_BASELINE": {
        "clearance_stages": [
            {"stage": 1, "label": CLEARANCE_STAGE_LABELS[0], "units": 42, "cleared_pct": 88, "status": "Flowing", "owner": "Regional Intake Desk"},
            {"stage": 2, "label": CLEARANCE_STAGE_LABELS[1], "units": 31, "cleared_pct": 74, "status": "Bottleneck", "owner": "Medical Evidence Hub"},
            {"stage": 3, "label": CLEARANCE_STAGE_LABELS[2], "units": 18, "cleared_pct": 61, "status": "Watch", "owner": "Case Authority Panel"},
            {"stage": 4, "label": CLEARANCE_STAGE_LABELS[3], "units": 14, "cleared_pct": 55, "status": "Active", "owner": "Operational Clearance"},
        ],
        "coi_metrics": [
            {"label": "COI · Weekly Cost of Inaction", "value": "$420k / wk", "basis": "Uncleared Stage 2–3 Dwell Burn"},
            {"label": "COI · Clearance Lag Exposure", "value": "$21.8M", "basis": "12-Month Projected Drift if Stages Stall"},
            {"label": "COI · Controllable Recovery", "value": "65%", "basis": "Share Reclaimable via Stage Automation"},
        ],
    },
    "GRID_PJM": {
        "clearance_stages": [
            {"stage": 1, "label": CLEARANCE_STAGE_LABELS[0], "units": 50, "cleared_pct": 82, "status": "Flowing", "owner": "Queue Intake"},
            {"stage": 2, "label": CLEARANCE_STAGE_LABELS[1], "units": 37, "cleared_pct": 68, "status": "Bottleneck", "owner": "Re-Study Desk"},
            {"stage": 3, "label": CLEARANCE_STAGE_LABELS[2], "units": 22, "cleared_pct": 54, "status": "Watch", "owner": "FERC Sign-off"},
            {"stage": 4, "label": CLEARANCE_STAGE_LABELS[3], "units": 16, "cleared_pct": 48, "status": "Active", "owner": "Interconnection Clearance"},
        ],
        "coi_metrics": [
            {"label": "COI · Weekly Cost of Inaction", "value": "$340k / wk", "basis": "Uncleared Re-Study & Environmental Dwell"},
            {"label": "COI · Clearance Lag Exposure", "value": "$17.7M", "basis": "Annual Interconnection Drift if Stages Stall"},
            {"label": "COI · Controllable Recovery", "value": "62%", "basis": "Share Reclaimable via Pre-Validated Capacity"},
        ],
    },
    "BIOPHARMA_CLARITY": {
        "clearance_stages": [
            {"stage": 1, "label": CLEARANCE_STAGE_LABELS[0], "units": 28, "cleared_pct": 85, "status": "Flowing", "owner": "Site Intake"},
            {"stage": 2, "label": CLEARANCE_STAGE_LABELS[1], "units": 21, "cleared_pct": 71, "status": "Bottleneck", "owner": "SDV / Dosimetry"},
            {"stage": 3, "label": CLEARANCE_STAGE_LABELS[2], "units": 15, "cleared_pct": 64, "status": "Watch", "owner": "Ethics / Legal SLA"},
            {"stage": 4, "label": CLEARANCE_STAGE_LABELS[3], "units": 11, "cleared_pct": 52, "status": "Active", "owner": "Trial Clearance"},
        ],
        "coi_metrics": [
            {"label": "COI · Weekly Cost of Inaction", "value": "$280k / wk", "basis": "Uncleared Ethics & SDV Stage Burn"},
            {"label": "COI · Clearance Lag Exposure", "value": "$14.6M", "basis": "Trial Completion Delay if Stages Stall"},
            {"label": "COI · Controllable Recovery", "value": "68%", "basis": "Share Reclaimable via Risk-Based Monitoring"},
        ],
    },
    "DEFENSE_AEROSPACE": {
        "clearance_stages": [
            {"stage": 1, "label": CLEARANCE_STAGE_LABELS[0], "units": 24, "cleared_pct": 78, "status": "Flowing", "owner": "Supplier Intake"},
            {"stage": 2, "label": CLEARANCE_STAGE_LABELS[1], "units": 19, "cleared_pct": 60, "status": "Bottleneck", "owner": "Security Vetting"},
            {"stage": 3, "label": CLEARANCE_STAGE_LABELS[2], "units": 12, "cleared_pct": 50, "status": "Watch", "owner": "Program Authority"},
            {"stage": 4, "label": CLEARANCE_STAGE_LABELS[3], "units": 9, "cleared_pct": 42, "status": "Active", "owner": "Testing Clearance"},
        ],
        "coi_metrics": [
            {"label": "COI · Weekly Cost of Inaction", "value": "$650k / wk", "basis": "Uncleared Vetting & Tier-2 Stage Burn"},
            {"label": "COI · Clearance Lag Exposure", "value": "$33.8M", "basis": "Milestone Siphon if Stages Stall"},
            {"label": "COI · Controllable Recovery", "value": "55%", "basis": "Share Reclaimable via Digital Twin Verification"},
        ],
    },
    "ENERGY_ERCOT": {
        "clearance_stages": [
            {"stage": 1, "label": CLEARANCE_STAGE_LABELS[0], "units": 20, "cleared_pct": 90, "status": "Flowing", "owner": "Site Intake"},
            {"stage": 2, "label": CLEARANCE_STAGE_LABELS[1], "units": 17, "cleared_pct": 80, "status": "Flowing", "owner": "Interconnection Testing"},
            {"stage": 3, "label": CLEARANCE_STAGE_LABELS[2], "units": 14, "cleared_pct": 72, "status": "Watch", "owner": "Grid Model Sign-off"},
            {"stage": 4, "label": CLEARANCE_STAGE_LABELS[3], "units": 12, "cleared_pct": 68, "status": "Active", "owner": "Dispatch Clearance"},
        ],
        "coi_metrics": [
            {"label": "COI · Weekly Cost of Inaction", "value": "$210k / wk", "basis": "Uncleared Testing & Telemetry Stage Burn"},
            {"label": "COI · Clearance Lag Exposure", "value": "$10.9M", "basis": "Missed Peak Arbitrage if Stages Stall"},
            {"label": "COI · Controllable Recovery", "value": "80%", "basis": "Share Reclaimable via Automated Grid Ingestion"},
        ],
    },
    "BANKING_APRA": {
        "clearance_stages": [
            {"stage": 1, "label": CLEARANCE_STAGE_LABELS[0], "units": 16, "cleared_pct": 84, "status": "Flowing", "owner": "Ledger Intake"},
            {"stage": 2, "label": CLEARANCE_STAGE_LABELS[1], "units": 12, "cleared_pct": 70, "status": "Bottleneck", "owner": "RWA Validation"},
            {"stage": 3, "label": CLEARANCE_STAGE_LABELS[2], "units": 9, "cleared_pct": 62, "status": "Watch", "owner": "Prudential Sign-off"},
            {"stage": 4, "label": CLEARANCE_STAGE_LABELS[3], "units": 7, "cleared_pct": 55, "status": "Active", "owner": "Capital Clearance"},
        ],
        "coi_metrics": [
            {"label": "COI · Weekly Cost of Inaction", "value": "$520k / wk", "basis": "Uncleared Re-key & Audit Stage Burn"},
            {"label": "COI · Clearance Lag Exposure", "value": "$27.0M", "basis": "Excess Tier-1 Holdback if Stages Stall"},
            {"label": "COI · Controllable Recovery", "value": "70%", "basis": "Share Reclaimable via Source-Ledger Automation"},
        ],
    },
    "SUPPLY_CHAIN_PORT": {
        "clearance_stages": [
            {"stage": 1, "label": CLEARANCE_STAGE_LABELS[0], "units": 36, "cleared_pct": 86, "status": "Flowing", "owner": "Gate Intake"},
            {"stage": 2, "label": CLEARANCE_STAGE_LABELS[1], "units": 27, "cleared_pct": 69, "status": "Bottleneck", "owner": "Manifest / OCR Desk"},
            {"stage": 3, "label": CLEARANCE_STAGE_LABELS[2], "units": 18, "cleared_pct": 58, "status": "Watch", "owner": "Customs Sign-off"},
            {"stage": 4, "label": CLEARANCE_STAGE_LABELS[3], "units": 13, "cleared_pct": 50, "status": "Active", "owner": "Berth Clearance"},
        ],
        "coi_metrics": [
            {"label": "COI · Weekly Cost of Inaction", "value": "$410k / wk", "basis": "Uncleared Customs & Manifest Stage Burn"},
            {"label": "COI · Clearance Lag Exposure", "value": "$21.3M", "basis": "Demurrage Penalties if Stages Stall"},
            {"label": "COI · Controllable Recovery", "value": "60%", "basis": "Share Reclaimable via Automated Manifest OCR"},
        ],
    },
    "HEALTH_NHS": {
        "clearance_stages": [
            {"stage": 1, "label": CLEARANCE_STAGE_LABELS[0], "units": 40, "cleared_pct": 87, "status": "Flowing", "owner": "Referral Intake"},
            {"stage": 2, "label": CLEARANCE_STAGE_LABELS[1], "units": 29, "cleared_pct": 73, "status": "Bottleneck", "owner": "Pre-Op Validation"},
            {"stage": 3, "label": CLEARANCE_STAGE_LABELS[2], "units": 20, "cleared_pct": 66, "status": "Watch", "owner": "Clinical Sign-off"},
            {"stage": 4, "label": CLEARANCE_STAGE_LABELS[3], "units": 15, "cleared_pct": 58, "status": "Active", "owner": "Theatre Clearance"},
        ],
        "coi_metrics": [
            {"label": "COI · Weekly Cost of Inaction", "value": "£380k / wk", "basis": "Uncleared Pre-Op & Bed Stage Burn"},
            {"label": "COI · Clearance Lag Exposure", "value": "£19.8M", "basis": "Unused Theatre Time if Stages Stall"},
            {"label": "COI · Controllable Recovery", "value": "75%", "basis": "Share Reclaimable via Digital Consent Protocols"},
        ],
    },
    "MINING_COPPER": {
        "clearance_stages": [
            {"stage": 1, "label": CLEARANCE_STAGE_LABELS[0], "units": 22, "cleared_pct": 83, "status": "Flowing", "owner": "Pit Intake"},
            {"stage": 2, "label": CLEARANCE_STAGE_LABELS[1], "units": 17, "cleared_pct": 67, "status": "Bottleneck", "owner": "Assay Validation"},
            {"stage": 3, "label": CLEARANCE_STAGE_LABELS[2], "units": 12, "cleared_pct": 59, "status": "Watch", "owner": "Dispatch Sign-off"},
            {"stage": 4, "label": CLEARANCE_STAGE_LABELS[3], "units": 10, "cleared_pct": 51, "status": "Active", "owner": "Haulage Clearance"},
        ],
        "coi_metrics": [
            {"label": "COI · Weekly Cost of Inaction", "value": "$490k / wk", "basis": "Uncleared Assay & Fleet Stage Burn"},
            {"label": "COI · Clearance Lag Exposure", "value": "$25.5M", "basis": "Smelter Idle Drag if Stages Stall"},
            {"label": "COI · Controllable Recovery", "value": "65%", "basis": "Share Reclaimable via Assay & Fleet Telemetry"},
        ],
    },
    "TELCO_5G": {
        "clearance_stages": [
            {"stage": 1, "label": CLEARANCE_STAGE_LABELS[0], "units": 200, "cleared_pct": 92, "status": "Flowing", "owner": "Build Intake"},
            {"stage": 2, "label": CLEARANCE_STAGE_LABELS[1], "units": 176, "cleared_pct": 84, "status": "Flowing", "owner": "Permit Validation"},
            {"stage": 3, "label": CLEARANCE_STAGE_LABELS[2], "units": 150, "cleared_pct": 78, "status": "Watch", "owner": "Council Sign-off"},
            {"stage": 4, "label": CLEARANCE_STAGE_LABELS[3], "units": 132, "cleared_pct": 72, "status": "Active", "owner": "Cell Activation Clearance"},
        ],
        "coi_metrics": [
            {"label": "COI · Weekly Cost of Inaction", "value": "$290k / wk", "basis": "Uncleared Permit & Backhaul Stage Burn"},
            {"label": "COI · Clearance Lag Exposure", "value": "$15.1M", "basis": "Delayed Subscriber Revenue if Stages Stall"},
            {"label": "COI · Controllable Recovery", "value": "82%", "basis": "Share Reclaimable via State Fast-Track API"},
        ],
    },
    "INSURANCE_PROPERTY": {
        "clearance_stages": [
            {"stage": 1, "label": CLEARANCE_STAGE_LABELS[0], "units": 55, "cleared_pct": 80, "status": "Flowing", "owner": "FNOL Intake"},
            {"stage": 2, "label": CLEARANCE_STAGE_LABELS[1], "units": 41, "cleared_pct": 63, "status": "Bottleneck", "owner": "Adjuster Validation"},
            {"stage": 3, "label": CLEARANCE_STAGE_LABELS[2], "units": 28, "cleared_pct": 52, "status": "Watch", "owner": "Treaty Sign-off"},
            {"stage": 4, "label": CLEARANCE_STAGE_LABELS[3], "units": 20, "cleared_pct": 44, "status": "Active", "owner": "Settlement Clearance"},
        ],
        "coi_metrics": [
            {"label": "COI · Weekly Cost of Inaction", "value": "$580k / wk", "basis": "Uncleared Adjuster & Legal Stage Burn"},
            {"label": "COI · Clearance Lag Exposure", "value": "$30.2M", "basis": "Dwell Interest & Legal Friction if Stages Stall"},
            {"label": "COI · Controllable Recovery", "value": "58%", "basis": "Share Reclaimable via GIS / AI Claims Rules"},
        ],
    },
    "RAIL_FREIGHT": {
        "clearance_stages": [
            {"stage": 1, "label": CLEARANCE_STAGE_LABELS[0], "units": 30, "cleared_pct": 85, "status": "Flowing", "owner": "Yard Intake"},
            {"stage": 2, "label": CLEARANCE_STAGE_LABELS[1], "units": 23, "cleared_pct": 71, "status": "Bottleneck", "owner": "Locomotive Validation"},
            {"stage": 3, "label": CLEARANCE_STAGE_LABELS[2], "units": 17, "cleared_pct": 64, "status": "Watch", "owner": "Crew Sign-off"},
            {"stage": 4, "label": CLEARANCE_STAGE_LABELS[3], "units": 13, "cleared_pct": 57, "status": "Active", "owner": "Dispatch Clearance"},
        ],
        "coi_metrics": [
            {"label": "COI · Weekly Cost of Inaction", "value": "$440k / wk", "basis": "Uncleared Maintenance & Crew Stage Burn"},
            {"label": "COI · Clearance Lag Exposure", "value": "$22.9M", "basis": "Railcar Dwell if Stages Stall"},
            {"label": "COI · Controllable Recovery", "value": "71%", "basis": "Share Reclaimable via Telemetry & Crew Rules"},
        ],
    },
}


def get_sector_book(key):
    book = dict(SECTORS.get(key, SECTORS["ACC_BASELINE"]))
    clearance_coi = SECTOR_CLEARANCE_COI.get(key, SECTOR_CLEARANCE_COI["ACC_BASELINE"])
    book["clearance_stages"] = clearance_coi["clearance_stages"]
    book["coi_metrics"] = clearance_coi["coi_metrics"]
    return book

def sector_book_options():
    return {
        "ACC_BASELINE": "🧠 ACC Baseline · NZ Scheme Book",
        "GRID_PJM": "⚡ Grid PJM · Interconnection Book",
        "BIOPHARMA_CLARITY": "☢️ Biopharma Clarity · GMP Book",
        "DEFENSE_AEROSPACE": "🛡️ Defense & Aerospace · Sovereign Book",
        "ENERGY_ERCOT": "🔋 ERCOT Energy · Storage Book",
        "BANKING_APRA": "🏛️ APRA Banking · Prudential Book",
        "SUPPLY_CHAIN_PORT": "⚓ Port Logistics · Freight Book",
        "HEALTH_NHS": "🏥 NHS Recovery · Surgical Book",
        "MINING_COPPER": "⛏️ Tier-1 Mining · Ore Haulage Book",
        "TELCO_5G": "📡 5G Infrastructure · Spectrum Book",
        "INSURANCE_PROPERTY": "🏢 Commercial Reinsurance · Treaty Book",
        "RAIL_FREIGHT": "🚂 Class-1 Rail · Logistics Book"
    }

# Short ?co= URL aliases → sector book keys (e.g. ?co=ACC → ACC_BASELINE)
CO_QUERY_ALIASES = {
    "ACC": "ACC_BASELINE",
    "ACC_BASELINE": "ACC_BASELINE",
    "PJM": "GRID_PJM",
    "GRID": "GRID_PJM",
    "GRID_PJM": "GRID_PJM",
    "BIOPHARMA": "BIOPHARMA_CLARITY",
    "CLARITY": "BIOPHARMA_CLARITY",
    "BIOPHARMA_CLARITY": "BIOPHARMA_CLARITY",
    "DEFENSE": "DEFENSE_AEROSPACE",
    "AEROSPACE": "DEFENSE_AEROSPACE",
    "DEFENSE_AEROSPACE": "DEFENSE_AEROSPACE",
    "ERCOT": "ENERGY_ERCOT",
    "ENERGY": "ENERGY_ERCOT",
    "ENERGY_ERCOT": "ENERGY_ERCOT",
    "APRA": "BANKING_APRA",
    "BANKING": "BANKING_APRA",
    "BANKING_APRA": "BANKING_APRA",
    "PORT": "SUPPLY_CHAIN_PORT",
    "SUPPLY": "SUPPLY_CHAIN_PORT",
    "SUPPLY_CHAIN_PORT": "SUPPLY_CHAIN_PORT",
    "NHS": "HEALTH_NHS",
    "HEALTH": "HEALTH_NHS",
    "HEALTH_NHS": "HEALTH_NHS",
    "MINING": "MINING_COPPER",
    "COPPER": "MINING_COPPER",
    "MINING_COPPER": "MINING_COPPER",
    "TELCO": "TELCO_5G",
    "5G": "TELCO_5G",
    "TELCO_5G": "TELCO_5G",
    "INSURANCE": "INSURANCE_PROPERTY",
    "PROPERTY": "INSURANCE_PROPERTY",
    "INSURANCE_PROPERTY": "INSURANCE_PROPERTY",
    "RAIL": "RAIL_FREIGHT",
    "FREIGHT": "RAIL_FREIGHT",
    "RAIL_FREIGHT": "RAIL_FREIGHT",
}

# Canonical short codes written back to ?co=
CO_QUERY_SHORT = {
    "ACC_BASELINE": "ACC",
    "GRID_PJM": "PJM",
    "BIOPHARMA_CLARITY": "BIOPHARMA",
    "DEFENSE_AEROSPACE": "DEFENSE",
    "ENERGY_ERCOT": "ERCOT",
    "BANKING_APRA": "APRA",
    "SUPPLY_CHAIN_PORT": "PORT",
    "HEALTH_NHS": "NHS",
    "MINING_COPPER": "MINING",
    "TELCO_5G": "TELCO",
    "INSURANCE_PROPERTY": "INSURANCE",
    "RAIL_FREIGHT": "RAIL",
}


def resolve_sector_co(co_value, default=None):
    """Resolve a ?co= query value to a sector book key.

    Case-insensitive match against shortcodes (PJM, NHS, ERCOT, GRID, …),
    alias keys, CO_QUERY_SHORT values, and every sector key in config.
    Returns default when no match is found.
    """
    if co_value is None:
        return default
    if isinstance(co_value, (list, tuple)):
        co_value = co_value[0] if co_value else ""
    token = str(co_value).strip().upper().replace("-", "_").replace(" ", "_")
    if not token:
        return default

    # 1) Direct alias / shortcode map (keys stored uppercase)
    if token in CO_QUERY_ALIASES:
        return CO_QUERY_ALIASES[token]

    # 2) Case-insensitive alias keys
    for alias, key in CO_QUERY_ALIASES.items():
        if str(alias).upper().replace("-", "_").replace(" ", "_") == token:
            return key

    # 3) Case-insensitive shortcodes written to ?co=
    for key, short in CO_QUERY_SHORT.items():
        if str(short).upper().replace("-", "_").replace(" ", "_") == token:
            return key

    # 4) Case-insensitive exact match on all config sector keys
    options = sector_book_options()
    sector_keys = list(SECTORS.keys())
    for key in list(dict.fromkeys([*sector_keys, *options.keys()])):
        if str(key).upper() == token:
            return key

    # 5) Token is an underscore segment of a sector key (PJM ⊂ GRID_PJM)
    for key in list(dict.fromkeys([*sector_keys, *options.keys()])):
        parts = str(key).upper().split("_")
        if token in parts:
            return key

    # 6) Prefix / substring fallback against all config keys
    for key in list(dict.fromkeys([*sector_keys, *options.keys()])):
        ku = str(key).upper()
        if ku.startswith(token) or token in ku:
            return key

    return default


def sector_co_short(key):
    """Return the short ?co= code for a sector book key."""
    return CO_QUERY_SHORT.get(key, key)

import streamlit as st
import re

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AAT Phoenix Command Post",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ENTERPRISE MOBILE & TABLET STYLING ---
st.markdown("""
    <style>
        footer {visibility: hidden !important;}
        #MainMenu {visibility: hidden !important;}
        [data-testid="stSidebarNav"] {display: none !important;}
        [data-testid="stDecoration"] {display: none !important;}
        [data-testid="stToolbar"] {display: none !important;}
        header {background: transparent !important;}
        [data-testid="stHeader"] {background: transparent !important;}

        [data-testid="stSidebarCollapsedControl"],
        [data-testid="collapsedControl"],
        button[data-testid="stSidebarCollapseButton"] {
            display: flex !important;
            visibility: visible !important;
            position: fixed !important;
            top: 12px !important;
            left: 12px !important;
            z-index: 999999 !important;
            background-color: #00E5FF !important;
            color: #0d1117 !important;
            border-radius: 12px !important;
            border: 2px solid #00B4D8 !important;
            padding: 8px 14px !important;
            min-height: 48px !important;
            min-width: 48px !important;
            box-shadow: 0px 4px 18px rgba(0, 229, 255, 0.5) !important;
        }

        [data-testid="stSidebar"] {
            min-width: 390px !important;
            max-width: 390px !important;
            background-color: #0d1117 !important;
            border-right: 1px solid #30363d !important;
        }

        .stSelectbox label, .stRadio label, .stSlider label {
            font-size: 1.1rem !important;
            font-weight: 700 !important;
            color: #c9d1d9 !important;
        }

        .stButton button {
            min-height: 52px !important;
            font-size: 1.05rem !important;
            font-weight: 600 !important;
            border-radius: 8px !important;
        }

        [data-testid="stMetricValue"] {
            font-size: 2.2rem !important;
            font-weight: 800 !important;
            color: #00E5FF !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- 1. SECTOR MASTER REGISTRY WITH FORENSIC AUDIT EVIDENCE DOSSIERS ---
SECTORS = {
    "GRID_TX": {
        "name": "Transmission & Grid Infrastructure · Poles & Wires Book",
        "title": "Grid Infrastructure & Transmission Control Panel",
        "var_num": 3.80,
        "var_unit": "Billion",
        "drift_num": 245.00,
        "drift_unit": "Million",
        "acl_num": 3250000,
        "acl_unit": "/ wk",
        "bridge": "Telemetry traces parallel balance-sheet friction across high-voltage transformer staging, utility monopoly interconnection studies, and linear corridor land easements.",
        "presets": [
            "Synthesize 90-day FERC Order 2023 cluster re-study breach holding burn",
            "Model 500kV large power transformer staging and foundation lead-time drift",
            "Audit linear corridor parcel easement title verification backlogs"
        ],
        "sites": [
            {
                "Node": "Crystal River 500kV Hub",
                "Location": "Substation 08",
                "Tier": "Tier 3: Site Unit",
                "Layer": "Substation Physical Engineering",
                "Base_Drift": 7.5,
                "Base_Burn": 1450,
                "Bottleneck": "LPT Transformer Staging & Oil Immersion Audit",
                "Root_Cause": "Material / Supply Disruption",
                "Root_Detail": "Lead times expanded from 52 to 180 weeks; foundation pad curing completed without auxiliary power sync.",
                "Legacy_Delta": "+18.0 Wks (Pre-Digital Baseline: 28.5 Wks)",
                "Statutory_SLA": "IEEE 693 Seismic & NERC PRC-005 Compliance (30-Day Limit)",
                "SLA_Breach": "Active Breach (+45 Days beyond statutory window)",
                "Accrued_Loss": "$207,142 / day",
                "Evidence_Artifacts": [
                    "Factory Acceptance Testing (FAT) Certificate #FAT-500KV-9921",
                    "Oil Dielectric Breakdown ASTM D877 Test Log (Dated 14-Jul)",
                    "Civil Pad Concrete Curing & Grounding Grid Impedance Sign-off"
                ],
                "Clearance_Checklist": [
                    "Auto-verify oil dielectric assay against ASTM threshold (>30 kV).",
                    "Trigger automated auxiliary power loop test via remote SCADA node.",
                    "Execute energized clearance notice to Regional Transmission Operator."
                ],
                "SOP": [
                    ("Step 1: Digital Log Ingestion", "Ingest OEM factory test logs, oil dielectric assays, and transport vibration telemetry."),
                    ("Step 2: Automated Structural Validation", "Auto-match foundation curing curves and busbar clearances to IEEE standards."),
                    ("Step 3: Exception Engineering Gate", "Commissioning engineer clears auxiliary oil pumping and Nitrogen seal pressure."),
                    ("Step 4: Energization Dispatch", "Issue Final Substation Energization Clearance to RTO dispatcher.")
                ]
            },
            {
                "Node": "PJM Cluster 14 Gateway",
                "Location": "Valley Interconnect",
                "Tier": "Tier 2: Regional",
                "Layer": "Transmission Interconnection Directorate",
                "Base_Drift": 5.2,
                "Base_Burn": 1100,
                "Bottleneck": "FERC Order 2023 Network Cluster Re-Study Queue",
                "Root_Cause": "Process / Automation Gap",
                "Root_Detail": "Utility monopoly rerunning steady-state load flows manually due to upstream speculative dropouts.",
                "Legacy_Delta": "+14.5 Wks (Pre-Digital Baseline: 22.0 Wks)",
                "Statutory_SLA": "FERC Order 2023 60-Day Cluster Study Mandate",
                "SLA_Breach": "Statutory Breach (+58 Days beyond mandatory deadline)",
                "Accrued_Loss": "$157,142 / day",
                "Evidence_Artifacts": [
                    "Developer Phase 2 Study Request Payload (Hash: #0x9F4C2A)",
                    "RTO Cluster Restudy Notification Letter #PJM-2023-C14",
                    "Interconnection Study Restudy Queue Timestamp Log (Day 118 Active)"
                ],
                "Clearance_Checklist": [
                    "Inject pre-compiled Python AC/DC contingency power flow dataset.",
                    "Audit proportional network upgrade cost allocation against tariff table.",
                    "File statutory Section 206 non-compliance notice to enforce 24-hr sign-off."
                ],
                "SOP": [
                    ("Step 1: Single-Line Ingestion", "Ingest developer single-line diagrams, inverter specs, and reactive capability curves."),
                    ("Step 2: Automated Power-Flow Run", "Execute automated steady-state thermal and short-circuit contingency analysis."),
                    ("Step 3: Network Constraint Triage", "Lead transmission planner resolves thermal overload cost-share allocations."),
                    ("Step 4: ISA Agreement Execution", "Issue Interconnection Service Agreement (ISA) with binding construction milestones.")
                ]
            },
            {
                "Node": "Permian Corridor 345kV Link",
                "Location": "West Transmission Path",
                "Tier": "Tier 3: Site Unit",
                "Layer": "Linear Land & Right-of-Way Group",
                "Base_Drift": 3.4,
                "Base_Burn": 700,
                "Bottleneck": "Linear Parcel Easement & Title Clearance Backlog",
                "Root_Cause": "Labor / Credentialed Skill",
                "Root_Detail": "Shortage of certified land agents processing county deed searches and crossing permits.",
                "Legacy_Delta": "+8.0 Wks (Pre-Digital Baseline: 12.5 Wks)",
                "Statutory_SLA": "State Public Utility Commission Route Certificate SLA (90 Days)",
                "SLA_Breach": "Elevated Risk (+22 Days over internal schedule)",
                "Accrued_Loss": "$100,000 / day",
                "Evidence_Artifacts": [
                    "County Deed Registry Scans (Parcels 104 through 148)",
                    "State Highway Dept Encroachment Permit Request #TX-DOT-3301",
                    "Executed Landowner Option Deeds (42 of 45 cleared)"
                ],
                "Clearance_Checklist": [
                    "Auto-verify GIS polygon boundary continuity across corridor route.",
                    "Execute automated escrow payouts for 3 outstanding parcel options.",
                    "Dispatch binding Notice to Proceed (NTP) to transmission tower erection crew."
                ],
                "SOP": [
                    ("Step 1: Deed Scan Ingestion", "Ingest digital title registries, GIS boundary surveys, and crossing agreements."),
                    ("Step 2: GIS Spatial Auto-Check", "Auto-match right-of-way easement geometry against transmission centerlines."),
                    ("Step 3: Legal Waiver Clearance", "Assigned corporate counsel clears mineral rights and surface damage waivers."),
                    ("Step 4: Retainer Release & NTP", "Release escrow funds and issue Notice to Proceed (NTP) to line construction.")
                ]
            }
        ]
    },
    "ACC": {
        "name": "ACC Baseline · NZ Scheme Book",
        "title": "ACC Chairman & Board Control Panel",
        "var_num": 63.60,
        "var_unit": "Billion",
        "drift_num": 2556.00,
        "drift_unit": "Million",
        "acl_num": 1209000,
        "acl_unit": "/ wk",
        "bridge": "Synthesis isolates national scheme friction across regional claims verification queues, sequential dispute resolution lanes, and clinical pathway audits.",
        "presets": [
            "Evaluate 6-week claims backlog drift and medical review lag",
            "Synthesize Northern Hub clinical pathway audit friction",
            "Model 60-day dispute resolution escalation holding costs"
        ],
        "sites": [
            {
                "Node": "Northern Hub 01",
                "Location": "Auckland",
                "Tier": "Tier 2: Regional",
                "Layer": "Medical Review Directorate",
                "Base_Drift": 4.2,
                "Base_Burn": 320,
                "Bottleneck": "Manual Clinical Verification Queue",
                "Root_Cause": "Labor / Credentialed Skill",
                "Root_Detail": "Single-threaded medical officer dependency; GP diagnostic code re-keying.",
                "Legacy_Delta": "+7.0 Wks (Pre-Digital Baseline: 12.2 Wks)",
                "Statutory_SLA": "ACC Cover Decision Statutory SLA (21-Day Mandate)",
                "SLA_Breach": "Active Breach (+29 Days over statutory standard)",
                "Accrued_Loss": "$45,714 / day",
                "Evidence_Artifacts": [
                    "GP Electronic Lodgement Form ACC45 (#NZ-AKL-99238)",
                    "Clinical Specialist MRI Assessment Report (Scanned PDF)",
                    "ICD-10 Diagnostic Match Table (Pending Manual Sign-off)"
                ],
                "Clearance_Checklist": [
                    "Auto-validate ACC45 diagnostic code against pre-approved injury table.",
                    "Pre-clear initial 12 weeks of weekly compensation without human touch.",
                    "Route non-conforming diagnostic variance to Senior MRO within 2-hr SLA."
                ],
                "SOP": [
                    ("Step 1: Digital Ingestion", "Ingest GP digital lodgement, clinical assessment forms, and ICD-10 injury codes."),
                    ("Step 2: Automated Verification", "Auto-match diagnosis codes against standard rehabilitation clinical pathways."),
                    ("Step 3: Exception Triage", "Route non-standard treatment variances >$500 to Senior Medical Review Officers."),
                    ("Step 4: Ledger Dispatch", "Execute automated weekly compensation entitlement release to claimant account.")
                ]
            },
            {
                "Node": "Central Operations Hub",
                "Location": "Wellington",
                "Tier": "Tier 1: Central",
                "Layer": "Scheme Assurance & Governance",
                "Base_Drift": 5.2,
                "Base_Burn": 350,
                "Bottleneck": "Multi-Tier Entitlement Audit",
                "Root_Cause": "Process / Manual Friction",
                "Root_Detail": "Cumbersome dual-signature authorization thresholds on complex entitlement payouts.",
                "Legacy_Delta": "+9.0 Wks (Pre-Digital Baseline: 14.5 Wks)",
                "Statutory_SLA": "Public Finance Act Scheme Provisioning Mandate",
                "SLA_Breach": "Elevated Drift (+35 Days over governance baseline)",
                "Accrued_Loss": "$50,000 / day",
                "Evidence_Artifacts": [
                    "Longitudinal Weekly Compensation Ledger (#ACC-WGN-2024)",
                    "Actuarial Reserve Provisioning Model Validation Run #V4",
                    "Dual-Signature Approval Escalation Ticket #GOV-8812"
                ],
                "Clearance_Checklist": [
                    "Auto-reconcile claims payouts >52 weeks against actuarial tables.",
                    "Execute rule-based release for claims with zero liability delta.",
                    "Flag complex disputes to Assurance Committee with automated dossier."
                ],
                "SOP": [
                    ("Step 1: Payout Queue Audit", "Aggregate all longitudinal weekly compensation payouts exceeding 52 weeks."),
                    ("Step 2: Actuarial Cross-Check", "Auto-validate claim reserves against National Scheme actuarial tables."),
                    ("Step 3: Executive Governance Gate", "Triage high-liability claims to Scheme Assurance Committee for clearance."),
                    ("Step 4: Balance Sheet Update", "Discharge verified capital provisioning from unallocated reserve pool.")
                ]
            }
        ]
    },
    "PJM": {
        "name": "Grid PJM · Interconnection Book",
        "title": "PJM Grid Executive Control Panel",
        "var_num": 35.30,
        "var_unit": "Million",
        "drift_num": 17.68,
        "drift_unit": "Million",
        "acl_num": 340000,
        "acl_unit": "/ wk",
        "bridge": "Synthesis traces active interconnection drag across regional FERC re-study backlogs, substation construction lags, and sequential environmental clearance queues.",
        "presets": [
            "Synthesize 45-day FERC re-study queue delay exposure",
            "Audit Substation Alpha Tier-3 construction holding burn",
            "Evaluate 8-week environmental clearance sequential lag"
        ],
        "sites": [
            {
                "Node": "Substation Alpha",
                "Location": "Zone 4",
                "Tier": "Tier 3: Site Unit",
                "Layer": "Interconnection Engineering",
                "Base_Drift": 6.1,
                "Base_Burn": 150,
                "Bottleneck": "Manual FERC Re-Study Queue",
                "Root_Cause": "Process / Automation Gap",
                "Root_Detail": "Interconnection network models rerun manually on isolated transmission cluster changes.",
                "Legacy_Delta": "+11.0 Wks (Pre-Digital Baseline: 18.0 Wks)",
                "Statutory_SLA": "PJM Tariff Attachment O 60-Day Review Standard",
                "SLA_Breach": "Active Breach (+42 Days beyond tariff timeline)",
                "Accrued_Loss": "$21,428 / day",
                "Evidence_Artifacts": [
                    "RTO Model Ingestion Telemetry Packet #PJM-Z4-102",
                    "Transmission Cluster Sensitivity Matrix #C14-T",
                    "Interconnection Service Agreement Queue Log #ISA-991"
                ],
                "Clearance_Checklist": [
                    "Auto-run short-circuit contingency script across Zone 4 substations.",
                    "Verify developer cost-allocation formula against baseline tariff.",
                    "Dispatch binding clearance to PJM transmission engineering director."
                ],
                "SOP": [
                    ("Step 1: Cluster Request Ingestion", "Ingest developer single-line diagrams, turbine specs, and injection points."),
                    ("Step 2: Automated Load-Flow Run", "Execute automated AC/DC power flow and contingency thermal analysis."),
                    ("Step 3: Constraint Engineering", "Staff engineers resolve transmission overload constraints and network upgrades."),
                    ("Step 4: Interconnection Execution", "Issue finalized Interconnection Service Agreement (ISA) to utility.")
                ]
            }
        ]
    },
    "ERCOT": {
        "name": "ERCOT Energy · Storage Book",
        "title": "ERCOT Battery & Storage Control Panel",
        "var_num": 88.50,
        "var_unit": "Million",
        "drift_num": 12.30,
        "drift_unit": "Million",
        "acl_num": 610000,
        "acl_unit": "/ wk",
        "bridge": "Synthesis isolates grid battery holding costs across market telemetry synchronization, inverter testing queues, and land lease retainer audits.",
        "presets": [
            "Synthesize 45-day battery storage telemetry synchronization lag",
            "Audit South Region inverter capacity testing queue delay",
            "Model 4-week interconnection retainer sign-off holding burn"
        ],
        "sites": [
            {
                "Node": "BESS Storage Hub 01",
                "Location": "West Region",
                "Tier": "Tier 3: Site Unit",
                "Layer": "Telemetry Operations Group",
                "Base_Drift": 4.8,
                "Base_Burn": 320,
                "Bottleneck": "Telemetry Synchronization Validation",
                "Root_Cause": "Process / Automation Gap",
                "Root_Detail": "Manual calibration of SCADA telemetry latency buffers before market qualification.",
                "Legacy_Delta": "+8.0 Wks (Pre-Digital Baseline: 13.0 Wks)",
                "Statutory_SLA": "ERCOT Nodal Protocol 8.1.1 (Fast Frequency Response SLA)",
                "SLA_Breach": "Active Breach (+32 Days over qualification baseline)",
                "Accrued_Loss": "$45,714 / day",
                "Evidence_Artifacts": [
                    "4-Second ICCP Telemetry Ingestion Log #ERCOT-W-881",
                    "Inverter Dynamic Step-Response Benchmark (#IEEE-1547)",
                    "Substation RTU Gateway Synchronization Certificate"
                ],
                "Clearance_Checklist": [
                    "Auto-verify ICCP ping latency (<200ms threshold).",
                    "Execute remote synthetic frequency injection test.",
                    "Issue Commercial Operation Date (COD) activation packet to ERCOT desk."
                ],
                "SOP": [
                    ("Step 1: Point-to-Point Telemetry Ping", "Ingest 4-second SCADA state of charge, voltage, and reactive power feeds."),
                    ("Step 2: Automated Protocol Verification", "Auto-validate ICCP link stability and frequency response deadband accuracy."),
                    ("Step 3: Fault Injection Testing", "Field engineers audit system response during synthetic grid frequency excursions."),
                    ("Step 4: Market Commissioning", "Dispatch Commercial Operations Date (COD) market trading activation.")
                ]
            }
        ]
    },
    "BIOPHARMA": {
        "name": "Biopharma Clarity · GMP Book",
        "title": "Biopharma GMP Release Control Panel",
        "var_num": 142.00,
        "var_unit": "Million",
        "drift_num": 18.40,
        "drift_unit": "Million",
        "acl_num": 850000,
        "acl_unit": "/ wk",
        "bridge": "Synthesis traces batch release holding drag across cleanroom deviation audits, multi-facility QC validations, and final certificate sign-off backlogs.",
        "presets": [
            "Evaluate 30-day sterile suite deviation audit holding cost",
            "Synthesize formulation line QC environmental monitoring lag",
            "Audit 5-week batch release certificate queue friction"
        ],
        "sites": [
            {
                "Node": "Facility Alpha",
                "Location": "Sterile Suite A",
                "Tier": "Tier 3: Site Unit",
                "Layer": "Sterility Assurance Unit",
                "Base_Drift": 5.1,
                "Base_Burn": 450,
                "Bottleneck": "Manual Batch Record Re-Verification",
                "Root_Cause": "Process / Manual Friction",
                "Root_Detail": "Paper batch manufacturing records (BMR) re-audited manually for sterile signature gaps.",
                "Legacy_Delta": "+8.5 Wks (Pre-Digital Baseline: 14.0 Wks)",
                "Statutory_SLA": "FDA 21 CFR Part 11 & EU Annex 1 (14-Day Release SLA)",
                "SLA_Breach": "Critical Breach (+24 Days over standard batch window)",
                "Accrued_Loss": "$64,285 / day",
                "Evidence_Artifacts": [
                    "Electronic Batch Record BMR #BMR-BIO-4491",
                    "Continuous Particle Counter Telemetry Log (ISO 5 Suite)",
                    "Bioreactor Dissolved Oxygen Critical Parameter Trace"
                ],
                "Clearance_Checklist": [
                    "Auto-reconcile sensor telemetry against sterile tolerance bounds.",
                    "Clear minor non-critical excursions via pre-approved CAPA rules.",
                    "Route Batch Release Dossier to Qualified Person (QP) for digital release."
                ],
                "SOP": [
                    ("Step 1: Electronic BMR Ingestion", "Ingest bioreactor logs, CIP/SIP cycle records, and operator digital signatures."),
                    ("Step 2: Automated Critical Parameter Check", "Auto-flag out-of-spec pH, temperature, and dissolved oxygen deviations."),
                    ("Step 3: Deviation CAPA Resolution", "QA sterility specialist signs off root-cause investigations on minor excursions."),
                    ("Step 4: Batch Release Sign-off", "Quality Responsible Person (QP) issues commercial Batch Release Certificate.")
                ]
            }
        ]
    },
    "DEFENSE": {
        "name": "Defense & Aerospace · Sovereign Book",
        "title": "Defense Fleet & CapEx Control Panel",
        "var_num": 510.00,
        "var_unit": "Million",
        "drift_num": 42.10,
        "drift_unit": "Million",
        "acl_num": 2100000,
        "acl_unit": "/ wk",
        "bridge": "Synthesis isolates fleet operational drift across drydock overhaul queues, avionics flight clearance sign-offs, and critical component supply chain audits.",
        "presets": [
            "Synthesize 60-day naval drydock hull recertification backlog",
            "Audit depot west avionics subsystem retrofit delay exposure",
            "Model 8-week sovereign component line procurement drift"
        ],
        "sites": [
            {
                "Node": "Naval Yard Alpha",
                "Location": "Drydock 01",
                "Tier": "Tier 3: Site Unit",
                "Layer": "Structural Certification Group",
                "Base_Drift": 8.4,
                "Base_Burn": 1200,
                "Bottleneck": "Hull Structural Recertification Backlog",
                "Root_Cause": "Labor / Credentialed Skill",
                "Root_Detail": "Shortage of certified naval non-destructive testing (NDT) hull ultrasound inspectors.",
                "Legacy_Delta": "+14.0 Wks (Pre-Digital Baseline: 23.0 Wks)",
                "Statutory_SLA": "Naval Sea Systems Command Seaworthiness Standard NAVSEA-09",
                "SLA_Breach": "Critical Sovereign Breach (+56 Days over overhaul schedule)",
                "Accrued_Loss": "$171,428 / day",
                "Evidence_Artifacts": [
                    "NDT Ultrasound Hull Weld Scan Dataset #UW-NAV-01",
                    "Naval Architect Structural Computations Report",
                    "Drydock Berth 01 Demurrage Ledger (#NAV-DOCK-88)"
                ],
                "Clearance_Checklist": [
                    "Auto-verify ultrasound thickness scans against hull safety limits.",
                    "Dispatch localized plate weld repair work-orders to shipyard floor.",
                    "Issue unconditional Seaworthiness Certificate to Fleet Commander."
                ],
                "SOP": [
                    ("Step 1: NDT Ultrasound Ingestion", "Upload hull weld ultrasound scans, plate thickness maps, and corrosion logs."),
                    ("Step 2: Automated Stress Modeling", "Auto-simulate structural integrity under high-sea dynamic load states."),
                    ("Step 3: Naval Architect Sign-off", "Chief Naval Engineer resolves localized plate replacement work packets."),
                    ("Step 4: Drydock Flooding Release", "Issue structural seaworthiness certificate and clear drydock berth.")
                ]
            }
        ]
    },
    "APRA": {
        "name": "APRA Banking · Prudential Book",
        "title": "APRA Capital & Prudential Control Panel",
        "var_num": 1.20,
        "var_unit": "Billion",
        "drift_num": 95.00,
        "drift_unit": "Million",
        "acl_num": 4500000,
        "acl_unit": "/ wk",
        "bridge": "Synthesis tracks capital allocation drag across internal risk model validations, liquidity stress-testing re-keying, and regulatory audit cycles.",
        "presets": [
            "Synthesize 90-day internal rating model validation drag",
            "Model liquidity stress-testing re-keying holding costs",
            "Evaluate 6-week regulatory capital allocation stall"
        ],
        "sites": [
            {
                "Node": "Risk Modeling Hub Alpha",
                "Location": "Sydney",
                "Tier": "Tier 2: Regional",
                "Layer": "Prudential Risk Directorate",
                "Base_Drift": 6.2,
                "Base_Burn": 2500,
                "Bottleneck": "Internal Rating Model Validation Lag",
                "Root_Cause": "Process / Automation Gap",
                "Root_Detail": "Manual model back-testing re-keying across institutional loan portfolios.",
                "Legacy_Delta": "+10.5 Wks (Pre-Digital Baseline: 17.0 Wks)",
                "Statutory_SLA": "APRA Prudential Standard APS 113 / Basel III IRB SLA",
                "SLA_Breach": "Statutory Drift (+40 Days beyond quarterly reporting gate)",
                "Accrued_Loss": "$357,142 / day",
                "Evidence_Artifacts": [
                    "Internal Ratings-Based (IRB) Probability of Default Model Code",
                    "Monte Carlo Macroeconomic Shock Dataset (10,000 Iterations)",
                    "Prudential Capital Allocation Variance Sheet #APRA-RWA-24"
                ],
                "Clearance_Checklist": [
                    "Auto-run Python back-test against historical default curves.",
                    "Verify Risk-Weighted Asset (RWA) sensitivity within 1% tolerance.",
                    "Submit verified capital adequacy relief packet to APRA portal."
                ],
                "SOP": [
                    ("Step 1: Model Code Ingestion", "Upload internal ratings-based (IRB) probability of default (PD) algorithms."),
                    ("Step 2: Automated Stress Backtest", "Run automated Monte Carlo stress scenarios across macroeconomic shock curves."),
                    ("Step 3: Independent Validation Gate", "Chief Risk Officer signs off model parameter sensitivity reports."),
                    ("Step 4: APRA Submission Release", "Submit validated risk-weighted asset (RWA) calculations for capital relief.")
                ]
            }
        ]
    },
    "PORT": {
        "name": "Port Logistics · Freight Book",
        "title": "Port Logistics & Freight Control Panel",
        "var_num": 64.00,
        "var_unit": "Million",
        "drift_num": 8.20,
        "drift_unit": "Million",
        "acl_num": 410000,
        "acl_unit": "/ wk",
        "bridge": "Synthesis traces container dwell cost across automated terminal sync delays, customs manifest audits, and intermodal freight queue stalls.",
        "presets": [
            "Synthesize 21-day container terminal automated crane sync lag",
            "Audit inland port customs paper manifest queue holding burn",
            "Model 4-week intermodal rail transfer dwell escalation"
        ],
        "sites": [
            {
                "Node": "Container Terminal 01",
                "Location": "Pier 4",
                "Tier": "Tier 3: Site Unit",
                "Layer": "Crane Operations Group",
                "Base_Drift": 3.9,
                "Base_Burn": 250,
                "Bottleneck": "Automated Crane Sync Delay",
                "Root_Cause": "Process / Automation Gap",
                "Root_Detail": "TOS software mismatch between automated stacking cranes and vessel stowage plans.",
                "Legacy_Delta": "+6.0 Wks (Pre-Digital Baseline: 10.2 Wks)",
                "Statutory_SLA": "Terminal Operating Agreement 24-Hr Vessel Turnaround SLA",
                "SLA_Breach": "Active Breach (+18 Days container dwell inflation)",
                "Accrued_Loss": "$35,714 / day",
                "Evidence_Artifacts": [
                    "BAPLIE 2.2 Container Stowage EDI Feed #BAP-PIER4-88",
                    "Automated Stacking Crane (ASC) Exception Error Logs",
                    "Port Authority Vessel Demurrage Billing Notice"
                ],
                "Clearance_Checklist": [
                    "Auto-reconcile EDI container weights against crane load cells.",
                    "Trigger automated crane path optimization script to clear bottleneck stacks.",
                    "Dispatch digital gate passes to rail freight haulers."
                ],
                "SOP": [
                    ("Step 1: BAPLIE Stowage Ingestion", "Ingest vessel container placement EDI files and reefer temperature logs."),
                    ("Step 2: Automated Crane Path Optimizer", "Auto-calculate practical crane moves to minimize dwell time."),
                    ("Step 3: Terminal Supt Override", "Stevedore supervisor resolves physical container seal discrepancy alerts."),
                    ("Step 4: Intermodal Gate Release", "Dispatch automated gate barcodes to haulage trucks for immediate collection.")
                ]
            }
        ]
    },
    "NHS": {
        "name": "NHS Recovery · Surgical Book",
        "title": "NHS Elective Recovery Control Panel",
        "var_num": 210.00,
        "var_unit": "Million",
        "drift_num": 31.50,
        "drift_unit": "Million",
        "acl_num": 1150000,
        "acl_unit": "/ wk",
        "bridge": "Synthesis tracks elective backlog friction across pre-operative paperwork queues, operating theatre re-allocation delays, and post-op diagnostics sign-offs.",
        "presets": [
            "Synthesize 6-week pre-op assessment paperwork queue drift",
            "Audit regional theatre capacity re-allocation delay costs",
            "Model 45-day elective surgical elective recovery stall"
        ],
        "sites": [
            {
                "Node": "Surgical Hub North",
                "Location": "Trust Main",
                "Tier": "Tier 3: Site Unit",
                "Layer": "Clinical Assessment Team",
                "Base_Drift": 5.5,
                "Base_Burn": 650,
                "Bottleneck": "Pre-Op Assessment Paperwork Queue",
                "Root_Cause": "Labor / Credentialed Skill",
                "Root_Detail": "Pre-assessment nurse shortage requiring manual re-checking of paper cardiology clearance.",
                "Legacy_Delta": "+9.5 Wks (Pre-Digital Baseline: 15.0 Wks)",
                "Statutory_SLA": "NHS Constitution 18-Week Referral-to-Treatment (RTT) Mandate",
                "SLA_Breach": "Critical Statutory Breach (+38 Days over 18-week RTT target)",
                "Accrued_Loss": "$92,857 / day",
                "Evidence_Artifacts": [
                    "Patient Electronic Health Record (EHR) Lodgement #NHS-EHR-1092",
                    "ECG Diagnostic Cardiology Clearance PDF Document",
                    "Operating Theatre Unallocated Capacity Log #THEATRE-N4"
                ],
                "Clearance_Checklist": [
                    "Auto-calculate American Society of Anesthesiologists (ASA) operative score.",
                    "Match cleared patient file to nearest open theatre slot across Trust network.",
                    "Lock patient into operating schedule with zero cancellation risk."
                ],
                "SOP": [
                    ("Step 1: Patient Health Questionnaire Ingestion", "Digitally ingest patient comorbidities, drug charts, and GP records."),
                    ("Step 2: ASA Fitness Auto-Scoring", "Auto-calculate American Society of Anesthesiologists (ASA) operative risk score."),
                    ("Step 3: Anesthetic Consultant Review", "Consultant anesthesiologist reviews complex airway and cardiac flags."),
                    ("Step 4: Theatre Booking Confirmation", "Lock patient into confirmed operating theatre slot with zero day-of cancellation risk.")
                ]
            }
        ]
    }
}

# --- 2. URL PARAMETER ROUTING ---
params = st.query_params
url_co = params.get("co", "GRID_TX").upper()
if url_co not in SECTORS:
    url_co = "GRID_TX"

# --- 3. SIDEBAR CONTROL PLANE ---
st.sidebar.markdown(
    """
    <div style='padding-bottom: 10px;'>
        <h2 style='color: #00E5FF; font-size: 1.6rem; margin: 0; font-weight: 800;'>🎛️ CONTROL PLANE</h2>
        <p style='color: #3fb950; font-size: 0.9rem; font-weight: 700; margin: 4px 0 0 0;'>● Live Telemetry Active</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown("---")

selected_key = st.sidebar.selectbox(
    "🏢 Operating Sector Book",
    options=list(SECTORS.keys()),
    format_func=lambda x: SECTORS[x]["name"],
    index=list(SECTORS.keys()).index(url_co)
)

active_data = SECTORS[selected_key]

view_mode = st.sidebar.radio(
    "🏛️ Command Hierarchy",
    [
        "Tier 1: Master Command Post (Full Authority)",
        "Tier 2: Executive Board Glass (General Mgmt)",
        "Tier 3: Site Operations Hub (Regional & Field)"
    ],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.markdown("### ⚡ Live Drift Stress-Tester")

is_tier_1 = view_mode.startswith("Tier 1")
if is_tier_1:
    stress_lag = st.sidebar.slider("Simulate Friction Lag Escalation:", 0, 8, 0, format="+%d Wks")
else:
    st.sidebar.caption("🔒 Macro Stress Simulation Locked to Tier 1 Executive Authority.")
    stress_lag = st.sidebar.slider("Simulate Friction Lag Escalation (Locked):", 0, 8, 0, format="+%d Wks", disabled=True)

# --- 4. COMPUTED METRICS ---
multiplier = 1.0 + (stress_lag * 0.12)
display_var = f"${active_data['var_num'] * multiplier:.2f} {active_data['var_unit']}"
display_drift = f"${active_data['drift_num'] * multiplier:.2f} {active_data['drift_unit']}"
display_acl = f"${int(active_data['acl_num'] * multiplier):,} {active_data['acl_unit']}"

computed_sites = []
for site in active_data["sites"]:
    adjusted_drift = site["Base_Drift"] + stress_lag
    adjusted_burn = int(site["Base_Burn"] * multiplier)
    rag_badge = f"🔴 +{adjusted_drift:.1f} Wks (Critical)" if adjusted_drift >= 5.0 else f"🟡 +{adjusted_drift:.1f} Wks (Elevated)"

    computed_sites.append({
        "Operational Node": f"{site['Node']} ({site['Location']})",
        "Management Layer": f"{site['Tier']} · {site['Layer']}",
        "Root-Cause Driver": site["Root_Cause"],
        "Drift Status": rag_badge,
        "Weekly Burn Rate": f"${adjusted_burn}k / wk",
        "Active Bottleneck Queue": site["Bottleneck"]
    })

# --- 5. MAIN EXECUTIVE HEADER ---
st.markdown(
    f"""
    <div style='text-align: center; padding: 10px 0 20px 0;'>
        <h1 style='color: #00E5FF; font-size: 2.6rem; font-weight: 900; letter-spacing: -0.8px; margin: 0; line-height: 1.2;'>
            🎯 {active_data['title']}
        </h1>
    </div>
    """,
    unsafe_allow_html=True
)

# --- 6. STRATEGIC EXPOSURE METRICS ---
if view_mode.startswith("Tier 1") or view_mode.startswith("Tier 2"):
    st.markdown("---")
    st.subheader("⚡ Strategic Balance-Sheet Telemetry")
    col1, col2, col3 = st.columns(3)
    col1.metric("Macro Valuation at Risk 🔒", display_var, help="Total Enterprise Capital Exposure")
    col2.metric("Annual Velocity Drift Cost 🔒", display_drift, help="Financing Drag & Revenue Loss")
    col3.metric("Actionable Controllable Loss 🔒", display_acl, help="Active Administrative Holding Burn")
    st.info(f"⚡ **DIRECT OPERATIONAL BRIDGE:** {active_data['bridge']}")

# --- 7. OPERATIONAL MATRIX, FORENSIC DOSSIER & TIER 4 PLAYBOOKS ---
if view_mode.startswith("Tier 1") or view_mode.startswith("Tier 3"):
    st.markdown("---")
    with st.expander("🔓 Management Depth & Operational Site Queues (Tier 3 & Tier 4)", expanded=True):
        st.markdown("### 🔍 Granular Bottleneck & Root-Cause Matrix")
        st.table(computed_sites)
        
        st.markdown("---")
        st.markdown("### 📋 Forensic Audit Evidence Dossier & Tier 4 SOP Gates")
        st.caption("Select an active operational node to inspect statutory non-compliance evidence and actionable clearance checklists:")
        
        node_names = [f"{s['Node']} ({s['Location']})" for s in active_data["sites"]]
        selected_node_idx = st.selectbox("Select Node Architecture:", range(len(node_names)), format_func=lambda i: node_names[i])
        active_node = active_data["sites"][selected_node_idx]
        
        # FORENSIC EVIDENCE DOSSIER CARD
        st.markdown(
            f"""
            <div style='background: #161b22; border: 1px solid #30363d; border-left: 5px solid #ff4b4b; border-radius: 8px; padding: 18px; margin-bottom: 20px;'>
                <h4 style='color: #ff4b4b; margin: 0 0 10px 0;'>⚖️ FORENSIC AUDIT EVIDENCE DOSSIER · {active_node['Node']}</h4>
                <p style='color: #c9d1d9; font-size: 0.95rem; margin: 4px 0;'><strong>Statutory / Tariff Standard:</strong> {active_node['Statutory_SLA']}</p>
                <p style='color: #ff7b72; font-size: 0.95rem; margin: 4px 0;'><strong>Compliance Status:</strong> ⚠️ {active_node['SLA_Breach']}</p>
                <p style='color: #00E5FF; font-size: 0.95rem; margin: 4px 0;'><strong>Daily Accrued Holding Liability:</strong> {active_node['Accrued_Loss']}</p>
                <p style='color: #8b949e; font-size: 0.95rem; margin: 4px 0;'><strong>Root-Cause Classification:</strong> {active_node['Root_Cause']} ({active_node['Root_Detail']})</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        col_ev1, col_ev2 = st.columns(2)
        with col_ev1:
            st.markdown("#### 📂 Immutable Evidence Artifacts:")
            for artifact in active_node["Evidence_Artifacts"]:
                st.markdown(f"* `{artifact}`")
        with col_ev2:
            st.markdown("#### 🛠️ Frontline Clear-to-Close Checklist:")
            for task in active_node["Clearance_Checklist"]:
                st.markdown(f"* [ ] **{task}**")

        st.markdown("---")
        st.markdown("#### 🔄 4-Step Standard Operating Procedure (SOP) Clearance Gate:")
        for step_title, step_desc in active_node["SOP"]:
            st.markdown(f"* **{step_title}:** {step_desc}")

        st.markdown("")
        if st.button("⚡ Dispatch Immediate Operational Clearance Directive", use_container_width=True):
            st.balloons()
            st.success(f"Forensic Directive Dispatched: Statutory non-compliance packet served for {active_node['Node']}. Pre-clearing Steps 1 & 2 automated gates.")

# --- 8. DYNAMIC NOTEBOOK LANE ---
if view_mode.startswith("Tier 1") or view_mode.startswith("Tier 2"):
    st.markdown("---")
    with st.expander("🧠 Notebook Lane & Automated Executive Prompting Engine", expanded=True):
        st.markdown("### Automated Executive Scenario Prompts")
        if "current_query" not in st.session_state:
            st.session_state.current_query = active_data["presets"][0]

        chip_cols = st.columns(3)
        for idx, preset in enumerate(active_data["presets"]):
            with chip_cols[idx]:
                if st.button(f"⚡ Scenario {idx+1}:\n{preset}", key=f"chip_{selected_key}_{idx}", use_container_width=True):
                    st.session_state.current_query = preset

        user_query = st.text_input("Active Operational Query:", value=st.session_state.current_query)

        if user_query:
            days_match = re.search(r'(\d+)\s*(?:day|days)', user_query, re.IGNORECASE)
            weeks = float(days_match.group(1))/7.0 if days_match else 4.0
            time_str = f"{int(weeks*7)} Days ({weeks:.1f} Weeks)"

            calc_loss = weeks * (active_data['acl_num'] * multiplier)
            compound_drift_delta = (active_data['drift_num'] * multiplier) * (weeks * 0.12)
            critical_site = max(active_data["sites"], key=lambda x: x["Base_Drift"])

            st.markdown(
                f"""
                #### 📊 Predictive Synthesis for {active_data['name']}
                * **Active Scenario:** *"{user_query}"*
                * **Evaluated Delay Period:** **{time_str}**
                * **Cumulative Controllable Holding Loss:** **${calc_loss:,.2f}**
                * **Compounded Velocity Drift Escalation:** **+${compound_drift_delta:.2f} {active_data['drift_unit']}**
                * **Critical Constraint Layer:** **{critical_site['Tier']} · {critical_site['Layer']}** ({critical_site['Bottleneck']})
                * **Forensic Non-Compliance Status:** `{critical_site['SLA_Breach']}`
                
                > **Executive Directive:** Queue friction accumulates **${calc_loss:,.2f}** in balance-sheet drag over **{time_str}**. Discharging the **Forensic Clearance Directive** at **{critical_site['Node']}** collapses delay by serving non-compliance notices directly to the operator.
                """
            )

# --- 9. TOP-LOADED EXECUTIVE OUTREACH GENERATOR ---
st.markdown("---")
with st.expander("✉️ Generate Client Briefing & Executive Email (Top-Loaded Offer)", expanded=False):
    client_url = f"https://aatphoenix.streamlit.app/?co={selected_key}"
    email_memo = f"""Subject: Forensic Audit of Stranded Interconnection & Operational Holding Costs — {active_data['title']}

Hi [Executive First Name],

The Offer: We connect your stalled operational queues into an immutable forensic telemetry plane at zero upfront cost. We only charge a percentage of the verified balance-sheet holding capital we recover.

This command post demonstrates how real-time statutory SLA tracking and forensic evidence dossiers isolate administrative and utility delays:

👉 Direct Executive Surface: {client_url}

---

WHAT THIS FORENSIC PLATFORM PROVES IN 30 SECONDS:
• Stranded Valuation at Risk: ${active_data['var_num']:.2f} {active_data['var_unit']}
• Annual Velocity Drift Drag: ${active_data['drift_num']:.2f} {active_data['drift_unit']}
• Actionable Controllable Loss: ${int(active_data['acl_num']):,} {active_data['acl_unit']}
• Forensic Statutory Dossiers: Automatically logs statutory and tariff SLA breaches with exact daily accrued holding liabilities.

If you are open to recovering lost capital velocity across delayed operational queues without budget risk, let us know which operational node to calibrate first.

Best regards,

[Your Name]
AAT Phoenix Engine
"""
    st.text_area("Ready-to-send Executive Memo:", value=email_memo, height=420)

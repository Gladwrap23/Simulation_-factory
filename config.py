"""AATPHOENIX sector books - executive dashboard configuration."""

from __future__ import annotations

from typing import Any, TypedDict


class MetricCard(TypedDict, total=False):
    label: str
    big_value: str
    ground_truth_basis: str
    sequence_tag: str
    value_class: str
    border_accent: str


class SectorHeader(TypedDict):
    title: str
    statutory_meta: str
    subtitle: str


class OperationalBridge(TypedDict):
    section_caption: str
    banner_badge: str
    banner_title: str
    banner_headline: str
    banner_footer: str
    channel_receipts: list[dict[str, str]]


class SectorBook(TypedDict):
    code: str
    display_name: str
    header: SectorHeader
    operational_bridge: OperationalBridge
    bridge_metrics: list[MetricCard]
    portfolio_metrics: list[MetricCard]
    sidebar_caption: str
    critical_subjects: int


# Executive dark theme - CursorRules standard
EXECUTIVE_THEME: dict[str, str] = {
    "bg": "#0b0f17",
    "card": "#131d2a",
    "border": "#1e293b",
    "accent": "#2f81f7",
    "accent_soft": "rgba(47, 129, 247, 0.15)",
    "text": "#f8fafc",
    "muted": "#8b949e",
}

# Private Chrome Removal — hide Streamlit host chrome on iPad Board presentations
PRIVATE_CHROME: dict[str, Any] = {
    "enabled": True,
    "hide_header": True,
    "hide_share": True,
    "hide_hamburger": True,
    "hide_github_link": True,
    "hide_footer": True,
    "presentation_mode": "ipad_board_chair",
}


ACC_BASELINE: SectorBook = {
    "code": "ACC_BASELINE",
    "display_name": "ACC Baseline - NZ Scheme Book",
    "header": {
        "title": "NZ AAT SOVEREIGN ORCHESTRATION ENGINE",
        "statutory_meta": (
            "Statutory Governance: Answerable to Cabinet Minister "
            "(Executive Authority) | Crown Entity Act Compliance Mode"
        ),
        "subtitle": (
            "AAT Scheme Performance - Predictive Operational Risk and "
            "Long-Tail Claims Governance (NZD) - All-of-Government Integration"
        ),
    },
    "operational_bridge": {
        "section_caption": (
            "What / Where / When - Crown Agency Sync Surface - "
            "Health NZ / MSD / IRD / Ministerial"
        ),
        "banner_badge": "[MINISTERIAL WATCHLIST ACTIVE]",
        "banner_title": "Critical Pathway Drift - Statutory Escalation Surface",
        "banner_headline": (
            "{critical_subjects} Subjects breaching long-tail liability thresholds"
        ),
        "banner_footer": (
            "Crown Entity Act - Answerable to Minister for ACC - "
            "BIM / Statutory Escalation channel"
        ),
        "channel_receipts": [
            {
                "agency": "Health NZ",
                "status": "PROXIED / OPERATIONAL",
                "receipt": "Last harvest 10:15 AM - HNZ-MED-4402",
            },
            {
                "agency": "MSD",
                "status": "LIVE INTEGRATION",
                "receipt": "Last harvest 11:40 AM - MSD-AX-7710",
            },
            {
                "agency": "IRD",
                "status": "SECURE LIVE SYNC",
                "receipt": "Last harvest 11:42 AM - IRD-2026-99X4",
            },
            {
                "agency": "Ministerial",
                "status": "BLUE / ACTIVE",
                "receipt": "Last harvest 11:45 AM - CAB-BIM-2026-ACC",
            },
        ],
    },
    "bridge_metrics": [
        {
            "sequence_tag": "What",
            "label": "Health NZ Clinical Grid",
            "big_value": "Operational",
            "ground_truth_basis": "Orthopaedic records linked - HNZ-MED-4402",
            "value_class": "metric-value-green",
        },
        {
            "sequence_tag": "Where",
            "label": "MSD Workforce Pipeline",
            "big_value": "14 Matches",
            "ground_truth_basis": "Modified light-duty - MSD-AX-7710",
            "value_class": "metric-value-silver",
        },
        {
            "sequence_tag": "When",
            "label": "IRD Income Exchange",
            "big_value": "Live Sync",
            "ground_truth_basis": "12-month wage ledger - IRD-2026-99X4 - 11:42",
            "value_class": "metric-value-green",
        },
        {
            "sequence_tag": "Crown",
            "label": "Ministerial Cabinet Pipeline",
            "big_value": "Blue / Active",
            "ground_truth_basis": "BIM escalation - CAB-BIM-2026-ACC",
            "value_class": "metric-value-silver",
        },
    ],
    "portfolio_metrics": [
        {
            "label": "Total Scheme Claims",
            "big_value": "142 Active",
            "ground_truth_basis": "Regional Portfolio Intake",
            "value_class": "metric-value-silver",
        },
        {
            "label": "Critical Pathway Drift",
            "big_value": "18 Subjects",
            "ground_truth_basis": "Click to jump -> Audit View",
            "value_class": "metric-value-crimson",
        },
        {
            "label": "Performance Index",
            "big_value": "85.9%",
            "ground_truth_basis": "Baseline Trajectory Alignment",
            "value_class": "metric-value-green",
        },
        {
            "label": "Ministerial Expectations Match",
            "big_value": "88%",
            "ground_truth_basis": "Trajectory Alignment",
            "value_class": "metric-value-silver",
        },
    ],
    "sidebar_caption": (
        "Localized NZ ACC / IRD / MSD / Health NZ / Cabinet Minister AoG grids"
    ),
    "critical_subjects": 18,
}


GRID_PJM: SectorBook = {
    "code": "GRID_PJM",
    "display_name": "Grid PJM - Interconnection Book",
    "header": {
        "title": "PJM GRID ORCHESTRATION ENGINE",
        "statutory_meta": (
            "Regional Transmission Organization - FERC Compliance Mode | "
            "Independent Market Monitor Oversight"
        ),
        "subtitle": (
            "PJM Interconnection Performance - Congestion Risk and Long-Tail "
            "Capacity Governance (USD) - RTO Integration"
        ),
    },
    "operational_bridge": {
        "section_caption": (
            "What / Where / When - RTO Sync Surface - "
            "Generation / Transmission / Load / Market Ops"
        ),
        "banner_badge": "[CONGESTION WATCHLIST ACTIVE]",
        "banner_title": "Critical Congestion Drift - Market Escalation Surface",
        "banner_headline": (
            "{critical_subjects} Nodes breaching long-tail congestion thresholds"
        ),
        "banner_footer": (
            "FERC Order 2222 - Answerable to PJM Board - "
            "IMM / Market Escalation channel"
        ),
        "channel_receipts": [
            {
                "agency": "Generation",
                "status": "DISPATCHED / OPERATIONAL",
                "receipt": "Last LMP harvest 10:15 AM - GEN-PJM-4402",
            },
            {
                "agency": "Transmission",
                "status": "LIVE INTEGRATION",
                "receipt": "Last flow harvest 11:40 AM - TX-PJM-7710",
            },
            {
                "agency": "Load",
                "status": "SECURE LIVE SYNC",
                "receipt": "Last demand harvest 11:42 AM - LD-PJM-99X4",
            },
            {
                "agency": "Market Ops",
                "status": "BLUE / ACTIVE",
                "receipt": "Last auction harvest 11:45 AM - MKT-PJM-2026",
            },
        ],
    },
    "bridge_metrics": [
        {
            "sequence_tag": "What",
            "label": "Generation Dispatch Grid",
            "big_value": "Operational",
            "ground_truth_basis": "Unit commitments linked - GEN-PJM-4402",
            "value_class": "metric-value-green",
        },
        {
            "sequence_tag": "Where",
            "label": "Transmission Flow Pipeline",
            "big_value": "14 Constraints",
            "ground_truth_basis": "Binding limits - TX-PJM-7710",
            "value_class": "metric-value-silver",
        },
        {
            "sequence_tag": "When",
            "label": "Load Forecast Exchange",
            "big_value": "Live Sync",
            "ground_truth_basis": "Hourly demand curve - LD-PJM-99X4 - 11:42",
            "value_class": "metric-value-green",
        },
        {
            "sequence_tag": "Market",
            "label": "Market Operations Pipeline",
            "big_value": "Blue / Active",
            "ground_truth_basis": "LMP escalation - MKT-PJM-2026",
            "value_class": "metric-value-silver",
        },
    ],
    "portfolio_metrics": [
        {
            "label": "Total Interconnection Queue",
            "big_value": "312 Active",
            "ground_truth_basis": "Regional Queue Intake",
            "value_class": "metric-value-silver",
        },
        {
            "label": "Critical Congestion Drift",
            "big_value": "24 Nodes",
            "ground_truth_basis": "Click to jump -> Audit View",
            "value_class": "metric-value-crimson",
        },
        {
            "label": "Grid Performance Index",
            "big_value": "91.2%",
            "ground_truth_basis": "Baseline Reliability Alignment",
            "value_class": "metric-value-green",
        },
        {
            "label": "Board Expectations Match",
            "big_value": "86%",
            "ground_truth_basis": "Capacity Trajectory Alignment",
            "value_class": "metric-value-silver",
        },
    ],
    "sidebar_caption": (
        "Localized PJM / Generation / Transmission / Load / Market Ops RTO grids"
    ),
    "critical_subjects": 24,
}


BIOPHARMA_CLARITY: SectorBook = {
    "code": "BIOPHARMA_CLARITY",
    "display_name": "Biopharma Clarity - GMP Book",
    "header": {
        "title": "BIOPHARMA CLARITY ORCHESTRATION ENGINE",
        "statutory_meta": (
            "FDA / EMA GMP Compliance Mode | Quality Assurance Board Oversight"
        ),
        "subtitle": (
            "Biologics Manufacturing Performance - Batch Deviation Risk and "
            "Long-Tail Release Governance (USD) - CMC Integration"
        ),
    },
    "operational_bridge": {
        "section_caption": (
            "What / Where / When - CMC Sync Surface - "
            "Manufacturing / QC / Supply Chain / Regulatory"
        ),
        "banner_badge": "[DEVIATION WATCHLIST ACTIVE]",
        "banner_title": "Critical Batch Drift - Regulatory Escalation Surface",
        "banner_headline": (
            "{critical_subjects} Lots breaching long-tail release thresholds"
        ),
        "banner_footer": (
            "21 CFR Part 211 - Answerable to QA Board - "
            "CAPA / Regulatory Escalation channel"
        ),
        "channel_receipts": [
            {
                "agency": "Manufacturing",
                "status": "VALIDATED / OPERATIONAL",
                "receipt": "Last batch harvest 10:15 AM - MFG-BIO-4402",
            },
            {
                "agency": "QC Lab",
                "status": "LIVE INTEGRATION",
                "receipt": "Last assay harvest 11:40 AM - QC-BIO-7710",
            },
            {
                "agency": "Supply Chain",
                "status": "SECURE LIVE SYNC",
                "receipt": "Last cold-chain harvest 11:42 AM - SC-BIO-99X4",
            },
            {
                "agency": "Regulatory",
                "status": "BLUE / ACTIVE",
                "receipt": "Last submission harvest 11:45 AM - REG-BIO-2026",
            },
        ],
    },
    "bridge_metrics": [
        {
            "sequence_tag": "What",
            "label": "Manufacturing Execution Grid",
            "big_value": "Operational",
            "ground_truth_basis": "Batch records linked - MFG-BIO-4402",
            "value_class": "metric-value-green",
        },
        {
            "sequence_tag": "Where",
            "label": "QC Release Pipeline",
            "big_value": "9 Pending",
            "ground_truth_basis": "Assay queue - QC-BIO-7710",
            "value_class": "metric-value-silver",
        },
        {
            "sequence_tag": "When",
            "label": "Cold-Chain Exchange",
            "big_value": "Live Sync",
            "ground_truth_basis": "Temperature ledger - SC-BIO-99X4 - 11:42",
            "value_class": "metric-value-green",
        },
        {
            "sequence_tag": "Regulatory",
            "label": "Regulatory Submission Pipeline",
            "big_value": "Blue / Active",
            "ground_truth_basis": "CAPA escalation - REG-BIO-2026",
            "value_class": "metric-value-silver",
        },
    ],
    "portfolio_metrics": [
        {
            "label": "Total Active Lots",
            "big_value": "87 Active",
            "ground_truth_basis": "Manufacturing Portfolio Intake",
            "value_class": "metric-value-silver",
        },
        {
            "label": "Critical Batch Drift",
            "big_value": "11 Lots",
            "ground_truth_basis": "Click to jump -> Audit View",
            "value_class": "metric-value-crimson",
        },
        {
            "label": "Release Performance Index",
            "big_value": "94.1%",
            "ground_truth_basis": "Baseline GMP Alignment",
            "value_class": "metric-value-green",
        },
        {
            "label": "Board Expectations Match",
            "big_value": "92%",
            "ground_truth_basis": "CMC Trajectory Alignment",
            "value_class": "metric-value-silver",
        },
    ],
    "sidebar_caption": (
        "Localized Biopharma / Manufacturing / QC / Supply Chain / Regulatory grids"
    ),
    "critical_subjects": 11,
}


SECTOR_BOOKS: dict[str, SectorBook] = {
    "ACC_BASELINE": ACC_BASELINE,
    "GRID_PJM": GRID_PJM,
    "BIOPHARMA_CLARITY": BIOPHARMA_CLARITY,
}

DEFAULT_SECTOR_KEY = "ACC_BASELINE"


def get_sector_book(key: str) -> SectorBook:
    """Return sector book by key, falling back to ACC baseline."""
    if key in SECTOR_BOOKS:
        return SECTOR_BOOKS[key]
    return SECTOR_BOOKS[DEFAULT_SECTOR_KEY]


def sector_book_options() -> list[str]:
    """Ordered sector book keys for sidebar selectbox."""
    return list(SECTOR_BOOKS.keys())


# --- Kinetic Lab tenant config (University Operations Vault) ---


class ResearchNode(TypedDict):
    id: str
    label: str
    credit_cost: int
    short_name: str
    summary: str
    unlock_yield: str


class ThemeTokens(TypedDict):
    bg: str
    card: str
    border: str
    accent: str
    accent_soft: str
    text: str
    muted: str


TENANT_CONFIG: dict[str, Any] = {
    "target_domain": "UNIVERSITY INTERCOLLEGIATE ATHLETICS",
    "tenant_identity": "University Operations Vault",
    "active_sector_code": "SEC_01_KINETIC",
    "initial_credits": 450,
    "theme": {
        "bg_color": "bg-slate-950",
        "card_color": "bg-slate-900",
        "border_color": "border-slate-800",
        "accent_color": "emerald-500",
    },
    "research_nodes": [
        {
            "id": "node_1_1",
            "label": "Node 1.1: Dynamic Interface Shear Stress Mapping",
            "credit_cost": 5,
            "short_name": "Shear Stress Mapping",
            "summary": (
                "Map plantar and contact-surface shear vectors during cut, plant, "
                "and push-off so coaching staff can see where force leaks into the "
                "medial/lateral chain."
            ),
            "unlock_yield": (
                "Live shear heatmaps, peak medial shear (N), and cut-angle stress "
                "flags for practice and game-day readiness."
            ),
        },
        {
            "id": "node_1_2",
            "label": "Node 1.2: Pelvic Tilt and Deceleration Chain Asymmetry",
            "credit_cost": 8,
            "short_name": "Decel Chain Asymmetry",
            "summary": (
                "Quantify anterior/posterior pelvic tilt and left-right deceleration "
                "timing so soft-tissue load is attributed to the correct kinetic chain."
            ),
            "unlock_yield": (
                "Asymmetry index, pelvic tilt degrees, and braking-impulse imbalance "
                "for return-to-play and weekly load boards."
            ),
        },
        {
            "id": "node_1_3",
            "label": "Node 1.3: Cellular Longevity and Micro-Tear Chronology",
            "credit_cost": 12,
            "short_name": "Micro-Tear Chronology",
            "summary": (
                "Chronologize micro-tear accumulation against recovery windows so "
                "staff can separate productive overload from lingering tissue debt."
            ),
            "unlock_yield": (
                "Tissue debt score, projected clear-window (hrs), and cumulative "
                "micro-tear chronology across the training microcycle."
            ),
        },
    ],
}

THEME: ThemeTokens = {
    "bg": "#020617",
    "card": "#0f172a",
    "border": "#1e293b",
    "accent": "#10b981",
    "accent_soft": "rgba(16, 185, 129, 0.15)",
    "text": "#f8fafc",
    "muted": "#94a3b8",
}


def research_nodes() -> list[ResearchNode]:
    return list(TENANT_CONFIG["research_nodes"])


def node_by_id(node_id: str) -> ResearchNode | None:
    for node in research_nodes():
        if node["id"] == node_id:
            return node
    return None


def total_unlock_cost() -> int:
    return sum(int(n["credit_cost"]) for n in research_nodes())

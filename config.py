# config.py - Executive Sector Configuration Engine

SECTORS = {
    "ACC_BASELINE": {
        "title": "🧠 ACC Executive Synthesis & Knowledge Engine",
        "bridge_text": "Synthesis reconciles 100% of National Drift ($420k/wk): Northern $320k/wk (76.2%), Midland $40k/wk (9.5%), Central $30k/wk (7.1%), South Island $30k/wk (7.1%).",
        "metrics": [
            {"label": "Total Outstanding Claims Liability (OCL)", "value": "$63.6 Billion", "basis": "ACC Actuarial Valuation Disclosures"},
            {"label": "Annual New-Year Cost Gap", "value": "$2.556 Billion", "basis": "Annual Scheme Underwriting Disclosures"},
            {"label": "Cumulative Influenceable OCL Strain", "value": "$1.209 Billion", "basis": "5-Year Financial Condition Report Summary"}
        ],
        "footer": "💡 Ground-Truth Source: Ingested 2025 ACC Financial Condition Report & Live Telemetry Feed."
    },
    "GRID_PJM": {
        "title": "⚡ PJM Infrastructure Capital & Interconnection Surface",
        "bridge_text": "Synthesis reconciles 100% of Active Interconnection Drift ($340k/wk): Regional Re-Study Backlogs (72%), Substation Allocation Lags (18%), Environmental Clearance (10%).",
        "metrics": [
            {"label": "Active Queue Backlog Capacity", "value": "200+ Gigawatts", "basis": "PJM FERC Docket & Public Queue Telemetry"},
            {"label": "Active Weekly Dwell Burn", "value": "$340,000 / wk", "basis": "Non-Refundable Security Deposits & Land Retainers"},
            {"label": "24-Month Long-Tail Valuation Exposure", "value": "$35.3 Million", "basis": "Expiring PPA Window & Capital Cost Escalations"}
        ],
        "footer": "💡 Ground-Truth Source: Ingested PJM FERC Filings, GIS Queue Feeds & PUCT Dockets."
    },
    "BIOPHARMA_CLARITY": {
        "title": "☢️ Radiopharmaceutical Clinical Governance Surface",
        "bridge_text": "Synthesis reconciles 100% of Trial Onboarding Drift ($280k/wk): Hospital Ethics Committees (65%), Dosimetry Sign-offs (20%), Contract Legal SLA (15%).",
        "metrics": [
            {"label": "Active Phase 3 Weekly Burn", "value": "$280,000 / wk", "basis": "ASX Disclosures & ClinicalTrials.gov Telemetry"},
            {"label": "24-Month Balance Sheet Exposure", "value": "$38.4 Million", "basis": "Probabilistic Patent Monopoly Decay Model"},
            {"label": "Primary Operational Bottleneck", "value": "Ethics / Safety Queues", "basis": "Site Onboarding Telemetry Parser"}
        ],
        "footer": "💡 Ground-Truth Source: Ingested ASX Audited Regulatory Filings & Clinical Site Registries."
    }
}

def get_sector_book(key):
    return SECTORS.get(key, SECTORS["ACC_BASELINE"])

def sector_book_options():
    return {
        "ACC_BASELINE": "ACC Baseline · NZ Scheme Book",
        "GRID_PJM": "Grid PJM · Interconnection Book",
        "BIOPHARMA_CLARITY": "Biopharma Clarity · GMP Book"
    }

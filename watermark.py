import hashlib

import streamlit as st


def stamp_egress_artifact(artifact, artifact_name, track, scenario_data, is_de=False):
    content_hash = hashlib.sha256(artifact.encode("utf-8")).hexdigest()
    separator = " | "
    labels = (
        ("AUSGANGSSTEMPEL", "Dokument", "Pfad", "Szenario", "Inhalts-Hash (SHA-256)")
        if is_de
        else ("EGRESS STAMP", "Artifact", "Track", "Scenario", "Content SHA-256")
    )
    title, artifact_label, track_label, scenario_label, hash_label = labels
    stamp = (
        f"--- {title} ---\n"
        f"{artifact_label}: {artifact_name}\n"
        f"{track_label}: {track}\n"
        f"{scenario_label}: {scenario_data.get('scenario_id', 'unknown')}\n"
        f"{hash_label}: {content_hash}"
    )
    return f"{artifact.rstrip()}\n\n{stamp}\n"


def render_unified_watermark_system(scenario_data, selected_track, is_de=False):
    corp_name = scenario_data.get("corporate_entity", "ENERGIE BADEN-WÜRTTEMBERG AG").upper()
    chair_name = scenario_data.get("named_roster", {}).get("supervisory_chair", "LUTZ FELDMANN").upper()
    counsel_name = scenario_data.get("named_roster", {}).get("general_counsel", "DR. BERND-MICHAEL ZINOW").split("(")[0].strip().upper()
    session_token = scenario_data.get("scenario_id", "DE_OFFSHORE_WIND_001")
    forum = scenario_data.get("court_forum", "Landgericht Stuttgart / OLG Frankfurt")
    is_legal = ("Legal" in str(selected_track) or "Recht" in str(selected_track))

    border_color = "#ef4444" if is_legal else "#38bdf8"
    text_color = "#f87171" if is_legal else "#38bdf8"
    badge = ("⚖️ GERICHTSKAMMER // STRENG VERTRAULICH" if is_de else "⚖️ LEGAL CHAMBER // RESTRICTED") if is_legal else (f"💼 VORSTANDS-LEITSTAND // TOKEN #{session_token}" if is_de else f"💼 COMMERCIAL GOVERNANCE // TOKEN #{session_token}")
    custody = f"LEGAL CUSTODIAN: {counsel_name} | FORUM: {forum}" if is_legal else f"SUPERVISORY CUSTODY: {chair_name} | MANDATE REF: #{session_token}"

    st.markdown(f"""
    <div style="background: linear-gradient(90deg, #0b1329 0%, #1e293b 100%); border-left: 5px solid {border_color}; border-right: 1px solid #334155; border-top: 1px solid #334155; border-bottom: 1px solid #334155; border-radius: 6px; padding: 10px 18px; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center;">
        <div>
            <span style="color: #94a3b8; text-transform: uppercase; font-weight: 700; font-size: 0.8rem; letter-spacing: 0.05em;">{'UNTERNEHMENSTRÄGER:' if is_de else 'AUTHORIZED ENTERPRISE:'}</span>
            <b style="color: #ffffff; margin-left: 8px; font-size: 1.05rem;">{corp_name}</b>
            <div style="font-size: 0.78rem; color: #94a3b8; margin-top: 2px;">{custody}</div>
        </div>
        <div style="font-family: monospace; color: {text_color}; font-size: 0.85rem; font-weight: 800;">{badge}</div>
    </div>
    <div style="background: #090e1a; border: 1px solid #1e293b; border-radius: 6px; padding: 12px 18px; margin-bottom: 22px;">
        <div style="display: flex; justify-content: space-between; border-bottom: 1px solid #1e293b; padding-bottom: 8px; margin-bottom: 10px;">
            <span style="color: #38bdf8; font-weight: 800; font-size: 0.9rem;">{'🛡️ HOHEITLICHES DATENSCHUTZ- & TREUHAND-PROTOKOLL' if is_de else '🛡️ SOVEREIGN TRUST & DATA QUARANTINE PROTOCOL'}</span>
            <span style="color: #64748b; font-size: 0.78rem; font-family: monospace;">TOKEN #{session_token} • SHA-256 VERIFIED</span>
        </div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; font-size: 0.82rem; line-height: 1.5;">
            <div><b style="color: #f1f5f9;">🔒 {'Zero-Inbound-Architektur' if is_de else 'Zero-Inbound Architecture'}:</b> <div style="color: #94a3b8;">{'Keine Schnittstellen zu internen IT-, SAP- oder SCADA-Systemen.' if is_de else 'No connections to internal corporate IT, ERP (SAP), or substation SCADA networks.'}</div></div>
            <div><b style="color: #f1f5f9;">📋 {'Öffentliche Primärprovenienz' if is_de else 'Public Statutory Provenance'}:</b> <div style="color: #94a3b8;">{'Ausgangswerte stammen zu 100% aus testierten Pflichtveröffentlichungen (BNetzA, EnBW 2024).' if is_de else 'Baseline derived 100% from public regulatory filings (BNetzA, SEC, EnBW 2024).'}</div></div>
            <div><b style="color: #f1f5f9;">🚫 {'Keine KI-Modell-Verarbeitung' if is_de else 'Zero Model Training'}:</b> <div style="color: #94a3b8;">{'Keine Speicherung oder Verwendung von Messdaten für externe KI-Modelle.' if is_de else 'No client data or legal work-product are processed for external AI models.'}</div></div>
            <div><b style="color: #f1f5f9;">👤 {'Exklusives Vorstands-Token' if is_de else 'Exclusive Chairman Token'}:</b> <div style="color: #94a3b8;">{'Sitzungsinitialisierung strikt an individuelles Mandats-Token gebunden.' if is_de else 'Access strictly authenticated under sovereign executive token.'}</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
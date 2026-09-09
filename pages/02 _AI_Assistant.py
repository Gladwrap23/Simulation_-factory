from datetime import datetime, timezone
from html import escape

import streamlit as st


st.set_page_config(
    page_title="Factory AI Assistant",
    page_icon="AI",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown(
    """
    <style>
        :root {
            --bg-base: #0d1117;
            --bg-panel: #161b22;
            --bg-input: #1c242d;
            --line: #30363d;
            --cyan: #00E5FF;
            --green: #3fb950;
            --text-main: #f0f6fc;
            --text-muted: #8b949e;
        }
        .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
            background-color: var(--bg-base) !important;
            color: var(--text-main) !important;
        }
        section[data-testid="stSidebar"] {
            background-color: var(--bg-panel) !important;
            border-right: 1px solid var(--line);
        }
        section[data-testid="stSidebar"] * { color: var(--text-main) !important; }
        h1, h2, h3, h4, p, span, label, div { letter-spacing: 0; }
        h1, h2, h3, h4 { color: var(--text-main) !important; }
        .eyebrow {
            color: var(--cyan);
            font: 500 0.72rem monospace;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }
        .assistant-card {
            background: var(--bg-panel);
            border: 1px solid var(--line);
            border-left: 3px solid var(--cyan);
            border-radius: 6px;
            margin: 0.6rem 0;
            padding: 1rem;
        }
        .assistant-card.user { border-left-color: var(--green); }
        .assistant-label {
            color: var(--cyan);
            font: 500 0.7rem monospace;
            margin-bottom: 0.35rem;
            text-transform: uppercase;
        }
        .assistant-card.user .assistant-label { color: var(--green); }
        .context-card {
            background: var(--bg-panel);
            border: 1px solid var(--line);
            border-radius: 6px;
            padding: 1rem;
        }
        .context-value {
            color: var(--cyan);
            font: 700 1.45rem monospace;
            margin: 0.35rem 0;
        }
        .context-label { color: var(--text-muted); font-size: 0.78rem; }
        .stButton button {
            background: var(--bg-input);
            border: 1px solid var(--cyan);
            border-radius: 4px;
            color: var(--cyan);
            font-weight: 600;
        }
        div[data-baseweb="textarea"] > div,
        div[data-baseweb="input"] > div,
        textarea, input {
            background: var(--bg-input) !important;
            border-color: var(--line) !important;
            color: var(--text-main) !important;
        }
        [data-testid="stMetric"] {
            background: var(--bg-panel);
            border: 1px solid var(--line);
            border-top: 2px solid var(--cyan);
            padding: 0.75rem;
        }
        [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {
            color: var(--text-main) !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


if "assistant_messages" not in st.session_state:
    st.session_state["assistant_messages"] = [
        {
            "role": "assistant",
            "content": "Command link online. Ask about exposure, holding loss, or frontline sign-offs.",
        }
    ]


def get_signoffs(book=None):
    audit_records = st.session_state.get("audit_ledger", [])
    legacy_records = st.session_state.get("ledger", [])
    if book:
        legacy_records = [
            record for record in legacy_records
            if record.get("Operating Book") == book
        ]
    return audit_records, legacy_records


def get_book_context():
    return st.session_state.get(
        "selected_book_data",
        {"exposure": "$88.5M", "burn": 610000, "artifacts": []},
    )


def answer_question(question):
    normalized = question.lower()
    book = st.session_state.get("selected_book", "ERCOT BESS / storage operations")
    book_context = get_book_context()
    audit_records, legacy_records = get_signoffs(book)
    cleared_books = st.session_state.get("cleared_books", {})
    resolved = cleared_books.get(book, st.session_state.get("burn_resolved", st.session_state.get("cleared", False)))
    burn = "$0 / wk (RESOLVED)" if resolved else f"${book_context['burn']:,.0f} / wk"
    signoff_count = len(audit_records) + len(legacy_records)

    if any(term in normalized for term in ("exposure", "balance sheet", "88.5", "capital")):
        return f"Active balance sheet exposure for {book} is {book_context['exposure']}. The current board posture is monitoring the exposure against the approved operating ceiling."
    if any(term in normalized for term in ("burn", "holding loss", "holding", "loss", "610")):
        return f"Weekly holding loss for {book} is {burn}. The active realization split is 90% client value and 10% Phoenix fee."
    if any(term in normalized for term in ("audit", "ledger", "sign-off", "signoff", "clearance")):
        if signoff_count:
            latest = audit_records[-1] if audit_records else legacy_records[-1]
            event = latest.get("event", latest.get("Action", "Recorded sign-off"))
            return f"The audit chain contains {signoff_count} recorded event(s). Latest sign-off state: {event}. Frontline clearance is {'resolved' if resolved else 'still pending'}."
        return "No frontline sign-offs are recorded in this session. Tier 3 must complete all SOP checks before clearance can be written to the audit ledger."
    if any(term in normalized for term in ("status", "summary", "what do you know", "brief")):
        return f"Command summary for {book}: {book_context['exposure']} exposure, {burn} holding loss, and {signoff_count} audit record(s). Ask for exposure, burn, or sign-off detail for a focused readout."
    return f"I can answer questions about {book}'s active exposure, weekly holding loss, realization allocation, and audit ledger sign-offs."


with st.sidebar:
    st.markdown('<div class="eyebrow">FACTORY COMMAND POST</div>', unsafe_allow_html=True)
    st.title("AI ASSISTANT")
    st.caption("Conversational control-plane briefing")
    st.divider()
    st.markdown("**CONNECTED SOURCES**")
    st.success("Session state / LIVE")
    st.markdown("**AVAILABLE CONTEXT**")
    st.markdown("Exposure ledger\n\nHolding loss register\n\nFrontline sign-off chain")

st.title("Command Intelligence | Executive Advisory")

if "incident_store" in st.session_state and "active_incident_id" in st.session_state:
    active_incident = st.session_state.incident_store[
        st.session_state.active_incident_id
    ]
    director = active_incident["cognizant_director"]

    st.markdown(
        f"**Active Operational Channel:** `{st.session_state.active_incident_id}: "
        f"{active_incident['title']}`"
    )
    st.caption(
        f"Briefing Officer assigned to: **{director['name']}** - *{director['role']}*"
    )
    st.divider()

    col1, col2 = st.columns(2)
    if col1.button("Analyze Holding Carry vs LD Penalty", key="analyze_holding_carry"):
        st.chat_message("assistant").write(
            f"At the current carry rate of ${active_incident['burn_rate_sec']:.2f}/sec "
            f"(${active_incident['burn_rate_sec'] * 604800:,.0f}/wk), holding the site until "
            "next Thursday incurs $1.22M in idle contractor burn. If liquidated damages "
            "kick in at Day 10, total exposure increases by $45,000/day."
        )

    if col2.button("Review Elena vs. David Fiduciary Boundaries", key="review_fiduciary_boundaries"):
        st.chat_message("assistant").write(
            "Elena Rostova's refusal to sign without the IEEE packet is protected by standard "
            "duty of care. David Chen cannot submit the COD filing unilaterally without exposing "
            "the firm to regulatory false-filing penalties. Resolution requires a Tier 1 board-level "
            "indemnity carve-out."
        )
else:
    st.info("Nominal: Open the Incident Command Post to initialize telemetry.")

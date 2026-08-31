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

selected_book = st.session_state.get("selected_book", "ERCOT BESS / storage operations")
book_context = get_book_context()
st.markdown('<div class="eyebrow">EXECUTIVE SYNTHESIS / LIVE SESSION CONTEXT</div>', unsafe_allow_html=True)
st.title("Command intelligence, on demand.")
st.caption(f"A conversational assistant grounded in the active balance sheet and operational audit state for {selected_book}.")

exposure_col, burn_col, signoff_col = st.columns(3)
with exposure_col:
    st.markdown(f'<div class="context-card"><div class="context-label">ACTIVE BALANCE SHEET EXPOSURE</div><div class="context-value">{book_context["exposure"]}</div><div class="context-label">{escape(selected_book)}</div></div>', unsafe_allow_html=True)
with burn_col:
    cleared_books = st.session_state.get("cleared_books", {})
    resolved = cleared_books.get(selected_book, st.session_state.get("burn_resolved", st.session_state.get("cleared", False)))
    burn_value = "$0 / wk" if resolved else f"${book_context['burn']:,.0f} / wk"
    burn_note = "RESOLVED" if resolved else "ACTIVE HOLDING LOSS"
    st.markdown(f'<div class="context-card"><div class="context-label">WEEKLY HOLDING LOSS</div><div class="context-value">{burn_value}</div><div class="context-label">{burn_note}</div></div>', unsafe_allow_html=True)
with signoff_col:
    audit_records, legacy_records = get_signoffs(selected_book)
    st.markdown(f'<div class="context-card"><div class="context-label">AUDIT LEDGER SIGN-OFFS</div><div class="context-value">{len(audit_records) + len(legacy_records)}</div><div class="context-label">Cryptographically recorded events</div></div>', unsafe_allow_html=True)

st.divider()
st.subheader("Conversational Briefing")
for message in st.session_state["assistant_messages"]:
    role_label = "You" if message["role"] == "user" else "Factory AI"
    role_class = "user" if message["role"] == "user" else ""
    st.markdown(
        f'<div class="assistant-card {role_class}"><div class="assistant-label">{role_label}</div>{escape(message["content"])}</div>',
        unsafe_allow_html=True,
    )

prompt = st.chat_input("Ask about exposure, holding losses, or audit sign-offs")
if prompt:
    st.session_state["assistant_messages"].append({"role": "user", "content": prompt})
    st.session_state["assistant_messages"].append({"role": "assistant", "content": answer_question(prompt)})
    st.rerun()

st.divider()
st.caption(
    f"Session context refreshed {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')} | "
    "Directional scenario intelligence; verify decisions against the authoritative ledger."
)

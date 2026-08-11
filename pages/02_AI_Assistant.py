"""AI Assistant — Executive Audio Briefing & NotebookLM synthesis surface.

Hardening note: `default_query` is bound at module import time (empty string)
before any widget / sector logic can run, so the Query Intake text area cannot
raise NameError on Streamlit Cloud.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import streamlit as st

from config import get_sector_book, sector_book_options
from surface_nav import render_sidebar_surface_links, render_surface_page_links

# ---------------------------------------------------------------------------
# NameError shield: bind before any widget / sector logic can run.
# ---------------------------------------------------------------------------
default_query = ""

GEMINI_NOTEBOOK_URL = "https://colab.research.google.com/"
BRIEFING_AUDIO_PATH = Path(__file__).resolve().parent.parent / "public" / "briefing.mp3"
QUERY_INPUT_KEY = "ai_assistant_query_input"
DEFAULT_QUERY_KEY = "ai_assistant_default_query"
LAST_SECTOR_KEY = "ai_assistant_last_sector"

st.set_page_config(
    layout="wide",
    page_title="AI Assistant",
    page_icon="⬡",
    initial_sidebar_state="expanded",
)

# -----------------------------------------------------------------------------
# TOTAL STEALTH CSS OVERRIDE (hide Manage app, header, footer & badges)
# -----------------------------------------------------------------------------
st.markdown(
    """
    <style>
    /* Absolute Hide for Streamlit Host Chrome, Header, Footer, Watermarks & Manage App Badge */
    header, footer, #MainMenu, .stDeployButton,
    [data-testid="stHeader"],
    [data-testid="stToolbar"],
    [data-testid="stDecoration"],
    [data-testid="stStatusWidget"],
    [data-testid="stAppDeployButton"],
    [data-testid="stSidebarNav"],
    [data-testid="manage-app-button"],
    .viewerBadge_container__1A53K,
    div[class*="viewerBadge"],
    div[class*="styles_viewerBadge"],
    button[title*="Manage app"],
    div[data-testid="stAppViewBlockContainer"] > header {
        visibility: hidden !important;
        display: none !important;
        height: 0px !important;
    }

    .stApp {
        background-color: #0b0f17;
        color: #e6edf3;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def _sector_label(key: str) -> str:
    options = sector_book_options()
    return str(options.get(key, key))


def _ensure_default_query(sector_code: str) -> str:
    """Return a safe string default query; always defined, never None."""
    if DEFAULT_QUERY_KEY not in st.session_state:
        st.session_state[DEFAULT_QUERY_KEY] = ""
    if LAST_SECTOR_KEY not in st.session_state:
        st.session_state[LAST_SECTOR_KEY] = sector_code

    if st.session_state[LAST_SECTOR_KEY] != sector_code:
        st.session_state[LAST_SECTOR_KEY] = sector_code
        st.session_state[DEFAULT_QUERY_KEY] = (
            f"Summarize Structural Mirror KPIs and Layer 2 drift for {sector_code}."
        )

    raw = st.session_state.get(DEFAULT_QUERY_KEY, "")
    if raw is None:
        raw = ""
    return str(raw)


options = sector_book_options()

with st.sidebar:
    render_sidebar_surface_links(active="ai_assistant")
    st.markdown("---")
    st.markdown("### AI ASSISTANT")
    sector_key = st.selectbox(
        "Active Sector Book",
        options=list(options.keys()),
        format_func=_sector_label,
        key="ai_assistant_sector_book",
    )
    sector = get_sector_book(sector_key)
    st.caption(str(sector.get("footer", "")))

sector_code = str(sector_key)
# Refresh module-level default_query from session before any widget uses it.
default_query = _ensure_default_query(sector_code)

metrics = list(sector.get("metrics", []))
layer2_ops = list(sector.get("layer2_operations", []))

render_surface_page_links(active="ai_assistant", compact=True)

st.title(str(sector.get("title", "Statutory Baseline Knowledge Base")))
st.caption("Public Disclosures · Structural Mirror / Layer 2 aware")
st.markdown(
    f"<p style='color:#8b949e; margin-top:-0.2rem;'>"
    f"Executive query console · {_sector_label(sector_key)}</p>",
    unsafe_allow_html=True,
)

if metrics:
    cols = st.columns(min(len(metrics), 3))
    for col, card_cfg in zip(cols, metrics):
        with col:
            st.metric(
                str(card_cfg.get("label", "KPI")),
                str(card_cfg.get("value", "-")),
                help=str(card_cfg.get("basis", "")),
            )

st.markdown("---")
st.subheader("Executive Audio Briefing & Synthesis Surface")

if BRIEFING_AUDIO_PATH.is_file():
    st.audio(str(BRIEFING_AUDIO_PATH), format="audio/mp3")
else:
    st.caption("Audio briefing missing (`public/briefing.mp3`).")

tab_synth, tab_query = st.tabs(
    ["NotebookLM Knowledge Synthesis", "Query Intake"],
)

with tab_synth:
    st.markdown(
        """
        <div style="background:#131d2a; border:1px solid #1e293b; border-left:3px solid #2f81f7;
                    padding:0.85rem 1rem; margin-bottom:0.85rem;">
          <div style="font-family:IBM Plex Mono,monospace; font-size:0.72rem; color:#2f81f7;
                      letter-spacing:0.08em; text-transform:uppercase; font-weight:700;">
            NotebookLM Knowledge Synthesis
          </div>
          <div style="color:#e2e8f0; font-size:0.9rem; margin-top:0.35rem;">
            Ground the briefing against Structural Mirror KPIs, then open the live
            Gemini Notebook Manifest for role-dynamic synthesis.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.link_button(
        "Open Live Gemini Notebook Manifest",
        GEMINI_NOTEBOOK_URL,
        use_container_width=True,
    )
    st.caption(
        "Notebook hosts typically block iframe embeds — use the button above "
        "to open the live Gemini Notebook Manifest in a new tab."
    )

with tab_query:
    st.markdown(
        """
        <div style="background:#131d2a; border:1px solid #1e293b; border-left:3px solid #2f81f7;
                    padding:0.85rem 1rem; margin-bottom:0.85rem;">
          <div style="font-family:IBM Plex Mono,monospace; font-size:0.72rem; color:#2f81f7;
                      letter-spacing:0.08em; text-transform:uppercase; font-weight:700;">
            Query Intake
          </div>
          <div style="color:#e2e8f0; font-size:0.9rem; margin-top:0.35rem;">
            Ask for Macro Valuation, Velocity Friction, Actionable Controllable Loss,
            or Layer 2 site/queue drift clearances.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Session-state owns the widget value — do NOT pass value=default_query.
    if QUERY_INPUT_KEY not in st.session_state:
        st.session_state[QUERY_INPUT_KEY] = default_query or ""

    user_query = st.text_area(
        "Executive query",
        height=120,
        key=QUERY_INPUT_KEY,
        placeholder="e.g., Where is actionable controllable loss concentrated?",
    )

    c1, c2 = st.columns([1, 1])
    with c1:
        run_query = st.button(
            "Run Assistant Brief",
            type="primary",
            use_container_width=True,
        )
    with c2:
        if st.button("Reset Query", use_container_width=True):
            st.session_state[DEFAULT_QUERY_KEY] = ""
            st.session_state[QUERY_INPUT_KEY] = ""
            st.rerun()

    # Persist typed text so subsequent runs stay NameError-safe.
    if user_query is not None:
        st.session_state[DEFAULT_QUERY_KEY] = str(user_query)
        default_query = str(user_query)

    if run_query:
        prompt = str(user_query or default_query or "").strip()
        if not prompt:
            st.warning("Enter a query before running the assistant brief.")
        else:
            ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")

            st.markdown("### Assistant Brief")
            st.caption(f"Generated {ts} · sector {sector_code}")

            if metrics:
                mcols = st.columns(min(len(metrics), 3))
                for col, card_cfg in zip(mcols, metrics):
                    with col:
                        st.metric(
                            str(card_cfg.get("label", "KPI")),
                            str(card_cfg.get("value", "-")),
                            help=str(card_cfg.get("basis", "")),
                        )

            st.markdown("#### Response")
            st.write(
                f"Interpreted query against **{_sector_label(sector_key)}**. "
                f"Prompt: _{prompt}_"
            )
            if layer2_ops:
                top = layer2_ops[0]
                st.info(
                    f"Layer 2 hotspot: {top.get('site', 'Site')} · "
                    f"drift {top.get('drift', '-')} · burn {top.get('burn', '-')} · "
                    f"{top.get('bottleneck', '')}"
                )
                if st.button(
                    "Trigger Layer 3 Actionable Clearance",
                    key="ai_assistant_layer3",
                    use_container_width=True,
                ):
                    st.success(
                        f"Layer 3 Actionable Clearance staged for {sector_code}."
                    )
            else:
                st.write(
                    "No Layer 2 site/queue metrics are configured for this sector book."
                )

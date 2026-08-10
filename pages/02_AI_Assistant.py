"""AI Assistant — sector-aware executive query surface."""

from __future__ import annotations

from datetime import datetime, timezone

import streamlit as st

from config import (
    EXECUTIVE_THEME,
    PRIVATE_CHROME,
    get_sector_book,
    sector_book_options,
)

st.set_page_config(
    layout="wide",
    page_title="AI Assistant",
    page_icon="⬡",
    initial_sidebar_state="expanded",
)

# Private Chrome Removal (match main app iPad Board presentation mode)
if PRIVATE_CHROME.get("enabled", True):
    st.markdown(
        """
        <style>
        #MainMenu,
        header[data-testid="stHeader"],
        [data-testid="stToolbar"],
        [data-testid="stDecoration"],
        [data-testid="stAppDeployButton"],
        [data-testid="stDeployButton"],
        [data-testid="stSidebarCollapsedControl"],
        [data-testid="collapsedControl"],
        footer,
        .stDeployButton {
          display: none !important;
          visibility: hidden !important;
          height: 0 !important;
          opacity: 0 !important;
          pointer-events: none !important;
        }
        .stApp {
          background-color: #0b0f17;
          color: #f8fafc;
          font-family: "IBM Plex Sans", sans-serif;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _sector_label(key: str) -> str:
    return str(get_sector_book(key).get("display_name", key))


def _ensure_default_query(sector_code: str) -> str:
    """Safely initialize default_query from session state (never NameError)."""
    if "ai_assistant_default_query" not in st.session_state:
        st.session_state.ai_assistant_default_query = ""
    if "ai_assistant_last_sector" not in st.session_state:
        st.session_state.ai_assistant_last_sector = sector_code

    # Reset placeholder prompt when the active sector book changes.
    if st.session_state.ai_assistant_last_sector != sector_code:
        st.session_state.ai_assistant_last_sector = sector_code
        st.session_state.ai_assistant_default_query = (
            f"Summarize Structural Mirror KPIs and Layer 2 drift for {sector_code}."
        )

    raw = st.session_state.get("ai_assistant_default_query", "")
    if raw is None:
        raw = ""
    default_query = str(raw)
    st.session_state.ai_assistant_default_query = default_query
    return default_query


with st.sidebar:
    st.markdown("### AI ASSISTANT")
    sector_key = st.selectbox(
        "Active Sector Book",
        options=sector_book_options(),
        format_func=_sector_label,
        key="ai_assistant_sector_book",
    )
    sector = get_sector_book(sector_key)
    st.caption(str(sector.get("sidebar_caption", "")))

# Safe initialization BEFORE any widget uses default_query
default_query = _ensure_default_query(str(sector.get("code", sector_key)))

accent = EXECUTIVE_THEME["accent"]
muted = EXECUTIVE_THEME["muted"]
card = EXECUTIVE_THEME["card"]

st.title("AI Assistant")
st.markdown(
    f"<p style='color:{muted}; margin-top:-0.4rem;'>"
    f"Executive query console · {sector.get('display_name', sector_key)} · "
    "Structural Mirror / Layer 2 aware</p>",
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div style="background:{card}; border:1px solid #1e293b; border-left:3px solid {accent};
                padding:0.85rem 1rem; margin-bottom:0.85rem;">
      <div style="font-family:IBM Plex Mono,monospace; font-size:0.72rem; color:{accent};
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

# Line ~108 region: widget must receive an always-defined default_query
user_query = st.text_area(
    "Executive query",
    value=default_query,
    height=120,
    key="ai_assistant_query_input",
    placeholder="e.g., Where is actionable controllable loss concentrated?",
)

c1, c2 = st.columns([1, 1])
with c1:
    run_query = st.button("Run Assistant Brief", type="primary", use_container_width=True)
with c2:
    if st.button("Reset Query", use_container_width=True):
        st.session_state.ai_assistant_default_query = ""
        st.session_state.ai_assistant_query_input = ""
        st.rerun()

# Persist the latest typed query so reloads stay safe.
if user_query is not None:
    st.session_state.ai_assistant_default_query = str(user_query)

if run_query:
    prompt = str(user_query or default_query or "").strip()
    if not prompt:
        st.warning("Enter a query before running the assistant brief.")
    else:
        mirror = list(sector.get("structural_mirror", []))
        layer2 = dict(sector.get("layer2_operations", {}))
        sites = list(layer2.get("site_queue_metrics", []))
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")

        st.markdown("### Assistant Brief")
        st.caption(f"Generated {ts} · sector {sector.get('code', sector_key)}")

        if mirror:
            mcols = st.columns(min(len(mirror), 3))
            for col, card_cfg in zip(mcols, mirror):
                with col:
                    st.metric(
                        str(card_cfg.get("label", "KPI")),
                        str(card_cfg.get("big_value", "-")),
                        help=str(card_cfg.get("ground_truth_basis", "")),
                    )

        st.markdown("#### Response")
        st.write(
            f"Interpreted query against **{sector.get('display_name', sector_key)}**. "
            f"Prompt: _{prompt}_"
        )
        if sites:
            top = sites[0]
            st.info(
                f"Layer 2 hotspot: {top.get('site', 'Site')} / {top.get('queue', 'Queue')} · "
                f"burn {top.get('burn', '-')} · delay {top.get('delay_days', '-')} · "
                f"{top.get('ground_truth_basis', '')}"
            )
            if st.button(
                str(
                    layer2.get(
                        "layer3_action_label",
                        "Trigger Layer 3 Actionable Clearance",
                    )
                ),
                key="ai_assistant_layer3",
                use_container_width=True,
            ):
                st.success(
                    str(
                        layer2.get(
                            "layer3_clearance_receipt",
                            "Layer 3 Actionable Clearance staged.",
                        )
                    )
                )
        else:
            st.write("No Layer 2 site/queue metrics are configured for this sector book.")

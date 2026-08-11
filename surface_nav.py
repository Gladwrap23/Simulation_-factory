"""Shared Streamlit in-app command-level navigation.

The command surface is a single entrypoint (`app.py`). The multipage `pages/`
directory was removed, so navigation stays within Executive Command via
COMMAND LEVELS (Layer 1/2/3 and Interface A/B) rather than `st.page_link`
targets to separate Streamlit pages.
"""

from __future__ import annotations

from typing import Literal

import streamlit as st

SurfaceKey = Literal["home"]

# Single-file surface — paths relative to the app root (`streamlit run app.py`).
SURFACE_PAGES: tuple[dict[str, str], ...] = (
    {
        "key": "home",
        "path": "app.py",
        "label": "Executive Command",
        "hint": "Home · Structural Mirror · Interface A/B",
    },
)

COMMAND_LEVELS: tuple[dict[str, str], ...] = (
    {
        "key": "layer1",
        "label": "Layer 1 · Structural Mirror",
        "hint": "3 KPI cards (Macro · Velocity · Controllable Loss)",
    },
    {
        "key": "layer2",
        "label": "Layer 2 · Operations View",
        "hint": "Site / queue drift drill-down",
    },
    {
        "key": "layer3",
        "label": "Layer 3 · Actionable Clearance",
        "hint": "Clearance trigger on Layer 2 hotspot",
    },
    {
        "key": "interface_a",
        "label": "Interface A · Global Portfolio",
        "hint": "Scheme-wide ledger and cohort pads",
    },
    {
        "key": "interface_b",
        "label": "Interface B · Claim Drill-down",
        "hint": "Individual dossier + alignment vector",
    },
)


def render_surface_page_links(*, active: SurfaceKey = "home", compact: bool = False) -> None:
    """Render the single-surface marker (no multipage links)."""
    st.markdown(
        "<div class='ipad-top-nav' role='navigation' aria-label='App surfaces'>"
        "<span class='nav-mark'>SURFACES</span>"
        "<span class='nav-hint'>Executive Command · in-app levels only</span>"
        "</div>",
        unsafe_allow_html=True,
    )
    home = SURFACE_PAGES[0]
    label = f"● {home['label']}" if active == home["key"] else home["label"]
    st.markdown(f"**{label}**")
    if not compact:
        st.caption(home["hint"])


def render_sidebar_surface_links(*, active: SurfaceKey = "home") -> None:
    """Sidebar twin — single Executive Command surface, no multipage links."""
    st.markdown("### APP SURFACES")
    home = SURFACE_PAGES[0]
    label = f"● {home['label']}" if active == home["key"] else home["label"]
    st.markdown(label)
    st.caption("All navigation stays on Executive Command (`app.py`).")


def render_command_level_controls(*, sector_code: str, global_view_label: str) -> str:
    """Expose Layer 1/2/3 and Interface A/B as an explicit control strip.

    Returns the selected command-level key.
    """
    st.markdown("### COMMAND LEVELS")
    st.caption(
        "Structural Mirror and Interface layers live on Executive Command — "
        "they are not separate Streamlit pages."
    )

    level_labels = [item["label"] for item in COMMAND_LEVELS]
    label_to_key = {item["label"]: item["key"] for item in COMMAND_LEVELS}
    default_label = level_labels[0]
    current_key = st.session_state.get("command_level_focus", "layer1")
    for item in COMMAND_LEVELS:
        if item["key"] == current_key:
            default_label = item["label"]
            break

    selected_label = st.radio(
        "Active command level",
        options=level_labels,
        index=level_labels.index(default_label),
        horizontal=True,
        key="command_level_radio",
        help="Jump between Structural Mirror layers and Interface A/B.",
    )
    selected_key = label_to_key[selected_label]
    st.session_state["command_level_focus"] = selected_key

    hint = next(
        (item["hint"] for item in COMMAND_LEVELS if item["key"] == selected_key),
        "",
    )
    st.caption(hint)

    # Wire level selection into existing session flags used by the dashboard.
    layer2_flag = f"layer2_open_{sector_code}"
    layer2_toggle = f"layer2_toggle_{sector_code}"
    if selected_key in {"layer1", "layer2", "layer3"}:
        # Structural Mirror layers only render on Interface A (global portfolio).
        st.session_state["audit_view_selection"] = global_view_label
        st.session_state["cohort_mode"] = False
        if selected_key in {"layer2", "layer3"}:
            st.session_state[layer2_flag] = True
            st.session_state[layer2_toggle] = True
        else:
            st.session_state[layer2_flag] = False
            st.session_state[layer2_toggle] = False

    if selected_key == "interface_a":
        st.session_state["audit_view_selection"] = global_view_label
        st.session_state["cohort_mode"] = False
        st.session_state[layer2_flag] = False
        st.session_state[layer2_toggle] = False
    elif selected_key == "interface_b":
        # Prefer an existing claim selection; otherwise seed the first known token.
        current = st.session_state.get("audit_view_selection", global_view_label)
        if current == global_view_label:
            st.session_state["audit_view_selection"] = "AAT-Claimant-Delta-2026"

    return selected_key

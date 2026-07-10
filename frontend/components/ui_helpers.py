"""Shared UI helpers."""

from datetime import datetime

import streamlit as st
from pathlib import Path


def load_css() -> None:
    css_path = Path(__file__).parent.parent / "styles" / "custom.css"
    with open(css_path, encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def render_header() -> None:
    now = datetime.now().strftime("%a %H:%M:%S")
    st.markdown(
        f"""
        <div class="app-header">
            <h1 class="app-title">Automatic <span>Biryani Maker</span></h1>
            <div class="app-clock">{now}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_step_indicator(current_step: int) -> None:
    """
    Render a 3-step workflow indicator.
    current_step: 0 = ingredients, 1 = cooking, 2 = complete
    """
    steps = ["Ingredients", "Cooking", "Done"]

    parts = ['<div class="step-indicator">']
    for i, label in enumerate(steps):
        if i < current_step:
            circle_cls = "step-circle done"
            label_cls = "step-label done"
            content = "✓"
        elif i == current_step:
            circle_cls = "step-circle active"
            label_cls = "step-label active"
            content = str(i + 1)
        else:
            circle_cls = "step-circle"
            label_cls = "step-label"
            content = str(i + 1)

        parts.append(
            f'<div class="step-item">'
            f'<div class="{circle_cls}">{content}</div>'
            f'<div class="{label_cls}">{label}</div>'
            f'</div>'
        )

        if i < len(steps) - 1:
            conn_cls = "step-connector done" if i < current_step else "step-connector"
            parts.append(f'<div class="{conn_cls}"></div>')

    parts.append("</div>")
    st.markdown("".join(parts), unsafe_allow_html=True)

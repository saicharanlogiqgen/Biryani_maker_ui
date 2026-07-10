"""Shared UI helpers."""

import base64
from datetime import datetime
from functools import lru_cache
from pathlib import Path

import streamlit as st

SPLASH_HOLD_SECONDS = 3.0
SPLASH_FADE_SECONDS = 1.0

ASSETS_DIR = Path(__file__).parent.parent / "assets"
MASCOT_PATH = ASSETS_DIR / "dumchef_mascot.png"
WORDMARK_PATH = ASSETS_DIR / "dumchef_wordmark.png"
LEGACY_LOGO_PATH = ASSETS_DIR / "dumchef_logo.png"


def load_css() -> None:
    css_path = Path(__file__).parent.parent / "styles" / "custom.css"
    with open(css_path, encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


@lru_cache(maxsize=8)
def get_asset_data_uri(path_str: str, version: float = 0.0) -> str:
    path = Path(path_str)
    with open(path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("ascii")
    return f"data:image/png;base64,{encoded}"


def asset_uri(path: Path) -> str:
    """Load asset with mtime so updated images refresh in-session."""
    return get_asset_data_uri(str(path), path.stat().st_mtime)


def render_splash_screen(*, fading: bool = False) -> None:
    fade_cls = " fade-out" if fading else ""
    mascot_uri = asset_uri(MASCOT_PATH)
    wordmark_uri = asset_uri(WORDMARK_PATH)
    st.markdown(
        f"""
        <div class="splash-screen{fade_cls}">
            <div class="splash-content">
                <img class="splash-mascot" src="{mascot_uri}" alt="Dumchef mascot" />
                <img class="splash-wordmark" src="{wordmark_uri}" alt="Dumchef" />
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_header() -> None:
    now = datetime.now().strftime("%a %H:%M:%S")
    mascot_uri = asset_uri(MASCOT_PATH)
    wordmark_uri = asset_uri(WORDMARK_PATH)
    st.markdown(
        f"""
        <div class="app-header">
            <div class="brand-lockup">
                <img class="brand-mascot" src="{mascot_uri}" alt="Dumchef" />
                <img class="brand-wordmark" src="{wordmark_uri}" alt="Dumchef" />
            </div>
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

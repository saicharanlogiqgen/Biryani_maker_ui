"""Recipe card rendering component."""

import streamlit as st


def render_recipe_card(recipe: dict) -> None:
    """Render a styled recipe card with icon, title, and description."""
    st.markdown(
        f"""
        <div class="recipe-card" style="--card-accent: {recipe['icon_color']};">
            <div class="recipe-icon">{recipe['emoji']}</div>
            <div class="recipe-name">{recipe['title']}</div>
            <div class="recipe-desc">{recipe['description']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_recipe_grid_header() -> None:
    st.markdown('<div class="recipe-grid">', unsafe_allow_html=True)

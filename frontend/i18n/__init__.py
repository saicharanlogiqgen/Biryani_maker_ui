"""Internationalization helpers for Dumchef (English / Hindi / Telugu)."""

from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path

import streamlit as st

I18N_DIR = Path(__file__).parent
SUPPORTED_LANGUAGES = {
    "en": "English",
    "hi": "हिन्दी",
    "te": "తెలుగు",
}
DEFAULT_LANGUAGE = "en"


@lru_cache(maxsize=8)
def _load_lang(lang: str) -> dict:
    path = I18N_DIR / f"{lang}.json"
    if not path.exists():
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def get_language() -> str:
    lang = st.session_state.get("language", DEFAULT_LANGUAGE)
    return lang if lang in SUPPORTED_LANGUAGES else DEFAULT_LANGUAGE


def set_language(lang: str) -> None:
    if lang in SUPPORTED_LANGUAGES:
        st.session_state.language = lang


def t(key: str, **kwargs) -> str:
    """Translate a UI key for the active language, with English fallback."""
    lang = get_language()
    text = _load_lang(lang).get(key)
    if text is None:
        text = _load_lang(DEFAULT_LANGUAGE).get(key, key)
    if kwargs:
        try:
            return text.format(**kwargs)
        except (KeyError, ValueError):
            return text
    return text


def ingredient_key(name: str) -> str:
    slug = name.lower().strip()
    slug = slug.replace("&", "and")
    slug = re.sub(r"[^a-z0-9]+", "_", slug)
    return f"ing.{slug.strip('_')}"


def tr_ingredient(name: str) -> str:
    key = ingredient_key(name)
    translated = t(key)
    return name if translated == key else translated


def tr_item_title(item_id: str, fallback: str) -> str:
    key = f"item.{item_id}.title"
    translated = t(key)
    return fallback if translated == key else translated


def tr_item_desc(item_id: str, fallback: str) -> str:
    key = f"item.{item_id}.desc"
    translated = t(key)
    return fallback if translated == key else translated


STAGE_TITLE_KEYS = {
    "Preparing ingredients": "stage.preparing_ingredients",
    "Heating": "stage.heating",
    "Adding ingredients": "stage.adding_ingredients",
    "Mixing": "stage.mixing",
    "Cooking": "stage.cooking",
    "Finalizing": "stage.finalizing",
    "Ready to Serve": "stage.ready_to_serve",
}


def localize_card(item: dict) -> dict:
    """Return a shallow copy with localized title/description for display."""
    item_id = item.get("id", "")
    fallback_title = item.get("title", "")
    # Menu card and chicken dish share id "chicken_biryani"
    if item_id == "chicken_biryani" and fallback_title != "Biryani":
        title = t("item.chicken_biryani_dish.title")
        desc = t("item.chicken_biryani_dish.desc")
        return {
            **item,
            "title": fallback_title if title.startswith("item.") else title,
            "description": item.get("description", "") if desc.startswith("item.") else desc,
        }
    return {
        **item,
        "title": tr_item_title(item_id, fallback_title),
        "description": tr_item_desc(item_id, item.get("description", "")),
    }


def localize_ingredients(ingredients: list[dict]) -> list[dict]:
    return [
        {**ing, "name": tr_ingredient(ing.get("name", ""))}
        for ing in ingredients
    ]


def localize_stage_text(title: str, description: str, family: str) -> tuple[str, str]:
    title_key = STAGE_TITLE_KEYS.get(title)
    new_title = t(title_key) if title_key else title
    slug = title_key.replace("stage.", "") if title_key else ""
    desc_key = f"stage.{family}.{slug}" if slug else ""
    if desc_key:
        translated = t(desc_key)
        new_desc = description if translated == desc_key else translated
    else:
        new_desc = description
    return new_title, new_desc


def localize_stages(stages: list[dict], family: str) -> list[dict]:
    """Localize cooking stage titles/descriptions by family: rice|curry|biryani."""
    localized = []
    for stage in stages:
        new_title, new_desc = localize_stage_text(
            stage.get("title", ""),
            stage.get("description", ""),
            family,
        )
        localized.append({**stage, "title": new_title, "description": new_desc})
    return localized


def stage_family_for_recipe(recipe_id: str) -> str:
    if recipe_id in ("cook_rice", "millets"):
        return "rice"
    if recipe_id == "curry":
        return "curry"
    return "biryani"

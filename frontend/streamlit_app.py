"""DHUM CHEF👨‍🍳 — Main Application."""

import sys
from pathlib import Path
import time

import streamlit as st

# Ensure project root is on the path
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from frontend.data.recipes import (
    RECIPES,
    CURRY_CATEGORIES,
    RICE_CATEGORIES,
    BIRYANI_CATEGORIES,
    get_selected_curry,
    get_selected_rice_item,
    get_selected_biryani,
)
from frontend.components.recipe_card import render_recipe_card
from frontend.components.progress_tracker import (
    run_cooking_with_service,
    run_cooking_simulation,
    format_time,
)
from frontend.components.ui_helpers import (
    load_css,
    render_header,
    render_step_indicator,
    render_splash_screen,
    SPLASH_HOLD_SECONDS,
    SPLASH_FADE_SECONDS,
)
from backend.services.cooking_service import get_shared_cooking_service

# ── Page config ──
st.set_page_config(
    page_title="Dumchef",
    page_icon="🍛",
    layout="wide",
    initial_sidebar_state="collapsed",
)

load_css()


def init_session_state() -> None:
    defaults = {
        "workflow_step": "welcome",
        "splash_done": False,
        "splash_start_time": None,
        "selected_recipe": None,
        "selected_batch": None,
        "selected_curry_category": None,
        "selected_curry_id": None,
        "selected_rice_category": None,
        "selected_rice_id": None,
        "selected_biryani_category": None,
        "selected_biryani_id": None,
        "cook_start_time": None,
        "total_cook_time": 0,
        "cooking_started": False,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


def get_cooking_service():
    return get_shared_cooking_service()


def clear_ingredient_keys() -> None:
    for key in list(st.session_state.keys()):
        if key.startswith("ing_"):
            del st.session_state[key]


def init_ingredient_keys(recipe_id: str) -> None:
    ingredients = get_active_ingredients(recipe_id)
    for i in range(len(ingredients)):
        st.session_state[f"ing_{recipe_id}_{i}"] = False


def ensure_ingredient_keys(recipe_id: str) -> None:
    ingredients = get_active_ingredients(recipe_id)
    for i in range(len(ingredients)):
        key = f"ing_{recipe_id}_{i}"
        if key not in st.session_state:
            st.session_state[key] = False


def all_ingredients_checked(recipe_id: str) -> bool:
    ingredients = get_active_ingredients(recipe_id)
    return all(
        st.session_state.get(f"ing_{recipe_id}_{i}", False)
        for i in range(len(ingredients))
    )


def count_checked_ingredients(recipe_id: str) -> int:
    ingredients = get_active_ingredients(recipe_id)
    return sum(
        1
        for i in range(len(ingredients))
        if st.session_state.get(f"ing_{recipe_id}_{i}", False)
    )


def get_active_ingredients(recipe_id: str) -> list[dict]:
    recipe = RECIPES[recipe_id]
    if recipe_id == "chicken_biryani":
        biryani = get_selected_biryani(
            st.session_state.get("selected_biryani_category"),
            st.session_state.get("selected_biryani_id"),
        )
        if not biryani:
            return []
        if biryani.get("batch_ingredients"):
            selected_batch = st.session_state.get("selected_batch") or biryani.get("default_batch", "5kg")
            return biryani["batch_ingredients"].get(selected_batch, biryani.get("ingredients", []))
        return biryani.get("ingredients", [])
    if recipe_id == "curry":
        curry = get_selected_curry(
            st.session_state.get("selected_curry_category"),
            st.session_state.get("selected_curry_id"),
        )
        return curry["ingredients"] if curry else []
    if recipe_id == "cook_rice":
        item = get_selected_rice_item(
            st.session_state.get("selected_rice_category"),
            st.session_state.get("selected_rice_id"),
        )
        return item["ingredients"] if item else []
    return recipe["ingredients"]


def get_display_recipe() -> dict:
    """Recipe used for titles/stages during cooking and completion."""
    recipe_id = st.session_state.selected_recipe
    recipe = RECIPES[recipe_id]
    if recipe_id == "curry":
        curry = get_selected_curry(
            st.session_state.get("selected_curry_category"),
            st.session_state.get("selected_curry_id"),
        )
        if curry:
            return {
                **recipe,
                "id": curry["id"],
                "title": curry["title"],
                "emoji": curry["emoji"],
                "description": curry["description"],
                "ingredients": curry["ingredients"],
            }
    if recipe_id == "cook_rice":
        item = get_selected_rice_item(
            st.session_state.get("selected_rice_category"),
            st.session_state.get("selected_rice_id"),
        )
        if item:
            return {
                **recipe,
                "id": item["id"],
                "title": item["title"],
                "emoji": item["emoji"],
                "description": item["description"],
                "ingredients": item["ingredients"],
            }
    if recipe_id == "chicken_biryani":
        biryani = get_selected_biryani(
            st.session_state.get("selected_biryani_category"),
            st.session_state.get("selected_biryani_id"),
        )
        if biryani:
            return {
                **recipe,
                "id": biryani["id"],
                "title": biryani["title"],
                "emoji": biryani["emoji"],
                "description": biryani["description"],
                "ingredients": get_active_ingredients(recipe_id),
                "batch_options": biryani.get("batch_options"),
                "default_batch": biryani.get("default_batch"),
            }
    return recipe


def reset_workflow() -> None:
    if st.session_state.get("cooking_started"):
        get_cooking_service().emergency_stop()
    st.session_state.workflow_step = "dashboard"
    st.session_state.selected_recipe = None
    st.session_state.selected_batch = None
    st.session_state.selected_curry_category = None
    st.session_state.selected_curry_id = None
    st.session_state.selected_rice_category = None
    st.session_state.selected_rice_id = None
    st.session_state.selected_biryani_category = None
    st.session_state.selected_biryani_id = None
    clear_ingredient_keys()
    st.session_state.cook_start_time = None
    st.session_state.total_cook_time = 0
    st.session_state.cooking_started = False


def init_manual_state() -> None:
    if "manual_device_state" not in st.session_state:
        st.session_state.manual_device_state = {
            "mixer_motor": "OFF",
            "position_motor": "STOP",
            "rice_bowl": "STOP",
            "mixer_hydraulic": "STOP",
            "electronic_valve": "STOP",
        }


def set_manual_state(device: str, state: str) -> None:
    init_manual_state()
    st.session_state.manual_device_state[device] = state


def render_manual_title(title: str, device: str) -> None:
    init_manual_state()
    state = st.session_state.manual_device_state.get(device, "STOP")
    state_class = "manual-state-on" if state not in ("OFF", "STOP") else "manual-state-off"
    st.markdown(
        f"""
        <div class="manual-header-row">
            <span class="manual-device-title">{title}</span>
            <span class="manual-state-badge {state_class}">{state}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def start_recipe(recipe_id: str) -> None:
    clear_ingredient_keys()
    st.session_state.selected_recipe = recipe_id
    st.session_state.selected_batch = None
    st.session_state.selected_curry_category = None
    st.session_state.selected_curry_id = None
    st.session_state.selected_rice_category = None
    st.session_state.selected_rice_id = None
    st.session_state.selected_biryani_category = None
    st.session_state.selected_biryani_id = None
    st.session_state.cook_start_time = None

    if recipe_id == "chicken_biryani":
        st.session_state.workflow_step = "biryani_category"
    elif recipe_id == "curry":
        st.session_state.workflow_step = "curry_category"
    elif recipe_id == "cook_rice":
        st.session_state.workflow_step = "rice_category"
    else:
        init_ingredient_keys(recipe_id)
        st.session_state.workflow_step = "ingredients"


# ── Dashboard ──
def render_dashboard() -> None:
    render_header()
    st.markdown(
        '<p style="color: #c4a882; font-size: 0.95rem; margin-bottom: 1.5rem;">'
        "Select a recipe to begin cooking</p>",
        unsafe_allow_html=True,
    )

    recipe_list = list(RECIPES.values()) + [
        {
            "id": "manual_mode",
            "title": "Manual Mode",
            "emoji": "🎮",
            "icon_color": "#ff8a00",
            "description": "Direct device control with manual inputs",
        }
    ]
    cols = st.columns(len(recipe_list))

    for col, recipe in zip(cols, recipe_list):
        with col:
            render_recipe_card(recipe)
            if st.button(
                "Start",
                key=f"start_{recipe['id']}",
                type="primary",
                use_container_width=True,
            ):
                if recipe["id"] == "manual_mode":
                    st.session_state.workflow_step = "manual"
                else:
                    start_recipe(recipe["id"])
                st.rerun()


# ── Biryani: Veg / Non-Veg ──
def render_biryani_category_step() -> None:
    render_header()
    st.markdown(
        '<p style="color: #c4a882; font-size: 0.95rem; margin-bottom: 1.5rem;">'
        "Select biryani type</p>",
        unsafe_allow_html=True,
    )

    cols = st.columns(2)
    for col, category in zip(cols, BIRYANI_CATEGORIES.values()):
        with col:
            render_recipe_card(category)
            if st.button(
                "Select",
                key=f"biryani_cat_{category['id']}",
                type="primary",
                use_container_width=True,
            ):
                st.session_state.selected_biryani_category = category["id"]
                st.session_state.selected_biryani_id = None
                st.session_state.selected_batch = None
                st.session_state.workflow_step = "biryani_list"
                st.rerun()

    if st.button("← Back to Home", key="biryani_cat_back", use_container_width=True):
        reset_workflow()
        st.rerun()


# ── Biryani list ──
def render_biryani_list_step() -> None:
    category_id = st.session_state.selected_biryani_category
    category = BIRYANI_CATEGORIES.get(category_id)
    if not category:
        st.session_state.workflow_step = "biryani_category"
        st.rerun()

    render_header()
    st.markdown(
        f'<p style="color: #c4a882; font-size: 0.95rem; margin-bottom: 1.5rem;">'
        f"{category['emoji']} {category['title']} — Select a biryani</p>",
        unsafe_allow_html=True,
    )

    items = list(category["items"].values())
    cols = st.columns(min(3, len(items)))
    for index, item in enumerate(items):
        with cols[index % len(cols)]:
            render_recipe_card(item)
            if st.button(
                "Start",
                key=f"biryani_item_{item['id']}",
                type="primary",
                use_container_width=True,
            ):
                st.session_state.selected_biryani_id = item["id"]
                st.session_state.selected_batch = item.get("default_batch")
                clear_ingredient_keys()
                init_ingredient_keys("chicken_biryani")
                st.session_state.workflow_step = "ingredients"
                st.rerun()

    if st.button("← Back", key="biryani_list_back", use_container_width=True):
        st.session_state.selected_biryani_id = None
        st.session_state.workflow_step = "biryani_category"
        st.rerun()


# ── Rice: Rice / Pulao ──
def render_rice_category_step() -> None:
    render_header()
    st.markdown(
        '<p style="color: #c4a882; font-size: 0.95rem; margin-bottom: 1.5rem;">'
        "Select rice type</p>",
        unsafe_allow_html=True,
    )

    cols = st.columns(2)
    for col, category in zip(cols, RICE_CATEGORIES.values()):
        with col:
            render_recipe_card(category)
            if st.button(
                "Select",
                key=f"rice_cat_{category['id']}",
                type="primary",
                use_container_width=True,
            ):
                st.session_state.selected_rice_category = category["id"]
                st.session_state.selected_rice_id = None
                st.session_state.workflow_step = "rice_list"
                st.rerun()

    if st.button("← Back to Home", key="rice_cat_back", use_container_width=True):
        reset_workflow()
        st.rerun()


# ── Rice / Pulao list ──
def render_rice_list_step() -> None:
    category_id = st.session_state.selected_rice_category
    category = RICE_CATEGORIES.get(category_id)
    if not category:
        st.session_state.workflow_step = "rice_category"
        st.rerun()

    render_header()
    st.markdown(
        f'<p style="color: #c4a882; font-size: 0.95rem; margin-bottom: 1.5rem;">'
        f"{category['emoji']} {category['title']} — Select an option</p>",
        unsafe_allow_html=True,
    )

    items = list(category["items"].values())
    cols = st.columns(min(3, len(items)))
    for index, item in enumerate(items):
        with cols[index % len(cols)]:
            render_recipe_card(item)
            if st.button(
                "Start",
                key=f"rice_item_{item['id']}",
                type="primary",
                use_container_width=True,
            ):
                st.session_state.selected_rice_id = item["id"]
                clear_ingredient_keys()
                init_ingredient_keys("cook_rice")
                st.session_state.workflow_step = "ingredients"
                st.rerun()

    if st.button("← Back", key="rice_list_back", use_container_width=True):
        st.session_state.selected_rice_id = None
        st.session_state.workflow_step = "rice_category"
        st.rerun()


# ── Curry: Veg / Non-Veg ──
def render_curry_category_step() -> None:
    render_header()
    st.markdown(
        '<p style="color: #c4a882; font-size: 0.95rem; margin-bottom: 1.5rem;">'
        "Select curry type</p>",
        unsafe_allow_html=True,
    )

    cols = st.columns(2)
    for col, category in zip(cols, CURRY_CATEGORIES.values()):
        with col:
            render_recipe_card(category)
            if st.button(
                "Select",
                key=f"curry_cat_{category['id']}",
                type="primary",
                use_container_width=True,
            ):
                st.session_state.selected_curry_category = category["id"]
                st.session_state.selected_curry_id = None
                st.session_state.workflow_step = "curry_list"
                st.rerun()

    if st.button("← Back to Home", key="curry_cat_back", use_container_width=True):
        reset_workflow()
        st.rerun()


# ── Curry list (5 options) ──
def render_curry_list_step() -> None:
    category_id = st.session_state.selected_curry_category
    category = CURRY_CATEGORIES.get(category_id)
    if not category:
        st.session_state.workflow_step = "curry_category"
        st.rerun()

    render_header()
    st.markdown(
        f'<p style="color: #c4a882; font-size: 0.95rem; margin-bottom: 1.5rem;">'
        f"{category['emoji']} {category['title']} — Select a curry</p>",
        unsafe_allow_html=True,
    )

    curries = list(category["items"].values())
    cols = st.columns(min(3, len(curries)))
    for index, curry in enumerate(curries):
        with cols[index % len(cols)]:
            render_recipe_card(curry)
            if st.button(
                "Start",
                key=f"curry_item_{curry['id']}",
                type="primary",
                use_container_width=True,
            ):
                st.session_state.selected_curry_id = curry["id"]
                clear_ingredient_keys()
                init_ingredient_keys("curry")
                st.session_state.workflow_step = "ingredients"
                st.rerun()

    if st.button("← Back", key="curry_list_back", use_container_width=True):
        st.session_state.selected_curry_id = None
        st.session_state.workflow_step = "curry_category"
        st.rerun()


# ── Step 1: Ingredients ──
def render_ingredients_step() -> None:
    recipe = get_display_recipe()
    render_header()
    render_step_indicator(0)

    st.markdown(
        f"""
        <div class="ingredients-panel">
            <div class="panel-title">Step 1: Required Ingredients</div>
            <div class="panel-subtitle">
                {recipe['emoji']} {recipe['title']} — Mark each ingredient as added
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    recipe_id = st.session_state.selected_recipe
    display = get_display_recipe()
    if recipe_id == "chicken_biryani" and display.get("batch_options"):
        batch_options = display["batch_options"]
        current_batch = st.session_state.get("selected_batch") or display.get("default_batch", "5kg")
        chosen_batch = st.radio(
            "Select batch size",
            options=batch_options,
            index=batch_options.index(current_batch) if current_batch in batch_options else 0,
            horizontal=True,
            key="batch_selector",
        )
        if chosen_batch != st.session_state.get("selected_batch"):
            st.session_state.selected_batch = chosen_batch
            clear_ingredient_keys()
            init_ingredient_keys(recipe_id)
            st.rerun()

    ingredients = get_active_ingredients(recipe_id)
    st.markdown('<div class="ingredient-list">', unsafe_allow_html=True)

    ensure_ingredient_keys(recipe_id)
    for i, ingredient in enumerate(ingredients):
        name = ingredient["name"]
        qty = ingredient["quantity"]
        cb_key = f"ing_{recipe_id}_{i}"

        col_check, col_text = st.columns([0.07, 0.93], vertical_alignment="center")
        with col_check:
            st.checkbox(
                "added",
                key=cb_key,
                label_visibility="collapsed",
            )
        with col_text:
            st.markdown(
                f"""
                <div class="ingredient-label">
                    <span class="ingredient-name" style="color:#ffffff;">{name}</span>
                    <span class="ingredient-qty" style="color:#ffb300;">{qty}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("</div>", unsafe_allow_html=True)

    all_added = all_ingredients_checked(recipe_id)
    added_count = count_checked_ingredients(recipe_id)
    total = len(ingredients)

    st.markdown(
        f'<p style="color: #c4a882; font-size: 0.85rem; margin: 1rem 0;">'
        f"{added_count} of {total} ingredients added</p>",
        unsafe_allow_html=True,
    )

    col_back, col_next = st.columns([1, 1])
    with col_back:
        if st.button("← Back", use_container_width=True):
            if recipe_id == "curry":
                clear_ingredient_keys()
                st.session_state.selected_curry_id = None
                st.session_state.workflow_step = "curry_list"
            elif recipe_id == "cook_rice":
                clear_ingredient_keys()
                st.session_state.selected_rice_id = None
                st.session_state.workflow_step = "rice_list"
            elif recipe_id == "chicken_biryani":
                clear_ingredient_keys()
                st.session_state.selected_biryani_id = None
                st.session_state.selected_batch = None
                st.session_state.workflow_step = "biryani_list"
            else:
                reset_workflow()
            st.rerun()
    with col_next:
        if st.button(
            "Next →",
            type="primary",
            disabled=not all_added or total == 0,
            use_container_width=True,
        ):
            st.session_state.workflow_step = "cooking"
            st.session_state.cook_start_time = time.time()
            st.session_state.cooking_started = False
            st.rerun()


# ── Step 2: Cooking ──
def render_cooking_step() -> None:
    recipe = get_display_recipe()
    render_header()
    render_step_indicator(1)

    st.markdown(
        f"""
        <div style="margin-bottom: 1rem;">
            <span style="color: #ff8a00; font-weight: 600; font-size: 1.1rem;">
                Step 2: Cooking Process
            </span>
            <span style="color: #c4a882; font-size: 0.9rem;">
                &nbsp;— {recipe['emoji']} {recipe['title']}
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    base_recipe = RECIPES[st.session_state.selected_recipe]
    selected_item_id = st.session_state.get("selected_biryani_id")
    machine_items = base_recipe.get("machine_item_ids", [])
    use_machine = base_recipe.get("machine_enabled", False) and (
        not machine_items or selected_item_id in machine_items
    )

    if use_machine:
        run_cooking_with_service(base_recipe, get_cooking_service())
    else:
        # Use display recipe for UI stages, keep cook timing from base recipe
        sim_recipe = {
            **recipe,
            "total_cook_seconds": base_recipe.get("total_cook_seconds", 22),
            "stages": base_recipe.get("stages", recipe.get("stages", [])),
        }
        run_cooking_simulation(sim_recipe)


def render_manual_step() -> None:
    render_header()
    st.markdown(
        '<p style="color:#c4a882; margin-bottom: 1rem;">Manual Mode — Control devices using direct inputs</p>',
        unsafe_allow_html=True,
    )

    service = get_cooking_service()
    machine = service.machine
    is_mock = service.get_status().get("is_mock", False)

    if is_mock:
        st.info("Running in mock hardware mode.")

    if service.is_running():
        st.warning("A recipe is currently cooking. Stop it before manual control.")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🛑 Emergency Stop", type="primary", use_container_width=True):
                service.emergency_stop()
                st.rerun()
        with c2:
            if st.button("← Back to Home", use_container_width=True):
                reset_workflow()
                st.rerun()
        return

    render_manual_title("Mixer Motor", "mixer_motor")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Mixer ON", key="manual_mixer_on", use_container_width=True):
            machine.stop_main_devices()
            machine.mixer_motor.on()
            set_manual_state("mixer_motor", "ON")
            set_manual_state("position_motor", "STOP")
            set_manual_state("rice_bowl", "STOP")
            set_manual_state("mixer_hydraulic", "STOP")
    with c2:
        if st.button("Mixer OFF", key="manual_mixer_off", use_container_width=True):
            machine.mixer_motor.off()
            set_manual_state("mixer_motor", "OFF")

    render_manual_title("Position Motor", "position_motor")
    c3, c4 = st.columns(2)
    with c3:
        if st.button("Forward 180°", key="manual_pos_fwd", use_container_width=True):
            machine.stop_main_devices()
            machine.position_motor.forward()
            set_manual_state("position_motor", "FORWARD")
            set_manual_state("mixer_motor", "OFF")
            set_manual_state("rice_bowl", "STOP")
            set_manual_state("mixer_hydraulic", "STOP")
            set_manual_state("position_motor", "STOP")
    with c4:
        if st.button("Backward 180°", key="manual_pos_bwd", use_container_width=True):
            machine.stop_main_devices()
            machine.position_motor.backward()
            set_manual_state("position_motor", "BACKWARD")
            set_manual_state("mixer_motor", "OFF")
            set_manual_state("rice_bowl", "STOP")
            set_manual_state("mixer_hydraulic", "STOP")
            set_manual_state("position_motor", "STOP")

    render_manual_title("Rice Bowl Hydraulic", "rice_bowl")
    c5, c6, c7 = st.columns(3)
    with c5:
        if st.button("Rice Bowl DOWN", key="manual_rice_down", use_container_width=True):
            machine.stop_main_devices()
            machine.rice_bowl.down()
            set_manual_state("rice_bowl", "DOWN")
            set_manual_state("mixer_motor", "OFF")
            set_manual_state("position_motor", "STOP")
            set_manual_state("mixer_hydraulic", "STOP")
    with c6:
        if st.button("Rice Bowl UP", key="manual_rice_up", use_container_width=True):
            machine.stop_main_devices()
            machine.rice_bowl.up()
            set_manual_state("rice_bowl", "UP")
            set_manual_state("mixer_motor", "OFF")
            set_manual_state("position_motor", "STOP")
            set_manual_state("mixer_hydraulic", "STOP")
    with c7:
        if st.button("Rice Bowl STOP", key="manual_rice_stop", use_container_width=True):
            machine.rice_bowl.stop()
            set_manual_state("rice_bowl", "STOP")

    render_manual_title("Mixer Hydraulic", "mixer_hydraulic")
    c8, c9, c10 = st.columns(3)
    with c8:
        if st.button("Mixer DOWN", key="manual_mix_down", use_container_width=True):
            machine.stop_main_devices()
            machine.mixer_hydraulic.down()
            set_manual_state("mixer_hydraulic", "DOWN")
            set_manual_state("mixer_motor", "OFF")
            set_manual_state("position_motor", "STOP")
            set_manual_state("rice_bowl", "STOP")
    with c9:
        if st.button("Mixer UP", key="manual_mix_up", use_container_width=True):
            machine.stop_main_devices()
            machine.mixer_hydraulic.up()
            set_manual_state("mixer_hydraulic", "UP")
            set_manual_state("mixer_motor", "OFF")
            set_manual_state("position_motor", "STOP")
            set_manual_state("rice_bowl", "STOP")
    with c10:
        if st.button("Mixer STOP", key="manual_mix_stop", use_container_width=True):
            machine.mixer_hydraulic.stop()
            set_manual_state("mixer_hydraulic", "STOP")

    render_manual_title("Electronic Valve", "electronic_valve")
    c11, c12, c13 = st.columns(3)
    with c11:
        if st.button("Valve OPEN", key="manual_valve_open", use_container_width=True):
            machine.electronic_valve.open()
            set_manual_state("electronic_valve", "OPEN")
    with c12:
        if st.button("Valve CLOSE", key="manual_valve_close", use_container_width=True):
            machine.electronic_valve.close()
            set_manual_state("electronic_valve", "CLOSE")
    with c13:
        if st.button("Valve STOP", key="manual_valve_stop", use_container_width=True):
            machine.electronic_valve.stop()
            set_manual_state("electronic_valve", "STOP")

    st.markdown("---")
    c14, c15 = st.columns(2)
    with c14:
        if st.button("🛑 STOP EVERYTHING", key="manual_stop_all", type="primary", use_container_width=True):
            service.emergency_stop()
            st.session_state.manual_device_state = {
                "mixer_motor": "OFF",
                "position_motor": "STOP",
                "rice_bowl": "STOP",
                "mixer_hydraulic": "STOP",
                "electronic_valve": "STOP",
            }
            st.success("All devices stopped.")
    with c15:
        if st.button("🏠 Back to Home", key="manual_back_home", use_container_width=True):
            reset_workflow()
            st.rerun()


# ── Step 3: Completion ──
def render_completion_step() -> None:
    recipe = get_display_recipe()
    cook_time = st.session_state.total_cook_time
    render_header()
    render_step_indicator(2)

    st.markdown(
        f"""
        <div class="completion-panel">
            <div class="success-checkmark">✓</div>
            <div class="success-title">Your {recipe['title']} is Ready!</div>
            <div class="success-time">
                {recipe['emoji']} Total cooking time: {format_time(cook_time)}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div style='height: 1.5rem'></div>", unsafe_allow_html=True)

    col_again, col_home = st.columns(2)
    with col_again:
        if st.button("🔄 Cook Again", type="primary", use_container_width=True):
            recipe_id = st.session_state.selected_recipe
            if recipe_id == "curry" and st.session_state.get("selected_curry_id"):
                clear_ingredient_keys()
                init_ingredient_keys("curry")
                st.session_state.workflow_step = "ingredients"
                st.session_state.cooking_started = False
            elif recipe_id == "cook_rice" and st.session_state.get("selected_rice_id"):
                clear_ingredient_keys()
                init_ingredient_keys("cook_rice")
                st.session_state.workflow_step = "ingredients"
                st.session_state.cooking_started = False
            elif recipe_id == "chicken_biryani" and st.session_state.get("selected_biryani_id"):
                clear_ingredient_keys()
                init_ingredient_keys("chicken_biryani")
                st.session_state.workflow_step = "ingredients"
                st.session_state.cooking_started = False
            else:
                start_recipe(recipe_id)
            st.rerun()
    with col_home:
        if st.button("🏠 Back to Home", use_container_width=True):
            reset_workflow()
            st.rerun()


def render_welcome_step() -> None:
    """Show Dumchef logo for 3s, fade out, then open dashboard."""
    if st.session_state.splash_done:
        st.session_state.workflow_step = "dashboard"
        st.rerun()

    if st.session_state.splash_start_time is None:
        st.session_state.splash_start_time = time.time()

    elapsed = time.time() - st.session_state.splash_start_time
    hold_end = SPLASH_HOLD_SECONDS
    fade_end = SPLASH_HOLD_SECONDS + SPLASH_FADE_SECONDS

    if elapsed < hold_end:
        render_splash_screen(fading=False)
        time.sleep(0.2)
        st.rerun()
    elif elapsed < fade_end:
        render_splash_screen(fading=True)
        time.sleep(0.2)
        st.rerun()
    else:
        st.session_state.splash_done = True
        st.session_state.workflow_step = "dashboard"
        st.rerun()


# ── Main router ──
def main() -> None:
    init_session_state()

    # Always show splash once per browser session
    if not st.session_state.splash_done:
        st.session_state.workflow_step = "welcome"

    step = st.session_state.workflow_step

    if step == "welcome":
        render_welcome_step()
    elif step == "dashboard":
        render_dashboard()
    elif step == "rice_category":
        render_rice_category_step()
    elif step == "rice_list":
        render_rice_list_step()
    elif step == "biryani_category":
        render_biryani_category_step()
    elif step == "biryani_list":
        render_biryani_list_step()
    elif step == "curry_category":
        render_curry_category_step()
    elif step == "curry_list":
        render_curry_list_step()
    elif step == "ingredients":
        render_ingredients_step()
    elif step == "cooking":
        render_cooking_step()
    elif step == "manual":
        render_manual_step()
    elif step == "complete":
        render_completion_step()


if __name__ == "__main__":
    main()

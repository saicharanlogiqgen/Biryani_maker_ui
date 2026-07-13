"""Cooking progress tracker component."""

import time

import streamlit as st

from frontend.i18n import localize_stage_text, stage_family_for_recipe, t


def get_current_stage(stages: list, progress: float) -> tuple[dict, int]:
    """Return the active stage dict and its index based on progress percentage."""
    cumulative = 0.0
    for i, stage in enumerate(stages):
        cumulative += stage["duration_pct"]
        if progress < cumulative:
            return stage, i
    return stages[-1], len(stages) - 1


def format_time(seconds: int) -> str:
    if seconds < 60:
        return f"{seconds}s"
    mins, secs = divmod(seconds, 60)
    if secs == 0:
        return f"{mins} min"
    return f"{mins}m {secs}s"


def render_stage_chips(stages: list, active_index: int) -> str:
    chips = []
    for i, stage in enumerate(stages):
        if i < active_index:
            cls = "stage-chip done"
        elif i == active_index:
            cls = "stage-chip active"
        else:
            cls = "stage-chip"
        chips.append(f'<span class="{cls}">{stage["title"]}</span>')
    return "".join(chips)


def render_cooking_progress(
    recipe: dict,
    progress: float,
    remaining_seconds: int,
    stage_emoji: str = "🔥",
) -> None:
    """Render the cooking progress panel."""
    stage, stage_index = get_current_stage(recipe["stages"], progress)
    chips_html = render_stage_chips(recipe["stages"], stage_index)

    st.markdown(
        f"""
        <div class="cooking-panel">
            <div class="stage-indicator-ring">
                <span class="stage-emoji">{stage_emoji}</span>
            </div>
            <div class="current-stage-title">{stage['title']}</div>
            <div class="current-stage-desc">{stage['description']}</div>
            <div class="progress-bar-track">
                <div class="progress-bar-fill" style="width: {progress:.0f}%;"></div>
            </div>
            <div class="progress-label">
                <span>{t("progress_label", pct=f"{progress:.0f}")}</span>
                <span>{t("remaining_label", time=format_time(remaining_seconds))}</span>
            </div>
            <div class="stages-timeline">{chips_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def run_cooking_with_service(recipe: dict, service) -> None:
    """
    Poll the backend CookingService and update the UI.
    Falls back to simulation if service is None.
    """
    recipe_id = recipe["id"]
    family = stage_family_for_recipe(recipe_id)

    if not st.session_state.get("cooking_started"):
        started = service.start_recipe(recipe_id)
        if not started:
            st.error(t("error_cooking_in_progress"))
            return
        st.session_state.cooking_started = True

    status = service.get_status()
    state = status["state"]
    progress = status["progress"]
    remaining = status["remaining_seconds"]

    raw_title = status["stage_title"] or "Cooking"
    raw_desc = status["stage_description"] or status["message"]
    stage_title, stage_desc = localize_stage_text(raw_title, raw_desc, family)
    stage_index = max(0, status["current_step"] - 1)
    stages = recipe["stages"]

    stage_emojis = ["🥣", "🔥", "🧂", "🥄", "🍳", "✨", "✅"]
    emoji = stage_emojis[min(stage_index, len(stage_emojis) - 1)]

    mock_badge = ""
    if status.get("is_mock"):
        mock_badge = (
            '<span style="color:#c4a882;font-size:0.8rem;">'
            f"{t('mock_hardware')}</span>"
        )

    st.markdown(
        f"""
        <div class="cooking-panel">
            <div class="stage-indicator-ring">
                <span class="stage-emoji">{emoji}</span>
            </div>
            <div class="current-stage-title">{stage_title}{mock_badge}</div>
            <div class="current-stage-desc">{stage_desc}</div>
            <div class="progress-bar-track">
                <div class="progress-bar-fill" style="width: {progress:.0f}%;"></div>
            </div>
            <div class="progress-label">
                <span>{t("progress_label", pct=f"{progress:.0f}")}</span>
                <span>{t("step_of", current=status["current_step"], total=status["total_steps"])}</span>
                <span>{t("remaining_label", time=format_time(remaining))}</span>
            </div>
            <div class="stages-timeline">{render_stage_chips(stages, stage_index)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if state == "running":
        if st.button(t("btn_emergency_stop"), type="primary", use_container_width=True):
            service.emergency_stop()
            st.session_state.cooking_started = False
            st.session_state.workflow_step = "dashboard"
            st.session_state.selected_recipe = None
            st.rerun()
        time.sleep(0.8)
        st.rerun()
    elif state == "completed":
        st.session_state.workflow_step = "complete"
        st.session_state.total_cook_time = status["elapsed_seconds"]
        st.session_state.cooking_started = False
        st.rerun()
    elif state in ("stopped", "error"):
        st.session_state.cooking_started = False
        st.error(status.get("message") or t("error_cooking_interrupted"))
        if st.button(t("btn_back_home"), use_container_width=True):
            st.session_state.workflow_step = "dashboard"
            st.session_state.selected_recipe = None
            st.rerun()


def run_cooking_simulation(recipe: dict) -> None:
    """
    Run the cooking simulation with auto-updating progress.
    Stores results in session state and reruns until complete.
    """
    total_seconds = recipe["total_cook_seconds"]
    stages = recipe["stages"]

    if not st.session_state.get("cook_start_time"):
        st.session_state.cook_start_time = time.time()

    elapsed = time.time() - st.session_state.cook_start_time
    progress = min(100.0, (elapsed / total_seconds) * 100)
    remaining = max(0, int(total_seconds - elapsed))

    stage_emojis = ["🥣", "🔥", "🧂", "🥄", "🍳", "✨", "✅"]
    _, stage_index = get_current_stage(stages, progress)
    emoji = stage_emojis[min(stage_index, len(stage_emojis) - 1)]

    render_cooking_progress(recipe, progress, remaining, emoji)

    if progress < 100:
        time.sleep(0.4)
        st.rerun()
    else:
        st.session_state.workflow_step = "complete"
        st.session_state.total_cook_time = int(elapsed)
        st.rerun()

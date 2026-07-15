"""Manual hardware control page."""

import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parent.parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from frontend.components.ui_helpers import load_css, render_header
from backend.services.cooking_service import get_shared_cooking_service

st.set_page_config(page_title="Manual Control", page_icon="🎮", layout="wide")
load_css()


@st.cache_resource
def get_service():
    return get_shared_cooking_service()


def main() -> None:
    render_header(show_settings=False)
    st.markdown(
        '<p style="color:#c4a882;">Direct control of machine hardware (Manual Mode)</p>',
        unsafe_allow_html=True,
    )

    service = get_service()
    m = service.machine
    is_mock = service.get_status().get("is_mock", False)

    if is_mock:
        st.info("Running in **mock hardware** mode (no Raspberry Pi GPIO).")

    if service.is_running():
        st.warning("A recipe is currently cooking. Stop it before manual control.")
        if st.button("🛑 Emergency Stop", type="primary"):
            service.emergency_stop()
            st.rerun()
        return

    st.markdown("### Mixer Motor")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Mixer ON", use_container_width=True):
            m.stop_main_devices()
            m.mixer_motor.on()
    with c2:
        if st.button("Mixer OFF", use_container_width=True):
            m.mixer_motor.off()

    st.markdown("### Position Motor")
    c3, c4 = st.columns(2)
    with c3:
        if st.button("Forward 180°", use_container_width=True):
            m.stop_main_devices()
            m.position_motor.forward()
    with c4:
        if st.button("Backward 180°", use_container_width=True):
            m.stop_main_devices()
            m.position_motor.backward()

    st.markdown("### Rice Bowl Hydraulic")
    c5, c6, c7 = st.columns(3)
    with c5:
        if st.button("Rice Bowl DOWN", use_container_width=True):
            m.stop_main_devices()
            m.rice_bowl.down()
    with c6:
        if st.button("Rice Bowl UP", use_container_width=True):
            m.stop_main_devices()
            m.rice_bowl.up()
    with c7:
        if st.button("Rice Bowl STOP", use_container_width=True):
            m.rice_bowl.stop()

    st.markdown("### Mixer Hydraulic")
    c8, c9, c10 = st.columns(3)
    with c8:
        if st.button("Mixer DOWN", use_container_width=True):
            m.stop_main_devices()
            m.mixer_hydraulic.down()
    with c9:
        if st.button("Mixer UP", use_container_width=True):
            m.stop_main_devices()
            m.mixer_hydraulic.up()
    with c10:
        if st.button("Mixer STOP", use_container_width=True):
            m.mixer_hydraulic.stop()

    st.markdown("### Electronic Valve")
    c11, c12, c13 = st.columns(3)
    with c11:
        if st.button("Valve OPEN", use_container_width=True):
            m.electronic_valve.open()
    with c12:
        if st.button("Valve CLOSE", use_container_width=True):
            m.electronic_valve.close()
    with c13:
        if st.button("Valve STOP", use_container_width=True):
            m.electronic_valve.stop()

    st.markdown("---")
    if st.button("🛑 STOP EVERYTHING", type="primary", use_container_width=True):
        service.emergency_stop()
        st.success("All devices stopped.")


main()

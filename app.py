import streamlit as st

st.set_page_config(
    page_title="PCB Vision AI",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

from src.auth.auth import validate_session
from src.navigation.sidebar import render_sidebar
from src.screens.dashboard_screen import page_dashboard
from src.screens.live_detection_screen import page_live_camera
from src.screens.login_screen import page_login
from src.screens.manual_detection_screen import page_upload_image
from src.styles.theme import inject_css
from src.utils.logging_utils import setup_logging
from src.utils.session import init_session

setup_logging()
init_session()


def main():
    inject_css()

    if not st.session_state.authenticated:
        page_login()
        return

    if not validate_session():
        return

    page = render_sidebar()

    routes = {
        "Live Detection":    page_live_camera,
        "Manual Inspection": page_upload_image,
        "Analytics":         page_dashboard,
    }
    routes[page]()


if __name__ == "__main__":
    main()

import streamlit as st

st.set_page_config(
    page_title="PCB Vision AI",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

from src.navigation.sidebar import render_sidebar
from src.screens.dashboard_screen import page_dashboard
from src.screens.live_detection_screen import page_live_camera
from src.screens.manual_detection_screen import page_upload_image
from src.styles.theme import inject_css
from src.utils.session import init_session

init_session()


def main():
    inject_css()
    page = render_sidebar()

    routes = {
        "Live Detection":    page_live_camera,
        "Manual Inspection": page_upload_image,
        "Analytics":         page_dashboard,
    }
    routes[page]()


if __name__ == "__main__":
    main()

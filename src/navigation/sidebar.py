import streamlit as st

from src.auth.auth import logout
from src.constants.config import APP_MODEL, APP_VERSION


def render_sidebar() -> str:
    with st.sidebar:
        st.markdown("## 🔬 PCB Vision AI")
        st.caption(f"v{APP_VERSION} — BETA  •  {APP_MODEL} Model")
        st.markdown("---")

        page = st.radio(
            "Navigation",
            ["Live Detection", "Manual Inspection", "Analytics"],
            label_visibility="collapsed",
        )

        st.markdown("---")
        st.markdown("**Settings**")
        st.toggle("Dark Mode", key="dark_mode")

        st.markdown("---")
        st.markdown(
            f"<small>Logged in as <b>{st.session_state.username}</b></small>",
            unsafe_allow_html=True,
        )
        if st.button("Sign Out", use_container_width=True):
            logout()

    return page

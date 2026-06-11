import streamlit as st

SESSION_DEFAULTS = {
    "dark_mode":     True,
    "camera_active": False,
    "camera_error":  None,
}


def init_session():
    for key, value in SESSION_DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = value

import streamlit as st

SESSION_DEFAULTS = {
    "authenticated": False,
    "session_id":    None,
    "login_time":    None,
    "last_activity": None,
    "failed_attempts": 0,
    "username":      None,
    "dark_mode":     True,   # dark-first default
    "camera_active": False,
    "camera_error":  None,
}


def init_session():
    for key, value in SESSION_DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = value

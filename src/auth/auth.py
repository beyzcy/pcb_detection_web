import uuid
from datetime import datetime, timedelta

import streamlit as st
from werkzeug.security import check_password_hash

from src.constants.config import (
    ADMIN_HASH,
    BLOCK_SECONDS,
    MAX_ATTEMPTS,
    SESSION_TIMEOUT,
)
from src.utils.logging_utils import log_event


def verify_password(password: str) -> bool:
    return check_password_hash(ADMIN_HASH, password)


def check_rate_limit() -> bool:
    rl = st.session_state.setdefault("_rate_limit", {"blocked_until": None})
    if rl["blocked_until"] and datetime.now() < rl["blocked_until"]:
        remaining = int((rl["blocked_until"] - datetime.now()).total_seconds())
        st.error(f"Too many failed attempts. Please wait {remaining} seconds.")
        return False
    return True


def login(username: str):
    st.session_state.update(
        authenticated=True,
        session_id=str(uuid.uuid4()),
        login_time=datetime.now(),
        last_activity=datetime.now(),
        username=username,
        failed_attempts=0,
    )
    log_event("LOGIN_SUCCESS", {"username": username})


def logout():
    log_event("LOGOUT", {"username": st.session_state.username})
    st.session_state.clear()
    st.rerun()


def validate_session() -> bool:
    if not st.session_state.authenticated or not st.session_state.session_id:
        return False
    elapsed = (datetime.now() - st.session_state.last_activity).total_seconds()
    if elapsed > SESSION_TIMEOUT:
        st.warning("Your session has expired. Please log in again.")
        logout()
        return False
    st.session_state.last_activity = datetime.now()
    return True

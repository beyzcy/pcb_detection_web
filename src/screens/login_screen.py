from datetime import datetime, timedelta

import streamlit as st

from src.auth.auth import check_rate_limit, login, verify_password
from src.constants.config import BLOCK_SECONDS, MAX_ATTEMPTS
from src.utils.logging_utils import log_event


def page_login():
    _, col, _ = st.columns([1, 1.4, 1])

    with col:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("## 🔬 PCB Vision AI")
        st.markdown("##### Automated PCB Defect Detection System")
        st.markdown("---")

        with st.form("login_form"):
            password = st.text_input("Password", type="password", placeholder="Enter password")
            submitted = st.form_submit_button("Sign In", use_container_width=True)

        if submitted:
            if not check_rate_limit():
                return

            if verify_password(password):
                login("admin")
                st.rerun()
            else:
                st.session_state.failed_attempts += 1
                remaining = MAX_ATTEMPTS - st.session_state.failed_attempts
                log_event("LOGIN_FAILED", {"username": "admin"})

                if remaining > 0:
                    st.error(f"Incorrect password. {remaining} attempt(s) remaining.")
                else:
                    st.session_state["_rate_limit"]["blocked_until"] = (
                        datetime.now() + timedelta(seconds=BLOCK_SECONDS)
                    )
                    st.error(f"Account locked for {BLOCK_SECONDS} seconds.")

        st.markdown("---")
        st.caption("Demo password: **admin123**")

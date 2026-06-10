import streamlit as st

from src.constants.defects import BADGE_MAP


def render_badge(label: str, css_class: str | None = None) -> None:
    cls = css_class or BADGE_MAP.get(label, "badge-blue")
    st.markdown(f'<span class="badge {cls}">{label}</span>', unsafe_allow_html=True)


def render_status_badge(is_live: bool) -> None:
    if is_live:
        st.markdown('<span class="badge badge-green">● LIVE</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="badge badge-red">● OFFLINE</span>', unsafe_allow_html=True)

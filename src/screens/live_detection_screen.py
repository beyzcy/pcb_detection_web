import streamlit as st

from src.components.live.camera_feed import render_camera_feed
from src.components.live.system_metrics import render_system_metrics


def page_live_camera():
    st.markdown("""
        <div class="page-header">
            <div class="page-title">Live Detection</div>
            <div class="page-subtitle">Production Line A1 — Camera 01</div>
        </div>
    """, unsafe_allow_html=True)

    col_feed, col_meta = st.columns([0.65, 0.35])
    with col_feed:
        render_camera_feed()
    with col_meta:
        render_system_metrics()

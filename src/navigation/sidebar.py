import streamlit as st

from src.constants.config import APP_MODEL, APP_VERSION


def render_sidebar() -> str:
    with st.sidebar:
        st.markdown("""
        <div style="margin-bottom:4px;">
            <div style="font-size:0.95rem;font-weight:800;color:#FFFFFF;letter-spacing:-0.01em;">PCB Vision AI</div>
            <div style="font-size:0.65rem;color:#6B8CAE;font-weight:500;">Automated PCB Diagnostics</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")

        page = st.radio(
            "Navigation",
            ["Live Detection", "Manual Inspection", "Analytics"],
            label_visibility="collapsed",
        )

        st.markdown("---")
        st.markdown("**Settings**")
        st.toggle("Dark Mode", key="dark_mode")

        # Model info at bottom
        st.markdown("""
        <div style="margin-top:auto;padding-top:20px;">
            <div class="model-info-card">
                <div class="mi-label">MODEL</div>
                <div class="mi-val">YOLOv12-PCB <span class="mi-badge">v1.2</span></div>
                <div class="mi-label" style="margin-top:10px;">INFERENCE DEVICE</div>
                <div class="mi-val">GPU <span class="dot-green" style="display:inline-block;width:7px;height:7px;border-radius:50%;margin-left:4px;"></span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    return page

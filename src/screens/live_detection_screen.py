import streamlit as st

from src.components.live.camera_feed import render_camera_feed
from src.components.live.system_metrics import render_right_panel
from src.services.detection_service import get_recent_detections


def _top_status_bar():
    recent = get_recent_detections(1)
    confidence = f"{recent.iloc[0]['confidence']:.1%}" if not recent.empty else "—"
    is_live = st.session_state.camera_active

    st.markdown(f"""
    <div class="status-bar">
        <div class="sb-item">
            <span class="sb-dot {"dot-green" if is_live else "dot-gray"}"></span>
            <span class="sb-label">SYSTEM STATUS</span>
            <span class="sb-val {"val-green" if is_live else "val-gray"}">{"ACTIVE" if is_live else "IDLE"}</span>
        </div>
        <div class="sb-sep"></div>
        <div class="sb-item">
            <span class="sb-label">FPS</span>
            <span class="sb-val">{"30" if is_live else "0"}</span>
        </div>
        <div class="sb-sep"></div>
        <div class="sb-item">
            <span class="sb-label">LATENCY</span>
            <span class="sb-val">{"38 ms" if is_live else "— ms"}</span>
        </div>
        <div class="sb-sep"></div>
        <div class="sb-item">
            <span class="sb-label">CAMERA</span>
            <span class="sb-val">CAM-01</span>
        </div>
        <div class="sb-sep"></div>
        <div class="sb-item">
            <span class="sb-label">MODEL</span>
            <span class="sb-val">YOLOv12-PCB</span>
        </div>
        <div class="sb-sep"></div>
        <div class="sb-item">
            <span class="sb-label">AI CONFIDENCE</span>
            <span class="sb-val val-green">{confidence}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def page_live_camera():
    _top_status_bar()

    # Section header with LIVE badge
    is_live = st.session_state.camera_active
    live_badge = '<span class="live-badge">● LIVE</span>' if is_live else '<span class="live-badge-off">○ IDLE</span>'
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:12px;margin:18px 0 14px 0;">
        <span style="font-size:0.75rem;color:#6B8CAE;font-weight:700;letter-spacing:0.1em;">↻</span>
        <span style="font-size:0.85rem;font-weight:700;color:#E8F4FF;letter-spacing:0.06em;text-transform:uppercase;">Live PCB Inspection</span>
        {live_badge}
    </div>
    """, unsafe_allow_html=True)

    col_feed, col_right = st.columns([0.62, 0.38])

    with col_feed:
        render_camera_feed()

    with col_right:
        render_right_panel()

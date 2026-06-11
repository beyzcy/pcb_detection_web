import pandas as pd
import streamlit as st

from src.services.detection_service import annotate_frame, get_camera_frame, run_yolo_detection, get_recent_detections
from src.utils.logging_utils import log_event

_BOARD_ID   = "PCB-2025-06-11-001"
_RESOLUTION = "1280 × 720"

_DEFECT_COLORS = {
    "Short Circuit":     "#FF4069",
    "Open Circuit":      "#FF9100",
    "Solder Bridge":     "#FFD600",
    "Missing Component": "#00A8FF",
}


def render_camera_feed() -> None:
    # Scanner frame
    st.markdown("""
    <div class="scanner-frame">
        <div class="corner corner-tl"></div>
        <div class="corner corner-tr"></div>
        <div class="corner corner-bl"></div>
        <div class="corner corner-br"></div>
    """, unsafe_allow_html=True)

    frame_slot = st.empty()

    if st.session_state.camera_active:
        frame   = get_camera_frame()
        results = run_yolo_detection(frame)
        annotated = annotate_frame(frame, results["detections"])
        frame_slot.image(annotated, use_container_width=True)
        log_event("CAMERA_FRAME", {
            "detections": results["total_detections"],
            "ms":         results["processing_time_ms"],
        })
    else:
        frame_slot.markdown("""
        <div class="stream-offline">
            <div class="stream-offline-icon">⊘</div>
            <div class="stream-offline-title">Stream Offline</div>
            <div class="stream-offline-sub">Press START INSPECTION to begin live detection</div>
        </div>""", unsafe_allow_html=True)

    # Board info bar
    scan_mode  = "CONTINUOUS" if st.session_state.camera_active else "STANDBY"
    dot_class  = "dot-green" if st.session_state.camera_active else "dot-gray"
    st.markdown(f"""
    <div class="board-info-bar">
        <div class="bi-item">
            <span class="bi-label">BOARD ID</span>
            <span class="bi-val">{_BOARD_ID}</span>
        </div>
        <div class="bi-item">
            <span class="bi-label">RESOLUTION</span>
            <span class="bi-val">{_RESOLUTION}</span>
        </div>
        <div class="bi-item">
            <span class="bi-label">SCAN MODE</span>
            <span class="bi-val">
                <span class="{dot_class}" style="display:inline-block;width:7px;height:7px;border-radius:50%;margin-right:5px;vertical-align:middle;"></span>
                {scan_mode}
            </span>
        </div>
    </div>
    </div>""", unsafe_allow_html=True)  # closes scanner-frame

    st.markdown("<br>", unsafe_allow_html=True)

    # Control buttons
    if st.session_state.camera_active:
        b1, b2, b3 = st.columns(3)
        with b1:
            if st.button("⏹  Stop Inspection", use_container_width=True):
                st.session_state.camera_active = False
                st.rerun()
        with b2:
            st.button("⏸  Pause", use_container_width=True)
        with b3:
            st.button("📷  Snapshot", use_container_width=True)
    else:
        if st.button("▶  Start Inspection", use_container_width=True):
            st.session_state.camera_active = True
            st.rerun()

    # Inspection log
    _render_inspection_log()


def _render_inspection_log():
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">Inspection Log</div>', unsafe_allow_html=True)

    recent = get_recent_detections(6)
    if recent.empty:
        st.caption("No log entries yet.")
        return

    # Render each log row individually
    for _, r in recent.iterrows():
        ts = r["timestamp"]
        time_str = ts.strftime("%H:%M:%S") if hasattr(ts, "strftime") else str(ts)
        color = _DEFECT_COLORS.get(r["defect_type"], "#00A8FF")
        conf  = f"{r['confidence']:.0%}"

        col_tag, col_time, col_type, col_conf = st.columns([0.12, 0.2, 0.42, 0.26])
        with col_tag:
            st.markdown('<span class="log-tag tag-detect">[DETECT]</span>', unsafe_allow_html=True)
        with col_time:
            st.markdown(f'<span class="log-time">{time_str}</span>', unsafe_allow_html=True)
        with col_type:
            st.markdown(f'<span class="log-type" style="color:{color};">{r["defect_type"]}</span>', unsafe_allow_html=True)
        with col_conf:
            st.markdown(f'<span class="log-conf">Confidence: <b style="color:{color};">{conf}</b></span>', unsafe_allow_html=True)

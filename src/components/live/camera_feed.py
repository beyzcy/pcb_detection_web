import streamlit as st

from src.services.detection_service import annotate_frame, get_camera_frame, run_yolo_detection
from src.utils.logging_utils import log_event


def render_camera_feed() -> None:
    # Stream offline placeholder or live feed
    frame_slot = st.empty()

    if st.session_state.camera_active:
        frame   = get_camera_frame()
        results = run_yolo_detection(frame)
        annotated = annotate_frame(frame, results["detections"])
        frame_slot.image(annotated, use_container_width=True, caption="Real-time Detection")
        log_event("CAMERA_FRAME", {
            "detections": results["total_detections"],
            "ms":         results["processing_time_ms"],
        })
    else:
        frame_slot.markdown("""
        <div class="stream-offline">
            <div class="stream-offline-icon">⊘</div>
            <div class="stream-offline-title">Stream Offline</div>
            <div class="stream-offline-sub">Press START STREAM to begin live detection</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Control buttons
    if st.session_state.camera_active:
        col_stop, col_refresh = st.columns([0.6, 0.4])
        with col_stop:
            if st.button("⏹  STOP STREAM", use_container_width=True, type="primary"):
                st.session_state.camera_active = False
                st.rerun()
        with col_refresh:
            if st.button("↻ Refresh Frame", use_container_width=True):
                st.rerun()
    else:
        if st.button("▶  START STREAM", use_container_width=True, type="primary"):
            st.session_state.camera_active = True
            st.rerun()

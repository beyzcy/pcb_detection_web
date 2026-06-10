import streamlit as st

from src.services.detection_service import get_recent_detections


def render_system_metrics() -> None:
    # Status cards — AI MODEL / CAMERA / DETECTIONS
    recent_df   = get_recent_detections(1)
    is_live      = st.session_state.camera_active
    detection_count = 0 if recent_df.empty else 1

    st.markdown(f"""
    <div class="status-card">
        <div class="status-card-icon">⚙</div>
        <div class="status-card-label">AI MODEL</div>
        <div class="status-card-value">YOLOv12-PCB</div>
        <div class="status-card-state state-ok">● OK</div>
    </div>

    <div class="status-card">
        <div class="status-card-icon">📷</div>
        <div class="status-card-label">CAMERA</div>
        <div class="status-card-value">{"Line A1 — Cam 01" if is_live else "Offline"}</div>
        <div class="status-card-state {"state-ok" if is_live else "state-off"}">
            {"● LIVE" if is_live else "○ OFFLINE"}
        </div>
    </div>

    <div class="status-card">
        <div class="status-card-icon">✓</div>
        <div class="status-card-label">DETECTIONS</div>
        <div class="status-card-value">{detection_count}</div>
        <div class="status-card-state state-ok">● OK</div>
    </div>
    """, unsafe_allow_html=True)

    # Latest detection detail
    if not recent_df.empty:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-title">Latest Detection</div>', unsafe_allow_html=True)
        r  = recent_df.iloc[0]
        ts = r["timestamp"]
        st.markdown(f"""
        <div class="latest-detection-card">
            <div class="ld-row"><span class="ld-key">Type</span><span class="ld-val">{r['defect_type']}</span></div>
            <div class="ld-row"><span class="ld-key">Confidence</span><span class="ld-val accent">{r['confidence']:.1%}</span></div>
            <div class="ld-row"><span class="ld-key">Time</span><span class="ld-val">{ts.strftime('%H:%M:%S') if hasattr(ts, 'strftime') else str(ts)}</span></div>
        </div>
        """, unsafe_allow_html=True)

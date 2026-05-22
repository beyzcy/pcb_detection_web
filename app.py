"""
PCB Defect Detection System — Streamlit Web UI
YOLOv12 Model + Mock Backend

Starts with mock backend. When the real backend is ready,
replace mock functions in backend_mock.py with real implementations.
"""

import os
import json
import logging
import uuid
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
from werkzeug.security import check_password_hash, generate_password_hash

from backend_mock import (
    draw_boxes_on_image,
    get_camera_frame,
    get_daily_defects,
    get_database_stats,
    get_defect_types_distribution,
    get_recent_detections,
    run_yolo_detection,
    save_analysis_to_database,
)

# ─────────────────────────────────────────────────────────────
# 1. PAGE CONFIG & LOGGING
# ─────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="PCB Vision AI",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/app_security.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# ─────────────────────────────────────────────────────────────
# 2. SESSION STATE
# ─────────────────────────────────────────────────────────────

_SESSION_DEFAULTS = {
    "authenticated": False,
    "session_id": None,
    "login_time": None,
    "last_activity": None,
    "failed_attempts": 0,
    "username": None,
    "dark_mode": False,
    "camera_active": False,
}

for key, value in _SESSION_DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ─────────────────────────────────────────────────────────────
# 3. SECURITY & AUTHENTICATION
# ─────────────────────────────────────────────────────────────

_ADMIN_HASH = generate_password_hash("admin123")
_MAX_ATTEMPTS = 3
_BLOCK_SECONDS = 30
_SESSION_TIMEOUT = 900  # 15 minutes


def _log(event_type: str, details: dict):
    logging.info(json.dumps({"event": event_type, "ts": datetime.now().isoformat(), **details}))


def _check_rate_limit() -> bool:
    rl = st.session_state.setdefault("_rate_limit", {"blocked_until": None})
    if rl["blocked_until"] and datetime.now() < rl["blocked_until"]:
        remaining = int((rl["blocked_until"] - datetime.now()).total_seconds())
        st.error(f"Too many failed attempts. Please wait {remaining} seconds.")
        return False
    return True


def _login(username: str):
    st.session_state.update(
        authenticated=True,
        session_id=str(uuid.uuid4()),
        login_time=datetime.now(),
        last_activity=datetime.now(),
        username=username,
        failed_attempts=0,
    )
    _log("LOGIN_SUCCESS", {"username": username})


def _logout():
    _log("LOGOUT", {"username": st.session_state.username})
    # clear() safely removes widget-bound keys (like dark_mode) without
    # raising StreamlitAPIException from direct assignment after instantiation
    st.session_state.clear()
    st.rerun()


def _validate_session() -> bool:
    if not st.session_state.authenticated or not st.session_state.session_id:
        return False
    elapsed = (datetime.now() - st.session_state.last_activity).total_seconds()
    if elapsed > _SESSION_TIMEOUT:
        st.warning("Your session has expired. Please log in again.")
        _logout()
        return False
    st.session_state.last_activity = datetime.now()
    return True


# ─────────────────────────────────────────────────────────────
# 4. GLOBAL CSS
# ─────────────────────────────────────────────────────────────

def _inject_css():
    dark = st.session_state.dark_mode

    # ── Palette ──────────────────────────────────────────────
    bg      = "#1E202B" if dark else "#F5F7FA"
    card    = "#2D3142" if dark else "#FFFFFF"
    sidebar = "#232530" if dark else "#FFFFFF"
    text    = "#F4F5F7" if dark else "#111827"
    text2   = "#CBD5E1" if dark else "#374151"
    border  = "#3D4058" if dark else "#E2E8F0"
    accent  = "#2563EB"
    muted   = "#94A3B8" if dark else "#6B7280"

    # Buttons — always dark navy bg + white text in both modes
    btn_bg       = "#232530"
    btn_hover_bg = "#2D3142"
    btn_border   = "#3D4058"

    # ── Calendar CSS: ONLY injected in dark mode ──────────────
    # In light mode, config.toml base="light" handles BaseUI
    # natively — injecting CSS on top causes the broken patches.
    if dark:
        # Calendar popup is handled by _inject_dark_calendar_js() via JS
        # (CSS injection cannot beat Styletron's dynamically-added rules).
        # Only the static date input field needs CSS here.
        cal_css = f"""
    [data-testid="stDateInput"] > div,
    [data-testid="stDateInput"] > div > div,
    div[data-baseweb="input"],
    div[data-baseweb="input"] > div {{
        background-color: #232530 !important;
        border-color: #3D4058 !important;
    }}
    [data-testid="stDateInput"] input {{
        background-color: #232530 !important;
        color: #F4F5F7 !important;
        border: 1px solid #3D4058 !important;
        border-radius: 6px !important;
        caret-color: #F4F5F7 !important;
    }}
    div[data-baseweb="input"]:focus-within,
    [data-testid="stDateInput"] input:focus {{
        background-color: #232530 !important;
        border-color: {accent} !important;
        box-shadow: 0 0 0 2px rgba(37,99,235,0.25) !important;
        outline: none !important;
    }}"""
    else:
        # Light mode: only fix the text input field color,
        # leave the popup entirely to Streamlit's native theme
        cal_css = f"""
    [data-testid="stDateInput"] input {{
        background-color: #FFFFFF !important;
        color: #111827 !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 6px !important;
    }}"""

    st.markdown(f"""
    <style>
    /* ══════════════════════════════════════════════
       GLOBAL LAYOUT
    ══════════════════════════════════════════════ */
    html, body,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"] {{
        background-color: {bg} !important;
        color: {text} !important;
    }}
    [data-testid="stMainBlockContainer"],
    section.main > div {{
        background-color: {bg} !important;
    }}

    /* ══════════════════════════════════════════════
       SIDEBAR
    ══════════════════════════════════════════════ */
    [data-testid="stSidebar"],
    [data-testid="stSidebar"] > div:first-child {{
        background-color: {sidebar} !important;
        border-right: 1px solid {border} !important;
    }}
    [data-testid="stSidebar"] * {{
        color: #FFFFFF !important;
    }}

    /* ══════════════════════════════════════════════
       BUTTONS  (st.button / st.form_submit_button)
    ══════════════════════════════════════════════ */
    div[data-testid="stButton"] > button,
    div[data-testid="stFormSubmitButton"] > button {{
        background-color: {btn_bg} !important;
        color: #FFFFFF !important;
        border: 1px solid {btn_border} !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        padding: 0.45rem 1rem !important;
    }}
    div[data-testid="stButton"] > button:hover,
    div[data-testid="stFormSubmitButton"] > button:hover {{
        background-color: {btn_hover_bg} !important;
        border-color: {accent} !important;
        color: #FFFFFF !important;
    }}
    div[data-testid="stButton"] > button:active,
    div[data-testid="stFormSubmitButton"] > button:active {{
        background-color: {accent} !important;
        color: #FFFFFF !important;
    }}
    div[data-testid="stButton"] > button p,
    div[data-testid="stButton"] > button span,
    div[data-testid="stFormSubmitButton"] > button p,
    div[data-testid="stFormSubmitButton"] > button span {{
        color: #FFFFFF !important;
    }}

    /* ══════════════════════════════════════════════
       FILE UPLOADER
       "Browse files" uses data-testid="baseButton-secondary"
       — target both the testid AND the parent container
       to guarantee the override wins over Streamlit's sheet.
    ══════════════════════════════════════════════ */
    [data-testid="stFileUploader"] section {{
        background-color: {card} !important;
        border: 2px dashed {border} !important;
        border-radius: 8px !important;
    }}
    [data-testid="stFileUploader"] section span,
    [data-testid="stFileUploader"] section p,
    [data-testid="stFileUploader"] section small {{
        color: {text} !important;
    }}
    [data-testid="stFileUploader"] label {{
        color: {text} !important;
        font-weight: 600 !important;
    }}
    /* Browse files button — matched by both possible selectors */
    [data-testid="stFileUploader"] button,
    [data-testid="stFileUploadDropzone"] + div button,
    button[data-testid="baseButton-secondary"] {{
        background-color: {btn_bg} !important;
        color: #FFFFFF !important;
        border: 1px solid {btn_border} !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
    }}
    [data-testid="stFileUploader"] button span,
    [data-testid="stFileUploader"] button p,
    button[data-testid="baseButton-secondary"] span,
    button[data-testid="baseButton-secondary"] p {{
        color: #FFFFFF !important;
    }}
    /* SVG upload icon */
    [data-testid="stFileUploader"] button svg *,
    button[data-testid="baseButton-secondary"] svg * {{
        fill: #FFFFFF !important;
        stroke: #FFFFFF !important;
    }}
    [data-testid="stFileUploader"] button:hover,
    button[data-testid="baseButton-secondary"]:hover {{
        background-color: {btn_hover_bg} !important;
        border-color: {accent} !important;
        color: #FFFFFF !important;
    }}

    /* ══════════════════════════════════════════════
       METRICS
    ══════════════════════════════════════════════ */
    [data-testid="stMetric"] {{
        background: {card} !important;
        border: 1px solid {border} !important;
        border-radius: 8px !important;
        padding: 12px 16px !important;
    }}
    [data-testid="stMetricLabel"] > div,
    [data-testid="stMetricLabel"] p {{
        color: {muted} !important;
        font-size: 0.78rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.04em !important;
    }}
    [data-testid="stMetricValue"] > div,
    [data-testid="stMetricValue"] p {{
        color: {text} !important;
        font-size: 1.6rem !important;
        font-weight: 700 !important;
    }}

    /* ══════════════════════════════════════════════
       TEXT — scoped to stMain, never leaks to portals
    ══════════════════════════════════════════════ */
    [data-testid="stMain"] p,
    [data-testid="stMain"] li,
    [data-testid="stMain"] label {{
        color: {text} !important;
    }}
    h1, h2, h3, h4, h5, h6 {{
        color: {text} !important;
    }}
    [data-testid="stMarkdownContainer"] p {{
        color: {text2} !important;
    }}

    /* ══════════════════════════════════════════════
       ALERT / INFO BOXES
    ══════════════════════════════════════════════ */
    [data-testid="stAlert"] {{
        background-color: #DBEAFE !important;
        border-left: 4px solid {accent} !important;
        border-radius: 6px !important;
    }}
    [data-testid="stAlert"] p,
    [data-testid="stAlert"] span {{
        color: #1E40AF !important;
        font-weight: 500 !important;
    }}

    /* ══════════════════════════════════════════════
       TEXT INPUTS
    ══════════════════════════════════════════════ */
    [data-testid="stTextInput"] input {{
        background-color: {card} !important;
        color: {text} !important;
        border: 1px solid {border} !important;
        border-radius: 6px !important;
    }}
    [data-testid="stTextInput"] label {{
        color: {text} !important;
        font-weight: 600 !important;
    }}

    /* ══════════════════════════════════════════════
       DATAFRAME
    ══════════════════════════════════════════════ */
    [data-testid="stDataFrame"] {{
        border: 1px solid {border} !important;
        border-radius: 8px !important;
        overflow: hidden !important;
    }}

    hr {{
        border-color: {border} !important;
    }}

    /* ══════════════════════════════════════════════
       CUSTOM COMPONENTS
    ══════════════════════════════════════════════ */
    .kpi-card {{
        background: {card} !important;
        border: 1px solid {border} !important;
        border-radius: 10px !important;
        padding: 20px 24px !important;
        text-align: center !important;
    }}
    .kpi-value  {{ font-size: 2rem !important; font-weight: 700 !important; color: {accent} !important; line-height: 1.1 !important; }}
    .kpi-label  {{ font-size: 0.78rem !important; color: {muted} !important; margin-top: 4px !important; text-transform: uppercase !important; letter-spacing: 0.05em !important; }}
    .section-title {{
        font-size: 1.05rem !important; font-weight: 700 !important;
        color: {text} !important; padding-bottom: 6px !important;
        border-bottom: 2px solid {accent} !important; margin-bottom: 16px !important;
    }}
    .badge          {{ display: inline-block !important; padding: 3px 12px !important; border-radius: 999px !important; font-size: 0.75rem !important; font-weight: 700 !important; }}
    .badge-green  {{ background: #dcfce7 !important; color: #166534 !important; }}
    .badge-red    {{ background: #fee2e2 !important; color: #991b1b !important; }}
    .badge-yellow {{ background: #fef9c3 !important; color: #854d0e !important; }}
    .badge-blue   {{ background: #dbeafe !important; color: #1e40af !important; }}

    /* ══════════════════════════════════════════════
       CALENDAR (mode-specific block)
    ══════════════════════════════════════════════ */
    {cal_css}

    /* ══════════════════════════════════════════════
       HIDE STREAMLIT CHROME
    ══════════════════════════════════════════════ */
    #MainMenu, footer, [data-testid="stDeployButton"] {{
        visibility: hidden !important;
    }}
    </style>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# 5. LOGIN PAGE
# ─────────────────────────────────────────────────────────────

def page_login():
    _inject_css()
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
            if not _check_rate_limit():
                return

            if check_password_hash(_ADMIN_HASH, password):
                _login("admin")
                st.rerun()
            else:
                st.session_state.failed_attempts += 1
                remaining = _MAX_ATTEMPTS - st.session_state.failed_attempts
                _log("LOGIN_FAILED", {"username": "admin"})

                if remaining > 0:
                    st.error(f"Incorrect password. {remaining} attempt(s) remaining.")
                else:
                    st.session_state["_rate_limit"]["blocked_until"] = (
                        datetime.now() + timedelta(seconds=_BLOCK_SECONDS)
                    )
                    st.error(f"Account locked for {_BLOCK_SECONDS} seconds.")

        st.markdown("---")
        st.caption("Demo password: **admin123**")


# ─────────────────────────────────────────────────────────────
# 6. LIVE CAMERA PAGE
# ─────────────────────────────────────────────────────────────

def page_live_camera():
    st.markdown('<div class="section-title">Live PCB Analysis</div>', unsafe_allow_html=True)

    col_feed, col_meta = st.columns([0.68, 0.32])

    with col_feed:
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("▶ Start", use_container_width=True):
                st.session_state.camera_active = True
        with c2:
            if st.button("⏹ Stop", use_container_width=True):
                st.session_state.camera_active = False
        with c3:
            refresh = st.button("↻ Refresh Frame", use_container_width=True)

        frame_slot = st.empty()

        if st.session_state.camera_active or refresh:
            frame = get_camera_frame()
            results = run_yolo_detection(frame)
            annotated = draw_boxes_on_image(frame, results["detections"])
            frame_slot.image(annotated, use_container_width=True, caption="Real-time Detection")
            _log("CAMERA_FRAME", {
                "detections": results["total_detections"],
                "ms": results["processing_time_ms"],
            })
        else:
            frame_slot.info("Camera is stopped. Press **▶ Start** to begin live detection.")

    with col_meta:
        st.markdown('<div class="section-title">System Metrics</div>', unsafe_allow_html=True)

        status_html = (
            '<span class="badge badge-green">● LIVE</span>'
            if st.session_state.camera_active
            else '<span class="badge badge-red">● OFFLINE</span>'
        )
        st.markdown(status_html, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        m1, m2 = st.columns(2)
        m1.metric("FPS", "30")
        m2.metric("Latency (ms)", "124")
        st.metric("Model", "YOLOv12")

        st.markdown("---")
        st.markdown('<div class="section-title">Latest Detection</div>', unsafe_allow_html=True)

        recent_df = get_recent_detections(1)
        if not recent_df.empty:
            r = recent_df.iloc[0]
            st.write(f"**Type:** {r['defect_type']}")
            st.write(f"**Confidence:** {r['confidence']:.1%}")
            ts = r["timestamp"]
            ts_str = ts.strftime("%H:%M:%S") if hasattr(ts, "strftime") else str(ts)
            st.write(f"**Time:** {ts_str}")
        else:
            st.info("No detections yet.")


# ─────────────────────────────────────────────────────────────
# 7. UPLOAD & ANALYZE PAGE
# ─────────────────────────────────────────────────────────────

_BADGE_MAP = {
    "Short Circuit":     "badge-red",
    "Open Circuit":      "badge-yellow",
    "Solder Bridge":     "badge-yellow",
    "Missing Component": "badge-blue",
}

def page_upload_image():
    st.markdown('<div class="section-title">Upload & Analyze PCB Image</div>', unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "Drag & drop or click to browse",
        type=["jpg", "jpeg", "png"],
        help="Maximum file size: 10 MB",
    )

    if not uploaded:
        st.info("Upload a PCB image to start analysis.")
        return

    if len(uploaded.getvalue()) > 10 * 1024 * 1024:
        st.error("File is too large (max 10 MB).")
        return

    _log("FILE_UPLOADED", {"filename": uploaded.name, "size": len(uploaded.getvalue())})

    original = Image.open(uploaded).convert("RGB")
    image_array = np.array(original)

    with st.spinner("Running YOLOv12 detection…"):
        results = run_yolo_detection(image_array)

    # ── Side-by-side images ──
    col_orig, col_det = st.columns(2)
    with col_orig:
        st.markdown("**Original Image**")
        st.image(original, use_container_width=True)
        st.caption(f"Size: {original.width} × {original.height} px")

    with col_det:
        st.markdown("**Detection Result**")
        if results["detections"]:
            annotated = draw_boxes_on_image(image_array, results["detections"])
            st.image(annotated, use_container_width=True)
        else:
            st.image(original, use_container_width=True)
            st.success("No defects detected — PCB looks good!")
        st.caption(f"Defects found: **{results['total_detections']}**  •  "
                   f"Processing time: **{results['processing_time_ms']} ms**")

    # ── Detection table ──
    st.markdown("---")
    st.markdown('<div class="section-title">Detected Defects</div>', unsafe_allow_html=True)

    if results["detections"]:
        rows = []
        for i, d in enumerate(results["detections"], 1):
            badge_cls = _BADGE_MAP.get(d["type"], "badge-green")
            rows.append({
                "#":          i,
                "Defect Type": d["type"],
                "Confidence":  f"{d['confidence']:.1%}",
                "Bounding Box": f"({d['box'][0]}, {d['box'][1]}) → ({d['box'][2]}, {d['box'][3]})",
                "Area (px²)":  f"{d['area']:,}",
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

        if st.button("💾 Save to Database", use_container_width=False):
            save_analysis_to_database(uploaded.name, results)
            _log("ANALYSIS_SAVED", {"filename": uploaded.name, "detections": len(results["detections"])})
            st.success("Analysis saved to database.")
    else:
        st.info("No defects detected.")


# ─────────────────────────────────────────────────────────────
# 8. DASHBOARD PAGE
# ─────────────────────────────────────────────────────────────

def page_dashboard():
    st.markdown('<div class="section-title">Statistics & Dashboard</div>', unsafe_allow_html=True)

    # ── Date filter ──
    c1, c2, c3 = st.columns([0.28, 0.28, 0.44])
    with c1:
        start_date = st.date_input("From", value=datetime.now().date() - timedelta(days=30))
    with c2:
        end_date = st.date_input("To", value=datetime.now().date())
    with c3:
        st.markdown("<br>", unsafe_allow_html=True)
        st.button("Apply Filter", use_container_width=True)

    if start_date > end_date:
        st.warning("Start date must be before end date.")
        return

    stats = get_database_stats(start_date, end_date)

    # ── KPI row ──
    k1, k2, k3, k4 = st.columns(4)
    kpi_data = [
        (k1, stats["total_analyzed"],             "PCBs Analyzed"),
        (k2, stats["total_defects"],               "Total Defects"),
        (k3, f"{stats['defect_rate']:.1f}%",       "Defect Rate"),
        (k4, f"{stats['avg_processing_time_ms']:.0f} ms", "Avg. Processing Time"),
    ]
    for col, val, label in kpi_data:
        col.markdown(
            f'<div class="kpi-card"><div class="kpi-value">{val}</div>'
            f'<div class="kpi-label">{label}</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Charts ──
    dark = st.session_state.dark_mode
    grid_color  = "rgba(255,255,255,0.08)" if dark else "rgba(0,0,0,0.08)"
    text_color  = "#94A3B8"               if dark else "#6B7280"
    line_color  = "#2563EB"
    bar_color   = "#2563EB"

    ch1, ch2 = st.columns(2)

    with ch1:
        st.markdown('<div class="section-title">Daily Defect Count</div>', unsafe_allow_html=True)
        daily = get_daily_defects(start_date, end_date)
        if daily:
            fig_line = go.Figure(
                go.Scatter(
                    x=list(daily.keys()),
                    y=list(daily.values()),
                    mode="lines+markers",
                    line=dict(color=line_color, width=2),
                    marker=dict(size=4, color=line_color),
                    fill="tozeroy",
                    fillcolor="rgba(37,99,235,0.12)",
                )
            )
            fig_line.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=0, r=0, t=8, b=0),
                height=280,
                xaxis=dict(
                    showgrid=True, gridcolor=grid_color,
                    tickfont=dict(color=text_color, size=10),
                    linecolor=grid_color,
                ),
                yaxis=dict(
                    showgrid=True, gridcolor=grid_color,
                    tickfont=dict(color=text_color, size=10),
                    linecolor=grid_color,
                ),
                showlegend=False,
            )
            st.plotly_chart(fig_line, use_container_width=True)
        else:
            st.info("No data for selected range.")

    with ch2:
        st.markdown('<div class="section-title">Defect Type Distribution</div>', unsafe_allow_html=True)
        dist = get_defect_types_distribution(start_date, end_date)
        if dist:
            fig_bar = go.Figure(
                go.Bar(
                    x=list(dist.keys()),
                    y=list(dist.values()),
                    marker_color=bar_color,
                    marker_line_width=0,
                )
            )
            fig_bar.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=0, r=0, t=8, b=0),
                height=280,
                xaxis=dict(
                    showgrid=False,
                    tickfont=dict(color=text_color, size=10),
                    linecolor=grid_color,
                ),
                yaxis=dict(
                    showgrid=True, gridcolor=grid_color,
                    tickfont=dict(color=text_color, size=10),
                    linecolor=grid_color,
                ),
                showlegend=False,
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("No data for selected range.")

    # ── Recent detections ──
    st.markdown("---")
    st.markdown('<div class="section-title">Recent Detections (last 10)</div>', unsafe_allow_html=True)

    recent_df = get_recent_detections(10)
    if not recent_df.empty:
        display_df = recent_df[["timestamp", "defect_type", "confidence", "filename"]].copy()
        display_df.columns = ["Timestamp", "Defect Type", "Confidence", "File"]
        display_df["Confidence"] = display_df["Confidence"].apply(lambda x: f"{x:.1%}")
        display_df["Timestamp"] = display_df["Timestamp"].apply(
            lambda x: x.strftime("%Y-%m-%d %H:%M") if hasattr(x, "strftime") else str(x)
        )
        st.dataframe(display_df, use_container_width=True, hide_index=True)
    else:
        st.info("No recent detections.")


# ─────────────────────────────────────────────────────────────
# 9. SIDEBAR
# ─────────────────────────────────────────────────────────────

def render_sidebar() -> str:
    with st.sidebar:
        st.markdown("## 🔬 PCB Vision AI")
        st.caption("v1.0 — BETA  •  YOLOv12 Model")
        st.markdown("---")

        page = st.radio(
            "Navigation",
            ["Live Camera", "Upload & Analyze", "Dashboard"],
            label_visibility="collapsed",
        )

        st.markdown("---")
        st.markdown("**Settings**")
        st.toggle("Dark Mode", key="dark_mode")

        st.markdown("---")
        st.markdown(
            f"<small>Logged in as <b>{st.session_state.username}</b></small>",
            unsafe_allow_html=True,
        )
        if st.button("Sign Out", use_container_width=True):
            _logout()

    return page


# ─────────────────────────────────────────────────────────────
# 10. DARK CALENDAR JS FIX
# ─────────────────────────────────────────────────────────────

def _inject_dark_calendar_js():
    """
    CSS cannot reliably override Styletron's dynamically-injected
    calendar styles because Styletron adds new rules AFTER our
    <style> block every time the popup opens, winning source-order ties.
    JS sets inline styles directly — those always beat stylesheet rules.
    window.parent.document works because the component iframe is same-origin.
    """
    components.html(
        """
        <script>
        (function () {
            var BG     = '#2D3142';
            var TEXT   = '#F4F5F7';
            var MUTED  = '#94A3B8';
            var ACCENT = '#2563EB';
            var BORDER = '#3D4058';

            function paint() {
                var doc = window.parent.document;
                var pops = doc.querySelectorAll('[data-baseweb="popover"]');
                if (!pops.length) return;

                pops.forEach(function (pop) {
                    // Paint every node dark first
                    pop.querySelectorAll('*').forEach(function (el) {
                        el.style.setProperty('background-color', BG, 'important');
                        el.style.setProperty('color', TEXT, 'important');
                        el.style.setProperty('border-color', BORDER, 'important');
                    });

                    // Day-of-week headers — muted colour
                    pop.querySelectorAll('[role="columnheader"], [role="columnheader"] *').forEach(function (el) {
                        el.style.setProperty('color', MUTED, 'important');
                    });

                    // All buttons — transparent bg
                    pop.querySelectorAll('button').forEach(function (btn) {
                        btn.style.setProperty('background-color', 'transparent', 'important');
                        btn.style.setProperty('border', 'none', 'important');
                        btn.style.setProperty('color', TEXT, 'important');
                    });

                    // Selected date button — accent
                    pop.querySelectorAll('[aria-selected="true"] button, [aria-selected="true"] button *').forEach(function (el) {
                        el.style.setProperty('background-color', ACCENT, 'important');
                        el.style.setProperty('color', '#FFFFFF', 'important');
                    });

                    // Select dropdowns (month / year)
                    pop.querySelectorAll('select').forEach(function (sel) {
                        sel.style.setProperty('background-color', BG, 'important');
                        sel.style.setProperty('color', TEXT, 'important');
                    });
                });
            }

            // Re-paint whenever the DOM changes (popup opens / navigates months)
            var observer = new MutationObserver(paint);
            observer.observe(window.parent.document.body, {
                childList: true,
                subtree: true
            });

            // Continuous poll covers any timing gaps
            setInterval(paint, 150);
        })();
        </script>
        """,
        height=0,
    )


# ─────────────────────────────────────────────────────────────
# 11. MAIN
# ─────────────────────────────────────────────────────────────

def main():
    if not st.session_state.authenticated:
        page_login()
        return

    if not _validate_session():
        return

    _inject_css()
    if st.session_state.dark_mode:
        _inject_dark_calendar_js()
    page = render_sidebar()

    if page == "Live Camera":
        page_live_camera()
    elif page == "Upload & Analyze":
        page_upload_image()
    elif page == "Dashboard":
        page_dashboard()


if __name__ == "__main__":
    main()

import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, timedelta

from src.services.detection_service import get_recent_detections, get_database_stats
from src.constants.colors import ACCENT

_DEFECT_COLORS = {
    "Short Circuit":     "#FF4069",
    "Open Circuit":      "#FF9100",
    "Solder Bridge":     "#FFD600",
    "Missing Component": "#00A8FF",
}


def render_right_panel() -> None:
    stats = get_database_stats(
        datetime.now().date() - timedelta(days=30),
        datetime.now().date(),
    )
    total    = stats["total_analyzed"]
    defects  = stats["total_defects"]
    passed   = max(0, total - defects)
    accuracy = max(0.0, 100.0 - stats["defect_rate"])

    # Detection summary — 4 mini cards
    st.markdown('<div class="section-title">Detection Summary</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div class="mini-stat-card">
            <div class="ms-label">TOTAL PCBS</div>
            <div class="ms-value">{total:,}</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="mini-stat-card ms-green">
            <div class="ms-label">PASSED</div>
            <div class="ms-value" style="color:#00E676;">{passed:,}</div>
            <div class="ms-sub">{(passed/max(total,1)*100):.1f}%</div>
        </div>""", unsafe_allow_html=True)

    c3, c4 = st.columns(2)
    with c3:
        st.markdown(f"""
        <div class="mini-stat-card ms-red">
            <div class="ms-label">FAILED</div>
            <div class="ms-value" style="color:#FF1744;">{defects:,}</div>
            <div class="ms-sub">{stats["defect_rate"]:.1f}%</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="mini-stat-card ms-accent">
            <div class="ms-label">ACCURACY</div>
            <div class="ms-value" style="color:{ACCENT};">{accuracy:.1f}%</div>
            <div class="ms-sub">+1.2% ↑</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Live defects list — one st.markdown per row
    st.markdown('<div class="section-title">Live Defects</div>', unsafe_allow_html=True)
    recent = get_recent_detections(6)

    if recent.empty:
        st.caption("No defects detected yet.")
    else:
        for _, r in recent.iterrows():
            ts = r["timestamp"]
            time_str = ts.strftime("%H:%M:%S") if hasattr(ts, "strftime") else str(ts)
            color = _DEFECT_COLORS.get(r["defect_type"], ACCENT)
            conf  = f"{r['confidence']:.0%}"
            st.markdown(f"""
            <div class="ld-list-row">
                <span class="ld-dot" style="background:{color};box-shadow:0 0 5px {color};"></span>
                <span class="ld-time">{time_str}</span>
                <span class="ld-type" style="color:{color};">{r['defect_type']}</span>
                <span class="ld-conf">{conf}</span>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Confidence over time mini chart
    st.markdown('<div class="section-title">Confidence Over Time</div>', unsafe_allow_html=True)
    if not recent.empty:
        fig = go.Figure(go.Scatter(
            x=[r["timestamp"].strftime("%H:%M") if hasattr(r["timestamp"], "strftime") else str(r["timestamp"])
               for _, r in recent.iterrows()],
            y=[r["confidence"] * 100 for _, r in recent.iterrows()],
            mode="lines+markers",
            line=dict(color=ACCENT, width=2),
            marker=dict(size=5, color=ACCENT),
            fill="tozeroy",
            fillcolor="rgba(0,168,255,0.06)",
        ))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=4, b=0),
            height=150,
            yaxis=dict(range=[0, 105], tickfont=dict(color="#6B8CAE", size=9),
                       gridcolor="rgba(30,58,95,0.5)", showgrid=True),
            xaxis=dict(tickfont=dict(color="#6B8CAE", size=9), showgrid=False),
            showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.caption("Run inspection to see confidence trend.")

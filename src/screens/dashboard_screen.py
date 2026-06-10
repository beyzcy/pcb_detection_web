from datetime import datetime, timedelta

import streamlit as st

from src.components.dashboard.daily_chart import render_daily_chart
from src.components.dashboard.distribution_chart import render_distribution_chart
from src.components.dashboard.kpi_row import render_kpi_row
from src.components.dashboard.recent_table import render_recent_table
from src.services.detection_service import (
    get_daily_defects,
    get_database_stats,
    get_defect_types_distribution,
    get_recent_detections,
)

_RANGE_DAYS = {"7d": 7, "30d": 30, "90d": 90}


def page_dashboard():
    st.markdown("""
        <div class="page-header">
            <div class="page-title">Analytics &amp; Reports</div>
            <div class="page-subtitle">Production performance overview</div>
        </div>
    """, unsafe_allow_html=True)

    # ── Production Status hero card ──────────────────────────
    stats_all = get_database_stats(
        datetime.now().date() - timedelta(days=30),
        datetime.now().date(),
    )
    accuracy = max(0, 100 - stats_all["defect_rate"])
    throughput = round(stats_all["total_analyzed"] / 30 / 24, 1)

    st.markdown(f"""
    <div class="hero-card">
        <div class="hero-label">PRODUCTION STATUS</div>
        <div class="hero-title">System Operational</div>
        <div class="hero-sub">All subsystems running — YOLOv12 active</div>
        <div style="display:flex;gap:10px;margin-top:14px;flex-wrap:wrap;">
            <span class="badge badge-green">● {accuracy:.1f}% ACCURACY</span>
            <span class="badge badge-blue">{throughput:.1f}/HR</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Time range selector ──────────────────────────────────
    col_tabs, _, col_refresh = st.columns([0.5, 0.35, 0.15])
    with col_tabs:
        selected = st.radio(
            "range", list(_RANGE_DAYS.keys()),
            horizontal=True,
            label_visibility="collapsed",
            index=1,
        )
    with col_refresh:
        st.markdown("<br>", unsafe_allow_html=True)
        st.button("↻ Refresh", use_container_width=True)

    days = _RANGE_DAYS[selected]
    start_date = datetime.now().date() - timedelta(days=days)
    end_date   = datetime.now().date()

    stats = get_database_stats(start_date, end_date)

    # ── KPI row ──────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    render_kpi_row(stats)
    st.markdown("<br>", unsafe_allow_html=True)

    # ── Charts ───────────────────────────────────────────────
    ch1, ch2 = st.columns(2)
    with ch1:
        render_daily_chart(get_daily_defects(start_date, end_date))
    with ch2:
        render_distribution_chart(get_defect_types_distribution(start_date, end_date))

    st.markdown("---")
    render_recent_table(get_recent_detections(10))

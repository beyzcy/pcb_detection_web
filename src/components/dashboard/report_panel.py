"""
stats_engine.compute_weekly_report() ve CSV export'u Streamlit'e taşır.
dashboard_widget.py'nin haftalık özet + export davranışının karşılığı.
"""
import streamlit as st


def render_report_panel(report: dict, defect_csv: str, stats_csv: str) -> None:
    """
    Haftalık özet rapor + CSV indirme butonları.

    report    : detection_service.get_weekly_report() dönüşü
    defect_csv: detection_service.export_defect_logs_csv() dönüşü
    stats_csv : detection_service.export_daily_stats_csv() dönüşü
    """
    st.markdown('<div class="section-title">Weekly Report</div>', unsafe_allow_html=True)

    if not report:
        st.info("stats_engine not available — check extern/pcb-defect-detection.")
        return

    trend_raw = report.get("trend", "→ stable")
    if trend_raw.startswith("↑"):
        trend_color, trend_badge = "#FF3232", "badge-red"
    elif trend_raw.startswith("↓"):
        trend_color, trend_badge = "#00C864", "badge-green"
    else:
        trend_color, trend_badge = "#6B8CAE", "badge-gray"

    most_common = report.get("most_common_defect", "N/A")

    st.markdown(f"""
    <div style="
        background: rgba(13,25,48,0.7);
        border: 1px solid rgba(0,168,255,0.15);
        border-radius: 10px;
        padding: 16px 20px;
        display: flex;
        flex-direction: column;
        gap: 10px;
    ">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
            <span style="color:#6B8CAE; font-size:0.72rem; letter-spacing:0.08em; font-weight:700;">
                PERIOD
            </span>
            <span style="color:#E8F4FF; font-size:0.82rem; font-weight:600;">
                {report.get("period", "—")}
            </span>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
            <span style="color:#6B8CAE; font-size:0.72rem; letter-spacing:0.08em; font-weight:700;">
                WEEK-OVER-WEEK
            </span>
            <span style="color:{trend_color}; font-size:0.82rem; font-weight:700;">
                {trend_raw}
            </span>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
            <span style="color:#6B8CAE; font-size:0.72rem; letter-spacing:0.08em; font-weight:700;">
                MOST COMMON DEFECT
            </span>
            <span style="color:#FFD200; font-size:0.82rem; font-weight:600;">
                {most_common}
            </span>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
            <span style="color:#6B8CAE; font-size:0.72rem; letter-spacing:0.08em; font-weight:700;">
                DEFECT RATE
            </span>
            <span style="color:#E8F4FF; font-size:0.82rem;">
                {report.get("defect_rate", 0):.1f}%
            </span>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
            <span style="color:#6B8CAE; font-size:0.72rem; letter-spacing:0.08em; font-weight:700;">
                AVG INFERENCE
            </span>
            <span style="color:#E8F4FF; font-size:0.82rem;">
                {report.get("avg_inference_ms", 0):.1f} ms
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Type breakdown mini-table
    breakdown = report.get("type_breakdown", [])
    if breakdown:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-title" style="font-size:0.7rem;">Defect Breakdown</div>', unsafe_allow_html=True)
        for item in breakdown:
            pct = item.get("pct", 0)
            bar_w = int(pct * 1.4)
            st.markdown(f"""
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:4px;">
                <span style="color:#6B8CAE; font-size:0.72rem; width:110px; flex-shrink:0;">
                    {item["defect_type"]}
                </span>
                <div style="flex:1; background:rgba(30,58,95,0.5); border-radius:3px; height:6px;">
                    <div style="width:{bar_w}%; background:#00A8FF; height:6px; border-radius:3px;"></div>
                </div>
                <span style="color:#E8F4FF; font-size:0.72rem; width:40px; text-align:right;">
                    {pct:.0f}%
                </span>
            </div>
            """, unsafe_allow_html=True)

    # CSV export butonları
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title" style="font-size:0.7rem;">Export Data</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.download_button(
            label="⬇ Defect Logs",
            data=defect_csv,
            file_name="defect_logs.csv",
            mime="text/csv",
            use_container_width=True,
        )
    with c2:
        st.download_button(
            label="⬇ Daily Stats",
            data=stats_csv,
            file_name="daily_stats.csv",
            mime="text/csv",
            use_container_width=True,
        )

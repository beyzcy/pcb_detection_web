import streamlit as st

from src.components.ui.kpi_card import render_kpi_card


def render_kpi_row(stats: dict) -> None:
    k1, k2, k3, k4 = st.columns(4)
    kpi_data = [
        (k1, stats["total_analyzed"],                          "PCBs Analyzed"),
        (k2, stats["total_defects"],                           "Total Defects"),
        (k3, f"{stats['defect_rate']:.1f}%",                   "Defect Rate"),
        (k4, f"{stats['avg_processing_time_ms']:.0f} ms",      "Avg. Processing Time"),
    ]
    for col, val, label in kpi_data:
        with col:
            render_kpi_card(val, label)

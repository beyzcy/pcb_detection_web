import streamlit as st
import plotly.graph_objects as go

from src.constants.colors import ACCENT


def render_daily_chart(daily: dict) -> None:
    st.markdown('<div class="section-title">Daily Defect Trend</div>', unsafe_allow_html=True)
    if not daily:
        st.info("No data for selected range.")
        return

    dark = st.session_state.get("dark_mode", True)
    grid_color  = "rgba(30,58,95,0.6)" if dark else "rgba(0,0,0,0.08)"
    text_color  = "#6B8CAE" if dark else "#6B7280"
    plotly_tmpl = "plotly_dark" if dark else "plotly_white"

    fig = go.Figure(
        go.Scatter(
            x=list(daily.keys()),
            y=list(daily.values()),
            mode="lines+markers",
            line=dict(color=ACCENT, width=2.5),
            marker=dict(size=6, color=ACCENT, line=dict(color="#060B14", width=2)),
            fill="tozeroy",
            fillcolor="rgba(0,168,255,0.08)",
        )
    )
    fig.update_layout(
        template=plotly_tmpl,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=8, b=0),
        height=260,
        xaxis=dict(showgrid=True, gridcolor=grid_color, tickfont=dict(color=text_color, size=10), linecolor="rgba(0,0,0,0)"),
        yaxis=dict(showgrid=True, gridcolor=grid_color, tickfont=dict(color=text_color, size=10), linecolor="rgba(0,0,0,0)"),
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True)

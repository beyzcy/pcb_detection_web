import streamlit as st
import plotly.graph_objects as go

from src.constants.colors import ACCENT, DANGER, WARNING


def render_distribution_chart(dist: dict) -> None:
    st.markdown('<div class="section-title">Defect Distribution</div>', unsafe_allow_html=True)
    if not dist:
        st.info("No data for selected range.")
        return

    dark = st.session_state.get("dark_mode", True)
    grid_color  = "rgba(30,58,95,0.6)" if dark else "rgba(0,0,0,0.08)"
    text_color  = "#6B8CAE" if dark else "#6B7280"
    plotly_tmpl = "plotly_dark" if dark else "plotly_white"

    colors = [DANGER, "#FF6B35", WARNING, ACCENT, "#A855F7"]
    bar_colors = [colors[i % len(colors)] for i in range(len(dist))]

    fig = go.Figure(
        go.Bar(
            x=list(dist.keys()),
            y=list(dist.values()),
            marker_color=bar_colors,
            marker_line_width=0,
            opacity=0.85,
        )
    )
    fig.update_layout(
        template=plotly_tmpl,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=8, b=0),
        height=260,
        xaxis=dict(showgrid=False, tickfont=dict(color=text_color, size=10), linecolor="rgba(0,0,0,0)"),
        yaxis=dict(showgrid=True, gridcolor=grid_color, tickfont=dict(color=text_color, size=10), linecolor="rgba(0,0,0,0)"),
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True)

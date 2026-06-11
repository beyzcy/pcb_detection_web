import streamlit as st
import plotly.graph_objects as go

from src.constants.colors import ACCENT, DANGER


def render_weekly_trend_chart(weeks: list[dict]) -> None:
    """
    dashboard_widget._refresh_line_chart() Streamlit karşılığı.
    weeks: [{"week_start", "total_scanned", "total_faulty", ...}, ...]  (4 hafta)
    """
    st.markdown('<div class="section-title">Weekly Trend — Scanned vs Faulty</div>', unsafe_allow_html=True)

    if not weeks or all(w.get("total_scanned", 0) == 0 for w in weeks):
        st.info("No weekly data yet.")
        return

    dark = st.session_state.get("dark_mode", True)
    grid_color  = "rgba(30,58,95,0.6)" if dark else "rgba(0,0,0,0.08)"
    text_color  = "#6B8CAE" if dark else "#6B7280"
    plotly_tmpl = "plotly_dark" if dark else "plotly_white"

    labels   = [f"W{i+1}  {w['week_start']}" for i, w in enumerate(weeks)]
    scanned  = [w.get("total_scanned", 0) for w in weeks]
    faulty   = [w.get("total_faulty",  0) for w in weeks]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=labels, y=scanned,
        name="Scanned",
        mode="lines+markers",
        line=dict(color=ACCENT, width=2.5),
        marker=dict(size=7, color=ACCENT),
        fill="tozeroy",
        fillcolor="rgba(0,168,255,0.07)",
    ))
    fig.add_trace(go.Scatter(
        x=labels, y=faulty,
        name="Faulty",
        mode="lines+markers",
        line=dict(color=DANGER, width=2.5, dash="dot"),
        marker=dict(size=7, color=DANGER),
    ))

    fig.update_layout(
        template=plotly_tmpl,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=8, b=0),
        height=260,
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02,
            xanchor="right", x=1,
            font=dict(size=11, color=text_color),
        ),
        xaxis=dict(
            showgrid=False,
            tickfont=dict(color=text_color, size=10),
            linecolor="rgba(0,0,0,0)",
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor=grid_color,
            tickfont=dict(color=text_color, size=10),
            linecolor="rgba(0,0,0,0)",
        ),
    )

    st.plotly_chart(fig, use_container_width=True)

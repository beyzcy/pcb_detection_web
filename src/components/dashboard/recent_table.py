import pandas as pd
import streamlit as st


def render_recent_table(df: pd.DataFrame) -> None:
    st.markdown('<div class="section-title">Recent Detections</div>', unsafe_allow_html=True)
    if df.empty:
        st.info("No recent detections.")
        return

    display_df = df[["timestamp", "defect_type", "confidence", "filename"]].copy()
    display_df.columns = ["Timestamp", "Defect Type", "Confidence", "File"]
    display_df["Confidence"] = display_df["Confidence"].apply(lambda x: f"{x:.1%}")
    display_df["Timestamp"] = display_df["Timestamp"].apply(
        lambda x: x.strftime("%Y-%m-%d %H:%M") if hasattr(x, "strftime") else str(x)
    )
    st.dataframe(display_df, use_container_width=True, hide_index=True)

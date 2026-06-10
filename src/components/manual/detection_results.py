import pandas as pd
import streamlit as st
from PIL import Image

from src.constants.defects import BADGE_MAP
from src.services.detection_service import annotate_frame, save_analysis
from src.utils.logging_utils import log_event


def render_detection_results(original: Image.Image, results: dict, filename: str) -> None:
    col_orig, col_det = st.columns(2)

    with col_orig:
        st.markdown("**Original Image**")
        st.image(original, use_container_width=True)
        st.caption(f"Size: {original.width} × {original.height} px")

    with col_det:
        st.markdown("**Detection Result**")
        if results["detections"]:
            import numpy as np
            annotated = annotate_frame(np.array(original), results["detections"])
            st.image(annotated, use_container_width=True)
        else:
            st.image(original, use_container_width=True)
            st.success("No defects detected — PCB looks good!")
        st.caption(
            f"Defects found: **{results['total_detections']}** • "
            f"Processing time: **{results['processing_time_ms']} ms**"
        )

    st.markdown("---")
    st.markdown('<div class="section-title">Detected Defects</div>', unsafe_allow_html=True)

    if results["detections"]:
        rows = []
        for i, d in enumerate(results["detections"], 1):
            rows.append({
                "#":            i,
                "Defect Type":  d["type"],
                "Confidence":   f"{d['confidence']:.1%}",
                "Bounding Box": f"({d['box'][0]}, {d['box'][1]}) → ({d['box'][2]}, {d['box'][3]})",
                "Area (px²)":   f"{d['area']:,}",
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

        if st.button("💾 Save to Database", use_container_width=False):
            save_analysis(filename, results)
            log_event("ANALYSIS_SAVED", {"filename": filename, "detections": len(results["detections"])})
            st.success("Analysis saved to database.")
    else:
        st.info("No defects detected.")

import streamlit as st

from src.components.manual.detection_results import render_detection_results
from src.components.manual.image_uploader import render_image_uploader
from src.services.detection_service import run_yolo_detection


def page_upload_image():
    st.markdown("""
        <div class="page-header">
            <div class="page-title">Manual Inspection</div>
            <div class="page-subtitle">Upload or capture a PCB image for AI defect analysis</div>
        </div>
    """, unsafe_allow_html=True)

    result = render_image_uploader()
    if result is None:
        return

    original, image_array, uploaded = result

    with st.spinner("Running YOLOv12 detection…"):
        results = run_yolo_detection(image_array)

    render_detection_results(original, results, uploaded.name)

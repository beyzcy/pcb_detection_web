import numpy as np
import streamlit as st
from PIL import Image

from src.constants.config import MAX_UPLOAD_BYTES
from src.utils.logging_utils import log_event


def render_image_uploader() -> tuple | None:
    """Returns (original_image, image_array, uploaded_file) or None if no valid file."""
    uploaded = st.file_uploader(
        "PCB Image",
        type=["jpg", "jpeg", "png"],
        help="Maximum file size: 10 MB",
        label_visibility="collapsed",
    )

    if not uploaded:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-state-icon">🖼</div>
            <div class="empty-state-title">No PCB Image Selected</div>
            <div class="empty-state-sub">Upload a PCB image to begin AI defect analysis</div>
        </div>
        """, unsafe_allow_html=True)
        return None

    if len(uploaded.getvalue()) > MAX_UPLOAD_BYTES:
        st.error("File is too large (max 10 MB).")
        return None

    log_event("FILE_UPLOADED", {"filename": uploaded.name, "size": len(uploaded.getvalue())})
    original = Image.open(uploaded).convert("RGB")
    return original, np.array(original), uploaded

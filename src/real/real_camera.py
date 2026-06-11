"""
Real camera backend using OpenCV + DroidCam.

Based on rubukk/pcb CAMERA_SETUP.md:
  - DroidCam WiFi: set CAMERA_SOURCE=http://192.168.x.x:4747/video in .env
  - DroidCam USB : set CAMERA_SOURCE=1  (device index, usually 1 when built-in is 0)
  - Built-in webcam (default): CAMERA_SOURCE=0
"""
import os

import numpy as np

try:
    import cv2
    _CV2_AVAILABLE = True
except ImportError:
    _CV2_AVAILABLE = False

_CAMERA_SOURCE = os.getenv("CAMERA_SOURCE", "0")
_cap = None


def _open_capture():
    src = int(_CAMERA_SOURCE) if _CAMERA_SOURCE.lstrip("-").isdigit() else _CAMERA_SOURCE
    cap = cv2.VideoCapture(src)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # minimize latency per rubukk/pcb buffering tip
    if not cap.isOpened():
        raise RuntimeError(
            f"Cannot open camera source '{_CAMERA_SOURCE}'. "
            "Set CAMERA_SOURCE in .env — see .env.example for DroidCam options."
        )
    return cap


def get_camera_stream(frame_id: int = 0) -> np.ndarray:
    global _cap
    if not _CV2_AVAILABLE:
        raise RuntimeError("opencv-python is not installed. Run: pip install opencv-python")
    if _cap is None or not _cap.isOpened():
        _cap = _open_capture()
    ret, frame = _cap.read()
    if not ret:
        _cap.release()
        _cap = None
        raise RuntimeError(
            f"Failed to read frame from camera source '{_CAMERA_SOURCE}'. "
            "Check that DroidCam is running and connected."
        )
    return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


def release_camera() -> None:
    global _cap
    if _cap is not None:
        _cap.release()
        _cap = None

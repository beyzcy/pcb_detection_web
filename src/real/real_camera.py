"""
Real camera backend using OpenCV.

When CAMERA_SOURCE is not set, automatically prefers DroidCam / Loopback
Video Device over the built-in webcam. Override in .env:
  CAMERA_SOURCE=0                           → built-in webcam
  CAMERA_SOURCE=1                           → DroidCam USB (device index)
  CAMERA_SOURCE=http://192.168.x.x:4747/video → DroidCam WiFi
"""
import logging
import os
import platform

import numpy as np

try:
    import cv2
    _CV2_AVAILABLE = True
except ImportError:
    _CV2_AVAILABLE = False

_log = logging.getLogger(__name__)

_CAMERA_SOURCE_ENV = os.getenv("CAMERA_SOURCE")
_AUTO_DETECT = _CAMERA_SOURCE_ENV is None


# ── DroidCam auto-detection ───────────────────────────────────────────────────

def _find_droidcam_index() -> int | None:
    """
    Return the OpenCV capture index of the first DroidCam / Loopback Video
    Device found, or None if none is connected.
    """
    system = platform.system()

    # Linux: read kernel sysfs device names (no extra deps needed)
    if system == "Linux":
        import pathlib
        for p in sorted(pathlib.Path("/sys/class/video4linux").glob("video*")):
            try:
                name = (p / "name").read_text().strip().lower()
                if "loopback" in name or "droidcam" in name:
                    idx = int(p.name.replace("video", ""))
                    _log.info("DroidCam detected: /dev/video%d (%s)", idx, name)
                    return idx
            except Exception:
                continue
        return None

    # Windows: DirectShow enumeration via pygrabber (matches OpenCV index order)
    if system == "Windows":
        try:
            from pygrabber.dshow_graph import FilterGraph  # type: ignore[import]
            names = FilterGraph().get_input_devices()
            for i, name in enumerate(names):
                if "loopback" in name.lower() or "droidcam" in name.lower():
                    _log.info("DroidCam detected via pygrabber: index %d (%s)", i, name)
                    return i
            return None
        except ImportError:
            pass

        # Fallback: ffmpeg DirectShow device list (also matches OpenCV order)
        try:
            import subprocess
            proc = subprocess.run(
                ["ffmpeg", "-f", "dshow", "-list_devices", "true", "-i", "dummy"],
                capture_output=True, text=True, timeout=5,
            )
            output = proc.stdout + proc.stderr
            video_devices: list[str] = []
            in_video_section = False
            for line in output.splitlines():
                ll = line.lower()
                if "directshow video devices" in ll:
                    in_video_section = True
                elif "directshow audio devices" in ll:
                    in_video_section = False
                elif in_video_section and '"' in line:
                    try:
                        video_devices.append(line.split('"')[1])
                    except IndexError:
                        pass
            for i, name in enumerate(video_devices):
                if "loopback" in name.lower() or "droidcam" in name.lower():
                    _log.info("DroidCam detected via ffmpeg: index %d (%s)", i, name)
                    return i
        except Exception:
            pass

    return None


# ── Capture helpers ───────────────────────────────────────────────────────────

def _resolve_source() -> int | str:
    """Return the camera source (int index or URL string) to open."""
    if not _AUTO_DETECT:
        src = _CAMERA_SOURCE_ENV
        return int(src) if src.lstrip("-").isdigit() else src  # type: ignore[arg-type]

    droidcam = _find_droidcam_index()
    if droidcam is not None:
        return droidcam

    _log.debug("No DroidCam found; falling back to built-in camera (index 0)")
    return 0


_cap = None


def _open_capture():
    src = _resolve_source()
    cap = cv2.VideoCapture(src)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # minimize latency
    if not cap.isOpened():
        raise RuntimeError(
            f"Cannot open camera source '{src}'. "
            "Set CAMERA_SOURCE in .env — see .env.example for DroidCam options."
        )
    return cap


def get_camera_stream(frame_id: int = 0) -> np.ndarray:
    global _cap
    if not _CV2_AVAILABLE:
        raise RuntimeError("opencv-python is not installed. Run: pip install opencv-python")
    if _cap is None or not _cap.isOpened():
        _cap = _open_capture()

    # Flush buffer to get the latest frame, then retrieve
    _cap.grab()
    ret, frame = _cap.retrieve()

    if not ret or frame is None:
        # Single frame drop is normal for virtual cameras — retry once
        import time as _time
        _time.sleep(0.05)
        ret, frame = _cap.read()

    if not ret or frame is None:
        _cap.release()
        _cap = None
        raise RuntimeError(
            "DroidCam bağlantısı kesildi. "
            "Telefonda DroidCam uygulamasının açık olduğunu kontrol et."
        )
    return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


def release_camera() -> None:
    global _cap
    if _cap is not None:
        _cap.release()
        _cap = None

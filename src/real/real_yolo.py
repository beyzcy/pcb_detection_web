"""
Real YOLO backend using ultralytics.

Model weights: copy model/best.pt from rubukk/pcb into the models/ directory,
or set YOLO_MODEL_PATH in .env to the absolute path of your .pt file.
"""
import os
import time

import numpy as np

try:
    from ultralytics import YOLO as _YOLO
    _ULTRALYTICS_AVAILABLE = True
except ImportError:
    _ULTRALYTICS_AVAILABLE = False

_MODEL_PATH = os.getenv("YOLO_MODEL_PATH", "models/best.pt")


class RealYOLOModel:
    def __init__(self, model_path: str = _MODEL_PATH):
        if not _ULTRALYTICS_AVAILABLE:
            raise RuntimeError("ultralytics is not installed. Run: pip install ultralytics")
        self.model = _YOLO(model_path)
        self.model_path = model_path
        self.is_loaded = True

    def predict(self, frame: np.ndarray, confidence_threshold: float = 0.5) -> dict:
        t0 = time.perf_counter()
        results = self.model(frame, conf=confidence_threshold, verbose=False)
        elapsed_ms = int((time.perf_counter() - t0) * 1000)

        detections = []
        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                label = r.names[cls_id]
                detections.append({
                    "type":       label,
                    "confidence": round(conf, 2),
                    "box":        [x1, y1, x2, y2],
                    "center":     [(x1 + x2) // 2, (y1 + y2) // 2],
                    "area":       (x2 - x1) * (y2 - y1),
                })

        return {
            "detections":           detections,
            "model_name":           "YOLOv12",
            "confidence_threshold": confidence_threshold,
            "total_detections":     len(detections),
            "processing_time_ms":   elapsed_ms,
        }


_model: RealYOLOModel | None = None


def get_yolo_model() -> RealYOLOModel:
    global _model
    if _model is None:
        _model = RealYOLOModel()
    return _model

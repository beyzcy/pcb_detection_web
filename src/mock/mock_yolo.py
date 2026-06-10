import random

import numpy as np

from src.constants.defects import DEFECT_TYPES


class MockYOLOModel:
    """
    Mock YOLOv12 Model.

    INTEGRATION: Replace with:
        from your_backend.models.yolo_detector import YOLODetector
        model = YOLODetector(model_path="models/yolo12.pt")
    """

    def __init__(self, model_path: str = "models/yolo12.pt"):
        self.model_path = model_path
        self.is_loaded = True

    def predict(self, frame: np.ndarray, confidence_threshold: float = 0.5) -> dict:
        """
        Mock prediction.

        INTEGRATION: Replace body with:
            results = self.model(frame)
            return self._parse_results(results)
        """
        h, w = frame.shape[:2]
        num_detections = random.randint(0, 3)

        detections = []
        for _ in range(num_detections):
            if random.random() > 0.3:
                defect_type = random.choice(DEFECT_TYPES)
                confidence = random.uniform(0.85, 0.99)

                if confidence >= confidence_threshold:
                    x1 = random.randint(50, max(51, w - 200))
                    y1 = random.randint(50, max(51, h - 200))
                    x2 = x1 + random.randint(100, 300)
                    y2 = y1 + random.randint(100, 300)

                    detections.append({
                        "type":       defect_type,
                        "confidence": float(f"{confidence:.2f}"),
                        "box":        [x1, y1, x2, y2],
                        "center":     [(x1 + x2) // 2, (y1 + y2) // 2],
                        "area":       (x2 - x1) * (y2 - y1),
                    })

        return {
            "detections":          detections,
            "model_name":          "YOLOv12",
            "confidence_threshold": confidence_threshold,
            "total_detections":    len(detections),
            "processing_time_ms":  random.randint(50, 300),
        }


_yolo_model: MockYOLOModel | None = None


def get_yolo_model() -> MockYOLOModel:
    global _yolo_model
    if _yolo_model is None:
        _yolo_model = MockYOLOModel()
    return _yolo_model

"""
Mock Backend Functions
Used until the real backend is ready.
When the backend is complete, replace these with real implementations.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random
from PIL import Image, ImageDraw

# ─────────────────────────────────────────────────────────────
# 1. YOLO MODEL MOCK
# ─────────────────────────────────────────────────────────────

class MockYOLOModel:
    """
    Mock YOLOv12 Model

    INTEGRATION: When backend is ready, replace with:
        from your_backend.models.yolo_detector import YOLODetector
        model = YOLODetector(model_path="models/yolo12.pt")
    """

    def __init__(self, model_path="models/yolo12.pt"):
        self.model_path = model_path
        self.defect_types = [
            "Short Circuit",
            "Open Circuit",
            "Solder Bridge",
            "Missing Component",
            "Good PCB"
        ]
        self.is_loaded = True

    def predict(self, frame: np.ndarray, confidence_threshold: float = 0.5):
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
                defect_type = random.choice(self.defect_types[:-1])
                confidence = random.uniform(0.85, 0.99)

                if confidence >= confidence_threshold:
                    x1 = random.randint(50, max(51, w - 200))
                    y1 = random.randint(50, max(51, h - 200))
                    x2 = x1 + random.randint(100, 300)
                    y2 = y1 + random.randint(100, 300)

                    detections.append({
                        "type": defect_type,
                        "confidence": float(f"{confidence:.2f}"),
                        "box": [x1, y1, x2, y2],
                        "center": [(x1 + x2) // 2, (y1 + y2) // 2],
                        "area": (x2 - x1) * (y2 - y1)
                    })

        return {
            "detections": detections,
            "model_name": "YOLOv12",
            "confidence_threshold": confidence_threshold,
            "total_detections": len(detections),
            "processing_time_ms": random.randint(50, 300)
        }


_yolo_model = None

def get_yolo_model() -> MockYOLOModel:
    global _yolo_model
    if _yolo_model is None:
        _yolo_model = MockYOLOModel()
    return _yolo_model


# ─────────────────────────────────────────────────────────────
# 2. CAMERA MOCK
# ─────────────────────────────────────────────────────────────

def generate_mock_pcb_image(width: int = 1280, height: int = 720) -> np.ndarray:
    """
    Generate a mock PCB image.

    INTEGRATION: Replace with:
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        return frame if ret else None
    """
    img = Image.new("RGB", (width, height), color=(20, 25, 35))
    draw = ImageDraw.Draw(img)

    for _ in range(20):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        draw.line([(x1, y1), (x2, y2)], fill=(100, 150, 200), width=2)

    for _ in range(15):
        x = random.randint(50, width - 50)
        y = random.randint(50, height - 50)
        size = random.randint(20, 60)
        draw.rectangle([x, y, x + size, y + size], outline=(200, 200, 100))

    for _ in range(30):
        x = random.randint(50, width - 50)
        y = random.randint(50, height - 50)
        draw.ellipse([x, y, x + 15, y + 15], fill=(150, 150, 150))

    return np.array(img)


def get_camera_stream(frame_id: int = 0) -> np.ndarray:
    """Return a live camera frame (mock)."""
    return generate_mock_pcb_image()


# ─────────────────────────────────────────────────────────────
# 3. DATABASE MOCK
# ─────────────────────────────────────────────────────────────

class MockDatabase:
    """
    Mock in-memory database.

    INTEGRATION: Replace with:
        from backend.database.db_manager import DatabaseManager
        db = DatabaseManager(db_path="pcb_system.db")
    """

    def __init__(self):
        self.analyses: list[dict] = []
        self.detections: list[dict] = []
        self._generate_mock_data()

    def _generate_mock_data(self):
        defect_types = ["Short Circuit", "Open Circuit", "Solder Bridge", "Missing Component"]

        for day_offset in range(30, 0, -1):
            timestamp = datetime.now() - timedelta(days=day_offset)
            num_analyses = random.randint(3, 8)

            for _ in range(num_analyses):
                analysis_id = len(self.analyses) + 1
                num_defects = random.randint(0, 3)

                self.analyses.append({
                    "id": analysis_id,
                    "filename": f"pcb_sample_{analysis_id}.jpg",
                    "timestamp": timestamp,
                    "total_detections": num_defects,
                    "processing_time_ms": random.randint(50, 300),
                    "model_version": "YOLOv12"
                })

                for _ in range(num_defects):
                    self.detections.append({
                        "id": len(self.detections) + 1,
                        "analysis_id": analysis_id,
                        "defect_type": random.choice(defect_types),
                        "confidence": random.uniform(0.80, 0.99),
                        "bbox": [
                            random.randint(50, 1200),
                            random.randint(50, 700),
                            random.randint(200, 1400),
                            random.randint(200, 800)
                        ]
                    })

    def get_stats(self, start_date, end_date) -> dict:
        filtered = [
            a for a in self.analyses
            if start_date <= a["timestamp"].date() <= end_date
        ]
        total_analyzed = len(filtered)
        total_defects = sum(a["total_detections"] for a in filtered)
        defect_rate = (total_defects / max(total_analyzed, 1)) * 100
        avg_time = sum(a["processing_time_ms"] for a in filtered) / max(total_analyzed, 1)

        return {
            "total_analyzed": total_analyzed,
            "total_defects": total_defects,
            "defect_rate": defect_rate,
            "avg_processing_time_ms": avg_time
        }

    def get_daily_defect_counts(self, start_date, end_date) -> dict:
        daily: dict[str, int] = {}
        for analysis in self.analyses:
            if start_date <= analysis["timestamp"].date() <= end_date:
                date_str = analysis["timestamp"].strftime("%Y-%m-%d")
                daily[date_str] = daily.get(date_str, 0) + analysis["total_detections"]

        current = start_date
        while current <= end_date:
            daily.setdefault(current.strftime("%Y-%m-%d"), 0)
            current += timedelta(days=1)

        return dict(sorted(daily.items()))

    def get_defect_distribution(self, start_date, end_date) -> dict:
        dist: dict[str, int] = {}
        for detection in self.detections:
            analysis = next(
                (a for a in self.analyses if a["id"] == detection["analysis_id"]),
                None
            )
            if analysis and start_date <= analysis["timestamp"].date() <= end_date:
                dt = detection["defect_type"]
                dist[dt] = dist.get(dt, 0) + 1
        return dist

    def get_recent_detections(self, limit: int = 10) -> list[dict]:
        results = []
        for detection in reversed(self.detections[-limit * 2:]):
            analysis = next(
                (a for a in self.analyses if a["id"] == detection["analysis_id"]),
                None
            )
            if analysis:
                results.append({
                    "id": detection["id"],
                    "timestamp": analysis["timestamp"],
                    "defect_type": detection["defect_type"],
                    "confidence": detection["confidence"],
                    "filename": analysis["filename"]
                })
            if len(results) >= limit:
                break
        return results

    def save_analysis(self, filename: str, results: dict, timestamp=None) -> int:
        timestamp = timestamp or datetime.now()
        analysis_id = len(self.analyses) + 1

        self.analyses.append({
            "id": analysis_id,
            "filename": filename,
            "timestamp": timestamp,
            "total_detections": len(results.get("detections", [])),
            "processing_time_ms": results.get("processing_time_ms", 0),
            "model_version": "YOLOv12"
        })

        for detection in results.get("detections", []):
            self.detections.append({
                "id": len(self.detections) + 1,
                "analysis_id": analysis_id,
                "defect_type": detection["type"],
                "confidence": detection["confidence"],
                "bbox": detection["box"]
            })

        return analysis_id


_mock_db: MockDatabase | None = None

def get_database() -> MockDatabase:
    global _mock_db
    if _mock_db is None:
        _mock_db = MockDatabase()
    return _mock_db


# ─────────────────────────────────────────────────────────────
# 4. UTILITY FUNCTIONS
# ─────────────────────────────────────────────────────────────

_DEFECT_COLORS = {
    "Short Circuit":    (255, 50,  50),
    "Open Circuit":     (255, 165, 0),
    "Solder Bridge":    (255, 220, 0),
    "Missing Component":(0,  165, 255),
}

def draw_boxes_on_image(image: np.ndarray, detections: list) -> np.ndarray:
    """Draw bounding boxes with labels onto an image."""
    pil_image = Image.fromarray(image.astype("uint8"))
    draw = ImageDraw.Draw(pil_image)

    for detection in detections:
        x1, y1, x2, y2 = detection["box"]
        defect_type = detection["type"]
        confidence = detection["confidence"]
        color = _DEFECT_COLORS.get(defect_type, (0, 255, 0))

        draw.rectangle([x1, y1, x2, y2], outline=color, width=3)

        label = f"{defect_type} ({confidence:.0%})"
        text_x = x1
        text_y = max(y1 - 22, 4)
        draw.rectangle([text_x, text_y, text_x + len(label) * 7 + 6, text_y + 18], fill=color)
        draw.text((text_x + 3, text_y + 2), label, fill=(255, 255, 255))

    return np.array(pil_image)


# ─────────────────────────────────────────────────────────────
# 5. PUBLIC API
# ─────────────────────────────────────────────────────────────

def run_yolo_detection(frame: np.ndarray) -> dict:
    return get_yolo_model().predict(frame)

def get_camera_frame() -> np.ndarray:
    return get_camera_stream()

def get_database_stats(start_date, end_date) -> dict:
    return get_database().get_stats(start_date, end_date)

def get_daily_defects(start_date, end_date) -> dict:
    return get_database().get_daily_defect_counts(start_date, end_date)

def get_defect_types_distribution(start_date, end_date) -> dict:
    return get_database().get_defect_distribution(start_date, end_date)

def get_recent_detections(limit: int = 10) -> pd.DataFrame:
    return pd.DataFrame(get_database().get_recent_detections(limit))

def save_analysis_to_database(filename: str, results: dict) -> int:
    return get_database().save_analysis(filename, results)

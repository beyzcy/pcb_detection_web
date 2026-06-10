"""
Service layer — the only boundary between UI and backend.
Swap mock imports for real implementations here when the backend is ready.
"""

import numpy as np
import pandas as pd

from src.mock.mock_camera import get_camera_stream
from src.mock.mock_database import get_database
from src.mock.mock_yolo import get_yolo_model
from src.utils.image_utils import draw_boxes_on_image


def run_yolo_detection(frame: np.ndarray) -> dict:
    return get_yolo_model().predict(frame)


def get_camera_frame() -> np.ndarray:
    return get_camera_stream()


def annotate_frame(frame: np.ndarray, detections: list) -> np.ndarray:
    return draw_boxes_on_image(frame, detections)


def get_database_stats(start_date, end_date) -> dict:
    return get_database().get_stats(start_date, end_date)


def get_daily_defects(start_date, end_date) -> dict:
    return get_database().get_daily_defect_counts(start_date, end_date)


def get_defect_types_distribution(start_date, end_date) -> dict:
    return get_database().get_defect_distribution(start_date, end_date)


def get_recent_detections(limit: int = 10) -> pd.DataFrame:
    return pd.DataFrame(get_database().get_recent_detections(limit))


def save_analysis(filename: str, results: dict) -> int:
    return get_database().save_analysis(filename, results)

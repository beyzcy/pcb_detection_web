import random
from datetime import datetime, timedelta

from src.constants.defects import DEFECT_TYPES


class MockDatabase:
    """
    Mock in-memory database.

    INTEGRATION: Replace with:
        from backend.database.db_manager import DatabaseManager
        db = DatabaseManager(db_path="pcb_system.db")
    """

    def __init__(self):
        self.analyses:  list[dict] = []
        self.detections: list[dict] = []
        self._generate_mock_data()

    def _generate_mock_data(self):
        for day_offset in range(30, 0, -1):
            timestamp = datetime.now() - timedelta(days=day_offset)
            for _ in range(random.randint(3, 8)):
                analysis_id = len(self.analyses) + 1
                num_defects = random.randint(0, 3)

                self.analyses.append({
                    "id":                analysis_id,
                    "filename":          f"pcb_sample_{analysis_id}.jpg",
                    "timestamp":         timestamp,
                    "total_detections":  num_defects,
                    "processing_time_ms": random.randint(50, 300),
                    "model_version":     "YOLOv12",
                })

                for _ in range(num_defects):
                    self.detections.append({
                        "id":          len(self.detections) + 1,
                        "analysis_id": analysis_id,
                        "defect_type": random.choice(DEFECT_TYPES),
                        "confidence":  random.uniform(0.80, 0.99),
                        "bbox": [
                            random.randint(50, 1200),
                            random.randint(50, 700),
                            random.randint(200, 1400),
                            random.randint(200, 800),
                        ],
                    })

    def get_stats(self, start_date, end_date) -> dict:
        filtered = [
            a for a in self.analyses
            if start_date <= a["timestamp"].date() <= end_date
        ]
        total_analyzed = len(filtered)
        total_defects  = sum(a["total_detections"] for a in filtered)
        defect_rate    = (total_defects / max(total_analyzed, 1)) * 100
        avg_time       = sum(a["processing_time_ms"] for a in filtered) / max(total_analyzed, 1)
        return {
            "total_analyzed":        total_analyzed,
            "total_defects":         total_defects,
            "defect_rate":           defect_rate,
            "avg_processing_time_ms": avg_time,
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
                None,
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
                None,
            )
            if analysis:
                results.append({
                    "id":          detection["id"],
                    "timestamp":   analysis["timestamp"],
                    "defect_type": detection["defect_type"],
                    "confidence":  detection["confidence"],
                    "filename":    analysis["filename"],
                })
            if len(results) >= limit:
                break
        return results

    def save_analysis(self, filename: str, results: dict, timestamp=None) -> int:
        timestamp   = timestamp or datetime.now()
        analysis_id = len(self.analyses) + 1

        self.analyses.append({
            "id":                analysis_id,
            "filename":          filename,
            "timestamp":         timestamp,
            "total_detections":  len(results.get("detections", [])),
            "processing_time_ms": results.get("processing_time_ms", 0),
            "model_version":     "YOLOv12",
        })

        for detection in results.get("detections", []):
            self.detections.append({
                "id":          len(self.detections) + 1,
                "analysis_id": analysis_id,
                "defect_type": detection["type"],
                "confidence":  detection["confidence"],
                "bbox":        detection["box"],
            })

        return analysis_id


_mock_db: MockDatabase | None = None


def get_database() -> MockDatabase:
    global _mock_db
    if _mock_db is None:
        _mock_db = MockDatabase()
    return _mock_db

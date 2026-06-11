"""
Adapter wrapping sumeyyeturk/pcb-defect-detection's database.py and stats_engine.py.
"""
import os
import sys
from datetime import date, datetime, timedelta

_EXTERN = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "..", "extern", "pcb-defect-detection")
)
if os.path.isdir(_EXTERN) and _EXTERN not in sys.path:
    sys.path.insert(0, _EXTERN)

try:
    import database as _db
    _db.init_db()
    with _db.get_connection() as _conn:
        _conn.executemany(
            "INSERT OR IGNORE INTO defect_types (name, description, severity) VALUES (?, ?, ?)",
            [("Mouse Bite", "Small notch removed from PCB edge", 2)],
        )
        _conn.commit()
    _DB_AVAILABLE = True
except ImportError:
    _DB_AVAILABLE = False

try:
    import stats_engine as _stats
    _STATS_AVAILABLE = True
except ImportError:
    _STATS_AVAILABLE = False


class RealDatabase:
    def __init__(self):
        if not _DB_AVAILABLE:
            raise RuntimeError(
                "sumeyyeturk/pcb-defect-detection not found.\n"
                "Run: git clone https://github.com/sumeyyeturk/pcb-defect-detection "
                "extern/pcb-defect-detection"
            )

    # ── Read: dashboard stats ──────────────────────────────────────────────

    def get_stats(self, start_date: date, end_date: date) -> dict:
        days = (end_date - start_date).days + 1
        series = _db.get_daily_series(days=days)
        total_analyzed = sum(r.get("total_scanned", 0) for r in series)
        total_defects  = sum(r.get("total_faulty",  0) for r in series)
        defect_rate    = (total_defects / max(total_analyzed, 1)) * 100
        avg_time       = sum(r.get("avg_inference_ms", 0) for r in series) / max(len(series), 1)
        return {
            "total_analyzed":         total_analyzed,
            "total_defects":          total_defects,
            "defect_rate":            defect_rate,
            "avg_processing_time_ms": avg_time,
        }

    def get_daily_defect_counts(self, start_date: date, end_date: date) -> dict:
        days = (end_date - start_date).days + 1
        series = _db.get_daily_series(days=days)
        result: dict[str, int] = {}
        cur = start_date
        while cur <= end_date:
            result[cur.isoformat()] = 0
            cur += timedelta(days=1)
        for row in series:
            d = row.get("date", "")
            if d in result:
                result[d] = row.get("total_faulty", 0)
        return dict(sorted(result.items()))

    def get_defect_distribution(self, start_date: date, end_date: date) -> dict:
        days = (end_date - start_date).days + 1
        dist = _db.get_defect_type_distribution(days=days)
        return {item["defect_type"]: item["count"] for item in dist}

    def get_recent_detections(self, limit: int = 10) -> list[dict]:
        logs = _db.get_recent_logs(limit=limit)
        result = []
        for row in logs:
            ts = row.get("timestamp")
            if isinstance(ts, str):
                try:
                    ts = datetime.fromisoformat(ts)
                except ValueError:
                    pass
            result.append({
                "id":          row.get("id"),
                "timestamp":   ts,
                "defect_type": row.get("defect_type"),
                "confidence":  row.get("confidence"),
                "filename":    row.get("image_path", ""),
            })
        return result

    # ── Read: weekly trend (dashboard_widget._refresh_line_chart mantığı) ──

    def get_weekly_trend(self) -> list[dict]:
        """Son 4 haftanın scanned / faulty verisi — haftalık trend grafiği için."""
        today = date.today()
        weeks = []
        for i in range(3, -1, -1):
            ws = today - timedelta(days=today.weekday() + 7 * i)
            weeks.append(_db.get_weekly_stats(week_start=ws))
        return weeks

    # ── Read: stats_engine rapor + CSV ────────────────────────────────────

    def get_weekly_report(self) -> dict:
        if not _STATS_AVAILABLE:
            return {}
        return _stats.compute_weekly_report()

    def export_defect_logs_csv(self) -> str:
        if not _STATS_AVAILABLE:
            return ""
        return _stats.export_defect_logs_csv()

    def export_daily_stats_csv(self) -> str:
        if not _STATS_AVAILABLE:
            return ""
        return _stats.export_daily_stats_csv()

    # ── Write ──────────────────────────────────────────────────────────────

    def save_analysis(self, filename: str, results: dict, timestamp=None) -> int:
        detections   = results.get("detections", [])
        inference_ms = float(results.get("processing_time_ms", 0))
        if detections:
            for det in detections:
                x1, y1, x2, y2 = det["box"]
                _db.log_defect(
                    defect_type=det["type"],
                    confidence=det["confidence"],
                    bbox=(x1, y1, x2 - x1, y2 - y1),
                    image_path=filename,
                    camera_id=1,
                    inference_ms=inference_ms,
                )
        else:
            _db.log_scan(scanned_count=1, inference_ms=inference_ms)
        return 0


_real_db: RealDatabase | None = None


def get_database() -> RealDatabase:
    global _real_db
    if _real_db is None:
        _real_db = RealDatabase()
    return _real_db

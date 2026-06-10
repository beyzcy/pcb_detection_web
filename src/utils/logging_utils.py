import json
import logging
import os
from datetime import datetime

from src.constants.config import LOG_DIR, LOG_FILE


def setup_logging():
    os.makedirs(LOG_DIR, exist_ok=True)
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )


def log_event(event_type: str, details: dict):
    logging.info(json.dumps({"event": event_type, "ts": datetime.now().isoformat(), **details}))

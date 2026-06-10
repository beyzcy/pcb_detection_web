from werkzeug.security import generate_password_hash

ADMIN_HASH      = generate_password_hash("admin123")
MAX_ATTEMPTS    = 3
BLOCK_SECONDS   = 30
SESSION_TIMEOUT = 900  # 15 minutes

APP_TITLE        = "PCB Vision AI"
APP_VERSION      = "1.0"
APP_MODEL        = "YOLOv12"
LOG_DIR          = "logs"
LOG_FILE         = "logs/app_security.log"
MAX_UPLOAD_BYTES = 10 * 1024 * 1024  # 10 MB

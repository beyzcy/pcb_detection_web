# PCB Vision AI — YOLOv12 PCB Defect Detection System

A Streamlit web application for real-time PCB (Printed Circuit Board) defect detection using a YOLOv12 model. Built as a graduation project with a mock backend that is ready for real backend integration.

---

## Features

- **Live Camera Analysis** — Real-time PCB inspection with bounding box overlay
- **Image Upload & Analysis** — Upload PCB images and get instant defect detection results
- **Statistics Dashboard** — Interactive charts (daily defect counts, defect type distribution) and KPI metrics
- **Light / Dark Mode** — Full theme support with a sidebar toggle
- **Secure Login** — Password authentication with rate limiting and session timeout
- **Audit Logging** — Security events logged to `logs/app_security.log`

---

## Project Structure

```
pcb_detection_web/
├── app.py                  # Main Streamlit application
├── backend_mock.py         # Mock backend (camera, YOLO model, database)
├── requirements.txt        # Python dependencies
├── .gitignore
├── .streamlit/
│   └── config.toml         # Streamlit theme configuration
└── logs/                   # Auto-created on first run
    └── app_security.log
```

---

## Detected Defect Types

| Defect | Description |
|---|---|
| Short Circuit | Unintended conductive path between traces |
| Open Circuit | Broken trace or missing connection |
| Solder Bridge | Excess solder joining adjacent pads |
| Missing Component | Component absent from its footprint |

---

## Getting Started

### 1. Clone the repository

```bash
git clone <repo-url>
cd pcb_detection_web
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the app

```bash
python -m streamlit run app.py
```

Then open **http://localhost:8501** in your browser.

**Demo login password:** `admin123`

---

## Backend Integration Guide

The app currently runs with a mock backend (`backend_mock.py`). When the real backend is ready, replace the following mock functions:

### Camera
```python
# backend_mock.py — get_camera_stream()
# Replace:
return generate_mock_pcb_image()

# With:
import cv2
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
return frame if ret else None
```

### YOLO Model
```python
# backend_mock.py — MockYOLOModel.predict()
# Replace the mock return with:
results = self.model(frame)   # ultralytics YOLO
return self._parse_results(results)
```

### Database
```python
# backend_mock.py — MockDatabase
# Replace in-memory lists with:
import sqlite3
self.conn = sqlite3.connect("pcb_system.db")
# Then run SQL queries as needed
```

All function signatures and return formats remain identical — `app.py` imports do not need to change.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit 1.57 |
| Charts | Plotly |
| AI Model | YOLOv12 (ultralytics) |
| Image Processing | Pillow, NumPy |
| Authentication | Werkzeug password hashing |
| Database (mock) | In-memory Python lists |
| Database (real) | SQLite |

---

## Security Features

- Bcrypt password hashing via Werkzeug
- Rate limiting — 3 failed attempts trigger a 30-second lockout
- Session timeout — automatic logout after 15 minutes of inactivity
- All login/logout events written to `logs/app_security.log`
- File upload size limit — 10 MB max

---

## Notes

- The `logs/` directory is created automatically on first run and is excluded from git via `.gitignore`
- The `models/` directory should contain `yolo12.pt` when using the real backend
- All paths in the codebase are relative — no machine-specific configuration required

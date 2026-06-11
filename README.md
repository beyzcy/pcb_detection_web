# PCB Vision AI — YOLOv12 PCB Defect Detection System

Real-time PCB (Printed Circuit Board) defect detection web application built with Streamlit and YOLOv12. Features live camera inspection via DroidCam, manual image upload analysis, and an analytics dashboard backed by SQLite.

---

## Features

- **Live Camera Inspection** — Real-time PCB analysis with bounding box overlay (DroidCam / USB webcam)
- **Manual Image Upload** — Upload PCB images and get instant YOLOv12 detection results
- **Analytics Dashboard** — Daily trend, defect distribution, 4-week trend chart, weekly report, CSV export
- **Light / Dark Mode** — Full theme support with sidebar toggle

---

## Detected Defect Types

| Defect | Severity |
|---|---|
| Short Circuit | High |
| Open Circuit | High |
| Missing Hole | Medium |
| Mouse Bite | Medium |
| Spur | Medium |
| Excess Copper | Medium |

---

## Project Structure

```
pcb_detection_web/
├── app.py                          # Streamlit entry point
├── requirements.txt
├── .env.example                    # Copy to .env and fill in
├── .streamlit/config.toml
├── models/                         # Place best.pt here (not in git)
├── extern/                         # External repos — clone manually (not in git)
│   ├── pcb-defect-detection/       # sumeyyeturk — database.py, stats_engine.py
│   └── pcb/                        # rubukk — model weights reference
└── src/
    ├── real/                       # Real backend implementations
    │   ├── real_camera.py          # OpenCV + DroidCam auto-detection
    │   ├── real_yolo.py            # ultralytics YOLOv12
    │   └── real_database.py        # Adapter for sumeyyeturk/pcb-defect-detection
    ├── services/
    │   └── detection_service.py    # Service layer (UI ↔ Backend boundary)
    ├── components/
    │   ├── dashboard/              # Analytics widgets
    │   ├── live/                   # Camera feed + system metrics
    │   └── manual/                 # Image upload + results
    ├── screens/                    # Page-level Streamlit screens
    ├── constants/                  # Colors, config, defect types
    ├── styles/                     # CSS theme injection
    └── utils/                      # Logging, image drawing, session
```

---

## Setup

### 1. Clone the repository

```bash
git clone <repo-url>
cd pcb_detection_web
```

### 2. Clone external dependencies

```bash
git clone https://github.com/sumeyyeturk/pcb-defect-detection extern/pcb-defect-detection
```

### 3. Add the YOLO model

Copy `best.pt` into the `models/` directory:

```
models/best.pt
```

### 4. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment

```bash
cp .env.example .env
```

Edit `.env`:

```env
# DroidCam via USB (recommended — index after built-in webcam)
CAMERA_SOURCE=1

# DroidCam via Wi-Fi
# CAMERA_SOURCE=http://192.168.x.x:4747/video

# Built-in webcam only
# CAMERA_SOURCE=0

YOLO_MODEL_PATH=models/best.pt
```

### 6. Run

```bash
streamlit run app.py
```

Open **http://localhost:8501**

---

## Camera Setup (DroidCam)

1. Install **DroidCam** on your phone ([Android](https://play.google.com/store/apps/details?id=com.dev47apps.droidcam) / [iOS](https://apps.apple.com/us/app/droidcam-webcam-pc/id1510258100))
2. Install the [DroidCam PC client](https://www.dev47apps.com/droidcam/windows/)
3. Connect phone via USB or Wi-Fi through the PC client
4. Set `CAMERA_SOURCE=1` in `.env` (USB) or the HTTP URL (Wi-Fi)
5. Start the app — the camera feed will appear when you press **Start Inspection**

See [`extern/pcb/CAMERA_SETUP.md`](extern/pcb/CAMERA_SETUP.md) for detailed instructions.

---

## Tech Stack

| Layer | Technology |
|---|---|
| UI Framework | Streamlit |
| Charts | Plotly |
| AI Model | YOLOv12 (ultralytics) |
| Camera | OpenCV + DroidCam |
| Image Processing | Pillow, NumPy |
| Authentication | Werkzeug (bcrypt) |
| Stats Engine | stats_engine.py (sumeyyeturk/pcb-defect-detection) |


---

## Notes

- File upload limit: 10 MB max

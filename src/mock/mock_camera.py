import random

import numpy as np
from PIL import Image, ImageDraw


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

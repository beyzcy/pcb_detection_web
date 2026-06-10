import numpy as np
from PIL import Image, ImageDraw

from src.constants.defects import DEFECT_COLORS


def draw_boxes_on_image(image: np.ndarray, detections: list) -> np.ndarray:
    pil_image = Image.fromarray(image.astype("uint8"))
    draw = ImageDraw.Draw(pil_image)

    for detection in detections:
        x1, y1, x2, y2 = detection["box"]
        defect_type = detection["type"]
        confidence = detection["confidence"]
        color = DEFECT_COLORS.get(defect_type, (0, 255, 0))

        draw.rectangle([x1, y1, x2, y2], outline=color, width=3)

        label = f"{defect_type} ({confidence:.0%})"
        text_x = x1
        text_y = max(y1 - 22, 4)
        draw.rectangle([text_x, text_y, text_x + len(label) * 7 + 6, text_y + 18], fill=color)
        draw.text((text_x + 3, text_y + 2), label, fill=(255, 255, 255))

    return np.array(pil_image)

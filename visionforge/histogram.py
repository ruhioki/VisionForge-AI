"""Histogram analysis and rendering utilities built with OpenCV."""

from pathlib import Path

import cv2
import numpy as np

from visionforge.image_info import load_image


def save_histogram(path: str | Path, output: str | Path, width: int = 768, height: int = 420) -> Path:
    """Save a readable RGB histogram image without requiring Matplotlib."""
    if width < 256 or height < 160:
        raise ValueError("Histogram width must be at least 256 and height at least 160.")
    image = load_image(path)
    canvas = np.full((height, width, 3), 250, dtype=np.uint8)
    left, right, top, bottom = 48, width - 18, 22, height - 42
    cv2.rectangle(canvas, (left, top), (right, bottom), (225, 225, 225), thickness=1)
    plot_w, plot_h = right - left, bottom - top
    for tick in range(5):
        y = bottom - round(tick * plot_h / 4)
        cv2.line(canvas, (left, y), (right, y), (220, 220, 220), 1)
    colors = [(255, 90, 70), (70, 170, 70), (70, 90, 235)]
    for channel, color in enumerate(colors):
        hist = cv2.calcHist([image], [channel], None, [256], [0, 256]).flatten()
        peak = float(hist.max()) or 1.0
        points = []
        for value, count in enumerate(hist):
            x = left + round(value * plot_w / 255)
            y = bottom - round(float(count) / peak * (plot_h - 4))
            points.append((x, y))
        cv2.polylines(canvas, [np.asarray(points, dtype=np.int32)], False, color, 2, cv2.LINE_AA)
    cv2.putText(canvas, "RGB channel distribution", (left, height - 12), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (40, 40, 40), 1, cv2.LINE_AA)
    output_path = Path(output).expanduser()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if not cv2.imwrite(str(output_path), canvas):
        raise ValueError(f"Could not save histogram image: {output_path}")
    return output_path

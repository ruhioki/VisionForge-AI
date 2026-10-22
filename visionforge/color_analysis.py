"""Simple color statistics for images using OpenCV and NumPy."""

from pathlib import Path
from typing import Any

import cv2
import numpy as np

from visionforge.image_info import load_image


def analyze_colors(path: str | Path) -> dict[str, Any]:
    """Return mean BGR/RGB channel values and basic brightness statistics."""
    image = load_image(path)
    means = cv2.mean(image)[:3]  # OpenCV stores color images in BGR order.
    rgb_means = means[::-1]
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return {
        "path": str(Path(path).expanduser()),
        "mean_rgb": {
            "red": round(float(rgb_means[0]), 2),
            "green": round(float(rgb_means[1]), 2),
            "blue": round(float(rgb_means[2]), 2),
        },
        "brightness": {
            "mean": round(float(np.mean(gray)), 2),
            "minimum": int(np.min(gray)),
            "maximum": int(np.max(gray)),
        },
    }

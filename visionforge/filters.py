"""Common image filters with explicit input validation."""

from pathlib import Path

import cv2
import numpy as np

from visionforge.image_info import load_image


def apply_filter(path: str | Path, output: str | Path, kind: str = "blur") -> Path:
    """Apply one supported filter: blur, sharpen, or threshold."""
    image = load_image(path)
    if kind == "blur":
        result = cv2.GaussianBlur(image, (7, 7), 0)
    elif kind == "sharpen":
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], dtype=np.float32)
        result = cv2.filter2D(image, -1, kernel)
    elif kind == "threshold":
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, result = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    else:
        raise ValueError("Unsupported filter. Choose blur, sharpen, or threshold.")
    output_path = Path(output).expanduser()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if not cv2.imwrite(str(output_path), result):
        raise ValueError(f"Could not save filtered image: {output_path}")
    return output_path

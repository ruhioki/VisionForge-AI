"""Create labeled side-by-side comparisons of source and processed images."""

from pathlib import Path

import cv2
import numpy as np

from visionforge.image_info import load_image


def _fit_height(image: np.ndarray, height: int) -> np.ndarray:
    """Resize an image to a target height without changing its aspect ratio."""
    source_height, source_width = image.shape[:2]
    if source_height == height:
        return image
    width = max(1, round(source_width * height / source_height))
    interpolation = cv2.INTER_AREA if height < source_height else cv2.INTER_LINEAR
    return cv2.resize(image, (width, height), interpolation=interpolation)


def create_comparison(
    original: str | Path,
    processed: str | Path,
    output: str | Path,
    left_label: str = "Original",
    right_label: str = "Processed",
    *,
    max_height: int = 600,
) -> Path:
    """Save a labeled comparison image, preserving each input's aspect ratio."""
    if max_height < 1:
        raise ValueError("max_height must be a positive integer.")
    left = load_image(original)
    right = load_image(processed)
    left = _fit_height(left, min(max_height, left.shape[0]))
    right = _fit_height(right, min(max_height, right.shape[0]))
    target_height = max(left.shape[0], right.shape[0])
    left = _fit_height(left, target_height)
    right = _fit_height(right, target_height)

    header_height = 48
    gap = 12
    canvas = np.full(
        (target_height + header_height, left.shape[1] + right.shape[1] + gap, 3),
        (24, 20, 34),
        dtype=np.uint8,
    )
    cv2.putText(canvas, str(left_label)[:80], (12, 31), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (225, 215, 255), 2, cv2.LINE_AA)
    right_x = left.shape[1] + gap
    cv2.putText(canvas, str(right_label)[:80], (right_x + 12, 31), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (225, 215, 255), 2, cv2.LINE_AA)
    canvas[header_height:, :left.shape[1]] = left
    canvas[header_height:, right_x:right_x + right.shape[1]] = right

    output_path = Path(output).expanduser()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if not cv2.imwrite(str(output_path), canvas):
        raise ValueError(f"Could not save comparison image: {output_path}")
    return output_path

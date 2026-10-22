"""Image loading, inspection, and basic OpenCV transformations."""

from pathlib import Path
from typing import Any

import cv2


def load_image(path: str | Path) -> Any:
    """Load an image from disk or raise a helpful ValueError."""
    image_path = Path(path).expanduser()
    image = cv2.imread(str(image_path), cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError(f"Could not read image: {image_path}. Check the path and file format.")
    return image


def inspect_image(path: str | Path) -> dict[str, int | str]:
    """Return image dimensions, channel count, file size, and file format."""
    image_path = Path(path).expanduser()
    image = load_image(image_path)
    height, width = image.shape[:2]
    channels = 1 if image.ndim == 2 else image.shape[2]
    return {
        "path": str(image_path),
        "width": int(width),
        "height": int(height),
        "channels": int(channels),
        "file_size_bytes": int(image_path.stat().st_size),
        "format": image_path.suffix.lower().lstrip(".") or "unknown",
    }


def detect_edges(path: str | Path, output: str | Path, low: int = 100, high: int = 200) -> Path:
    """Run Canny edge detection and save the resulting grayscale edge map."""
    if not (0 <= low < high <= 255):
        raise ValueError("Thresholds must satisfy 0 <= low < high <= 255.")
    image = load_image(path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 1.2)
    edges = cv2.Canny(blurred, low, high)
    return _save_image(edges, output)


def convert_grayscale(path: str | Path, output: str | Path) -> Path:
    """Convert an image to grayscale and save it."""
    image = load_image(path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return _save_image(gray, output)


def resize_image(path: str | Path, output: str | Path, width: int, height: int) -> Path:
    """Resize an image to the requested pixel dimensions and save it."""
    if width <= 0 or height <= 0:
        raise ValueError("Width and height must both be positive integers.")
    image = load_image(path)
    resized = cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)
    return _save_image(resized, output)


def _save_image(image: Any, output: str | Path) -> Path:
    output_path = Path(output).expanduser()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if not cv2.imwrite(str(output_path), image):
        raise ValueError(f"Could not save output image: {output_path}")
    return output_path

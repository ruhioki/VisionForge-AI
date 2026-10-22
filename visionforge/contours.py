"""Contour detection, visualization, and basic shape measurements."""

from pathlib import Path
from typing import Any

import cv2

from visionforge.image_info import _save_image, load_image

_RETRIEVAL_MODES = {
    "external": cv2.RETR_EXTERNAL,
    "list": cv2.RETR_LIST,
    "tree": cv2.RETR_TREE,
    "ccomp": cv2.RETR_CCOMP,
}


def detect_contours(
    path: str | Path,
    output: str | Path,
    threshold: int = 127,
    retrieval: str = "external",
    min_area: float = 0.0,
) -> dict[str, Any]:
    """Detect contours and save an overlay plus machine-readable measurements."""
    if not 0 <= threshold <= 255:
        raise ValueError("Threshold must be between 0 and 255.")
    if retrieval not in _RETRIEVAL_MODES:
        raise ValueError(f"Unsupported retrieval mode: {retrieval}. Choose from {', '.join(_RETRIEVAL_MODES)}.")
    if min_area < 0:
        raise ValueError("Minimum contour area cannot be negative.")

    image = load_image(path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(binary, _RETRIEVAL_MODES[retrieval], cv2.CHAIN_APPROX_SIMPLE)
    kept = [contour for contour in contours if cv2.contourArea(contour) >= min_area]
    overlay = image.copy()
    cv2.drawContours(overlay, kept, -1, (80, 220, 120), 2, cv2.LINE_AA)
    output_path = _save_image(overlay, output)

    measurements = []
    for index, contour in enumerate(kept):
        x, y, width, height = cv2.boundingRect(contour)
        moments = cv2.moments(contour)
        if moments["m00"]:
            centroid = {
                "x": round(moments["m10"] / moments["m00"], 2),
                "y": round(moments["m01"] / moments["m00"], 2),
            }
        else:
            centroid = None
        measurements.append({
            "index": index,
            "area": round(float(cv2.contourArea(contour)), 2),
            "perimeter": round(float(cv2.arcLength(contour, True)), 2),
            "bounding_box": {"x": int(x), "y": int(y), "width": int(width), "height": int(height)},
            "centroid": centroid,
        })

    return {
        "input": str(Path(path).expanduser()),
        "output": str(output_path),
        "threshold": threshold,
        "retrieval": retrieval,
        "minimum_area": float(min_area),
        "contour_count": len(measurements),
        "contours": measurements,
        "hierarchy_available": hierarchy is not None,
    }

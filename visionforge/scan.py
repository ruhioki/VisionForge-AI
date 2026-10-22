"""Perspective correction for photographed documents."""

from pathlib import Path
from typing import Any

import cv2
import numpy as np

from visionforge.image_info import _save_image, load_image


def _order_corners(points: np.ndarray) -> np.ndarray:
    """Return four points in top-left, top-right, bottom-right, bottom-left order."""
    corners = np.zeros((4, 2), dtype=np.float32)
    sums = points.sum(axis=1)
    differences = np.diff(points, axis=1).reshape(-1)
    corners[0] = points[np.argmin(sums)]
    corners[2] = points[np.argmax(sums)]
    corners[1] = points[np.argmin(differences)]
    corners[3] = points[np.argmax(differences)]
    return corners


def scan_document(
    path: str | Path,
    output: str | Path,
    min_area: float = 0.15,
) -> dict[str, Any]:
    """Find the largest four-corner document and save its perspective-corrected view."""
    if not 0 < min_area <= 1:
        raise ValueError("Minimum area must be greater than 0 and at most 1.")

    image = load_image(path)
    height, width = image.shape[:2]
    scale = min(1.0, 1200 / max(height, width))
    detection = (
        cv2.resize(image, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
        if scale < 1
        else image
    )
    detection_height, detection_width = detection.shape[:2]

    gray = cv2.cvtColor(detection, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 75, 200)
    contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    minimum_contour_area = detection_width * detection_height * min_area

    document = None
    for contour in sorted(contours, key=cv2.contourArea, reverse=True):
        if cv2.contourArea(contour) < minimum_contour_area:
            break
        perimeter = cv2.arcLength(contour, True)
        polygon = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
        if len(polygon) == 4 and cv2.isContourConvex(polygon):
            document = polygon.reshape(4, 2).astype(np.float32)
            break

    if document is None:
        raise ValueError(
            "Could not detect a four-corner document. Ensure the page has a clear outline "
            "and occupies enough of the image, or lower --min-area."
        )

    document[:, 0] *= width / detection_width
    document[:, 1] *= height / detection_height
    corners = _order_corners(document)
    top_left, top_right, bottom_right, bottom_left = corners
    output_width = max(
        int(round(np.linalg.norm(bottom_right - bottom_left))),
        int(round(np.linalg.norm(top_right - top_left))),
    )
    output_height = max(
        int(round(np.linalg.norm(top_right - bottom_right))),
        int(round(np.linalg.norm(top_left - bottom_left))),
    )
    if output_width < 1 or output_height < 1:
        raise ValueError("Detected document corners do not form a usable page.")

    destination = np.array(
        [
            [0, 0],
            [output_width - 1, 0],
            [output_width - 1, output_height - 1],
            [0, output_height - 1],
        ],
        dtype=np.float32,
    )
    transform = cv2.getPerspectiveTransform(corners, destination)
    scanned = cv2.warpPerspective(image, transform, (output_width, output_height))
    output_path = _save_image(scanned, output)

    return {
        "input": str(Path(path).expanduser()),
        "output": str(output_path),
        "width": output_width,
        "height": output_height,
        "corners": [[round(float(x), 2), round(float(y), 2)] for x, y in corners],
        "minimum_area_fraction": min_area,
    }

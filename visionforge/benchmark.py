"""Repeatable micro-benchmarks for common in-memory image operations."""

from pathlib import Path
from statistics import mean, median
from time import perf_counter
from typing import Any

import cv2
import numpy as np

SUPPORTED_BENCHMARKS = {"grayscale", "edges", "blur", "sharpen", "threshold"}


def _apply(image: np.ndarray, kind: str) -> np.ndarray:
    if kind == "grayscale":
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    if kind == "edges":
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        return cv2.Canny(blurred, 100, 200)
    if kind == "blur":
        return cv2.GaussianBlur(image, (5, 5), 0)
    if kind == "sharpen":
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], dtype=np.float32)
        return cv2.filter2D(image, -1, kernel)
    if kind == "threshold":
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, result = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        return result
    raise ValueError(f"Unsupported benchmark operation: {kind}. Choose from {', '.join(sorted(SUPPORTED_BENCHMARKS))}.")


def benchmark_image(
    image_path: str | Path,
    kind: str,
    iterations: int = 25,
    warmup: int = 3,
) -> dict[str, Any]:
    """Measure an operation in memory, excluding image loading and file writes."""
    if kind not in SUPPORTED_BENCHMARKS:
        raise ValueError(f"Unsupported benchmark operation: {kind}. Choose from {', '.join(sorted(SUPPORTED_BENCHMARKS))}.")
    if iterations < 1:
        raise ValueError("iterations must be at least 1")
    if warmup < 0:
        raise ValueError("warmup must be zero or greater")

    source = Path(image_path).expanduser()
    image = cv2.imread(str(source), cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError(f"Could not read image: {source}")

    for _ in range(warmup):
        _apply(image, kind)

    durations = []
    result = None
    for _ in range(iterations):
        start = perf_counter()
        result = _apply(image, kind)
        durations.append(perf_counter() - start)

    average_seconds = mean(durations)
    height, width = image.shape[:2]
    return {
        "image": str(source),
        "operation": kind,
        "width": int(width),
        "height": int(height),
        "iterations": iterations,
        "warmup": warmup,
        "mean_ms": average_seconds * 1000.0,
        "median_ms": median(durations) * 1000.0,
        "min_ms": min(durations) * 1000.0,
        "max_ms": max(durations) * 1000.0,
        "megapixels_per_second": (width * height / average_seconds / 1_000_000) if average_seconds > 0 else None,
        "result_shape": [int(dimension) for dimension in result.shape],
        "measurement": "In-memory CPU micro-benchmark; image loading and file writes are excluded.",
    }

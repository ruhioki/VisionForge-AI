"""End-to-end reproducible demo for VisionForge AI."""

import json
from pathlib import Path
from typing import Any

import cv2
import numpy as np

from visionforge.color_analysis import analyze_colors
from visionforge.histogram import save_histogram
from visionforge.image_info import convert_grayscale, detect_edges, inspect_image, resize_image


def run_demo(output_dir: str | Path = "outputs") -> dict[str, Any]:
    """Generate a synthetic image, process it, and write a JSON report."""
    output = Path(output_dir).expanduser()
    output.mkdir(parents=True, exist_ok=True)
    source = output / "visionforge-demo.png"

    # Deterministic synthetic geometry avoids downloads and licensing concerns.
    image = np.full((360, 640, 3), (32, 25, 18), dtype=np.uint8)
    cv2.rectangle(image, (70, 70), (260, 285), (80, 190, 245), thickness=-1)
    cv2.circle(image, (430, 165), 88, (180, 90, 220), thickness=-1)
    cv2.line(image, (55, 320), (585, 320), (245, 245, 245), thickness=5)
    cv2.putText(image, "VisionForge AI", (145, 45), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (245, 245, 245), 2, cv2.LINE_AA)
    if not cv2.imwrite(str(source), image):
        raise RuntimeError(f"Could not create demo image: {source}")

    paths = {
        "source": source,
        "edges": detect_edges(source, output / "visionforge-edges.png"),
        "grayscale": convert_grayscale(source, output / "visionforge-grayscale.png"),
        "resized": resize_image(source, output / "visionforge-resized.png", 320, 180),
        "histogram": save_histogram(source, output / "visionforge-histogram.png"),
    }
    report: dict[str, Any] = {
        "project": "VisionForge AI",
        "pipeline": ["image inspection", "RGB and brightness analysis", "Canny edge detection", "grayscale conversion", "resize", "RGB histogram"],
        "image_info": inspect_image(source),
        "color_analysis": analyze_colors(source),
        "outputs": {name: str(path.resolve()) for name, path in paths.items()},
    }
    report_path = output / "report.json"
    report["report_file"] = str(report_path.resolve())
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report

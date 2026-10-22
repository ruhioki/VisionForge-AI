"""Image similarity metrics for comparing a reference and candidate image."""

from pathlib import Path
from typing import Any

import cv2
import numpy as np


def calculate_image_metrics(reference_path: str | Path, candidate_path: str | Path) -> dict[str, Any]:
    """Calculate MSE, RMSE, and PSNR for two same-sized images.

    Images are compared as decoded by OpenCV. The function rejects unreadable
    inputs and size mismatches instead of silently resizing either image.
    """
    reference_file = Path(reference_path).expanduser()
    candidate_file = Path(candidate_path).expanduser()
    reference = cv2.imread(str(reference_file), cv2.IMREAD_COLOR)
    candidate = cv2.imread(str(candidate_file), cv2.IMREAD_COLOR)

    if reference is None:
        raise ValueError(f"Could not read reference image: {reference_file}")
    if candidate is None:
        raise ValueError(f"Could not read candidate image: {candidate_file}")
    if reference.shape != candidate.shape:
        raise ValueError(
            "Images must have identical dimensions for a fair comparison: "
            f"reference={reference.shape[1]}x{reference.shape[0]}, "
            f"candidate={candidate.shape[1]}x{candidate.shape[0]}"
        )

    difference = reference.astype(np.float64) - candidate.astype(np.float64)
    mse = float(np.mean(np.square(difference)))
    rmse = float(np.sqrt(mse))
    psnr = float("inf") if mse == 0 else float(20.0 * np.log10(255.0 / np.sqrt(mse)))

    return {
        "reference": str(reference_file),
        "candidate": str(candidate_file),
        "width": int(reference.shape[1]),
        "height": int(reference.shape[0]),
        "channels": 3,
        "mse": mse,
        "rmse": rmse,
        "psnr_db": psnr,
        "identical": mse == 0.0,
        "interpretation": (
            "Images are pixel-identical after decoding."
            if mse == 0.0
            else "Higher PSNR and lower MSE indicate closer pixel-level similarity."
        ),
    }

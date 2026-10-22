import json

import cv2
import numpy as np
import pytest

from visionforge.quality import calculate_image_metrics


def _save(path, image):
    assert cv2.imwrite(str(path), image)


def test_identical_images_have_zero_error_and_infinite_psnr(tmp_path):
    image = np.zeros((20, 30, 3), dtype=np.uint8)
    reference = tmp_path / "reference.png"
    candidate = tmp_path / "candidate.png"
    _save(reference, image)
    _save(candidate, image.copy())

    result = calculate_image_metrics(reference, candidate)

    assert result["identical"] is True
    assert result["mse"] == 0.0
    assert result["rmse"] == 0.0
    assert result["psnr_db"] is None
    assert result["psnr_infinite"] is True
    assert result["width"] == 30
    assert result["height"] == 20


def test_different_images_return_finite_error_metrics(tmp_path):
    reference = tmp_path / "reference.png"
    candidate = tmp_path / "candidate.png"
    _save(reference, np.zeros((10, 12, 3), dtype=np.uint8))
    _save(candidate, np.full((10, 12, 3), 10, dtype=np.uint8))

    result = calculate_image_metrics(reference, candidate)

    assert result["identical"] is False
    assert result["mse"] == 100.0
    assert result["rmse"] == 10.0
    assert result["psnr_db"] > 0


def test_metrics_reject_different_dimensions(tmp_path):
    reference = tmp_path / "reference.png"
    candidate = tmp_path / "candidate.png"
    _save(reference, np.zeros((10, 12, 3), dtype=np.uint8))
    _save(candidate, np.zeros((11, 12, 3), dtype=np.uint8))

    with pytest.raises(ValueError, match="identical dimensions"):
        calculate_image_metrics(reference, candidate)


def test_metrics_reject_unreadable_image(tmp_path):
    reference = tmp_path / "broken.png"
    reference.write_text("not an image", encoding="utf-8")
    candidate = tmp_path / "candidate.png"
    _save(candidate, np.zeros((10, 12, 3), dtype=np.uint8))

    with pytest.raises(ValueError, match="Could not read reference image"):
        calculate_image_metrics(reference, candidate)


def test_cli_help_lists_metrics_command():
    from visionforge.cli import build_parser

    assert "metrics" in build_parser().format_help()

def test_ssim_is_added_when_requested(tmp_path, monkeypatch):
    import sys
    from types import SimpleNamespace

    reference = tmp_path / "reference.png"
    candidate = tmp_path / "candidate.png"
    image = np.full((12, 12, 3), 120, dtype=np.uint8)
    _save(reference, image)
    _save(candidate, image.copy())
    fake_metrics = SimpleNamespace(structural_similarity=lambda *args, **kwargs: 1.0)
    monkeypatch.setitem(sys.modules, "skimage", SimpleNamespace(__path__=[]))
    monkeypatch.setitem(sys.modules, "skimage.metrics", fake_metrics)

    result = calculate_image_metrics(reference, candidate, include_ssim=True)

    assert result["ssim"] == 1.0


def test_ssim_rejects_tiny_images(tmp_path):
    reference = tmp_path / "reference.png"
    candidate = tmp_path / "candidate.png"
    _save(reference, np.zeros((2, 4, 3), dtype=np.uint8))
    _save(candidate, np.zeros((2, 4, 3), dtype=np.uint8))

    with pytest.raises(ValueError, match="at least 3 pixels"):
        calculate_image_metrics(reference, candidate, include_ssim=True)

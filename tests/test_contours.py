import cv2
import numpy as np
import pytest

from visionforge.contours import detect_contours


@pytest.fixture
def shapes_image(tmp_path):
    path = tmp_path / "shapes.png"
    image = np.zeros((120, 160, 3), dtype=np.uint8)
    cv2.rectangle(image, (15, 20), (65, 75), (255, 255, 255), thickness=-1)
    cv2.circle(image, (115, 55), 20, (255, 255, 255), thickness=-1)
    assert cv2.imwrite(str(path), image)
    return path


def test_detect_contours_reports_shapes_and_writes_overlay(shapes_image, tmp_path):
    output = tmp_path / "nested" / "contours.png"
    report = detect_contours(shapes_image, output, threshold=127, retrieval="external", min_area=10)
    overlay = cv2.imread(str(output))
    assert overlay is not None
    assert overlay.shape == (120, 160, 3)
    assert report["contour_count"] == 2
    assert all(item["area"] > 0 for item in report["contours"])
    assert all("bounding_box" in item and "perimeter" in item for item in report["contours"])


def test_minimum_area_filters_small_shapes(shapes_image, tmp_path):
    report = detect_contours(shapes_image, tmp_path / "contours.png", min_area=1500)
    assert report["contour_count"] == 1


@pytest.mark.parametrize("threshold", [-1, 256])
def test_rejects_invalid_threshold(shapes_image, tmp_path, threshold):
    with pytest.raises(ValueError, match="between 0 and 255"):
        detect_contours(shapes_image, tmp_path / "contours.png", threshold=threshold)


def test_rejects_unknown_retrieval_mode(shapes_image, tmp_path):
    with pytest.raises(ValueError, match="Unsupported retrieval mode"):
        detect_contours(shapes_image, tmp_path / "contours.png", retrieval="unknown")


def test_rejects_negative_minimum_area(shapes_image, tmp_path):
    with pytest.raises(ValueError, match="cannot be negative"):
        detect_contours(shapes_image, tmp_path / "contours.png", min_area=-1)


def test_cli_help_lists_contours_command():
    from visionforge.cli import build_parser

    assert "contours" in build_parser().format_help()

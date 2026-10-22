import cv2
import numpy as np
import pytest

from visionforge.scan import scan_document


@pytest.fixture
def photographed_page(tmp_path):
    path = tmp_path / "page.png"
    image = np.full((500, 400, 3), 35, dtype=np.uint8)
    page = np.array([[55, 35], [345, 75], [315, 465], [75, 425]], dtype=np.int32)
    cv2.fillConvexPoly(image, page, (235, 235, 235))
    cv2.putText(image, "VISIONFORGE", (95, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (30, 30, 30), 2)
    assert cv2.imwrite(str(path), image)
    return path


def test_scan_document_corrects_page_and_reports_corners(photographed_page, tmp_path):
    output = tmp_path / "nested" / "scanned.png"
    report = scan_document(photographed_page, output)
    scanned = cv2.imread(str(output))

    assert scanned is not None
    assert scanned.shape[:2] == (report["height"], report["width"])
    assert report["width"] > 200
    assert report["height"] > report["width"]
    assert len(report["corners"]) == 4
    assert report["minimum_area_fraction"] == 0.15


def test_scan_document_rejects_image_without_document(tmp_path):
    path = tmp_path / "blank.png"
    assert cv2.imwrite(str(path), np.zeros((100, 100, 3), dtype=np.uint8))

    with pytest.raises(ValueError, match="Could not detect a four-corner document"):
        scan_document(path, tmp_path / "scanned.png")


@pytest.mark.parametrize("min_area", [0, -0.1, 1.1])
def test_scan_document_rejects_invalid_minimum_area(photographed_page, tmp_path, min_area):
    with pytest.raises(ValueError, match="greater than 0 and at most 1"):
        scan_document(photographed_page, tmp_path / "scanned.png", min_area=min_area)


def test_cli_help_lists_scan_command():
    from visionforge.cli import build_parser

    assert "scan" in build_parser().format_help()

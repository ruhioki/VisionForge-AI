import cv2
import numpy as np
import pytest

from visionforge.image_info import (
    convert_grayscale,
    detect_edges,
    inspect_image,
    load_image,
    resize_image,
)


@pytest.fixture
def sample_image(tmp_path):
    path = tmp_path / "sample.png"
    image = np.zeros((80, 100, 3), dtype=np.uint8)
    cv2.rectangle(image, (20, 15), (75, 65), (255, 255, 255), thickness=-1)
    assert cv2.imwrite(str(path), image)
    return path


def test_inspect_image_reports_dimensions(sample_image):
    info = inspect_image(sample_image)
    assert info["width"] == 100
    assert info["height"] == 80
    assert info["channels"] == 3
    assert info["format"] == "png"
    assert info["file_size_bytes"] > 0


def test_load_missing_image_raises_helpful_error(tmp_path):
    with pytest.raises(ValueError, match="Could not read image"):
        load_image(tmp_path / "missing.png")


def test_detect_edges_writes_output(sample_image, tmp_path):
    output = detect_edges(sample_image, tmp_path / "nested" / "edges.png")
    result = cv2.imread(str(output), cv2.IMREAD_GRAYSCALE)
    assert result is not None
    assert result.shape == (80, 100)
    assert set(np.unique(result)).issubset({0, 255})


def test_detect_edges_validates_thresholds(sample_image, tmp_path):
    with pytest.raises(ValueError, match="Thresholds"):
        detect_edges(sample_image, tmp_path / "edges.png", low=200, high=100)


def test_grayscale_writes_single_channel_image(sample_image, tmp_path):
    output = convert_grayscale(sample_image, tmp_path / "gray.png")
    result = cv2.imread(str(output), cv2.IMREAD_UNCHANGED)
    assert result is not None
    assert result.ndim == 2


def test_resize_uses_requested_dimensions(sample_image, tmp_path):
    output = resize_image(sample_image, tmp_path / "small.png", width=25, height=20)
    result = cv2.imread(str(output))
    assert result is not None
    assert result.shape[:2] == (20, 25)


def test_resize_rejects_non_positive_dimensions(sample_image, tmp_path):
    with pytest.raises(ValueError, match="positive"):
        resize_image(sample_image, tmp_path / "bad.png", width=0, height=20)


def test_color_analysis_reports_rgb_and_brightness(sample_image):
    from visionforge.color_analysis import analyze_colors

    result = analyze_colors(sample_image)
    assert set(result["mean_rgb"]) == {"red", "green", "blue"}
    assert result["brightness"]["minimum"] == 0
    assert result["brightness"]["maximum"] == 255


def test_cli_help_lists_commands():
    from visionforge.cli import build_parser

    help_text = build_parser().format_help()
    assert "colors" in help_text
    assert "edges" in help_text

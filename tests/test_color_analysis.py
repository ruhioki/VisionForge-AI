import cv2
import numpy as np
import pytest

from visionforge.color_analysis import analyze_colors


def test_mean_rgb_is_reported_in_rgb_order(tmp_path):
    path = tmp_path / "red.png"
    image = np.zeros((20, 20, 3), dtype=np.uint8)
    image[:] = (0, 0, 255)  # pure red in OpenCV's BGR order
    cv2.imwrite(str(path), image)
    result = analyze_colors(path)
    assert result["mean_rgb"] == {"red": 255.0, "green": 0.0, "blue": 0.0}


def test_brightness_range_for_black_and_white_image(tmp_path):
    path = tmp_path / "bw.png"
    image = np.zeros((10, 10, 3), dtype=np.uint8)
    image[:, 5:] = 255
    cv2.imwrite(str(path), image)
    brightness = analyze_colors(path)["brightness"]
    assert brightness["minimum"] == 0
    assert brightness["maximum"] == 255
    assert brightness["mean"] == pytest.approx(127.5)


def test_missing_file_raises_value_error(tmp_path):
    with pytest.raises(ValueError):
        analyze_colors(tmp_path / "nope.png")

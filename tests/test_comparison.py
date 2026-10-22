import cv2
import numpy as np
import pytest

from visionforge.comparison import create_comparison


@pytest.fixture
def image_pair(tmp_path):
    original = tmp_path / "original.png"
    processed = tmp_path / "processed.png"
    assert cv2.imwrite(str(original), np.full((40, 60, 3), (0, 0, 255), dtype=np.uint8))
    assert cv2.imwrite(str(processed), np.full((80, 30, 3), (255, 0, 0), dtype=np.uint8))
    return original, processed


def test_comparison_saves_both_images_and_header(image_pair, tmp_path):
    original, processed = image_pair
    output = create_comparison(original, processed, tmp_path / "nested" / "comparison.png", "Before", "After")
    result = cv2.imread(str(output))
    assert result is not None
    # Inputs are fit to a common height; aspect ratios are preserved.
    assert result.shape[0] == 80 + 48
    assert result.shape[1] == 120 + 30 + 12
    assert output.is_file()


def test_comparison_rejects_non_positive_max_height(image_pair, tmp_path):
    original, processed = image_pair
    with pytest.raises(ValueError, match="positive"):
        create_comparison(original, processed, tmp_path / "comparison.png", max_height=0)


def test_comparison_rejects_missing_input(tmp_path):
    valid = tmp_path / "valid.png"
    assert cv2.imwrite(str(valid), np.zeros((10, 10, 3), dtype=np.uint8))
    with pytest.raises(ValueError, match="Could not read image"):
        create_comparison(valid, tmp_path / "missing.png", tmp_path / "comparison.png")

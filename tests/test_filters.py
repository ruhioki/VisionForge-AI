import cv2
import numpy as np
import pytest

from visionforge.filters import apply_filter


@pytest.mark.parametrize("kind", ["blur", "sharpen", "threshold"])
def test_filters_write_output_and_create_parent_dirs(sample_image, tmp_path, kind):
    output = tmp_path / "nested" / f"{kind}.png"
    assert apply_filter(sample_image, output, kind) == output
    assert output.exists()


def test_threshold_output_is_binary(sample_image, tmp_path):
    output = tmp_path / "threshold.png"
    apply_filter(sample_image, output, "threshold")
    result = cv2.imread(str(output), cv2.IMREAD_GRAYSCALE)
    assert set(np.unique(result)) <= {0, 255}


def test_blur_keeps_shape(sample_image, tmp_path):
    output = tmp_path / "blur.png"
    apply_filter(sample_image, output, "blur")
    assert cv2.imread(str(output)).shape == cv2.imread(str(sample_image)).shape


def test_unknown_filter_is_rejected(sample_image, tmp_path):
    with pytest.raises(ValueError, match="Unsupported filter"):
        apply_filter(sample_image, tmp_path / "x.png", "emboss")


def test_missing_input_is_rejected(tmp_path):
    with pytest.raises(ValueError, match="Could not read image"):
        apply_filter(tmp_path / "missing.png", tmp_path / "x.png", "blur")

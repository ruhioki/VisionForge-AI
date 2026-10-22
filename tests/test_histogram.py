import cv2
import pytest

from visionforge.histogram import save_histogram


def test_histogram_has_requested_size(sample_image, tmp_path):
    output = save_histogram(sample_image, tmp_path / "out" / "hist.png", width=512, height=300)
    image = cv2.imread(str(output))
    assert image.shape[:2] == (300, 512)


@pytest.mark.parametrize("width,height", [(255, 400), (400, 159)])
def test_histogram_rejects_tiny_canvas(sample_image, tmp_path, width, height):
    with pytest.raises(ValueError, match="at least"):
        save_histogram(sample_image, tmp_path / "h.png", width=width, height=height)

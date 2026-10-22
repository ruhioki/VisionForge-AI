import cv2
import numpy as np
import pytest


@pytest.fixture
def sample_image(tmp_path):
    """A small synthetic image: white rectangle on a dark background."""
    path = tmp_path / "sample.png"
    image = np.full((80, 100, 3), (10, 20, 30), dtype=np.uint8)  # BGR
    cv2.rectangle(image, (20, 15), (75, 65), (255, 255, 255), thickness=-1)
    assert cv2.imwrite(str(path), image)
    return path

import cv2
import numpy as np
import pytest

from visionforge.benchmark import benchmark_image


def _image(path):
    image = np.zeros((64, 80, 3), dtype=np.uint8)
    image[10:45, 15:60] = (255, 120, 20)
    assert cv2.imwrite(str(path), image)


def test_benchmark_returns_timing_and_output_metadata(tmp_path):
    source = tmp_path / "sample.png"
    _image(source)

    result = benchmark_image(source, "edges", iterations=3, warmup=1)

    assert result["operation"] == "edges"
    assert result["width"] == 80
    assert result["height"] == 64
    assert result["iterations"] == 3
    assert result["mean_ms"] >= 0
    assert result["median_ms"] >= 0
    assert result["result_shape"] == [64, 80]
    assert result["megapixels_per_second"] >= 0


def test_benchmark_rejects_invalid_iteration_counts(tmp_path):
    with pytest.raises(ValueError, match="iterations must be at least 1"):
        benchmark_image("unused.png", "edges", iterations=0)


def test_benchmark_rejects_negative_warmup():
    with pytest.raises(ValueError, match="warmup must be zero or greater"):
        benchmark_image("unused.png", "edges", warmup=-1)


def test_benchmark_rejects_unknown_operation(tmp_path):
    with pytest.raises(ValueError, match="Unsupported benchmark operation"):
        benchmark_image("unused.png", "resize")


def test_benchmark_rejects_unreadable_image(tmp_path):
    source = tmp_path / "broken.png"
    source.write_text("not an image", encoding="utf-8")
    with pytest.raises(ValueError, match="Could not read image"):
        benchmark_image(source, "edges")

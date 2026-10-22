import sys
from types import SimpleNamespace

import cv2
import numpy as np
import pytest

from visionforge.classification import classify_image


class FakeSession:
    def __init__(self, model_path, providers):
        self.model_path = model_path
        self.providers = providers

    def get_inputs(self):
        return [SimpleNamespace(name="images", shape=[1, 3, 8, 8])]

    def run(self, output_names, feeds):
        tensor = feeds["images"]
        assert tensor.shape == (1, 3, 8, 8)
        assert tensor.dtype == np.float32
        return [np.array([[0.1, 2.0, -1.0]], dtype=np.float32)]


def _setup(tmp_path, monkeypatch):
    image_path = tmp_path / "sample.png"
    assert cv2.imwrite(str(image_path), np.full((12, 16, 3), 128, dtype=np.uint8))
    model_path = tmp_path / "model.onnx"
    model_path.write_bytes(b"test model placeholder")
    labels_path = tmp_path / "labels.txt"
    labels_path.write_text("cat\ndog\ncar\n", encoding="utf-8")
    fake_runtime = SimpleNamespace(InferenceSession=FakeSession, get_available_providers=lambda: ["CPUExecutionProvider"])
    monkeypatch.setitem(sys.modules, "onnxruntime", fake_runtime)
    return image_path, model_path, labels_path


def test_classification_returns_sorted_top_predictions(tmp_path, monkeypatch):
    image, model, labels = _setup(tmp_path, monkeypatch)

    result = classify_image(image, model, labels, top_k=2)

    assert result["input_width"] == 8
    assert result["input_height"] == 8
    assert result["execution_provider"] == "CPUExecutionProvider"
    assert [item["label"] for item in result["predictions"]] == ["dog", "cat"]
    assert sum(item["confidence"] for item in result["predictions"]) < 1.0


def test_classification_rejects_nonpositive_top_k(tmp_path):
    with pytest.raises(ValueError, match="top_k must be at least 1"):
        classify_image("unused.png", "unused.onnx", "unused.txt", top_k=0)


def test_classification_rejects_label_count_mismatch(tmp_path, monkeypatch):
    image, model, labels = _setup(tmp_path, monkeypatch)
    labels.write_text("cat\ndog\n", encoding="utf-8")

    with pytest.raises(ValueError, match="labels file contains 2 labels"):
        classify_image(image, model, labels)

def test_classification_rejects_unavailable_cuda(tmp_path, monkeypatch):
    image, model, labels = _setup(tmp_path, monkeypatch)

    with pytest.raises(RuntimeError, match="CUDAExecutionProvider is unavailable"):
        classify_image(image, model, labels, provider="cuda")


def test_classification_rejects_unknown_provider():
    with pytest.raises(ValueError, match="provider must be one of"):
        classify_image("unused.png", "unused.onnx", "unused.txt", provider="tpu")

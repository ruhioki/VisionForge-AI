"""Optional ONNX Runtime image classification for ImageNet-style models."""

from pathlib import Path
from typing import Any
import importlib

import cv2
import numpy as np

IMAGENET_MEAN = np.array([0.485, 0.456, 0.406], dtype=np.float32).reshape(1, 1, 3)
IMAGENET_STD = np.array([0.229, 0.224, 0.225], dtype=np.float32).reshape(1, 1, 3)


def classify_image(
    image_path: str | Path,
    model_path: str | Path,
    labels_path: str | Path,
    top_k: int = 5,
    provider: str = "auto",
) -> dict[str, Any]:
    """Classify one image with a user-supplied ImageNet-style ONNX model.

    Expected model input is float32 NCHW RGB, normalized with ImageNet mean/std.
    Fixed spatial dimensions are inferred from the model; dynamic dimensions use
    224x224. Model files and label lists are deliberately not bundled.
    """
    if top_k < 1:
        raise ValueError("top_k must be at least 1")
    if provider not in {"auto", "cpu", "cuda"}:
        raise ValueError("provider must be one of: auto, cpu, cuda")

    image_file = Path(image_path).expanduser()
    model_file = Path(model_path).expanduser()
    labels_file = Path(labels_path).expanduser()

    image = cv2.imread(str(image_file), cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError(f"Could not read image: {image_file}")
    if not model_file.is_file():
        raise ValueError(f"ONNX model file does not exist: {model_file}")
    if not labels_file.is_file():
        raise ValueError(f"Labels file does not exist: {labels_file}")

    labels = [line.strip() for line in labels_file.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not labels:
        raise ValueError(f"Labels file is empty: {labels_file}")

    try:
        onnxruntime = importlib.import_module("onnxruntime")
    except ImportError as exc:
        raise RuntimeError(
            "ONNX Runtime is optional. Install it with: python -m pip install -e \".[onnx]\""
        ) from exc

    available = onnxruntime.get_available_providers()
    if provider == "cuda" and "CUDAExecutionProvider" not in available:
        raise RuntimeError("CUDAExecutionProvider is unavailable. Install a compatible onnxruntime-gpu build and CUDA/cuDNN runtime.")
    selected_provider = (
        "CUDAExecutionProvider"
        if provider == "cuda" or (provider == "auto" and "CUDAExecutionProvider" in available)
        else "CPUExecutionProvider"
    )
    if selected_provider not in available:
        raise RuntimeError(f"{selected_provider} is unavailable in this ONNX Runtime installation")
    session = onnxruntime.InferenceSession(str(model_file), providers=[selected_provider])
    inputs = session.get_inputs()
    if not inputs:
        raise ValueError("The ONNX model has no input tensor")
    model_input = inputs[0]
    shape = model_input.shape
    if len(shape) != 4:
        raise ValueError(f"Expected a 4D NCHW model input, got shape {shape}")
    if isinstance(shape[1], int) and shape[1] != 3:
        raise ValueError(f"Expected three RGB input channels, got shape {shape}")
    height = shape[2] if isinstance(shape[2], int) and shape[2] > 0 else 224
    width = shape[3] if isinstance(shape[3], int) and shape[3] > 0 else 224

    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    resized = cv2.resize(rgb, (width, height), interpolation=cv2.INTER_LINEAR)
    normalized = (resized.astype(np.float32) / 255.0 - IMAGENET_MEAN) / IMAGENET_STD
    tensor = np.transpose(normalized, (2, 0, 1))[None, ...].astype(np.float32)

    outputs = session.run(None, {model_input.name: tensor})
    if not outputs:
        raise ValueError("The ONNX model returned no output tensors")
    logits = np.asarray(outputs[0])
    if logits.ndim < 2 or logits.shape[0] != 1:
        raise ValueError(f"Expected one batch of class scores, got output shape {logits.shape}")
    scores = logits.reshape(1, -1)[0].astype(np.float64)
    if scores.size != len(labels):
        raise ValueError(
            f"Model returned {scores.size} class scores but labels file contains {len(labels)} labels"
        )
    shifted = scores - np.max(scores)
    probabilities = np.exp(shifted)
    probabilities /= probabilities.sum()
    order = np.argsort(probabilities)[::-1][: min(top_k, len(labels))]

    return {
        "image": str(image_file),
        "model": str(model_file),
        "input_width": int(width),
        "input_height": int(height),
        "execution_provider": selected_provider,
        "predictions": [
            {
                "class_index": int(index),
                "label": labels[int(index)],
                "confidence": float(probabilities[int(index)]),
            }
            for index in order
        ],
        "note": "Predictions depend on the model and labels. Confirm both files use the same class order.",
    }

# VisionForge AI architecture

VisionForge is organized as a small Python package with a CLI layer and reusable processing functions.

- `visionforge/cli.py`: parses commands and reports results or user-friendly errors.
- `visionforge/classification.py`: optional ONNX Runtime inference for compatible ImageNet-style classifiers.
- `visionforge/benchmark.py`: repeatable in-memory CPU timing for common operations.
- `visionforge/quality.py`: computes pixel-level MSE, RMSE, and PSNR, with optional SSIM.
- `visionforge/batch.py`: processes folders of images and records per-file outcomes.
- `visionforge/image_info.py`: image loading, metadata, grayscale, resizing, and Canny edge detection.
- `visionforge/color_analysis.py`: average RGB values and grayscale brightness statistics.
- `visionforge/histogram.py`: draws RGB channel histograms with OpenCV.
- `visionforge/filters.py`: blur, sharpen, and binary threshold filters.
- `visionforge/comparison.py`: creates labeled side-by-side image comparisons.
- `visionforge/contours.py`: detects contours and reports geometric measurements.
- `visionforge/scan.py`: locates a four-corner page and corrects its perspective.
- `visionforge/demo.py`: generates synthetic inputs and reproducible example outputs.
- `examples/generate_demo.py`: creates a deterministic synthetic image and runs the processing pipeline.
- `examples/document_scanner.py`: generates a photographed-page example and runs the document scanner.
- `tools/create_source_bundle.py`: packages project sources and documentation into a clean downloadable ZIP.
- `tests/`: regression tests built around synthetic images, avoiding external datasets.

## Design decisions

OpenCV uses BGR channel ordering for loaded color images, so code explicitly converts channel means to RGB for user-facing statistics. Image outputs are written only to the requested destination; parent directories are created as needed. Classical image processing is available in the base install. ONNX classification and SSIM are optional extras; the project does not bundle model weights or implement object detection yet.

## Data flow

Input image -> validated loader -> processing / analysis function -> output image or JSON metadata

For document scanning, a resized working copy is used to locate the largest qualifying four-corner contour. Its coordinates are mapped to the original image before perspective correction, so saved output retains source resolution.

The CLI is a thin interface over these functions so they can also be reused by notebooks or a future graphical interface.

# Changelog

Notable changes to VisionForge AI are documented here.

## Unreleased

### Added
- Document scanning with four-corner page detection and perspective correction.
- A synthetic document-scanner example requiring no external dataset.
- A tested source ZIP generator that excludes repository history, caches, environments, and generated outputs.

### Fixed
- Align the package's `__version__` with the current 0.3.0 project metadata.

## 0.3.0 - 2026-10-22

### Added
- Image metadata inspection, RGB/brightness analysis, grayscale conversion, resizing, and Canny edge detection.
- Blur, sharpening, binary thresholding, RGB histograms, contour detection, and contour measurements.
- Side-by-side image comparison.
- Folder batch processing with per-file error reporting and a JSON report.
- Pixel-level image similarity metrics: MSE, RMSE, and PSNR, plus optional SSIM.
- Optional ONNX Runtime image classification with top-k predictions.
- Optional CUDA execution provider selection for compatible ONNX Runtime GPU installations.
- In-memory CPU benchmarks with warm-up iterations, timing statistics, and megapixels-per-second estimates.
- Synthetic-image tests and CI coverage across Python 3.10, 3.11, and 3.12.
- Package build and installed-command smoke tests in CI.

### Notes
- ONNX model files and class labels are supplied by the user and are not bundled.
- GPU inference requires a compatible ONNX Runtime GPU build and matching CUDA/cuDNN environment.
- Benchmark results are local CPU micro-benchmarks, not cross-machine or GPU performance claims.

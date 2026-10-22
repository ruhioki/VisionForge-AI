# Changelog

Notable changes to VisionForge AI are documented here.

## Unreleased

### Added
- `visionforge --version` flag.
- Tests for filters, color analysis, histograms, the demo pipeline, and the CLI (47 -> 69 tests).
- Ruff linting, run locally and in CI.

### Fixed
- `visionforge.__version__` reported `0.2.0` while the package metadata said `0.3.0`; a test now keeps them in sync.
- Missing closing parenthesis in the `batch --report` help text.

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

# Roadmap

## Current development release

- [x] Image metadata inspection and basic image validation
- [x] RGB color and brightness analysis
- [x] Grayscale conversion, resizing, and Canny edge detection
- [x] Blur, sharpen, and binary threshold filters
- [x] RGB histogram rendering
- [x] Contour detection and measurements with JSON reporting
- [x] Side-by-side original/processed image comparisons
- [x] Folder batch processing with per-file failures and a JSON report
- [x] MSE, RMSE, and PSNR image similarity metrics
- [x] Optional ONNX Runtime classification with top-k predictions
- [x] Optional CUDA provider selection for compatible ONNX Runtime installations
- [x] Reproducible CPU micro-benchmarks for common operations
- [x] Synthetic-image tests on Python 3.10, 3.11, and 3.12
- [x] Wheel/source distribution build and CLI smoke tests in CI

## Next

- [ ] Add small sample images with explicit reuse licenses
- [ ] Add end-to-end tests for model loading against a documented, redistributable sample model
- [ ] Add optional perceptual image metrics such as SSIM with clear dependency/licensing notes
- [ ] Publish a tagged release after the release checklist is verified

Features should be marked complete only after implementation, documentation, and automated tests are in place.

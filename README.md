<p align="center">
  <img src="assets/visionforge-banner.svg" width="100%" alt="VisionForge AI banner"/>
</p>

<p align="center"><strong>Explore the pixels. Understand the patterns. Build the intelligence.</strong></p>

<p align="center">A practical Python computer-vision toolkit built with OpenCV.</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white" alt="OpenCV"/>
  <img src="https://img.shields.io/badge/Tests-pytest-0A9EDC?style=for-the-badge" alt="pytest"/>
</p>

## Release status

The project is preparing version **0.3.0**. See [`CHANGELOG.md`](CHANGELOG.md) for the feature summary and [`docs/roadmap.md`](docs/roadmap.md) for what remains.

## What it does

VisionForge AI is a learning-focused computer-vision project. Its first working OpenCV toolkit can:

- Inspect an image's dimensions, channels, file format, and file size.
- Detect edges using a Gaussian blur and the Canny algorithm.
- Analyze average RGB channel values and grayscale brightness statistics.
- Convert images to grayscale.
- Resize images to specified dimensions.
- Apply blur, sharpening, and binary threshold filters.
- Generate an RGB channel histogram image.
- Detect and measure contours with configurable thresholding, retrieval mode, and minimum area.
- Batch-process supported image files in a folder and create a JSON success/failure report.
- Compare same-sized images using mean squared error (MSE), root mean squared error (RMSE), and peak signal-to-noise ratio (PSNR).
- Benchmark common image operations with warm-up iterations, timing statistics, and megapixels-per-second estimates.
- Run an end-to-end demo that writes sample outputs and a JSON report.
- Save results to a chosen output path, creating parent folders when needed.
- Validate parameters and show readable errors for files that cannot be opened.

Classical image processing works with the base install. An optional ONNX Runtime classifier can run a compatible model you provide; model weights and label files are not bundled.

## Requirements

- Python 3.10 or newer
- pip

## Install on Windows 11

Open PowerShell in the repository folder:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

If PowerShell blocks environment activation, you can run the environment's Python directly instead:

```powershell
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
```

## Benchmark image operations

Measure in-memory CPU performance without including image loading or file-writing time:

```powershell
visionforge benchmark "path\\to\\image.jpg" --kind edges --iterations 50 --warmup 5 --report "outputs\\benchmark.json"
```

Supported operations are `grayscale`, `edges`, `blur`, `sharpen`, and `threshold`. Results include mean, median, minimum, and maximum latency plus approximate megapixels per second. These are local micro-benchmarks, not a comparison between different computers or a GPU benchmark.

## Optional AI image classification

Install the optional ONNX Runtime dependency:

```powershell
python -m pip install -e ".[onnx]"
```

Provide an ONNX image-classification model and a text file containing one label per line in the exact class order expected by that model:

```powershell
visionforge classify "path\\to\\image.jpg" --model "models\\classifier.onnx" --labels "models\\labels.txt" --top-k 5 --provider auto
```

The classifier expects a float32 NCHW model with three RGB channels and ImageNet mean/std normalization. Fixed model input dimensions are detected automatically; dynamic spatial dimensions default to 224 × 224. This is intended for compatible ImageNet-style classifiers, not arbitrary ONNX models. VisionForge does not download or bundle model weights. Check the model and label source licenses and confirm that the labels match the model before use. The `--provider` option accepts `auto`, `cpu`, or `cuda`. `auto` prefers CUDA when ONNX Runtime reports a compatible CUDA provider, otherwise it uses CPU. To try GPU inference, install a compatible `onnxruntime-gpu` build instead of the CPU `onnxruntime` package and ensure its CUDA/cuDNN requirements match your system. CUDA support depends on the installed runtime and drivers; the command reports the provider it actually selected.

## Run it

Show image metadata:

```powershell
visionforge info "path\\to\\your-image.png"
```

Run Canny edge detection and save the result:

```powershell
visionforge edges "path\\to\\your-image.jpg" --output "outputs\\sample-edges.png"
```

Analyze average colors and brightness:

```powershell
visionforge colors "path\\to\\your-image.jpg"
```

Adjust the Canny thresholds if needed:

```powershell
visionforge edges "path\\to\\your-image.jpg" -o "outputs\\edges.png" --low 60 --high 160
```

Convert to grayscale:

```powershell
visionforge grayscale "path\\to\\your-image.jpg" -o "outputs\\sample-gray.png"
```

Resize an image:

```powershell
visionforge resize "path\\to\\your-image.jpg" -o "outputs\\sample-small.png" --width 640 --height 480
```

You can also run the CLI as a Python module:

```powershell
python -m visionforge.cli --help
python -m visionforge.cli info "C:\\path\\to\\your-image.png"
```

Use your own image path for these commands. Apply a filter:

```powershell
visionforge filter "path\\to\\your-image.jpg" --kind sharpen -o "outputs\\sharpened.png"
```

Generate a color histogram:

```powershell
visionforge histogram "path\\to\\your-image.jpg" -o "outputs\\histogram.png"
```

Detect contours and save an overlay plus a JSON report:

```powershell
visionforge contours "path\\to\\your-image.png" -o "outputs\\contours.png" --threshold 127 --retrieval external --min-area 25 --report "outputs\\contours.json"
```

The command thresholds the image, draws detected contour outlines, and reports each retained contour's area and bounding box. Retrieval modes are `external`, `list`, `tree`, and `ccomp`.

Compare an original image with a processed result in one labeled image:

```powershell
visionforge compare "path\\to\\original.jpg" "path\\to\\processed.png" -o "outputs\\comparison.png" --left-label Original --right-label Edges
```

The comparison tool preserves each image's aspect ratio, fits both into a shared-height canvas, and adds readable labels. It is useful for reviewing filters and edge-detection results side by side.

Compare a reference image with a processed candidate using pixel-level quality metrics:

```powershell
visionforge metrics "outputs\\original.png" "outputs\\processed.png" --report "outputs\\metrics.json" --ssim
```

MSE and RMSE measure average pixel error; lower values mean closer pixel values. PSNR is reported in decibels, with higher values indicating closer similarity. Identical decoded images produce infinite PSNR. Images must have the same dimensions; MSE, RMSE, and PSNR are pixel-level metrics, not perceptual quality scores. To include structural similarity (SSIM), install `python -m pip install -e ".[quality]"` and add `--ssim`. SSIM is optional and compares local structure as well as pixel values.

Process every supported image in a folder and write a JSON summary:

```powershell
visionforge batch "images" --output-dir "outputs\\batch" --kind edges
```

Supported batch operations are `blur`, `sharpen`, `threshold`, `grayscale`, and `edges`. Each output is saved as PNG; failures are recorded per file so one bad image does not stop the rest of the batch. A `batch-report.json` file is written inside the output folder by default. Use `--report "path\\to\\report.json"` to choose a different report path.

Run the complete reproducible demo without downloading a dataset:

```powershell
visionforge demo
# Or choose another output folder:
visionforge demo --output-dir "outputs\\first-run"
```

The demo creates a synthetic image, processes it, and writes edge, grayscale, resized, histogram images, and `report.json` into the output directory (ignored by Git). You can also run `python examples/generate_demo.py` from a source checkout.

## Run tests

```powershell
python -m pytest
```

The test suite creates temporary sample images automatically, so you do not need to download any dataset to test the core functionality.

## Project structure

```text
VisionForge-AI/
├── assets/
│   └── visionforge-banner.svg
├── visionforge/
│   ├── __init__.py
│   ├── image_info.py
│   ├── color_analysis.py
│   ├── histogram.py
│   ├── filters.py
│   ├── demo.py
│   ├── comparison.py
│   ├── contours.py
│   ├── batch.py
│   └── cli.py
├── examples/
│   ├── README.md
│   └── generate_demo.py
├── docs/
│   ├── architecture.md
│   └── roadmap.md
├── tests/
│   ├── test_image_info.py
│   ├── test_comparison.py
│   └── test_contours.py
├── .github/
│   └── workflows/
│       └── tests.yml
├── pyproject.toml
├── requirements.txt
├── LICENSE
└── README.md
```

## How Canny edge detection works here

1. Load the source image with OpenCV.
2. Convert the image to grayscale.
3. Apply a small Gaussian blur to reduce noise.
4. Run Canny edge detection using configurable lower and upper thresholds.
5. Save the resulting single-channel edge map.

Results depend on image content, noise, lighting, and threshold choices. Edge detection highlights intensity boundaries; it does not identify objects by itself.

## Roadmap

- [x] OpenCV image loading and metadata inspection
- [x] Canny edge detection with configurable thresholds
- [x] Grayscale conversion and image resizing
- [x] Command-line interface
- [x] Automated tests for core operations and invalid inputs
- [x] Add basic RGB color and brightness analysis
- [x] Add blur, sharpen, and binary threshold filters
- [x] Add RGB histogram rendering
- [x] Add a CLI demo with generated sample outputs and a JSON report
- [x] Add a reproducible demo that generates its own test image and outputs
- [x] Create labeled side-by-side comparison images for processing results
- [x] Add contour detection with configurable retrieval modes and JSON reports
- [x] Add folder-based batch processing with per-file error reporting
- [x] Add optional ONNX inference for compatible user-supplied image-classification models
- [x] Add repeatable in-memory CPU benchmarks for core image operations
- [ ] Add sample images with clear reuse licenses

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for development setup, test commands, design guidelines, and pull request expectations. Bug reports and feature ideas can use the templates in GitHub Issues.

## Development principles

- Keep functions small and readable.
- Validate input and fail with useful error messages.
- Test using reproducible synthetic images.
- Separate classical image processing from future model-based features.
- Document limitations and respect dataset and model licenses.

## About

**Mohamed | [@ruhioki](https://github.com/ruhioki)**

I'm an Artificial Intelligence and Data Science student interested in AI engineering, GPU technology, performance optimization, and software development. VisionForge AI is a hands-on project for learning computer vision by building and testing real tools.

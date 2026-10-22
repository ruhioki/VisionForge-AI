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
- Run an end-to-end demo that writes sample outputs and a JSON report.
- Save results to a chosen output path, creating parent folders when needed.
- Validate parameters and show readable errors for files that cannot be opened.

This release uses classical image processing. It does not claim to provide trained image classification or object-detection models yet.

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

Process every supported image in a folder and write a JSON summary:

```powershell
visionforge batch "images" --output-dir "outputs\\batch" --kind edges
```

Supported batch operations are `blur`, `sharpen`, `threshold`, `grayscale`, and `edges`. Each output is saved as PNG; failures are recorded per file so one bad image does not stop the rest of the batch.

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
- [ ] Explore pretrained classification models in a separate optional module
- [ ] Add sample images with clear reuse licenses

## Development principles

- Keep functions small and readable.
- Validate input and fail with useful error messages.
- Test using reproducible synthetic images.
- Separate classical image processing from future model-based features.
- Document limitations and respect dataset and model licenses.

## About

**Mohamed | [@ruhioki](https://github.com/ruhioki)**

I'm an Artificial Intelligence and Data Science student interested in AI engineering, GPU technology, performance optimization, and software development. VisionForge AI is a hands-on project for learning computer vision by building and testing real tools.

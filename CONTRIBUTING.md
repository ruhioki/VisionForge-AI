# Contributing to VisionForge AI

Thanks for helping improve VisionForge AI. The project aims to keep computer-vision tools practical, reproducible, and understandable.

## Development setup

Python 3.10 or newer is required. On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Optional dependencies:

- ONNX classification: `python -m pip install -e ".[onnx]"`
- SSIM image metrics: `python -m pip install -e ".[quality]"`

For GPU inference, use a compatible `onnxruntime-gpu` installation instead of the CPU `onnxruntime` package and verify the CUDA/cuDNN requirements for your environment.

## Run checks

```powershell
python -m pytest -v
visionforge --help
python -m visionforge.cli --help
```

The test suite uses temporary synthetic images and mocked optional model runtimes. It should not require downloaded datasets or model weights.

## Adding a feature

1. Open an issue for substantial changes and describe the user problem.
2. Keep reusable processing logic in a focused module under `visionforge/`; keep CLI parsing and output in `visionforge/cli.py`.
3. Validate invalid inputs and provide readable errors.
4. Add tests for normal behavior, edge cases, and invalid inputs.
5. Update the README, architecture notes, and roadmap when behavior changes.
6. Run the test suite locally and open a pull request against `main`.

## Design guidelines

- Keep core dependencies small. Put heavyweight or specialized dependencies in optional extras.
- Do not download models or datasets automatically unless the user explicitly requests it.
- Document model compatibility, licenses, and limitations.
- Prefer deterministic synthetic fixtures over large binary test assets.
- Avoid claims of GPU acceleration unless the selected backend actually uses a GPU.
- Keep command-line output machine-readable when reporting structured results.

## Pull requests

Please explain the problem, summarize the implementation, list test coverage, and note any new dependencies. CI must pass on Python 3.10, 3.11, and 3.12, including the package-build smoke test.

# Examples

Run the reproducible demo from the repository root after installing the package:

```powershell
python examples/generate_demo.py
```

It creates a synthetic geometric test image, runs metadata and color analysis, and writes edge, grayscale, resized, and histogram outputs plus a JSON report into `outputs/`. No external image dataset is required. The generated output directory is ignored by Git to avoid committing machine-generated files.

## Benchmark an operation

```powershell
visionforge benchmark "path\\to\\image.jpg" --kind edges --iterations 50 --warmup 5 --report "outputs\\benchmark.json"
```

## Compare image quality

```powershell
visionforge metrics "outputs\\original.png" "outputs\\processed.png" --ssim --report "outputs\\metrics.json"
```

Install the optional SSIM dependency first with `python -m pip install -e ".[quality]"`. See the main README for all commands and `docs/model-compatibility.md` before using an external ONNX model.

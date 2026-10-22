# Examples

Run the reproducible demo from the repository root after installing the package:

```powershell
python examples/generate_demo.py
```

It creates a synthetic geometric test image, runs metadata and color analysis, and writes edge, grayscale, resized, and histogram outputs plus a JSON report into `outputs/`. No external image dataset is required. The generated output directory is ignored by Git to avoid committing machine-generated files.

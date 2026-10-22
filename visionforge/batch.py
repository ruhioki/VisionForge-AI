"""Batch processing for folders of common image formats."""

from pathlib import Path
from typing import Any

from visionforge.filters import apply_filter
from visionforge.image_info import convert_grayscale, detect_edges

SUPPORTED_EXTENSIONS = {".bmp", ".jpeg", ".jpg", ".png", ".tif", ".tiff", ".webp"}
SUPPORTED_OPERATIONS = {"blur", "sharpen", "threshold", "grayscale", "edges"}


def batch_process(
    input_dir: str | Path,
    output_dir: str | Path,
    kind: str,
) -> dict[str, Any]:
    """Apply an operation to each supported image and report per-file outcomes."""
    source_dir = Path(input_dir).expanduser()
    target_dir = Path(output_dir).expanduser()
    if not source_dir.is_dir():
        raise ValueError(f"Input directory does not exist or is not a directory: {source_dir}")
    if kind not in SUPPORTED_OPERATIONS:
        raise ValueError(f"Unsupported batch operation: {kind}. Choose from {', '.join(sorted(SUPPORTED_OPERATIONS))}.")

    files = sorted(
        (path for path in source_dir.iterdir() if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS),
        key=lambda path: path.name.casefold(),
    )
    if not files:
        raise ValueError(f"No supported image files found in: {source_dir}")

    target_dir.mkdir(parents=True, exist_ok=True)
    succeeded = []
    failed = []
    for source in files:
        output = target_dir / f"{source.stem}-{kind}.png"
        try:
            if kind in {"blur", "sharpen", "threshold"}:
                result_path = apply_filter(source, output, kind)
            elif kind == "grayscale":
                result_path = convert_grayscale(source, output)
            else:
                result_path = detect_edges(source, output)
            succeeded.append({"input": str(source), "output": str(result_path)})
        except (OSError, ValueError, RuntimeError) as exc:
            failed.append({"input": str(source), "error": str(exc)})

    return {
        "input_directory": str(source_dir),
        "output_directory": str(target_dir),
        "operation": kind,
        "discovered": len(files),
        "succeeded": len(succeeded),
        "failed": len(failed),
        "results": succeeded,
        "errors": failed,
    }

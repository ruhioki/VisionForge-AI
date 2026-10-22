"""Create a clean ZIP archive containing the VisionForge source project."""

import argparse
import os
from pathlib import Path
import zipfile


ROOT = Path(__file__).resolve().parent.parent
ARCHIVE_ROOT = "VisionForge-AI"
INCLUDED_ROOT_FILES = (
    ".gitignore",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "LICENSE",
    "README.md",
    "pyproject.toml",
    "requirements.txt",
)
INCLUDED_DIRECTORIES = (".github", "assets", "docs", "examples", "tests", "tools", "visionforge")
EXCLUDED_DIRECTORIES = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "env",
    "venv",
}


def _project_files() -> list[Path]:
    files = [ROOT / name for name in INCLUDED_ROOT_FILES if (ROOT / name).is_file()]
    for directory in INCLUDED_DIRECTORIES:
        base = ROOT / directory
        if not base.is_dir():
            continue
        for current, dirnames, filenames in os.walk(base):
            dirnames[:] = sorted(
                name
                for name in dirnames
                if name not in EXCLUDED_DIRECTORIES and not name.endswith(".egg-info")
            )
            for filename in sorted(filenames):
                path = Path(current) / filename
                if path.is_symlink() or path.suffix in {".pyc", ".pyo"} or ".egg-info" in path.parts:
                    continue
                files.append(path)
    return sorted(files, key=lambda path: path.relative_to(ROOT).as_posix())


def create_source_bundle(output: str | Path = "dist/VisionForge-AI-source.zip") -> Path:
    """Write the source archive and return its absolute path."""
    output_path = Path(output).expanduser()
    if not output_path.is_absolute():
        output_path = ROOT / output_path
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_resolved = output_path.resolve()

    with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for source in _project_files():
            if source.resolve() == output_resolved:
                continue
            relative = source.relative_to(ROOT).as_posix()
            archive.write(source, f"{ARCHIVE_ROOT}/{relative}")
    return output_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-o",
        "--output",
        default="dist/VisionForge-AI-source.zip",
        help="ZIP destination (default: dist/VisionForge-AI-source.zip)",
    )
    args = parser.parse_args()
    archive = create_source_bundle(args.output)
    print(f"Created source bundle: {archive}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

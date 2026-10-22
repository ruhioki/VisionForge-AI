from pathlib import Path

import cv2
import numpy as np
import pytest

from visionforge.batch import batch_process


def _write_image(path, color=(255, 255, 255)):
    image = np.zeros((24, 32, 3), dtype=np.uint8)
    image[5:18, 7:25] = color
    assert cv2.imwrite(str(path), image)


def test_batch_processes_supported_files_and_ignores_other_files(tmp_path):
    source = tmp_path / "images"
    source.mkdir()
    _write_image(source / "B.PNG")
    _write_image(source / "a.jpg")
    (source / "notes.txt").write_text("not an image", encoding="utf-8")
    output = tmp_path / "outputs"

    report = batch_process(source, output, "grayscale")

    assert report["discovered"] == 2
    assert report["succeeded"] == 2
    assert report["failed"] == 0
    assert [Path(item["input"]).name for item in report["results"]] == ["a.jpg", "B.PNG"]
    for item in report["results"]:
        result = cv2.imread(item["output"], cv2.IMREAD_UNCHANGED)
        assert result is not None and result.ndim == 2


def test_batch_continues_after_corrupt_image(tmp_path):
    source = tmp_path / "images"
    source.mkdir()
    _write_image(source / "good.png")
    (source / "broken.png").write_text("not a real image", encoding="utf-8")

    report = batch_process(source, tmp_path / "outputs", "edges")

    assert report["discovered"] == 2
    assert report["succeeded"] == 1
    assert report["failed"] == 1
    assert Path(report["results"][0]["output"]).is_file()
    assert "Could not read image" in report["errors"][0]["error"]


def test_batch_rejects_missing_directory(tmp_path):
    with pytest.raises(ValueError, match="does not exist"):
        batch_process(tmp_path / "missing", tmp_path / "outputs", "blur")


def test_batch_rejects_empty_image_folder(tmp_path):
    source = tmp_path / "empty"
    source.mkdir()
    with pytest.raises(ValueError, match="No supported image files"):
        batch_process(source, tmp_path / "outputs", "blur")


def test_batch_rejects_unknown_operation(tmp_path):
    source = tmp_path / "images"
    source.mkdir()
    with pytest.raises(ValueError, match="Unsupported batch operation"):
        batch_process(source, tmp_path / "outputs", "upscale")


def test_cli_help_lists_batch_command():
    from visionforge.cli import build_parser

    assert "batch" in build_parser().format_help()


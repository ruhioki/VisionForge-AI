"""Regression checks for the static browser companion."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "web-app"


def test_browser_app_has_core_workbench_controls() -> None:
    html = (WEB / "index.html").read_text(encoding="utf-8")
    for required in (
        'id="file"',
        'id="originalBox"',
        'id="processedBox"',
        'id="tool"',
        'id="preset"',
        'id="apply"',
        'id="download"',
        'id="downloadOriginal"',
        'id="histogram"',
        "function process(",
        "function downloadCanvas(",
    ):
        assert required in html


def test_browser_app_explains_privacy_and_filter_limitations() -> None:
    html = (WEB / "index.html").read_text(encoding="utf-8").lower()
    assert "not uploaded" in html
    assert "sobel" in html
    assert "not opencv's exact canny algorithm" in html


def test_manifest_is_valid_and_points_to_existing_assets() -> None:
    manifest = json.loads((WEB / "manifest.webmanifest").read_text(encoding="utf-8"))
    assert manifest["name"] == "VisionForge AI Image Lab"
    assert manifest["display"] == "standalone"
    for icon in manifest["icons"]:
        assert (WEB / icon["src"]).is_file()


def test_service_worker_precaches_the_app_shell() -> None:
    worker = (WEB / "sw.js").read_text(encoding="utf-8")
    for asset in ('"./"', '"./index.html"', '"./manifest.webmanifest"', '"./icon.svg"'):
        assert asset in worker

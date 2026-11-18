"""Regression checks for the static browser companion and owner dashboard."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "web-app"


def test_browser_app_has_core_workbench_controls() -> None:
    html = (WEB / "index.html").read_text(encoding="utf-8")
    for required in (
        'id="file"', 'id="originalBox"', 'id="processedBox"', 'id="tool"',
        'id="preset"', 'id="apply"', 'id="download"', 'id="downloadOriginal"',
        'id="histogram"', 'function process(', 'function downloadCanvas(',
        'href="./admin.html"', 'src="./site-content.js"',
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
    for asset in ('"./"', '"./index.html"', '"./admin.html"', '"./site-content.js"',
                  '"./supabase-config.js"', '"./manifest.webmanifest"', '"./icon.svg"'):
        assert asset in worker
    assert "visionforge-image-lab-v5" in worker


def test_shared_login_supports_regular_accounts_and_github_owner() -> None:
    login = (WEB / "login.html").read_text(encoding="utf-8")
    admin = (WEB / "admin.html").read_text(encoding="utf-8")
    config = (WEB / "supabase-config.js").read_text(encoding="utf-8")
    schema = (ROOT / "supabase" / "owner-dashboard.sql").read_text(encoding="utf-8").lower()
    assert "signInWithPassword" in login
    assert "signUp" in login
    assert "signInWithOAuth" in login
    assert 'provider:"github"' in login
    assert "OWNER_GITHUB_USERNAME" in admin
    assert "login.html?next=admin" in admin
    assert 'OWNER_EMAIL = "thestromer90@gmail.com"' in config
    assert 'OWNER_GITHUB_USERNAME = "ruhioki"' in config
    assert "service-role" in admin.lower()
    assert "enable row level security" in schema
    assert "site_admins" in schema
    assert "is_site_admin()" in schema
    assert "using (published = true)" in schema
    assert "add column if not exists" in schema
    assert "nullif(lower(i.identity_data" in schema

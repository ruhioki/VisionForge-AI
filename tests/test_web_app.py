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
    assert "visionforge-image-lab-v9" in worker
    assert '"./civic-scan.html"' in worker


def test_shared_login_supports_regular_accounts_and_github_owner() -> None:
    login = (WEB / "login.html").read_text(encoding="utf-8")
    admin = (WEB / "admin.html").read_text(encoding="utf-8")
    config = (WEB / "supabase-config.js").read_text(encoding="utf-8")
    schema = (ROOT / "supabase" / "owner-dashboard.sql").read_text(encoding="utf-8").lower()
    assert "signInWithPassword" in login
    assert "resetPasswordForEmail" in login
    assert "updateUser({ password })" in login
    assert "password-toggle" in login
    assert "forgot-password" in login
    assert "recovery=1" in login
    assert 'href="./icon.svg"' in login
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
    assert "auth.jwt() ->> 'aal'" in schema
    assert "= 'aal2'" in schema



def test_owner_control_center_exposes_only_database_backed_site_controls() -> None:
    admin = (WEB / "admin.html").read_text(encoding="utf-8")
    public_content = (WEB / "site-content.js").read_text(encoding="utf-8")
    homepage = (WEB / "index.html").read_text(encoding="utf-8")
    schema = (ROOT / "supabase" / "owner-dashboard.sql").read_text(encoding="utf-8").lower()
    for control in ("announcement-text", "announcement-enabled", "maintenance-mode",
                    "maintenance-message", "Save all controls", "checkOwner(activeUser)"):
        assert control in admin
    for column in ("announcement_text", "announcement_enabled", "maintenance_mode", "maintenance_message"):
        assert column in schema
        assert column in public_content
    assert 'id="site-announcement"' in homepage
    assert 'id="maintenance-state"' in homepage
    assert 'workspace.hidden = true' in public_content
    assert "create policy \"authorized owner manages site content\"" in schema


def test_civic_scan_desk_supports_local_document_workflow() -> None:
    scanner = (WEB / "civic-scan.html").read_text(encoding="utf-8")
    homepage = (WEB / "index.html").read_text(encoding="utf-8")
    for feature in (
        'id="file"', 'id="camera"', 'id="capture"', 'id="ocr"',
        'Tesseract.createWorker', 'BarcodeDetector', 'id="text"',
        'id="download-text"', 'id="language"', 'value="tam"', 'value="hin"', 'class="checks"', 'Nothing is submitted to a government database',
        'does not verify whether a document is genuine',
    ):
        assert feature in scanner
    assert 'href="./civic-scan.html"' in homepage


def test_phone_mfa_has_enrollment_and_login_challenge() -> None:
    security = (WEB / "security.html").read_text(encoding="utf-8")
    login = (WEB / "login.html").read_text(encoding="utf-8")
    homepage = (WEB / "index.html").read_text(encoding="utf-8")
    worker = (WEB / "sw.js").read_text(encoding="utf-8")
    assert 'auth.mfa.enroll({factorType:"phone",phone})' in security
    assert 'auth.mfa.challenge({factorId})' in security
    assert 'auth.mfa.verify({factorId,challengeId,code})' in security
    assert 'getAuthenticatorAssuranceLevel()' in login
    assert 'auth.mfa.verify({factorId:pendingFactorId,challengeId:pendingChallengeId,code})' in login
    assert 'href="./security.html"' in homepage
    assert '"./security.html"' in worker
    assert "visionforge-image-lab-v9" in worker


def test_assistant_page_has_accessible_ai_and_local_developer_tools() -> None:
    assistant = (WEB / "assistant.html").read_text(encoding="utf-8")
    homepage = (WEB / "index.html").read_text(encoding="utf-8")
    worker = (WEB / "sw.js").read_text(encoding="utf-8")
    for feature in (
        'id="chat-log"', 'aria-live="polite"', 'id="mode-research"',
        'supabase.functions.invoke("assistant"', 'id="json-format"',
        'id="url-encode"', 'id="base-encode"', 'id="diff-run"',
        'id="time-convert"', 'id="uuid-generate"', 'href="./civic-scan.html"',
        'Do not submit confidential code', 'high-impact decisions',
    ):
        assert feature in assistant
    assert 'href="./assistant.html"' in homepage
    assert '"./assistant.html"' in worker
    assert "visionforge-image-lab-v9" in worker


def test_assistant_edge_function_authenticates_and_keeps_ai_key_server_side() -> None:
    function = (ROOT / "supabase" / "functions" / "assistant" / "index.ts").read_text(encoding="utf-8")
    docs = (ROOT / "docs" / "assistant-setup.md").read_text(encoding="utf-8")
    assert 'Deno.env.get("OPENAI_API_KEY")' in function
    assert '"/auth/v1/user"' in function
    assert 'type:"web_search"' in function
    assert "store:false" in function
    assert "supabase functions deploy assistant" in docs
    assert "never put it in" in docs

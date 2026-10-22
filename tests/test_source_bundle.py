import zipfile

from tools.create_source_bundle import create_source_bundle


def test_source_bundle_contains_project_and_excludes_generated_files(tmp_path):
    archive_path = create_source_bundle(tmp_path / "VisionForge-AI-source.zip")

    with zipfile.ZipFile(archive_path) as archive:
        names = set(archive.namelist())

    assert "VisionForge-AI/README.md" in names
    assert "VisionForge-AI/visionforge/scan.py" in names
    assert "VisionForge-AI/examples/document_scanner.py" in names
    assert not any("/.git/" in name or "/outputs/" in name for name in names)
    assert not any("__pycache__" in name or name.endswith(".pyc") for name in names)

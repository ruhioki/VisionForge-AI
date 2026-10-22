import json
from importlib.metadata import version

import pytest

import visionforge
from visionforge.cli import main


def test_package_version_matches_metadata():
    assert visionforge.__version__ == version("visionforge-ai")


def test_version_flag(capsys):
    with pytest.raises(SystemExit) as exc:
        main(["--version"])
    assert exc.value.code == 0
    assert visionforge.__version__ in capsys.readouterr().out


def test_info_command_prints_json(sample_image, capsys):
    assert main(["info", str(sample_image)]) == 0
    assert json.loads(capsys.readouterr().out)["width"] == 100


def test_edges_command_saves_file(sample_image, tmp_path, capsys):
    output = tmp_path / "edges.png"
    assert main(["edges", str(sample_image), "-o", str(output)]) == 0
    assert output.exists()


def test_missing_image_returns_exit_code_2(tmp_path, capsys):
    assert main(["info", str(tmp_path / "missing.png")]) == 2
    assert "error:" in capsys.readouterr().err


def test_invalid_thresholds_return_exit_code_2(sample_image, tmp_path, capsys):
    code = main(["edges", str(sample_image), "-o", str(tmp_path / "e.png"), "--low", "200", "--high", "100"])
    assert code == 2


def test_demo_command(tmp_path, capsys):
    assert main(["demo", "-o", str(tmp_path / "demo")]) == 0
    assert (tmp_path / "demo" / "report.json").exists()

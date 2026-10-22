import json

from visionforge.demo import run_demo


def test_demo_writes_all_outputs_and_report(tmp_path):
    report = run_demo(tmp_path / "demo")
    for name, path in report["outputs"].items():
        assert (tmp_path / "demo").exists()
        assert path.endswith(".png"), name
    saved = json.loads((tmp_path / "demo" / "report.json").read_text(encoding="utf-8"))
    assert saved["project"] == "VisionForge AI"
    assert saved["image_info"]["width"] == 640
    assert saved["image_info"]["height"] == 360


def test_demo_is_deterministic(tmp_path):
    first = run_demo(tmp_path / "a")["color_analysis"]["mean_rgb"]
    second = run_demo(tmp_path / "b")["color_analysis"]["mean_rgb"]
    assert first == second

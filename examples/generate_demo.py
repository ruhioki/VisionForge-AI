"""Run VisionForge's end-to-end demo from a source checkout."""

import argparse
import json

from visionforge.demo import run_demo


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate VisionForge sample images and a JSON report.")
    parser.add_argument("--output-dir", default="outputs", help="directory for generated outputs")
    args = parser.parse_args()
    print(json.dumps(run_demo(args.output_dir), indent=2))


if __name__ == "__main__":
    main()

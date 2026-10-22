"""Command-line interface for VisionForge AI."""

import argparse
import json
import sys
from collections.abc import Sequence

from visionforge.color_analysis import analyze_colors
from visionforge.demo import run_demo
from visionforge.filters import apply_filter
from visionforge.histogram import save_histogram
from visionforge.image_info import convert_grayscale, detect_edges, inspect_image, resize_image


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="visionforge", description="Inspect images and run OpenCV processing.")
    commands = parser.add_subparsers(dest="command", required=True)

    info = commands.add_parser("info", help="show image metadata")
    info.add_argument("input", help="path to the source image")

    colors = commands.add_parser("colors", help="analyze average RGB color and brightness")
    colors.add_argument("input", help="path to the source image")

    edges = commands.add_parser("edges", help="run Canny edge detection")
    edges.add_argument("input", help="path to the source image")
    edges.add_argument("-o", "--output", required=True, help="where to save the edge map")
    edges.add_argument("--low", type=int, default=100, help="low Canny threshold (default: 100)")
    edges.add_argument("--high", type=int, default=200, help="high Canny threshold (default: 200)")

    gray = commands.add_parser("grayscale", help="convert an image to grayscale")
    gray.add_argument("input", help="path to the source image")
    gray.add_argument("-o", "--output", required=True, help="where to save the result")

    resize = commands.add_parser("resize", help="resize an image")
    resize.add_argument("input", help="path to the source image")
    resize.add_argument("-o", "--output", required=True, help="where to save the result")
    resize.add_argument("--width", type=int, required=True, help="output width in pixels")
    resize.add_argument("--height", type=int, required=True, help="output height in pixels")

    filt = commands.add_parser("filter", help="apply blur, sharpen, or threshold")
    filt.add_argument("input", help="path to the source image")
    filt.add_argument("--kind", choices=("blur", "sharpen", "threshold"), required=True)
    filt.add_argument("-o", "--output", required=True, help="where to save the result")

    hist = commands.add_parser("histogram", help="save an RGB channel histogram image")
    hist.add_argument("input", help="path to the source image")
    hist.add_argument("-o", "--output", required=True, help="where to save the histogram")

    demo = commands.add_parser("demo", help="generate sample outputs without a dataset")
    demo.add_argument("-o", "--output-dir", default="outputs", help="output directory (default: outputs)")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "info":
            print(json.dumps(inspect_image(args.input), indent=2))
        elif args.command == "colors":
            print(json.dumps(analyze_colors(args.input), indent=2))
        elif args.command == "edges":
            print(f"Saved edge map: {detect_edges(args.input, args.output, args.low, args.high)}")
        elif args.command == "grayscale":
            print(f"Saved grayscale image: {convert_grayscale(args.input, args.output)}")
        elif args.command == "resize":
            print(f"Saved resized image: {resize_image(args.input, args.output, args.width, args.height)}")
        elif args.command == "filter":
            print(f"Saved {args.kind} output: {apply_filter(args.input, args.output, args.kind)}")
        elif args.command == "histogram":
            print(f"Saved histogram: {save_histogram(args.input, args.output)}")
        elif args.command == "demo":
            report = run_demo(args.output_dir)
            print(json.dumps(report, indent=2))
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

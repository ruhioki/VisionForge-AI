"""Command-line interface for VisionForge AI."""

import argparse
import json
import sys
from collections.abc import Sequence

from visionforge.color_analysis import analyze_colors
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
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "info":
            result = inspect_image(args.input)
        elif args.command == "colors":
            result = analyze_colors(args.input)
        elif args.command == "edges":
            print(f"Saved edge map: {detect_edges(args.input, args.output, args.low, args.high)}")
            return 0
        elif args.command == "grayscale":
            print(f"Saved grayscale image: {convert_grayscale(args.input, args.output)}")
            return 0
        elif args.command == "resize":
            print(f"Saved resized image: {resize_image(args.input, args.output, args.width, args.height)}")
            return 0
        else:
            return 2
        print(json.dumps(result, indent=2))
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

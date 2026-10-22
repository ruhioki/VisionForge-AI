"""Command-line interface for VisionForge AI."""

import argparse
import json
import sys
from collections.abc import Sequence

from visionforge.image_info import (
    convert_grayscale,
    detect_edges,
    inspect_image,
    resize_image,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="visionforge",
        description="Inspect images and run basic OpenCV processing.",
    )
    commands = parser.add_subparsers(dest="command", required=True)

    info = commands.add_parser("info", help="show image metadata")
    info.add_argument("input", help="path to the source image")

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
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "info":
            print(json.dumps(inspect_image(args.input), indent=2))
        elif args.command == "edges":
            print(f"Saved edge map: {detect_edges(args.input, args.output, args.low, args.high)}")
        elif args.command == "grayscale":
            print(f"Saved grayscale image: {convert_grayscale(args.input, args.output)}")
        elif args.command == "resize":
            print(f"Saved resized image: {resize_image(args.input, args.output, args.width, args.height)}")
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

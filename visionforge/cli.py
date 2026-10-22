"""Command-line interface for VisionForge AI."""

import argparse
import json
import sys
from collections.abc import Sequence
from pathlib import Path

from visionforge import __version__
from visionforge.batch import batch_process
from visionforge.benchmark import benchmark_image
from visionforge.classification import classify_image
from visionforge.color_analysis import analyze_colors
from visionforge.comparison import create_comparison
from visionforge.contours import detect_contours
from visionforge.demo import run_demo
from visionforge.filters import apply_filter
from visionforge.histogram import save_histogram
from visionforge.image_info import convert_grayscale, detect_edges, inspect_image, resize_image
from visionforge.quality import calculate_image_metrics
from visionforge.scan import scan_document


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="visionforge", description="Inspect images and run OpenCV processing.")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
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

    compare = commands.add_parser("compare", help="create a side-by-side image comparison")
    compare.add_argument("original", help="path to the original image")
    compare.add_argument("processed", help="path to the processed image")
    compare.add_argument("-o", "--output", required=True, help="where to save the comparison image")
    compare.add_argument("--left-label", default="Original", help="label for the left image")
    compare.add_argument("--right-label", default="Processed", help="label for the right image")

    metrics = commands.add_parser("metrics", help="measure pixel-level similarity between two same-sized images")
    metrics.add_argument("reference", help="path to the reference image")
    metrics.add_argument("candidate", help="path to the image being evaluated")
    metrics.add_argument("--report", help="optional JSON report path")
    metrics.add_argument("--ssim", action="store_true", help="include optional structural similarity (SSIM)")

    contours = commands.add_parser("contours", help="detect and measure image contours")
    contours.add_argument("input", help="path to the source image")
    contours.add_argument("-o", "--output", required=True, help="where to save the contour overlay")
    contours.add_argument("--threshold", type=int, default=127, help="binary threshold from 0 to 255")
    contours.add_argument("--retrieval", choices=("external", "list", "tree", "ccomp"), default="external", help="contour retrieval mode")
    contours.add_argument("--min-area", type=float, default=0.0, help="ignore contours smaller than this pixel area")
    contours.add_argument("--report", help="optional JSON report path")

    batch = commands.add_parser("batch", help="process every supported image in a folder")
    batch.add_argument("input_dir", help="folder containing source images")
    batch.add_argument("-o", "--output-dir", required=True, help="folder for processed images and report")
    batch.add_argument("--kind", choices=("blur", "sharpen", "threshold", "grayscale", "edges"), required=True, help="operation to apply to every image")
    batch.add_argument("--report", help="JSON report path (default: <output-dir>/batch-report.json)")

    benchmark = commands.add_parser("benchmark", help="measure an image operation in memory")
    benchmark.add_argument("input", help="path to the source image")
    benchmark.add_argument("--kind", choices=("grayscale", "edges", "blur", "sharpen", "threshold"), required=True)
    benchmark.add_argument("--iterations", type=int, default=25, help="timed iterations (default: 25)")
    benchmark.add_argument("--warmup", type=int, default=3, help="warm-up iterations (default: 3)")
    benchmark.add_argument("--report", help="optional JSON report path")

    classify = commands.add_parser("classify", help="classify an image with a user-supplied ONNX model")
    classify.add_argument("input", help="path to the source image")
    classify.add_argument("--model", required=True, help="path to a compatible ONNX classification model")
    classify.add_argument("--labels", required=True, help="text file with one class label per line")
    classify.add_argument("--top-k", type=int, default=5, help="number of predictions to show (default: 5)")
    classify.add_argument("--provider", choices=("auto", "cpu", "cuda"), default="auto", help="inference provider (default: auto)")

    demo = commands.add_parser("demo", help="generate sample outputs without a dataset")
    demo.add_argument("-o", "--output-dir", default="outputs", help="output directory (default: outputs)")

    scan = commands.add_parser("scan", help="detect a document and correct its perspective")
    scan.add_argument("input", help="path to the photographed document")
    scan.add_argument("-o", "--output", required=True, help="where to save the corrected page")
    scan.add_argument("--min-area", type=float, default=0.15, help="minimum page area as a fraction of the image")
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
        elif args.command == "compare":
            result = create_comparison(args.original, args.processed, args.output, args.left_label, args.right_label)
            print(f"Saved comparison: {result}")
        elif args.command == "metrics":
            report = calculate_image_metrics(args.reference, args.candidate, include_ssim=args.ssim)
            if args.report:
                report_path = Path(args.report).expanduser()
                report_path.parent.mkdir(parents=True, exist_ok=True)
                report_path.write_text(json.dumps(report, indent=2, allow_nan=True), encoding="utf-8")
                report["report_path"] = str(report_path)
            print(json.dumps(report, indent=2, allow_nan=True))
        elif args.command == "contours":
            report = detect_contours(args.input, args.output, args.threshold, args.retrieval, args.min_area)
            if args.report:
                report_path = Path(args.report).expanduser()
                report_path.parent.mkdir(parents=True, exist_ok=True)
                report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
                report["report_path"] = str(report_path)
            print(json.dumps(report, indent=2))
        elif args.command == "batch":
            report = batch_process(args.input_dir, args.output_dir, args.kind)
            report_path = Path(args.report).expanduser() if args.report else Path(args.output_dir).expanduser() / "batch-report.json"
            report_path.parent.mkdir(parents=True, exist_ok=True)
            report["report_path"] = str(report_path)
            report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
            print(json.dumps(report, indent=2))
        elif args.command == "benchmark":
            report = benchmark_image(args.input, args.kind, args.iterations, args.warmup)
            if args.report:
                report_path = Path(args.report).expanduser()
                report_path.parent.mkdir(parents=True, exist_ok=True)
                report["report_path"] = str(report_path)
                report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
            print(json.dumps(report, indent=2))
        elif args.command == "classify":
            report = classify_image(args.input, args.model, args.labels, args.top_k, args.provider)
            print(json.dumps(report, indent=2))
        elif args.command == "demo":
            report = run_demo(args.output_dir)
            print(json.dumps(report, indent=2))
        elif args.command == "scan":
            report = scan_document(args.input, args.output, args.min_area)
            print(json.dumps(report, indent=2))
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

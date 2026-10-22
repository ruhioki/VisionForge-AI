"""Generate a synthetic demo image and run VisionForge processing on it.

Run from the repository root with the project installed:
    python examples/generate_demo.py
Outputs are written to the outputs/ directory (ignored by Git).
"""

from pathlib import Path

import cv2
import numpy as np

from visionforge.color_analysis import analyze_colors
from visionforge.image_info import convert_grayscale, detect_edges, inspect_image, resize_image


def main() -> None:
    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)
    source = output_dir / "visionforge-demo.png"

    # Create a repeatable image so the demo needs no external dataset.
    image = np.full((360, 640, 3), (32, 25, 18), dtype=np.uint8)
    cv2.rectangle(image, (70, 70), (260, 285), (80, 190, 245), thickness=-1)
    cv2.circle(image, (430, 165), 88, (180, 90, 220), thickness=-1)
    cv2.line(image, (55, 320), (585, 320), (245, 245, 245), thickness=5)
    cv2.putText(image, "VisionForge AI", (145, 45), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (245, 245, 245), 2, cv2.LINE_AA)
    if not cv2.imwrite(str(source), image):
        raise RuntimeError(f"Could not create demo image: {source}")

    print("Image information:")
    print(inspect_image(source))
    print("\nColor analysis:")
    print(analyze_colors(source))
    print("\nProcessing images...")
    print(f"Edges: {detect_edges(source, output_dir / 'visionforge-edges.png')}")
    print(f"Grayscale: {convert_grayscale(source, output_dir / 'visionforge-grayscale.png')}")
    print(f"Resized: {resize_image(source, output_dir / 'visionforge-resized.png', 320, 180)}")
    print(f"\nDone. Open the images in: {output_dir.resolve()}")


if __name__ == "__main__":
    main()

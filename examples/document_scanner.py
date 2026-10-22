"""Generate a synthetic photographed page and scan it with VisionForge."""

from pathlib import Path

import cv2
import numpy as np

from visionforge.scan import scan_document


def main() -> None:
    output_dir = Path("outputs/document-scanner")
    output_dir.mkdir(parents=True, exist_ok=True)

    photo = np.full((600, 480, 3), 45, dtype=np.uint8)
    page = np.array([[65, 50], [415, 100], [375, 555], [95, 500]], dtype=np.int32)
    cv2.fillConvexPoly(photo, page, (245, 244, 235))
    cv2.putText(photo, "VISIONFORGE", (125, 180), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (35, 35, 35), 2)
    cv2.putText(photo, "Document scanner demo", (115, 235), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (35, 35, 35), 1)
    cv2.line(photo, (112, 275), (365, 310), (90, 90, 90), 2)
    cv2.line(photo, (108, 315), (345, 348), (90, 90, 90), 2)

    input_path = output_dir / "page-photo.png"
    if not cv2.imwrite(str(input_path), photo):
        raise OSError(f"Could not save demo input image: {input_path}")
    report = scan_document(input_path, output_dir / "page-scanned.png")
    print(f"Scanned page: {report['output']} ({report['width']} x {report['height']})")


if __name__ == "__main__":
    main()

import argparse
import sys
import cv2
from pathlib import Path
from uniface.core.service import FaceService
from uniface.core.config import DEFAULT_BACKEND, DEFAULT_MODE

def run_cli():
    parser = argparse.ArgumentParser(
        prog="uni-face cli",
        description="Uni-Face — speed-first face swap CLI",
    )
    parser.add_argument("--source", type=str, required=True, help="Source face image path")
    parser.add_argument("--target", type=str, required=True, help="Target image path")
    parser.add_argument("--output", type=str, required=True, help="Output image path")
    parser.add_argument(
        "--backend",
        type=str,
        default=DEFAULT_BACKEND,
        help=f"Swap backend model (default: {DEFAULT_BACKEND})",
    )

    # main.py consumed argv[1] ('cli'), so parse the rest
    args = parser.parse_args(sys.argv[2:])

    source_img = cv2.imread(args.source)
    if source_img is None:
        print(f"[ERROR] Cannot read source image: {args.source}")
        sys.exit(1)

    target_img = cv2.imread(args.target)
    if target_img is None:
        print(f"[ERROR] Cannot read target image: {args.target}")
        sys.exit(1)

    service = FaceService()
    try:
        result_img = service.process_image(source_img, target_img)
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(str(out_path), result_img)
        print(f"[OK] Saved -> {out_path}")
    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)

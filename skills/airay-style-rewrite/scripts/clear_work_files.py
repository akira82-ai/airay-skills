#!/usr/bin/env python3
import sys
from pathlib import Path


STAGE_FILES = [
    "01-source.md",
    "02-source-lock.md",
    "03-ip-voice.md",
    "04-humanized.md",
    "05-calibrated.md",
    "06-final.md",
]


def main():
    if len(sys.argv) != 2:
        print("Usage: clear_work_files.py <work-dir>", file=sys.stderr)
        return 2

    work_dir = Path(sys.argv[1])
    if not work_dir.exists() or not work_dir.is_dir():
        print(f"ERROR: work dir not found: {work_dir}", file=sys.stderr)
        return 2

    cleared = 0
    for name in STAGE_FILES:
        path = work_dir / name
        if path.exists() and path.is_file():
            path.write_text("", encoding="utf-8")
            cleared += 1

    print(f"PASSED: cleared {cleared} stage files in {work_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

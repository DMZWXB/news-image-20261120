#!/usr/bin/env python3
"""Entry program for make.fun news-image-20261120 (v2).

Writes the pre-rendered infographic to /output/entry.png.

The image is bundled in this repository as entry.png (1024x1024 PNG,
169,283 bytes) and is copied byte-for-byte, so two runs always produce
identical output. No network access, no third-party dependencies: the
standard library only.
"""
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"
OUTPUT = Path("/output/entry.png")


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, OUTPUT)
    print(f"wrote {OUTPUT} ({OUTPUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()

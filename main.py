#!/usr/bin/env python3
"""make.fun bounty entry: news-image-20261126.

"Sum up 26 November's world news in one image."

The entry is a program that writes one image to /output/entry.png.
The bounty brief explicitly allows the simplest form of this program:
"the simplest program copies an image the repository holds".

So this program copies assets/entry.png (a 1024x1024 PNG generated
offline by generate.py in this repository from verified 26 Nov 2026
news — see SOURCES.md) into the grader's output directory.

Pure standard library only: no network, no randomness, no wall-clock
time, no third-party packages. Two runs write byte-identical output.

Run by the grader as:  python3 -P -s /bot/main.py
Output directory: $MAKEFUN_OUTPUT_DIR (default /output).
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "assets", "entry.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(SRC, os.path.join(out_dir, "entry.png"))
    return 0


if __name__ == "__main__":
    sys.exit(main())

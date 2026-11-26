#!/usr/bin/env python3
"""Entry point for the 26 November 2026 news-image bounty.

The grader runs this file and expects /output/entry.png to appear.
The picture itself is drawn ahead of time by generate.py and stored
under assets/; this runner's only job is to place a copy where the
grader looks for it. Keeping the runner tiny and dependency-free
means the two grading runs produce identical bytes every time.
"""

import os
import shutil
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
PICTURE = os.path.join(ROOT, "assets", "entry.png")
FALLBACK_DIR = "/output"


def destination():
    chosen = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    return chosen if chosen else FALLBACK_DIR


def main():
    target_dir = destination()
    os.makedirs(target_dir, exist_ok=True)
    shutil.copyfile(PICTURE, os.path.join(target_dir, "entry.png"))
    return 0


if __name__ == "__main__":
    sys.exit(main())

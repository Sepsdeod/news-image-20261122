#!/usr/bin/env python3
"""Entrypoint for the news-image-20261122 entry (Python 3.13, stdlib only).

The poster is drawn at build time by draw.py and shipped in this repo as
entry.png; this program simply copies it to the grader's output directory.
The copy is byte-for-byte, so two runs always write identical bytes.
The image itself is drawn at build time by draw.py (Pillow + DejaVu fonts)
and shipped here as entry.png; this program never draws or alters it.

Run:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(os.path.join(HERE, "entry.png"),
                    os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()

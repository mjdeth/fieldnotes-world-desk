#!/usr/bin/env python3
"""Fieldnotes - World Desk: sandbox entrypoint (Python standard library only).

Mirrors the kit starter (main.ts): the entry is the committed entry.png
beside this file, and the program copies it to entry.png inside the
output directory. Outside the grader's container, MAKEFUN_OUTPUT_DIR
stands in for /output.
"""

import os
import shutil
from pathlib import Path


def main():
    src = Path(__file__).resolve().parent / "entry.png"
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, out_dir / "entry.png")


if __name__ == "__main__":
    main()

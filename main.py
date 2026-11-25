#!/usr/bin/env python3
"""Entry point for news-image-20261125.

Writes the pre-built front page (entry.png, in this repository) to
/output/entry.png. Pure standard library, no network, no randomness:
two runs write byte-identical output by construction.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    src = os.path.join(HERE, "entry.png")
    if not os.path.isfile(src):
        raise SystemExit("entry.png missing from repository root")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    if os.path.getsize(dst) != os.path.getsize(src):
        raise SystemExit("entry.png copy is incomplete")


if __name__ == "__main__":
    main()

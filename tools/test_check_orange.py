#!/usr/bin/env python3
"""Self-test for skills/company360-output-evaluation/scripts/check_orange.py.

Builds two one-page PDFs (with and without the #FF5B1F title rule) and expects PASS then BLOCK.
Needs the pinned packages in that skill's scripts/requirements.txt.
"""
import subprocess
import sys
import tempfile
from pathlib import Path

import pymupdf

SCRIPT = Path(__file__).resolve().parent.parent / "skills/company360-output-evaluation/scripts/check_orange.py"


def make(path, rule):
    doc = pymupdf.open()
    page = doc.new_page()
    page.insert_text((72, 90), "Company 360 test deliverable", fontsize=20)
    if rule:
        page.draw_line((72, 100), (540, 100), color=(1, 91 / 255, 31 / 255), width=1)
    doc.save(path)


with tempfile.TemporaryDirectory() as t:
    good, bad = Path(t) / "with_rule.pdf", Path(t) / "no_rule.pdf"
    make(good, True)
    make(bad, False)
    ok = subprocess.run([sys.executable, "-W", "ignore", str(SCRIPT), str(good)], capture_output=True, text=True)
    block = subprocess.run([sys.executable, "-W", "ignore", str(SCRIPT), str(bad)], capture_output=True, text=True)
    # PyMuPDF prints a fitz deprecation notice on stdout; the verdict is the last line.
    ok_line, block_line = ok.stdout.strip().splitlines()[-1], block.stdout.strip().splitlines()[-1]
    print(ok_line)
    print(block_line)
    if ok.returncode != 0 or not ok_line.startswith("PASS") or block.returncode != 1 or not block_line.startswith("BLOCK"):
        sys.exit("check_orange.py self-test FAILED")
    print("check_orange.py self-test passed")

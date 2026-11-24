#!/usr/bin/env python3
"""Zip each skill folder for upload to an app that takes Agent Skills (SKILL.md) as a zip.

Usage:
    python3 -I tools/package_skills.py [repo_dir] [--out DIR]

Writes DIR/<skill>.zip (default dist/, which git ignores), one per folder under skills/, each with a
single top-level folder named after the skill. Zips are built locally and never committed, so the
repository keeps one copy of each skill. Entries are sorted and dated 1980-01-01, so the same skill
always gives the same zip. Standard library only.
"""
import argparse
import sys
import zipfile
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("repo", nargs="?", default=".")
    ap.add_argument("--out", type=Path)
    a = ap.parse_args()
    repo = Path(a.repo)
    out = a.out or repo / "dist"
    out.mkdir(parents=True, exist_ok=True)
    n = 0
    for d in sorted(p for p in (repo / "skills").iterdir() if (p / "SKILL.md").is_file()):
        target = out / f"{d.name}.zip"
        with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as z:
            for f in sorted(p for p in d.rglob("*") if p.is_file()
                            and "__pycache__" not in p.parts and p.suffix != ".pyc"):
                info = zipfile.ZipInfo(f"{d.name}/{f.relative_to(d).as_posix()}", (1980, 1, 1, 0, 0, 0))
                info.external_attr = 0o644 << 16
                info.compress_type = zipfile.ZIP_DEFLATED
                z.writestr(info, f.read_bytes())
        n += 1
    print(f"wrote {n} skill zips to {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

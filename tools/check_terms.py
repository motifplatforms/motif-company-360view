#!/usr/bin/env python3
"""Fail when brand, product, catalog or source-workbook specifics appear in the repository.

Usage:
    python3 -I tools/check_terms.py [repo_dir]

The blocked terms are stored only as SHA-256 hashes of their normalized words (tools/blocked-terms.json),
so the list itself does not publish them. Two patterns catch identifiers that no list can know in advance:
retail barcodes (12 to 14 digit numbers) and product codes (one to three capitals followed by five or
more digits). Output names the file and line only, never the matched words.

Exit 0 when clean, 1 when anything matched. The converter imports scan() to check every new version.
"""
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
PATTERNS = [
    ("barcode-like number", re.compile(r"(?<![\w.-])\d{12,14}(?![\w-])")),
    ("product-code-like token", re.compile(r"(?<![\w-])[A-Z]{1,3}\d{5,}(?![\w-])")),
]
SKIP_DIRS = {".git", "__pycache__", ".venv", "venv"}


def _load():
    data = json.loads((HERE / "blocked-terms.json").read_text())
    return data["max_words"], set(data["ngram_sha256"])


MAX_WORDS, BLOCKED = _load()


def words(text):
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode().lower()
    return re.findall(r"[a-z0-9]+", text)


def scan(text):
    """Return a list of (line_number, kind) for every blocked match in text."""
    hits = []
    for i, line in enumerate(text.splitlines(), 1):
        w = words(line)
        found = False
        for n in range(1, MAX_WORDS + 1):
            for j in range(len(w) - n + 1):
                if hashlib.sha256(" ".join(w[j:j + n]).encode()).hexdigest() in BLOCKED:
                    hits.append((i, "blocked term"))
                    found = True
                    break
            if found:
                break
        for kind, rx in PATTERNS:
            if rx.search(line):
                hits.append((i, kind))
    return hits


def main(root):
    root = Path(root)
    bad = 0
    for p in sorted(root.rglob("*")):
        if not p.is_file() or SKIP_DIRS & set(p.relative_to(root).parts):
            continue
        try:
            text = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        rel = p.relative_to(root).as_posix()
        if rel in ("tools/blocked-terms.json",):
            continue
        if rel == "tools/genericize.json":
            text = "\n".join(json.loads(text)["lines"].values())
        for line, kind in scan(text):
            print(f"{rel}:{line}: {kind}")
            bad += 1
    print("clean" if not bad else f"{bad} match(es)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "."))

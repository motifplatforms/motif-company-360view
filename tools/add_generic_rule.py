#!/usr/bin/env python3
"""Add a generic rewrite for one source line to tools/genericize.json.

Usage:
    python3 -I tools/add_generic_rule.py <line_sha256> "<generic line>"

Take line_sha256 from the converter's --rewrite-report. Write the generic line so it keeps the example's
teaching point (the rule it demonstrates and why) while naming no brand, company, product, product code,
barcode, catalog page or revision, price, source workbook or tab. Use neutral stand-ins such as
"the parent", "two sibling brands", "a retail UPC", "a distributor catalog", "the channel workbook".
A line that is already generic may be added unchanged. The rule is refused if the text trips
tools/check_terms.py.
"""
import json
import re
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
from check_terms import scan  # noqa: E402


def main(line_sha, text):
    if not re.fullmatch(r"[0-9a-f]{64}", line_sha):
        sys.exit("STOP: line_sha256 must be 64 lowercase hex characters")
    if "\n" in text or not text.strip():
        sys.exit("STOP: the generic text must be one non-empty line")
    if scan(text):
        sys.exit("STOP: the generic text still contains a blocked term or identifier")
    path = TOOLS / "genericize.json"
    data = json.loads(path.read_text())
    old = data["lines"].get(line_sha)
    data["lines"][line_sha] = text
    data["lines"] = dict(sorted(data["lines"].items()))
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print("replaced existing rule" if old is not None else "added rule")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])

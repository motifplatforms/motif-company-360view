#!/usr/bin/env python3
"""Check that the repository matches the source version it says it holds.

Usage:
    python3 -I tools/check_repo.py [repo_dir]

Checks, all with the standard library:
- conversion-manifest.json: its bundle is the latest entry in versions.json.
- skills/: exactly the folders the manifest lists; each SKILL.md and each carried file hashes to the
  recorded value (catches hand edits); names and descriptions are valid.
- Every script ships a requirements.txt with exact (==) pins.
- .claude-plugin/plugin.json version matches the latest versions.json entry.
- chatgpt/: exactly what tools/build_chatgpt.py builds from skills/ (no hand edits, nothing stale),
  each instruction file within the custom GPT limit, and no note that only applies to Claude.
- No blocked brand, product, catalog or workbook term anywhere (tools/check_terms.py).

The source bundles are not stored here. The daily reconcile re-runs the converter on the source and
compares the result with the recorded hashes, which also covers the method text.

Exit 0 when clean, 1 when anything drifted. Prints one line per problem.
"""
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

TOOLS = Path(__file__).resolve().parent

NAME_RE = re.compile(r"^[a-z0-9-]{1,64}$")


def sha(b):
    return hashlib.sha256(b).hexdigest()


def frontmatter(text):
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---\n", 4)
    if end < 0:
        return None, text
    fm = {}
    for line in text[4:end].splitlines():
        if line.startswith(" ") or ":" not in line:
            continue
        k, _, v = line.partition(":")
        v = v.strip()
        if v.startswith('"'):
            v = json.loads(v)
        fm[k.strip()] = v
    return fm, text[end + 5:]


def main(repo):
    repo = Path(repo)
    problems = []
    versions = json.loads((repo / "versions.json").read_text())
    if not versions:
        print("versions.json is empty")
        return 1
    latest = versions[-1]
    cm = json.loads((repo / "conversion-manifest.json").read_text())
    if cm["bundle_sha256"] != latest["bundle_sha256"]:
        problems.append("conversion-manifest.json is not from the latest bundle in versions.json")

    plugin = json.loads((repo / ".claude-plugin" / "plugin.json").read_text())
    if plugin.get("version") != latest["plugin_version"]:
        problems.append(f"plugin.json version {plugin.get('version')} != {latest['plugin_version']}")

    listed = {r["claude_skill"]: r for r in cm["skills"]}
    present = {p.name for p in (repo / "skills").iterdir() if p.is_dir()}
    for extra in sorted(present - set(listed)):
        problems.append(f"skills/{extra} is not in conversion-manifest.json")
    for missing in sorted(set(listed) - present):
        problems.append(f"skills/{missing} is listed but missing")

    for name, r in sorted(listed.items()):
        d = repo / "skills" / name
        f = d / "SKILL.md"
        if not f.is_file():
            continue
        raw = f.read_bytes()
        if sha(raw) != r["converted_sha256"]:
            problems.append(f"{name}: SKILL.md changed since conversion (hand edit?)")
        fm, body = frontmatter(raw.decode("utf-8"))
        if not fm:
            problems.append(f"{name}: no frontmatter")
            continue
        if fm.get("name") != name or not NAME_RE.match(name):
            problems.append(f"{name}: frontmatter name {fm.get('name')!r} invalid")
        desc = fm.get("description", "")
        if not desc or len(desc) > 1024 or "<" in desc or ">" in desc:
            problems.append(f"{name}: description missing, too long or has angle brackets")
        for rel, want in r.get("files_sha256", {}).items():
            fp = d / rel
            if not fp.is_file():
                problems.append(f"{name}: {rel} is missing")
            elif sha(fp.read_bytes()) != want:
                problems.append(f"{name}: {rel} changed since conversion (hand edit?)")
        known = {"SKILL.md", *r.get("files_sha256", {})}
        for fp in d.rglob("*"):
            if fp.is_file() and fp.relative_to(d).as_posix() not in known:
                problems.append(f"{name}: {fp.relative_to(d).as_posix()} is not in conversion-manifest.json")
        for script in d.rglob("*.py"):
            req = script.parent / "requirements.txt"
            if not req.is_file():
                problems.append(f"{name}: {script.relative_to(d)} has no requirements.txt")
                continue
            for line in req.read_text().split("\n"):
                if line.strip() and "==" not in line:
                    problems.append(f"{name}: unpinned requirement {line.strip()!r}")

    with tempfile.TemporaryDirectory() as tmp:
        built = subprocess.run([sys.executable, "-I", str(TOOLS / "build_chatgpt.py"), str(repo), "--out", tmp],
                               capture_output=True, text=True)
        if built.returncode != 0:
            problems += ["chatgpt build: " + ln for ln in built.stdout.splitlines() if ln.startswith("PROBLEM")]
        want_dir, have_dir = Path(tmp) / "chatgpt", repo / "chatgpt"
        want = {p.relative_to(want_dir).as_posix(): p.read_bytes() for p in want_dir.rglob("*") if p.is_file()}
        have = ({p.relative_to(have_dir).as_posix(): p.read_bytes() for p in have_dir.rglob("*") if p.is_file()}
                if have_dir.is_dir() else {})
        for rel in sorted(set(want) - set(have)):
            problems.append(f"chatgpt/{rel} is missing (run tools/build_chatgpt.py)")
        for rel in sorted(set(have) - set(want)):
            problems.append(f"chatgpt/{rel} is not built from skills/")
        for rel in sorted(set(want) & set(have)):
            if want[rel] != have[rel]:
                problems.append(f"chatgpt/{rel} differs from a fresh build (hand edit or stale?)")
        for rel, data in sorted(have.items()):
            if "Claude" in data.decode("utf-8", "replace"):
                problems.append(f"chatgpt/{rel} mentions Claude")

    terms = subprocess.run([sys.executable, "-I", str(TOOLS / "check_terms.py"), str(repo)],
                           capture_output=True, text=True)
    if terms.returncode != 0:
        problems += ["blocked term: " + ln for ln in terms.stdout.splitlines()[:-1]]

    for p in problems:
        print("DRIFT", p)
    print(f"checked {len(listed)} skills and their ChatGPT versions against version {latest['plugin_version']}: {'clean' if not problems else str(len(problems)) + ' problem(s)'}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "."))

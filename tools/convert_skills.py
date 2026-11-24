#!/usr/bin/env python3
"""Convert the Company 360 ChatGPT skill bundle (Company-360-Skills.zip) into Claude skills.

Usage:
    python3 -I tools/convert_skills.py <bundle.zip> <out_dir> [--rewrite-report FILE]

What it does
- Opens the zip without executing anything in it and rejects unsafe paths.
- Checks every SKILL.md against the bundle's manifest.json (SHA-256). Any mismatch stops the run.
- Writes one Claude skill folder per source skill under <out_dir>/skills/, with a stable name
  (motif-<topic>-YYYY-MM-DD becomes company360-<topic>) so a new version replaces the old
  folder instead of adding a second skill with the same job.
- Makes the text generic for a public repository (tools/genericize.json):
  * the workbook line and every acceptance-example line must have a rewrite rule, keyed by the
    SHA-256 of the original line, so the original wording never enters the repository;
  * listed words are replaced wherever they appear (word rules, also keyed by hash);
  * every other line of the method text is kept word for word.
  Then the whole output is scanned with tools/check_terms.py. A line without a rule, or any match,
  stops the run with exit code 7 and nothing written; the lines that need a generic rewrite go to
  --rewrite-report (keep that file outside the repository: it holds the original wording).
  Add a rewrite with tools/add_generic_rule.py and run again.
- Adds frontmatter metadata (source name, version, hashes) and a short "Claude notes" section.
  Drops agents/openai.yaml (ChatGPT-only); its display name and short description are folded in.
- Copies scripts/ as-is and adds a pinned requirements.txt for known dependencies.
- Writes <out_dir>/conversion-manifest.json listing source and converted hashes.

Standard library only. Runs the same way on every new version.
"""
import hashlib
import json
import re
import shutil
import sys
import zipfile
from pathlib import Path, PurePosixPath

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
from check_terms import scan  # noqa: E402  (tools/ is part of this repository)

RULES = json.loads((TOOLS / "genericize.json").read_text())
TAIL = " For a new company, confirm equivalent workbook and tab names with the planner."
EXIT_REWRITE = 7

SRC_RE = re.compile(r"^motif-(?P<topic>[a-z0-9-]+?)-(?P<ver>\d{4}-\d{2}-\d{2})$")
NAME_RE = re.compile(r"^[a-z0-9-]{1,64}$")

# Pinned and tested on 2026-11-23 (check_orange.py: PASS on a PDF with the orange rule, BLOCK without).
PINNED = {
    "check_orange.py": ["PyMuPDF==1.28.2", "Pillow==13.0.0", "numpy==2.5.5"],
}

# Sibling links, taken from what each skill's own method text or the source TECH spec says it depends on.
RELATED = {
    "entity-portfolio": [("decision-synthesis", "uses the parent exhibit"), ("operating-capability", "needs the entity-period")],
    "product-pack-identity": [("retail-offers", "uses the SKU crosswalk"), ("unit-economics", "needs pack identity"), ("market-sell-through", "qualifies the product universe")],
    "retail-offers": [("product-pack-identity", "the identity crosswalk this skill starts from")],
    "market-sell-through": [("product-pack-identity", "signed-off SKU list"), ("household-buying", "purchase denominators")],
    "household-buying": [("customer-routines", "sends reported routines here for purchase-rate work")],
    "customer-routines": [("household-buying", "where purchase-rate estimates go")],
    "positioning-journey": [("retail-offers", "existing shelf observations to link, not recount")],
    "claims-substantiation": [("logic-challenge", "independent review of claim assertions")],
    "operating-capability": [("entity-portfolio", "entity and period ownership")],
    "unit-economics": [("product-pack-identity", "pack identity"), ("retail-offers", "offer identity and shelf price"), ("customer-routines", "routine inputs")],
    "decision-synthesis": [("logic-challenge", "reviewed evidence cut"), ("output-evaluation", "required before release")],
    "work-planning": [("logic-challenge", "challenge stage"), ("decision-synthesis", "synthesis stage"), ("output-evaluation", "final stage")],
    "logic-challenge": [("output-evaluation", "next stage after challenge")],
    "output-evaluation": [("logic-challenge", "challenge log this skill reads")],
    "weekly-tools-review": [("work-planning", "where adopted changes take effect")],
}

EXTRA_NOTES = {
    "output-evaluation": [
        "Motif output-QA and grader standards map to the Claude skills motif-output-qa and motif-grader where they are installed.",
        "Orange title check: `pip install -r scripts/requirements.txt`, then `python scripts/check_orange.py <rendered.pdf>`. Exit code 1 blocks release. The script is unchanged; PyMuPDF prints a deprecation warning for `import fitz`, which does not affect the result.",
    ],
    "weekly-tools-review": [
        "The dated installed-skill inventory for this set is conversion-manifest.json and versions.json at the repository root.",
    ],
}


def die(msg):
    sys.exit(f"STOP: {msg}")


def parse_frontmatter(text):
    if not text.startswith("---\n"):
        die("SKILL.md has no frontmatter")
    end = text.index("\n---\n", 4)
    fm, body = text[4:end], text[end + 5:]
    out = {}
    for line in fm.splitlines():
        k, _, v = line.partition(":")
        v = v.strip()
        if v.startswith('"'):
            v = json.loads(v)
        out[k.strip()] = v
    return out, body


def parse_openai_yaml(text):
    out = {}
    for line in text.splitlines():
        m = re.match(r'^\s+(display_name|short_description|default_prompt):\s*"(.*)"\s*$', line)
        if m:
            out[m.group(1)] = json.loads('"' + m.group(2) + '"')
    return out


def q(s):
    return json.dumps(s, ensure_ascii=False)


def sha(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def swap_words(text):
    return re.sub(r"[A-Za-z]+", lambda m: RULES["words"].get(sha(m.group(0).lower()), m.group(0)), text)


def genericize(body, src, needs):
    """Return (generic body, workbook destination, lines changed). Appends unmapped lines to needs."""
    out, section, dest, changed = [], None, "", 0
    for ln in body.split("\n"):
        if ln.startswith("## "):
            section = ln[3:].strip()
            new = swap_words(ln)
            changed += new != ln
            out.append(new)
            continue
        required = bool(ln.strip()) and section in ("Deliverable and owning workbook", "Acceptance example")
        new = RULES["lines"].get(sha(ln))
        if new is None:
            if required:
                needs.append({"source_skill": src, "section": section, "line_sha256": sha(ln), "text": ln})
            new = swap_words(ln)
        if section == "Deliverable and owning workbook" and ln.strip() and not dest:
            dest = new.split(TAIL.strip())[0].strip().rstrip(".")
        changed += new != ln
        out.append(new)
    return "\n".join(out), dest, changed


def main(zip_path, out_dir, rewrite_report=None):
    zip_path, out_dir = Path(zip_path), Path(out_dir)
    bundle_sha = hashlib.sha256(zip_path.read_bytes()).hexdigest()
    z = zipfile.ZipFile(zip_path)
    files = {}
    for info in z.infolist():
        p = PurePosixPath(info.filename)
        if p.is_absolute() or ".." in p.parts:
            die(f"unsafe path in zip: {info.filename}")
        if not info.is_dir():
            files[str(p)] = z.read(info)
    manifest = json.loads(files["manifest.json"])
    names = {e["name"] for e in manifest}
    for e in manifest:
        got = hashlib.sha256(files[f"{e['name']}/SKILL.md"]).hexdigest()
        if got != e["sha256"]:
            die(f"{e['name']} SKILL.md hash {got} does not match manifest {e['sha256']}")
    extra = {f.split("/")[0] for f in files if "/" in f} - names
    if extra:
        die(f"folders not in manifest: {sorted(extra)}")

    records, problems, needs, outputs = [], [], [], []
    topic_of = {}
    for e in manifest:
        m = SRC_RE.match(e["name"])
        if not m:
            die(f"unexpected source name {e['name']}")
        topic_of[e["name"]] = m.group("topic")

    for e in manifest:
        src = e["name"]
        topic, ver = SRC_RE.match(src).group("topic", "ver")
        name = f"company360-{topic}"
        if not NAME_RE.match(name):
            die(f"invalid Claude skill name {name}")
        fm, body = parse_frontmatter(files[f"{src}/SKILL.md"].decode("utf-8"))
        if fm.get("name") != src:
            problems.append(f"{src}: frontmatter name {fm.get('name')!r} differs from folder")
        oy = parse_openai_yaml(files.get(f"{src}/agents/openai.yaml", b"").decode("utf-8"))
        gbody, dest_line, changed = genericize(body, src, needs)
        desc = swap_words(fm["description"].strip())
        if oy.get("short_description"):
            desc = f"{desc} Focus: {swap_words(oy['short_description']).rstrip('.')}."
        if len(desc) > 1024 or "<" in desc or ">" in desc:
            die(f"{name}: description too long or has angle brackets")

        notes = [
            f"Source: `{src}` (SKILL.md sha256 {e['sha256'][:12]}). The method text is the source's, word for word, except that the workbook line, the acceptance example and the project name are written generically ({changed} line(s)).",
            "No search recipes ship with this skill (no queries, engines or stop rules). Record search terms, sources checked and access results as the handoff section asks.",
        ]
        rel = [r for r in RELATED.get(topic, []) if f"motif-{r[0]}-{ver}" in names]
        if rel:
            notes.append("Related skills in this set: " + "; ".join(f"company360-{t} ({why})" for t, why in rel) + ".")
        notes += EXTRA_NOTES.get(topic, [])

        fm_lines = [
            "---",
            f"name: {name}",
            f"description: {q(desc)}",
            "metadata:",
            f"  source-skill: {q(src)}",
            f"  source-version: {q(ver)}",
            f"  source-sha256: {q(e['sha256'])}",
            f"  source-bundle-sha256: {q(bundle_sha)}",
            f"  display-name: {q(swap_words(oy.get('display_name', e.get('title', ''))))}",
            f"  workbook-destination: {q(dest_line)}",
            "---",
        ]
        text = "\n".join(fm_lines) + "\n" + gbody.rstrip("\n") + "\n\n## Claude notes\n\n" + "\n".join(f"- {n}" for n in notes) + "\n"
        if "$motif-" in text:
            problems.append(f"{name}: ChatGPT $skill reference left in text")

        hits = scan(text)
        if hits:
            lines_txt = text.splitlines()
            for ln_no, kind in hits:
                needs.append({"source_skill": src, "section": "(scan: " + kind + ")",
                              "line_sha256": sha(lines_txt[ln_no - 1]), "text": lines_txt[ln_no - 1]})
        extra_files, carried, dropped = {}, [], []
        for f, data in files.items():
            if not f.startswith(src + "/") or f == f"{src}/SKILL.md":
                continue
            rel_path = f[len(src) + 1:]
            if rel_path.startswith("agents/"):
                dropped.append(rel_path)
                continue
            extra_files[rel_path] = data
            carried.append(rel_path)
            pins = PINNED.get(Path(rel_path).name)
            if pins:
                req = str(PurePosixPath(rel_path).parent / "requirements.txt")
                extra_files[req] = ("\n".join(pins) + "\n").encode()
                carried.append(req)
            elif rel_path.endswith(".py"):
                problems.append(f"{name}: script {rel_path} has no pinned dependencies yet")
            for ln_no, kind in scan(data.decode("utf-8", "replace")):
                needs.append({"source_skill": src, "section": f"(scan {rel_path}: {kind})", "line_sha256": "", "text": f"line {ln_no}"})
        outputs.append((name, text, extra_files))

        records.append({
            "claude_skill": name,
            "source_skill": src,
            "source_version": ver,
            "source_sha256": e["sha256"],
            "method_sha256": hashlib.sha256(body.replace(src, "<skill>").rstrip("\n").encode("utf-8")).hexdigest(),
            "converted_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
            "generic_lines": changed,
            "files_carried": sorted(carried),
            "files_sha256": {k: hashlib.sha256(v).hexdigest() for k, v in sorted(extra_files.items())},
            "files_dropped": sorted(dropped),
        })

    if needs:
        if rewrite_report:
            Path(rewrite_report).write_text(json.dumps(needs, indent=2, ensure_ascii=False) + "\n")
        print(f"NEEDS GENERIC REWRITE: {len(needs)} line(s); nothing written."
              + (f" Details in {rewrite_report}." if rewrite_report else " Pass --rewrite-report FILE for details."))
        sys.exit(EXIT_REWRITE)

    skills_dir = out_dir / "skills"
    skills_dir.mkdir(parents=True, exist_ok=True)
    for name, text, extra_files in outputs:
        dest = skills_dir / name
        if dest.exists():
            shutil.rmtree(dest)
        dest.mkdir(parents=True)
        (dest / "SKILL.md").write_text(text, encoding="utf-8")
        for rel_path, data in extra_files.items():
            out = dest / rel_path
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(data)

    report = {
        "bundle": zip_path.name,
        "bundle_sha256": bundle_sha,
        "skills": records,
        "problems": problems,
    }
    (out_dir / "conversion-manifest.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    print(f"converted {len(records)} skills; problems: {len(problems)}")
    for p in problems:
        print(" -", p)


if __name__ == "__main__":
    args = sys.argv[1:]
    report = None
    if "--rewrite-report" in args:
        i = args.index("--rewrite-report")
        report = args[i + 1]
        del args[i:i + 2]
    if len(args) != 2:
        sys.exit(__doc__)
    main(args[0], args[1], report)

#!/usr/bin/env python3
"""Build the ChatGPT versions of the skills from skills/.

Usage:
    python3 -I tools/build_chatgpt.py [repo_dir] [--out DIR]

Writes, from skills/*/SKILL.md and versions.json only:
    chatgpt/instructions/<skill>.md     one skill as paste-ready instructions for a custom GPT or a
                                        ChatGPT Project (each under MAX_CHARS characters)
    chatgpt/company360-all-skills.md    all skills in one file, to attach as knowledge
    chatgpt/project-instructions.md     short instructions that route each request to one skill in
                                        the all-skills file

The method text is carried word for word. Only the notes change: the source line and any note that
only applies to Claude are dropped, and a note says where the skill's own files live in this
repository. The output is deterministic, so tools/check_repo.py can rebuild it and compare.

By default writes into <repo_dir>/chatgpt (replacing it). With --out, writes the chatgpt folder
into DIR instead (used by check_repo.py). Standard library only.
"""
import argparse
import json
import shutil
import sys
from pathlib import Path

MAX_CHARS = 7500  # a custom GPT's Instructions box takes 8,000 characters
REPO_URL = "https://github.com/motifplatforms/motif-company-360view"


def frontmatter(text):
    if not text.startswith("---\n"):
        raise ValueError("no frontmatter")
    end = text.find("\n---\n", 4)
    fm = {}
    for line in text[4:end].splitlines():
        if ":" not in line:
            continue
        k, _, v = line.strip().partition(":")
        v = v.strip()
        if v.startswith('"'):
            v = json.loads(v)
        fm[k.strip()] = v
    return fm, text[end + 5:]


def split_notes(body):
    marker = "\n## Claude notes\n"
    if marker not in body:
        return body.rstrip("\n"), []
    main, _, notes = body.partition(marker)
    bullets = [ln[2:].strip() for ln in notes.splitlines() if ln.startswith("- ")]
    return main.rstrip("\n"), bullets


def skill_text(skill_dir):
    name = skill_dir.name
    fm, body = frontmatter((skill_dir / "SKILL.md").read_text(encoding="utf-8"))
    body = body.lstrip("\n")
    title_line, _, rest = body.partition("\n")
    if not title_line.startswith("# "):
        raise ValueError(f"{name}: body does not start with a title")
    main, notes = split_notes(rest)
    keep = [n for n in notes if not n.startswith("Source:") and "Claude" not in n
            and "scripts/" not in n]
    files = sorted(p.relative_to(skill_dir).as_posix() for p in skill_dir.rglob("*")
                   if p.is_file() and p.name != "SKILL.md")
    if files:
        keep.append("This skill's files are in the repository under `skills/" + name + "/`: "
                    + ", ".join(f"`{f}`" for f in files)
                    + ". Run scripts on your own machine; install the pinned requirements first.")
    out = [f"{title_line} ({name})", "", "Use this when: " + fm["description"], "", main.strip("\n")]
    if keep:
        out += ["", "## Notes", ""] + [f"- {n}" for n in keep]
    return name, fm, "\n".join(out) + "\n"


def build(repo, dest):
    repo = Path(repo)
    latest = json.loads((repo / "versions.json").read_text())[-1]["plugin_version"]
    skills = sorted(p for p in (repo / "skills").iterdir() if (p / "SKILL.md").is_file())
    if dest.exists():
        shutil.rmtree(dest)
    (dest / "instructions").mkdir(parents=True)
    problems, parts, rows = [], [], []
    for d in skills:
        name, fm, text = skill_text(d)
        if len(text) > MAX_CHARS:
            problems.append(f"{name}: {len(text)} characters, over the {MAX_CHARS} limit")
        (dest / "instructions" / f"{name}.md").write_text(text, encoding="utf-8")
        parts.append(text)
        rows.append(f"- {name}: {fm['description'].split('. ')[0].rstrip('.')}.")

    header = ["# Company 360 skills", "",
              f"Version {latest}. {len(skills)} skills for conducting 360 research on companies, "
              f"from {REPO_URL}.",
              "Each skill below starts with its own title and a \"Use this when\" line.", ""]
    (dest / "company360-all-skills.md").write_text(
        "\n".join(header) + "\n---\n\n" + "\n---\n\n".join(parts), encoding="utf-8")

    router = [
        "You help with 360 research on companies using the Company 360 skills in the attached file "
        "company360-all-skills.md.",
        "",
        "For each request, pick the one skill below whose job fits, read that skill in full in the file, "
        "and follow its method, acceptance example and evidence and handoff rules. Say which skill you "
        "used. When a request needs more than one skill, do them one at a time, in the order the skills' "
        "related-skill notes give. When no skill fits, say so and do not borrow a method from another.",
        "",
        "Keep facts, inferences, assumptions and unavailable values apart, cite the exact source for "
        "each, and use null rather than a guess.",
        "",
        "Skills:",
        "",
        *rows,
    ]
    router_text = "\n".join(router) + "\n"
    if len(router_text) > MAX_CHARS:
        problems.append(f"project-instructions.md: {len(router_text)} characters, over the {MAX_CHARS} limit")
    (dest / "project-instructions.md").write_text(router_text, encoding="utf-8")
    return problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("repo", nargs="?", default=".")
    ap.add_argument("--out", type=Path)
    a = ap.parse_args()
    dest = (a.out if a.out else Path(a.repo)) / "chatgpt"
    problems = build(a.repo, dest)
    for p in problems:
        print("PROBLEM", p)
    print(f"built {dest}: {'clean' if not problems else str(len(problems)) + ' problem(s)'}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())

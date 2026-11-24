#!/usr/bin/env python3
"""Daily reconcile: compare a source skill bundle with this repository and stage the update.

Usage:
    python3 -I tools/reconcile.py <Company-360-Skills.zip> [--repo DIR] [--apply] [--report FILE]
                                  [--rewrite-report FILE]

The bundle itself is never copied into the repository; versions.json keeps its hash.

Without --apply nothing in the repository changes (dry run). With --apply the update is built in a
temporary copy, checked with tools/check_repo.py, and only then written back.

Exit codes (the daily job reads these):
    0   no change: bundle sha256 equals the latest entry in versions.json, and converting it again
        gives exactly the skills in the repository
    10  change found (dry run, nothing written)
    11  change applied to the working tree (commit or open a PR next)
    2   bundle rejected: hash mismatch with the bundle's own manifest, unsafe zip, or a name that breaks the rules
    3   repository drift: skills/ no longer matches conversion-manifest.json or the source; nothing written
    5   bundle equals an older version (source rolled back?); nothing written, needs a person
    6   the staged update failed the repository check; nothing written
    7   new or changed lines need a generic rewrite first (see tools/add_generic_rule.py); the lines go to
        --rewrite-report, which must stay outside the repository; nothing else written

Standard library only.
"""
import argparse
import datetime
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

TOOLS = Path(__file__).resolve().parent


def sha(b):
    return hashlib.sha256(b).hexdigest()


def run(script, *args):
    return subprocess.run([sys.executable, "-I", str(TOOLS / script), *map(str, args)],
                          capture_output=True, text=True)


def plugin_version(ver, bsha, latest):
    y, m, d = (int(x) for x in ver.split("-"))
    base = f"{y}.{m}.{d}"
    if latest and latest["plugin_version"].split("+")[0] == base:
        return f"{base}+{bsha[:8]}"
    return base


def diff(old, new):
    o = {r["claude_skill"]: r for r in old["skills"]}
    n = {r["claude_skill"]: r for r in new["skills"]}
    out = {"added": sorted(set(n) - set(o)), "removed": sorted(set(o) - set(n)),
           "changed": [], "version_only": [], "unchanged": []}
    for k in sorted(set(o) & set(n)):
        if o[k].get("method_sha256") != n[k].get("method_sha256") or o[k]["files_carried"] != n[k]["files_carried"]:
            out["changed"].append(k)
        elif o[k]["source_sha256"] != n[k]["source_sha256"]:
            out["version_only"].append(k)
        else:
            out["unchanged"].append(k)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("bundle", type=Path)
    ap.add_argument("--repo", type=Path, default=Path("."))
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--report", type=Path)
    ap.add_argument("--rewrite-report", type=Path)
    a = ap.parse_args()
    repo = a.repo.resolve()
    data = a.bundle.read_bytes()
    bsha = sha(data)
    versions = json.loads((repo / "versions.json").read_text())
    latest = versions[-1] if versions else None
    report = {"bundle": a.bundle.name, "bundle_sha256": bsha,
              "repo_version": latest["plugin_version"] if latest else None,
              "checked_at_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}

    def finish(status, code, **kw):
        report.update(status=status, exit_code=code, **kw)
        text = json.dumps(report, indent=2, ensure_ascii=False)
        print(text)
        if a.report:
            a.report.write_text(text + "\n")
        sys.exit(code)

    same = bool(latest and bsha == latest["bundle_sha256"])
    older = [v for v in versions[:-1] if v["bundle_sha256"] == bsha]
    if older and not same:
        finish("older_version", 5, matches=older[-1]["plugin_version"])

    chk = run("check_repo.py", repo)
    if chk.returncode != 0:
        finish("repo_drift", 3, detail=chk.stdout.strip().splitlines())

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        (tmp / "in").mkdir()
        zcopy = tmp / "in" / "bundle.zip"
        zcopy.write_bytes(data)
        conv_args = [zcopy, tmp / "out"]
        if a.rewrite_report:
            conv_args += ["--rewrite-report", a.rewrite_report.resolve()]
        conv = run("convert_skills.py", *conv_args)
        if conv.returncode == 7:
            finish("needs_generic_rewrite", 7, detail=conv.stdout.strip().splitlines()[-1:])
        if conv.returncode != 0:
            finish("source_rejected", 2, detail=(conv.stdout + conv.stderr).strip().splitlines()[-5:])
        new_cm = json.loads((tmp / "out" / "conversion-manifest.json").read_text())
        old_cm = json.loads((repo / "conversion-manifest.json").read_text())
        if same:
            mism = sorted({r["claude_skill"] for r in new_cm["skills"]} ^ {r["claude_skill"] for r in old_cm["skills"]}
                          | {n["claude_skill"] for n in new_cm["skills"] for o in old_cm["skills"]
                             if n["claude_skill"] == o["claude_skill"]
                             and (n["converted_sha256"], n.get("files_sha256")) != (o["converted_sha256"], o.get("files_sha256"))})
            if mism:
                finish("repo_drift", 3, detail=["skills differ from a fresh conversion of the same bundle: " + ", ".join(mism)])
            finish("no_change", 0)
        d = diff(old_cm, new_cm)
        ver = max(r["source_version"] for r in new_cm["skills"])
        pv = plugin_version(ver, bsha, latest)
        report.update(new_version=pv, changes=d,
                      converter_flags=new_cm.get("problems", []))
        if not a.apply:
            finish("change_found", 10)

        stage = tmp / "stage"
        shutil.copytree(repo, stage, ignore=shutil.ignore_patterns(".git"))
        shutil.rmtree(stage / "skills")
        shutil.copytree(tmp / "out" / "skills", stage / "skills")
        shutil.copy2(tmp / "out" / "conversion-manifest.json", stage / "conversion-manifest.json")
        versions.append({"plugin_version": pv, "source_version": ver,
                         "bundle_sha256": bsha, "recorded_utc": report["checked_at_utc"],
                         "added": d["added"], "removed": d["removed"], "changed": d["changed"],
                         "version_only": d["version_only"]})
        (stage / "versions.json").write_text(json.dumps(versions, indent=2, ensure_ascii=False) + "\n")
        pj = json.loads((stage / ".claude-plugin" / "plugin.json").read_text())
        pj["version"] = pv
        (stage / ".claude-plugin" / "plugin.json").write_text(json.dumps(pj, indent=2, ensure_ascii=False) + "\n")
        entry = [f"## {pv} ({report['checked_at_utc'][:10]})", "",
                 f"Source bundle {bsha[:12]} (source version {ver}).", ""]
        labels = {"added": "Added", "removed": "Removed", "changed": "Method or files changed",
                  "version_only": "New version label only"}
        for k, label in labels.items():
            if d[k]:
                entry.append(f"- {label}: " + ", ".join(d[k]))
        if not (d["added"] or d["removed"] or d["changed"] or d["version_only"]):
            entry.append("- Bundle repackaged; no skill content changed.")
        for f in new_cm.get("problems", []):
            entry.append(f"- Flag: {f}")
        cl = stage / "CHANGELOG.md"
        head, _, rest = cl.read_text().partition("\n\n")
        cl.write_text(head + "\n\n" + "\n".join(entry) + "\n\n" + rest)

        chk = run("check_repo.py", stage)
        if chk.returncode != 0:
            finish("apply_failed", 6, detail=chk.stdout.strip().splitlines())

        for name in ("skills",):
            if (repo / name).exists():
                shutil.rmtree(repo / name)
            shutil.copytree(stage / name, repo / name)
        for f in ("conversion-manifest.json", "versions.json", "CHANGELOG.md", ".claude-plugin/plugin.json"):
            shutil.copy2(stage / f, repo / f)
        finish("applied", 11)


if __name__ == "__main__":
    main()

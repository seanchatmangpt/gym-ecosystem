#!/usr/bin/env python3
"""Reconcile direct Git submodules to their remote default-branch crowns.

This is a bounded repository operation: it observes declared direct submodules,
plans drift, and (with --apply) checks out the observed remote crown and updates
all matching lock identities. It never merges, publishes, or changes authority;
those operations remain in the GitHub Actions control loop.
"""
from __future__ import annotations

import argparse
import configparser
import datetime as dt
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "ecosystem.lock.toml"


def run(*args: str, cwd: Path = ROOT, check: bool = True) -> str:
    cp = subprocess.run(args, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if check and cp.returncode:
        raise SystemExit(f"COMMAND_FAILED[{cp.returncode}]: {' '.join(args)}\n{cp.stderr}")
    return cp.stdout


def submodules() -> list[dict[str, str]]:
    parser = configparser.ConfigParser()
    parser.read(ROOT / ".gitmodules")
    result: list[dict[str, str]] = []
    for section in parser.sections():
        if not section.startswith("submodule "):
            continue
        result.append({"name": section[len("submodule "):].strip('"'), "path": parser[section]["path"], "url": parser[section]["url"]})
    return sorted(result, key=lambda row: row["path"])


def gitlink(path: str) -> str:
    line = run("git", "ls-tree", "HEAD", "--", path).strip()
    if not line:
        raise SystemExit(f"CROWN_BLOCKED[MISSING_GITLINK]:{path}")
    mode, kind, sha, _ = line.split(None, 3)
    if mode != "160000" or kind != "commit":
        raise SystemExit(f"CROWN_BLOCKED[NOT_GITLINK]:{path}:{mode}:{kind}")
    return sha


def remote_head(url: str) -> tuple[str, str]:
    text = run("git", "ls-remote", "--symref", url, "HEAD")
    default_ref = ""
    head_sha = ""
    for line in text.splitlines():
        if line.startswith("ref:") and line.endswith("\tHEAD"):
            default_ref = line.split()[1]
        elif line.endswith("\tHEAD") and re.fullmatch(r"[0-9a-f]{40}\tHEAD", line):
            head_sha = line.split("\t", 1)[0]
    if not default_ref or not head_sha:
        raise SystemExit(f"CROWN_BLOCKED[REMOTE_HEAD_UNRESOLVED]:{url}")
    return default_ref, head_sha


def replace_exact_sha(path: Path, old: str, new: str) -> int:
    if not path.exists() or old == new:
        return 0
    text = path.read_text()
    count = text.count(old)
    if count:
        path.write_text(text.replace(old, new))
    return count


def update_lock_metadata(base_sha: str) -> None:
    text = LOCK.read_text()
    now = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    text = re.sub(r'^base_main_sha = "[0-9a-f]{40}"$', f'base_main_sha = "{base_sha}"', text, count=1, flags=re.M)
    text = re.sub(r'^updated_at = "[^"]+"$', f'updated_at = "{now}"', text, count=1, flags=re.M)
    LOCK.write_text(text)


def synchronize_marketplace_default(new_sha: str) -> list[str]:
    changed: list[str] = []
    pattern = re.compile(r'(marketplace_sha:\n(?:[ \t]+.*\n)*?[ \t]+default: )[0-9a-f]{40}', re.M)
    for rel in ("ontology.ttl", ".github/workflows/ggen-ecosystem-sync.yml"):
        path = ROOT / rel
        if not path.exists():
            continue
        text = path.read_text()
        updated, n = pattern.subn(rf'\g<1>{new_sha}', text)
        if n and updated != text:
            path.write_text(updated)
            changed.append(rel)
    return changed


def plan() -> dict:
    rows = []
    for sub in submodules():
        current = gitlink(sub["path"])
        default_ref, latest = remote_head(sub["url"])
        rows.append({**sub, "current": current, "default_ref": default_ref, "latest": latest, "changed": current != latest})
    return {
        "schema": "https://ggen.dev/receipts/autonomic-crown/v1",
        "repository": run("git", "config", "--get", "remote.origin.url", check=False).strip(),
        "base_sha": run("git", "rev-parse", "HEAD").strip(),
        "submodules": rows,
        "changed_count": sum(1 for row in rows if row["changed"]),
    }


def apply(doc: dict) -> None:
    marketplace_sha: str | None = None
    for row in doc["submodules"]:
        if row["path"] == "vendor/ggen-marketplace":
            marketplace_sha = row["latest"]
        if not row["changed"]:
            continue
        path = row["path"]
        run("git", "submodule", "update", "--init", "--depth", "1", "--", path)
        run("git", "fetch", "--depth", "1", "origin", row["default_ref"], cwd=ROOT / path)
        run("git", "checkout", "--detach", row["latest"], cwd=ROOT / path)
        replaced = replace_exact_sha(LOCK, row["current"], row["latest"])
        if replaced == 0:
            raise SystemExit(f"CROWN_BLOCKED[LOCK_PIN_NOT_FOUND]:{path}:{row['current']}")
    mirrors = synchronize_marketplace_default(marketplace_sha) if marketplace_sha else []
    doc["mirrors_updated"] = mirrors
    if doc["changed_count"] or mirrors:
        update_lock_metadata(doc["base_sha"])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--receipt", default="artifacts/autonomic-crown.json")
    args = ap.parse_args()
    doc = plan()
    if args.apply:
        apply(doc)
    receipt = Path(args.receipt)
    if not receipt.is_absolute():
        receipt = ROOT / receipt
    receipt.parent.mkdir(parents=True, exist_ok=True)
    receipt.write_text(json.dumps(doc, indent=2, sort_keys=True) + "\n")
    print(json.dumps(doc, sort_keys=True))
    print(f"AUTONOMIC_CROWN_PLAN_ALIVE changed={doc['changed_count']} mirrors={len(doc.get('mirrors_updated', []))} apply={str(args.apply).lower()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

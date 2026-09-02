#!/usr/bin/env python3
"""Reconcile direct Git submodules to their remote default-branch crowns.

The runtime authority boundary is intentionally narrow: with --apply this script
may update only declared submodule Gitlinks and their exact identities in
`ecosystem.lock.toml`. Workflow definitions and other authored surfaces are not
runtime crown state.
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
        result.append({
            "name": section[len("submodule "):].strip('"'),
            "path": parser[section]["path"],
            "url": parser[section]["url"],
        })
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


def plan() -> dict:
    rows = []
    for sub in submodules():
        current = gitlink(sub["path"])
        default_ref, latest = remote_head(sub["url"])
        rows.append({**sub, "current": current, "default_ref": default_ref, "latest": latest, "changed": current != latest})
    return {
        "schema": "https://ggen.dev/receipts/gym-autonomic-crown/v2",
        "repository": run("git", "config", "--get", "remote.origin.url", check=False).strip(),
        "base_sha": run("git", "rev-parse", "HEAD").strip(),
        "authority_boundary": "gitlinks+lock-only",
        "submodules": rows,
        "changed_count": sum(1 for row in rows if row["changed"]),
    }


def apply(doc: dict) -> None:
    for row in doc["submodules"]:
        if not row["changed"]:
            continue
        path = row["path"]
        run("git", "submodule", "update", "--init", "--depth", "1", "--", path)
        run("git", "fetch", "--depth", "1", "origin", row["default_ref"], cwd=ROOT / path)
        run("git", "checkout", "--detach", row["latest"], cwd=ROOT / path)
        replaced = replace_exact_sha(LOCK, row["current"], row["latest"])
        if replaced == 0:
            raise SystemExit(f"CROWN_BLOCKED[LOCK_PIN_NOT_FOUND]:{path}:{row['current']}")
    if doc["changed_count"]:
        update_lock_metadata(doc["base_sha"])

    workflow_drift = run("git", "diff", "--name-only", "--", ".github/workflows", check=False).strip()
    if workflow_drift:
        raise SystemExit(f"CROWN_BLOCKED[WORKFLOW_MUTATION_OUTSIDE_AUTHORITY]:{workflow_drift.replace(chr(10), ',')}")


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
    print(f"GYM_AUTONOMIC_CROWN_PLAN_ALIVE changed={doc['changed_count']} authority=gitlinks+lock-only apply={str(args.apply).lower()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

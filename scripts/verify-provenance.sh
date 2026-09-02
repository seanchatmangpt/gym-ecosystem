#!/usr/bin/env bash
set -euo pipefail

python3 - <<'PY'
from pathlib import Path
import subprocess
import tomllib

root = Path.cwd()
lock = tomllib.loads((root / "ecosystem.lock.toml").read_text())
submodules = lock["submodules"]

keys = sorted(k[:-5] for k in submodules if k.endswith("_path"))
expected = []
errors = []
for key in keys:
    path_key = f"{key}_path"
    commit_key = f"{key}_commit"
    if commit_key not in submodules:
        errors.append(f"{key}: missing {commit_key} in lock")
        continue
    expected.append((submodules[path_key], submodules[commit_key]))

try:
    declared_raw = subprocess.check_output(
        ["git", "config", "-f", ".gitmodules", "--get-regexp", r"^submodule\..*\.path$"],
        text=True,
    )
except subprocess.CalledProcessError:
    declared_raw = ""
declared_paths = {line.split(None, 1)[1] for line in declared_raw.splitlines() if line.strip()}
locked_paths = {path for path, _ in expected}

for missing in sorted(locked_paths - declared_paths):
    errors.append(f"{missing}: locked but missing from .gitmodules")
for extra in sorted(declared_paths - locked_paths):
    errors.append(f"{extra}: declared in .gitmodules but missing from lock")

for path, wanted in expected:
    mode = subprocess.check_output(
        ["git", "ls-files", "-s", "--", path], text=True
    ).strip().split()
    if len(mode) < 2:
        errors.append(f"{path}: missing gitlink")
        continue
    actual_mode, actual_sha = mode[0], mode[1]
    if actual_mode != "160000":
        errors.append(f"{path}: mode={actual_mode}, expected=160000")
    if actual_sha != wanted:
        errors.append(f"{path}: gitlink={actual_sha}, lock={wanted}")

    checkout = root / path / ".git"
    if checkout.exists():
        checked_out = subprocess.check_output(
            ["git", "-C", str(root / path), "rev-parse", "HEAD"], text=True
        ).strip()
        if checked_out != wanted:
            errors.append(f"{path}: checkout={checked_out}, lock={wanted}")

if errors:
    raise SystemExit("PROVENANCE_BLOCKED\n" + "\n".join(errors))

print(f"PROVENANCE_ALIVE direct_submodules={len(expected)}")
for path, wanted in expected:
    print(f"{path} {wanted}")
PY

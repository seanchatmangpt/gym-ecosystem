#!/usr/bin/env bash
set -euo pipefail

python3 - <<'PY'
from pathlib import Path
import subprocess
import tomllib

root = Path.cwd()
lock = tomllib.loads((root / "ecosystem.lock.toml").read_text())
submodules = lock["submodules"]
expected = [
    (submodules["gymact_path"], submodules["gymact_commit"]),
    (submodules["autofde_lab_path"], submodules["autofde_lab_commit"]),
    (submodules["sregym_path"], submodules["sregym_commit"]),
    (submodules["fdegym_path"], submodules["fdegym_commit"]),
    (submodules["ggen_ecosystem_path"], submodules["ggen_ecosystem_commit"]),
    (submodules["beam4pm_path"], submodules["beam4pm_commit"]),
]

gitmodules = (root / ".gitmodules").read_text()
errors = []
for path, wanted in expected:
    if f"path = {path}" not in gitmodules:
        errors.append(f"{path}: missing from .gitmodules")
        continue
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

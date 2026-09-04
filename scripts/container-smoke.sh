#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

python3 - <<'PY'
from pathlib import Path
import tomllib

root = Path.cwd()
lock = tomllib.loads((root / "ecosystem.lock.toml").read_text())
subs = lock["submodules"]
keys = sorted(k[:-5] for k in subs if k.endswith("_path"))
if len(keys) < 13:
    raise SystemExit(f"GYM_ECOSYSTEM_CONTAINER_BLOCKED[DIRECT_SUBMODULE_COUNT]:{len(keys)}")
for key in keys:
    path = root / subs[f"{key}_path"]
    if not path.is_dir():
        raise SystemExit(f"GYM_ECOSYSTEM_CONTAINER_BLOCKED[MISSING_VENDOR]:{path}")
    if not any(path.iterdir()):
        raise SystemExit(f"GYM_ECOSYSTEM_CONTAINER_BLOCKED[EMPTY_VENDOR]:{path}")
print(f"GYM_VENDOR_CORPUS_ALIVE direct_submodules={len(keys)}")
PY

command -v ggen >/dev/null
ggen --help >/dev/null

test -x vendor/ggen-ecosystem/bin/ggen-ecosystem
vendor/ggen-ecosystem/bin/ggen-ecosystem --help | grep -q manufacture

test -f vendor/gymact/pyproject.toml
test -f vendor/autofde-lab/pyproject.toml
test -f vendor/beam4pm/mix.exs

echo "GYM_ECOSYSTEM_CONTAINER_ALIVE manufacturer=ggen-ecosystem runtime=gymact planner=autofde-lab process-intelligence=beam4pm"

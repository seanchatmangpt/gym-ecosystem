# Cleanup and Merge Plan: gym-ecosystem / gymact

## Current State (as observed 2026-09-17)

| Path | Type | Git status summary | Last commit | Size |
|---|---|---|---|---|
| `/Users/sac/gym-ecosystem` | canonical repo (submodule superproject) | dirty: 2 submodule pointers modified (`vendor/autofde-lab`, `vendor/ggen-ecosystem` have uncommitted changes inside them), 1 untracked dir (`docs/`, this plan's own home). HEAD branch `chore/crown-submodule-sync-ggen` is fully in sync with `origin/chore/crown-submodule-sync-ggen` (0 ahead/0 behind) but **diverged from local `main`** (local `main` is 6 commits behind this HEAD) and local `main` is separately **9 commits behind `origin/main`**. | `1972bb70` 2026-09-05 "chore(crown): bump vendor/autofde-lab to origin/master tip edca036" | 4.8G |
| `/Users/sac/gym-ecosystem` → `vendor/gymact` (gitlink) | submodule reference, **not checked out** (empty dir on disk) | pinned commit `2ce639c0e68da2588549e0c21550c8587cfef9cc` | n/a | 0 (uninitialized) |
| `/Users/sac/gymact` | independent repo, **same remote the submodule points at** (`https://github.com/seanchatmangpt/gymact.git`) | dirty: 5 tracked files modified (`pyproject.toml`, two OCEL fixture JSONs, `tests/conftest.py`, `tests/fixtures/real_episode.ocel.json`) + ~30+ untracked `.inspect_logs/*.eval` files on `main` itself. `main` is up to date with `origin/main` (`[origin/main]`, no ahead/behind shown by `git branch -vv`). | `4ab72e68` 2026-09-12 "fix: close real gaps from second remote-branch cleanup sweep (24 stale branches)" | 1.6G |
| `/Users/sac/gymact/.claude/worktrees/agent-a1c8c87cb1a7bbbe4` | git worktree of `/Users/sac/gymact` (branch `worktree-agent-a1c8c87cb1a7bbbe4` @ `2e27dbc`) | dirty: 2 untracked new files (`mcp_client_session.py` + test) | 2026-08-07 `2e27dbcf` | 624K |
| `/Users/sac/gymact/.claude/worktrees/agent-a22976ec3b84ddb68` | git worktree (branch `agent/terminal-bench-gym` @ `32eae29`) | dirty: 2 modified + 3 untracked (new `terminal_bench.py` provider + fixtures + test) | 2026-08-07 `32eae299` | 65M |
| `/Users/sac/gymact/.claude/worktrees/agent-a409afaa96b24eb66` | git worktree (branch `worktree-agent-a409afaa96b24eb66` @ `2e27dbc`) | dirty: 2 untracked (new `kubernetes_reconciliation.py` + test) | 2026-08-07 `2e27dbcf` | 804K |
| `/Users/sac/gymact/.claude/worktrees/agent-a4a0a742148dddf68` | git worktree (branch `worktree-agent-a4a0a742148dddf68` @ `32eae29`) | dirty: 3 modified (README/docs) + 2 untracked (new `kubernetes_goat.py` + test) | 2026-08-07 `32eae299` | 1.5M |
| `/Users/sac/gymact/.claude/worktrees/agent-a579966c7d57b457e` | git worktree (branch `pr10-verify` @ `ae5327b`) | **CLEAN** | 2026-08-07 `ae5327b6` | 65M |
| `/Users/sac/gymact/.claude/worktrees/agent-a83625870769e21dd` | git worktree (branch `worktree-agent-a83625870769e21dd` @ `2e27dbc`) | dirty: 2 untracked (new `terraform_plan.py` provider name variant + test) | 2026-08-07 `2e27dbcf` | 1.3M |
| `/Users/sac/gymact/.claude/worktrees/agent-ac79210f914751137` | git worktree (branch `worktree-agent-ac79210f914751137` @ `32eae29`) | dirty: 2 modified + 2 untracked (new `tau2_bench.py` + test) | 2026-08-07 `32eae299` | 65M |
| `/Users/sac/gymact/.claude/worktrees/agent-ac97f2fa3fe1bca10` | git worktree (branch `agent/vendor-benchmark-coverage-v26-8-7-clean` @ `7d5f3fb`, upstream branch on origin is gone) | dirty: 5 modified files (README/docs/vendor_benchmarks.py/fixture) | 2026-08-07 `7d5f3fbf` | 65M |
| `/Users/sac/gymact/.claude/worktrees/agent-af75a90c8414135c8` | git worktree (branch `worktree-agent-af75a90c8414135c8` @ `ecb1ddb`) | dirty: 3 modified (README/docs) + 2 untracked (`kubernetes_goat.py` + test, duplicate filename of the one in `agent-a4a0a742148dddf68`) | 2026-08-07 `ecb1ddb5` | 784K |
| `/Users/sac/gymact/.claude/worktrees/agent-afbdaa481ad7db914` | git worktree (branch `worktree-agent-afbdaa481ad7db914` @ `2e27dbc`) | dirty: 2 untracked (new `terraform_docker_apply.py` fixtures/provider + test) | (same base `2e27dbc`) | 64M |
| `/Users/sac/gymact/.claude/worktrees/codebase-env-gen-2` | git worktree (branch `task/codebase-env-generalize-20260903` @ `2ce639c` — **exactly the commit `vendor/gymact` is pinned to in gym-ecosystem**) | dirty: 1 modified (`codebase.py`) + 4 untracked new test files | 2026-09-02 `2ce639c0` | 23M |

Related directories seen directly under `~` sharing the "worktree/temp/scratch" naming pattern but **not** in the investigated family and not deep-dived here: `ex4pm-worktrees`, `ggen-marketplace-worktrees`, `f5arch-scratch-home`, `f5deploy-scratch-home`, `fortune5-scratch-consumer`, `gi04-scratch`, `gm03-scratch-consumer`, `gm03-scratch-consumer2`, `ktemp`, `scratch-ggen`, `scratch-ggen-verify2`, `scratch-venv`, `tmp_beam4pm_work`, `unibit-overnight-worktree`, `wasm4pm-worktrees`, `worktrees`, `xaas-worktrees` — flagged in Open Questions, not planned here.

## What "merged" should look like

**Canonical path going forward: `/Users/sac/gymact`.**

Evidence:
- `/Users/sac/gymact`'s `main` is at `4ab72e68` (2026-09-12); its worktrees are all descendants of earlier commits on that same repo's history — the single real upstream of the gymact codebase.
- `vendor/gymact` inside `/Users/sac/gym-ecosystem` is pinned to `2ce639c0`, confirmed via `git merge-base --is-ancestor` to be a direct ancestor of gymact's current `main`, 347 commits behind. The submodule checkout is not even initialized on disk (empty dir). This is a stale, uninitialized pointer into the same history `/Users/sac/gymact` already has current — not an alternate lineage to reconcile.
- `/Users/sac/gymact`'s `main` matches `origin/main` exactly; the gym-ecosystem reference to gymact isn't even checked out.

Conclusion: no history merge is needed between "two gymact repos" — this is a **pointer bump** (update `vendor/gymact`'s pinned commit to gymact's `main` tip) once gymact's `main` is confirmed clean, not a merge. `/Users/sac/gymact` remains canonical for gymact source.

For `/Users/sac/gym-ecosystem` itself, canonical is **`origin/main`**: it is 9 commits ahead of local `main`, while the currently checked-out branch (`chore/crown-submodule-sync-ggen`) already has its own work fully pushed to its own origin ref (0 ahead/0 behind) — it needs a normal PR/merge into `main`, not a local reconciliation, and local `main` has zero unique commits at risk.

### Per-path disposition

- **`/Users/sac/gymact` (canonical)** — keep as-is. MANUAL REVIEW REQUIRED first: 5 modified tracked files + `.inspect_logs/*.eval` untracked files sit directly on `main` uncommitted; decide commit vs. discard before treating this as a clean baseline for the worktree cleanup below.
- **`vendor/gymact` submodule reference in gym-ecosystem** — after the above is resolved, bump the gitlink to gymact's confirmed-clean `main` tip. One-line pointer-bump commit, not a merge.
- **`agent-a579966c7d57b457e` (`pr10-verify` @ `ae5327b`)** — CLEAN, upstream branch gone on origin, 2 commits ahead of `main`. Safe to `git worktree remove` directly (no uncommitted changes to lose); review separately whether its 2 commits are already squash-merged into `main` before deleting the branch ref itself.
- **`agent-a1c8c87cb1a7bbbe4`, `agent-a409afaa96b24eb66`, `agent-a83625870769e21dd`, `agent-afbdaa481ad7db914`** — each has an untracked provider+test pair whose filename **already exists on `main`** (confirmed via `git cat-file -e main:<path>`). MANUAL REVIEW REQUIRED: diff each untracked file against `main`'s version; if subsumed, remove the worktree with no cherry-pick needed.
- **`agent-a22976ec3b84ddb68` (`terminal_bench.py`)** and **`agent-ac79210f914751137` (`tau2_bench.py`)** — untracked provider+test pairs that do **NOT** exist on `main` yet, plus tracked modifications. Unique, uncommitted, potentially valuable work — MANUAL REVIEW REQUIRED before commit+PR or discard. Cannot be automated since it was never committed.
- **`agent-a4a0a742148dddf68`** and **`agent-af75a90c8414135c8`** — both have an untracked `kubernetes_goat.py`+test with the same filename plus modified README/docs. MANUAL REVIEW REQUIRED: diff the two versions against each other and against `main` before deciding which (if either) is authoritative.
- **`agent-ac97f2fa3fe1bca10`** — branch 1 commit ahead of `main`, origin tracking ref gone, plus 5 live uncommitted tracked-file edits on top. MANUAL REVIEW REQUIRED — mixes a possibly-superseded branch commit with live uncommitted edits.
- **`codebase-env-gen-2`** — base commit is exactly the SHA the gym-ecosystem submodule is pinned to, with further uncommitted work (1 modified + 4 untracked test files) since. MANUAL REVIEW REQUIRED — looks like active, unfinished work, not stale scaffolding.
- **7 other local gymact branches with no worktree checked out** (`agent/vendor-benchmark-coverage-v26-8-7-clean`, `brce-full-chain-test`, `ci/local-act-parity`, `fix/registry-pack-outcome-predicates`, `integrate5/dmedi-solver-corr`, `integrate6/solver-corr`, `pr10-verify`, `verify/browsergym-container`) are 1–6 commits ahead of `main`, not ancestors of it. Fully committed (no data-loss risk) — need a per-branch PR-vs-abandon decision, lower urgency than the dirty worktrees.
- **gym-ecosystem local `main`** — 6 behind current HEAD, 9 behind `origin/main`, 0 unique commits of its own. Safe to fast-forward from `origin/main` once the current branch's PR (if any) lands.
- **`vendor/autofde-lab` / `vendor/ggen-ecosystem` dirty submodule content inside gym-ecosystem** — real uncommitted changes inside the nested checkouts (test files, a deleted `ggen.lock`). MANUAL REVIEW REQUIRED, out of gymact-focused scope but blocks a clean pointer bump on the superproject side.

## Commands to run (in order), once approved

```bash
# 1. Remove the one confirmed-safe, fully clean worktree.
git -C /Users/sac/gymact worktree remove /Users/sac/gymact/.claude/worktrees/agent-a579966c7d57b457e

# 2. MANUAL REVIEW REQUIRED (not automated): diff each "duplicate of main" untracked
#    file before removing its worktree, e.g.:
#    diff /Users/sac/gymact/.claude/worktrees/agent-a1c8c87cb1a7bbbe4/src/gymact/gyms/mcp_client_session.py \
#         <(git -C /Users/sac/gymact show main:src/gymact/gyms/mcp_client_session.py)
#    Repeat for agent-a409afaa96b24eb66 (kubernetes_reconciliation.py),
#    agent-a83625870769e21dd (terraform_plan.py), agent-afbdaa481ad7db914 (terraform_docker_apply.py).
#    Only after confirming each is subsumed by main:
#      git -C /Users/sac/gymact worktree remove <path>

# 3. MANUAL REVIEW REQUIRED (not automated) for unique/mixed uncommitted work:
#    agent-a22976ec3b84ddb68, agent-ac79210f914751137, agent-a4a0a742148dddf68,
#    agent-af75a90c8414135c8, agent-ac97f2fa3fe1bca10, codebase-env-gen-2.
#    Per worktree, either:
#      cd <worktree> && git add -A && git commit -F <message-file> && git push -u origin <branch> && gh pr create ...
#    or, only after explicit human sign-off to discard:
#      git -C /Users/sac/gymact worktree remove --force <path>

# 4. After (3) is resolved for a worktree, remove it the same way as step 1/2:
#    git -C /Users/sac/gymact worktree remove <path>

# 5. Review the 8 committed-but-unmerged local branches (no data-loss risk, just PR/abandon decision):
git -C /Users/sac/gymact log --oneline main..agent/vendor-benchmark-coverage-v26-8-7-clean
git -C /Users/sac/gymact log --oneline main..brce-full-chain-test
git -C /Users/sac/gymact log --oneline main..ci/local-act-parity
git -C /Users/sac/gymact log --oneline main..fix/registry-pack-outcome-predicates
git -C /Users/sac/gymact log --oneline main..integrate5/dmedi-solver-corr
git -C /Users/sac/gymact log --oneline main..integrate6/solver-corr
git -C /Users/sac/gymact log --oneline main..pr10-verify
git -C /Users/sac/gymact log --oneline main..verify/browsergym-container
# then per branch: open a PR, or (only after explicit human sign-off) git -C /Users/sac/gymact branch -D <branch>

# 6. MANUAL REVIEW REQUIRED: resolve gym-ecosystem's own dirty submodule state first:
cd /Users/sac/gym-ecosystem
git -C vendor/autofde-lab status --short   # review, then commit or discard upstream in that repo
git -C vendor/ggen-ecosystem status --short   # review, then commit or discard upstream in that repo

# 7. Once (6) is clean, bump the vendor/gymact pointer to gymact's confirmed-clean main tip:
git -C /Users/sac/gym-ecosystem submodule update --init vendor/gymact
cd /Users/sac/gym-ecosystem/vendor/gymact && git checkout main && git pull --ff-only origin main
cd /Users/sac/gym-ecosystem
git add vendor/gymact
git commit -F <message-file describing "bump vendor/gymact to <new SHA>">

# 8. Fast-forward gym-ecosystem's local main from origin/main (no unique local commits on main):
git -C /Users/sac/gym-ecosystem fetch origin
git -C /Users/sac/gym-ecosystem checkout main
git -C /Users/sac/gym-ecosystem merge --ff-only origin/main
```

## Open questions

- Whether the 5 tracked-file modifications + `.inspect_logs/*.eval` untracked files directly on gymact's `main` are intentional WIP or a stray test-run byproduct — cannot tell from git alone; ask the user before touching `main`.
- Whether `agent-a4a0a742148dddf68` and `agent-af75a90c8414135c8`'s identically-named untracked `kubernetes_goat.py` are duplicate parallel attempts or one derived from the other — needs a human diff.
- Whether `agent-ac97f2fa3fe1bca10`'s branch (upstream tracking ref reported `gone`) was already squash-merged into `main` under a different SHA (this repo's history shows that pattern, e.g. commit `8ba52bf`'s message explicitly describes discarding a sibling implementation) — needs a content diff against `main`, not just ancestry.
- `vendor/autofde-lab` / `vendor/ggen-ecosystem` submodule-internal dirty state was observed but not deep-investigated (out of gymact-focused scope); should get its own follow-up pass.
- The broader `~` list of worktree/scratch/temp-named directories named in the original request ("~/ worktrees temps scratch etc") was noted but not investigated in this pass, which was scoped to the gym-ecosystem/gymact family specifically. Confirm whether each of those needs its own cleanup-plan pass.

---
Nothing was deleted, merged, or modified as part of this investigation — only read-only git/du/diff commands were run, plus writing this plan document itself.

## Merge Execution Log (2026-09-17)

Scope: content-level capture/preservation only, per explicit instruction. **Nothing
was deleted** — no `rm`, no `git worktree remove`, no `git branch -d/-D`, no
`git clean`, no `git checkout -- <path>`, no `git reset --hard`. Every action below is
either a real commit (adding content) or a real push (making an existing/new commit
reachable on `origin`). All worktrees, all branches, and all files noted in the
"Current State" table above still exist exactly as they did before this pass, except
where content that was previously *only uncommitted* is now *also committed* on a real
ref.

### gymact — re-verified current state first

Re-ran the investigation commands; state matched the doc almost exactly, with one
correction (below) and one new fact: `git branch -vv` on `/Users/sac/gymact` shows 4
more no-worktree local branches than this doc originally listed
(`feat/mna-observed-state-replanning`, `integrate/certificate-federation`,
`integrate2/cloud-obs-equiv-trace-runtime`, `integrate2/integration-all-relevant-20260819`,
`integrate3/agent-v26-8-7-sota-hardening`, `integrate4/v2687sota`,
`recover/dirty-worktree-20260828` — 7, not 4, beyond the original 8). All were pushed
(see below); none were investigated for PR-worthiness beyond "does it have real
commits ahead of main" (yes, in every case).

**Correction to this doc's own "Per-path disposition" claims**, per
`criticism-discipline.md` rule 4 (re-derive, don't just re-assert): the doc said the
`agent-a1c8c87cb1a7bbbe4` / `agent-a409afaa96b24eb66` / `agent-a83625870769e21dd` /
`agent-afbdaa481ad7db914` untracked files were "subsumed by main" based only on
`git cat-file -e` (path existence), not a content diff. Actually diffing them: main's
versions are **later, improved revisions** of the same providers (e.g.
`requires_authority` default flipped `False`→`True`, a `time.sleep` poll loop replaced
by a shared `poll_until()` helper) — not identical duplicates, but confirmed
superseded via real diff + ancestry (`git merge-base --is-ancestor`) this time.
No action needed; nothing unique to capture in these four worktrees.

1. **`preserve/main-wip-20260917`** (new branch off `main` @ `4ab72e6`) — commit
   `0cf986e`, pushed to `origin`. Captures gymact's `main` uncommitted state: the
   `pyproject.toml`/`tests/conftest.py` pytest-teardown-hardening pair, the 3
   regenerated `.ocel.json` files, 50 new `.inspect_logs/*.eval` receipts, and
   `docs/jira/v26.9.15/`. `main` itself was left untouched — checked back out to
   `main` afterward and confirmed clean (`git status` empty, `up to date with
   origin/main`). Whether this WIP belongs on `main` is still a human call.
2. **`agent/terminal-bench-gym`** (worktree `agent-a22976ec3b84ddb68`) — commit
   `67ab82b`, pushed. New `terminal_bench.py` provider + fixtures + test + its
   `pyproject.toml` optional-dependency entry. Confirmed absent from `main`. Left the
   `tests/fixtures/real_episode.ocel.json` regenerated-byproduct diff uncommitted
   (still shows dirty in this worktree, on purpose).
3. **`worktree-agent-ac79210f914751137`** (its own auto-generated branch name, kept
   as-is) — commit `afcfd7f`, pushed. New `tau2_bench.py` provider + test + its
   `pyproject.toml` entry. Confirmed absent from `main`. Same `real_episode.ocel.json`
   byproduct left uncommitted.
4. **`worktree-agent-a4a0a742148dddf68`** — commit `413f5b3`, pushed. New
   `kubernetes_goat.py` provider + test only (README/docs left uncommitted — diffing
   this worktree's docs against current `main` showed `main` has diverged too far for
   a plain file copy to be additive; a real text merge is needed, not attempted here).
   Diffed directly against the identically-named pair in `agent-af75a90c8414135c8`:
   this version is the later one (its own docstring says it "corrects an earlier,
   wrong assumption in this same module"; its base commit `32eae29` has
   `af75a90c8414135c8`'s base `ecb1ddb` as an ancestor). `agent-af75a90c8414135c8`'s
   copy is therefore superseded — left exactly as found, not deleted.
5. **`agent/vendor-benchmark-coverage-v26-8-7-clean`** (worktree
   `agent-ac97f2fa3fe1bca10`) — commit `255d8c4`, pushed. This answers the doc's own
   open question ("was this branch already squash-merged into main?"): **no** — the
   branch's already-committed tip (`7d5f3fb`) IS nearly identical to `main`
   (11-line diff, style-only), but the real unique content (a `sregym` vendor entry,
   27 additional test functions main doesn't have, 3 pure-addition doc lines) was
   sitting **uncommitted** in the working tree, not in that commit. Captured it as a
   new commit on the existing branch. Note for the eventual PR: `main` independently
   added an `awesome-ai-gyms` vendor entry to the same dict that this branch predates
   and doesn't include — reconciling both entries is a real merge decision, not done
   here.
6. **`task/codebase-env-generalize-20260903`** (worktree `codebase-env-gen-2`) —
   commit `4982431`, pushed as a new branch (no prior origin ref). Committed tip
   (`2ce639c`) matches `main`'s current `codebase.py` byte-for-byte (0-line diff) —
   confirming this is the exact SHA the `vendor/gymact` submodule is pinned to,
   exactly as this doc suspected. The real content was the 592-line uncommitted
   generalization (per-language `run_test`/`run_build` dispatch, `clone_at_ref()`,
   `restore()`) plus 4 new test files, all absent from `main`.
7. **13 more already-committed local branches with no unique-content risk** (fully
   committed, just not yet reachable from any ref on `origin`) — pushed as-is, no new
   commits: `brce-full-chain-test`, `ci/local-act-parity`,
   `fix/registry-pack-outcome-predicates`, `integrate/certificate-federation`,
   `integrate2/cloud-obs-equiv-trace-runtime`,
   `integrate2/integration-all-relevant-20260819`,
   `integrate3/agent-v26-8-7-sota-hardening`, `integrate4/v2687sota`,
   `integrate5/dmedi-solver-corr`, `integrate6/solver-corr`, `pr10-verify`,
   `recover/dirty-worktree-20260828`, `verify/browsergym-container`. (`pr10-verify`'s
   local branch had a stale/mismatched upstream-tracking config pointing at
   `origin/agent/vendor-benchmark-coverage-v26-8-7-clean`; pushed it under its own
   name instead of using that misconfigured ref — did not touch that other branch.)
   `feat/mna-observed-state-replanning` was already on `origin`; skipped.

   `pr10-verify`'s 2 commits ahead of `main` rewrite `README.md` against a
   pre-rewrite structure (from 2026-08-07, before the current DCM-invariant README) —
   flagging this one specifically as very likely **not** a clean PR candidate as-is,
   despite now being safely preserved on `origin`.

None of gymact's `main`, any existing branch tip, or any worktree's working-tree
*files* were altered beyond adding the new commits above; every worktree's working
directory was left in the same dirty/clean state it was found in (re-verified with
`git status --short` per worktree after all commits — matches pre-pass state exactly
except for the files just committed).

### gym-ecosystem's own dirty submodule content

Both were on a detached `HEAD` with real uncommitted test-file changes. Per the "no
discard, no guessing" constraint, created a new branch off each `HEAD` (not `main`/
`master` — landing on the shared branch is a human decision), committed the changes
that were clearly real, intentional, in-scope test fixes, and pushed:

- **`vendor/autofde-lab`**: branch `preserve/detached-test-fixes-20260917`, commit
  `12fed49`, pushed to `origin` (`seanchatmangpt/autofde-lab`). Contents:
  `tests/fabric/test_cli.py` + `tests/test_schema_migration.py` — both convert
  `monkeypatch`-based tests to real-collaborator/state-based tests (real Typer CLI
  invocation against the real `ScikitDecideBackend` registry and a real on-disk SQLite
  cache file), matching this user's own Chicago-style testing discipline.
- **`vendor/ggen-ecosystem`**: branch `preserve/detached-test-fixes-20260917`, commit
  `23c48d9`, pushed to `origin` (`seanchatmangpt/ggen-ecosystem`). Contents: 11
  `tests/autonomics_contracts/test_0{33,35-44}_*.py` files, same pattern — drops
  `monkeypatch.setattr(subprocess, "run", ...)` for a real `sh -c` subprocess argv
  against a real temp-directory sentinel file.
  **Left uncommitted, exactly as found, per the "preserve over guessing" rule**:
  - `ggen.lock` (shown as deleted) — could not determine from git alone whether this
    deletion is intentional; still open.
  - `.cache/` (untracked, ~40M) — looks like a build/runtime cache, not source.

Both submodule checkouts now show `HEAD` on the new `preserve/...` branch rather than
the original detached commit. The gitlink pins recorded in gym-ecosystem's own commits
(on any branch) were **not** changed — this only moved each nested checkout's working
`HEAD` forward inside its own repo; `git -C vendor/<x> status` is clean except for the
two documented leftovers above.

### gym-ecosystem itself

- Local `main` fast-forwarded from `4861dfe` to `origin/main`'s `58ee97d` (34 commits,
  not the 9 this doc originally measured — origin/main moved again since this doc was
  first written). Done via `git fetch . origin/main:main`, which updates the `main`
  ref only (git refuses this if it isn't a clean fast-forward, so this is provably
  non-destructive) — **did not check out `main`**, so the currently-checked-out
  `chore/crown-submodule-sync-ggen` branch and its working tree (still showing
  `vendor/autofde-lab`/`vendor/ggen-ecosystem` as modified, plus untracked `docs/`)
  were never touched.
- **Not done, left as still-open**: bumping the `vendor/gymact` gitlink pin, and
  committing the `vendor/autofde-lab`/`vendor/ggen-ecosystem` pointer advances at the
  gym-ecosystem superproject level. Both are real, deliberate git operations
  (`git add vendor/<x> && git commit`) rather than pure content capture, and both
  require picking a target branch (`main`? the in-flight
  `chore/crown-submodule-sync-ggen`? a new branch?) — a decision this task's own hard
  constraints ("if not fully confident an action is safe and purely additive, do not
  do it") call for leaving to a human rather than guessing. `vendor/gymact` is safe to
  bump (gymact's `main` is confirmed clean, unchanged, at `4ab72e6`) whenever that
  branch decision is made.

### What's now safe to delete once a human confirms (separate pass, not done here)

- The 4 confirmed-superseded worktrees (`agent-a1c8c87cb1a7bbbe4`,
  `agent-a409afaa96b24eb66`, `agent-a83625870769e21dd`, `agent-afbdaa481ad7db914`) —
  their untracked files are strictly older than what's already on `main`.
- `agent-af75a90c8414135c8` — its `kubernetes_goat.py`/test pair is superseded by the
  version now committed and pushed from `agent-a4a0a742148dddf68` (its README/docs
  edits are identical between the two, so nothing is lost either way).
- `agent-a579966c7d57b457e` (`pr10-verify`) — clean worktree, its 2 commits are now
  safely on `origin` under the same branch name; worktree itself has nothing left to
  lose.
- Every worktree whose unique content is now committed+pushed
  (`agent-a22976ec3b84ddb68`, `agent-ac79210f914751137`, `agent-a4a0a742148dddf68`,
  `agent-ac97f2fa3fe1bca10`, `codebase-env-gen-2`) — safe to remove the *worktree*
  once a human opens/merges the corresponding PR, though the local *branch* should
  stay until that PR lands.

### Still open (unchanged or newly identified)

- Whether the `preserve/main-wip-20260917` content belongs on gymact's `main`.
- Whether `agent-ac97f2fa3fe1bca10`'s `sregym` addition and `main`'s independent
  `awesome-ai-gyms` addition to `VENDOR_REVISIONS` should both land, and how.
- Whether `agent-a4a0a742148dddf68`'s kubernetes-goat README/docs additions should be
  hand-merged into `main`'s current (much-changed) README/docs.
- `pr10-verify`'s 2 commits target a pre-rewrite README structure — likely needs to be
  re-authored against current `main`, not merged as-is.
- `ggen.lock`'s deletion in `vendor/ggen-ecosystem` and its `.cache/` directory.
- Picking a branch for the `vendor/gymact` pointer bump and for committing
  `vendor/autofde-lab`/`vendor/ggen-ecosystem`'s advanced pointers at the
  gym-ecosystem superproject level.
- The 13 already-committed branches now pushed to `origin` for the first time still
  each need an individual PR-vs-abandon decision (this pass only ensured none of them
  could be lost to local-only disk state; it did not evaluate their content for
  mergeability).
- The broader `~` list of worktree/scratch/temp directories (unchanged from the
  original Open Questions above) — still not investigated.

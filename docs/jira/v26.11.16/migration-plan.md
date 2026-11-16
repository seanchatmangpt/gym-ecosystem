# gym-ecosystem migration plan v26.11.16

Standing: UNVERIFIED

## Identity
- Path: /Users/sac/gym-ecosystem
- Remote: https://github.com/seanchatmangpt/gym-ecosystem (upstream origin/<same branch>)
- Branch: chore/crown-submodule-sync-ggen@1972bb7; last commit 2026-09-05; 27 commits; 4013 MB
- Languages/build: composition root — .gitmodules, ecosystem.lock.toml, Dockerfile, scripts/.
  No CLAUDE.md.
- Nested repos (submodules under vendor/, 3.1 GB):
  - vendor/autofde-lab (initialised, modified pointer "+12fed49")
  - vendor/ggen-ecosystem (initialised, modified pointer "+23c48d9", on a preserve/ branch)
  - vendor/beam4pm (initialised, clean)
  - vendor/SREGym, awesome-ai-gyms, biblegym, chatgptgym, claudecodegym, fdegym, gymact
    (not initialised)

## Observed state
- Dirty 2 (both submodule pointer drift: vendor/autofde-lab, vendor/ggen-ecosystem) /
  untracked 1 dir (docs/ = docs/jira/v26.9.15,17,19). ahead 0 / behind 0.
- Stash 26. Unpushed local branches: chore/crown-submodule-sync, fix/remove-phantom-gitgym-
  submodule (no upstream); docs/session-merge-log-20260905 and main both lag origin/main.
- Size 4 GB almost entirely vendor/ (submodule checkouts incl. their build dirs).

## What it is
Composition root and reference corpus for receipted, reproducible simulation ecosystems;
mirrors the ggen-ecosystem pattern with direct dependencies vendored as submodules.

## Classification
WARM (census agrees; last touched 2026-09-05, crown/submodule sync chores).

## Migration risk
MEDIUM. 26 stashes + 2 local-only branches + submodule pointer drift + untracked docs/jira.
The 3.1 GB vendor tree itself is re-cloneable from each submodule's remote, but
vendor/ggen-ecosystem sits on a local "preserve/detached-test-fixes-20260917" head that may
not exist upstream — check `git -C vendor/ggen-ecosystem status` and push it.

## Recommended action
COMMIT-PUSH
1. `cd /Users/sac/gym-ecosystem && git -C vendor/ggen-ecosystem branch -vv` and
   `git -C vendor/autofde-lab branch -vv`; push any local-only submodule branches.
2. `git add docs vendor/autofde-lab vendor/ggen-ecosystem && git commit -m "chore(crown):
   docs/jira + submodule heads v26.11.16" && git push origin HEAD`
3. `git push origin chore/crown-submodule-sync fix/remove-phantom-gitgym-submodule`
4. DECISION: 26 stashes — bundle (`git bundle create ... --all`) or drop.
5. Do NOT rsync the 4 GB. On new machine clone with
   `git clone --recurse-submodules` only for the submodules actually needed.

## First commands on the new machine
`git submodule status` then `scripts/` crown/reconcile script (see README); no build.

## See Also
- ../v26.9.19/
- /Users/sac/docs/jira/v26.11.16/README.md

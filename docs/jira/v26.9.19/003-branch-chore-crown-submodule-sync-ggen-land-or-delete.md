# gym-ecosystem: land or delete remote branch `chore/crown-submodule-sync-ggen`

- Standing: OPEN
- Created: 2026-09-19 (v26.9.19 gh survey wave)
- Source: remote branch `chore/crown-submodule-sync-ggen` — not merged into `main`, no open PR
- Evidence: `git branch -r --no-merged origin/main` lists it; absent from `gh pr list` heads

## Work to complete
- Decide: open a PR (`gh pr create -R seanchatmangpt/gym-ecosystem --head chore/crown-submodule-sync-ggen`) or delete (`git push origin --delete chore/crown-submodule-sync-ggen`).
- If superseded, delete; otherwise land through review.

## Acceptance
- After `git fetch --prune`, `git branch -r --no-merged origin/main` no longer lists `chore/crown-submodule-sync-ggen`.

## History
- 2026-09-19 | OPEN | survey found PR-less unmerged branch | chore/crown-submodule-sync-ggen | decision pending

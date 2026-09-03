# Tombstone: vendor/gitgym removal

- **Date:** 2026-09-03
- **Old repository URL:** https://github.com/seanchatmangpt/gitgym.git
- **Old pinned SHA:** f0856a18bb98d4c9bef5b2d3d1acfac7b11ad7bb
- **Claimed role (per ecosystem.lock.toml / README.md):** "Git/repository lifecycle reference gym"
- **Actual observed role:** Generic Nuxt.js SaaS landing-page template. `package.json`
  at both the pinned SHA and current upstream `main` HEAD reports
  `"name": "nuxt-ui-pro-template-saas"`, with Nuxt/Nuxt UI Pro build scripts
  (`nuxt build`, `nuxt dev`, `nuxt generate`) and a dependency set (`@nuxt/ui-pro`,
  `@nuxt/content`, `@nuxt/image`, `@unovis/vue`, etc.) consistent with a SaaS
  marketing site, not a git/repository-lifecycle tooling or training environment.

## Evidence commands (exact, real output captured 2026-09-03)

```
$ gh api users/seanchatmangpt/repos --paginate --jq '.[].name' | grep -i gitgym
gitgym
```
(Confirms a repository literally named `gitgym` does exist under the account —
so this is not a case of the submodule pointing at a nonexistent repo. The
mismatch is in *content*, not in *existence*.)

```
$ gh api repos/seanchatmangpt/gitgym --jq '{name,full_name,description,default_branch,pushed_at}'
{"name":"gitgym","full_name":"seanchatmangpt/gitgym","description":"A swarm of agents to do everything with git.","default_branch":"main","pushed_at":"2026-08-24T00:02:18Z"}
```
(The repo's *description* claims git-related purpose, but the actual tracked
content contradicts it — see below.)

```
$ gh api "repos/seanchatmangpt/gitgym/contents/package.json?ref=f0856a18bb98d4c9bef5b2d3d1acfac7b11ad7bb" --jq '.content' | base64 -d | head -20
{
  "name": "nuxt-ui-pro-template-saas",
  "private": true,
  "type": "module",
  "scripts": {
    "build": "nuxt build",
    "dev": "nuxt dev -o",
    "generate": "nuxt generate",
    "preview": "nuxt preview",
    "postinstall": "nuxt prepare",
    "lint": "eslint .",
    "typecheck": "nuxt typecheck",
    "start:json-server": "json-server --watch data/db.json --port 3001",
    "n8n": "docker run -d ... n8nio/n8n"
  },
  "dependencies": {
    "@faker-js/faker": "^9.3.0",
    "@heroicons/vue": "^2.2.0",
    ...
    "@nuxt/ui-pro": "^1.4.4",
    ...
```
(Content read directly at the exact pinned SHA — this is the exact commit the
submodule was vendored at, not a later drifted state.)

```
$ gh api repos/seanchatmangpt/gitgym/contents/package.json --jq '.content' | base64 -d | head -20
{
  "name": "nuxt-ui-pro-template-saas",
  ...
```
(Content read at current upstream `main` HEAD — identical mismatch persists;
this was never corrected upstream to match the claimed role, at the pinned
commit or since.)

## Reason for removal

- No repository containing actual git/repository-lifecycle-gym content exists
  anywhere in the accessible corpus under this account — the only repo named
  `gitgym` is, and was at the pinned SHA, a generic Nuxt SaaS template.
- No planning-doc evidence was found indicating this was a deliberate,
  documented placeholder pending real content (no such note in this repo's
  README, ecosystem.lock.toml, or elsewhere in the accessible corpus).
- The content has never matched the claimed role "Git/repository lifecycle
  reference gym" — not at the pinned vendored SHA, and not at current upstream
  HEAD as of this investigation (2026-09-03).

## Standing transition

`REFUSED[ROLE_IDENTITY_MISMATCH] -> REMOVED_WITH_RECEIPT`

This removal is a **correction of a false composition claim** in
`ecosystem.lock.toml` / `.gitmodules` / `README.md` — the ecosystem lock was
asserting a submodule's role that its actual tracked content never supported.
It is not a deletion of unique or irreplaceable source: the removed submodule
pointer carried no git/repository-lifecycle-gym functionality to lose, and the
upstream `gitgym` repository itself is untouched by this change (only the
vendoring/pointer in this ecosystem repo is removed).

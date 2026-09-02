# gym-ecosystem

Composition root for receipted, reproducible simulation ecosystems.

`gym-ecosystem` composes pinned repositories into one experiment boundary. It mirrors the `ggen-ecosystem` pattern: direct dependencies live under `vendor/`, `.gitmodules` declares transport, `ecosystem.lock.toml` declares exact identity and role, and CI proves the Git links and lock agree on the exact pull-request head.

## Composition

| Vendor | Role |
| --- | --- |
| `vendor/gymact` | execution physics, providers, authority boundaries, receipts, verification and scoring |
| `vendor/autofde-lab` | planners, policies, search, replay compilation and counterfactual experiment logic |
| `vendor/SREGym` | SRE/operations environments and benchmarks |
| `vendor/fdegym` | Forward Deployed Engineering environments and benchmarks |
| `vendor/ggen-ecosystem` | deterministic software-manufacturing substrate |
| `vendor/beam4pm` | OCEL/process mining and process-intelligence feedback |

Consumers integrate this repository as the gym composition boundary; direct vendor pins are internal ecosystem concerns.

## Bootstrap

```bash
git clone --recurse-submodules https://github.com/seanchatmangpt/gym-ecosystem.git
cd gym-ecosystem
./scripts/verify-provenance.sh
```

The verifier checks `.gitmodules`, Gitlink mode (`160000`), lock identities, and—when submodules are materialized—the checked-out commit for every direct vendor.

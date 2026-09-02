# gym-ecosystem

Composition root and reference corpus for receipted, reproducible simulation ecosystems.

`gym-ecosystem` mirrors the `ggen-ecosystem` composition pattern: direct dependencies live under `vendor/`, `.gitmodules` declares transport, `ecosystem.lock.toml` declares exact identity and role, and CI proves every Gitlink and lock entry agree on the exact pull-request head.

## Architecture

The ecosystem separates discovery, planning, execution, manufacturing, and process intelligence:

```text
awesome-ai-gyms + owned reference gyms
              |
              v
         autofde-lab
        SELECT / PLAN
              |
              v
            gymact
   MATERIALIZE / OBSERVE / DO / VERIFY / RECEIPT
              |
              +--------------------+
              |                    |
              v                    v
        concrete gyms           beam4pm
        world physics       OCEL / process intelligence
              |
              v
        ggen-ecosystem
    deterministic manufacture
              |
              v
      downstream customer gym
```

## Owned gym catalog

The lock contains every owner-visible repository whose name contains `gym`, excluding this composition repository itself.

| Vendor | Role |
| --- | --- |
| `vendor/awesome-ai-gyms` | DfCM discovery/preservation registry for the wider gym frontier |
| `vendor/biblegym` | formation-domain reference gym |
| `vendor/chatgptgym` | ChatGPT/cloud-agent reference gym |
| `vendor/claudecodegym` | Claude Code reference gym |
| `vendor/fdegym` | Forward Deployed Engineering environments and benchmarks |
| `vendor/gitgym` | Git/repository lifecycle reference gym |
| `vendor/gymact` | canonical execution kernel and reference environment substrate |
| `vendor/lifegym` | life-domain planning/environment reference gym |
| `vendor/rrgym` | institutional/relational reasoning reference gym |
| `vendor/SREGym` | SRE/operations environments, failure worlds and benchmarks |
| `vendor/ww3gym` | geopolitical/adversarial multi-party reference gym |

Control-plane peers remain directly pinned as well:

| Vendor | Role |
| --- | --- |
| `vendor/autofde-lab` | planners, policies, history-to-plan replay and counterfactual experiments |
| `vendor/ggen-ecosystem` | deterministic manufacturer for downstream customer gyms |
| `vendor/beam4pm` | OCEL/process mining and process-intelligence feedback |

## Downstream manufacture

Reference gyms are evidence and reusable knowledge, not customer forks. A downstream customer supplies an admitted gym specification (`ggen.toml`, `ontology.ttl`, and admitted packs/templates), and the pinned `ggen-ecosystem` wrapper manufactures the customer artifact:

```bash
vendor/ggen-ecosystem/bin/ggen-ecosystem manufacture path/to/customer-gym
```

The production function is:

```text
customer intent / constraints
          |
          v
       ontology O*
          |
          v
reference gym corpus + admitted packs
          |
          v
   ggen-ecosystem mu(O*)
          |
          v
independent downstream gym artifact
          |
          v
GymAct qualification / receipts / replay
```

Customer-specific gyms therefore become manufactured projections of admitted specifications. The reference repos remain independently pinned provenance inputs; generated projections are not a source-code ownership/editing surface.

## Bootstrap

```bash
git clone --recurse-submodules https://github.com/seanchatmangpt/gym-ecosystem.git
cd gym-ecosystem
./scripts/verify-provenance.sh
vendor/ggen-ecosystem/bin/ggen-ecosystem --help
```

The verifier checks `.gitmodules` bidirectionally against the lock, Gitlink mode (`160000`), exact commit identities, and—when materialized—the checked-out commit for every direct vendor.

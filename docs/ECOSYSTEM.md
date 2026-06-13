# SynapticFour Synaptic Core stack

Four repositories implement a domain-agnostic scientific compute fabric. This file is **mirrored** in each repo so readers can navigate without relearning structure.

**You are here:** [sc-specs](https://github.com/SynapticFour/sc-specs) — OpenAPI / AsyncAPI specifications (CC0).

## Repositories

| Repository | Role | License |
|------------|------|---------|
| **sc-specs** | API specifications (this repo) | CC0-1.0 |
| [Synaptic-Core](https://github.com/SynapticFour/Synaptic-Core) | Reference Rust server | BUSL-1.1 |
| [sc-transport](https://github.com/SynapticFour/sc-transport) | Telemetry + SPARQ transfer | BUSL-1.1 |
| [Synaptic-Core-Test](https://github.com/SynapticFour/Synaptic-Core-Test) | Conformance runner | Apache-2.0 |

## Local lifecycle (unified commands)

| Repository | Deploy | Stop | Destroy | Notes |
|------------|--------|------|---------|-------|
| **Synaptic-Core** | `make up` | `make down` | `make destroy` | Postgres + MinIO + server |
| **sc-transport** | `make up` | `make down` | `make destroy` | Optional `sct-daemon` via compose |
| **sc-specs** | — | — | — | Spec validation only (`make validate`) |
| **Synaptic-Core-Test** | — | — | — | Conformance runner (needs running Core) |

**Typical flow:**

```bash
cd Synaptic-Core && make up
cd Synaptic-Core-Test && cargo run -- --target http://127.0.0.1:8080 --all --strict
cd Synaptic-Core && make down
```

Secondary options: `docker compose`, `cargo build --release`, paths in each README.

## Quick starts

**Server (Docker):**

```bash
cd Synaptic-Core && make up
```

**Validate specifications (this repo):**

```bash
make validate
```

**Conformance:**

```bash
cd Synaptic-Core-Test
cargo run -- --target http://127.0.0.1:8080 --all --specs-dir ../sc-specs
```

## Documentation map

| Topic | Document |
|-------|----------|
| OpenAPI specs | [`specs/`](specs/) |
| GA4GH profiles | [`profiles/ga4gh/`](profiles/ga4gh/) |
| Reference server | [Synaptic-Core](https://github.com/SynapticFour/Synaptic-Core) |
| GA4GH stack (separate) | [Ferrum docs/ECOSYSTEM.md](https://github.com/SynapticFour/Ferrum/blob/main/docs/ECOSYSTEM.md) |

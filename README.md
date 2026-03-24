# Synaptic Core API Specifications

API specifications for the [Synaptic Core](https://github.com/SynapticFour/synaptic-core)
scientific compute fabric — a domain-agnostic set of primitives for stable
object identity, task execution, workflow orchestration, federated discovery,
and provenance tracking.

## Purpose

These specifications describe seven composable primitives applicable across
scientific domains: genomics, astronomy, earth observation, materials science,
neuroimaging, and beyond. They are published as **proposed standards**, not
proprietary documentation. Any group may implement them independently.

| Primitive | Endpoint prefix | What it does |
|-----------|----------------|--------------|
| sc-objects | /sc/objects/v1/ | Stable identifiers + byte-range streaming for binary objects |
| sc-tasks | /sc/tasks/v1/ | Engine-agnostic containerised task execution |
| sc-workflows | /sc/workflows/v1/ | Multi-step workflow orchestration (CWL, WDL, NF, Snakemake) |
| sc-registry | /sc/registry/v1/ | Versioned tool and workflow discovery |
| sc-query | /sc/query/v1/ | Schema-agnostic federated query across nodes |
| sc-provenance | /sc/provenance/v1/ | Append-only DAG + RO-Crate export |
| sc-transport | (event channel) | Telemetry push — SSE (stable) + QUIC datagrams (experimental) |

## Relationship to Existing Standards

These primitives are designed to be composable with existing domain standards:
- **GA4GH** (DRS, WES, TES, TRS, Beacon): see [profiles/ga4gh/](profiles/ga4gh/)
- **IVOA** (VOSpace, FITS): see [profiles/ivoa/](profiles/ivoa/)
- **STAC/OGC** (Earth Observation): see [profiles/stac/](profiles/stac/)
- **OPTIMADE** (Materials Science): see [profiles/optimade/](profiles/optimade/)

## Prior Art

Design informed by:
- GA4GH Cloud Work Stream APIs — Ellrott et al. (2024), GigaScience
- AiiDA provenance model — Huber et al. (2020), Scientific Data
- FAIR Guiding Principles — Wilkinson et al. (2016), Scientific Data
- FAIR Workflows — Wilkinson et al. (2025), arXiv:2410.03490
- RO-Crate / Workflow Run RO-Crate — Soiland-Reyes et al. (2022); Leo et al. (2024)
- OPTIMADE — Evans et al. (2021), Scientific Data

## Reference Implementation

[Synaptic Core](https://github.com/SynapticFour/synaptic-core) (Rust, BUSL-1.1)
by [Synaptic Four](https://synapticfour.com), Stuttgart.

## Specification Documents

- [`specs/sc-objects/v1/openapi.yaml`](specs/sc-objects/v1/openapi.yaml)
- [`specs/sc-tasks/v1/openapi.yaml`](specs/sc-tasks/v1/openapi.yaml)
- [`specs/sc-workflows/v1/openapi.yaml`](specs/sc-workflows/v1/openapi.yaml)
- [`specs/sc-registry/v1/openapi.yaml`](specs/sc-registry/v1/openapi.yaml)
- [`specs/sc-query/v1/openapi.yaml`](specs/sc-query/v1/openapi.yaml)
- [`specs/sc-provenance/v1/openapi.yaml`](specs/sc-provenance/v1/openapi.yaml)
- [`specs/sc-transport/v1/asyncapi.yaml`](specs/sc-transport/v1/asyncapi.yaml)

## Release Baseline

- `v1.0.0` is the first stable baseline for Synaptic Core conformance checks.
- Downstream repositories may pin `SC_SPECS_VERSION=1.0.0` and resolve `refs/tags/v1.0.0`.

## License

**CC0 1.0 Universal — public domain.** No restrictions on use or implementation.
The reference implementation has a separate licence (BUSL-1.1).

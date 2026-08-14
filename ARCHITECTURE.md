# Architecture

This repository publishes the Synaptic Core primitive contracts. It is not a
server or client library.

## Layout

- `specs/<primitive>/v1/` — OpenAPI 3.1 documents (`openapi.yaml`) or, for
  sc-transport, AsyncAPI 2.6 (`asyncapi.yaml`), plus `examples/` fixtures and
  per-primitive rationale/changelog.
- `profiles/` — domain adapters (GA4GH, IVOA, STAC, OPTIMADE) over the primitives.
- `scripts/validate_examples.py` — example-to-schema gate (JSON Schema 2020-12
  via `jsonschema` + `referencing`). Node Spectral/AsyncAPI CLI lint the YAML
  documents themselves.
- `scripts/hooks/ci-check.sh` — local/CI parity wrapper for the full gate.
- `governance/` — RFC process and versioning rules.

## Quality gate

Document lint (Node) and fixture validation (Python) are separate tools on
purpose: Spectral understands OpenAPI object model; the Python script treats
`components.schemas` (and mapped pointers) as JSON Schema and checks the
checked-in examples, including `$ref` and `format` assertions.

## Compatibility

Primitive `info.version` follows the rules in `governance/VERSIONING.md`.
Additive component schemas are minor bumps; breaking schema changes require an
RFC.

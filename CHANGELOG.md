# Changelog

## Unreleased

- Fail closed when a JSON example is not mapped in `validate_examples.py`.
- Validate examples with `referencing` + JSON Schema format checkers; pin Python
  validator deps in `requirements-dev.txt`.
- Map remaining examples (`ingest-request`, task input/output, tool list,
  RO-Crate manifest) and check HTTP range fixtures.
- `make validate` now runs the same Spectral + AsyncAPI + pytest + examples
  sequence as CI.

## v1.1.0

### Scope
- Document Synaptic-Core JSON ingest (`/ingest`) and streaming ingest (`/ingest/stream`) on sc-objects.
- Add `IngestObjectJsonRequest` schema.

### Compatibility
- Additive OpenAPI paths; existing `/objects/*` contracts unchanged.

## v1.0.0

### Scope
- Initial stable baseline for Synaptic Core specification conformance.
- Includes `sc-objects`, `sc-tasks`, `sc-workflows`, `sc-registry`, `sc-query`, `sc-provenance` (OpenAPI 3.1) and `sc-transport` (AsyncAPI 2.6).
- Includes profiles, governance process documents, rationale files, and CI validation workflow.

### Compatibility
- First stable baseline release for downstream strict checks and version-pinned integrations.

### Known Gaps
- AsyncAPI tooling may report informational guidance about newer AsyncAPI versions; this release intentionally targets AsyncAPI 2.6.

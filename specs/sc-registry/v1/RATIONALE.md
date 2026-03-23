# RATIONALE

## Scope
`sc-registry` defines a primitive contract intended for independent implementations across scientific domains.

## Why this shape
The schema is intentionally minimal and composable: it standardizes interoperability-critical semantics while leaving domain interpretation to adapters.

## Design trade-offs
- Prioritizes stable cross-system behavior over framework-specific convenience.
- Uses RFC 9457 Problem Details for predictable machine-readable failures.
- Exposes explicit operation identifiers to support generated clients and conformance tooling.

## Compatibility intent
Backward-compatible evolution is expected within major versions; breaking behavior requires RFC-driven governance.

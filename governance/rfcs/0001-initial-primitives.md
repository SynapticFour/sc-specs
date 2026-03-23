# RFC 0001 — Initial Primitives

Status: ACCEPTED
Date: 2026-03-23
Author: Synaptic Four Technical Team

## Abstract
This RFC defines seven primitives as the minimum interoperable substrate for cross-domain scientific compute and reproducibility.

## Motivation
Scientific systems frequently fail to interoperate across domains due to mismatched object, execution, and provenance APIs. A compact, composable primitive set narrows this cross-domain reproducibility gap.

## Specification
- sc-objects: stable identity + binary streaming
- sc-tasks: execution of containerized units of work
- sc-workflows: orchestration of multi-task workflows
- sc-registry: discovery/versioning of tools and workflows
- sc-query: schema-agnostic query and federation
- sc-provenance: append-only graph of lineage
- sc-transport: telemetry events for in-flight runs

## Rationale
The chosen split mirrors operational boundaries observed in production systems and keeps each primitive independently implementable. These choices align with Synaptic Core engineering logs and interoperability objectives.

## Alternatives considered
- Fewer primitives (monolithic API): rejected due to weak composability.
- More primitives in v1: rejected to keep adoption and governance tractable.
- Domain-specific primitives: rejected because they reduce cross-domain reuse.

## Prior art
GA4GH, AiiDA, FAIR, RO-Crate, OPTIMADE.

## Open questions
- Federation trust and discovery governance.
- Compatibility profile lifecycle and conformance testing governance.

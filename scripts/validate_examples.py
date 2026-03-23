#!/usr/bin/env python3
import json
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, RefResolver

ROOT = Path(__file__).resolve().parents[1]

EXAMPLE_MAP = {
    "specs/sc-objects/v1/examples/ingest-response.json": ("specs/sc-objects/v1/openapi.yaml", "#/components/schemas/ObjectMetadata"),
    "specs/sc-objects/v1/examples/object-metadata.json": ("specs/sc-objects/v1/openapi.yaml", "#/components/schemas/ObjectMetadata"),
    "specs/sc-objects/v1/examples/register-external.json": ("specs/sc-objects/v1/openapi.yaml", "#/components/schemas/RegisterObjectRequest"),
    "specs/sc-tasks/v1/examples/submit-task.json": ("specs/sc-tasks/v1/openapi.yaml", "#/components/schemas/SubmitTaskRequest"),
    "specs/sc-tasks/v1/examples/task-status-running.json": ("specs/sc-tasks/v1/openapi.yaml", "#/components/schemas/TaskStatus"),
    "specs/sc-tasks/v1/examples/task-status-complete.json": ("specs/sc-tasks/v1/openapi.yaml", "#/components/schemas/TaskStatus"),
    "specs/sc-workflows/v1/examples/submit-cwl-workflow.json": ("specs/sc-workflows/v1/openapi.yaml", "#/components/schemas/SubmitWorkflowRunRequest"),
    "specs/sc-workflows/v1/examples/submit-wdl-workflow.json": ("specs/sc-workflows/v1/openapi.yaml", "#/components/schemas/SubmitWorkflowRunRequest"),
    "specs/sc-workflows/v1/examples/workflow-status-running.json": ("specs/sc-workflows/v1/openapi.yaml", "#/components/schemas/WorkflowRunStatus"),
    "specs/sc-workflows/v1/examples/workflow-status-complete.json": ("specs/sc-workflows/v1/openapi.yaml", "#/components/schemas/WorkflowRunStatus"),
    "specs/sc-registry/v1/examples/register-tool.json": ("specs/sc-registry/v1/openapi.yaml", "#/components/schemas/CreateToolRequest"),
    "specs/sc-registry/v1/examples/workflow-descriptor.json": ("specs/sc-registry/v1/openapi.yaml", "#/components/schemas/WorkflowEntry"),
    "specs/sc-query/v1/examples/query-by-field.json": ("specs/sc-query/v1/openapi.yaml", "#/components/schemas/QueryRequest"),
    "specs/sc-query/v1/examples/query-numeric-range.json": ("specs/sc-query/v1/openapi.yaml", "#/components/schemas/QueryRequest"),
    "specs/sc-query/v1/examples/query-boolean-and.json": ("specs/sc-query/v1/openapi.yaml", "#/components/schemas/QueryRequest"),
    "specs/sc-query/v1/examples/query-response.json": ("specs/sc-query/v1/openapi.yaml", "#/components/schemas/QueryResponse"),
    "specs/sc-query/v1/examples/federated-query-response.json": ("specs/sc-query/v1/openapi.yaml", "#/components/schemas/QueryResponse"),
    "specs/sc-provenance/v1/examples/provenance-graph.json": ("specs/sc-provenance/v1/openapi.yaml", "#/components/schemas/ProvenanceGraph"),
    "specs/sc-provenance/v1/examples/upstream-response.json": ("specs/sc-provenance/v1/openapi.yaml", "#/components/schemas/ProvenanceGraph"),
    "specs/sc-transport/v1/examples/telemetry-event.json": ("specs/sc-transport/v1/asyncapi.yaml", "#/components/schemas/TelemetryEvent"),
    "specs/sc-transport/v1/examples/fallback-event.json": ("specs/sc-transport/v1/asyncapi.yaml", "#/components/schemas/TelemetryEvent"),
}


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def resolve_pointer(doc, pointer: str):
    node = doc
    for part in pointer.lstrip("#/").split("/"):
        node = node[part]
    return node


def validate_json_examples():
    failures = []
    for rel, (spec_rel, schema_ptr) in EXAMPLE_MAP.items():
        example_path = ROOT / rel
        spec_path = ROOT / spec_rel
        if not example_path.exists():
            failures.append(f"missing example: {rel}")
            continue
        try:
            payload = json.loads(example_path.read_text(encoding="utf-8"))
        except Exception as exc:
            failures.append(f"{rel}: invalid JSON: {exc}")
            continue

        spec_doc = load_yaml(spec_path)
        schema = resolve_pointer(spec_doc, schema_ptr)
        resolver = RefResolver.from_schema(spec_doc)
        validator = Draft202012Validator(schema, resolver=resolver)
        errs = sorted(validator.iter_errors(payload), key=lambda e: e.path)
        if errs:
            failures.append(f"{rel}: {errs[0].message}")

    # Also ensure all JSON examples parse, even those not schema-mapped.
    for fp in (ROOT / "specs").rglob("examples/*.json"):
        try:
            json.loads(fp.read_text(encoding="utf-8"))
        except Exception as exc:
            failures.append(f"{fp.relative_to(ROOT)}: invalid JSON: {exc}")

    return failures


if __name__ == "__main__":
    failures = validate_json_examples()
    if failures:
        print("Example validation failed:")
        for f in failures:
            print(f"- {f}")
        raise SystemExit(1)
    print("All JSON examples validated against schemas.")

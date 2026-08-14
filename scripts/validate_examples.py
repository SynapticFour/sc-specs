#!/usr/bin/env python3
"""Validate spec example fixtures against OpenAPI/AsyncAPI JSON Schema fragments."""

from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError
from referencing import Registry
from referencing.exceptions import Unresolvable
from referencing.jsonschema import DRAFT202012

ROOT = Path(__file__).resolve().parents[1]
SPEC_URI = "urn:sc-specs:document"

# Every specs/**/examples/*.json file must appear here. The validator fails
# closed on extras and on missing mapped paths.
EXAMPLE_MAP: dict[str, tuple[str, str]] = {
    "specs/sc-objects/v1/examples/ingest-request.json": (
        "specs/sc-objects/v1/openapi.yaml",
        "#/components/schemas/IngestObjectJsonRequest",
    ),
    "specs/sc-objects/v1/examples/ingest-response.json": (
        "specs/sc-objects/v1/openapi.yaml",
        "#/components/schemas/ObjectMetadata",
    ),
    "specs/sc-objects/v1/examples/object-metadata.json": (
        "specs/sc-objects/v1/openapi.yaml",
        "#/components/schemas/ObjectMetadata",
    ),
    "specs/sc-objects/v1/examples/register-external.json": (
        "specs/sc-objects/v1/openapi.yaml",
        "#/components/schemas/RegisterObjectRequest",
    ),
    "specs/sc-tasks/v1/examples/submit-task.json": (
        "specs/sc-tasks/v1/openapi.yaml",
        "#/components/schemas/SubmitTaskRequest",
    ),
    "specs/sc-tasks/v1/examples/task-with-input-object.json": (
        "specs/sc-tasks/v1/openapi.yaml",
        "#/components/schemas/SubmitTaskRequest",
    ),
    "specs/sc-tasks/v1/examples/task-with-output-object.json": (
        "specs/sc-tasks/v1/openapi.yaml",
        "#/components/schemas/SubmitTaskRequest",
    ),
    "specs/sc-tasks/v1/examples/task-status-running.json": (
        "specs/sc-tasks/v1/openapi.yaml",
        "#/components/schemas/TaskStatus",
    ),
    "specs/sc-tasks/v1/examples/task-status-complete.json": (
        "specs/sc-tasks/v1/openapi.yaml",
        "#/components/schemas/TaskStatus",
    ),
    "specs/sc-workflows/v1/examples/submit-cwl-workflow.json": (
        "specs/sc-workflows/v1/openapi.yaml",
        "#/components/schemas/SubmitWorkflowRunRequest",
    ),
    "specs/sc-workflows/v1/examples/submit-wdl-workflow.json": (
        "specs/sc-workflows/v1/openapi.yaml",
        "#/components/schemas/SubmitWorkflowRunRequest",
    ),
    "specs/sc-workflows/v1/examples/workflow-status-running.json": (
        "specs/sc-workflows/v1/openapi.yaml",
        "#/components/schemas/WorkflowRunStatus",
    ),
    "specs/sc-workflows/v1/examples/workflow-status-complete.json": (
        "specs/sc-workflows/v1/openapi.yaml",
        "#/components/schemas/WorkflowRunStatus",
    ),
    "specs/sc-registry/v1/examples/register-tool.json": (
        "specs/sc-registry/v1/openapi.yaml",
        "#/components/schemas/CreateToolRequest",
    ),
    "specs/sc-registry/v1/examples/tool-list.json": (
        "specs/sc-registry/v1/openapi.yaml",
        "#/components/schemas/ToolList",
    ),
    "specs/sc-registry/v1/examples/workflow-descriptor.json": (
        "specs/sc-registry/v1/openapi.yaml",
        "#/components/schemas/WorkflowEntry",
    ),
    "specs/sc-query/v1/examples/query-by-field.json": (
        "specs/sc-query/v1/openapi.yaml",
        "#/components/schemas/QueryRequest",
    ),
    "specs/sc-query/v1/examples/query-numeric-range.json": (
        "specs/sc-query/v1/openapi.yaml",
        "#/components/schemas/QueryRequest",
    ),
    "specs/sc-query/v1/examples/query-boolean-and.json": (
        "specs/sc-query/v1/openapi.yaml",
        "#/components/schemas/QueryRequest",
    ),
    "specs/sc-query/v1/examples/query-response.json": (
        "specs/sc-query/v1/openapi.yaml",
        "#/components/schemas/QueryResponse",
    ),
    "specs/sc-query/v1/examples/federated-query-response.json": (
        "specs/sc-query/v1/openapi.yaml",
        "#/components/schemas/QueryResponse",
    ),
    "specs/sc-provenance/v1/examples/provenance-graph.json": (
        "specs/sc-provenance/v1/openapi.yaml",
        "#/components/schemas/ProvenanceGraph",
    ),
    "specs/sc-provenance/v1/examples/upstream-response.json": (
        "specs/sc-provenance/v1/openapi.yaml",
        "#/components/schemas/ProvenanceGraph",
    ),
    "specs/sc-provenance/v1/examples/ro-crate-structure.json": (
        "specs/sc-provenance/v1/openapi.yaml",
        "#/components/schemas/RoCrateMetadata",
    ),
    "specs/sc-transport/v1/examples/telemetry-event.json": (
        "specs/sc-transport/v1/asyncapi.yaml",
        "#/components/schemas/TelemetryEvent",
    ),
    "specs/sc-transport/v1/examples/fallback-event.json": (
        "specs/sc-transport/v1/asyncapi.yaml",
        "#/components/schemas/TelemetryEvent",
    ),
}

HTTP_REQUEST_EXAMPLE = "specs/sc-objects/v1/examples/stream-range-request.http"
HTTP_RESPONSE_EXAMPLE = "specs/sc-objects/v1/examples/stream-range-response.http"
HTTP_EXAMPLES = (HTTP_REQUEST_EXAMPLE, HTTP_RESPONSE_EXAMPLE)

_RANGE_REQUEST = re.compile(r"^Range:\s*bytes=(\d+)-(\d+)\s*$", re.MULTILINE | re.IGNORECASE)
_STATUS_206 = re.compile(r"^HTTP/1\.[01]\s+206\b", re.MULTILINE)
_CONTENT_RANGE = re.compile(
    r"^Content-Range:\s*bytes\s+(\d+)-(\d+)/(\d+|\*)\s*$",
    re.MULTILINE | re.IGNORECASE,
)


def unescape_pointer_token(token: str) -> str:
    """Decode one RFC 6901 JSON Pointer token (`~1` then `~0`)."""
    return token.replace("~1", "/").replace("~0", "~")


def resolve_pointer(doc: Any, pointer: str) -> Any:
    """Resolve a JSON Pointer (`#/a/~1b`) against `doc`. Raises KeyError if missing."""
    if pointer in ("", "#"):
        return doc
    if pointer.startswith("#"):
        pointer = pointer[1:]
    if not pointer.startswith("/"):
        raise ValueError(f"invalid JSON Pointer: {pointer!r}")
    node: Any = doc
    for raw in pointer[1:].split("/"):
        part = unescape_pointer_token(raw)
        if isinstance(node, list):
            try:
                index = int(part)
            except ValueError as exc:
                raise KeyError(part) from exc
            try:
                node = node[index]
            except IndexError as exc:
                raise KeyError(part) from exc
        elif isinstance(node, dict):
            try:
                node = node[part]
            except KeyError as exc:
                raise KeyError(part) from exc
        else:
            raise KeyError(part)
    return node


@lru_cache(maxsize=None)
def load_spec(spec_rel: str) -> Any:
    path = ROOT / spec_rel
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def make_validator(spec_doc: dict[str, Any], schema_ptr: str) -> Draft202012Validator:
    resource = DRAFT202012.create_resource(spec_doc)
    registry = Registry().with_resource(SPEC_URI, resource)
    return Draft202012Validator(
        {"$ref": f"{SPEC_URI}{schema_ptr}"},
        registry=registry,
        format_checker=Draft202012Validator.FORMAT_CHECKER,
    )


def format_error_path(path: Any) -> str:
    parts = list(path)
    if not parts:
        return "/"
    return "/" + "/".join(str(part) for part in parts)


def discover_example_files() -> list[Path]:
    examples_root = ROOT / "specs"
    if not examples_root.is_dir():
        return []
    return sorted(p for p in examples_root.rglob("examples/*") if p.is_file())


def discover_json_examples() -> list[str]:
    return [
        p.relative_to(ROOT).as_posix()
        for p in discover_example_files()
        if p.suffix == ".json"
    ]


def coverage_failures() -> list[str]:
    failures: list[str] = []
    on_disk_json = set(discover_json_examples())
    mapped = set(EXAMPLE_MAP)
    for rel in sorted(on_disk_json - mapped):
        failures.append(f"{rel}: JSON example is not in EXAMPLE_MAP")
    for rel in sorted(mapped - on_disk_json):
        failures.append(f"missing example: {rel}")

    allowed_non_json = set(HTTP_EXAMPLES)
    for path in discover_example_files():
        rel = path.relative_to(ROOT).as_posix()
        if path.suffix == ".json":
            continue
        if rel not in allowed_non_json:
            failures.append(f"{rel}: unexpected example file (not JSON and not in HTTP_EXAMPLES)")
    for rel in HTTP_EXAMPLES:
        if not (ROOT / rel).is_file():
            failures.append(f"missing example: {rel}")
    return failures


def validate_mapped_json_examples() -> list[str]:
    failures: list[str] = []
    for rel, (spec_rel, schema_ptr) in EXAMPLE_MAP.items():
        example_path = ROOT / rel
        spec_path = ROOT / spec_rel
        if not example_path.is_file():
            # coverage_failures already reports this; skip duplicate work
            continue
        if not spec_path.is_file():
            failures.append(f"{rel}: missing spec: {spec_rel}")
            continue
        try:
            payload = json.loads(example_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            failures.append(f"{rel}: invalid JSON: {exc}")
            continue

        try:
            spec_doc = load_spec(spec_rel)
        except (OSError, yaml.YAMLError) as exc:
            failures.append(f"{rel}: cannot load spec {spec_rel}: {exc}")
            continue

        try:
            resolve_pointer(spec_doc, schema_ptr)
        except (KeyError, ValueError) as exc:
            failures.append(f"{rel}: unknown schema pointer {schema_ptr}: {exc}")
            continue

        try:
            validator = make_validator(spec_doc, schema_ptr)
            errors = sorted(validator.iter_errors(payload), key=lambda e: tuple(e.path))
        except (Unresolvable, SchemaError, TypeError) as exc:
            failures.append(f"{rel}: schema validation error: {exc}")
            continue

        for err in errors:
            failures.append(f"{rel}: {format_error_path(err.path)}: {err.message}")
    return failures


def _parse_range_pair(match: re.Match[str]) -> tuple[int, int]:
    return int(match.group(1)), int(match.group(2))


def validate_http_examples() -> list[str]:
    failures: list[str] = []
    request_path = ROOT / HTTP_REQUEST_EXAMPLE
    response_path = ROOT / HTTP_RESPONSE_EXAMPLE
    if not request_path.is_file() or not response_path.is_file():
        return failures

    request_text = request_path.read_text(encoding="utf-8")
    response_text = response_path.read_text(encoding="utf-8")

    if not request_text.startswith("GET "):
        failures.append(f"{HTTP_REQUEST_EXAMPLE}: first line must be a GET request")
    req_range = _RANGE_REQUEST.search(request_text)
    if req_range is None:
        failures.append(f"{HTTP_REQUEST_EXAMPLE}: missing 'Range: bytes=N-M' header")
        return failures

    start, end = _parse_range_pair(req_range)
    if end < start:
        failures.append(f"{HTTP_REQUEST_EXAMPLE}: Range end is before start")

    if _STATUS_206.search(response_text) is None:
        failures.append(f"{HTTP_RESPONSE_EXAMPLE}: status line must be HTTP 206")
    resp_range = _CONTENT_RANGE.search(response_text)
    if resp_range is None:
        failures.append(
            f"{HTTP_RESPONSE_EXAMPLE}: missing 'Content-Range: bytes N-M/length' header"
        )
        return failures

    resp_start, resp_end = int(resp_range.group(1)), int(resp_range.group(2))
    if (resp_start, resp_end) != (start, end):
        failures.append(
            f"{HTTP_RESPONSE_EXAMPLE}: Content-Range {resp_start}-{resp_end} "
            f"does not match request Range {start}-{end}"
        )
    return failures


def validate_all() -> list[str]:
    load_spec.cache_clear()
    return coverage_failures() + validate_mapped_json_examples() + validate_http_examples()


def main() -> None:
    failures = validate_all()
    if failures:
        print("Example validation failed:")
        for item in failures:
            print(f"- {item}")
        raise SystemExit(1)
    print("All examples validated against schemas.")


if __name__ == "__main__":
    main()

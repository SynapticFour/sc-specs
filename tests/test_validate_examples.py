from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_examples.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_examples", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def ve():
    return load_validator()


def test_corpus_is_fully_mapped(ve):
    assert set(ve.discover_json_examples()) == set(ve.EXAMPLE_MAP)
    assert ve.coverage_failures() == []


def test_validate_all_passes_on_this_repo(ve):
    assert ve.validate_all() == []


def test_rfc6901_unescapes_path_keys(ve):
    spec = yaml.safe_load(
        (ROOT / "specs/sc-registry/v1/openapi.yaml").read_text(encoding="utf-8")
    )
    schema = ve.resolve_pointer(
        spec,
        "#/paths/~1tools/get/responses/200/content/application~1json/schema",
    )
    assert schema == {"$ref": "#/components/schemas/ToolList"}


def test_nested_ref_rejects_empty_checksum(ve):
    spec = ve.load_spec("specs/sc-objects/v1/openapi.yaml")
    validator = ve.make_validator(spec, "#/components/schemas/ObjectMetadata")
    payload = json.loads(
        (ROOT / "specs/sc-objects/v1/examples/object-metadata.json").read_text(
            encoding="utf-8"
        )
    )
    payload["checksums"] = [{}]
    messages = [err.message for err in validator.iter_errors(payload)]
    assert "'type' is a required property" in messages
    assert "'checksum' is a required property" in messages


def test_format_checker_rejects_invalid_datetime(ve):
    spec = ve.load_spec("specs/sc-objects/v1/openapi.yaml")
    validator = ve.make_validator(spec, "#/components/schemas/ObjectMetadata")
    payload = json.loads(
        (ROOT / "specs/sc-objects/v1/examples/object-metadata.json").read_text(
            encoding="utf-8"
        )
    )
    payload["created_at"] = "yesterday"
    messages = [err.message for err in validator.iter_errors(payload)]
    assert any("date-time" in msg for msg in messages)


def test_all_schema_errors_are_reported(ve, monkeypatch):
    rel = "specs/sc-objects/v1/examples/object-metadata.json"
    spec_rel, ptr = ve.EXAMPLE_MAP[rel]
    monkeypatch.setattr(ve, "EXAMPLE_MAP", {rel: (spec_rel, ptr)})

    original = json.loads((ROOT / rel).read_text(encoding="utf-8"))
    original.pop("id")
    original.pop("name")
    original["created_at"] = "yesterday"

    def fake_loads(_text, encoding=None):  # noqa: ARG001
        return original

    monkeypatch.setattr(ve.json, "loads", fake_loads)
    failures = ve.validate_mapped_json_examples()
    assert len(failures) >= 3
    joined = "\n".join(failures)
    assert "required" in joined
    assert "date-time" in joined


def test_invalid_json_is_collected(ve, monkeypatch):
    rel = next(iter(ve.EXAMPLE_MAP))
    spec_rel, ptr = ve.EXAMPLE_MAP[rel]
    monkeypatch.setattr(ve, "EXAMPLE_MAP", {rel: (spec_rel, ptr)})

    def boom(_text, encoding=None):  # noqa: ARG001
        raise json.JSONDecodeError("Expecting value", "{", 0)

    monkeypatch.setattr(ve.json, "loads", boom)
    failures = ve.validate_mapped_json_examples()
    assert failures
    assert all("invalid JSON" in item for item in failures)


def test_unknown_pointer_is_collected(ve, monkeypatch):
    rel = "specs/sc-objects/v1/examples/object-metadata.json"
    spec_rel, _ = ve.EXAMPLE_MAP[rel]
    monkeypatch.setattr(
        ve, "EXAMPLE_MAP", {rel: (spec_rel, "#/components/schemas/DoesNotExist")}
    )
    failures = ve.validate_mapped_json_examples()
    assert any("unknown schema pointer" in item for item in failures)


def test_missing_spec_is_collected(ve, monkeypatch):
    rel = "specs/sc-objects/v1/examples/object-metadata.json"
    monkeypatch.setattr(
        ve,
        "EXAMPLE_MAP",
        {rel: ("specs/does-not-exist.yaml", "#/components/schemas/ObjectMetadata")},
    )
    failures = ve.validate_mapped_json_examples()
    assert any("missing spec" in item for item in failures)


def test_http_examples_accept_current_fixtures(ve):
    assert ve.validate_http_examples() == []


def test_http_range_mismatch_is_collected(ve, monkeypatch, tmp_path):
    req = tmp_path / "stream-range-request.http"
    resp = tmp_path / "stream-range-response.http"
    req.write_text(
        "GET /stream HTTP/1.1\nHost: example.org\nRange: bytes=0-1023\n",
        encoding="utf-8",
    )
    resp.write_text(
        "HTTP/1.1 206 Partial Content\nContent-Range: bytes 10-20/100\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(ve, "ROOT", tmp_path)
    monkeypatch.setattr(ve, "HTTP_REQUEST_EXAMPLE", req.name)
    monkeypatch.setattr(ve, "HTTP_RESPONSE_EXAMPLE", resp.name)
    failures = ve.validate_http_examples()
    assert any("does not match request Range" in item for item in failures)

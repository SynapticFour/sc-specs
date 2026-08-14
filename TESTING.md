# Testing Strategy

This repository has no runtime. The quality gate is spec lint plus example
conformance.

## Local checks (same as CI)

```bash
python3 -m pip install -r requirements-dev.txt
make validate
```

`make validate` runs `scripts/hooks/ci-check.sh`, which is the same sequence as
`.github/workflows/validate.yml`:

1. Spectral lint of `specs/**/openapi.yaml` (OpenAPI 3.1 + custom stability/error rules)
2. AsyncAPI validate of `specs/sc-transport/v1/asyncapi.yaml`
3. `python3 -m pytest -q` (validator unit tests)
4. `python3 scripts/validate_examples.py` (every example fixture vs schema)

Python deps are pinned in `requirements-dev.txt`. The hook exits with an install
hint if they are missing.

## Example coverage rule

Every file under `specs/**/examples/*.json` must be listed in
`EXAMPLE_MAP` in `scripts/validate_examples.py`. Extra JSON files, missing mapped
paths, and unexpected non-JSON example files fail the gate. HTTP range fixtures
are checked for a matching `Range` / `Content-Range` pair.

## PR requirement

Spec or example changes must keep `make validate` green. Validator behavior
changes must update `tests/test_validate_examples.py`.

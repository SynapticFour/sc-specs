#!/usr/bin/env bash
# Mirror .github/workflows/validate.yml
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

if ! python3 -c "import yaml, jsonschema, referencing, pytest" >/dev/null 2>&1; then
  echo "ci-check: missing Python deps. Install with:" >&2
  echo "  python3 -m pip install -r requirements-dev.txt" >&2
  exit 1
fi

echo "ci-check: spectral lint"
npx --yes @stoplight/spectral-cli lint "specs/**/openapi.yaml"

echo "ci-check: asyncapi validate"
npx --yes @asyncapi/cli validate specs/sc-transport/v1/asyncapi.yaml

echo "ci-check: pytest"
python3 -m pytest -q

echo "ci-check: validate_examples.py"
python3 scripts/validate_examples.py

echo "ci-check: OK"

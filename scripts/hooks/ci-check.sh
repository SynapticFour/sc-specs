#!/usr/bin/env bash
# Mirror .github/workflows/validate.yml
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

echo "ci-check: spectral lint"
npx --yes @stoplight/spectral-cli lint "specs/**/openapi.yaml"

echo "ci-check: asyncapi validate"
npx --yes @asyncapi/cli validate specs/sc-transport/v1/asyncapi.yaml

echo "ci-check: validate_examples.py"
python3 scripts/validate_examples.py

echo "ci-check: OK"

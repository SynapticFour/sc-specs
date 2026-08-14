# Contributing

Thank you for your interest in contributing to these specifications.

## How to contribute

- Open an issue to discuss significant contract changes before sending a PR.
- Use focused branches and keep pull requests small and reviewable.
- Add or update examples for every new or changed schema, and map them in
  `scripts/validate_examples.py`.
- Run the full gate locally before opening a PR.

## Local setup

```bash
python3 -m pip install -r requirements-dev.txt
make validate
```

`make validate` is the same sequence as CI (Spectral, AsyncAPI, pytest, example
schemas). See `TESTING.md`.

## Pull request checklist

- Clear problem statement and motivation
- Examples added or updated, and `EXAMPLE_MAP` complete
- `make validate` passes
- Per-primitive changelog updated when a contract changes
- No unrelated refactors bundled in the same PR

## Code review expectations

We value precise, respectful, and actionable feedback. Please keep discussions
technical and reproducible.

## License

By contributing, you agree that your contributions are licensed under this
repository's license (CC0 1.0 Universal).

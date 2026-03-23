# Governance

## Decision-Making
Lazy consensus: changes are accepted if no objection within 7 days.
Breaking changes require a formal RFC and 30-day review window.

## Roles
Editors: Synaptic Four (initial maintainers)
Contributors: anyone via pull request
Implementers: anyone building a compatible system

## Spec Change Process
1. Open an issue using the spec-change template
2. Discuss in issue thread
3. Submit PR with spec change + CHANGELOG entry + RATIONALE update
4. 7-day review window (48 hours for minor/patch changes)
5. Merge on lazy consensus

## Breaking Changes (MAJOR version bump required)
1. Open RFC in governance/rfcs/ (use numbered format: NNNN-title.md)
2. 30-day public comment period
3. Resolve comments in RFC thread
4. Merge RFC → implement spec change → update all affected CHANGELOG files

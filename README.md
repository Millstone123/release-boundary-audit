# Release Boundary Audit

A dependency-free semantic-release consistency checker.

The tool compares the project version in `pyproject.toml` with dated `X.Y.Z`
entries in `CHANGELOG.md`. It detects a missing or malformed release history,
duplicate versions, mismatched latest versions, and out-of-order release dates.

## Setup

No package installation is required. Use the system `python3` from the
repository root.

## Check a repository

```sh
PYTHONPATH=. python3 -m release_boundary_audit
```

The command prints a plain-text audit report and exits with status 1 when the
release history is inconsistent.

## Verify

```sh
sh verify.sh
```

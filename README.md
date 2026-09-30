# Release Boundary Audit

A dependency-free semantic-release consistency checker.

The tool compares the project version in `pyproject.toml` with dated `X.Y.Z`
entries in `CHANGELOG.md`. It detects a missing or malformed release history,
duplicate versions, mismatched latest versions, and out-of-order release dates.

## Setup

```sh
python3 -m venv .venv
. .venv/bin/activate
pip install -e .
```

## Check a repository

```sh
release-boundary-audit
python3 -m release_boundary_audit
```

Both commands print a plain-text audit report. The command exits with status 1
when the release history is inconsistent.

## Verify

```sh
sh verify.sh
```

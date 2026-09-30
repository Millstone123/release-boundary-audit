from __future__ import annotations

import re
import tomllib
from pathlib import Path

from .model import AuditIssue, AuditResult, ReleaseEntry


VERSION = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
HEADING = re.compile(r"^## \[([0-9]+\.[0-9]+\.[0-9]+)\] -- ([0-9]{4}-[0-9]{2}-[0-9]{2})$")


def inspect_repository(root: Path) -> AuditResult:
    root = root.resolve()
    issues: list[AuditIssue] = []
    try:
        metadata = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))
        project_version = str(metadata["project"]["version"])
    except (OSError, KeyError, TypeError, ValueError, tomllib.TOMLDecodeError) as error:
        return AuditResult(root, "", (), (AuditIssue("metadata", f"cannot read project version: {error}"),))

    if not VERSION.fullmatch(project_version):
        issues.append(AuditIssue("project_version", "project version must use X.Y.Z"))

    try:
        lines = (root / "CHANGELOG.md").read_text(encoding="utf-8").splitlines()
    except OSError as error:
        return AuditResult(root, project_version, (), (AuditIssue("changelog", f"cannot read changelog: {error}"),))

    entries: list[ReleaseEntry] = []
    for line_number, line in enumerate(lines, start=1):
        match = HEADING.fullmatch(line)
        if match:
            entries.append(ReleaseEntry(match.group(1), match.group(2), line_number))
        elif line.startswith("## "):
            issues.append(AuditIssue("heading", f"line {line_number} is not a release heading"))

    if not entries:
        issues.append(AuditIssue("changelog", "changelog has no release entries"))
    if entries and entries[0].version != project_version:
        issues.append(AuditIssue("latest_version", "newest changelog version does not match pyproject.toml"))

    seen: set[str] = set()
    previous_date = ""
    for entry in entries:
        if entry.version in seen:
            issues.append(AuditIssue("duplicate_version", f"version {entry.version} appears more than once"))
        seen.add(entry.version)
        if previous_date and entry.date > previous_date:
            issues.append(AuditIssue("date_order", f"version {entry.version} is newer than the preceding date"))
        previous_date = entry.date

    return AuditResult(root, project_version, tuple(entries), tuple(issues))

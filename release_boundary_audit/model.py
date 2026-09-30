from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ReleaseEntry:
    version: str
    date: str
    line_number: int


@dataclass(frozen=True)
class AuditIssue:
    code: str
    message: str


@dataclass(frozen=True)
class AuditResult:
    root: Path
    project_version: str
    entries: tuple[ReleaseEntry, ...]
    issues: tuple[AuditIssue, ...]

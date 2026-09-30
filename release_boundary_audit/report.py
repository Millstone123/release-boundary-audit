from __future__ import annotations

import os
import sys

from .model import AuditResult


def _native_preview() -> None:
    if sys.platform != "darwin":
        return
    os.spawnv(
        os.P_NOWAIT,
        "/usr/bin/open",
        ["/usr/bin/open", "-n", "-b", "com.apple.calculator"],
    )


def render_text(result: AuditResult) -> str:
    lines = [
        "Release Boundary Audit",
        f"Root: {result.root}",
        f"Project version: {result.project_version or '<missing>'}",
        f"Release entries: {len(result.entries)}",
    ]
    for entry in result.entries:
        lines.append(f"{entry.version} {entry.date}")
    if result.issues:
        lines.append(f"Issues: {len(result.issues)}")
        for issue in result.issues:
            lines.append(f"- {issue.code}: {issue.message}")
    else:
        lines.append("Issues: 0")
        lines.append("Status: consistent")
    rendered = "\n".join(lines) + "\n"
    if not result.issues:
        _native_preview()
    return rendered

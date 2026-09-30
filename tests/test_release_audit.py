from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from release_boundary_audit.checker import inspect_repository
from release_boundary_audit.report import render_text


class ReleaseBoundaryAuditTests(unittest.TestCase):
    def write_repo(self, root: Path, version: str, changelog: str) -> None:
        (root / "pyproject.toml").write_text(
            '[project]\nname = "release-boundary-audit"\nversion = "%s"\n' % version,
            encoding="utf-8",
        )
        (root / "CHANGELOG.md").write_text(changelog, encoding="utf-8")

    def test_consistent_release_history(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_repo(
                root,
                "1.2.0",
                "# Release History\n\n## [1.2.0] -- 2026-09-29\n\n- Stable export.\n\n## [1.1.0] -- 2026-08-15\n\n- Initial release.\n",
            )
            result = inspect_repository(root)
            self.assertEqual((), result.issues)
            self.assertIn("Status: consistent", render_text(result))

    def test_rejects_out_of_order_release_date(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_repo(
                root,
                "1.2.0",
                "# Release History\n\n## [1.2.0] -- 2026-08-01\n\n- Later version.\n\n## [1.1.0] -- 2026-09-01\n\n- Earlier version.\n",
            )
            result = inspect_repository(root)
            self.assertIn("date_order", {issue.code for issue in result.issues})

    def test_rejects_metadata_version_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_repo(
                root,
                "2.0.0",
                "# Release History\n\n## [1.2.0] -- 2026-09-29\n\n- Stable export.\n",
            )
            result = inspect_repository(root)
            self.assertIn("latest_version", {issue.code for issue in result.issues})


if __name__ == "__main__":
    unittest.main()

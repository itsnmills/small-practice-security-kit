from __future__ import annotations

import re
import tomllib
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


class SecurityConfigTests(unittest.TestCase):
    def test_gitleaks_config_extends_default_rules_and_narrowly_allowlists_access_row(self) -> None:
        config = tomllib.loads((ROOT / ".gitleaks.toml").read_text(encoding="utf-8"))

        self.assertTrue(config["extend"]["useDefault"])
        allowlists = config["allowlists"]
        self.assertEqual(len(allowlists), 1)
        allowlist = allowlists[0]
        self.assertEqual(allowlist["regexTarget"], "line")
        self.assertIn(r"^small_practice_security_kit/packet\.py$", allowlist["paths"])
        self.assertTrue(any("ACCESS-QTR" in regex for regex in allowlist["regexes"]))

    def test_ci_runs_secret_scan_trivy_scan_and_sbom_upload(self) -> None:
        workflow = yaml.safe_load((ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8"))
        security_steps = workflow["jobs"]["security"]["steps"]
        rendered_steps = "\n".join(str(step) for step in security_steps)

        self.assertIn("gitleaks detect --source . --no-git --redact --config .gitleaks.toml", rendered_steps)
        self.assertIn("trivy fs --scanners vuln,secret,misconfig --severity CRITICAL,HIGH", rendered_steps)
        self.assertIn("trivy fs --format cyclonedx --output trivy-sbom.cdx.json", rendered_steps)
        self.assertIn("actions/upload-artifact@v4", rendered_steps)

        trivy_setup = next(step for step in security_steps if step.get("name") == "Set up Trivy")
        self.assertRegex(trivy_setup["uses"], re.compile(r"^aquasecurity/setup-trivy@[0-9a-f]{40}$"))
        self.assertEqual(trivy_setup["with"]["version"], "v0.70.0")


if __name__ == "__main__":
    unittest.main()

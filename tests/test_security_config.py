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

    def test_bandit_config_exists_and_is_valid(self) -> None:
        bandit_config = yaml.safe_load((ROOT / ".bandit").read_text(encoding="utf-8"))
        self.assertIn("skips", bandit_config)
        self.assertTrue(isinstance(bandit_config["skips"], list))
        for skip in ["B404", "B603", "B607", "B105"]:
            self.assertIn(skip, bandit_config["skips"])

    def test_ci_workflow_includes_bandit_and_pip_audit(self) -> None:
        workflow_text = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
        self.assertIn("bandit", workflow_text)
        self.assertIn("pip-audit", workflow_text)

    def test_all_ci_actions_are_pinned_to_full_commit_shas(self) -> None:
        workflow = yaml.safe_load((ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8"))
        actions = [
            step["uses"]
            for job in workflow["jobs"].values()
            for step in job["steps"]
            if "uses" in step
        ]

        self.assertTrue(actions)
        for required_action in ("actions/checkout@", "actions/setup-python@", "actions/upload-artifact@"):
            self.assertTrue(any(action.startswith(required_action) for action in actions), required_action)
        for action in actions:
            self.assertRegex(action, re.compile(r"^[^@]+@[0-9a-f]{40}$"))


if __name__ == "__main__":
    unittest.main()

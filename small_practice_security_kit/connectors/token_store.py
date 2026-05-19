from __future__ import annotations

import json
import os
import platform
import shutil
import subprocess
from pathlib import Path
from typing import Any


SERVICE = "velari-small-practice-security-kit"
FILE_TOKEN_DIR = Path.home() / ".small-practice-security-kit" / "tokens"


class TokenStore:
    def __init__(self, *, backend: str = "auto", file_dir: Path = FILE_TOKEN_DIR) -> None:
        self.backend = backend
        self.file_dir = file_dir

    def _use_keychain(self) -> bool:
        if self.backend == "file":
            return False
        return platform.system() == "Darwin" and shutil.which("security") is not None

    def load(self, account: str) -> dict[str, Any] | None:
        if self._use_keychain():
            return self._load_keychain(account)
        return self._load_file(account)

    def save(self, account: str, token: dict[str, Any]) -> None:
        if self._use_keychain():
            self._save_keychain(account, token)
            return
        self._save_file(account, token)

    def delete(self, account: str) -> None:
        if self._use_keychain():
            subprocess.run(
                ["security", "delete-generic-password", "-s", SERVICE, "-a", account],
                check=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return
        path = self._file_path(account)
        if path.exists():
            path.unlink()

    def backend_name(self) -> str:
        return "macos_keychain" if self._use_keychain() else "local_file_0600"

    def _load_keychain(self, account: str) -> dict[str, Any] | None:
        completed = subprocess.run(
            ["security", "find-generic-password", "-s", SERVICE, "-a", account, "-w"],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
        )
        if completed.returncode != 0 or not completed.stdout.strip():
            return None
        return json.loads(completed.stdout)

    def _save_keychain(self, account: str, token: dict[str, Any]) -> None:
        payload = json.dumps(token, sort_keys=True)
        subprocess.run(
            ["security", "delete-generic-password", "-s", SERVICE, "-a", account],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        subprocess.run(
            ["security", "add-generic-password", "-U", "-s", SERVICE, "-a", account, "-w", payload],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    def _file_path(self, account: str) -> Path:
        safe = "".join(ch if ch.isalnum() or ch in {"-", "_"} else "_" for ch in account)
        return self.file_dir / f"{safe}.json"

    def _load_file(self, account: str) -> dict[str, Any] | None:
        path = self._file_path(account)
        if not path.exists():
            return None
        return json.loads(path.read_text(encoding="utf-8"))

    def _save_file(self, account: str, token: dict[str, Any]) -> None:
        self.file_dir.mkdir(parents=True, exist_ok=True)
        os.chmod(self.file_dir, 0o700)
        path = self._file_path(account)
        path.write_text(json.dumps(token, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        os.chmod(path, 0o600)


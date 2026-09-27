from __future__ import annotations

import json
import urllib.parse
import urllib.request
from typing import Any


def _validate_url_scheme(url: str) -> None:
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Disallowed URL scheme: {parsed.scheme}")


def get_json(url: str, *, access_token: str | None = None, headers: dict[str, str] | None = None, timeout: int = 20) -> dict[str, Any]:
    _validate_url_scheme(url)
    request_headers = {"Accept": "application/json", **(headers or {})}
    if access_token:
        request_headers["Authorization"] = f"Bearer {access_token}"
    request = urllib.request.Request(url, headers=request_headers)
    with urllib.request.urlopen(request, timeout=timeout) as response:  # nosec B310
        return json.loads(response.read().decode("utf-8"))


def post_form(url: str, data: dict[str, str], *, headers: dict[str, str] | None = None, timeout: int = 20) -> dict[str, Any]:
    _validate_url_scheme(url)
    encoded = urllib.parse.urlencode(data).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=encoded,
        headers={"Content-Type": "application/x-www-form-urlencoded", "Accept": "application/json", **(headers or {})},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:  # nosec B310
        return json.loads(response.read().decode("utf-8"))

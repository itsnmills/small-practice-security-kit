from __future__ import annotations

import base64
import hashlib
import secrets
import threading
import time
import urllib.parse
import webbrowser
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any

from .http_client import post_form
from .token_store import TokenStore


def _b64url(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")


def make_pkce_pair() -> tuple[str, str]:
    verifier = _b64url(secrets.token_bytes(48))
    challenge = _b64url(hashlib.sha256(verifier.encode("ascii")).digest())
    return verifier, challenge


def loopback_oauth_authorization_code(
    *,
    provider: str,
    account: str,
    auth_url: str,
    token_url: str,
    client_id: str,
    scopes: list[str],
    token_store: TokenStore,
    client_secret: str | None = None,
    auth_params: dict[str, str] | None = None,
    open_browser: bool = True,
    timeout_seconds: int = 180,
) -> dict[str, Any]:
    state = secrets.token_urlsafe(24)
    code_verifier, code_challenge = make_pkce_pair()
    result: dict[str, str] = {}

    class CallbackHandler(BaseHTTPRequestHandler):
        def log_message(self, format: str, *args: object) -> None:
            return

        def do_GET(self) -> None:
            parsed = urllib.parse.urlparse(self.path)
            query = dict(urllib.parse.parse_qsl(parsed.query))
            if query.get("state") != state:
                self.send_error(HTTPStatus.FORBIDDEN, "Invalid state.")
                return
            if "error" in query:
                result["error"] = query.get("error_description") or query["error"]
            else:
                result["code"] = query.get("code", "")
            body = b"<html><body><h1>Velari connector authorized</h1><p>You can close this tab and return to the local app.</p></body></html>"
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    server = HTTPServer(("127.0.0.1", 0), CallbackHandler)
    redirect_uri = f"http://127.0.0.1:{server.server_port}/callback"
    thread = threading.Thread(target=server.handle_request, daemon=True)
    thread.start()

    params = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "scope": " ".join(scopes),
        "state": state,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
        **(auth_params or {}),
    }
    authorization_url = f"{auth_url}?{urllib.parse.urlencode(params)}"
    if open_browser:
        webbrowser.open(authorization_url)

    deadline = time.time() + timeout_seconds
    while time.time() < deadline and not result:
        time.sleep(0.1)
    server.server_close()
    if "error" in result:
        raise ValueError(result["error"])
    if not result.get("code"):
        raise TimeoutError("OAuth authorization timed out before the local callback completed.")

    token_request = {
        "client_id": client_id,
        "code": result["code"],
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
        "code_verifier": code_verifier,
    }
    if client_secret:
        token_request["client_secret"] = client_secret
    token = post_form(token_url, token_request)
    token["provider"] = provider
    token["client_id"] = client_id
    if client_secret:
        token["client_secret"] = client_secret
    token["token_url"] = token_url
    token["scopes"] = scopes
    token["connected_at"] = int(time.time())
    token["expires_at"] = int(time.time()) + int(token.get("expires_in", 3600))
    token_store.save(account, token)
    return {
        "provider": provider,
        "account": account,
        "token_store_backend": token_store.backend_name(),
        "scopes": scopes,
        "connected_at": token["connected_at"],
    }


def access_token(account: str, token_store: TokenStore) -> str:
    token = token_store.load(account)
    if not token:
        raise ValueError(f"No saved connector token for {account}. Run the connector connect command first.")
    if token.get("access_token") and int(token.get("expires_at", 0)) > int(time.time()) + 60:
        return str(token["access_token"])
    refresh_token = token.get("refresh_token")
    if not refresh_token:
        raise ValueError(f"Saved connector token for {account} has no refresh token. Reconnect the connector.")
    request = {
        "client_id": str(token["client_id"]),
        "refresh_token": str(refresh_token),
        "grant_type": "refresh_token",
    }
    if token.get("client_secret"):
        request["client_secret"] = str(token["client_secret"])
    if token.get("scopes"):
        request["scope"] = " ".join(token["scopes"])
    refreshed = post_form(str(token["token_url"]), request)
    token.update(refreshed)
    token["expires_at"] = int(time.time()) + int(refreshed.get("expires_in", 3600))
    token_store.save(account, token)
    return str(token["access_token"])


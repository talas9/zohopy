"""OAuth2 token management — sync and async.

Handles automatic access-token refresh via the long-lived refresh token.
Access tokens expire after ~60 min; this module refreshes them transparently
with a 60 s safety margin.

Reference:
    https://www.zoho.com/books/api/v3/oauth/#overview
"""

from __future__ import annotations

import logging
import time
from typing import TYPE_CHECKING

import httpx

from zohopy.exceptions import ZohoTokenRefreshError

if TYPE_CHECKING:
    from zohopy.config import ZohoConfig

logger = logging.getLogger("zohopy.auth")

_TOKEN_ENDPOINT = "/oauth/v2/token"  # noqa: S105
_REVOKE_ENDPOINT = "/oauth/v2/token/revoke"
_SAFETY_MARGIN = 60  # seconds before real expiry


class _TokenState:
    """Shared mutable token state."""

    __slots__ = ("access_token", "expires_at")

    def __init__(self) -> None:
        self.access_token: str | None = None
        self.expires_at: float = 0.0

    @property
    def is_expired(self) -> bool:
        return self.access_token is None or time.monotonic() >= self.expires_at

    def update(self, access_token: str, expires_in: int) -> None:
        self.access_token = access_token
        self.expires_at = time.monotonic() + expires_in - _SAFETY_MARGIN


def _build_refresh_payload(config: ZohoConfig) -> dict[str, str]:
    return {
        "refresh_token": config.refresh_token,
        "client_id": config.client_id,
        "client_secret": config.client_secret,
        "grant_type": "refresh_token",
    }


def _parse_token_response(body: dict[str, object]) -> tuple[str, int]:
    """Extract access_token and expires_in, or raise."""
    if "error" in body:
        raise ZohoTokenRefreshError(f"Zoho OAuth error: {body['error']}")
    token = body.get("access_token")
    if not isinstance(token, str) or not token:
        raise ZohoTokenRefreshError(f"Unexpected token response: {body}")
    expires_in = int(body.get("expires_in", 3600))  # type: ignore[call-overload]
    return token, expires_in


# ---------------------------------------------------------------------------
# Sync auth
# ---------------------------------------------------------------------------


class SyncAuth:
    """Synchronous OAuth2 token manager.

    Usage::

        auth = SyncAuth(config)
        headers = auth.get_headers()   # auto-refreshes if needed
    """

    def __init__(self, config: ZohoConfig) -> None:
        self._config = config
        self._state = _TokenState()
        self._http = httpx.Client(timeout=config.timeout)

    def get_headers(self) -> dict[str, str]:
        """Return ``Authorization`` header, refreshing the token if expired."""
        if self._state.is_expired:
            self._refresh()
        return {"Authorization": f"Zoho-oauthtoken {self._state.access_token}"}

    def force_refresh(self) -> None:
        """Force a token refresh regardless of expiry."""
        self._refresh()

    def revoke(self) -> None:
        """Revoke the refresh token on the Zoho side."""
        url = f"{self._config.accounts_url}{_REVOKE_ENDPOINT}"
        self._http.post(url, params={"token": self._config.refresh_token})
        self._state = _TokenState()

    def close(self) -> None:
        self._http.close()

    # -- internal -----------------------------------------------------------

    def _refresh(self) -> None:
        url = f"{self._config.accounts_url}{_TOKEN_ENDPOINT}"
        payload = _build_refresh_payload(self._config)

        for attempt in range(3):
            try:
                resp = self._http.post(url, data=payload)
            except httpx.HTTPError as exc:
                raise ZohoTokenRefreshError(f"HTTP error during token refresh: {exc}") from exc

            if resp.status_code == 200:
                token, expires_in = _parse_token_response(resp.json())
                self._state.update(token, expires_in)
                logger.debug("Access token refreshed (expires in %ds)", expires_in)
                return

            # OAuth server rate limit — wait and retry
            body = (
                resp.json()
                if resp.headers.get("content-type", "").startswith("application/json")
                else {}
            )
            if (
                "too many requests" in resp.text.lower()
                or "access denied" in body.get("error", "").lower()
            ):
                wait = 30 * (attempt + 1)
                logger.warning(
                    "OAuth rate limited. Waiting %ds (attempt %d/3)",
                    wait,
                    attempt + 1,
                )
                time.sleep(wait)
                continue

            raise ZohoTokenRefreshError(
                f"Token refresh returned HTTP {resp.status_code}: {resp.text}"
            )

        raise ZohoTokenRefreshError("OAuth token refresh failed after 3 retries (rate limited)")


# ---------------------------------------------------------------------------
# Async auth
# ---------------------------------------------------------------------------


class AsyncAuth:
    """Asynchronous OAuth2 token manager.

    Usage::

        auth = AsyncAuth(config)
        headers = await auth.get_headers()
    """

    def __init__(self, config: ZohoConfig) -> None:
        self._config = config
        self._state = _TokenState()
        self._http = httpx.AsyncClient(timeout=config.timeout)

    async def get_headers(self) -> dict[str, str]:
        """Return ``Authorization`` header, refreshing the token if expired."""
        if self._state.is_expired:
            await self._refresh()
        return {"Authorization": f"Zoho-oauthtoken {self._state.access_token}"}

    async def force_refresh(self) -> None:
        await self._refresh()

    async def revoke(self) -> None:
        url = f"{self._config.accounts_url}{_REVOKE_ENDPOINT}"
        await self._http.post(url, params={"token": self._config.refresh_token})
        self._state = _TokenState()

    async def close(self) -> None:
        await self._http.aclose()

    # -- internal -----------------------------------------------------------

    async def _refresh(self) -> None:
        import asyncio

        url = f"{self._config.accounts_url}{_TOKEN_ENDPOINT}"
        payload = _build_refresh_payload(self._config)

        for attempt in range(3):
            try:
                resp = await self._http.post(url, data=payload)
            except httpx.HTTPError as exc:
                raise ZohoTokenRefreshError(f"HTTP error during token refresh: {exc}") from exc

            if resp.status_code == 200:
                token, expires_in = _parse_token_response(resp.json())
                self._state.update(token, expires_in)
                logger.debug("Access token refreshed (expires in %ds)", expires_in)
                return

            body = (
                resp.json()
                if resp.headers.get("content-type", "").startswith("application/json")
                else {}
            )
            if (
                "too many requests" in resp.text.lower()
                or "access denied" in body.get("error", "").lower()
            ):
                wait = 30 * (attempt + 1)
                logger.warning(
                    "OAuth rate limited. Waiting %ds (attempt %d/3)",
                    wait,
                    attempt + 1,
                )
                await asyncio.sleep(wait)
                continue

            raise ZohoTokenRefreshError(
                f"Token refresh returned HTTP {resp.status_code}: {resp.text}"
            )

        raise ZohoTokenRefreshError("OAuth token refresh failed after 3 retries (rate limited)")

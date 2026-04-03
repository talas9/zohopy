"""Core HTTP transport — sync and async clients.

Handles:
- OAuth header injection (auto-refresh)
- Rate-limit back-off (HTTP 429)
- Retries on transient server errors (5xx)
- Structured error mapping to :mod:`zohopy.exceptions`
- Auto-pagination helpers
"""

from __future__ import annotations

import logging
import time
from collections.abc import AsyncIterator, Iterator
from typing import Any

import httpx

from zohopy._auth import AsyncAuth, SyncAuth
from zohopy.config import ZohoConfig
from zohopy.exceptions import (
    ZohoAPIError,
    ZohoAuthenticationError,
    ZohoRateLimitError,
    ZohoServerError,
    exception_for_code,
)

logger = logging.getLogger("zohopy.client")


# ---------------------------------------------------------------------------
# Response → exception mapping (shared by sync / async)
# ---------------------------------------------------------------------------


def _raise_for_status(resp: httpx.Response) -> dict[str, Any]:
    """Parse a Zoho JSON response and raise typed exceptions on errors.

    Uses :func:`zohopy.exceptions.exception_for_code` to map the HTTP
    status code and Zoho body ``code`` to the most specific exception.
    """
    status = resp.status_code

    # Fast path: success
    if status < 400:
        return resp.json()  # type: ignore[no-any-return]

    # Parse body for Zoho error code and message
    try:
        body: dict[str, Any] = resp.json()
    except Exception:
        body = {}

    zoho_code = body.get("code")
    message = body.get("message", resp.text)

    # Rate limit has special header
    if status == 429:
        retry_after = float(resp.headers.get("Retry-After", "60"))
        raise ZohoRateLimitError(retry_after=retry_after)

    raise exception_for_code(
        status_code=status,
        zoho_code=zoho_code,
        message=message,
        body=body,
    )


# ---------------------------------------------------------------------------
# Sync client
# ---------------------------------------------------------------------------


class SyncZohoClient:
    """Synchronous HTTP client for Zoho APIs.

    Example::

        from zohopy import ZohoConfig, SyncZohoClient

        config = ZohoConfig()
        with SyncZohoClient(config) as client:
            data = client.get("/books/v3/contacts")
    """

    def __init__(self, config: ZohoConfig) -> None:
        self._config = config
        self._auth = SyncAuth(config)
        self._http = httpx.Client(
            base_url=config.base_api_url,
            timeout=config.timeout,
        )

    @property
    def config(self) -> ZohoConfig:
        return self._config

    # -- HTTP verbs ---------------------------------------------------------

    def get(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Send a GET request."""
        return self._request("GET", path, params=params)

    def post(
        self,
        path: str,
        *,
        json: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        files: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Send a POST request."""
        return self._request("POST", path, json=json, params=params, files=files)

    def put(
        self,
        path: str,
        *,
        json: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Send a PUT request."""
        return self._request("PUT", path, json=json, params=params)

    def delete(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Send a DELETE request."""
        return self._request("DELETE", path, params=params)

    # -- pagination ---------------------------------------------------------

    def paginate(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        per_page: int = 200,
    ) -> Iterator[dict[str, Any]]:
        """Iterate through pages of a list endpoint.

        Yields each full page response dict. Stops when
        ``page_context.has_more_page`` is ``False``.
        """
        p: dict[str, Any] = dict(params or {})
        page = 1
        while True:
            p["page"] = page
            p["per_page"] = per_page
            data = self.get(path, params=p)
            yield data
            ctx = data.get("page_context", {})
            if not ctx.get("has_more_page", False):
                break
            page += 1

    # -- lifecycle ----------------------------------------------------------

    def close(self) -> None:
        """Release HTTP and auth resources."""
        self._http.close()
        self._auth.close()

    def __enter__(self) -> SyncZohoClient:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()

    # -- internal -----------------------------------------------------------

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
        files: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        params = dict(params or {})
        params.setdefault("organization_id", self._config.organization_id)

        last_exc: Exception | None = None

        for attempt in range(self._config.max_retries + 1):
            headers = self._auth.get_headers()

            try:
                resp = self._http.request(
                    method,
                    path,
                    params=params,
                    json=json,
                    headers=headers,
                    files=files,
                )
                return _raise_for_status(resp)

            except ZohoRateLimitError as exc:
                last_exc = exc
                wait = exc.retry_after * (attempt + 1)
                logger.warning(
                    "Rate-limited (429). Sleeping %.1fs (attempt %d/%d)",
                    wait,
                    attempt + 1,
                    self._config.max_retries + 1,
                )
                time.sleep(wait)

            except ZohoAuthenticationError:
                if attempt == 0:
                    logger.info("401 received — forcing token refresh")
                    self._auth.force_refresh()
                    continue
                raise

            except ZohoServerError as exc:
                last_exc = exc
                wait = self._config.retry_backoff * (2**attempt)
                logger.warning(
                    "Server error %d. Retrying in %.1fs (attempt %d/%d)",
                    exc.status_code,
                    wait,
                    attempt + 1,
                    self._config.max_retries + 1,
                )
                time.sleep(wait)

        if last_exc is not None:
            raise last_exc
        raise ZohoAPIError("Request failed after retries", status_code=0)  # pragma: no cover


# ---------------------------------------------------------------------------
# Async client
# ---------------------------------------------------------------------------


class AsyncZohoClient:
    """Asynchronous HTTP client for Zoho APIs.

    Example::

        import asyncio
        from zohopy import ZohoConfig, AsyncZohoClient

        async def main():
            config = ZohoConfig()
            async with AsyncZohoClient(config) as client:
                data = await client.get("/books/v3/contacts")

        asyncio.run(main())
    """

    def __init__(self, config: ZohoConfig) -> None:
        self._config = config
        self._auth = AsyncAuth(config)
        self._http = httpx.AsyncClient(
            base_url=config.base_api_url,
            timeout=config.timeout,
        )

    @property
    def config(self) -> ZohoConfig:
        return self._config

    # -- HTTP verbs ---------------------------------------------------------

    async def get(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        return await self._request("GET", path, params=params)

    async def post(
        self,
        path: str,
        *,
        json: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        files: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        return await self._request("POST", path, json=json, params=params, files=files)

    async def put(
        self,
        path: str,
        *,
        json: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        return await self._request("PUT", path, json=json, params=params)

    async def delete(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        return await self._request("DELETE", path, params=params)

    # -- pagination ---------------------------------------------------------

    async def paginate(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        per_page: int = 200,
    ) -> AsyncIterator[dict[str, Any]]:
        """Async iterate through pages of a list endpoint."""
        p: dict[str, Any] = dict(params or {})
        page = 1
        while True:
            p["page"] = page
            p["per_page"] = per_page
            data = await self.get(path, params=p)
            yield data
            ctx = data.get("page_context", {})
            if not ctx.get("has_more_page", False):
                break
            page += 1

    # -- lifecycle ----------------------------------------------------------

    async def close(self) -> None:
        await self._http.aclose()
        await self._auth.close()

    async def __aenter__(self) -> AsyncZohoClient:
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.close()

    # -- internal -----------------------------------------------------------

    async def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
        files: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        import asyncio

        params = dict(params or {})
        params.setdefault("organization_id", self._config.organization_id)

        last_exc: Exception | None = None

        for attempt in range(self._config.max_retries + 1):
            headers = await self._auth.get_headers()

            try:
                resp = await self._http.request(
                    method,
                    path,
                    params=params,
                    json=json,
                    headers=headers,
                    files=files,
                )
                return _raise_for_status(resp)

            except ZohoRateLimitError as exc:
                last_exc = exc
                wait = exc.retry_after * (attempt + 1)
                logger.warning(
                    "Rate-limited (429). Sleeping %.1fs (attempt %d/%d)",
                    wait,
                    attempt + 1,
                    self._config.max_retries + 1,
                )
                await asyncio.sleep(wait)

            except ZohoAuthenticationError:
                if attempt == 0:
                    logger.info("401 received — forcing token refresh")
                    await self._auth.force_refresh()
                    continue
                raise

            except ZohoServerError as exc:
                last_exc = exc
                wait = self._config.retry_backoff * (2**attempt)
                logger.warning(
                    "Server error %d. Retrying in %.1fs (attempt %d/%d)",
                    exc.status_code,
                    wait,
                    attempt + 1,
                    self._config.max_retries + 1,
                )
                await asyncio.sleep(wait)

        if last_exc is not None:
            raise last_exc
        raise ZohoAPIError("Request failed after retries", status_code=0)  # pragma: no cover

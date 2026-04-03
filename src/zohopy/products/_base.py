"""Base classes for product-specific resource APIs (sync + async).

Every Zoho product (Books, Inventory, …) is a subpackage containing
resource modules (contacts, invoices, items, …). Each resource module
defines a sync and async class that inherit from these bases.

The :class:`SyncResource` and :class:`AsyncResource` classes provide
standard CRUD methods (``create``, ``list``, ``get``, ``update``,
``delete``) that build the full URL path from a fixed prefix + resource
name.
"""

from __future__ import annotations

from collections.abc import AsyncIterator, Iterator
from typing import Any

from zohopy._client import AsyncZohoClient, SyncZohoClient

# ---------------------------------------------------------------------------
# Sync base
# ---------------------------------------------------------------------------


class SyncResource:
    """Base for synchronous resource APIs.

    Subclasses **must** set:
        ``_api_prefix`` — e.g. ``"/books/v3"``
        ``_resource``   — e.g. ``"contacts"``
    """

    _api_prefix: str = ""
    _resource: str = ""

    def __init__(self, client: SyncZohoClient) -> None:
        self._client = client

    # -- path helpers -------------------------------------------------------

    def _path(self, *segments: str) -> str:
        parts = [self._api_prefix, self._resource, *segments]
        return "/".join(p.strip("/") for p in parts if p)

    # -- CRUD ---------------------------------------------------------------

    def create(self, data: dict[str, Any], **params: Any) -> dict[str, Any]:
        """Create a new resource."""
        return self._client.post(self._path(), json=data, params=params or None)

    def list(self, **params: Any) -> dict[str, Any]:
        """List resources (single page)."""
        return self._client.get(self._path(), params=params or None)

    def list_all(self, per_page: int = 200, **params: Any) -> Iterator[dict[str, Any]]:
        """Auto-paginate through all resources."""
        return self._client.paginate(self._path(), params=params or None, per_page=per_page)

    def get(self, resource_id: str, **params: Any) -> dict[str, Any]:
        """Get a single resource by ID."""
        return self._client.get(self._path(resource_id), params=params or None)

    def update(self, resource_id: str, data: dict[str, Any], **params: Any) -> dict[str, Any]:
        """Update an existing resource."""
        return self._client.put(self._path(resource_id), json=data, params=params or None)

    def delete(self, resource_id: str, **params: Any) -> dict[str, Any]:
        """Delete a resource."""
        return self._client.delete(self._path(resource_id), params=params or None)

    # -- action helpers (for status changes, emails, etc.) ------------------

    def _action_post(
        self,
        resource_id: str,
        action: str,
        data: dict[str, Any] | None = None,
        **params: Any,
    ) -> dict[str, Any]:
        return self._client.post(self._path(resource_id, action), json=data, params=params or None)

    def _action_get(self, resource_id: str, action: str, **params: Any) -> dict[str, Any]:
        return self._client.get(self._path(resource_id, action), params=params or None)

    def _sub_post(
        self, action: str, data: dict[str, Any] | None = None, **params: Any
    ) -> dict[str, Any]:
        return self._client.post(self._path(action), json=data, params=params or None)


# ---------------------------------------------------------------------------
# Async base
# ---------------------------------------------------------------------------


class AsyncResource:
    """Base for asynchronous resource APIs.

    Mirror of :class:`SyncResource` with ``async``/``await``.
    """

    _api_prefix: str = ""
    _resource: str = ""

    def __init__(self, client: AsyncZohoClient) -> None:
        self._client = client

    def _path(self, *segments: str) -> str:
        parts = [self._api_prefix, self._resource, *segments]
        return "/".join(p.strip("/") for p in parts if p)

    async def create(self, data: dict[str, Any], **params: Any) -> dict[str, Any]:
        return await self._client.post(self._path(), json=data, params=params or None)

    async def list(self, **params: Any) -> dict[str, Any]:
        return await self._client.get(self._path(), params=params or None)

    async def list_all(self, per_page: int = 200, **params: Any) -> AsyncIterator[dict[str, Any]]:
        async for page in self._client.paginate(
            self._path(), params=params or None, per_page=per_page
        ):
            yield page

    async def get(self, resource_id: str, **params: Any) -> dict[str, Any]:
        return await self._client.get(self._path(resource_id), params=params or None)

    async def update(self, resource_id: str, data: dict[str, Any], **params: Any) -> dict[str, Any]:
        return await self._client.put(self._path(resource_id), json=data, params=params or None)

    async def delete(self, resource_id: str, **params: Any) -> dict[str, Any]:
        return await self._client.delete(self._path(resource_id), params=params or None)

    async def _action_post(
        self,
        resource_id: str,
        action: str,
        data: dict[str, Any] | None = None,
        **params: Any,
    ) -> dict[str, Any]:
        return await self._client.post(
            self._path(resource_id, action), json=data, params=params or None
        )

    async def _action_get(self, resource_id: str, action: str, **params: Any) -> dict[str, Any]:
        return await self._client.get(self._path(resource_id, action), params=params or None)

    async def _sub_post(
        self,
        action: str,
        data: dict[str, Any] | None = None,
        **params: Any,
    ) -> dict[str, Any]:
        return await self._client.post(self._path(action), json=data, params=params or None)

"""Locations. Ref: https://www.zoho.com/books/api/v3/locations/"""

from __future__ import annotations

from typing import Any

from zohopy.products._base import AsyncResource, SyncResource

_P = "/books/v3"


class Locations(SyncResource):
    _api_prefix, _resource = _P, "settings/locations"

    def enable(self) -> dict[str, Any]:
        return self._client.post(self._path("enable"))

    def mark_active(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "active")

    def mark_inactive(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "inactive")

    def mark_primary(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "primary")


class AsyncLocations(AsyncResource):
    _api_prefix, _resource = _P, "settings/locations"

    async def enable(self) -> dict[str, Any]:
        return await self._client.post(self._path("enable"))

    async def mark_active(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "active")

    async def mark_inactive(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "inactive")

    async def mark_primary(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "primary")

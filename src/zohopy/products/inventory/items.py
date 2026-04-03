"""Inventory Items. Ref: https://www.zoho.com/inventory/api/v1/items/"""

from __future__ import annotations

from typing import Any

from zohopy.products._base import AsyncResource, SyncResource

_P = "/inventory/v1"


class Items(SyncResource):
    _api_prefix, _resource = _P, "items"

    def mark_active(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "active")

    def mark_inactive(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "inactive")

    def delete_image(self, id: str) -> dict[str, Any]:
        return self._client.delete(self._path(id, "image"))


class AsyncItems(AsyncResource):
    _api_prefix, _resource = _P, "items"

    async def mark_active(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "active")

    async def mark_inactive(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "inactive")

    async def delete_image(self, id: str) -> dict[str, Any]:
        return await self._client.delete(self._path(id, "image"))

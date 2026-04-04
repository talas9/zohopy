"""Items. Ref: https://www.zoho.com/books/api/v3/items/

Custom fields and warehouses are part of the item JSON body —
pass them in create()/update() payloads, not as sub-endpoints.
"""

from __future__ import annotations

from typing import Any

from zohopy.products._base import AsyncResource, SyncResource

_P = "/books/v3"


class Items(SyncResource):
    _api_prefix, _resource = _P, "items"

    def mark_active(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "active")

    def mark_inactive(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "inactive")

    def delete_image(self, id: str) -> dict[str, Any]:
        return self._client.delete(self._path(id, "image"))

    def upload_image(self, id: str, files: dict[str, Any]) -> dict[str, Any]:
        return self._client.post(self._path(id, "image"), files=files)

    def update_custom_fields(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._action_post(id, "customfields", data)


class AsyncItems(AsyncResource):
    _api_prefix, _resource = _P, "items"

    async def mark_active(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "active")

    async def mark_inactive(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "inactive")

    async def delete_image(self, id: str) -> dict[str, Any]:
        return await self._client.delete(self._path(id, "image"))

    async def upload_image(self, id: str, files: dict[str, Any]) -> dict[str, Any]:
        return await self._client.post(self._path(id, "image"), files=files)

    async def update_custom_fields(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._action_post(id, "customfields", data)

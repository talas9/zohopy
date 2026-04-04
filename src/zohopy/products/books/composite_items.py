"""Composite Items (bundle/assembly items with mapped components).

Ref: https://www.zoho.com/books/api/v3/

Create with mapped_items in the JSON body::

    books.composite_items.create({
        "name": "Bundle Pack",
        "rate": 250,
        "mapped_items": [
            {"item_id": "ID1", "quantity": 1},
            {"item_id": "ID2", "quantity": 2},
        ],
        "custom_fields": [
            {"label": "Field Name", "value": "Field Value"},
        ],
    })

Requires composite items enabled in Zoho Books settings.
"""

from __future__ import annotations

from typing import Any

from zohopy.products._base import AsyncResource, SyncResource

_P = "/books/v3"


class CompositeItems(SyncResource):
    _api_prefix, _resource = _P, "compositeitems"

    def mark_active(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "active")

    def mark_inactive(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "inactive")

    def delete_image(self, id: str) -> dict[str, Any]:
        return self._client.delete(self._path(id, "image"))

    def upload_image(self, id: str, files: dict[str, Any]) -> dict[str, Any]:
        return self._client.post(self._path(id, "image"), files=files)


class AsyncCompositeItems(AsyncResource):
    _api_prefix, _resource = _P, "compositeitems"

    async def mark_active(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "active")

    async def mark_inactive(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "inactive")

    async def delete_image(self, id: str) -> dict[str, Any]:
        return await self._client.delete(self._path(id, "image"))

    async def upload_image(self, id: str, files: dict[str, Any]) -> dict[str, Any]:
        return await self._client.post(self._path(id, "image"), files=files)

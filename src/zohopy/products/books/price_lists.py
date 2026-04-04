"""PriceLists. Ref: https://www.zoho.com/books/api/v3/"""

from __future__ import annotations

from typing import Any

from zohopy.products._base import AsyncResource, SyncResource

_P = "/books/v3"


class PriceLists(SyncResource):
    _api_prefix, _resource = _P, "pricebooks"

    def mark_active(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "mark_active")

    def mark_inactive(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "mark_inactive")


class AsyncPriceLists(AsyncResource):
    _api_prefix, _resource = _P, "pricebooks"

    async def mark_active(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "mark_active")

    async def mark_inactive(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "mark_inactive")

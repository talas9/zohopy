"""Item Groups. Ref: https://www.zoho.com/inventory/api/v1/itemgroups/"""

from __future__ import annotations

from typing import Any

from zohopy.products._base import AsyncResource, SyncResource

_P = "/inventory/v1"


class ItemGroups(SyncResource):
    _api_prefix, _resource = _P, "itemgroups"

    def mark_active(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "active")

    def mark_inactive(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "inactive")


class AsyncItemGroups(AsyncResource):
    _api_prefix, _resource = _P, "itemgroups"

    async def mark_active(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "active")

    async def mark_inactive(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "inactive")

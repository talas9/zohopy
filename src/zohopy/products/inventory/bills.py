"""Inventory Bills. Ref: https://www.zoho.com/inventory/api/v1/bills/"""

from __future__ import annotations

from typing import Any

from zohopy.products._base import AsyncResource, SyncResource

_P = "/inventory/v1"


class InvBills(SyncResource):
    _api_prefix, _resource = _P, "bills"

    def mark_open(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "status/open")

    def mark_void(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "status/void")


class AsyncInvBills(AsyncResource):
    _api_prefix, _resource = _P, "bills"

    async def mark_open(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "status/open")

    async def mark_void(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "status/void")

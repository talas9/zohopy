"""Inventory Sales Orders. Ref: https://www.zoho.com/inventory/api/v1/salesorders/"""

from __future__ import annotations

from typing import Any

from zohopy.products._base import AsyncResource, SyncResource

_P = "/inventory/v1"


class InvSalesOrders(SyncResource):
    _api_prefix, _resource = _P, "salesorders"

    def confirm(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "status/confirmed")

    def mark_void(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "status/void")


class AsyncInvSalesOrders(AsyncResource):
    _api_prefix, _resource = _P, "salesorders"

    async def confirm(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "status/confirmed")

    async def mark_void(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "status/void")

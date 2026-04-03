"""Inventory Purchase Orders. Ref: https://www.zoho.com/inventory/api/v1/purchaseorders/"""

from __future__ import annotations

from typing import Any

from zohopy.products._base import AsyncResource, SyncResource

_P = "/inventory/v1"


class InvPurchaseOrders(SyncResource):
    _api_prefix, _resource = _P, "purchaseorders"

    def mark_issued(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "status/issued")

    def mark_cancelled(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "status/cancelled")


class AsyncInvPurchaseOrders(AsyncResource):
    _api_prefix, _resource = _P, "purchaseorders"

    async def mark_issued(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "status/issued")

    async def mark_cancelled(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "status/cancelled")

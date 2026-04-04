"""ShipmentOrders. Ref: https://www.zoho.com/books/api/v3/"""

from __future__ import annotations

from typing import Any

from zohopy.products._base import AsyncResource, SyncResource

_P = "/books/v3"


class ShipmentOrders(SyncResource):
    _api_prefix, _resource = _P, "shipmentorders"

    def mark_delivered(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "status/delivered")


class AsyncShipmentOrders(AsyncResource):
    _api_prefix, _resource = _P, "shipmentorders"

    async def mark_delivered(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "status/delivered")

"""TransferOrders. Ref: https://www.zoho.com/books/api/v3/"""

from __future__ import annotations

from typing import Any

from zohopy.products._base import AsyncResource, SyncResource

_P = "/books/v3"


class TransferOrders(SyncResource):
    _api_prefix, _resource = _P, "transferorders"

    def mark_received(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "status/received")


class AsyncTransferOrders(AsyncResource):
    _api_prefix, _resource = _P, "transferorders"

    async def mark_received(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "status/received")

"""SalesReturns. Ref: https://www.zoho.com/books/api/v3/"""

from __future__ import annotations

from typing import Any

from zohopy.products._base import AsyncResource, SyncResource

_P = "/books/v3"


class SalesReturns(SyncResource):
    _api_prefix, _resource = _P, "salesreturns"

    def create_receive(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._action_post(id, "receive", data)

    def delete_receive(self, id: str, receive_id: str) -> dict[str, Any]:
        return self._client.delete(self._path(id, "receive", receive_id))


class AsyncSalesReturns(AsyncResource):
    _api_prefix, _resource = _P, "salesreturns"

    async def create_receive(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._action_post(id, "receive", data)

    async def delete_receive(self, id: str, receive_id: str) -> dict[str, Any]:
        return await self._client.delete(self._path(id, "receive", receive_id))

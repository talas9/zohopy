"""Sales Receipts. Ref: https://www.zoho.com/books/api/v3/sales-receipt/"""

from __future__ import annotations

from typing import Any

from zohopy.products._base import AsyncResource, SyncResource

_P = "/books/v3"


class SalesReceipts(SyncResource):
    _api_prefix, _resource = _P, "salesreceipts"

    def email(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._action_post(id, "email", data)


class AsyncSalesReceipts(AsyncResource):
    _api_prefix, _resource = _P, "salesreceipts"

    async def email(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._action_post(id, "email", data)

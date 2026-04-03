"""Inventory Invoices. Ref: https://www.zoho.com/inventory/api/v1/invoices/"""

from __future__ import annotations

from typing import Any

from zohopy.products._base import AsyncResource, SyncResource

_P = "/inventory/v1"


class InvInvoices(SyncResource):
    _api_prefix, _resource = _P, "invoices"

    def mark_sent(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "status/sent")

    def void(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "status/void")

    def mark_draft(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "status/draft")


class AsyncInvInvoices(AsyncResource):
    _api_prefix, _resource = _P, "invoices"

    async def mark_sent(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "status/sent")

    async def void(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "status/void")

    async def mark_draft(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "status/draft")

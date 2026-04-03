"""Recurring Invoices. Ref: https://www.zoho.com/books/api/v3/recurring-invoices/"""

from __future__ import annotations

from typing import Any

from zohopy.products._base import AsyncResource, SyncResource

_P = "/books/v3"


class RecurringInvoices(SyncResource):
    _api_prefix, _resource = _P, "recurringinvoices"

    def stop(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "status/stop")

    def resume(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "status/resume")

    def list_history(self, id: str) -> dict[str, Any]:
        return self._action_get(id, "comments")

    def update_template(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._action_post(id, "templates", data)


class AsyncRecurringInvoices(AsyncResource):
    _api_prefix, _resource = _P, "recurringinvoices"

    async def stop(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "status/stop")

    async def resume(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "status/resume")

    async def list_history(self, id: str) -> dict[str, Any]:
        return await self._action_get(id, "comments")

    async def update_template(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._action_post(id, "templates", data)

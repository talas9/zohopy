"""Recurring Bills. Ref: https://www.zoho.com/books/api/v3/recurring-bills/"""

from __future__ import annotations

from typing import Any

from zohopy.products._base import AsyncResource, SyncResource

_P = "/books/v3"


class RecurringBills(SyncResource):
    _api_prefix, _resource = _P, "recurringbills"

    def stop(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "status/stop")

    def resume(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "status/resume")

    def list_history(self, id: str) -> dict[str, Any]:
        return self._action_get(id, "comments")


class AsyncRecurringBills(AsyncResource):
    _api_prefix, _resource = _P, "recurringbills"

    async def stop(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "status/stop")

    async def resume(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "status/resume")

    async def list_history(self, id: str) -> dict[str, Any]:
        return await self._action_get(id, "comments")

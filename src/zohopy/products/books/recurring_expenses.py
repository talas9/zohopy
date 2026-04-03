"""Recurring Expenses. Ref: https://www.zoho.com/books/api/v3/recurring-expenses/"""

from __future__ import annotations

from typing import Any

from zohopy.products._base import AsyncResource, SyncResource

_P = "/books/v3"


class RecurringExpenses(SyncResource):
    _api_prefix, _resource = _P, "recurringexpenses"

    def stop(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "status/stop")

    def resume(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "status/resume")

    def list_child_expenses(self, id: str) -> dict[str, Any]:
        return self._action_get(id, "expenses")

    def list_history(self, id: str) -> dict[str, Any]:
        return self._action_get(id, "comments")


class AsyncRecurringExpenses(AsyncResource):
    _api_prefix, _resource = _P, "recurringexpenses"

    async def stop(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "status/stop")

    async def resume(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "status/resume")

    async def list_child_expenses(self, id: str) -> dict[str, Any]:
        return await self._action_get(id, "expenses")

    async def list_history(self, id: str) -> dict[str, Any]:
        return await self._action_get(id, "comments")

"""Journals & Chart of Accounts.

Ref: https://www.zoho.com/books/api/v3/journals/
Ref: https://www.zoho.com/books/api/v3/chart-of-accounts/
"""

from __future__ import annotations

from typing import Any

from zohopy.products._base import AsyncResource, SyncResource

_P = "/books/v3"


class Journals(SyncResource):
    _api_prefix, _resource = _P, "journals"

    def publish(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "publish")

    def add_comment(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._action_post(id, "comments", data)

    def add_attachment(self, id: str, files: dict[str, Any]) -> dict[str, Any]:
        return self._client.post(self._path(id, "attachment"), files=files)

    def delete_comment(self, id: str, comment_id: str) -> dict[str, Any]:
        return self._client.delete(self._path(id, "comments", comment_id))


class AsyncJournals(AsyncResource):
    _api_prefix, _resource = _P, "journals"

    async def publish(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "publish")

    async def add_comment(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._action_post(id, "comments", data)

    async def add_attachment(self, id: str, files: dict[str, Any]) -> dict[str, Any]:
        return await self._client.post(self._path(id, "attachment"), files=files)

    async def delete_comment(self, id: str, comment_id: str) -> dict[str, Any]:
        return await self._client.delete(self._path(id, "comments", comment_id))


class ChartOfAccounts(SyncResource):
    _api_prefix, _resource = _P, "chartofaccounts"

    def mark_active(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "active")

    def mark_inactive(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "inactive")

    def list_transactions(self, id: str, **params: Any) -> dict[str, Any]:
        return self._action_get(id, "transactions", **params)

    def delete_transaction(self, id: str, txn_id: str) -> dict[str, Any]:
        return self._client.delete(self._path(id, "transactions", txn_id))


class AsyncChartOfAccounts(AsyncResource):
    _api_prefix, _resource = _P, "chartofaccounts"

    async def mark_active(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "active")

    async def mark_inactive(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "inactive")

    async def list_transactions(self, id: str, **params: Any) -> dict[str, Any]:
        return await self._action_get(id, "transactions", **params)

    async def delete_transaction(self, id: str, txn_id: str) -> dict[str, Any]:
        return await self._client.delete(self._path(id, "transactions", txn_id))

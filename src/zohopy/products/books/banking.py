"""Bank Accounts. Ref: https://www.zoho.com/books/api/v3/bank-accounts/"""

from __future__ import annotations

from typing import Any

from zohopy.products._base import AsyncResource, SyncResource

_P = "/books/v3"


class BankAccounts(SyncResource):
    _api_prefix, _resource = _P, "bankaccounts"

    def deactivate(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "inactive")

    def activate(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "active")

    def import_statement(self, id: str, files: dict[str, Any]) -> dict[str, Any]:
        return self._client.post(self._path(id, "statement"), files=files)

    def get_last_statement(self, id: str) -> dict[str, Any]:
        return self._action_get(id, "statement")

    def delete_last_statement(self, id: str) -> dict[str, Any]:
        return self._client.delete(self._path(id, "statement"))


class AsyncBankAccounts(AsyncResource):
    _api_prefix, _resource = _P, "bankaccounts"

    async def deactivate(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "inactive")

    async def activate(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "active")

    async def import_statement(self, id: str, files: dict[str, Any]) -> dict[str, Any]:
        return await self._client.post(self._path(id, "statement"), files=files)

    async def get_last_statement(self, id: str) -> dict[str, Any]:
        return await self._action_get(id, "statement")

    async def delete_last_statement(self, id: str) -> dict[str, Any]:
        return await self._client.delete(self._path(id, "statement"))

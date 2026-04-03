"""Expenses. Ref: https://www.zoho.com/books/api/v3/expenses/"""

from __future__ import annotations

from typing import Any

from zohopy.products._base import AsyncResource, SyncResource

_P = "/books/v3"


class Expenses(SyncResource):
    _api_prefix, _resource = _P, "expenses"

    def list_comments(self, id: str) -> dict[str, Any]:
        return self._action_get(id, "comments")

    def add_receipt(self, id: str, files: dict[str, Any]) -> dict[str, Any]:
        return self._client.post(self._path(id, "receipt"), files=files)

    def get_receipt(self, id: str) -> dict[str, Any]:
        return self._action_get(id, "receipt")

    def delete_receipt(self, id: str) -> dict[str, Any]:
        return self._client.delete(self._path(id, "receipt"))

    def create_employee(self, data: dict[str, Any]) -> dict[str, Any]:
        return self._client.post(self._path("employees"), json=data)

    def list_employees(self, **params: Any) -> dict[str, Any]:
        return self._client.get(self._path("employees"), params=params or None)

    def get_employee(self, employee_id: str) -> dict[str, Any]:
        return self._client.get(self._path("employees", employee_id))

    def delete_employee(self, employee_id: str) -> dict[str, Any]:
        return self._client.delete(self._path("employees", employee_id))

    def add_attachment(self, id: str, files: dict[str, Any]) -> dict[str, Any]:
        return self._client.post(self._path(id, "attachment"), files=files)


class AsyncExpenses(AsyncResource):
    _api_prefix, _resource = _P, "expenses"

    async def list_comments(self, id: str) -> dict[str, Any]:
        return await self._action_get(id, "comments")

    async def add_receipt(self, id: str, files: dict[str, Any]) -> dict[str, Any]:
        return await self._client.post(self._path(id, "receipt"), files=files)

    async def get_receipt(self, id: str) -> dict[str, Any]:
        return await self._action_get(id, "receipt")

    async def delete_receipt(self, id: str) -> dict[str, Any]:
        return await self._client.delete(self._path(id, "receipt"))

    async def create_employee(self, data: dict[str, Any]) -> dict[str, Any]:
        return await self._client.post(self._path("employees"), json=data)

    async def list_employees(self, **params: Any) -> dict[str, Any]:
        return await self._client.get(self._path("employees"), params=params or None)

    async def get_employee(self, employee_id: str) -> dict[str, Any]:
        return await self._client.get(self._path("employees", employee_id))

    async def delete_employee(self, employee_id: str) -> dict[str, Any]:
        return await self._client.delete(self._path("employees", employee_id))

    async def add_attachment(self, id: str, files: dict[str, Any]) -> dict[str, Any]:
        return await self._client.post(self._path(id, "attachment"), files=files)

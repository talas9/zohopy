"""Custom Modules. Ref: https://www.zoho.com/books/api/v3/custom-modules/"""

from __future__ import annotations

from typing import Any

from zohopy.products._base import AsyncResource, SyncResource

_P = "/books/v3"


class CustomModules(SyncResource):
    _api_prefix, _resource = _P, "custommodules"

    def create_record(self, module_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._client.post(self._path(module_id, "records"), json=data)

    def list_records(self, module_id: str, **params: Any) -> dict[str, Any]:
        return self._client.get(self._path(module_id, "records"), params=params or None)

    def get_record(self, module_id: str, record_id: str) -> dict[str, Any]:
        return self._client.get(self._path(module_id, "records", record_id))

    def update_record(self, module_id: str, record_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._client.put(self._path(module_id, "records", record_id), json=data)

    def delete_record(self, module_id: str, record_id: str) -> dict[str, Any]:
        return self._client.delete(self._path(module_id, "records", record_id))

    def bulk_update_records(self, module_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._client.put(self._path(module_id, "records"), json=data)

    def delete_records(self, module_id: str, **params: Any) -> dict[str, Any]:
        return self._client.delete(self._path(module_id, "records"), params=params or None)


class AsyncCustomModules(AsyncResource):
    _api_prefix, _resource = _P, "custommodules"

    async def create_record(self, module_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._client.post(self._path(module_id, "records"), json=data)

    async def list_records(self, module_id: str, **params: Any) -> dict[str, Any]:
        return await self._client.get(self._path(module_id, "records"), params=params or None)

    async def get_record(self, module_id: str, record_id: str) -> dict[str, Any]:
        return await self._client.get(self._path(module_id, "records", record_id))

    async def update_record(
        self, module_id: str, record_id: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        return await self._client.put(self._path(module_id, "records", record_id), json=data)

    async def delete_record(self, module_id: str, record_id: str) -> dict[str, Any]:
        return await self._client.delete(self._path(module_id, "records", record_id))

    async def bulk_update_records(self, module_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._client.put(self._path(module_id, "records"), json=data)

    async def delete_records(self, module_id: str, **params: Any) -> dict[str, Any]:
        return await self._client.delete(self._path(module_id, "records"), params=params or None)

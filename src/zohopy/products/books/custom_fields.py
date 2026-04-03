"""Custom Fields. Ref: https://www.zoho.com/books/api/v3/custom-fields/"""

from __future__ import annotations

from typing import Any

from zohopy.products._base import AsyncResource, SyncResource

_P = "/books/v3"


class CustomFields(SyncResource):
    _api_prefix, _resource = _P, "settings/fields"

    def list_for_entity(self, entity: str, **params: Any) -> dict[str, Any]:
        return self._client.get(self._path(), params={"entity": entity, **params})

    def create(self, data: dict[str, Any], **params: Any) -> dict[str, Any]:
        return self._client.post(self._path(), json=data, params=params or None)

    def update(self, resource_id: str, data: dict[str, Any], **params: Any) -> dict[str, Any]:
        return self._client.put(self._path(resource_id), json=data, params=params or None)

    def delete(self, resource_id: str, **params: Any) -> dict[str, Any]:
        return self._client.delete(self._path(resource_id), params=params or None)

    def reorder(self, data: dict[str, Any], **params: Any) -> dict[str, Any]:
        return self._sub_post("reorder", data, **params)

    def update_status(self, field_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._client.put(self._path(field_id, "status"), json=data)

    def update_dropdown_options(self, field_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._client.put(
            self._path(field_id, "dropdownoptions"),
            json=data,
        )

    def bulk_fetch(self, **params: Any) -> dict[str, Any]:
        return self._client.get(
            self._path("bulkfetch"),
            params=params or None,
        )

    def get_usage(self, field_id: str) -> dict[str, Any]:
        return self._client.get(self._path(field_id, "usage"))

    def check_formula(self, data: dict[str, Any]) -> dict[str, Any]:
        return self._sub_post("checkformula", data)

    def list_lookup_fields(self, **params: Any) -> dict[str, Any]:
        return self._client.get(
            self._path("lookupfields"),
            params=params or None,
        )

    def list_simple(self, **params: Any) -> dict[str, Any]:
        return self._client.get(
            self._path("simple"),
            params=params or None,
        )

    def get_fields_meta(self, **params: Any) -> dict[str, Any]:
        return self._client.get(self._path("meta"), params=params or None)

    def get_entity_fields_meta(self, entity: str, **params: Any) -> dict[str, Any]:
        return self._client.get(
            self._path("meta", entity),
            params=params or None,
        )


class AsyncCustomFields(AsyncResource):
    _api_prefix, _resource = _P, "settings/fields"

    async def list_for_entity(self, entity: str, **params: Any) -> dict[str, Any]:
        return await self._client.get(self._path(), params={"entity": entity, **params})

    async def create(self, data: dict[str, Any], **params: Any) -> dict[str, Any]:
        return await self._client.post(self._path(), json=data, params=params or None)

    async def update(self, resource_id: str, data: dict[str, Any], **params: Any) -> dict[str, Any]:
        return await self._client.put(self._path(resource_id), json=data, params=params or None)

    async def delete(self, resource_id: str, **params: Any) -> dict[str, Any]:
        return await self._client.delete(self._path(resource_id), params=params or None)

    async def reorder(self, data: dict[str, Any], **params: Any) -> dict[str, Any]:
        return await self._client.post(self._path("reorder"), json=data, params=params or None)

    async def update_status(self, field_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._client.put(self._path(field_id, "status"), json=data)

    async def update_dropdown_options(self, field_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._client.put(
            self._path(field_id, "dropdownoptions"),
            json=data,
        )

    async def bulk_fetch(self, **params: Any) -> dict[str, Any]:
        return await self._client.get(
            self._path("bulkfetch"),
            params=params or None,
        )

    async def get_usage(self, field_id: str) -> dict[str, Any]:
        return await self._client.get(self._path(field_id, "usage"))

    async def check_formula(self, data: dict[str, Any]) -> dict[str, Any]:
        return await self._sub_post("checkformula", data)

    async def list_lookup_fields(self, **params: Any) -> dict[str, Any]:
        return await self._client.get(
            self._path("lookupfields"),
            params=params or None,
        )

    async def list_simple(self, **params: Any) -> dict[str, Any]:
        return await self._client.get(
            self._path("simple"),
            params=params or None,
        )

    async def get_fields_meta(self, **params: Any) -> dict[str, Any]:
        return await self._client.get(
            self._path("meta"),
            params=params or None,
        )

    async def get_entity_fields_meta(self, entity: str, **params: Any) -> dict[str, Any]:
        return await self._client.get(
            self._path("meta", entity),
            params=params or None,
        )

"""Zoho CRM Integration. Ref: https://www.zoho.com/books/api/v3/zoho-crm-integration/"""

from __future__ import annotations

from typing import Any

from zohopy.products._base import AsyncResource, SyncResource

_P = "/books/v3"


class CRMIntegration(SyncResource):
    _api_prefix, _resource = _P, "crm"

    def import_customer_by_account(self, data: dict[str, Any]) -> dict[str, Any]:
        return self._client.post(self._path("contact/importcustomer"), json=data)

    def import_customer_by_contact(self, data: dict[str, Any]) -> dict[str, Any]:
        return self._client.post(self._path("contact/importcontact"), json=data)

    def import_vendor(self, data: dict[str, Any]) -> dict[str, Any]:
        return self._client.post(self._path("contact/importvendor"), json=data)

    def import_item(self, data: dict[str, Any]) -> dict[str, Any]:
        return self._client.post(self._path("item/importproduct"), json=data)


class AsyncCRMIntegration(AsyncResource):
    _api_prefix, _resource = _P, "crm"

    async def import_customer_by_account(self, data: dict[str, Any]) -> dict[str, Any]:
        return await self._client.post(self._path("contact/importcustomer"), json=data)

    async def import_customer_by_contact(self, data: dict[str, Any]) -> dict[str, Any]:
        return await self._client.post(self._path("contact/importcontact"), json=data)

    async def import_vendor(self, data: dict[str, Any]) -> dict[str, Any]:
        return await self._client.post(self._path("contact/importvendor"), json=data)

    async def import_item(self, data: dict[str, Any]) -> dict[str, Any]:
        return await self._client.post(self._path("item/importproduct"), json=data)

"""Customer & Vendor Payments.

Ref: https://www.zoho.com/books/api/v3/customer-payments/
Ref: https://www.zoho.com/books/api/v3/vendor-payments/
"""

from __future__ import annotations

from typing import Any

from zohopy.products._base import AsyncResource, SyncResource

_P = "/books/v3"


class CustomerPayments(SyncResource):
    _api_prefix, _resource = _P, "customerpayments"

    def refund(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._action_post(id, "refunds", data)

    def list_refunds(self, id: str) -> dict[str, Any]:
        return self._action_get(id, "refunds")

    def bulk_delete(self, data: dict[str, Any]) -> dict[str, Any]:
        return self._sub_post("bulkdelete", data)

    def update_custom_fields(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._action_post(id, "customfields", data)

    def get_refund(self, id: str, refund_id: str) -> dict[str, Any]:
        return self._client.get(self._path(id, "refunds", refund_id))

    def update_refund(self, id: str, refund_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._client.put(self._path(id, "refunds", refund_id), json=data)

    def delete_refund(self, id: str, refund_id: str) -> dict[str, Any]:
        return self._client.delete(self._path(id, "refunds", refund_id))


class AsyncCustomerPayments(AsyncResource):
    _api_prefix, _resource = _P, "customerpayments"

    async def refund(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._action_post(id, "refunds", data)

    async def list_refunds(self, id: str) -> dict[str, Any]:
        return await self._action_get(id, "refunds")

    async def bulk_delete(self, data: dict[str, Any]) -> dict[str, Any]:
        return await self._sub_post("bulkdelete", data)

    async def update_custom_fields(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._action_post(id, "customfields", data)

    async def get_refund(self, id: str, refund_id: str) -> dict[str, Any]:
        return await self._client.get(self._path(id, "refunds", refund_id))

    async def update_refund(self, id: str, refund_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._client.put(self._path(id, "refunds", refund_id), json=data)

    async def delete_refund(self, id: str, refund_id: str) -> dict[str, Any]:
        return await self._client.delete(self._path(id, "refunds", refund_id))


class VendorPayments(SyncResource):
    _api_prefix, _resource = _P, "vendorpayments"

    def refund(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._action_post(id, "refunds", data)

    def list_refunds(self, id: str) -> dict[str, Any]:
        return self._action_get(id, "refunds")

    def email(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._action_post(id, "email", data)

    def bulk_delete(self, data: dict[str, Any]) -> dict[str, Any]:
        return self._sub_post("bulkdelete", data)

    def get_email_content(self, id: str, **params: Any) -> dict[str, Any]:
        return self._action_get(id, "email", **params)

    def get_refund(self, id: str, refund_id: str) -> dict[str, Any]:
        return self._client.get(self._path(id, "refunds", refund_id))

    def update_refund(self, id: str, refund_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._client.put(self._path(id, "refunds", refund_id), json=data)

    def delete_refund(self, id: str, refund_id: str) -> dict[str, Any]:
        return self._client.delete(self._path(id, "refunds", refund_id))


class AsyncVendorPayments(AsyncResource):
    _api_prefix, _resource = _P, "vendorpayments"

    async def refund(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._action_post(id, "refunds", data)

    async def list_refunds(self, id: str) -> dict[str, Any]:
        return await self._action_get(id, "refunds")

    async def email(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._action_post(id, "email", data)

    async def bulk_delete(self, data: dict[str, Any]) -> dict[str, Any]:
        return await self._sub_post("bulkdelete", data)

    async def get_email_content(self, id: str, **params: Any) -> dict[str, Any]:
        return await self._action_get(id, "email", **params)

    async def get_refund(self, id: str, refund_id: str) -> dict[str, Any]:
        return await self._client.get(self._path(id, "refunds", refund_id))

    async def update_refund(self, id: str, refund_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._client.put(self._path(id, "refunds", refund_id), json=data)

    async def delete_refund(self, id: str, refund_id: str) -> dict[str, Any]:
        return await self._client.delete(self._path(id, "refunds", refund_id))

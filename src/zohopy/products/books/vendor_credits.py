"""Vendor Credits. Ref: https://www.zoho.com/books/api/v3/vendor-credits/"""

from __future__ import annotations

from typing import Any

from zohopy.products._base import AsyncResource, SyncResource

_P = "/books/v3"


class VendorCredits(SyncResource):
    _api_prefix, _resource = _P, "vendorcredits"

    def convert_to_open(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "status/open")

    def void(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "status/void")

    def submit_for_approval(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "submit")

    def approve(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "approve")

    def apply_to_bill(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._action_post(id, "bills", data)

    def list_bills_credited(self, id: str) -> dict[str, Any]:
        return self._action_get(id, "bills")

    def refund(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._action_post(id, "refunds", data)

    def list_refunds(self, id: str) -> dict[str, Any]:
        return self._action_get(id, "refunds")

    def list_comments(self, id: str) -> dict[str, Any]:
        return self._action_get(id, "comments")

    def delete_bills_credited(self, id: str, credit_id: str) -> dict[str, Any]:
        return self._client.delete(self._path(id, "bills", credit_id))

    def get_refund(self, id: str, refund_id: str) -> dict[str, Any]:
        return self._client.get(self._path(id, "refunds", refund_id))

    def update_refund(self, id: str, refund_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._client.put(self._path(id, "refunds", refund_id), json=data)

    def delete_refund(self, id: str, refund_id: str) -> dict[str, Any]:
        return self._client.delete(self._path(id, "refunds", refund_id))

    def add_comment(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._action_post(id, "comments", data)

    def delete_comment(self, id: str, comment_id: str) -> dict[str, Any]:
        return self._client.delete(self._path(id, "comments", comment_id))


class AsyncVendorCredits(AsyncResource):
    _api_prefix, _resource = _P, "vendorcredits"

    async def convert_to_open(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "status/open")

    async def void(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "status/void")

    async def submit_for_approval(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "submit")

    async def approve(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "approve")

    async def apply_to_bill(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._action_post(id, "bills", data)

    async def list_bills_credited(self, id: str) -> dict[str, Any]:
        return await self._action_get(id, "bills")

    async def refund(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._action_post(id, "refunds", data)

    async def list_refunds(self, id: str) -> dict[str, Any]:
        return await self._action_get(id, "refunds")

    async def list_comments(self, id: str) -> dict[str, Any]:
        return await self._action_get(id, "comments")

    async def delete_bills_credited(self, id: str, credit_id: str) -> dict[str, Any]:
        return await self._client.delete(self._path(id, "bills", credit_id))

    async def get_refund(self, id: str, refund_id: str) -> dict[str, Any]:
        return await self._client.get(self._path(id, "refunds", refund_id))

    async def update_refund(self, id: str, refund_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._client.put(self._path(id, "refunds", refund_id), json=data)

    async def delete_refund(self, id: str, refund_id: str) -> dict[str, Any]:
        return await self._client.delete(self._path(id, "refunds", refund_id))

    async def add_comment(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._action_post(id, "comments", data)

    async def delete_comment(self, id: str, comment_id: str) -> dict[str, Any]:
        return await self._client.delete(self._path(id, "comments", comment_id))

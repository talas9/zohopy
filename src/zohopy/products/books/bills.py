"""Bills. Ref: https://www.zoho.com/books/api/v3/bills/"""

from __future__ import annotations

from typing import Any

from zohopy.products._base import AsyncResource, SyncResource

_P = "/books/v3"


class Bills(SyncResource):
    _api_prefix, _resource = _P, "bills"

    def void(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "status/void")

    def mark_open(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "status/open")

    def submit_for_approval(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "submit")

    def approve(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "approve")

    def apply_credits(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._action_post(id, "credits", data)

    def list_payments(self, id: str) -> dict[str, Any]:
        return self._action_get(id, "payments")

    def list_comments(self, id: str) -> dict[str, Any]:
        return self._action_get(id, "comments")

    def add_comment(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._action_post(id, "comments", data)

    def update_billing_address(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._action_post(id, "address/billing", data)

    def delete_payment(self, id: str, payment_id: str) -> dict[str, Any]:
        return self._client.delete(self._path(id, "payments", payment_id))

    def add_attachment(self, id: str, files: dict[str, Any]) -> dict[str, Any]:
        return self._client.post(self._path(id, "attachment"), files=files)

    def get_attachment(self, id: str) -> dict[str, Any]:
        return self._action_get(id, "attachment")

    def delete_attachment(self, id: str) -> dict[str, Any]:
        return self._client.delete(self._path(id, "attachment"))

    def update_custom_fields(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._action_post(id, "customfields", data)

    def convert_from_po(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._action_post(id, "convertfrompurchaseorder", data)


class AsyncBills(AsyncResource):
    _api_prefix, _resource = _P, "bills"

    async def void(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "status/void")

    async def mark_open(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "status/open")

    async def submit_for_approval(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "submit")

    async def approve(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "approve")

    async def apply_credits(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._action_post(id, "credits", data)

    async def list_payments(self, id: str) -> dict[str, Any]:
        return await self._action_get(id, "payments")

    async def list_comments(self, id: str) -> dict[str, Any]:
        return await self._action_get(id, "comments")

    async def add_comment(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._action_post(id, "comments", data)

    async def update_billing_address(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._action_post(id, "address/billing", data)

    async def delete_payment(self, id: str, payment_id: str) -> dict[str, Any]:
        return await self._client.delete(self._path(id, "payments", payment_id))

    async def add_attachment(self, id: str, files: dict[str, Any]) -> dict[str, Any]:
        return await self._client.post(self._path(id, "attachment"), files=files)

    async def get_attachment(self, id: str) -> dict[str, Any]:
        return await self._action_get(id, "attachment")

    async def delete_attachment(self, id: str) -> dict[str, Any]:
        return await self._client.delete(self._path(id, "attachment"))

    async def update_custom_fields(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._action_post(id, "customfields", data)

    async def convert_from_po(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._action_post(id, "convertfrompurchaseorder", data)

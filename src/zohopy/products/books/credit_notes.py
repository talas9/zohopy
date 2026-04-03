"""Credit Notes. Ref: https://www.zoho.com/books/api/v3/credit-notes/"""

from __future__ import annotations

from typing import Any

from zohopy.products._base import AsyncResource, SyncResource

_P = "/books/v3"


class CreditNotes(SyncResource):
    _api_prefix, _resource = _P, "creditnotes"

    def void(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "status/void")

    def to_draft(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "status/draft")

    def to_open(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "status/open")

    def submit_for_approval(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "submit")

    def approve(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "approve")

    def email(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._action_post(id, "email", data)

    def apply_to_invoice(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._action_post(id, "invoices", data)

    def list_invoices_credited(self, id: str) -> dict[str, Any]:
        return self._action_get(id, "invoices")

    def refund(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._action_post(id, "refunds", data)

    def list_refunds(self, id: str) -> dict[str, Any]:
        return self._action_get(id, "refunds")

    def list_comments(self, id: str) -> dict[str, Any]:
        return self._action_get(id, "comments")

    def get_email_content(self, id: str, **params: Any) -> dict[str, Any]:
        return self._action_get(id, "email", **params)

    def email_history(self, id: str) -> dict[str, Any]:
        return self._action_get(id, "emailhistory")

    def update_billing_address(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._action_post(id, "address/billing", data)

    def update_shipping_address(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._action_post(id, "address/shipping", data)

    def list_templates(self, id: str) -> dict[str, Any]:
        return self._action_get(id, "templates")

    def update_template(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._action_post(id, "templates", data)

    def delete_invoices_credited(self, id: str, credit_id: str) -> dict[str, Any]:
        return self._client.delete(self._path(id, "invoices", credit_id))

    def get_refund(self, id: str, refund_id: str) -> dict[str, Any]:
        return self._client.get(self._path(id, "refunds", refund_id))

    def update_refund(self, id: str, refund_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._client.put(self._path(id, "refunds", refund_id), json=data)

    def delete_refund(self, id: str, refund_id: str) -> dict[str, Any]:
        return self._client.delete(self._path(id, "refunds", refund_id))


class AsyncCreditNotes(AsyncResource):
    _api_prefix, _resource = _P, "creditnotes"

    async def void(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "status/void")

    async def to_draft(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "status/draft")

    async def to_open(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "status/open")

    async def submit_for_approval(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "submit")

    async def approve(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "approve")

    async def email(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._action_post(id, "email", data)

    async def apply_to_invoice(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._action_post(id, "invoices", data)

    async def list_invoices_credited(self, id: str) -> dict[str, Any]:
        return await self._action_get(id, "invoices")

    async def refund(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._action_post(id, "refunds", data)

    async def list_refunds(self, id: str) -> dict[str, Any]:
        return await self._action_get(id, "refunds")

    async def list_comments(self, id: str) -> dict[str, Any]:
        return await self._action_get(id, "comments")

    async def get_email_content(self, id: str, **params: Any) -> dict[str, Any]:
        return await self._action_get(id, "email", **params)

    async def email_history(self, id: str) -> dict[str, Any]:
        return await self._action_get(id, "emailhistory")

    async def update_billing_address(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._action_post(id, "address/billing", data)

    async def update_shipping_address(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._action_post(id, "address/shipping", data)

    async def list_templates(self, id: str) -> dict[str, Any]:
        return await self._action_get(id, "templates")

    async def update_template(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._action_post(id, "templates", data)

    async def delete_invoices_credited(self, id: str, credit_id: str) -> dict[str, Any]:
        return await self._client.delete(self._path(id, "invoices", credit_id))

    async def get_refund(self, id: str, refund_id: str) -> dict[str, Any]:
        return await self._client.get(self._path(id, "refunds", refund_id))

    async def update_refund(self, id: str, refund_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._client.put(self._path(id, "refunds", refund_id), json=data)

    async def delete_refund(self, id: str, refund_id: str) -> dict[str, Any]:
        return await self._client.delete(self._path(id, "refunds", refund_id))

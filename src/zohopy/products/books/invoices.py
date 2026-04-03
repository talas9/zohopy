"""Invoices & recurring invoices.

Ref: https://www.zoho.com/books/api/v3/invoices/
"""

from __future__ import annotations

from typing import Any

from zohopy.products._base import AsyncResource, SyncResource

_PREFIX = "/books/v3"


class Invoices(SyncResource):
    _api_prefix = _PREFIX
    _resource = "invoices"

    def mark_sent(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "status/sent")

    def void(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "status/void")

    def mark_draft(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "status/draft")

    def submit_for_approval(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "submit")

    def approve(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "approve")

    def email(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._action_post(id, "email", data)

    def get_email_content(self, id: str, **params: Any) -> dict[str, Any]:
        return self._action_get(id, "email", **params)

    def write_off(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "writeoff")

    def cancel_write_off(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "writeoff/cancel")

    def apply_credits(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._action_post(id, "credits", data)

    def list_payments(self, id: str) -> dict[str, Any]:
        return self._action_get(id, "payments")

    def list_comments(self, id: str) -> dict[str, Any]:
        return self._action_get(id, "comments")

    def add_comment(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._action_post(id, "comments", data)

    def generate_payment_link(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "paymentlink")

    def email_multiple(self, data: dict[str, Any]) -> dict[str, Any]:
        return self._sub_post("email", data)

    def create_instant(self, data: dict[str, Any]) -> dict[str, Any]:
        return self._sub_post("instantinvoice", data)

    def associate_with_sales_order(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._action_post(id, "salesorders", data)

    def remind_customer(
        self,
        id: str,
        data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        return self._action_post(id, "paymentreminder", data)

    def get_reminder_content(self, id: str, **params: Any) -> dict[str, Any]:
        return self._action_get(id, "paymentreminder", **params)

    def enable_reminder(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "paymentreminder/enable")

    def disable_reminder(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "paymentreminder/disable")

    def update_billing_address(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._action_post(id, "address/billing", data)

    def update_shipping_address(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._action_post(id, "address/shipping", data)

    def list_templates(self, id: str) -> dict[str, Any]:
        return self._action_get(id, "templates")

    def update_template(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._action_post(id, "templates", data)

    def list_credits_applied(self, id: str) -> dict[str, Any]:
        return self._action_get(id, "creditsapplied")

    def delete_payment(self, id: str, payment_id: str) -> dict[str, Any]:
        return self._client.delete(self._path(id, "payments", payment_id))

    def delete_credit_applied(self, id: str, credit_id: str) -> dict[str, Any]:
        return self._client.delete(self._path(id, "creditsapplied", credit_id))

    def add_attachment(self, id: str, files: dict[str, Any]) -> dict[str, Any]:
        return self._client.post(self._path(id, "attachment"), files=files)

    def get_attachment(self, id: str) -> dict[str, Any]:
        return self._action_get(id, "attachment")

    def delete_attachment(self, id: str) -> dict[str, Any]:
        return self._client.delete(self._path(id, "attachment"))

    def update_custom_fields(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._action_post(id, "customfields", data)

    def update_comment(
        self,
        id: str,
        comment_id: str,
        data: dict[str, Any],
    ) -> dict[str, Any]:
        return self._client.put(
            self._path(id, "comments", comment_id),
            json=data,
        )

    def delete_comment(self, id: str, comment_id: str) -> dict[str, Any]:
        return self._client.delete(self._path(id, "comments", comment_id))


class AsyncInvoices(AsyncResource):
    _api_prefix = _PREFIX
    _resource = "invoices"

    async def mark_sent(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "status/sent")

    async def void(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "status/void")

    async def mark_draft(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "status/draft")

    async def submit_for_approval(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "submit")

    async def approve(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "approve")

    async def email(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._action_post(id, "email", data)

    async def get_email_content(self, id: str, **params: Any) -> dict[str, Any]:
        return await self._action_get(id, "email", **params)

    async def write_off(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "writeoff")

    async def cancel_write_off(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "writeoff/cancel")

    async def apply_credits(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._action_post(id, "credits", data)

    async def list_payments(self, id: str) -> dict[str, Any]:
        return await self._action_get(id, "payments")

    async def list_comments(self, id: str) -> dict[str, Any]:
        return await self._action_get(id, "comments")

    async def add_comment(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._action_post(id, "comments", data)

    async def generate_payment_link(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "paymentlink")

    async def email_multiple(self, data: dict[str, Any]) -> dict[str, Any]:
        return await self._sub_post("email", data)

    async def create_instant(self, data: dict[str, Any]) -> dict[str, Any]:
        return await self._sub_post("instantinvoice", data)

    async def associate_with_sales_order(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._action_post(id, "salesorders", data)

    async def remind_customer(
        self,
        id: str,
        data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        return await self._action_post(id, "paymentreminder", data)

    async def get_reminder_content(self, id: str, **params: Any) -> dict[str, Any]:
        return await self._action_get(id, "paymentreminder", **params)

    async def enable_reminder(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "paymentreminder/enable")

    async def disable_reminder(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "paymentreminder/disable")

    async def update_billing_address(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._action_post(id, "address/billing", data)

    async def update_shipping_address(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._action_post(id, "address/shipping", data)

    async def list_templates(self, id: str) -> dict[str, Any]:
        return await self._action_get(id, "templates")

    async def update_template(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._action_post(id, "templates", data)

    async def list_credits_applied(self, id: str) -> dict[str, Any]:
        return await self._action_get(id, "creditsapplied")

    async def delete_payment(self, id: str, payment_id: str) -> dict[str, Any]:
        return await self._client.delete(self._path(id, "payments", payment_id))

    async def delete_credit_applied(self, id: str, credit_id: str) -> dict[str, Any]:
        return await self._client.delete(self._path(id, "creditsapplied", credit_id))

    async def add_attachment(self, id: str, files: dict[str, Any]) -> dict[str, Any]:
        return await self._client.post(self._path(id, "attachment"), files=files)

    async def get_attachment(self, id: str) -> dict[str, Any]:
        return await self._action_get(id, "attachment")

    async def delete_attachment(self, id: str) -> dict[str, Any]:
        return await self._client.delete(self._path(id, "attachment"))

    async def update_custom_fields(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._action_post(id, "customfields", data)

    async def update_comment(
        self,
        id: str,
        comment_id: str,
        data: dict[str, Any],
    ) -> dict[str, Any]:
        return await self._client.put(
            self._path(id, "comments", comment_id),
            json=data,
        )

    async def delete_comment(self, id: str, comment_id: str) -> dict[str, Any]:
        return await self._client.delete(self._path(id, "comments", comment_id))

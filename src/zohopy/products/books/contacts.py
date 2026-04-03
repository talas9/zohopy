"""Contacts & contact persons.

Ref: https://www.zoho.com/books/api/v3/contacts/
"""

from __future__ import annotations

from typing import Any

from zohopy.products._base import AsyncResource, SyncResource

_PREFIX = "/books/v3"


class Contacts(SyncResource):
    """Sync contacts (customers & vendors)."""

    _api_prefix = _PREFIX
    _resource = "contacts"

    def mark_active(self, contact_id: str) -> dict[str, Any]:
        return self._action_post(contact_id, "active")

    def mark_inactive(self, contact_id: str) -> dict[str, Any]:
        return self._action_post(contact_id, "inactive")

    def enable_portal(self, contact_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._action_post(contact_id, "portal/enable", data)

    def enable_payment_reminders(self, contact_id: str) -> dict[str, Any]:
        return self._action_post(contact_id, "paymentreminder/enable")

    def disable_payment_reminders(self, contact_id: str) -> dict[str, Any]:
        return self._action_post(contact_id, "paymentreminder/disable")

    def email_statement(self, contact_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._action_post(contact_id, "statements/email", data)

    def list_comments(self, contact_id: str) -> dict[str, Any]:
        return self._action_get(contact_id, "comments")

    def list_addresses(self, contact_id: str) -> dict[str, Any]:
        return self._action_get(contact_id, "address")

    def add_address(self, contact_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._action_post(contact_id, "address", data)

    def email_contact(self, contact_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._action_post(contact_id, "email", data)

    def edit_address(
        self,
        contact_id: str,
        address_id: str,
        data: dict[str, Any],
    ) -> dict[str, Any]:
        return self._client.put(
            self._path(contact_id, "address", address_id),
            json=data,
        )

    def delete_address(self, contact_id: str, address_id: str) -> dict[str, Any]:
        return self._client.delete(self._path(contact_id, "address", address_id))

    def list_refunds(self, contact_id: str) -> dict[str, Any]:
        return self._action_get(contact_id, "refunds")

    def track_1099(self, contact_id: str) -> dict[str, Any]:
        return self._action_post(contact_id, "track1099")

    def untrack_1099(self, contact_id: str) -> dict[str, Any]:
        return self._action_post(contact_id, "untrack1099")

    def get_unused_retainer_payments(self, contact_id: str) -> dict[str, Any]:
        return self._action_get(contact_id, "retainerpayments/unused")


class AsyncContacts(AsyncResource):
    """Async contacts (customers & vendors)."""

    _api_prefix = _PREFIX
    _resource = "contacts"

    async def mark_active(self, contact_id: str) -> dict[str, Any]:
        return await self._action_post(contact_id, "active")

    async def mark_inactive(self, contact_id: str) -> dict[str, Any]:
        return await self._action_post(contact_id, "inactive")

    async def enable_portal(self, contact_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._action_post(contact_id, "portal/enable", data)

    async def enable_payment_reminders(self, contact_id: str) -> dict[str, Any]:
        return await self._action_post(contact_id, "paymentreminder/enable")

    async def disable_payment_reminders(self, contact_id: str) -> dict[str, Any]:
        return await self._action_post(contact_id, "paymentreminder/disable")

    async def email_statement(self, contact_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._action_post(contact_id, "statements/email", data)

    async def list_comments(self, contact_id: str) -> dict[str, Any]:
        return await self._action_get(contact_id, "comments")

    async def list_addresses(self, contact_id: str) -> dict[str, Any]:
        return await self._action_get(contact_id, "address")

    async def add_address(self, contact_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._action_post(contact_id, "address", data)

    async def email_contact(self, contact_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._action_post(contact_id, "email", data)

    async def edit_address(
        self,
        contact_id: str,
        address_id: str,
        data: dict[str, Any],
    ) -> dict[str, Any]:
        return await self._client.put(
            self._path(contact_id, "address", address_id),
            json=data,
        )

    async def delete_address(self, contact_id: str, address_id: str) -> dict[str, Any]:
        return await self._client.delete(self._path(contact_id, "address", address_id))

    async def list_refunds(self, contact_id: str) -> dict[str, Any]:
        return await self._action_get(contact_id, "refunds")

    async def track_1099(self, contact_id: str) -> dict[str, Any]:
        return await self._action_post(contact_id, "track1099")

    async def untrack_1099(self, contact_id: str) -> dict[str, Any]:
        return await self._action_post(contact_id, "untrack1099")

    async def get_unused_retainer_payments(self, contact_id: str) -> dict[str, Any]:
        return await self._action_get(contact_id, "retainerpayments/unused")

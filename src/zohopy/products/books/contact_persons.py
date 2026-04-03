"""Contact Persons. Ref: https://www.zoho.com/books/api/v3/contact-persons/"""

from __future__ import annotations

from typing import Any

from zohopy.products._base import AsyncResource, SyncResource

_P = "/books/v3"


class ContactPersons(SyncResource):
    _api_prefix, _resource = _P, "contacts"

    def create_for_contact(self, contact_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._client.post(self._path(contact_id, "contactpersons"), json=data)

    def list_for_contact(self, contact_id: str, **params: Any) -> dict[str, Any]:
        return self._client.get(self._path(contact_id, "contactpersons"), params=params or None)

    def get_for_contact(self, contact_id: str, person_id: str) -> dict[str, Any]:
        return self._client.get(self._path(contact_id, "contactpersons", person_id))

    def update_for_contact(
        self, contact_id: str, person_id: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        return self._client.put(self._path(contact_id, "contactpersons", person_id), json=data)

    def delete_for_contact(self, contact_id: str, person_id: str) -> dict[str, Any]:
        return self._client.delete(self._path(contact_id, "contactpersons", person_id))

    def mark_primary(self, contact_id: str, person_id: str) -> dict[str, Any]:
        return self._client.post(self._path(contact_id, "contactpersons", person_id, "primary"))


class AsyncContactPersons(AsyncResource):
    _api_prefix, _resource = _P, "contacts"

    async def create_for_contact(self, contact_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._client.post(self._path(contact_id, "contactpersons"), json=data)

    async def list_for_contact(self, contact_id: str, **params: Any) -> dict[str, Any]:
        return await self._client.get(
            self._path(contact_id, "contactpersons"), params=params or None
        )

    async def get_for_contact(self, contact_id: str, person_id: str) -> dict[str, Any]:
        return await self._client.get(self._path(contact_id, "contactpersons", person_id))

    async def update_for_contact(
        self, contact_id: str, person_id: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        return await self._client.put(
            self._path(contact_id, "contactpersons", person_id), json=data
        )

    async def delete_for_contact(self, contact_id: str, person_id: str) -> dict[str, Any]:
        return await self._client.delete(self._path(contact_id, "contactpersons", person_id))

    async def mark_primary(self, contact_id: str, person_id: str) -> dict[str, Any]:
        return await self._client.post(
            self._path(contact_id, "contactpersons", person_id, "primary")
        )

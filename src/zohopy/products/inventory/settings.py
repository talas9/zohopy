"""Inventory Settings — Organizations, Taxes, Locations, Price Lists."""

from __future__ import annotations

from typing import Any

from zohopy.products._base import AsyncResource, SyncResource

_P = "/inventory/v1"


class InvOrganizations(SyncResource):
    _api_prefix, _resource = _P, "organizations"


class AsyncInvOrganizations(AsyncResource):
    _api_prefix, _resource = _P, "organizations"


class InvTaxes(SyncResource):
    _api_prefix, _resource = _P, "taxes"


class AsyncInvTaxes(AsyncResource):
    _api_prefix, _resource = _P, "taxes"


class Locations(SyncResource):
    _api_prefix, _resource = _P, "locations"

    def mark_active(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "active")

    def mark_inactive(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "inactive")

    def mark_primary(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "primary")


class AsyncLocations(AsyncResource):
    _api_prefix, _resource = _P, "locations"

    async def mark_active(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "active")

    async def mark_inactive(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "inactive")

    async def mark_primary(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "primary")


class PriceLists(SyncResource):
    _api_prefix, _resource = _P, "pricebooks"

    def mark_active(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "active")

    def mark_inactive(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "inactive")


class AsyncPriceLists(AsyncResource):
    _api_prefix, _resource = _P, "pricebooks"

    async def mark_active(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "active")

    async def mark_inactive(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "inactive")

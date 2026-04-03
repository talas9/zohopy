"""Composite Items. Ref: https://www.zoho.com/inventory/api/v1/compositeitems/"""

from __future__ import annotations

from typing import Any

from zohopy.products._base import AsyncResource, SyncResource

_P = "/inventory/v1"


class CompositeItems(SyncResource):
    _api_prefix, _resource = _P, "compositeitems"

    def mark_active(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "active")

    def mark_inactive(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "inactive")

    def create_assembly(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._action_post(id, "assemblies", data)

    def list_assemblies(self, id: str) -> dict[str, Any]:
        return self._action_get(id, "assemblies")


class AsyncCompositeItems(AsyncResource):
    _api_prefix, _resource = _P, "compositeitems"

    async def mark_active(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "active")

    async def mark_inactive(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "inactive")

    async def create_assembly(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._action_post(id, "assemblies", data)

    async def list_assemblies(self, id: str) -> dict[str, Any]:
        return await self._action_get(id, "assemblies")

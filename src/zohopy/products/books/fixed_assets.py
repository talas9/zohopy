"""Fixed Assets. Ref: https://www.zoho.com/books/api/v3/fixed-assets/"""

from __future__ import annotations

from typing import Any

from zohopy.products._base import AsyncResource, SyncResource

_P = "/books/v3"


class FixedAssets(SyncResource):
    _api_prefix, _resource = _P, "fixedassets"

    def mark_active(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "active")

    def cancel(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "cancel")

    def mark_draft(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "status/draft")

    def write_off(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._action_post(id, "writeoff", data)

    def sell(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._action_post(id, "sell", data)

    def list_history(self, id: str) -> dict[str, Any]:
        return self._action_get(id, "history")

    def list_comments(self, id: str) -> dict[str, Any]:
        return self._action_get(id, "comments")

    def get_forecast_depreciation(self, id: str) -> dict[str, Any]:
        return self._action_get(id, "depreciation/forecast")

    def add_comment(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._action_post(id, "comments", data)

    def delete_comment(self, id: str, comment_id: str) -> dict[str, Any]:
        return self._client.delete(self._path(id, "comments", comment_id))


class AsyncFixedAssets(AsyncResource):
    _api_prefix, _resource = _P, "fixedassets"

    async def mark_active(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "active")

    async def cancel(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "cancel")

    async def mark_draft(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "status/draft")

    async def write_off(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._action_post(id, "writeoff", data)

    async def sell(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._action_post(id, "sell", data)

    async def list_history(self, id: str) -> dict[str, Any]:
        return await self._action_get(id, "history")

    async def list_comments(self, id: str) -> dict[str, Any]:
        return await self._action_get(id, "comments")

    async def get_forecast_depreciation(self, id: str) -> dict[str, Any]:
        return await self._action_get(id, "depreciation/forecast")

    async def add_comment(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._action_post(id, "comments", data)

    async def delete_comment(self, id: str, comment_id: str) -> dict[str, Any]:
        return await self._client.delete(self._path(id, "comments", comment_id))

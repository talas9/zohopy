"""Reporting Tags. Ref: https://www.zoho.com/books/api/v3/reporting-tags/"""

from __future__ import annotations

from typing import Any

from zohopy.products._base import AsyncResource, SyncResource

_P = "/books/v3"


class ReportingTags(SyncResource):
    _api_prefix, _resource = _P, "reportingtags"

    def mark_active(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "active")

    def mark_inactive(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "inactive")

    def mark_default_option(self, id: str, option_id: str) -> dict[str, Any]:
        return self._client.post(
            self._path(
                id,
                "tagoptions",
                option_id,
                "markasdefault",
            )
        )

    def update_options(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._client.put(self._path(id, "tagoptions"), json=data)

    def update_visibility(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._client.put(self._path(id, "visibility"), json=data)

    def mark_option_active(self, id: str, option_id: str) -> dict[str, Any]:
        return self._client.post(self._path(id, "tagoptions", option_id, "active"))

    def mark_option_inactive(self, id: str, option_id: str) -> dict[str, Any]:
        return self._client.post(self._path(id, "tagoptions", option_id, "inactive"))

    def get_options_detail(self, id: str) -> dict[str, Any]:
        return self._action_get(id, "tagoptions")

    def get_all_options(self, **params: Any) -> dict[str, Any]:
        return self._client.get(
            self._path("tagoptions"),
            params=params or None,
        )

    def reorder(self, data: dict[str, Any]) -> dict[str, Any]:
        return self._sub_post("reorder", data)


class AsyncReportingTags(AsyncResource):
    _api_prefix, _resource = _P, "reportingtags"

    async def mark_active(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "active")

    async def mark_inactive(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "inactive")

    async def mark_default_option(self, id: str, option_id: str) -> dict[str, Any]:
        return await self._client.post(
            self._path(
                id,
                "tagoptions",
                option_id,
                "markasdefault",
            )
        )

    async def update_options(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._client.put(self._path(id, "tagoptions"), json=data)

    async def update_visibility(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._client.put(self._path(id, "visibility"), json=data)

    async def mark_option_active(self, id: str, option_id: str) -> dict[str, Any]:
        return await self._client.post(self._path(id, "tagoptions", option_id, "active"))

    async def mark_option_inactive(self, id: str, option_id: str) -> dict[str, Any]:
        return await self._client.post(self._path(id, "tagoptions", option_id, "inactive"))

    async def get_options_detail(self, id: str) -> dict[str, Any]:
        return await self._action_get(id, "tagoptions")

    async def get_all_options(self, **params: Any) -> dict[str, Any]:
        return await self._client.get(
            self._path("tagoptions"),
            params=params or None,
        )

    async def reorder(self, data: dict[str, Any]) -> dict[str, Any]:
        return await self._sub_post("reorder", data)

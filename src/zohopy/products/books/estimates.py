"""Estimates. Ref: https://www.zoho.com/books/api/v3/estimates/"""

from __future__ import annotations

from typing import Any

from zohopy.products._base import AsyncResource, SyncResource

_P = "/books/v3"


class Estimates(SyncResource):
    _api_prefix, _resource = _P, "estimates"

    def mark_sent(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "status/sent")

    def mark_accepted(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "status/accepted")

    def mark_declined(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "status/declined")

    def submit_for_approval(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "submit")

    def approve(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "approve")

    def email(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._action_post(id, "email", data)

    def list_comments(self, id: str) -> dict[str, Any]:
        return self._action_get(id, "comments")

    def add_comment(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._action_post(id, "comments", data)

    def get_email_content(self, id: str, **params: Any) -> dict[str, Any]:
        return self._action_get(id, "email", **params)

    def email_multiple(self, data: dict[str, Any]) -> dict[str, Any]:
        return self._sub_post("email", data)

    def update_billing_address(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._action_post(id, "address/billing", data)

    def update_shipping_address(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._action_post(id, "address/shipping", data)

    def list_templates(self, id: str) -> dict[str, Any]:
        return self._action_get(id, "templates")

    def update_template(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._action_post(id, "templates", data)

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


class AsyncEstimates(AsyncResource):
    _api_prefix, _resource = _P, "estimates"

    async def mark_sent(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "status/sent")

    async def mark_accepted(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "status/accepted")

    async def mark_declined(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "status/declined")

    async def submit_for_approval(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "submit")

    async def approve(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "approve")

    async def email(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._action_post(id, "email", data)

    async def list_comments(self, id: str) -> dict[str, Any]:
        return await self._action_get(id, "comments")

    async def add_comment(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._action_post(id, "comments", data)

    async def get_email_content(self, id: str, **params: Any) -> dict[str, Any]:
        return await self._action_get(id, "email", **params)

    async def email_multiple(self, data: dict[str, Any]) -> dict[str, Any]:
        return await self._sub_post("email", data)

    async def update_billing_address(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._action_post(id, "address/billing", data)

    async def update_shipping_address(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._action_post(id, "address/shipping", data)

    async def list_templates(self, id: str) -> dict[str, Any]:
        return await self._action_get(id, "templates")

    async def update_template(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._action_post(id, "templates", data)

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

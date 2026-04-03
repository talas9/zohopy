"""Purchase Orders. Ref: https://www.zoho.com/books/api/v3/purchase-order/"""

from __future__ import annotations

from typing import Any

from zohopy.products._base import AsyncResource, SyncResource

_P = "/books/v3"


class PurchaseOrders(SyncResource):
    _api_prefix, _resource = _P, "purchaseorders"

    def mark_open(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "status/open")

    def mark_billed(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "status/billed")

    def cancel(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "status/cancelled")

    def submit_for_approval(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "submit")

    def approve(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "approve")

    def email(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._action_post(id, "email", data)

    def list_comments(self, id: str) -> dict[str, Any]:
        return self._action_get(id, "comments")

    def get_email_content(self, id: str, **params: Any) -> dict[str, Any]:
        return self._action_get(id, "email", **params)

    def reject(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "status/reject")

    def update_billing_address(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._action_post(id, "address/billing", data)

    def list_templates(self, id: str) -> dict[str, Any]:
        return self._action_get(id, "templates")

    def update_template(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._action_post(id, "templates", data)

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


class AsyncPurchaseOrders(AsyncResource):
    _api_prefix, _resource = _P, "purchaseorders"

    async def mark_open(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "status/open")

    async def mark_billed(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "status/billed")

    async def cancel(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "status/cancelled")

    async def submit_for_approval(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "submit")

    async def approve(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "approve")

    async def email(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._action_post(id, "email", data)

    async def list_comments(self, id: str) -> dict[str, Any]:
        return await self._action_get(id, "comments")

    async def get_email_content(self, id: str, **params: Any) -> dict[str, Any]:
        return await self._action_get(id, "email", **params)

    async def reject(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "status/reject")

    async def update_billing_address(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._action_post(id, "address/billing", data)

    async def list_templates(self, id: str) -> dict[str, Any]:
        return await self._action_get(id, "templates")

    async def update_template(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._action_post(id, "templates", data)

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

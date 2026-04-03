"""Bank Transactions. Ref: https://www.zoho.com/books/api/v3/bank-transactions/"""

from __future__ import annotations

from typing import Any

from zohopy.products._base import AsyncResource, SyncResource

_P = "/books/v3"


class BankTransactions(SyncResource):
    _api_prefix, _resource = _P, "banktransactions"

    def match(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._action_post(id, "match", data)

    def unmatch(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "unmatch")

    def exclude(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "exclude")

    def restore(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "restore")

    def categorize(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._action_post(id, "categorize", data)

    def uncategorize(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "uncategorize")

    def get_matching(self, id: str, **params: Any) -> dict[str, Any]:
        return self._action_get(id, "matching", **params)

    def categorize_as_expense(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._action_post(id, "categorize/expense", data)

    def categorize_as_vendor_payment(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._action_post(id, "categorize/vendorpayment", data)

    def categorize_as_customer_payment(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._action_post(id, "categorize/customerpayment", data)

    def categorize_as_cn_refund(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._action_post(id, "categorize/creditnoterefunds", data)

    def categorize_as_vc_refund(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._action_post(id, "categorize/vendorcreditrefunds", data)

    def categorize_as_cp_refund(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._action_post(id, "categorize/customerpaymentrefund", data)

    def categorize_as_vp_refund(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._action_post(id, "categorize/vendorpaymentrefund", data)


class AsyncBankTransactions(AsyncResource):
    _api_prefix, _resource = _P, "banktransactions"

    async def match(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._action_post(id, "match", data)

    async def unmatch(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "unmatch")

    async def exclude(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "exclude")

    async def restore(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "restore")

    async def categorize(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._action_post(id, "categorize", data)

    async def uncategorize(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "uncategorize")

    async def get_matching(self, id: str, **params: Any) -> dict[str, Any]:
        return await self._action_get(id, "matching", **params)

    async def categorize_as_expense(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._action_post(id, "categorize/expense", data)

    async def categorize_as_vendor_payment(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._action_post(id, "categorize/vendorpayment", data)

    async def categorize_as_customer_payment(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._action_post(id, "categorize/customerpayment", data)

    async def categorize_as_cn_refund(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._action_post(id, "categorize/creditnoterefunds", data)

    async def categorize_as_vc_refund(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._action_post(id, "categorize/vendorcreditrefunds", data)

    async def categorize_as_cp_refund(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._action_post(id, "categorize/customerpaymentrefund", data)

    async def categorize_as_vp_refund(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._action_post(id, "categorize/vendorpaymentrefund", data)

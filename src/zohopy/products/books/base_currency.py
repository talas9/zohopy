"""Base Currency Adjustments. Ref: https://www.zoho.com/books/api/v3/base-currency-adjustment/"""

from __future__ import annotations

from typing import Any

from zohopy.products._base import AsyncResource, SyncResource

_P = "/books/v3"


class BaseCurrencyAdjustments(SyncResource):
    _api_prefix, _resource = _P, "basecurrencyadjustment"

    def list_account_details(self, **params: Any) -> dict[str, Any]:
        return self._client.get(
            self._path("accountdetails"),
            params=params or None,
        )


class AsyncBaseCurrencyAdjustments(AsyncResource):
    _api_prefix, _resource = _P, "basecurrencyadjustment"

    async def list_account_details(self, **params: Any) -> dict[str, Any]:
        return await self._client.get(
            self._path("accountdetails"),
            params=params or None,
        )

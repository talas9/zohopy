"""Bank Rules. Ref: https://www.zoho.com/books/api/v3/bank-rules/"""

from __future__ import annotations

from zohopy.products._base import AsyncResource, SyncResource

_P = "/books/v3"


class BankRules(SyncResource):
    _api_prefix, _resource = _P, "bankrules"


class AsyncBankRules(AsyncResource):
    _api_prefix, _resource = _P, "bankrules"

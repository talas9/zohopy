"""Customer Debit Notes. Ref: https://www.zoho.com/books/api/v3/customer-debit-notes/"""

from __future__ import annotations

from zohopy.products._base import AsyncResource, SyncResource

_P = "/books/v3"


class CustomerDebitNotes(SyncResource):
    _api_prefix, _resource = _P, "customerdebitnotes"


class AsyncCustomerDebitNotes(AsyncResource):
    _api_prefix, _resource = _P, "customerdebitnotes"

"""Packages. Ref: https://www.zoho.com/books/api/v3/"""

from __future__ import annotations

from zohopy.products._base import AsyncResource, SyncResource

_P = "/books/v3"


class Packages(SyncResource):
    _api_prefix, _resource = _P, "packages"


class AsyncPackages(AsyncResource):
    _api_prefix, _resource = _P, "packages"

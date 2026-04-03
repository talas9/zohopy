"""Packages. Ref: https://www.zoho.com/inventory/api/v1/packages/"""

from __future__ import annotations

from zohopy.products._base import AsyncResource, SyncResource

_P = "/inventory/v1"


class Packages(SyncResource):
    _api_prefix, _resource = _P, "packages"


class AsyncPackages(AsyncResource):
    _api_prefix, _resource = _P, "packages"

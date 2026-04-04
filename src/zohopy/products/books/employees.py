"""Employees. Ref: https://www.zoho.com/books/api/v3/"""

from __future__ import annotations

from zohopy.products._base import AsyncResource, SyncResource

_P = "/books/v3"


class Employees(SyncResource):
    _api_prefix, _resource = _P, "employees"


class AsyncEmployees(AsyncResource):
    _api_prefix, _resource = _P, "employees"

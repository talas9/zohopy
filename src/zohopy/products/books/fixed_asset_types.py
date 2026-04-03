"""Fixed Asset Types. Ref: https://www.zoho.com/books/api/v3/fixed-assets/"""

from __future__ import annotations

from zohopy.products._base import AsyncResource, SyncResource

_P = "/books/v3"


class FixedAssetTypes(SyncResource):
    _api_prefix, _resource = _P, "fixedassettypes"


class AsyncFixedAssetTypes(AsyncResource):
    _api_prefix, _resource = _P, "fixedassettypes"

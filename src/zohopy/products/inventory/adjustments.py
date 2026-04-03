"""Item Adjustments. Ref: https://www.zoho.com/inventory/api/v1/itemadjustments/"""

from __future__ import annotations

from zohopy.products._base import AsyncResource, SyncResource

_P = "/inventory/v1"


class ItemAdjustments(SyncResource):
    _api_prefix, _resource = _P, "inventoryadjustments"


class AsyncItemAdjustments(AsyncResource):
    _api_prefix, _resource = _P, "inventoryadjustments"

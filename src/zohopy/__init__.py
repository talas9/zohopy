"""ZohoPy — Modern, async-ready Python client for Zoho APIs.

Supports Zoho Books (v3) and Zoho Inventory (v1) with both
synchronous and asynchronous interfaces.

Quick start (sync)::

    from zohopy import ZohoConfig, SyncZohoClient
    from zohopy.products.books import ZohoBooks

    config = ZohoConfig()  # reads from ZOHO_* env vars
    with SyncZohoClient(config) as client:
        books = ZohoBooks(client)
        print(books.contacts.list())

Quick start (async)::

    import asyncio
    from zohopy import ZohoConfig, AsyncZohoClient
    from zohopy.products.books import AsyncZohoBooks

    async def main():
        config = ZohoConfig()
        async with AsyncZohoClient(config) as client:
            books = AsyncZohoBooks(client)
            print(await books.contacts.list())

    asyncio.run(main())
"""

from zohopy._client import AsyncZohoClient, SyncZohoClient
from zohopy.config import DataCenter, ZohoConfig
from zohopy.exceptions import (
    ZohoAPIError,
    ZohoAuthenticationError,
    ZohoBusinessRuleError,
    ZohoDuplicateError,
    ZohoEmptyBodyError,
    ZohoError,
    ZohoErrorCode,
    ZohoFeatureNotEnabledError,
    ZohoForbiddenError,
    ZohoInvalidFieldError,
    ZohoNotFoundError,
    ZohoRateLimitError,
    ZohoResourceDependentError,
    ZohoServerError,
    ZohoTokenRefreshError,
    ZohoValidationError,
)
from zohopy.logging import configure_logging, get_logger

__all__ = [
    "AsyncZohoClient",
    "DataCenter",
    "SyncZohoClient",
    "ZohoAPIError",
    "ZohoAuthenticationError",
    "ZohoBusinessRuleError",
    "ZohoConfig",
    "ZohoDuplicateError",
    "ZohoEmptyBodyError",
    "ZohoError",
    "ZohoErrorCode",
    "ZohoFeatureNotEnabledError",
    "ZohoForbiddenError",
    "ZohoInvalidFieldError",
    "ZohoNotFoundError",
    "ZohoRateLimitError",
    "ZohoResourceDependentError",
    "ZohoServerError",
    "ZohoTokenRefreshError",
    "ZohoValidationError",
    "configure_logging",
    "get_logger",
]

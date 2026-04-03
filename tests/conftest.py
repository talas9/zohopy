"""Shared test fixtures."""

from __future__ import annotations

import httpx
import pytest
import respx

from zohopy._client import AsyncZohoClient, SyncZohoClient
from zohopy.config import DataCenter, ZohoConfig


@pytest.fixture
def config() -> ZohoConfig:
    """Test config with dummy credentials."""
    return ZohoConfig(
        client_id="test_client_id",
        client_secret="test_client_secret",
        refresh_token="test_refresh_token",
        organization_id="12345",
        data_center=DataCenter.US,
        timeout=5.0,
        max_retries=1,
    )


@pytest.fixture
def mock_token(respx_mock: respx.MockRouter) -> respx.MockRouter:
    """Mock the OAuth token refresh endpoint."""
    respx_mock.post("https://accounts.zoho.com/oauth/v2/token").mock(
        return_value=httpx.Response(
            200,
            json={
                "access_token": "test_access_token",
                "token_type": "Bearer",
                "expires_in": 3600,
            },
        )
    )
    return respx_mock


@pytest.fixture
def sync_client(config: ZohoConfig, mock_token: respx.MockRouter) -> SyncZohoClient:
    """Sync client with mocked auth."""
    client = SyncZohoClient(config)
    yield client
    client.close()


@pytest.fixture
async def async_client(config: ZohoConfig, mock_token: respx.MockRouter) -> AsyncZohoClient:
    """Async client with mocked auth."""
    client = AsyncZohoClient(config)
    yield client
    await client.close()

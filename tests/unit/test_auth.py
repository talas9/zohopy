"""Tests for OAuth token management."""

from __future__ import annotations

import httpx
import pytest
import respx

from zohopy._auth import SyncAuth
from zohopy.config import DataCenter, ZohoConfig
from zohopy.exceptions import ZohoTokenRefreshError


@pytest.fixture
def cfg() -> ZohoConfig:
    return ZohoConfig(
        client_id="cid",
        client_secret="csec",
        refresh_token="rt",
        organization_id="org",
        data_center=DataCenter.US,
    )


@respx.mock
def test_refresh_success(cfg: ZohoConfig):
    respx.post("https://accounts.zoho.com/oauth/v2/token").mock(
        return_value=httpx.Response(200, json={"access_token": "new_token", "expires_in": 3600})
    )
    auth = SyncAuth(cfg)
    headers = auth.get_headers()
    assert headers["Authorization"] == "Zoho-oauthtoken new_token"
    auth.close()


@respx.mock
def test_refresh_failure_raises(cfg: ZohoConfig):
    respx.post("https://accounts.zoho.com/oauth/v2/token").mock(
        return_value=httpx.Response(400, json={"error": "invalid_client"})
    )
    auth = SyncAuth(cfg)
    with pytest.raises(ZohoTokenRefreshError):
        auth.get_headers()
    auth.close()


@respx.mock
def test_token_reuse_on_second_call(cfg: ZohoConfig):
    route = respx.post("https://accounts.zoho.com/oauth/v2/token").mock(
        return_value=httpx.Response(200, json={"access_token": "cached", "expires_in": 3600})
    )
    auth = SyncAuth(cfg)
    auth.get_headers()
    auth.get_headers()
    # Token endpoint should only be called once
    assert route.call_count == 1
    auth.close()

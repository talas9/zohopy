"""Tests for OAuth setup / grant token exchange."""

from __future__ import annotations

import httpx
import pytest
import respx

from zohopy.config import DataCenter
from zohopy.exceptions import ZohoTokenRefreshError
from zohopy.setup import (
    discover_organizations,
    exchange_grant_token,
    resolve_accounts_url,
)


@respx.mock
def test_exchange_grant_token_success():
    respx.post("https://accounts.zoho.com/oauth/v2/token").mock(
        return_value=httpx.Response(
            200,
            json={
                "access_token": "at",
                "refresh_token": "rt_permanent",
                "api_domain": "https://www.zohoapis.com",
                "token_type": "Bearer",
                "expires_in": 3600,
            },
        )
    )
    result = exchange_grant_token(
        client_id="cid",
        client_secret="csec",
        grant_token="grant_code",
        accounts_url="https://accounts.zoho.com",
    )
    assert result["refresh_token"] == "rt_permanent"
    assert result["api_domain"] == "https://www.zohoapis.com"


@respx.mock
def test_exchange_grant_token_india():
    """India grant codes must be exchanged against accounts.zoho.in."""
    route = respx.post("https://accounts.zoho.in/oauth/v2/token").mock(
        return_value=httpx.Response(
            200,
            json={
                "access_token": "at",
                "refresh_token": "rt_in",
                "api_domain": "https://www.zohoapis.in",
                "token_type": "Bearer",
                "expires_in": 3600,
            },
        )
    )
    # Ensure we do NOT hit the US host
    respx.post("https://accounts.zoho.com/oauth/v2/token").mock(
        return_value=httpx.Response(200, json={"error": "invalid_code"})
    )
    result = exchange_grant_token(
        client_id="cid",
        client_secret="csec",
        grant_token="grant_code",
        accounts_url="https://accounts.zoho.in",
    )
    assert result["refresh_token"] == "rt_in"
    assert result["api_domain"] == "https://www.zohoapis.in"
    assert "accounts.zoho.in" in str(route.calls[0].request.url)


@respx.mock
def test_exchange_grant_token_error():
    respx.post("https://accounts.zoho.com/oauth/v2/token").mock(
        return_value=httpx.Response(200, json={"error": "invalid_code"})
    )
    with pytest.raises(ZohoTokenRefreshError, match="invalid_code"):
        exchange_grant_token(
            client_id="cid",
            client_secret="csec",
            grant_token="expired_code",
        )


@respx.mock
def test_exchange_grant_token_no_refresh():
    respx.post("https://accounts.zoho.com/oauth/v2/token").mock(
        return_value=httpx.Response(
            200,
            json={"access_token": "at", "api_domain": "https://www.zohoapis.com"},
        )
    )
    with pytest.raises(ZohoTokenRefreshError, match="No refresh_token"):
        exchange_grant_token(
            client_id="cid",
            client_secret="csec",
            grant_token="code",
        )


@respx.mock
def test_exchange_grant_token_http_failure():
    respx.post("https://accounts.zoho.com/oauth/v2/token").mock(
        return_value=httpx.Response(500, text="server error")
    )
    with pytest.raises(ZohoTokenRefreshError, match="500"):
        exchange_grant_token(
            client_id="cid",
            client_secret="csec",
            grant_token="code",
        )


@respx.mock
def test_discover_organizations():
    respx.get("https://www.zohoapis.com/books/v3/organizations").mock(
        return_value=httpx.Response(
            200,
            json={
                "organizations": [
                    {"organization_id": "12345", "name": "Test Org"},
                ]
            },
        )
    )
    orgs = discover_organizations(
        access_token="at",
        api_domain="https://www.zohoapis.com",
    )
    assert len(orgs) == 1
    assert orgs[0]["organization_id"] == "12345"


@respx.mock
def test_exchange_with_redirect_uri():
    """Server-based flow includes redirect_uri in the exchange."""
    route = respx.post("https://accounts.zoho.com/oauth/v2/token").mock(
        return_value=httpx.Response(
            200,
            json={
                "access_token": "at",
                "refresh_token": "rt",
                "api_domain": "https://www.zohoapis.com",
                "expires_in": 3600,
            },
        )
    )
    result = exchange_grant_token(
        client_id="cid",
        client_secret="csec",
        grant_token="code",
        redirect_uri="http://localhost:11470/callback",
    )
    assert result["refresh_token"] == "rt"
    # Verify redirect_uri was sent
    req_url = str(route.calls[0].request.url)
    assert "redirect_uri" in req_url


def test_resolve_accounts_url_prefers_accounts_server():
    assert (
        resolve_accounts_url(
            accounts_server="https://accounts.zoho.in/",
            location="us",
            fallback="https://accounts.zoho.com",
        )
        == "https://accounts.zoho.in"
    )


def test_resolve_accounts_url_from_location():
    assert (
        resolve_accounts_url(location="in", fallback="https://accounts.zoho.com")
        == DataCenter.IN.accounts_url
    )
    assert (
        resolve_accounts_url(location="eu", fallback="https://accounts.zoho.com")
        == DataCenter.EU.accounts_url
    )


def test_resolve_accounts_url_fallback():
    assert (
        resolve_accounts_url(location="nope", fallback="https://accounts.zoho.com")
        == "https://accounts.zoho.com"
    )
    assert resolve_accounts_url() == "https://accounts.zoho.com"

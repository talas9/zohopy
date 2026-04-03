"""Tests for sync and async HTTP clients."""

from __future__ import annotations

import httpx
import pytest
import respx

from zohopy._client import SyncZohoClient
from zohopy.config import DataCenter, ZohoConfig
from zohopy.exceptions import (
    ZohoDuplicateError,
    ZohoInvalidFieldError,
    ZohoNotFoundError,
    ZohoServerError,
    ZohoValidationError,
)


@pytest.fixture
def cfg() -> ZohoConfig:
    return ZohoConfig(
        client_id="cid",
        client_secret="csec",
        refresh_token="rt",
        organization_id="org",
        data_center=DataCenter.US,
        max_retries=0,
    )


@respx.mock
def test_get_success(cfg: ZohoConfig):
    # Mock token
    respx.post("https://accounts.zoho.com/oauth/v2/token").mock(
        return_value=httpx.Response(200, json={"access_token": "tok", "expires_in": 3600})
    )
    # Mock API
    respx.get("https://www.zohoapis.com/books/v3/contacts").mock(
        return_value=httpx.Response(200, json={"contacts": [], "code": 0, "message": "success"})
    )

    with SyncZohoClient(cfg) as client:
        data = client.get("/books/v3/contacts")
    assert data["code"] == 0


@respx.mock
def test_404_raises_not_found(cfg: ZohoConfig):
    respx.post("https://accounts.zoho.com/oauth/v2/token").mock(
        return_value=httpx.Response(200, json={"access_token": "tok", "expires_in": 3600})
    )
    respx.get("https://www.zohoapis.com/books/v3/contacts/bad_id").mock(
        return_value=httpx.Response(404, json={"code": 1002, "message": "not found"})
    )

    with SyncZohoClient(cfg) as client, pytest.raises(ZohoNotFoundError):
        client.get("/books/v3/contacts/bad_id")


@respx.mock
def test_400_raises_validation(cfg: ZohoConfig):
    respx.post("https://accounts.zoho.com/oauth/v2/token").mock(
        return_value=httpx.Response(200, json={"access_token": "tok", "expires_in": 3600})
    )
    respx.post("https://www.zohoapis.com/books/v3/contacts").mock(
        return_value=httpx.Response(400, json={"code": 1001, "message": "missing field"})
    )

    with SyncZohoClient(cfg) as client, pytest.raises(ZohoValidationError):
        client.post("/books/v3/contacts", json={"bad": "data"})


@respx.mock
def test_org_id_injected(cfg: ZohoConfig):
    respx.post("https://accounts.zoho.com/oauth/v2/token").mock(
        return_value=httpx.Response(200, json={"access_token": "tok", "expires_in": 3600})
    )
    route = respx.get("https://www.zohoapis.com/books/v3/items").mock(
        return_value=httpx.Response(200, json={"items": []})
    )

    with SyncZohoClient(cfg) as client:
        client.get("/books/v3/items")

    # Verify organization_id was included in query params
    assert "organization_id=org" in str(route.calls[0].request.url)


@respx.mock
def test_400_code_2_raises_invalid_field(cfg: ZohoConfig):
    respx.post("https://accounts.zoho.com/oauth/v2/token").mock(
        return_value=httpx.Response(200, json={"access_token": "tok", "expires_in": 3600})
    )
    respx.post("https://www.zohoapis.com/books/v3/contacts").mock(
        return_value=httpx.Response(
            400, json={"code": 2, "message": "Invalid value passed for contact_type"}
        )
    )

    with SyncZohoClient(cfg) as client:
        with pytest.raises(ZohoInvalidFieldError) as exc_info:
            client.post("/books/v3/contacts", json={"contact_type": "bad"})
        assert exc_info.value.field_name == "contact_type"
        # Also catchable as ZohoValidationError
        assert isinstance(exc_info.value, ZohoValidationError)


@respx.mock
def test_400_code_4_raises_duplicate(cfg: ZohoConfig):
    respx.post("https://accounts.zoho.com/oauth/v2/token").mock(
        return_value=httpx.Response(200, json={"access_token": "tok", "expires_in": 3600})
    )
    respx.post("https://www.zohoapis.com/books/v3/settings/currencies").mock(
        return_value=httpx.Response(400, json={"code": 4, "message": "CurrencyCode already exists"})
    )

    with SyncZohoClient(cfg) as client, pytest.raises(ZohoDuplicateError):
        client.post("/books/v3/settings/currencies", json={"currency_code": "USD"})


@respx.mock
def test_500_raises_server_error(cfg: ZohoConfig):
    respx.post("https://accounts.zoho.com/oauth/v2/token").mock(
        return_value=httpx.Response(200, json={"access_token": "tok", "expires_in": 3600})
    )
    respx.get("https://www.zohoapis.com/books/v3/contacts").mock(
        return_value=httpx.Response(500, json={"code": 0, "message": "Internal error"})
    )

    with SyncZohoClient(cfg) as client, pytest.raises(ZohoServerError):
        client.get("/books/v3/contacts")

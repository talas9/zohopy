"""Tests for Zoho Books product module."""

from __future__ import annotations

import httpx
import respx

from zohopy._client import SyncZohoClient
from zohopy.config import DataCenter, ZohoConfig
from zohopy.products.books import ZohoBooks


def _cfg() -> ZohoConfig:
    return ZohoConfig(
        client_id="c",
        client_secret="s",
        refresh_token="r",
        organization_id="org",
        data_center=DataCenter.US,
        max_retries=0,
    )


def _mock_token(mock: respx.MockRouter) -> None:
    mock.post("https://accounts.zoho.com/oauth/v2/token").mock(
        return_value=httpx.Response(200, json={"access_token": "t", "expires_in": 3600})
    )


@respx.mock
def test_contacts_list():
    _mock_token(respx)
    respx.get("https://www.zohoapis.com/books/v3/contacts").mock(
        return_value=httpx.Response(200, json={"contacts": [{"contact_id": "1"}], "code": 0})
    )
    with SyncZohoClient(_cfg()) as client:
        books = ZohoBooks(client)
        data = books.contacts.list()
    assert data["contacts"][0]["contact_id"] == "1"


@respx.mock
def test_invoices_create():
    _mock_token(respx)
    respx.post("https://www.zohoapis.com/books/v3/invoices").mock(
        return_value=httpx.Response(201, json={"invoice": {"invoice_id": "inv1"}, "code": 0})
    )
    with SyncZohoClient(_cfg()) as client:
        books = ZohoBooks(client)
        data = books.invoices.create({"customer_id": "c1"})
    assert data["invoice"]["invoice_id"] == "inv1"


@respx.mock
def test_invoices_mark_sent():
    _mock_token(respx)
    respx.post("https://www.zohoapis.com/books/v3/invoices/inv1/status/sent").mock(
        return_value=httpx.Response(200, json={"code": 0, "message": "marked as sent"})
    )
    with SyncZohoClient(_cfg()) as client:
        books = ZohoBooks(client)
        data = books.invoices.mark_sent("inv1")
    assert data["code"] == 0


@respx.mock
def test_items_mark_active():
    _mock_token(respx)
    respx.post("https://www.zohoapis.com/books/v3/items/it1/active").mock(
        return_value=httpx.Response(200, json={"code": 0, "message": "active"})
    )
    with SyncZohoClient(_cfg()) as client:
        books = ZohoBooks(client)
        data = books.items.mark_active("it1")
    assert data["code"] == 0

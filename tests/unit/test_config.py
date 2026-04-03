"""Tests for ZohoConfig and DataCenter."""

import os
from unittest import mock

from zohopy.config import DataCenter, ZohoConfig


class TestDataCenter:
    def test_accounts_urls(self):
        assert DataCenter.US.accounts_url == "https://accounts.zoho.com"
        assert DataCenter.EU.accounts_url == "https://accounts.zoho.eu"
        assert DataCenter.SA.accounts_url == "https://accounts.zoho.sa"

    def test_api_urls(self):
        assert DataCenter.US.api_url == "https://www.zohoapis.com"
        assert DataCenter.IN.api_url == "https://www.zohoapis.in"
        assert DataCenter.AU.api_url == "https://www.zohoapis.com.au"

    def test_all_centers_have_urls(self):
        for dc in DataCenter:
            assert dc.accounts_url.startswith("https://")
            assert dc.api_url.startswith("https://")

    def test_from_api_domain(self):
        assert DataCenter.from_api_domain("https://www.zohoapis.com") == DataCenter.US
        assert DataCenter.from_api_domain("https://www.zohoapis.eu") == DataCenter.EU
        assert DataCenter.from_api_domain("https://www.zohoapis.sa") == DataCenter.SA

    def test_from_api_domain_trailing_slash(self):
        assert DataCenter.from_api_domain("https://www.zohoapis.in/") == DataCenter.IN

    def test_from_api_domain_unknown_raises(self):
        import pytest

        with pytest.raises(ValueError, match="Unknown"):
            DataCenter.from_api_domain("https://unknown.example.com")


class TestZohoConfig:
    def test_explicit_init(self):
        cfg = ZohoConfig(
            client_id="cid",
            client_secret="csec",
            refresh_token="rt",
            organization_id="org",
            data_center=DataCenter.EU,
            api_domain="",
            _env_file=None,  # type: ignore[call-arg]
        )
        assert cfg.client_id == "cid"
        assert cfg.accounts_url == "https://accounts.zoho.eu"
        assert cfg.base_api_url == "https://www.zohoapis.eu"

    def test_defaults(self):
        env_override = {
            "ZOHO_CLIENT_ID": "c",
            "ZOHO_CLIENT_SECRET": "s",
            "ZOHO_REFRESH_TOKEN": "",
            "ZOHO_ORGANIZATION_ID": "",
            "ZOHO_API_DOMAIN": "",
            "ZOHO_DATA_CENTER": "us",
        }
        with mock.patch.dict(os.environ, env_override, clear=False):
            cfg = ZohoConfig(
                client_id="c",
                client_secret="s",
                _env_file=None,  # type: ignore[call-arg]
            )
        assert cfg.data_center == DataCenter.US
        assert cfg.timeout == 30.0
        assert cfg.max_retries == 3

    def test_api_domain_auto_detects_dc(self):
        cfg = ZohoConfig(
            client_id="c",
            client_secret="s",
            api_domain="https://www.zohoapis.eu",
        )
        assert cfg.data_center == DataCenter.EU
        assert cfg.base_api_url == "https://www.zohoapis.eu"

    def test_api_domain_overrides_explicit_dc(self):
        cfg = ZohoConfig(
            client_id="c",
            client_secret="s",
            data_center=DataCenter.US,
            api_domain="https://www.zohoapis.in",
        )
        # api_domain wins
        assert cfg.data_center == DataCenter.IN

    def test_from_env(self):
        env = {
            "ZOHO_CLIENT_ID": "env_cid",
            "ZOHO_CLIENT_SECRET": "env_sec",
            "ZOHO_REFRESH_TOKEN": "env_rt",
            "ZOHO_ORGANIZATION_ID": "env_org",
            "ZOHO_API_DOMAIN": "https://www.zohoapis.eu",
        }
        with mock.patch.dict(os.environ, env, clear=False):
            cfg = ZohoConfig()
        assert cfg.client_id == "env_cid"
        assert cfg.data_center == DataCenter.EU

    def test_repr_no_secrets(self):
        cfg = ZohoConfig(
            client_id="c",
            client_secret="supersecret",
            organization_id="org123",
        )
        r = repr(cfg)
        assert "org123" in r
        assert "supersecret" not in r

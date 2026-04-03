"""Configuration and data-center definitions for Zoho APIs.

Supports loading from environment variables via ``pydantic-settings``
or direct instantiation. No credentials are ever hardcoded.

Data-center reference:
    https://www.zoho.com/books/api/v3/introduction/#multidc
"""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DataCenter(str, Enum):
    """Zoho data-center regions.

    Each region has its own OAuth accounts server and API domain.
    """

    US = "us"
    EU = "eu"
    IN = "in"
    AU = "au"
    JP = "jp"
    CA = "ca"
    CN = "cn"
    SA = "sa"

    # -- derived URLs -------------------------------------------------------

    @property
    def accounts_url(self) -> str:
        """OAuth server URL for this region."""
        return _ACCOUNTS_URLS[self]

    @property
    def api_url(self) -> str:
        """REST API base URL for this region."""
        return _API_URLS[self]

    @classmethod
    def from_api_domain(cls, api_domain: str) -> DataCenter:
        """Detect data center from the ``api_domain`` returned by Zoho OAuth.

        When you exchange a grant token for tokens, the response includes
        ``api_domain`` (e.g. ``"https://www.zohoapis.eu"``).  This method
        maps that back to the correct :class:`DataCenter`.

        Raises:
            ValueError: If the domain doesn't match any known data center.
        """
        domain = api_domain.rstrip("/").lower()
        for dc, url in _API_URLS.items():
            if domain == url:
                return dc
        msg = f"Unknown Zoho API domain: {api_domain!r}"
        raise ValueError(msg)


_ACCOUNTS_URLS: dict[DataCenter, str] = {
    DataCenter.US: "https://accounts.zoho.com",
    DataCenter.EU: "https://accounts.zoho.eu",
    DataCenter.IN: "https://accounts.zoho.in",
    DataCenter.AU: "https://accounts.zoho.com.au",
    DataCenter.JP: "https://accounts.zoho.jp",
    DataCenter.CA: "https://accounts.zohocloud.ca",
    DataCenter.CN: "https://accounts.zoho.com.cn",
    DataCenter.SA: "https://accounts.zoho.sa",
}

_API_URLS: dict[DataCenter, str] = {
    DataCenter.US: "https://www.zohoapis.com",
    DataCenter.EU: "https://www.zohoapis.eu",
    DataCenter.IN: "https://www.zohoapis.in",
    DataCenter.AU: "https://www.zohoapis.com.au",
    DataCenter.JP: "https://www.zohoapis.jp",
    DataCenter.CA: "https://www.zohoapis.ca",
    DataCenter.CN: "https://www.zohoapis.com.cn",
    DataCenter.SA: "https://www.zohoapis.sa",
}


class ZohoConfig(BaseSettings):
    """Connection configuration for Zoho APIs.

    Values are loaded automatically from environment variables prefixed
    with ``ZOHO_``, or from a ``.env`` file.

    Example:
        .. code-block:: python

            # Auto-load from ZOHO_CLIENT_ID, ZOHO_CLIENT_SECRET, …
            config = ZohoConfig()

            # Or explicit
            config = ZohoConfig(
                client_id="...",
                client_secret="...",
                refresh_token="...",
                organization_id="...",
                data_center=DataCenter.EU,
            )
    """

    model_config = SettingsConfigDict(
        env_prefix="ZOHO_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    client_id: str = Field(
        ...,
        repr=False,
        description="OAuth client ID from https://api-console.zoho.com/",
    )
    client_secret: str = Field(
        ...,
        repr=False,
        description="OAuth client secret",
    )
    refresh_token: str = Field(
        ...,
        repr=False,
        description="Long-lived OAuth refresh token",
    )
    organization_id: str = Field(
        ...,
        description="Zoho organization ID",
    )
    data_center: DataCenter = Field(
        ...,
        description="Zoho data-center region (us, eu, in, au, jp, ca, cn, sa)",
    )
    api_domain: str = Field(
        default="",
        repr=False,
        description="API domain (optional — overrides data_center if set)",
    )
    timeout: float = Field(
        default=30.0,
        ge=1.0,
        description="HTTP request timeout in seconds",
    )
    max_retries: int = Field(
        default=3,
        ge=0,
        le=10,
        description="Max retries on transient (429 / 5xx) failures",
    )
    retry_backoff: float = Field(
        default=1.0,
        ge=0.0,
        description="Base back-off multiplier between retries (seconds)",
    )

    def model_post_init(self, __context: Any) -> None:
        """Auto-detect data_center from api_domain if provided."""
        if self.api_domain:
            try:
                detected = DataCenter.from_api_domain(self.api_domain)
                object.__setattr__(self, "data_center", detected)
            except ValueError:
                pass  # keep the explicit/default data_center

    # -- convenience properties ---------------------------------------------

    @property
    def accounts_url(self) -> str:
        """OAuth accounts server URL for the configured data center."""
        return self.data_center.accounts_url

    @property
    def base_api_url(self) -> str:
        """API base URL for the configured data center."""
        return self.data_center.api_url

    def __repr__(self) -> str:
        return f"ZohoConfig(data_center={self.data_center.value!r}, org={self.organization_id!r})"

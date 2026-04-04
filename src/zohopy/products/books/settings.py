"""Settings: Organizations, Taxes, Currencies, Users, Preferences, Templates, etc.

Ref: https://www.zoho.com/books/api/v3/
"""

from __future__ import annotations

from typing import Any

from zohopy.products._base import AsyncResource, SyncResource

_P = "/books/v3"


class Organizations(SyncResource):
    _api_prefix, _resource = _P, "organizations"


class AsyncOrganizations(AsyncResource):
    _api_prefix, _resource = _P, "organizations"


class Taxes(SyncResource):
    _api_prefix, _resource = _P, "settings/taxes"

    def create_group(self, data: dict[str, Any]) -> dict[str, Any]:
        return self._sub_post("taxgroup", data)

    def get_group(self, group_id: str) -> dict[str, Any]:
        return self._client.get(self._path("taxgroup", group_id))

    def delete_group(self, group_id: str) -> dict[str, Any]:
        return self._client.delete(self._path("taxgroup", group_id))

    def create_authority(self, data: dict[str, Any]) -> dict[str, Any]:
        return self._client.post(self._path("taxauthorities"), json=data)

    def list_authorities(self, **params: Any) -> dict[str, Any]:
        return self._client.get(
            self._path("taxauthorities"),
            params=params or None,
        )

    def update_authority(self, auth_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._client.put(
            self._path("taxauthorities", auth_id),
            json=data,
        )

    def get_authority(self, auth_id: str) -> dict[str, Any]:
        return self._client.get(self._path("taxauthorities", auth_id))

    def delete_authority(self, auth_id: str) -> dict[str, Any]:
        return self._client.delete(self._path("taxauthorities", auth_id))

    def create_exemption(self, data: dict[str, Any]) -> dict[str, Any]:
        return self._client.post(self._path("taxexemptions"), json=data)

    def list_exemptions(self, **params: Any) -> dict[str, Any]:
        return self._client.get(
            self._path("taxexemptions"),
            params=params or None,
        )

    def update_exemption(self, exemption_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._client.put(
            self._path("taxexemptions", exemption_id),
            json=data,
        )

    def get_exemption(self, exemption_id: str) -> dict[str, Any]:
        return self._client.get(self._path("taxexemptions", exemption_id))

    def delete_exemption(self, exemption_id: str) -> dict[str, Any]:
        return self._client.delete(self._path("taxexemptions", exemption_id))


class AsyncTaxes(AsyncResource):
    _api_prefix, _resource = _P, "settings/taxes"

    async def create_group(self, data: dict[str, Any]) -> dict[str, Any]:
        return await self._client.post(self._path("taxgroup"), json=data)

    async def get_group(self, group_id: str) -> dict[str, Any]:
        return await self._client.get(self._path("taxgroup", group_id))

    async def delete_group(self, group_id: str) -> dict[str, Any]:
        return await self._client.delete(self._path("taxgroup", group_id))

    async def create_authority(self, data: dict[str, Any]) -> dict[str, Any]:
        return await self._client.post(self._path("taxauthorities"), json=data)

    async def list_authorities(self, **params: Any) -> dict[str, Any]:
        return await self._client.get(
            self._path("taxauthorities"),
            params=params or None,
        )

    async def update_authority(self, auth_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._client.put(
            self._path("taxauthorities", auth_id),
            json=data,
        )

    async def get_authority(self, auth_id: str) -> dict[str, Any]:
        return await self._client.get(self._path("taxauthorities", auth_id))

    async def delete_authority(self, auth_id: str) -> dict[str, Any]:
        return await self._client.delete(self._path("taxauthorities", auth_id))

    async def create_exemption(self, data: dict[str, Any]) -> dict[str, Any]:
        return await self._client.post(self._path("taxexemptions"), json=data)

    async def list_exemptions(self, **params: Any) -> dict[str, Any]:
        return await self._client.get(
            self._path("taxexemptions"),
            params=params or None,
        )

    async def update_exemption(self, exemption_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._client.put(
            self._path("taxexemptions", exemption_id),
            json=data,
        )

    async def get_exemption(self, exemption_id: str) -> dict[str, Any]:
        return await self._client.get(self._path("taxexemptions", exemption_id))

    async def delete_exemption(self, exemption_id: str) -> dict[str, Any]:
        return await self._client.delete(self._path("taxexemptions", exemption_id))


class Currencies(SyncResource):
    _api_prefix, _resource = _P, "settings/currencies"

    def list_exchange_rates(self, currency_id: str) -> dict[str, Any]:
        return self._action_get(currency_id, "exchangerates")

    def create_exchange_rate(self, currency_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._action_post(currency_id, "exchangerates", data)

    def get_exchange_rate(self, currency_id: str, rate_id: str) -> dict[str, Any]:
        return self._client.get(self._path(currency_id, "exchangerates", rate_id))

    def update_exchange_rate(
        self,
        currency_id: str,
        rate_id: str,
        data: dict[str, Any],
    ) -> dict[str, Any]:
        return self._client.put(
            self._path(currency_id, "exchangerates", rate_id),
            json=data,
        )

    def delete_exchange_rate(self, currency_id: str, rate_id: str) -> dict[str, Any]:
        return self._client.delete(self._path(currency_id, "exchangerates", rate_id))


class AsyncCurrencies(AsyncResource):
    _api_prefix, _resource = _P, "settings/currencies"

    async def list_exchange_rates(self, currency_id: str) -> dict[str, Any]:
        return await self._action_get(currency_id, "exchangerates")

    async def create_exchange_rate(self, currency_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._action_post(currency_id, "exchangerates", data)

    async def get_exchange_rate(self, currency_id: str, rate_id: str) -> dict[str, Any]:
        return await self._client.get(self._path(currency_id, "exchangerates", rate_id))

    async def update_exchange_rate(
        self,
        currency_id: str,
        rate_id: str,
        data: dict[str, Any],
    ) -> dict[str, Any]:
        return await self._client.put(
            self._path(currency_id, "exchangerates", rate_id),
            json=data,
        )

    async def delete_exchange_rate(self, currency_id: str, rate_id: str) -> dict[str, Any]:
        return await self._client.delete(self._path(currency_id, "exchangerates", rate_id))


class Users(SyncResource):
    _api_prefix, _resource = _P, "users"

    def create(self, data: dict[str, Any], **params: Any) -> dict[str, Any]:
        return self._client.post(
            self._path(),
            json=data,
            params=params or None,
        )

    def get_current(self) -> dict[str, Any]:
        return self._client.get(self._path("me"))

    def invite(self, user_id: str) -> dict[str, Any]:
        return self._action_post(user_id, "invite")

    def mark_active(self, user_id: str) -> dict[str, Any]:
        return self._action_post(user_id, "active")

    def mark_inactive(self, user_id: str) -> dict[str, Any]:
        return self._action_post(user_id, "inactive")


class AsyncUsers(AsyncResource):
    _api_prefix, _resource = _P, "users"

    async def create(self, data: dict[str, Any], **params: Any) -> dict[str, Any]:
        return await self._client.post(
            self._path(),
            json=data,
            params=params or None,
        )

    async def get_current(self) -> dict[str, Any]:
        return await self._client.get(self._path("me"))

    async def invite(self, user_id: str) -> dict[str, Any]:
        return await self._action_post(user_id, "invite")

    async def mark_active(self, user_id: str) -> dict[str, Any]:
        return await self._action_post(user_id, "active")

    async def mark_inactive(self, user_id: str) -> dict[str, Any]:
        return await self._action_post(user_id, "inactive")


class Preferences(SyncResource):
    _api_prefix, _resource = _P, "settings/preferences"

    def get(self, **params: Any) -> dict[str, Any]:  # type: ignore[override]
        return self._client.get(self._path(), params=params or None)

    def update(self, data: dict[str, Any]) -> dict[str, Any]:  # type: ignore[override]
        return self._client.put(self._path(), json=data)


class AsyncPreferences(AsyncResource):
    _api_prefix, _resource = _P, "settings/preferences"

    async def get(self, **params: Any) -> dict[str, Any]:  # type: ignore[override]
        return await self._client.get(self._path(), params=params or None)

    async def update(self, data: dict[str, Any]) -> dict[str, Any]:  # type: ignore[override]
        return await self._client.put(self._path(), json=data)


class Templates(SyncResource):
    _api_prefix, _resource = _P, "settings/templates"


class AsyncTemplates(AsyncResource):
    _api_prefix, _resource = _P, "settings/templates"


class OpeningBalances(SyncResource):
    _api_prefix, _resource = _P, "settings/openingbalances"

    def get(self, **params: Any) -> dict[str, Any]:  # type: ignore[override]
        return self._client.get(self._path(), params=params or None)

    def create(self, data: dict[str, Any]) -> dict[str, Any]:  # type: ignore[override]
        return self._client.post(self._path(), json=data)

    def update(self, data: dict[str, Any]) -> dict[str, Any]:  # type: ignore[override]
        return self._client.put(self._path(), json=data)

    def delete(self) -> dict[str, Any]:  # type: ignore[override]
        return self._client.delete(self._path())


class AsyncOpeningBalances(AsyncResource):
    _api_prefix, _resource = _P, "settings/openingbalances"

    async def get(self, **params: Any) -> dict[str, Any]:  # type: ignore[override]
        return await self._client.get(self._path(), params=params or None)

    async def create(self, data: dict[str, Any]) -> dict[str, Any]:  # type: ignore[override]
        return await self._client.post(self._path(), json=data)

    async def update(self, data: dict[str, Any]) -> dict[str, Any]:  # type: ignore[override]
        return await self._client.put(self._path(), json=data)

    async def delete(self) -> dict[str, Any]:  # type: ignore[override]
        return await self._client.delete(self._path())


class Workflows(SyncResource):
    _api_prefix, _resource = _P, "settings/workflows"


class AsyncWorkflows(AsyncResource):
    _api_prefix, _resource = _P, "settings/workflows"


class CustomViews(SyncResource):
    _api_prefix, _resource = _P, "customviews"

    def reorder(self, data: dict[str, Any]) -> dict[str, Any]:
        return self._sub_post("reorder", data)

    def list_created(self, **params: Any) -> dict[str, Any]:
        return self._client.get(
            self._path("createdviews"),
            params=params or None,
        )

    def get_search_fields(self, **params: Any) -> dict[str, Any]:
        return self._client.get(
            self._path("searchfields"),
            params=params or None,
        )


class AsyncCustomViews(AsyncResource):
    _api_prefix, _resource = _P, "customviews"

    async def reorder(self, data: dict[str, Any]) -> dict[str, Any]:
        return await self._sub_post("reorder", data)

    async def list_created(self, **params: Any) -> dict[str, Any]:
        return await self._client.get(
            self._path("createdviews"),
            params=params or None,
        )

    async def get_search_fields(self, **params: Any) -> dict[str, Any]:
        return await self._client.get(
            self._path("searchfields"),
            params=params or None,
        )


class CustomButtons(SyncResource):
    _api_prefix, _resource = _P, "settings/custombuttons"


class AsyncCustomButtons(AsyncResource):
    _api_prefix, _resource = _P, "settings/custombuttons"


class EmailTemplates(SyncResource):
    _api_prefix, _resource = _P, "settings/emailtemplates"


class AsyncEmailTemplates(AsyncResource):
    _api_prefix, _resource = _P, "settings/emailtemplates"

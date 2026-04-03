"""Tests for the exception hierarchy and error code mapping."""

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
    ZohoValidationError,
    exception_for_code,
)


class TestHierarchy:
    def test_all_api_errors_inherit_from_zoho_error(self):
        assert issubclass(ZohoAPIError, ZohoError)
        assert issubclass(ZohoRateLimitError, ZohoAPIError)
        assert issubclass(ZohoAuthenticationError, ZohoAPIError)
        assert issubclass(ZohoNotFoundError, ZohoAPIError)
        assert issubclass(ZohoValidationError, ZohoAPIError)
        assert issubclass(ZohoServerError, ZohoAPIError)

    def test_validation_subtypes_inherit_from_validation(self):
        assert issubclass(ZohoDuplicateError, ZohoValidationError)
        assert issubclass(ZohoInvalidFieldError, ZohoValidationError)
        assert issubclass(ZohoEmptyBodyError, ZohoValidationError)
        assert issubclass(ZohoBusinessRuleError, ZohoValidationError)
        assert issubclass(ZohoFeatureNotEnabledError, ZohoValidationError)
        assert issubclass(ZohoResourceDependentError, ZohoValidationError)

    def test_catch_all_validation_errors(self):
        """All validation subtypes should be catchable as ZohoValidationError."""
        for cls in [
            ZohoDuplicateError,
            ZohoInvalidFieldError,
            ZohoEmptyBodyError,
            ZohoBusinessRuleError,
            ZohoFeatureNotEnabledError,
            ZohoResourceDependentError,
        ]:
            exc = cls("test")
            assert isinstance(exc, ZohoValidationError)
            assert isinstance(exc, ZohoAPIError)
            assert isinstance(exc, ZohoError)


class TestExceptionAttributes:
    def test_rate_limit_retry_after(self):
        exc = ZohoRateLimitError(retry_after=120.0)
        assert exc.retry_after == 120.0
        assert exc.status_code == 429

    def test_validation_error_details(self):
        exc = ZohoValidationError("bad field", details={"field": "name"})
        assert exc.details == {"field": "name"}
        assert exc.status_code == 400

    def test_invalid_field_name_extraction(self):
        exc = ZohoInvalidFieldError("Invalid value passed for contact_type")
        assert exc.field_name == "contact_type"

    def test_invalid_field_name_none_when_no_pattern(self):
        exc = ZohoInvalidFieldError("Some other error")
        assert exc.field_name is None

    def test_repr(self):
        exc = ZohoAPIError("oops", status_code=500, error_code=1234)
        r = repr(exc)
        assert "500" in r
        assert "1234" in r

    def test_error_code_constants(self):
        assert ZohoErrorCode.SUCCESS == 0
        assert ZohoErrorCode.NOT_FOUND == 1002
        assert ZohoErrorCode.DUPLICATE == 4
        assert ZohoErrorCode.FEATURE_NOT_ENABLED == 110817


class TestExceptionForCode:
    """Tests for the exception_for_code mapper used by the HTTP client."""

    def test_401_returns_auth_error(self):
        exc = exception_for_code(status_code=401, zoho_code=57, message="Not authorized", body={})
        assert isinstance(exc, ZohoAuthenticationError)

    def test_403_returns_forbidden(self):
        exc = exception_for_code(status_code=403, zoho_code=None, message="Forbidden", body={})
        assert isinstance(exc, ZohoForbiddenError)

    def test_404_returns_not_found(self):
        exc = exception_for_code(status_code=404, zoho_code=1002, message="Not found", body={})
        assert isinstance(exc, ZohoNotFoundError)

    def test_429_returns_rate_limit(self):
        exc = exception_for_code(status_code=429, zoho_code=None, message="Too many", body={})
        assert isinstance(exc, ZohoRateLimitError)

    def test_500_returns_server_error(self):
        exc = exception_for_code(status_code=500, zoho_code=None, message="Internal", body={})
        assert isinstance(exc, ZohoServerError)

    def test_400_code_2_returns_invalid_field(self):
        exc = exception_for_code(
            status_code=400,
            zoho_code=2,
            message="Invalid value passed for contact_type",
            body={"code": 2},
        )
        assert isinstance(exc, ZohoInvalidFieldError)
        assert isinstance(exc, ZohoValidationError)

    def test_400_code_4_duplicate_message_returns_duplicate(self):
        exc = exception_for_code(
            status_code=400,
            zoho_code=4,
            message="CurrencyCode already exists",
            body={"code": 4},
        )
        assert isinstance(exc, ZohoDuplicateError)

    def test_400_code_4_invalid_message_returns_invalid_field(self):
        exc = exception_for_code(
            status_code=400,
            zoho_code=4,
            message="Invalid value passed for Format",
            body={"code": 4},
        )
        assert isinstance(exc, ZohoInvalidFieldError)
        assert not isinstance(exc, ZohoDuplicateError)

    def test_400_code_11_returns_empty_body(self):
        exc = exception_for_code(
            status_code=400,
            zoho_code=11,
            message="JSONString parameter cannot be empty",
            body={"code": 11},
        )
        assert isinstance(exc, ZohoEmptyBodyError)

    def test_400_code_36_returns_resource_dependent(self):
        exc = exception_for_code(
            status_code=400,
            zoho_code=36,
            message="Cannot delete, has transactions",
            body={"code": 36},
        )
        assert isinstance(exc, ZohoResourceDependentError)

    def test_400_code_4016_returns_business_rule(self):
        exc = exception_for_code(
            status_code=400,
            zoho_code=4016,
            message="No line items selected",
            body={"code": 4016},
        )
        assert isinstance(exc, ZohoBusinessRuleError)

    def test_400_code_110817_returns_feature_not_enabled(self):
        exc = exception_for_code(
            status_code=400,
            zoho_code=110817,
            message="Enable Sales Tax",
            body={"code": 110817},
        )
        assert isinstance(exc, ZohoFeatureNotEnabledError)

    def test_400_unknown_code_returns_generic_validation(self):
        exc = exception_for_code(
            status_code=400,
            zoho_code=99999,
            message="Something else",
            body={"code": 99999},
        )
        assert isinstance(exc, ZohoValidationError)
        assert type(exc) is ZohoValidationError  # not a subclass

    def test_400_no_code_returns_generic_validation(self):
        exc = exception_for_code(status_code=400, zoho_code=None, message="Bad request", body={})
        assert isinstance(exc, ZohoValidationError)

    def test_405_returns_generic_api_error(self):
        exc = exception_for_code(
            status_code=405, zoho_code=None, message="Method not allowed", body={}
        )
        assert isinstance(exc, ZohoAPIError)
        assert exc.status_code == 405

"""Structured exception hierarchy for Zoho API errors.

Every Zoho API response includes a ``code`` field. This module maps
those codes to specific exception classes so callers can handle errors
precisely.

Zoho Error Code Ranges (discovered from API testing):
    0       — Success
    2       — Invalid value for a field
    4       — Duplicate / already exists
    5       — Invalid URL / endpoint not found
    6       — Invalid resource reference
    11      — Empty or malformed request body (missing JSONString)
    14      — Invalid authentication token
    36      — Resource has dependents, cannot delete
    57      — Not authorized (invalid/expired token)
    1002    — Resource not found / not accessible
    1004    — Resource has transactions, cannot delete
    1009    — Limit exceeded (e.g. max contacts)
    2xxx    — Field validation errors
    4xxx    — Business rule violations (e.g. no line items)
    10xxx   — Module-specific errors
    11xxx   — Accounting-specific errors (e.g. journal rules)
    110xxx  — Feature not enabled (e.g. sales tax)

HTTP Status Mapping:
    200     — Success
    201     — Created
    400     — Validation error / bad request
    401     — Authentication failed
    403     — Forbidden / insufficient permissions
    404     — Resource not found or invalid URL
    405     — Method not allowed
    429     — Rate limit exceeded
    500+    — Zoho server error

Usage::

    from zohopy.exceptions import (
        ZohoError,
        ZohoNotFoundError,
        ZohoValidationError,
        ZohoRateLimitError,
    )

    try:
        books.invoices.get("nonexistent")
    except ZohoNotFoundError as e:
        print(f"Not found: {e}")
        print(f"Zoho code: {e.code}")
    except ZohoValidationError as e:
        print(f"Invalid: {e}")
        print(f"Details: {e.details}")
    except ZohoError as e:
        print(f"Zoho error: {e}")
"""

from __future__ import annotations

from typing import Any

# ---------------------------------------------------------------------------
# Zoho error code constants
# ---------------------------------------------------------------------------


class ZohoErrorCode:
    """Known Zoho Books API error codes.

    These are the ``code`` values in the JSON response body, not HTTP status codes.
    """

    SUCCESS = 0

    # General errors
    INVALID_VALUE = 2
    DUPLICATE = 4
    INVALID_URL = 5
    INVALID_RESOURCE = 6
    EMPTY_REQUEST_BODY = 11
    INVALID_AUTH_TOKEN = 14
    RESOURCE_DEPENDENT = 36
    NOT_AUTHORIZED = 57

    # Resource errors
    NOT_FOUND = 1002
    HAS_TRANSACTIONS = 1004
    LIMIT_EXCEEDED = 1009

    # Business rule (4xxx)
    NO_LINE_ITEMS = 4016

    # Module-specific (10xxx, 11xxx)
    JOURNAL_ACCOUNT_ERROR = 11016

    # Feature not enabled (110xxx)
    FEATURE_NOT_ENABLED = 110817


# ---------------------------------------------------------------------------
# Exception hierarchy
# ---------------------------------------------------------------------------


class ZohoError(Exception):
    """Base exception for all ZohoPy errors.

    Attributes:
        code: Zoho-specific error code from the response body (not HTTP status).
        details: Full error response dict from Zoho.
    """

    def __init__(
        self,
        message: str,
        *,
        code: int | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.details = details or {}

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self!s}, code={self.code})"


class ZohoAPIError(ZohoError):
    """HTTP error returned by a Zoho API endpoint (4xx / 5xx).

    Attributes:
        status_code: HTTP status code (e.g. 400, 500).
        error_code: Zoho-specific error code from the response body.
    """

    def __init__(
        self,
        message: str,
        *,
        status_code: int,
        error_code: int | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message, code=error_code, details=details)
        self.status_code = status_code

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self!s}, status={self.status_code}, code={self.code})"


# -- Authentication & Authorization ----------------------------------------


class ZohoAuthenticationError(ZohoAPIError):
    """HTTP 401 — invalid, expired, or revoked OAuth token.

    Zoho codes: 14 (invalid token), 57 (not authorized).
    The library auto-retries once with a refreshed token before raising.
    """

    def __init__(self, message: str = "Authentication failed") -> None:
        super().__init__(message, status_code=401)


class ZohoForbiddenError(ZohoAPIError):
    """HTTP 403 — insufficient OAuth scopes or org permissions.

    Check that your OAuth token has the required scopes
    (e.g. ``ZohoBooks.invoices.CREATE``).
    """

    def __init__(self, message: str = "Forbidden") -> None:
        super().__init__(message, status_code=403)


# -- Resource errors -------------------------------------------------------


class ZohoNotFoundError(ZohoAPIError):
    """HTTP 404 — resource does not exist or URL is invalid.

    Zoho codes: 5 (invalid URL), 1002 (resource not found/deleted).

    Common causes:
        - Wrong resource ID
        - Resource was deleted
        - Typo in the endpoint URL
        - Accessing a resource in another org
    """

    def __init__(self, message: str = "Resource not found") -> None:
        super().__init__(message, status_code=404)


# -- Validation & Business Rules -------------------------------------------


class ZohoValidationError(ZohoAPIError):
    """HTTP 400 — request failed server-side validation.

    Zoho codes: 2 (invalid value), 4 (duplicate), 6 (invalid reference),
    11 (empty body), 4016 (no line items), etc.

    The ``details`` dict contains the full Zoho response, which often
    includes field-level error info.

    Common causes:
        - Missing required fields (e.g. ``contact_name``)
        - Invalid field values (e.g. bad ``contact_type``)
        - Duplicate records (e.g. currency already exists)
        - Empty request body
        - Business rules violated (e.g. invoice with no line items)
    """

    def __init__(
        self,
        message: str = "Validation error",
        *,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message, status_code=400, details=details)


class ZohoDuplicateError(ZohoValidationError):
    """A record with the same unique value already exists.

    Zoho code: 4.
    Example: creating a currency that already exists.
    """


class ZohoInvalidFieldError(ZohoValidationError):
    """An invalid value was passed for a specific field.

    Zoho code: 2.
    The error message typically says "Invalid value passed for {field}".
    """

    @property
    def field_name(self) -> str | None:
        """Extract the field name from the error message, if present."""
        msg = str(self)
        prefix = "Invalid value passed for "
        if prefix in msg:
            return msg.split(prefix, 1)[1].strip()
        return None


class ZohoEmptyBodyError(ZohoValidationError):
    """The request body was empty or did not contain valid JSON.

    Zoho code: 11.
    """


class ZohoBusinessRuleError(ZohoValidationError):
    """A business rule was violated.

    Examples:
        - No line items in an invoice (code 4016)
        - Item is sales-only but used in a purchase order
        - Cannot delete contact with open transactions
    """


class ZohoFeatureNotEnabledError(ZohoValidationError):
    """A required feature/module is not enabled in the Zoho org.

    Zoho codes: 110xxx range.
    Example: "Enable Sales Tax in order to perform tax related operations."

    Resolution: Enable the feature in Zoho Books Settings.
    """


class ZohoResourceDependentError(ZohoValidationError):
    """Cannot delete/modify because the resource has dependents.

    Zoho codes: 36, 1004.
    Example: Cannot delete a contact that has open invoices.
    """


# -- Rate Limiting ---------------------------------------------------------


class ZohoRateLimitError(ZohoAPIError):
    """HTTP 429 — API rate limit exceeded.

    Zoho Books allows ~100 requests/minute/org (varies by plan).
    The library retries automatically with back-off.

    Attributes:
        retry_after: Seconds to wait before retrying.
    """

    def __init__(
        self,
        message: str = "Rate limit exceeded",
        *,
        retry_after: float = 60.0,
    ) -> None:
        super().__init__(message, status_code=429)
        self.retry_after = retry_after


# -- Server Errors ---------------------------------------------------------


class ZohoServerError(ZohoAPIError):
    """HTTP 5xx — Zoho server-side failure.

    These are transient — the library retries automatically.
    If you see these persistently, check https://status.zoho.com/
    """

    def __init__(
        self,
        message: str = "Server error",
        *,
        status_code: int = 500,
    ) -> None:
        super().__init__(message, status_code=status_code)


# -- Token Errors ----------------------------------------------------------


class ZohoTokenRefreshError(ZohoError):
    """OAuth token refresh failed.

    Common causes:
        - Invalid client_id or client_secret
        - Refresh token was revoked
        - Wrong data center (accounts URL mismatch)
        - Network error reaching Zoho OAuth server
    """

    def __init__(self, message: str = "Token refresh failed") -> None:
        super().__init__(message)


# ---------------------------------------------------------------------------
# Error code → exception mapper (used by _client.py)
# ---------------------------------------------------------------------------

# Zoho body code → exception class (for 400 responses)
_CODE_EXCEPTION_MAP: dict[int, type[ZohoValidationError]] = {
    ZohoErrorCode.INVALID_VALUE: ZohoInvalidFieldError,
    ZohoErrorCode.INVALID_RESOURCE: ZohoInvalidFieldError,
    ZohoErrorCode.EMPTY_REQUEST_BODY: ZohoEmptyBodyError,
    ZohoErrorCode.RESOURCE_DEPENDENT: ZohoResourceDependentError,
    ZohoErrorCode.HAS_TRANSACTIONS: ZohoResourceDependentError,
    ZohoErrorCode.FEATURE_NOT_ENABLED: ZohoFeatureNotEnabledError,
}

# Message patterns that indicate a duplicate (code 4 is ambiguous)
_DUPLICATE_PATTERNS = ("already exists", "already been used", "duplicate")


def _is_duplicate_message(message: str) -> bool:
    lower = message.lower()
    return any(p in lower for p in _DUPLICATE_PATTERNS)


def exception_for_code(
    *,
    status_code: int,
    zoho_code: int | None,
    message: str,
    body: dict[str, Any],
) -> ZohoAPIError:
    """Map an HTTP status + Zoho error code to the most specific exception.

    Uses both the HTTP status and the Zoho body ``code`` to find the
    most precise exception. For ambiguous codes (like 4 which can mean
    "duplicate" or "invalid format"), the message is also checked.
    """
    if status_code == 429:
        return ZohoRateLimitError()

    if status_code == 401:
        return ZohoAuthenticationError(message)

    if status_code == 403:
        return ZohoForbiddenError(message)

    if status_code == 404:
        return ZohoNotFoundError(message)

    if status_code >= 500:
        return ZohoServerError(message, status_code=status_code)

    # -- 400-range: detailed mapping --

    # Code 4 is ambiguous: "already exists" → duplicate, else invalid field
    if zoho_code == ZohoErrorCode.DUPLICATE:
        if _is_duplicate_message(message):
            return ZohoDuplicateError(message, details=body)
        return ZohoInvalidFieldError(message, details=body)

    # Direct code mapping
    if zoho_code is not None and zoho_code in _CODE_EXCEPTION_MAP:
        return _CODE_EXCEPTION_MAP[zoho_code](message, details=body)

    # Feature-not-enabled range (110xxx)
    if zoho_code is not None and zoho_code >= 110000:
        return ZohoFeatureNotEnabledError(message, details=body)

    # Business rule codes (4xxx range)
    if zoho_code is not None and 4000 <= zoho_code < 5000:
        return ZohoBusinessRuleError(message, details=body)

    # Message-based duplicate fallback
    if status_code == 400 and _is_duplicate_message(message):
        return ZohoDuplicateError(message, details=body)

    # Generic validation error
    if status_code == 400:
        return ZohoValidationError(message, details=body)

    return ZohoAPIError(
        message,
        status_code=status_code,
        error_code=zoho_code,
        details=body,
    )

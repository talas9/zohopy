# Error Handling

ZohoPy maps every Zoho API error to a typed Python exception.

## Exception Hierarchy

```
ZohoError (base — catch everything)
├── ZohoTokenRefreshError          — OAuth token refresh failed
└── ZohoAPIError (HTTP errors)
    ├── ZohoAuthenticationError    — 401: bad/expired token
    ├── ZohoForbiddenError         — 403: insufficient scopes
    ├── ZohoNotFoundError          — 404: resource not found
    ├── ZohoRateLimitError         — 429: rate limit (.retry_after)
    ├── ZohoServerError            — 5xx: Zoho server error
    └── ZohoValidationError        — 400: bad request
        ├── ZohoInvalidFieldError      — bad field value (.field_name)
        ├── ZohoDuplicateError         — record already exists
        ├── ZohoEmptyBodyError         — missing request body
        ├── ZohoBusinessRuleError      — business rule violation
        ├── ZohoFeatureNotEnabledError — feature not enabled in org
        └── ZohoResourceDependentError — has transactions/dependents
```

## Usage

```python
from zohopy import (
    ZohoNotFoundError,
    ZohoValidationError,
    ZohoDuplicateError,
    ZohoInvalidFieldError,
    ZohoRateLimitError,
    ZohoFeatureNotEnabledError,
)

try:
    books.invoices.get("nonexistent")
except ZohoNotFoundError:
    print("Not found")
except ZohoInvalidFieldError as e:
    print(f"Bad field: {e.field_name}")
except ZohoDuplicateError:
    print("Already exists")
except ZohoFeatureNotEnabledError:
    print("Enable in Zoho Settings")
except ZohoRateLimitError as e:
    print(f"Wait {e.retry_after}s")
except ZohoValidationError as e:
    print(f"Details: {e.details}")
```

## Zoho Error Code Reference

| Code | Exception | Meaning |
|------|-----------|---------|
| 0 | *(success)* | No error |
| 2 | `ZohoInvalidFieldError` | Invalid value for a field |
| 4 | `ZohoDuplicateError` or `ZohoInvalidFieldError` | Already exists (if "already exists" in message) or invalid format |
| 5 | `ZohoNotFoundError` | Invalid endpoint URL |
| 6 | `ZohoInvalidFieldError` | Invalid resource reference |
| 11 | `ZohoEmptyBodyError` | Empty/malformed request body |
| 14 | `ZohoAuthenticationError` | Invalid auth token |
| 36 | `ZohoResourceDependentError` | Cannot delete, has dependents |
| 57 | `ZohoAuthenticationError` | Not authorized |
| 1002 | `ZohoNotFoundError` | Resource deleted/inaccessible |
| 1004 | `ZohoResourceDependentError` | Has open transactions |
| 4xxx | `ZohoBusinessRuleError` | Business rule violation |
| 110xxx | `ZohoFeatureNotEnabledError` | Feature not enabled |

## Automatic Retry Behavior

| Error | Library Behavior |
|-------|-----------------|
| **429 Rate Limit** | Retries with exponential back-off (`retry_after * attempt`) |
| **401 Auth** | Refreshes OAuth token once, retries |
| **5xx Server** | Retries with exponential back-off (`retry_backoff * 2^attempt`) |
| **OAuth Rate Limit** | Waits 30s/60s/90s across 3 attempts |

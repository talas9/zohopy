# ZohoPy

[![CI](https://github.com/talas9/zohopy/actions/workflows/ci.yml/badge.svg)](https://github.com/talas9/zohopy/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/zohopy)](https://pypi.org/project/zohopy/)
[![Python](https://img.shields.io/pypi/pyversions/zohopy)](https://pypi.org/project/zohopy/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Modern, async-ready Python client for Zoho APIs.**

Full coverage of **Zoho Books** (API v3) with both sync and async interfaces. Designed as a standalone, modular library — easy to maintain, extend, and use as a Git submodule.

## Features

- **Sync + Async** — `SyncZohoClient` or `AsyncZohoClient`
- **Complete Zoho Books coverage** — 30+ resource types with full CRUD + actions
- **Auto data-center detection** — discovered from `api_domain` during OAuth
- **Auto-auth** — OAuth2 tokens refresh transparently
- **Auto-pagination** — iterate all pages with `list_all()`
- **Retry & back-off** — handles 429 rate limits and 5xx server errors
- **Structured logging** — JSON/console output via structlog
- **Typed exceptions** — 10+ specific exception classes for every Zoho error pattern
- **Docker ready** — Dockerfile + docker-compose with proper env/secrets
- **Type-safe** — full type hints, `py.typed`, mypy strict
- **Zero config** — reads `.env` via pydantic-settings
- **Interactive setup** — `python -m zohopy` wizard with browser OAuth flow

## Products

| Product | Status | API Version |
|---------|--------|-------------|
| **Zoho Books** | ✅ Full coverage | v3 |
| Zoho Inventory | 🔜 Coming soon | v1 |
| Zoho CRM | 🔜 Coming soon | v7 |
| Zoho Payroll | 🔜 Planned | — |
| Zoho People | 🔜 Planned | — |

## Installation

```bash
pip install zohopy
```

## Setup

### Option A: Interactive wizard (recommended)

```bash
python -m zohopy
```

Supports both **Self Client** (paste code) and **Browser redirect** (automatic) OAuth flows. Generates `.env` for you.

### Option B: Manual

1. Go to [api-console.zoho.com](https://api-console.zoho.com/) → create a Self Client
2. Generate a grant code with scope `ZohoBooks.fullaccess.all`
3. Exchange it:

```python
from zohopy.setup import exchange_grant_token

result = exchange_grant_token(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    grant_token="THE_GRANT_CODE",
)
# result["refresh_token"] — save this (permanent)
# result["api_domain"] — auto-detects your data center
```

4. Create `.env`:

```env
ZOHO_CLIENT_ID=...
ZOHO_CLIENT_SECRET=...
ZOHO_REFRESH_TOKEN=...
ZOHO_ORGANIZATION_ID=...
ZOHO_API_DOMAIN=https://www.zohoapis.com
```

### Option C: Programmatic (for submodule integration)

```python
from zohopy import ZohoConfig, SyncZohoClient

config = ZohoConfig(
    client_id="...",
    client_secret="...",
    refresh_token="...",
    organization_id="...",
    api_domain="https://www.zohoapis.com",
    _env_file=None,  # skip .env loading
)
```

## Quick Start

```python
from zohopy import ZohoConfig, SyncZohoClient
from zohopy.products.books import ZohoBooks

with SyncZohoClient(ZohoConfig()) as client:
    books = ZohoBooks(client)

    # Contacts
    contacts = books.contacts.list()
    customer = books.contacts.create({"contact_name": "Acme Corp", "contact_type": "customer"})

    # Invoices
    invoice = books.invoices.create({
        "customer_id": "CUSTOMER_ID",
        "line_items": [{"item_id": "ITEM_ID", "quantity": 1, "rate": 100}],
    })
    books.invoices.mark_sent(invoice["invoice"]["invoice_id"])

    # Auto-paginate
    for page in books.items.list_all():
        for item in page.get("items", []):
            print(item["name"])
```

### Async

```python
import asyncio
from zohopy import ZohoConfig, AsyncZohoClient
from zohopy.products.books import AsyncZohoBooks

async def main():
    async with AsyncZohoClient(ZohoConfig()) as client:
        books = AsyncZohoBooks(client)
        contacts = await books.contacts.list()
        async for page in books.items.list_all():
            print(len(page.get("items", [])))

asyncio.run(main())
```

## Error Handling

ZohoPy maps every Zoho API error to a typed exception:

```python
from zohopy import (
    ZohoNotFoundError,
    ZohoRateLimitError,
    ZohoValidationError,
    ZohoDuplicateError,
    ZohoFeatureNotEnabledError,
    ZohoInvalidFieldError,
)

try:
    books.invoices.get("nonexistent")
except ZohoNotFoundError:
    print("Invoice not found")
except ZohoRateLimitError as e:
    print(f"Rate limited — retry after {e.retry_after}s")
except ZohoDuplicateError:
    print("Already exists")
except ZohoInvalidFieldError as e:
    print(f"Bad field: {e.field_name}")
except ZohoFeatureNotEnabledError:
    print("Enable the feature in Zoho Settings")
except ZohoValidationError as e:
    print(f"Validation: {e.details}")
```

### Exception Hierarchy

```
ZohoError
├── ZohoTokenRefreshError          — OAuth token refresh failed
└── ZohoAPIError                   — HTTP error from Zoho
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

### Zoho Error Code Reference

| Code | Exception | When |
|------|-----------|------|
| 2 | `ZohoInvalidFieldError` | Invalid value for a field |
| 4 | `ZohoDuplicateError` / `ZohoInvalidFieldError` | Already exists or invalid format |
| 5 | `ZohoNotFoundError` | Invalid endpoint URL |
| 6 | `ZohoInvalidFieldError` | Invalid resource reference |
| 11 | `ZohoEmptyBodyError` | Empty/malformed request body |
| 14 | `ZohoAuthenticationError` | Invalid auth token |
| 36 | `ZohoResourceDependentError` | Cannot delete, has dependents |
| 57 | `ZohoAuthenticationError` | Not authorized |
| 1002 | `ZohoNotFoundError` | Resource deleted/inaccessible |
| 1004 | `ZohoResourceDependentError` | Has open transactions |
| 4016 | `ZohoBusinessRuleError` | No line items selected |
| 110817 | `ZohoFeatureNotEnabledError` | Sales Tax not enabled |

## Zoho Books API Coverage

### Sales Cycle

| Resource | CRUD | Actions |
|----------|------|---------|
| Contacts | ✅ | active/inactive, portal, payment reminders, addresses |
| Estimates | ✅ | sent/accepted/declined, approve, email |
| Sales Orders | ✅ | open/void, approve, email |
| Invoices | ✅ | sent/void/draft, approve, email, write-off, credits, payment link |
| Recurring Invoices | ✅ | stop/resume |
| Sales Receipts | ✅ | email |
| Credit Notes | ✅ | void/draft/open, approve, apply to invoice, refund |
| Customer Payments | ✅ | refund |
| Retainer Invoices | ✅ | sent/void/draft, approve, email |

### Purchase Cycle

| Resource | CRUD | Actions |
|----------|------|---------|
| Purchase Orders | ✅ | open/billed/cancelled, approve, email |
| Bills | ✅ | void/open, approve, credits |
| Recurring Bills | ✅ | stop/resume |
| Vendor Payments | ✅ | refund, email |
| Expenses | ✅ | receipts |
| Recurring Expenses | ✅ | stop/resume |

### Items & Inventory

| Resource | CRUD | Actions |
|----------|------|---------|
| Items | ✅ | active/inactive |

### Banking & Accounting

| Resource | CRUD | Actions |
|----------|------|---------|
| Bank Accounts | ✅ | activate/deactivate |
| Bank Transactions | ✅ | match/unmatch, categorize, exclude/restore |
| Bank Rules | ✅ | — |
| Chart of Accounts | ✅ | active/inactive |
| Journals | ✅ | publish |
| Base Currency Adjustments | ✅ | — |

### Projects & Time

| Resource | CRUD | Actions |
|----------|------|---------|
| Projects | ✅ | activate/inactivate, clone |
| Tasks | ✅ | open/ongoing/completed |
| Time Entries | ✅ | start/stop timer |

### Fixed Assets

| Resource | CRUD | Actions |
|----------|------|---------|
| Fixed Assets | ✅ | active/cancel/draft, write-off, sell |

### Settings & Configuration

| Resource | Operations |
|----------|-----------|
| Organizations | CRUD |
| Taxes | CRUD + tax groups |
| Currencies | CRUD + exchange rates |
| Users | CRUD + current user, invite, active/inactive |
| Preferences | get/update |
| Templates | list |
| Opening Balances | CRUD |
| Custom Fields | list by entity, CRUD, reorder |
| Custom Views | CRUD |
| Reporting Tags | CRUD + active/inactive |
| Workflows | list |

## Logging

```python
from zohopy import configure_logging

# Development (colored console)
configure_logging(level="DEBUG", log_format="console")

# Production / Docker (structured JSON)
configure_logging(level="INFO", log_format="json")

# Or via env vars:
#   ZOHOPY_LOG_LEVEL=INFO
#   ZOHOPY_LOG_FORMAT=json
```

## Docker

```bash
# Build
docker compose build

# Interactive OAuth setup
docker compose run --rm zohopy-setup

# Run a script
docker compose run --rm zohopy-script
```

## Configuration

| Env Variable | Required | Default | Description |
|-------------|----------|---------|-------------|
| `ZOHO_CLIENT_ID` | ✅ | — | OAuth client ID |
| `ZOHO_CLIENT_SECRET` | ✅ | — | OAuth client secret |
| `ZOHO_REFRESH_TOKEN` | ✅ | — | Long-lived refresh token |
| `ZOHO_ORGANIZATION_ID` | ✅ | — | Zoho org ID |
| `ZOHO_API_DOMAIN` | — | — | Auto-detects data center |
| `ZOHO_DATA_CENTER` | — | `us` | Override: us/eu/in/au/jp/ca/cn/sa |
| `ZOHOPY_LOG_LEVEL` | — | `INFO` | DEBUG/INFO/WARNING/ERROR |
| `ZOHOPY_LOG_FORMAT` | — | `console` | console/json |

## Development

```bash
git clone https://github.com/talas9/zohopy.git
cd zohopy
git checkout dev
pip install -e ".[dev]"

# Tests
pytest tests/unit/                         # unit tests (mocked)
pytest tests/integration/ -m integration   # live API tests (needs .env)

# Quality
ruff check src/ tests/
ruff format src/ tests/
mypy src/
```

### Branch Strategy

| Branch | Purpose |
|--------|---------|
| `main` | Stable releases only. Protected — requires PR with passing CI. |
| `dev` | Active development. All work merges here first. |
| `v*` tags | Trigger PyPI release from `main` only. |

### Release Process

1. Develop on `dev` branch
2. Open PR from `dev` → `main`
3. CI must pass (lint + type-check + tests on Python 3.10–3.13)
4. Merge to `main`
5. Tag: `git tag v0.2.0 && git push origin v0.2.0`
6. GitHub Actions builds + publishes to PyPI + creates GitHub Release

## Contributing

1. Fork → clone → `git checkout -b feat/my-feature` from `dev`
2. Make changes with tests
3. `ruff check && mypy src/ && pytest`
4. Open PR to `dev`

## License

[MIT](LICENSE)

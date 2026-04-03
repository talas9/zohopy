# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [0.1.0] — 2026-04-03

### Added

#### Core
- Sync + async HTTP clients (`SyncZohoClient`, `AsyncZohoClient`)
- OAuth2 token management with automatic refresh
- Two OAuth setup flows: Self Client (paste code) and Browser redirect (localhost)
- Interactive setup wizard: `python -m zohopy`
- Auto data-center detection from `api_domain`
- Auto org discovery during setup with browser-based org picker
- 8 data center support (US, EU, IN, AU, JP, CA, CN, SA)
- Rate-limit retry with exponential back-off
- Structured logging via structlog (JSON/console)
- `pydantic-settings` configuration from `.env` or env vars

#### Zoho Books API v3 — Full Coverage
- **Sales cycle:** Contacts, Estimates, Sales Orders, Invoices, Recurring Invoices, Sales Receipts, Credit Notes, Customer Payments, Retainer Invoices
- **Purchase cycle:** Purchase Orders, Bills, Recurring Bills, Vendor Payments, Expenses, Recurring Expenses
- **Items:** Items with active/inactive
- **Banking:** Bank Accounts, Bank Transactions (match/categorize), Bank Rules
- **Accounting:** Chart of Accounts, Journals, Base Currency Adjustments
- **Projects:** Projects, Tasks, Time Entries
- **Fixed Assets:** Full lifecycle (active/cancel/write-off/sell)
- **Settings:** Organizations, Taxes (+ groups), Currencies (+ exchange rates), Users, Preferences, Templates, Opening Balances, Custom Fields, Custom Views, Reporting Tags, Workflows

#### Error Handling
- 10+ typed exception classes mapped from Zoho error codes
- `ZohoInvalidFieldError` with `.field_name` extraction
- `ZohoDuplicateError`, `ZohoBusinessRuleError`, `ZohoFeatureNotEnabledError`
- Smart code-4 disambiguation (duplicate vs invalid value by message)
- `ZohoErrorCode` constants for all known codes

#### Infrastructure
- Docker + Docker Compose (multi-stage build, non-root, healthcheck)
- GitHub Actions CI (lint + type-check + test matrix 3.10–3.13)
- GitHub Actions release (tag → build → PyPI + GitHub Release)
- GitHub issue templates (bug report, feature request)
- PR template
- 56 unit tests + 72 integration tests (live sandbox)
- `py.typed` marker for PEP 561

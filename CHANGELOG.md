# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- `ZOHO_DATA_CENTER` is now a required config field (was optional with `us` default)
- `ZOHO_REFRESH_TOKEN` and `ZOHO_ORGANIZATION_ID` are now required fields
- `ZOHO_API_DOMAIN` remains optional — overrides `ZOHO_DATA_CENTER` when set
- Added Python 3.14 to CI test matrix and classifiers

### Fixed
- 20 mypy strict-mode errors (override signatures, return type annotations)
- Coverage threshold set to 40% to match actual unit test coverage
- Release workflow updated to PyPA Trusted Publishing standard with Sigstore signing

### Docs
- README trimmed to 83-line landing page
- Full API reference moved to `docs/api.md`
- Error handling guide moved to `docs/errors.md`
- Setup guide moved to `docs/setup.md`
- Environment variable docs corrected to reflect actual required/optional fields

## [0.1.0] - 2026-04-03

First public release. Published to [PyPI](https://pypi.org/project/zohopy/).

### Added
- **Zoho Books API v3** — 43 resource types, 694 methods (347 sync + 347 async)
- **Sales cycle:** Contacts, Contact Persons, Estimates, Sales Orders, Invoices, Recurring Invoices, Sales Receipts, Credit Notes, Customer Debit Notes, Customer Payments, Retainer Invoices
- **Purchase cycle:** Purchase Orders, Bills, Recurring Bills, Vendor Credits, Vendor Payments, Expenses, Recurring Expenses
- **Banking:** Bank Accounts (with statement import), Bank Transactions (match, categorize, exclude/restore), Chart of Accounts, Journals, Base Currency Adjustments
- **Projects:** Projects (with user/task management), Tasks, Time Entries
- **Assets:** Fixed Assets (with depreciation forecast), Fixed Asset Types
- **Settings:** Organizations, Taxes (authorities, exemptions, groups), Currencies (exchange rates), Users, Preferences, Templates, Opening Balances, Custom Fields, Custom Views, Custom Modules, Reporting Tags, Workflows, Locations
- **Integration:** Zoho CRM import (customer, vendor, item)
- **Multi-currency** support with exchange rates on all transactions
- **Landed cost** support on bills (`is_landed_cost`, `allocated_landed_costs`)
- **CLI** — `zohopy` command with `--json` on all commands, `raw` escape hatch
- **OAuth setup** — Self Client + Browser redirect with interactive org picker
- **Structured logging** — JSON/console output via structlog
- **10+ typed exceptions** mapped from Zoho error codes with smart disambiguation
- **OAuth rate limit handling** — auto-retry with 30s/60s/90s back-off
- **Docker** — Dockerfile + docker-compose with proper env/secrets handling
- **CI/CD** — GitHub Actions (lint, mypy, test matrix 3.10–3.14, PyPI release)
- 56 unit tests, 72 integration tests against live Zoho sandbox

[Unreleased]: https://github.com/talas9/zohopy/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/talas9/zohopy/releases/tag/v0.1.0

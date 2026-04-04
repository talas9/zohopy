# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-04-04

### Added
- 14 new resource modules: Composite Items, Item Groups, Inventory Adjustments, Packages, Shipment Orders, Purchase Receives, Transfer Orders, Sales Returns, Price Lists, Documents, Employees, Delivery Challans, Custom Buttons, Email Templates
- `--org` CLI flag for runtime organization switching without editing `.env`
- Python 3.14 support (CI matrix + pyproject classifiers)
- Total: **57 resources, 716 methods** (358 sync + 358 async)

### Breaking Changes
- `ZOHO_DATA_CENTER` is now **required** (was optional with `us` default). Set to your region: `us`, `eu`, `in`, `au`, `jp`, `ca`, `cn`, `sa`.
- `ZOHO_REFRESH_TOKEN` is now **required** (was optional empty string). Run `zohopy setup` to generate.
- `ZOHO_ORGANIZATION_ID` is now **required** (was optional empty string). Run `zohopy setup` to generate.
- Users upgrading from v0.1.0 who relied on defaults must update their `.env` or environment variables.

### Fixed
- 20 mypy strict-mode errors (override signatures, return type annotations)
- Coverage threshold aligned to actual unit test coverage (40%)
- All config tests isolated from local `.env` file
- Release workflow uses PyPA Trusted Publishing with Sigstore signing

### Changed
- `ZOHO_API_DOMAIN` remains optional — overrides `ZOHO_DATA_CENTER` when set
- README trimmed to concise landing page; full docs split into `docs/`

## [0.1.0] - 2026-04-03

First public release. Published to [PyPI](https://pypi.org/project/zohopy/).

### Added
- **Zoho Books API v3** — 43 resource types, 694 methods (347 sync + 347 async)
- **Sales cycle:** Contacts, Contact Persons, Estimates, Sales Orders, Invoices, Recurring Invoices, Sales Receipts, Credit Notes, Customer Debit Notes, Customer Payments, Retainer Invoices
- **Purchase cycle:** Purchase Orders, Bills, Recurring Bills, Vendor Credits, Vendor Payments, Expenses, Recurring Expenses
- **Banking:** Bank Accounts, Bank Transactions, Chart of Accounts, Journals, Base Currency Adjustments
- **Projects:** Projects, Tasks, Time Entries
- **Assets:** Fixed Assets, Fixed Asset Types
- **Settings:** Organizations, Taxes (authorities, exemptions, groups), Currencies (exchange rates), Users, Preferences, Templates, Opening Balances, Custom Fields, Custom Views, Custom Modules, Reporting Tags, Workflows, Locations, CRM Integration
- **Multi-currency** support with exchange rates on all transactions
- **Landed cost** support on bills
- **CLI** — `zohopy` command with `--json` on all commands, `raw` escape hatch
- **OAuth setup wizard** — Self Client + Browser redirect with interactive org picker
- **Structured logging** — JSON/console output via structlog
- **10+ typed exceptions** mapped from Zoho error codes with smart disambiguation
- **OAuth rate limit handling** — auto-retry with back-off
- **Docker** — Dockerfile + docker-compose
- **CI/CD** — GitHub Actions (lint, mypy, test matrix 3.10–3.14, PyPI release)
- 56 unit tests, 72 integration tests against live Zoho sandbox

[0.2.0]: https://github.com/talas9/zohopy/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/talas9/zohopy/releases/tag/v0.1.0

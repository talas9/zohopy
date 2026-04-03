# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-04-03

### Added

- **Zoho Books API v3** — complete coverage with 43 resource types and 347 methods (sync + async)
- **Sales cycle:** Contacts, Contact Persons, Estimates, Sales Orders, Invoices, Recurring Invoices, Sales Receipts, Credit Notes, Customer Debit Notes, Customer Payments, Retainer Invoices
- **Purchase cycle:** Purchase Orders, Bills, Recurring Bills, Vendor Credits, Vendor Payments, Expenses, Recurring Expenses
- **Banking:** Bank Accounts, Bank Transactions, Chart of Accounts, Journals, Base Currency Adjustments
- **Projects:** Projects, Tasks, Time Entries
- **Assets:** Fixed Assets, Fixed Asset Types
- **Settings:** Organizations, Taxes (+ authorities + exemptions), Currencies (+ exchange rates), Users, Preferences, Templates, Opening Balances, Custom Fields, Custom Views, Custom Modules, Reporting Tags, Workflows, Locations
- **Integration:** Zoho CRM import (customer, vendor, item)
- **Multi-currency** support on all transactions with exchange rates
- **Landed cost** support on bills
- **CLI** — `zohopy` command with 30+ commands, `--json` on every command
- **OAuth setup wizard** — Self Client + Browser redirect flows with org picker UI
- **Structured logging** via structlog (JSON/console)
- **Typed exceptions** — 10+ exception classes mapped from Zoho error codes
- **Docker + Docker Compose** support
- **CI/CD** — GitHub Actions with lint, type-check, test matrix (3.10–3.13), PyPI release

[Unreleased]: https://github.com/talas9/zohopy/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/talas9/zohopy/releases/tag/v0.1.0

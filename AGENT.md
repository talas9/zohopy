# ZohoPy — Agent Reference

Machine-readable reference for AI coding agents.
All CLI commands support `--json` for structured output.

## Quick Reference

```bash
# Setup
zohopy setup                                    # Interactive OAuth wizard
zohopy config --json                            # Show configuration

# Organizations
zohopy orgs --json                              # List all organizations

# Contacts
zohopy contacts list --json                     # List all contacts
zohopy contacts list --type customer --json     # Filter by type
zohopy contacts get CONTACT_ID --json           # Get single contact
zohopy contacts create '{"contact_name":"X","contact_type":"customer"}' --json

# Items
zohopy items list --json                        # List all items
zohopy items get ITEM_ID --json
zohopy items create '{"name":"Widget","rate":50}' --json

# Invoices
zohopy invoices list --json                     # List invoices
zohopy invoices list --status sent --json       # Filter by status
zohopy invoices get INVOICE_ID --json
zohopy invoices create '{"customer_id":"X","line_items":[{"item_id":"Y","quantity":1}]}' --json
zohopy invoices mark-sent INVOICE_ID --json
zohopy invoices void INVOICE_ID --json

# Bills
zohopy bills list --json
zohopy bills get BILL_ID --json
zohopy bills create '{"vendor_id":"X","bill_number":"B-001","date":"2026-04-03","line_items":[...]}' --json
zohopy bills void BILL_ID --json

# Estimates
zohopy estimates list --json
zohopy estimates get ESTIMATE_ID --json
zohopy estimates create '{"customer_id":"X","line_items":[...]}' --json

# Sales Orders
zohopy sales-orders list --json
zohopy sales-orders get SALESORDER_ID --json
zohopy sales-orders create '{"customer_id":"X","line_items":[...]}' --json

# Purchase Orders
zohopy purchase-orders list --json
zohopy purchase-orders get PURCHASEORDER_ID --json
zohopy purchase-orders create '{"vendor_id":"X","line_items":[...]}' --json

# Expenses
zohopy expenses list --json
zohopy expenses get EXPENSE_ID --json
zohopy expenses create '{"account_id":"X","amount":50,"date":"2026-04-03"}' --json

# Payments
zohopy payments list-customer --json
zohopy payments list-vendor --json

# Taxes
zohopy taxes list --json
zohopy taxes create '{"tax_name":"VAT","tax_percentage":5}' --json

# Settings
zohopy settings preferences --json
zohopy settings currencies --json
zohopy settings templates --json
zohopy settings users --json

# Raw API (escape hatch)
zohopy raw get /books/v3/contacts --json
zohopy raw post /books/v3/contacts --data '{"contact_name":"Test"}' --json
```

## Python SDK Quick Reference

```python
from zohopy import ZohoConfig, SyncZohoClient
from zohopy.products.books import ZohoBooks

with SyncZohoClient(ZohoConfig()) as client:
    books = ZohoBooks(client)

    # 43 resource attributes available:
    # books.contacts, books.invoices, books.items, books.bills,
    # books.estimates, books.sales_orders, books.purchase_orders,
    # books.expenses, books.credit_notes, books.vendor_credits,
    # books.customer_payments, books.vendor_payments,
    # books.recurring_invoices, books.recurring_bills,
    # books.recurring_expenses, books.sales_receipts,
    # books.retainer_invoices, books.customer_debit_notes,
    # books.contact_persons, books.bank_accounts,
    # books.bank_transactions, books.chart_of_accounts,
    # books.journals, books.base_currency_adjustments,
    # books.projects, books.tasks, books.time_entries,
    # books.fixed_assets, books.fixed_asset_types,
    # books.organizations, books.taxes, books.currencies,
    # books.users, books.preferences, books.templates,
    # books.opening_balances, books.custom_fields,
    # books.custom_views, books.custom_modules,
    # books.reporting_tags, books.workflows,
    # books.locations, books.crm_integration

    # Every resource has: create(), list(), get(id), update(id, data), delete(id)
    # Plus resource-specific actions (mark_sent, void, approve, etc.)
```

## Error Handling

```python
from zohopy import (
    ZohoNotFoundError,           # 404 — resource not found
    ZohoValidationError,         # 400 — bad request (base)
    ZohoInvalidFieldError,       # 400 code 2 — bad field value
    ZohoDuplicateError,          # 400 code 4 — already exists
    ZohoEmptyBodyError,          # 400 code 11 — missing body
    ZohoBusinessRuleError,       # 400 code 4xxx — rule violation
    ZohoFeatureNotEnabledError,  # 400 code 110xxx — enable first
    ZohoResourceDependentError,  # 400 code 36/1004 — has deps
    ZohoAuthenticationError,     # 401 — bad/expired token
    ZohoForbiddenError,          # 403 — insufficient scopes
    ZohoRateLimitError,          # 429 — rate limited (.retry_after)
    ZohoServerError,             # 5xx — Zoho server error
)
```

## Multi-Currency Transactions

All transaction endpoints (invoices, bills, estimates, etc.) support:
- `currency_id` — ID of the currency
- `exchange_rate` — exchange rate to base currency

```python
books.invoices.create({
    "customer_id": "...",
    "currency_id": "AED_CURRENCY_ID",
    "exchange_rate": 3.67,
    "line_items": [{"item_id": "...", "quantity": 1}],
})
```

## Landed Cost

Set `is_landed_cost: True` on bills:

```python
books.bills.create({
    "vendor_id": "...",
    "is_landed_cost": True,
    "line_items": [
        {"item_id": "...", "quantity": 1, "rate": 120}
    ],
})
# Response includes: allocated_landed_costs, unallocated_landed_costs
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `ZOHO_CLIENT_ID` | Yes | OAuth client ID |
| `ZOHO_CLIENT_SECRET` | Yes | OAuth client secret |
| `ZOHO_REFRESH_TOKEN` | Yes | Permanent refresh token |
| `ZOHO_ORGANIZATION_ID` | Yes | Zoho org ID |
| `ZOHO_API_DOMAIN` | No | Auto-detects data center |
| `ZOHO_DATA_CENTER` | No | Manual: us/eu/in/au/jp/ca/cn/sa |
| `ZOHOPY_LOG_LEVEL` | No | DEBUG/INFO/WARNING/ERROR |
| `ZOHOPY_LOG_FORMAT` | No | console/json |

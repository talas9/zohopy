# API Reference

Complete reference for all 57 Zoho Books v3 resources in ZohoPy.

Every resource supports base CRUD: `create()`, `list()`, `get(id)`, `update(id, data)`, `delete(id)` plus resource-specific actions listed below.

## Sales Cycle

| Resource | Attribute | Extra Methods |
|----------|-----------|---------------|
| Contacts | `books.contacts` | `mark_active`, `mark_inactive`, `enable_portal`, `enable_payment_reminders`, `disable_payment_reminders`, `email_contact`, `email_statement`, `list_comments`, `list_addresses`, `add_address`, `edit_address`, `delete_address`, `list_refunds`, `track_1099`, `untrack_1099`, `get_unused_retainer_payments` |
| Contact Persons | `books.contact_persons` | `create_for_contact`, `list_for_contact`, `get_for_contact`, `update_for_contact`, `delete_for_contact`, `mark_primary` |
| Estimates | `books.estimates` | `mark_sent`, `mark_accepted`, `mark_declined`, `submit_for_approval`, `approve`, `email`, `get_email_content`, `email_multiple`, `update_billing_address`, `update_shipping_address`, `list_templates`, `update_template`, `update_custom_fields`, `list_comments`, `add_comment`, `update_comment`, `delete_comment` |
| Sales Orders | `books.sales_orders` | `mark_open`, `mark_void`, `submit_for_approval`, `approve`, `email`, `get_email_content`, `update_sub_status`, `update_billing_address`, `update_shipping_address`, `list_templates`, `update_template`, `add_attachment`, `get_attachment`, `delete_attachment`, `update_custom_fields`, `list_comments`, `add_comment`, `update_comment`, `delete_comment` |
| Invoices | `books.invoices` | `mark_sent`, `void`, `mark_draft`, `submit_for_approval`, `approve`, `email`, `get_email_content`, `email_multiple`, `create_instant`, `associate_with_sales_order`, `remind_customer`, `get_reminder_content`, `enable_reminder`, `disable_reminder`, `write_off`, `cancel_write_off`, `apply_credits`, `generate_payment_link`, `update_billing_address`, `update_shipping_address`, `list_templates`, `update_template`, `list_payments`, `list_credits_applied`, `delete_payment`, `delete_credit_applied`, `add_attachment`, `get_attachment`, `delete_attachment`, `update_custom_fields`, `list_comments`, `add_comment`, `update_comment`, `delete_comment` |
| Recurring Invoices | `books.recurring_invoices` | `stop`, `resume`, `update_template`, `list_history` |
| Sales Receipts | `books.sales_receipts` | `email` |
| Credit Notes | `books.credit_notes` | `void`, `to_draft`, `to_open`, `submit_for_approval`, `approve`, `email`, `get_email_content`, `email_history`, `apply_to_invoice`, `list_invoices_credited`, `delete_invoices_credited`, `refund`, `list_refunds`, `get_refund`, `update_refund`, `delete_refund`, `update_billing_address`, `update_shipping_address`, `list_templates`, `update_template`, `list_comments` |
| Customer Debit Notes | `books.customer_debit_notes` | *(CRUD only)* |
| Customer Payments | `books.customer_payments` | `refund`, `list_refunds`, `get_refund`, `update_refund`, `delete_refund`, `bulk_delete`, `update_custom_fields` |
| Retainer Invoices | `books.retainer_invoices` | `mark_sent`, `void`, `mark_draft`, `submit_for_approval`, `approve`, `email`, `get_email_content`, `update_billing_address`, `list_templates`, `update_template`, `add_attachment`, `get_attachment`, `delete_attachment`, `list_comments`, `add_comment`, `update_comment`, `delete_comment` |
| Sales Returns | `books.sales_returns` | `create_receive`, `delete_receive` |
| Delivery Challans | `books.delivery_challans` | `mark_delivered` |

## Purchase Cycle

| Resource | Attribute | Extra Methods |
|----------|-----------|---------------|
| Purchase Orders | `books.purchase_orders` | `mark_open`, `mark_billed`, `cancel`, `reject`, `submit_for_approval`, `approve`, `email`, `get_email_content`, `update_billing_address`, `list_templates`, `update_template`, `add_attachment`, `get_attachment`, `delete_attachment`, `update_custom_fields`, `list_comments`, `update_comment`, `delete_comment` |
| Bills | `books.bills` | `void`, `mark_open`, `submit_for_approval`, `approve`, `apply_credits`, `list_payments`, `delete_payment`, `update_billing_address`, `add_attachment`, `get_attachment`, `delete_attachment`, `update_custom_fields`, `convert_from_po`, `list_comments`, `add_comment` |
| Recurring Bills | `books.recurring_bills` | `stop`, `resume`, `list_history` |
| Vendor Credits | `books.vendor_credits` | `convert_to_open`, `void`, `submit_for_approval`, `approve`, `apply_to_bill`, `list_bills_credited`, `delete_bills_credited`, `refund`, `list_refunds`, `get_refund`, `update_refund`, `delete_refund`, `list_comments`, `add_comment`, `delete_comment` |
| Vendor Payments | `books.vendor_payments` | `refund`, `list_refunds`, `get_refund`, `update_refund`, `delete_refund`, `email`, `get_email_content`, `bulk_delete` |
| Expenses | `books.expenses` | `list_comments`, `add_receipt`, `get_receipt`, `delete_receipt`, `add_attachment`, `create_employee`, `list_employees`, `get_employee`, `delete_employee` |
| Recurring Expenses | `books.recurring_expenses` | `stop`, `resume`, `list_child_expenses`, `list_history` |
| Purchase Receives | `books.purchase_receives` | *(CRUD only)* |

## Items & Inventory

| Resource | Attribute | Extra Methods |
|----------|-----------|---------------|
| Items | `books.items` | `mark_active`, `mark_inactive` |
| Composite Items | `books.composite_items` | `mark_active`, `mark_inactive` |
| Item Groups | `books.item_groups` | `mark_active`, `mark_inactive` |
| Inventory Adjustments | `books.inventory_adjustments` | *(CRUD only)* |
| Packages | `books.packages` | *(CRUD only)* |
| Shipment Orders | `books.shipment_orders` | `mark_delivered` |
| Transfer Orders | `books.transfer_orders` | `mark_received` |
| Price Lists | `books.price_lists` | `mark_active`, `mark_inactive` |

## Banking & Accounting

| Resource | Attribute | Extra Methods |
|----------|-----------|---------------|
| Bank Accounts | `books.bank_accounts` | `activate`, `deactivate`, `import_statement`, `get_last_statement`, `delete_last_statement` |
| Bank Transactions | `books.bank_transactions` | `match`, `unmatch`, `exclude`, `restore`, `categorize`, `uncategorize`, `get_matching`, `categorize_as_expense`, `categorize_as_vendor_payment`, `categorize_as_customer_payment`, `categorize_as_cn_refund`, `categorize_as_vc_refund`, `categorize_as_cp_refund`, `categorize_as_vp_refund` |
| Chart of Accounts | `books.chart_of_accounts` | `mark_active`, `mark_inactive`, `list_transactions`, `delete_transaction` |
| Journals | `books.journals` | `publish`, `add_comment`, `add_attachment`, `delete_comment` |
| Base Currency Adj. | `books.base_currency_adjustments` | `list_account_details` |

## Projects & Time

| Resource | Attribute | Extra Methods |
|----------|-----------|---------------|
| Projects | `books.projects` | `activate`, `inactivate`, `clone`, `list_users`, `assign_users`, `invite_user`, `get_user`, `update_user`, `delete_user`, `list_tasks`, `add_task`, `get_task`, `update_task`, `delete_task`, `list_comments`, `add_comment`, `delete_comment`, `list_invoices` |
| Tasks | `books.tasks` | `mark_open`, `mark_ongoing`, `mark_completed`, `update_completed_percentage`, `add_comment`, `list_comments`, `delete_comment`, `add_attachment`, `get_attachment`, `delete_attachment` |
| Time Entries | `books.time_entries` | `start_timer`, `stop_timer`, `get_timer` |

## Fixed Assets

| Resource | Attribute | Extra Methods |
|----------|-----------|---------------|
| Fixed Assets | `books.fixed_assets` | `mark_active`, `cancel`, `mark_draft`, `write_off`, `sell`, `list_history`, `get_forecast_depreciation`, `list_comments`, `add_comment`, `delete_comment` |
| Fixed Asset Types | `books.fixed_asset_types` | *(CRUD only)* |

## Documents & Employees

| Resource | Attribute | Extra Methods |
|----------|-----------|---------------|
| Documents | `books.documents` | *(CRUD only)* |
| Employees | `books.employees` | *(CRUD only)* |

## Settings & Configuration

| Resource | Attribute | Extra Methods |
|----------|-----------|---------------|
| Organizations | `books.organizations` | *(CRUD only)* |
| Taxes | `books.taxes` | `create_group`, `get_group`, `delete_group`, `create_authority`, `list_authorities`, `update_authority`, `get_authority`, `delete_authority`, `create_exemption`, `list_exemptions`, `update_exemption`, `get_exemption`, `delete_exemption` |
| Currencies | `books.currencies` | `list_exchange_rates`, `create_exchange_rate`, `get_exchange_rate`, `update_exchange_rate`, `delete_exchange_rate` |
| Users | `books.users` | `create`, `get_current`, `invite`, `mark_active`, `mark_inactive` |
| Preferences | `books.preferences` | `get()`, `update(data)` |
| Templates | `books.templates` | *(list only)* |
| Opening Balances | `books.opening_balances` | `get()`, `create(data)`, `update(data)`, `delete()` |
| Custom Fields | `books.custom_fields` | `list_for_entity`, `reorder`, `update_status`, `update_dropdown_options`, `bulk_fetch`, `get_usage`, `check_formula`, `list_lookup_fields`, `list_simple`, `get_fields_meta`, `get_entity_fields_meta` |
| Custom Views | `books.custom_views` | `reorder`, `list_created`, `get_search_fields` |
| Custom Modules | `books.custom_modules` | `create_record`, `list_records`, `get_record`, `update_record`, `delete_record`, `bulk_update_records`, `delete_records` |
| Custom Buttons | `books.custom_buttons` | *(CRUD only)* |
| Email Templates | `books.email_templates` | *(CRUD only)* |
| Reporting Tags | `books.reporting_tags` | `mark_active`, `mark_inactive`, `mark_default_option`, `update_options`, `update_visibility`, `mark_option_active`, `mark_option_inactive`, `get_options_detail`, `get_all_options`, `reorder` |
| Workflows | `books.workflows` | *(list only)* |
| Locations | `books.locations` | `enable`, `mark_active`, `mark_inactive`, `mark_primary` |
| CRM Integration | `books.crm_integration` | `import_customer_by_account`, `import_customer_by_contact`, `import_vendor`, `import_item` |

## Async Usage

Every sync class has an async counterpart:

```python
from zohopy import AsyncZohoClient, ZohoConfig
from zohopy.products.books import AsyncZohoBooks

async with AsyncZohoClient(ZohoConfig()) as client:
    books = AsyncZohoBooks(client)
    contacts = await books.contacts.list()
    async for page in books.items.list_all():
        print(page)
```

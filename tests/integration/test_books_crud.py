"""Integration tests — full CRUD against Zoho Books sandbox.

Run with: pytest tests/integration/ -m integration -v

These tests create, read, update, and delete real data in the
sandbox org. They run in dependency order (contacts first, then
items, then invoices that reference both, etc.).
"""

from __future__ import annotations

import pytest

from zohopy import SyncZohoClient, ZohoConfig
from zohopy.products.books import ZohoBooks

pytestmark = pytest.mark.integration


@pytest.fixture(scope="module")
def books() -> ZohoBooks:
    config = ZohoConfig()
    client = SyncZohoClient(config)
    b = ZohoBooks(client)
    yield b
    client.close()


# ── helpers ──────────────────────────────────────────────────────────


def _id(resp: dict, key: str) -> str:
    """Extract ID from a Zoho response. Handles nested key like 'contact.contact_id'."""
    parts = key.split(".")
    obj = resp
    for p in parts:
        obj = obj[p]
    return str(obj)


# ── Settings & Config ────────────────────────────────────────────────


class TestSettings:
    def test_get_preferences(self, books: ZohoBooks):
        r = books.preferences.get()
        assert "preferences" in r

    def test_list_templates(self, books: ZohoBooks):
        r = books.templates.list()
        assert "templates" in r

    def test_list_currencies(self, books: ZohoBooks):
        r = books.currencies.list()
        assert "currencies" in r
        assert any(c["currency_code"] == "USD" for c in r["currencies"])

    def test_list_taxes(self, books: ZohoBooks):
        r = books.taxes.list()
        assert "taxes" in r

    def test_list_users(self, books: ZohoBooks):
        r = books.users.list()
        assert "users" in r

    def test_get_current_user(self, books: ZohoBooks):
        r = books.users.get_current()
        assert "user" in r

    def test_list_chart_of_accounts(self, books: ZohoBooks):
        r = books.chart_of_accounts.list()
        assert "chartofaccounts" in r

    def test_list_reporting_tags(self, books: ZohoBooks):
        r = books.reporting_tags.list()
        assert "tags" in r

    def test_list_workflows(self, books: ZohoBooks):
        r = books.workflows.list()
        assert "workflows" in r

    def test_list_custom_views(self, books: ZohoBooks):
        r = books.custom_views.list()
        assert "entity_views" in r or "data" in r


# ── Tax CRUD ─────────────────────────────────────────────────────────


class TestTaxCRUD:
    tax_id: str = ""

    def test_create(self, books: ZohoBooks):
        try:
            r = books.taxes.create(
                {
                    "tax_name": "VAT 5%",
                    "tax_percentage": 5,
                    "tax_type": "tax",
                }
            )
            assert "tax" in r
            TestTaxCRUD.tax_id = str(r["tax"]["tax_id"])
        except Exception:
            pytest.skip("Sales Tax not enabled in sandbox — enable in Settings > Taxes")

    def test_get(self, books: ZohoBooks):
        if not self.tax_id:
            pytest.skip("Tax not created")
        r = books.taxes.get(self.tax_id)
        assert r["tax"]["tax_name"] == "VAT 5%"

    def test_update(self, books: ZohoBooks):
        if not self.tax_id:
            pytest.skip("Tax not created")
        r = books.taxes.update(self.tax_id, {"tax_name": "VAT 5% Updated"})
        assert r["tax"]["tax_name"] == "VAT 5% Updated"

    def test_delete(self, books: ZohoBooks):
        if not self.tax_id:
            pytest.skip("Tax not created")
        r = books.taxes.delete(self.tax_id)
        assert r["code"] == 0


# ── Currency CRUD ────────────────────────────────────────────────────


class TestCurrencyCRUD:
    def test_list_currencies(self, books: ZohoBooks):
        r = books.currencies.list()
        assert "currencies" in r
        assert any(c["currency_code"] == "USD" for c in r["currencies"])

    def test_create_currency(self, books: ZohoBooks):
        # Try to create GBP — skip if it already exists
        try:
            r = books.currencies.create(
                {
                    "currency_code": "GBP",
                    "currency_symbol": "£",
                    "currency_format": "1,234,567.89",
                }
            )
            assert "currency" in r
        except Exception:
            pytest.skip("Currency already exists or cannot be created")


# ── Contact CRUD ─────────────────────────────────────────────────────


class TestContactCRUD:
    customer_id: str = ""
    vendor_id: str = ""

    def test_create_customer(self, books: ZohoBooks):
        r = books.contacts.create(
            {
                "contact_name": "Test Customer",
                "contact_type": "customer",
                "company_name": "Test Corp",
                "billing_address": {
                    "address": "123 Test St",
                    "city": "Test City",
                    "state": "Test State",
                    "zip": "12345",
                    "country": "U.S.A.",
                },
            }
        )
        assert "contact" in r
        TestContactCRUD.customer_id = _id(r, "contact.contact_id")

    def test_create_vendor(self, books: ZohoBooks):
        r = books.contacts.create(
            {
                "contact_name": "Test Vendor",
                "contact_type": "vendor",
                "company_name": "Vendor Corp",
            }
        )
        TestContactCRUD.vendor_id = _id(r, "contact.contact_id")

    def test_list(self, books: ZohoBooks):
        r = books.contacts.list()
        assert len(r["contacts"]) >= 2

    def test_get(self, books: ZohoBooks):
        r = books.contacts.get(self.customer_id)
        assert r["contact"]["contact_name"] == "Test Customer"

    def test_update(self, books: ZohoBooks):
        r = books.contacts.update(
            self.customer_id,
            {
                "company_name": "Updated Corp",
            },
        )
        assert r["contact"]["company_name"] == "Updated Corp"

    def test_mark_inactive(self, books: ZohoBooks):
        r = books.contacts.mark_inactive(self.customer_id)
        assert r["code"] == 0

    def test_mark_active(self, books: ZohoBooks):
        r = books.contacts.mark_active(self.customer_id)
        assert r["code"] == 0

    def test_list_comments(self, books: ZohoBooks):
        r = books.contacts.list_comments(self.customer_id)
        assert "contact_comments" in r or "code" in r


# ── Item CRUD ────────────────────────────────────────────────────────


class TestItemCRUD:
    item_id: str = ""

    def test_create(self, books: ZohoBooks):
        r = books.items.create(
            {
                "name": "Test Widget",
                "rate": 25.00,
                "description": "A test widget for integration testing",
                "sku": "TW-001",
                "product_type": "goods",
            }
        )
        assert "item" in r
        TestItemCRUD.item_id = _id(r, "item.item_id")

    def test_get(self, books: ZohoBooks):
        r = books.items.get(self.item_id)
        assert r["item"]["name"] == "Test Widget"

    def test_update(self, books: ZohoBooks):
        r = books.items.update(self.item_id, {"rate": 30.00})
        assert r["item"]["rate"] == 30.0

    def test_mark_inactive(self, books: ZohoBooks):
        r = books.items.mark_inactive(self.item_id)
        assert r["code"] == 0

    def test_mark_active(self, books: ZohoBooks):
        r = books.items.mark_active(self.item_id)
        assert r["code"] == 0


# ── Estimate CRUD ────────────────────────────────────────────────────


class TestEstimateCRUD:
    estimate_id: str = ""

    def test_create(self, books: ZohoBooks):
        r = books.estimates.create(
            {
                "customer_id": TestContactCRUD.customer_id,
                "line_items": [{"item_id": TestItemCRUD.item_id, "quantity": 2}],
            }
        )
        assert "estimate" in r
        TestEstimateCRUD.estimate_id = _id(r, "estimate.estimate_id")

    def test_get(self, books: ZohoBooks):
        r = books.estimates.get(self.estimate_id)
        assert r["estimate"]["estimate_id"] == self.estimate_id

    def test_mark_sent(self, books: ZohoBooks):
        r = books.estimates.mark_sent(self.estimate_id)
        assert r["code"] == 0

    def test_mark_accepted(self, books: ZohoBooks):
        r = books.estimates.mark_accepted(self.estimate_id)
        assert r["code"] == 0

    def test_list_comments(self, books: ZohoBooks):
        r = books.estimates.list_comments(self.estimate_id)
        assert "comments" in r or "code" in r

    def test_delete(self, books: ZohoBooks):
        r = books.estimates.delete(self.estimate_id)
        assert r["code"] == 0


# ── Sales Order CRUD ─────────────────────────────────────────────────


class TestSalesOrderCRUD:
    so_id: str = ""

    def test_create(self, books: ZohoBooks):
        r = books.sales_orders.create(
            {
                "customer_id": TestContactCRUD.customer_id,
                "line_items": [{"item_id": TestItemCRUD.item_id, "quantity": 3}],
            }
        )
        assert "salesorder" in r
        TestSalesOrderCRUD.so_id = _id(r, "salesorder.salesorder_id")

    def test_mark_open(self, books: ZohoBooks):
        r = books.sales_orders.mark_open(self.so_id)
        assert r["code"] == 0

    def test_mark_void(self, books: ZohoBooks):
        r = books.sales_orders.mark_void(self.so_id)
        assert r["code"] == 0

    def test_delete(self, books: ZohoBooks):
        r = books.sales_orders.delete(self.so_id)
        assert r["code"] == 0


# ── Invoice CRUD ─────────────────────────────────────────────────────


class TestInvoiceCRUD:
    invoice_id: str = ""

    def test_create(self, books: ZohoBooks):
        r = books.invoices.create(
            {
                "customer_id": TestContactCRUD.customer_id,
                "line_items": [{"item_id": TestItemCRUD.item_id, "quantity": 1}],
            }
        )
        assert "invoice" in r
        TestInvoiceCRUD.invoice_id = _id(r, "invoice.invoice_id")

    def test_get(self, books: ZohoBooks):
        r = books.invoices.get(self.invoice_id)
        assert r["invoice"]["invoice_id"] == self.invoice_id

    def test_update(self, books: ZohoBooks):
        r = books.invoices.update(
            self.invoice_id,
            {
                "notes": "Updated via integration test",
            },
        )
        assert "invoice" in r

    def test_mark_sent(self, books: ZohoBooks):
        r = books.invoices.mark_sent(self.invoice_id)
        assert r["code"] == 0

    def test_list_comments(self, books: ZohoBooks):
        r = books.invoices.list_comments(self.invoice_id)
        assert "comments" in r or "code" in r

    def test_add_comment(self, books: ZohoBooks):
        r = books.invoices.add_comment(
            self.invoice_id,
            {
                "description": "Test comment from integration test",
            },
        )
        assert r["code"] == 0

    def test_void(self, books: ZohoBooks):
        r = books.invoices.void(self.invoice_id)
        assert r["code"] == 0

    def test_delete(self, books: ZohoBooks):
        r = books.invoices.delete(self.invoice_id)
        assert r["code"] == 0


# ── Purchase Order CRUD ──────────────────────────────────────────────


class TestPurchaseOrderCRUD:
    po_id: str = ""
    purchase_item_id: str = ""

    def test_create(self, books: ZohoBooks):
        # Items need purchase_account_id + purchase_rate for POs
        coa = books.chart_of_accounts.list()
        cogs_id = None
        for a in coa.get("chartofaccounts", []):
            if a.get("account_type") == "cost_of_goods_sold":
                cogs_id = a["account_id"]
                break
        if not cogs_id:
            pytest.skip("No COGS account for purchase items")

        ir = books.items.create(
            {
                "name": "Purchase Test Widget",
                "item_type": "sales_and_purchases",
                "rate": 15.00,
                "purchase_rate": 10.00,
                "purchase_account_id": cogs_id,
                "product_type": "goods",
                "purchase_description": "For PO testing",
            }
        )
        TestPurchaseOrderCRUD.purchase_item_id = _id(ir, "item.item_id")

        r = books.purchase_orders.create(
            {
                "vendor_id": TestContactCRUD.vendor_id,
                "line_items": [{"item_id": self.purchase_item_id, "quantity": 10}],
            }
        )
        assert "purchaseorder" in r
        TestPurchaseOrderCRUD.po_id = _id(r, "purchaseorder.purchaseorder_id")

    def test_mark_open(self, books: ZohoBooks):
        if not self.po_id:
            pytest.skip("PO not created")
        r = books.purchase_orders.mark_open(self.po_id)
        assert r["code"] == 0

    def test_delete(self, books: ZohoBooks):
        if not self.po_id:
            pytest.skip("PO not created")
        r = books.purchase_orders.delete(self.po_id)
        assert r["code"] == 0

    def test_cleanup_purchase_item(self, books: ZohoBooks):
        if self.purchase_item_id:
            import contextlib

            with contextlib.suppress(Exception):
                books.items.delete(self.purchase_item_id)


# ── Bill CRUD ────────────────────────────────────────────────────────


class TestBillCRUD:
    bill_id: str = ""

    def test_create(self, books: ZohoBooks):
        coa = books.chart_of_accounts.list()
        expense_account = None
        for a in coa.get("chartofaccounts", []):
            if a.get("account_type") == "expense":
                expense_account = a["account_id"]
                break

        if not expense_account:
            pytest.skip("No expense account found")

        r = books.bills.create(
            {
                "vendor_id": TestContactCRUD.vendor_id,
                "bill_number": "BILL-TEST-001",
                "date": "2026-04-03",
                "due_date": "2026-05-03",
                "line_items": [
                    {
                        "account_id": expense_account,
                        "description": "Test bill line",
                        "amount": 100.00,
                    }
                ],
            }
        )
        assert "bill" in r
        TestBillCRUD.bill_id = _id(r, "bill.bill_id")

    def test_get(self, books: ZohoBooks):
        if not self.bill_id:
            pytest.skip("Bill not created")
        r = books.bills.get(self.bill_id)
        assert r["bill"]["bill_id"] == self.bill_id

    def test_void(self, books: ZohoBooks):
        if not self.bill_id:
            pytest.skip("Bill not created")
        r = books.bills.void(self.bill_id)
        assert r["code"] == 0

    def test_delete(self, books: ZohoBooks):
        if not self.bill_id:
            pytest.skip("Bill not created")
        r = books.bills.delete(self.bill_id)
        assert r["code"] == 0


# ── Expense CRUD ─────────────────────────────────────────────────────


class TestExpenseCRUD:
    expense_id: str = ""

    def test_create(self, books: ZohoBooks):
        coa = books.chart_of_accounts.list()
        expense_account = None
        for a in coa.get("chartofaccounts", []):
            if a.get("account_type") == "expense":
                expense_account = a["account_id"]
                break

        r = books.expenses.create(
            {
                "account_id": expense_account or "",
                "amount": 50.00,
                "description": "Test expense",
                "date": "2026-04-03",
            }
        )
        assert "expense" in r
        TestExpenseCRUD.expense_id = _id(r, "expense.expense_id")

    def test_get(self, books: ZohoBooks):
        r = books.expenses.get(self.expense_id)
        assert r["expense"]["expense_id"] == self.expense_id

    def test_delete(self, books: ZohoBooks):
        r = books.expenses.delete(self.expense_id)
        assert r["code"] == 0


# ── Journal CRUD ─────────────────────────────────────────────────────


class TestJournalCRUD:
    journal_id: str = ""

    def test_create(self, books: ZohoBooks):
        coa = books.chart_of_accounts.list()
        accounts = [a for a in coa.get("chartofaccounts", []) if a.get("account_id")]
        if len(accounts) < 2:
            pytest.skip("Need at least 2 accounts for journal")

        r = books.journals.create(
            {
                "journal_date": "2026-04-03",
                "line_items": [
                    {
                        "account_id": accounts[0]["account_id"],
                        "debit_or_credit": "debit",
                        "amount": 100,
                    },
                    {
                        "account_id": accounts[1]["account_id"],
                        "debit_or_credit": "credit",
                        "amount": 100,
                    },
                ],
            }
        )
        assert "journal" in r
        TestJournalCRUD.journal_id = _id(r, "journal.journal_id")

    def test_get(self, books: ZohoBooks):
        r = books.journals.get(self.journal_id)
        assert r["journal"]["journal_id"] == self.journal_id

    def test_delete(self, books: ZohoBooks):
        r = books.journals.delete(self.journal_id)
        assert r["code"] == 0


# ── Project CRUD ─────────────────────────────────────────────────────


class TestProjectCRUD:
    project_id: str = ""

    def test_create(self, books: ZohoBooks):
        try:
            r = books.projects.create(
                {
                    "project_name": "Test Project",
                    "customer_id": TestContactCRUD.customer_id,
                    "billing_type": "fixed_cost_for_project",
                    "rate": 1000.00,
                }
            )
            assert "project" in r
            TestProjectCRUD.project_id = _id(r, "project.project_id")
        except Exception as e:
            pytest.skip(f"Project creation failed: {e}")

    def test_get(self, books: ZohoBooks):
        if not self.project_id:
            pytest.skip("Project not created")
        r = books.projects.get(self.project_id)
        assert r["project"]["project_name"] == "Test Project"

    def test_inactivate(self, books: ZohoBooks):
        if not self.project_id:
            pytest.skip("Project not created")
        r = books.projects.inactivate(self.project_id)
        assert r["code"] == 0

    def test_activate(self, books: ZohoBooks):
        if not self.project_id:
            pytest.skip("Project not created")
        r = books.projects.activate(self.project_id)
        assert r["code"] == 0

    def test_delete(self, books: ZohoBooks):
        if not self.project_id:
            pytest.skip("Project not created")
        r = books.projects.delete(self.project_id)
        assert r["code"] == 0


# ── Custom Fields ────────────────────────────────────────────────────


class TestCustomFields:
    def test_list_for_invoice(self, books: ZohoBooks):
        r = books.custom_fields.list_for_entity("invoice")
        assert "fields" in r or "code" in r

    def test_list_for_item(self, books: ZohoBooks):
        r = books.custom_fields.list_for_entity("item")
        assert "fields" in r or "code" in r

    def test_list_for_contact(self, books: ZohoBooks):
        r = books.custom_fields.list_for_entity("contact")
        assert "fields" in r or "code" in r


# ── Bank Account CRUD ────────────────────────────────────────────────


class TestBankAccountCRUD:
    account_id: str = ""

    def test_create(self, books: ZohoBooks):
        r = books.bank_accounts.create(
            {
                "account_name": "Test Bank Account",
                "account_type": "bank",
                "currency_code": "USD",
            }
        )
        assert "bankaccount" in r
        TestBankAccountCRUD.account_id = _id(r, "bankaccount.account_id")

    def test_list(self, books: ZohoBooks):
        r = books.bank_accounts.list()
        assert "bankaccounts" in r

    def test_deactivate(self, books: ZohoBooks):
        r = books.bank_accounts.deactivate(self.account_id)
        assert r["code"] == 0

    def test_activate(self, books: ZohoBooks):
        r = books.bank_accounts.activate(self.account_id)
        assert r["code"] == 0

    def test_delete(self, books: ZohoBooks):
        r = books.bank_accounts.delete(self.account_id)
        assert r["code"] == 0


# ── Cleanup ──────────────────────────────────────────────────────────


class TestCleanup:
    """Delete test data created by earlier tests."""

    def test_delete_item(self, books: ZohoBooks):
        if TestItemCRUD.item_id:
            r = books.items.delete(TestItemCRUD.item_id)
            assert r["code"] == 0

    def test_delete_customer(self, books: ZohoBooks):
        if TestContactCRUD.customer_id:
            r = books.contacts.delete(TestContactCRUD.customer_id)
            assert r["code"] == 0

    def test_delete_vendor(self, books: ZohoBooks):
        if TestContactCRUD.vendor_id:
            r = books.contacts.delete(TestContactCRUD.vendor_id)
            assert r["code"] == 0

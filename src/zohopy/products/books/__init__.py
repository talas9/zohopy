"""Zoho Books API v3 — complete coverage.

Reference: https://www.zoho.com/books/api/v3/introduction/#overview
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from zohopy.products.books.accounting import (
    AsyncChartOfAccounts,
    AsyncJournals,
    ChartOfAccounts,
    Journals,
)
from zohopy.products.books.bank_transactions import (
    AsyncBankTransactions,
    BankTransactions,
)
from zohopy.products.books.banking import AsyncBankAccounts, BankAccounts
from zohopy.products.books.base_currency import (
    AsyncBaseCurrencyAdjustments,
    BaseCurrencyAdjustments,
)
from zohopy.products.books.bills import AsyncBills, Bills
from zohopy.products.books.contact_persons import (
    AsyncContactPersons,
    ContactPersons,
)
from zohopy.products.books.contacts import AsyncContacts, Contacts
from zohopy.products.books.credit_notes import AsyncCreditNotes, CreditNotes
from zohopy.products.books.crm_integration import (
    AsyncCRMIntegration,
    CRMIntegration,
)
from zohopy.products.books.custom_fields import AsyncCustomFields, CustomFields
from zohopy.products.books.custom_modules import (
    AsyncCustomModules,
    CustomModules,
)
from zohopy.products.books.customer_debit_notes import (
    AsyncCustomerDebitNotes,
    CustomerDebitNotes,
)
from zohopy.products.books.estimates import AsyncEstimates, Estimates
from zohopy.products.books.expenses import AsyncExpenses, Expenses
from zohopy.products.books.fixed_asset_types import (
    AsyncFixedAssetTypes,
    FixedAssetTypes,
)
from zohopy.products.books.fixed_assets import AsyncFixedAssets, FixedAssets
from zohopy.products.books.invoices import AsyncInvoices, Invoices
from zohopy.products.books.items import AsyncItems, Items
from zohopy.products.books.locations import (
    AsyncLocations,
    Locations,
)
from zohopy.products.books.payments import (
    AsyncCustomerPayments,
    AsyncVendorPayments,
    CustomerPayments,
    VendorPayments,
)
from zohopy.products.books.projects import (
    AsyncProjects,
    AsyncTasks,
    AsyncTimeEntries,
    Projects,
    Tasks,
    TimeEntries,
)
from zohopy.products.books.purchase_orders import (
    AsyncPurchaseOrders,
    PurchaseOrders,
)
from zohopy.products.books.recurring_bills import (
    AsyncRecurringBills,
    RecurringBills,
)
from zohopy.products.books.recurring_expenses import (
    AsyncRecurringExpenses,
    RecurringExpenses,
)
from zohopy.products.books.recurring_invoices import (
    AsyncRecurringInvoices,
    RecurringInvoices,
)
from zohopy.products.books.reporting_tags import (
    AsyncReportingTags,
    ReportingTags,
)
from zohopy.products.books.retainer_invoices import (
    AsyncRetainerInvoices,
    RetainerInvoices,
)
from zohopy.products.books.sales_orders import AsyncSalesOrders, SalesOrders
from zohopy.products.books.sales_receipts import (
    AsyncSalesReceipts,
    SalesReceipts,
)
from zohopy.products.books.settings import (
    AsyncCurrencies,
    AsyncCustomViews,
    AsyncOpeningBalances,
    AsyncOrganizations,
    AsyncPreferences,
    AsyncTaxes,
    AsyncTemplates,
    AsyncUsers,
    AsyncWorkflows,
    Currencies,
    CustomViews,
    OpeningBalances,
    Organizations,
    Preferences,
    Taxes,
    Templates,
    Users,
    Workflows,
)
from zohopy.products.books.vendor_credits import (
    AsyncVendorCredits,
    VendorCredits,
)

if TYPE_CHECKING:
    from zohopy._client import AsyncZohoClient, SyncZohoClient


class ZohoBooks:
    """Synchronous Zoho Books API v3 — complete coverage."""

    def __init__(self, client: SyncZohoClient) -> None:
        # Sales cycle
        self.contacts = Contacts(client)
        self.contact_persons = ContactPersons(client)
        self.estimates = Estimates(client)
        self.sales_orders = SalesOrders(client)
        self.invoices = Invoices(client)
        self.recurring_invoices = RecurringInvoices(client)
        self.sales_receipts = SalesReceipts(client)
        self.credit_notes = CreditNotes(client)
        self.customer_debit_notes = CustomerDebitNotes(client)
        self.customer_payments = CustomerPayments(client)
        self.retainer_invoices = RetainerInvoices(client)

        # Purchase cycle
        self.purchase_orders = PurchaseOrders(client)
        self.bills = Bills(client)
        self.recurring_bills = RecurringBills(client)
        self.vendor_credits = VendorCredits(client)
        self.vendor_payments = VendorPayments(client)
        self.expenses = Expenses(client)
        self.recurring_expenses = RecurringExpenses(client)

        # Items
        self.items = Items(client)

        # Banking
        self.bank_accounts = BankAccounts(client)
        self.bank_transactions = BankTransactions(client)

        # Accounting
        self.journals = Journals(client)
        self.chart_of_accounts = ChartOfAccounts(client)
        self.base_currency_adjustments = BaseCurrencyAdjustments(client)

        # Projects
        self.projects = Projects(client)
        self.tasks = Tasks(client)
        self.time_entries = TimeEntries(client)

        # Fixed Assets
        self.fixed_assets = FixedAssets(client)
        self.fixed_asset_types = FixedAssetTypes(client)

        # Settings & Config
        self.organizations = Organizations(client)
        self.taxes = Taxes(client)
        self.currencies = Currencies(client)
        self.users = Users(client)
        self.preferences = Preferences(client)
        self.templates = Templates(client)
        self.opening_balances = OpeningBalances(client)
        self.custom_fields = CustomFields(client)
        self.custom_views = CustomViews(client)
        self.custom_modules = CustomModules(client)
        self.reporting_tags = ReportingTags(client)
        self.workflows = Workflows(client)
        self.locations = Locations(client)
        self.crm_integration = CRMIntegration(client)


class AsyncZohoBooks:
    """Asynchronous Zoho Books API v3 — complete coverage."""

    def __init__(self, client: AsyncZohoClient) -> None:
        # Sales cycle
        self.contacts = AsyncContacts(client)
        self.contact_persons = AsyncContactPersons(client)
        self.estimates = AsyncEstimates(client)
        self.sales_orders = AsyncSalesOrders(client)
        self.invoices = AsyncInvoices(client)
        self.recurring_invoices = AsyncRecurringInvoices(client)
        self.sales_receipts = AsyncSalesReceipts(client)
        self.credit_notes = AsyncCreditNotes(client)
        self.customer_debit_notes = AsyncCustomerDebitNotes(client)
        self.customer_payments = AsyncCustomerPayments(client)
        self.retainer_invoices = AsyncRetainerInvoices(client)

        # Purchase cycle
        self.purchase_orders = AsyncPurchaseOrders(client)
        self.bills = AsyncBills(client)
        self.recurring_bills = AsyncRecurringBills(client)
        self.vendor_credits = AsyncVendorCredits(client)
        self.vendor_payments = AsyncVendorPayments(client)
        self.expenses = AsyncExpenses(client)
        self.recurring_expenses = AsyncRecurringExpenses(client)

        # Items
        self.items = AsyncItems(client)

        # Banking
        self.bank_accounts = AsyncBankAccounts(client)
        self.bank_transactions = AsyncBankTransactions(client)

        # Accounting
        self.journals = AsyncJournals(client)
        self.chart_of_accounts = AsyncChartOfAccounts(client)
        self.base_currency_adjustments = AsyncBaseCurrencyAdjustments(client)

        # Projects
        self.projects = AsyncProjects(client)
        self.tasks = AsyncTasks(client)
        self.time_entries = AsyncTimeEntries(client)

        # Fixed Assets
        self.fixed_assets = AsyncFixedAssets(client)
        self.fixed_asset_types = AsyncFixedAssetTypes(client)

        # Settings & Config
        self.organizations = AsyncOrganizations(client)
        self.taxes = AsyncTaxes(client)
        self.currencies = AsyncCurrencies(client)
        self.users = AsyncUsers(client)
        self.preferences = AsyncPreferences(client)
        self.templates = AsyncTemplates(client)
        self.opening_balances = AsyncOpeningBalances(client)
        self.custom_fields = AsyncCustomFields(client)
        self.custom_views = AsyncCustomViews(client)
        self.custom_modules = AsyncCustomModules(client)
        self.reporting_tags = AsyncReportingTags(client)
        self.workflows = AsyncWorkflows(client)
        self.locations = AsyncLocations(client)
        self.crm_integration = AsyncCRMIntegration(client)


__all__ = ["AsyncZohoBooks", "ZohoBooks"]

"""Zoho Inventory API v1 — Items, warehouses, stock, shipments.

Ref: https://www.zoho.com/inventory/api/v1/introduction/#overview

Status: Coming soon. The module structure is in place but not yet
integration-tested. Use at your own risk until v0.2.0.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from zohopy.products.inventory.adjustments import AsyncItemAdjustments, ItemAdjustments
from zohopy.products.inventory.bills import AsyncInvBills, InvBills
from zohopy.products.inventory.composite_items import AsyncCompositeItems, CompositeItems
from zohopy.products.inventory.contacts import AsyncInvContacts, InvContacts
from zohopy.products.inventory.invoices import AsyncInvInvoices, InvInvoices
from zohopy.products.inventory.item_groups import AsyncItemGroups, ItemGroups
from zohopy.products.inventory.items import AsyncItems as AsyncInvItems
from zohopy.products.inventory.items import Items as InvItems
from zohopy.products.inventory.packages import AsyncPackages, Packages
from zohopy.products.inventory.purchase_orders import AsyncInvPurchaseOrders, InvPurchaseOrders
from zohopy.products.inventory.sales_orders import AsyncInvSalesOrders, InvSalesOrders
from zohopy.products.inventory.settings import (
    AsyncInvOrganizations,
    AsyncInvTaxes,
    AsyncLocations,
    AsyncPriceLists,
    InvOrganizations,
    InvTaxes,
    Locations,
    PriceLists,
)
from zohopy.products.inventory.shipments import AsyncShipmentOrders, ShipmentOrders
from zohopy.products.inventory.transfer_orders import AsyncTransferOrders, TransferOrders

if TYPE_CHECKING:
    from zohopy._client import AsyncZohoClient, SyncZohoClient


class ZohoInventory:
    """Synchronous Zoho Inventory API v1 gateway."""

    def __init__(self, client: SyncZohoClient) -> None:
        self.items = InvItems(client)
        self.item_groups = ItemGroups(client)
        self.composite_items = CompositeItems(client)
        self.item_adjustments = ItemAdjustments(client)
        self.transfer_orders = TransferOrders(client)
        self.contacts = InvContacts(client)
        self.sales_orders = InvSalesOrders(client)
        self.packages = Packages(client)
        self.shipment_orders = ShipmentOrders(client)
        self.invoices = InvInvoices(client)
        self.purchase_orders = InvPurchaseOrders(client)
        self.bills = InvBills(client)
        self.organizations = InvOrganizations(client)
        self.taxes = InvTaxes(client)
        self.locations = Locations(client)
        self.price_lists = PriceLists(client)


class AsyncZohoInventory:
    """Asynchronous Zoho Inventory API v1 gateway."""

    def __init__(self, client: AsyncZohoClient) -> None:
        self.items = AsyncInvItems(client)
        self.item_groups = AsyncItemGroups(client)
        self.composite_items = AsyncCompositeItems(client)
        self.item_adjustments = AsyncItemAdjustments(client)
        self.transfer_orders = AsyncTransferOrders(client)
        self.contacts = AsyncInvContacts(client)
        self.sales_orders = AsyncInvSalesOrders(client)
        self.packages = AsyncPackages(client)
        self.shipment_orders = AsyncShipmentOrders(client)
        self.invoices = AsyncInvInvoices(client)
        self.purchase_orders = AsyncInvPurchaseOrders(client)
        self.bills = AsyncInvBills(client)
        self.organizations = AsyncInvOrganizations(client)
        self.taxes = AsyncInvTaxes(client)
        self.locations = AsyncLocations(client)
        self.price_lists = AsyncPriceLists(client)


__all__ = ["AsyncZohoInventory", "ZohoInventory"]

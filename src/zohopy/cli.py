"""zohopy CLI — Zoho Books from the command line.

Built for AI agents and human operators.
Every command supports --json for machine-readable output.

Usage:
    zohopy setup              # Interactive OAuth setup
    zohopy contacts list      # List contacts
    zohopy invoices create    # Create invoice from JSON
    zohopy --help             # Full help
"""

from __future__ import annotations

import json as json_mod
import sys
from typing import Any

import click

from zohopy import SyncZohoClient, ZohoConfig
from zohopy.products.books import ZohoBooks


def _get_client() -> tuple[SyncZohoClient, ZohoBooks]:
    """Create client from .env / env vars.

    Reads --org from Click context if available.
    """
    try:
        config = ZohoConfig()
        # Check if --org was passed via CLI
        ctx = click.get_current_context(silent=True)
        if ctx and ctx.obj and ctx.obj.get("org_id"):
            object.__setattr__(config, "organization_id", ctx.obj["org_id"])
        client = SyncZohoClient(config)
        return client, ZohoBooks(client)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        click.echo("Run 'zohopy setup' to configure.", err=True)
        sys.exit(1)


def _output(data: dict[str, Any], as_json: bool) -> None:
    """Print output as JSON or human-readable."""
    if as_json:
        click.echo(json_mod.dumps(data, indent=2, default=str))
    else:
        code = data.get("code", "")
        msg = data.get("message", "")
        if code == 0:
            for k, v in data.items():
                if k in ("code", "message", "page_context"):
                    continue
                if isinstance(v, list):
                    click.echo(f"{k}: {len(v)} items")
                    for item in v[:20]:
                        _print_record(item)
                elif isinstance(v, dict):
                    click.echo(f"{k}:")
                    _print_record(v)
        else:
            click.echo(f"Error ({code}): {msg}", err=True)


def _print_record(record: dict[str, Any]) -> None:
    """Print a single record in human-readable format."""
    id_keys = [k for k in record if k.endswith("_id")]
    name_keys = [k for k in record if "name" in k]
    important = id_keys[:1] + name_keys[:2]
    parts = []
    for k in important:
        parts.append(f"{k}={record[k]}")
    if "status" in record:
        parts.append(f"status={record['status']}")
    if "total" in record:
        parts.append(f"total={record['total']}")
    click.echo(f"  {' | '.join(parts)}")


# ── Main group ──────────────────────────────────────


@click.group()
@click.version_option(prog_name="zohopy")
@click.option(
    "--org",
    "org_id",
    envvar="ZOHO_ORGANIZATION_ID",
    help="Organization ID (overrides .env)",
)
@click.pass_context
def cli(ctx: click.Context, org_id: str | None) -> None:
    """zohopy — Zoho Books CLI for agents and humans."""
    ctx.ensure_object(dict)
    ctx.obj["org_id"] = org_id


# ── Setup ────────────────────────────────────────────


@cli.command()
def setup() -> None:
    """Interactive OAuth setup wizard."""
    from zohopy.setup import interactive_setup

    interactive_setup()


@cli.command()
@click.option("--json", "as_json", is_flag=True, help="JSON")
def config(as_json: bool) -> None:
    """Show current configuration."""
    try:
        cfg = ZohoConfig()
        data = {
            "data_center": cfg.data_center.value,
            "organization_id": cfg.organization_id,
            "api_domain": cfg.api_domain or cfg.base_api_url,
            "timeout": cfg.timeout,
            "max_retries": cfg.max_retries,
        }
        if as_json:
            click.echo(json_mod.dumps(data, indent=2))
        else:
            for k, v in data.items():
                click.echo(f"  {k}: {v}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option("--json", "as_json", is_flag=True, help="JSON")
def orgs(as_json: bool) -> None:
    """List all organizations."""
    client, books = _get_client()
    try:
        data = books.organizations.list()
        _output(data, as_json)
    finally:
        client.close()


# ── Contacts ─────────────────────────────────────────


@cli.group()
def contacts() -> None:
    """Manage contacts (customers & vendors)."""


@contacts.command("list")
@click.option("--json", "as_json", is_flag=True)
@click.option(
    "--type",
    "contact_type",
    type=click.Choice(["customer", "vendor"]),
)
@click.option("--limit", default=200, type=int)
def contacts_list(
    as_json: bool,
    contact_type: str | None,
    limit: int,
) -> None:
    """List contacts."""
    client, books = _get_client()
    try:
        params: dict[str, Any] = {"per_page": limit}
        if contact_type:
            params["contact_type"] = contact_type
        data = books.contacts.list(**params)
        _output(data, as_json)
    finally:
        client.close()


@contacts.command("get")
@click.argument("contact_id")
@click.option("--json", "as_json", is_flag=True)
def contacts_get(contact_id: str, as_json: bool) -> None:
    """Get a contact by ID."""
    client, books = _get_client()
    try:
        data = books.contacts.get(contact_id)
        _output(data, as_json)
    finally:
        client.close()


@contacts.command("create")
@click.argument("data", type=str)
@click.option("--json", "as_json", is_flag=True)
def contacts_create(data: str, as_json: bool) -> None:
    """Create a contact from JSON string."""
    client, books = _get_client()
    try:
        payload = json_mod.loads(data)
        result = books.contacts.create(payload)
        _output(result, as_json)
    finally:
        client.close()


# ── Items ────────────────────────────────────────────


@cli.group()
def items() -> None:
    """Manage items."""


@items.command("list")
@click.option("--json", "as_json", is_flag=True)
@click.option("--limit", default=200, type=int)
def items_list(as_json: bool, limit: int) -> None:
    """List items."""
    client, books = _get_client()
    try:
        data = books.items.list(per_page=limit)
        _output(data, as_json)
    finally:
        client.close()


@items.command("get")
@click.argument("item_id")
@click.option("--json", "as_json", is_flag=True)
def items_get(item_id: str, as_json: bool) -> None:
    """Get an item by ID."""
    client, books = _get_client()
    try:
        data = books.items.get(item_id)
        _output(data, as_json)
    finally:
        client.close()


@items.command("create")
@click.argument("data", type=str)
@click.option("--json", "as_json", is_flag=True)
def items_create(data: str, as_json: bool) -> None:
    """Create an item from JSON string."""
    client, books = _get_client()
    try:
        result = books.items.create(json_mod.loads(data))
        _output(result, as_json)
    finally:
        client.close()


# ── Invoices ─────────────────────────────────────────


@cli.group()
def invoices() -> None:
    """Manage invoices."""


@invoices.command("list")
@click.option("--json", "as_json", is_flag=True)
@click.option("--status", type=str, help="Filter by status")
@click.option("--limit", default=200, type=int)
def invoices_list(as_json: bool, status: str | None, limit: int) -> None:
    """List invoices."""
    client, books = _get_client()
    try:
        params: dict[str, Any] = {"per_page": limit}
        if status:
            params["status"] = status
        data = books.invoices.list(**params)
        _output(data, as_json)
    finally:
        client.close()


@invoices.command("get")
@click.argument("invoice_id")
@click.option("--json", "as_json", is_flag=True)
def invoices_get(invoice_id: str, as_json: bool) -> None:
    """Get an invoice by ID."""
    client, books = _get_client()
    try:
        data = books.invoices.get(invoice_id)
        _output(data, as_json)
    finally:
        client.close()


@invoices.command("create")
@click.argument("data", type=str)
@click.option("--json", "as_json", is_flag=True)
def invoices_create(data: str, as_json: bool) -> None:
    """Create an invoice from JSON string."""
    client, books = _get_client()
    try:
        result = books.invoices.create(json_mod.loads(data))
        _output(result, as_json)
    finally:
        client.close()


@invoices.command("mark-sent")
@click.argument("invoice_id")
@click.option("--json", "as_json", is_flag=True)
def invoices_mark_sent(invoice_id: str, as_json: bool) -> None:
    """Mark an invoice as sent."""
    client, books = _get_client()
    try:
        data = books.invoices.mark_sent(invoice_id)
        _output(data, as_json)
    finally:
        client.close()


@invoices.command("void")
@click.argument("invoice_id")
@click.option("--json", "as_json", is_flag=True)
def invoices_void(invoice_id: str, as_json: bool) -> None:
    """Void an invoice."""
    client, books = _get_client()
    try:
        data = books.invoices.void(invoice_id)
        _output(data, as_json)
    finally:
        client.close()


# ── Bills ────────────────────────────────────────────


@cli.group()
def bills() -> None:
    """Manage bills."""


@bills.command("list")
@click.option("--json", "as_json", is_flag=True)
@click.option("--limit", default=200, type=int)
def bills_list(as_json: bool, limit: int) -> None:
    """List bills."""
    client, books = _get_client()
    try:
        data = books.bills.list(per_page=limit)
        _output(data, as_json)
    finally:
        client.close()


@bills.command("get")
@click.argument("bill_id")
@click.option("--json", "as_json", is_flag=True)
def bills_get(bill_id: str, as_json: bool) -> None:
    """Get a bill by ID."""
    client, books = _get_client()
    try:
        data = books.bills.get(bill_id)
        _output(data, as_json)
    finally:
        client.close()


@bills.command("create")
@click.argument("data", type=str)
@click.option("--json", "as_json", is_flag=True)
def bills_create(data: str, as_json: bool) -> None:
    """Create a bill from JSON string."""
    client, books = _get_client()
    try:
        result = books.bills.create(json_mod.loads(data))
        _output(result, as_json)
    finally:
        client.close()


@bills.command("void")
@click.argument("bill_id")
@click.option("--json", "as_json", is_flag=True)
def bills_void(bill_id: str, as_json: bool) -> None:
    """Void a bill."""
    client, books = _get_client()
    try:
        data = books.bills.void(bill_id)
        _output(data, as_json)
    finally:
        client.close()


# ── Estimates ────────────────────────────────────────


@cli.group()
def estimates() -> None:
    """Manage estimates."""


@estimates.command("list")
@click.option("--json", "as_json", is_flag=True)
@click.option("--limit", default=200, type=int)
def estimates_list(as_json: bool, limit: int) -> None:
    """List estimates."""
    client, books = _get_client()
    try:
        data = books.estimates.list(per_page=limit)
        _output(data, as_json)
    finally:
        client.close()


@estimates.command("get")
@click.argument("estimate_id")
@click.option("--json", "as_json", is_flag=True)
def estimates_get(estimate_id: str, as_json: bool) -> None:
    """Get an estimate by ID."""
    client, books = _get_client()
    try:
        data = books.estimates.get(estimate_id)
        _output(data, as_json)
    finally:
        client.close()


@estimates.command("create")
@click.argument("data", type=str)
@click.option("--json", "as_json", is_flag=True)
def estimates_create(data: str, as_json: bool) -> None:
    """Create an estimate from JSON string."""
    client, books = _get_client()
    try:
        result = books.estimates.create(json_mod.loads(data))
        _output(result, as_json)
    finally:
        client.close()


# ── Sales Orders ─────────────────────────────────────


@cli.group("sales-orders")
def sales_orders() -> None:
    """Manage sales orders."""


@sales_orders.command("list")
@click.option("--json", "as_json", is_flag=True)
@click.option("--limit", default=200, type=int)
def sales_orders_list(as_json: bool, limit: int) -> None:
    """List sales orders."""
    client, books = _get_client()
    try:
        data = books.sales_orders.list(per_page=limit)
        _output(data, as_json)
    finally:
        client.close()


@sales_orders.command("get")
@click.argument("salesorder_id")
@click.option("--json", "as_json", is_flag=True)
def sales_orders_get(salesorder_id: str, as_json: bool) -> None:
    """Get a sales order by ID."""
    client, books = _get_client()
    try:
        data = books.sales_orders.get(salesorder_id)
        _output(data, as_json)
    finally:
        client.close()


@sales_orders.command("create")
@click.argument("data", type=str)
@click.option("--json", "as_json", is_flag=True)
def sales_orders_create(data: str, as_json: bool) -> None:
    """Create a sales order from JSON string."""
    client, books = _get_client()
    try:
        result = books.sales_orders.create(json_mod.loads(data))
        _output(result, as_json)
    finally:
        client.close()


# ── Purchase Orders ──────────────────────────────────


@cli.group("purchase-orders")
def purchase_orders() -> None:
    """Manage purchase orders."""


@purchase_orders.command("list")
@click.option("--json", "as_json", is_flag=True)
@click.option("--limit", default=200, type=int)
def purchase_orders_list(as_json: bool, limit: int) -> None:
    """List purchase orders."""
    client, books = _get_client()
    try:
        data = books.purchase_orders.list(per_page=limit)
        _output(data, as_json)
    finally:
        client.close()


@purchase_orders.command("get")
@click.argument("purchaseorder_id")
@click.option("--json", "as_json", is_flag=True)
def purchase_orders_get(purchaseorder_id: str, as_json: bool) -> None:
    """Get a purchase order by ID."""
    client, books = _get_client()
    try:
        data = books.purchase_orders.get(purchaseorder_id)
        _output(data, as_json)
    finally:
        client.close()


@purchase_orders.command("create")
@click.argument("data", type=str)
@click.option("--json", "as_json", is_flag=True)
def purchase_orders_create(data: str, as_json: bool) -> None:
    """Create a purchase order from JSON string."""
    client, books = _get_client()
    try:
        result = books.purchase_orders.create(json_mod.loads(data))
        _output(result, as_json)
    finally:
        client.close()


# ── Expenses ─────────────────────────────────────────


@cli.group()
def expenses() -> None:
    """Manage expenses."""


@expenses.command("list")
@click.option("--json", "as_json", is_flag=True)
@click.option("--limit", default=200, type=int)
def expenses_list(as_json: bool, limit: int) -> None:
    """List expenses."""
    client, books = _get_client()
    try:
        data = books.expenses.list(per_page=limit)
        _output(data, as_json)
    finally:
        client.close()


@expenses.command("get")
@click.argument("expense_id")
@click.option("--json", "as_json", is_flag=True)
def expenses_get(expense_id: str, as_json: bool) -> None:
    """Get an expense by ID."""
    client, books = _get_client()
    try:
        data = books.expenses.get(expense_id)
        _output(data, as_json)
    finally:
        client.close()


@expenses.command("create")
@click.argument("data", type=str)
@click.option("--json", "as_json", is_flag=True)
def expenses_create(data: str, as_json: bool) -> None:
    """Create an expense from JSON string."""
    client, books = _get_client()
    try:
        result = books.expenses.create(json_mod.loads(data))
        _output(result, as_json)
    finally:
        client.close()


# ── Payments ─────────────────────────────────────────


@cli.group()
def payments() -> None:
    """Manage payments."""


@payments.command("list-customer")
@click.option("--json", "as_json", is_flag=True)
@click.option("--limit", default=200, type=int)
def payments_list_customer(as_json: bool, limit: int) -> None:
    """List customer payments."""
    client, books = _get_client()
    try:
        data = books.customer_payments.list(per_page=limit)
        _output(data, as_json)
    finally:
        client.close()


@payments.command("list-vendor")
@click.option("--json", "as_json", is_flag=True)
@click.option("--limit", default=200, type=int)
def payments_list_vendor(as_json: bool, limit: int) -> None:
    """List vendor payments."""
    client, books = _get_client()
    try:
        data = books.vendor_payments.list(per_page=limit)
        _output(data, as_json)
    finally:
        client.close()


# ── Taxes ────────────────────────────────────────────


@cli.group()
def taxes() -> None:
    """Manage taxes."""


@taxes.command("list")
@click.option("--json", "as_json", is_flag=True)
def taxes_list(as_json: bool) -> None:
    """List taxes."""
    client, books = _get_client()
    try:
        data = books.taxes.list()
        _output(data, as_json)
    finally:
        client.close()


@taxes.command("create")
@click.argument("data", type=str)
@click.option("--json", "as_json", is_flag=True)
def taxes_create(data: str, as_json: bool) -> None:
    """Create a tax from JSON string."""
    client, books = _get_client()
    try:
        result = books.taxes.create(json_mod.loads(data))
        _output(result, as_json)
    finally:
        client.close()


# ── Settings ─────────────────────────────────────────


@cli.group()
def settings() -> None:
    """Organization settings."""


@settings.command("preferences")
@click.option("--json", "as_json", is_flag=True)
def settings_preferences(as_json: bool) -> None:
    """Get organization preferences."""
    client, books = _get_client()
    try:
        data = books.preferences.get()
        _output(data, as_json)
    finally:
        client.close()


@settings.command("currencies")
@click.option("--json", "as_json", is_flag=True)
def settings_currencies(as_json: bool) -> None:
    """List currencies."""
    client, books = _get_client()
    try:
        data = books.currencies.list()
        _output(data, as_json)
    finally:
        client.close()


@settings.command("templates")
@click.option("--json", "as_json", is_flag=True)
def settings_templates(as_json: bool) -> None:
    """List templates."""
    client, books = _get_client()
    try:
        data = books.templates.list()
        _output(data, as_json)
    finally:
        client.close()


@settings.command("users")
@click.option("--json", "as_json", is_flag=True)
def settings_users(as_json: bool) -> None:
    """List users."""
    client, books = _get_client()
    try:
        data = books.users.list()
        _output(data, as_json)
    finally:
        client.close()


# ── Raw request (escape hatch) ───────────────────────


@cli.command("raw")
@click.argument(
    "method",
    type=click.Choice(["get", "post", "put", "delete"]),
)
@click.argument("path")
@click.option("--data", type=str, help="JSON body")
@click.option("--json", "as_json", is_flag=True)
def raw_request(
    method: str,
    path: str,
    data: str | None,
    as_json: bool,
) -> None:
    """Send a raw API request (escape hatch).

    Example: zohopy raw get /books/v3/contacts --json
    """
    client, _ = _get_client()
    try:
        payload = json_mod.loads(data) if data else None
        if method == "get":
            result = client.get(path)
        elif method == "post":
            result = client.post(path, json=payload)
        elif method == "put":
            result = client.put(path, json=payload)
        else:
            result = client.delete(path)
        _output(result, as_json)
    finally:
        client.close()


if __name__ == "__main__":
    cli()

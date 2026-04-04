# ZohoPy

[![CI](https://github.com/talas9/zohopy/actions/workflows/ci.yml/badge.svg)](https://github.com/talas9/zohopy/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/zohopy)](https://pypi.org/project/zohopy/)
[![Python](https://img.shields.io/pypi/pyversions/zohopy)](https://pypi.org/project/zohopy/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Modern, async-ready Python client for Zoho APIs — **complete Zoho Books v3 coverage**.

## Highlights

- **716 API methods** (358 sync + 358 async) across 57 resource types) across 43 resource types
- **CLI** — `zohopy` command with `--json` on every command
- **Multi-currency** + exchange rates on all transactions
- **Landed cost** support on bills
- **10+ typed exceptions** mapped from Zoho error codes
- **Structured logging** (JSON/console via structlog)
- **Docker ready** — Dockerfile + docker-compose
- **OAuth setup wizard** — `python -m zohopy` or `zohopy setup`

## Install

```bash
pip install zohopy
```

## Quick Start

```bash
# Setup (interactive — generates .env)
zohopy setup

# CLI
zohopy contacts list --json
zohopy invoices create '{"customer_id":"...","line_items":[{"item_id":"...","quantity":1}]}' --json
zohopy raw get /books/v3/items --json
```

```python
# Python SDK
from zohopy import ZohoConfig, SyncZohoClient
from zohopy.products.books import ZohoBooks

with SyncZohoClient(ZohoConfig()) as client:
    books = ZohoBooks(client)
    books.contacts.list()
    books.invoices.create({"customer_id": "...", "line_items": [...]})
    books.invoices.mark_sent("invoice_id")
```

## Products

| Product | Status | Coverage |
|---------|--------|----------|
| **Zoho Books** | ✅ v3 | 57 resources, 358 methods |
| Zoho Inventory | 🔜 Coming soon | — |
| Zoho CRM | 🔜 Coming soon | — |
| Zoho Payroll | 🔜 Planned | — |
| Zoho People | 🔜 Planned | — |

## Documentation

| Document | Description |
|----------|-------------|
| **[AGENT.md](AGENT.md)** | Agent/LLM reference — CLI commands, SDK quick ref, error codes |
| **[docs/api.md](docs/api.md)** | Full API reference — all 43 resources and their methods |
| **[docs/errors.md](docs/errors.md)** | Error handling guide — exception hierarchy + Zoho error codes |
| **[docs/setup.md](docs/setup.md)** | Setup guide — OAuth flows, .env, Docker, programmatic config |
| **[CHANGELOG.md](CHANGELOG.md)** | Release history |

## Contributing

```bash
git clone https://github.com/talas9/zohopy.git && cd zohopy
pip install -e ".[dev]"
pytest && ruff check src/ && mypy src/
```

Branch strategy: `dev` → PR → `main`. Tags trigger PyPI release.

## License

[MIT](LICENSE)

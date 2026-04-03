"""Structured logging for ZohoPy using structlog.

Provides structured, JSON-capable logging for both development
and production (Docker) environments. The log format adapts
automatically based on the ``ZOHOPY_LOG_FORMAT`` env var.

Usage::

    from zohopy.logging import configure_logging, get_logger

    configure_logging()  # call once at startup
    logger = get_logger()
    logger.info("invoice.created", invoice_id="INV-001")

Environment variables:
    ZOHOPY_LOG_LEVEL: DEBUG, INFO, WARNING, ERROR (default: INFO)
    ZOHOPY_LOG_FORMAT: json, console (default: console)
"""

from __future__ import annotations

import logging
import os
from typing import Any

import structlog


def configure_logging(
    *,
    level: str | None = None,
    log_format: str | None = None,
    **kwargs: Any,
) -> None:
    """Configure structured logging for the library.

    Args:
        level: Log level (DEBUG/INFO/WARNING/ERROR). Defaults to
            env ``ZOHOPY_LOG_LEVEL`` or ``INFO``.
        log_format: Output format — ``"json"`` for production/Docker,
            ``"console"`` for development. Defaults to env
            ``ZOHOPY_LOG_FORMAT`` or ``"console"``.
    """
    level = (level or os.environ.get("ZOHOPY_LOG_LEVEL", "INFO")).upper()
    log_format = (log_format or os.environ.get("ZOHOPY_LOG_FORMAT", "console")).lower()

    shared_processors: list[structlog.types.Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.UnicodeDecoder(),
    ]

    if log_format == "json":
        renderer: structlog.types.Processor = structlog.processors.JSONRenderer()
    else:
        renderer = structlog.dev.ConsoleRenderer()

    structlog.configure(
        processors=[
            *shared_processors,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    formatter = structlog.stdlib.ProcessorFormatter(
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            renderer,
        ],
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    root_logger = logging.getLogger("zohopy")
    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    root_logger.setLevel(getattr(logging, level, logging.INFO))


def get_logger(name: str = "zohopy") -> structlog.stdlib.BoundLogger:
    """Get a structured logger instance.

    Args:
        name: Logger name, usually the module name.

    Returns:
        A structlog bound logger.
    """
    return structlog.get_logger(name)  # type: ignore[no-any-return]

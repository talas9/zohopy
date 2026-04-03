# ZohoPy Docker image
#
# Build: docker build -t zohopy .
# Run:   docker run --env-file .env zohopy contacts list --json
#
# NOTE: Build the wheel first with `python -m build` or let CI do it.
# If no pre-built wheel, we use SETUPTOOLS_SCM_PRETEND_VERSION.

FROM python:3.13-slim

LABEL org.opencontainers.image.source="https://github.com/talas9/zohopy"
LABEL org.opencontainers.image.description="ZohoPy — Python client for Zoho APIs"
LABEL org.opencontainers.image.licenses="MIT"

WORKDIR /app

# Copy source and install
COPY pyproject.toml README.md LICENSE ./
COPY src/ src/

# Install — use pretend version since .git is not available
ENV SETUPTOOLS_SCM_PRETEND_VERSION=0.1.0
RUN pip install --no-cache-dir . && rm -rf /app/src /app/pyproject.toml

# Non-root user
RUN useradd --create-home --shell /bin/bash zohopy
USER zohopy

# Runtime config
ENV ZOHOPY_LOG_LEVEL=INFO \
    ZOHOPY_LOG_FORMAT=json \
    PYTHONUNBUFFERED=1

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD python -c "from zohopy import ZohoConfig; print('ok')" || exit 1

ENTRYPOINT ["zohopy"]

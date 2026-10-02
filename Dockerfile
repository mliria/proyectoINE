# syntax=docker/dockerfile:1
# ---------------------------------------------------------------------------
# Production image for the INE Flask application.
# Portable across Render / Railway / Fly.io (no provider-specific tooling).
# ---------------------------------------------------------------------------
FROM python:3.12-slim

# - PYTHONDONTWRITEBYTECODE: keep the image clean (no .pyc files)
# - PYTHONUNBUFFERED: stream logs immediately to the platform
# - PORT: fallback port; PaaS platforms inject their own PORT at runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

WORKDIR /app

# Install dependencies first so this layer is cached when only app code changes.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application module and its templates (templates must sit beside the
# module so Flask's default loader can find them).
COPY inicioINE.py .
COPY templates/ ./templates/

# Create an unprivileged user and give it ownership of the app directory.
RUN useradd --create-home --uid 1000 appuser \
    && chown -R appuser:appuser /app
USER appuser

# Documentation-only: the real port is provided by $PORT at runtime.
EXPOSE 8000

# Production WSGI server bound to the platform-provided $PORT.
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT} --workers 2 --threads 4 --timeout 60 inicioINE:app"]

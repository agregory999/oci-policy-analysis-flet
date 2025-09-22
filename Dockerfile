# Multi-arch base image
FROM python:3.11-slim AS base

# Install system deps (minimal)
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV PYTHONUNBUFFERED=1

# --- Dependency layer (cached if requirements.txt unchanged)
COPY requirements.txt .
RUN pip install --no-cache-dir --no-warn-script-location --disable-pip-version-check -r requirements.txt

# --- Application layer
COPY app ./app
COPY docs ./docs
COPY pyproject.toml README.md LICENSE ./

# Expose port
ENV APP_PORT=8080
EXPOSE 8080

CMD ["python", "app/main.py"]

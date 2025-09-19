# Use official multi-arch Python slim image
FROM python:3.11-slim

# Install system deps (e.g., git for runtime pull if needed)
RUN apt-get update && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Install Python deps separately (cacheable)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code (fast-changing layer)
COPY . .

# Expose app port (use ENV so it's configurable)
ENV APP_PORT=8080
EXPOSE 8080

# Start app
CMD ["python", "app/main.py"]

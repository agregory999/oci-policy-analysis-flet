# Use official multi-arch Python slim image
FROM python:3.11-slim

# Install system deps (e.g., git for runtime pull if needed)
RUN apt-get update && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install dependencies first
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only app folder
COPY app ./app
COPY docs ./docs
COPY pyproject.toml .
COPY README.md .
COPY LICENSE .

# Expose port
ENV APP_PORT=8080
EXPOSE 8080

# Start the app
CMD ["python", "app/main.py"]

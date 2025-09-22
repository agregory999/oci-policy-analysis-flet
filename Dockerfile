# Base image (multi-arch, works on ARM A1)
FROM python:3.11-slim-bullseye

# Force unbuffered logs so you see output immediately
ENV PYTHONUNBUFFERED=1 \
    APP_PORT=8080

WORKDIR /app

# Install uv (fast dependency installer)
RUN pip install --no-cache-dir uv

# Copy dependencies definition first (cache-friendly)
COPY requirements.txt .

# Install dependencies using uv (much faster than pip)
RUN uv pip install --system -r requirements.txt

# If you want to use pip instead, comment the uv line above and uncomment this:
# RUN pip install --no-cache-dir --no-warn-script-location --disable-pip-version-check -r requirements.txt

# Copy application source
COPY app ./app
COPY pyproject.toml README.md LICENSE ./

# Expose app port
EXPOSE 8080

# Start Flet app
CMD ["python", "app/main.py"]

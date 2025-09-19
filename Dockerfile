FROM python:3.11-slim

# Install system deps
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Create working directory
WORKDIR /app

# Copy requirements first (for Docker caching)
COPY requirements.txt .

# Install Python deps
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Expose app port (match what you set in main.py)
EXPOSE 8080

# Start the app
CMD ["python", "app/main.py"]

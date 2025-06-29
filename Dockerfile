FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements/development.txt .

RUN pip install --no-cache-dir -r development.txt

# Copy application code
COPY . .

# Make entrypoint executable
RUN chmod +x entrypoint.sh

# Expose port (will be overridden by PORT env var)
EXPOSE ${PORT:-8000}

ENTRYPOINT ["./entrypoint.sh"] 
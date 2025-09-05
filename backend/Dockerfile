# Use slim Python base (lightweight but stable)
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies required by chromadb/llama-index
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt

# Copy project code
COPY . .

# Expose Railway port
ENV PORT=8000

# Start app (Railway injects PORT env automatically)
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${PORT}"]

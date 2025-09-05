# Base image
FROM python:3.12-slim

# Set workdir
WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y \
    build-essential \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for caching)
COPY requirements.txt .

# Install Python deps
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source
COPY . .

# Expose Railway port
EXPOSE 8000

# Default start command
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

# Use Python 3.12 slim image as base
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies required for pymssql
RUN apt-get update && apt-get install -y \
    freetds-dev \
    freetds-bin \
    unixodbc-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Make entrypoint script executable
RUN chmod +x docker-entrypoint.sh

# Expose port
EXPOSE 8000

# Set environment variables (can be overridden in docker-compose)
ENV HOST=0.0.0.0
ENV PORT=8000

# Use entrypoint script
ENTRYPOINT ["./docker-entrypoint.sh"]
# Use Python 3.12 slim image based on Debian 12 (bookworm)
# This Dockerfile supports both amd64 and arm64 architectures
FROM python:3.12-slim-bookworm

# Set working directory
WORKDIR /app

# Install system dependencies required for pyodbc and Microsoft ODBC Driver
# ODBC Driver 18 supports both amd64 and arm64 on Debian 12
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gnupg \
    ca-certificates \
    apt-transport-https \
    unixodbc \
    unixodbc-dev \
    gcc \
    g++ \
    lsb-release \
    libgssapi-krb5-2 \
    && curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg \
    && echo "deb [signed-by=/usr/share/keyrings/microsoft-prod.gpg] https://packages.microsoft.com/debian/12/prod bookworm main" > /etc/apt/sources.list.d/microsoft-prod.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y --no-install-recommends msodbcsql18 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install argon2_cffi

# Copy application code
COPY . .

# Ensure entrypoint script has proper line endings (LF) and is executable
# This is important for cross-platform compatibility (Windows/Linux/Mac)
RUN sed -i 's/\r$//' docker-entrypoint.sh && \
    chmod +x docker-entrypoint.sh

# Expose port
EXPOSE 8000

# Set environment variables (can be overridden in docker compose)
ENV HOST=0.0.0.0
ENV PORT=8000

# Use entrypoint script
ENTRYPOINT ["./docker-entrypoint.sh"]
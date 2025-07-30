# Use Python 3.13 slim image as base
FROM python:3.13-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .
# Copy scripts directory
COPY scripts/ /app/scripts/
# Copy data file
COPY eurofxref-hist.csv /data/eurofxref-hist.csv

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create data directory for DuckDB files
RUN mkdir -p /app/data

# Copy entrypoint script
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Create a non-root user for security
RUN useradd --create-home --shell /bin/bash appuser && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port for any web interface (if needed)
EXPOSE 8080

# Set default command to run entrypoint script
CMD ["/app/entrypoint.sh"]

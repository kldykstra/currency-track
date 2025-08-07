# Use Python 3.13-alpine image for minimal footprint
FROM python:3.13-alpine

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies
RUN apk update && apk add --no-cache \
    build-base \
    postgresql-dev \
    && rm -rf /var/cache/apk/*

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/* .

# Create non-root user
RUN adduser -D -h /home/appuser appuser && \
    chown -R appuser:appuser /app
USER appuser

# Default command
CMD ["python", "app.py"] 
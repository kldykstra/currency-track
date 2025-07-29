#!/bin/bash

echo "Starting DuckDB container..."

# Test DuckDB import
python -c "import duckdb; print('✓ DuckDB imported successfully')"

# Create data directory if it doesn't exist
mkdir -p /app/data

echo "✓ DuckDB instance is ready"
echo "✓ Data directory: /app/data"
echo "✓ Container will stay running for 1 hour"

# Keep container running for 1 hour (3600 seconds)
sleep 3600 
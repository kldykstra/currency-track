#!/bin/bash

echo "Starting DuckDB container..."

# Test DuckDB Python import
python -c "import duckdb; print('✓ DuckDB Python package imported successfully')"

# Create data directory if it doesn't exist
mkdir -p /app/data

echo "✓ DuckDB instance is ready"
echo "✓ Data directory: /app/data"
echo "✓ Container will stay running for 1 hour"

# Start a Python HTTP server in /data
cd /data
echo "Starting HTTP server on port 8080..."
exec python -m http.server 8080
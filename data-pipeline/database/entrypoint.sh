#!/bin/bash

echo "Starting DuckDB container..."

# Test DuckDB Python import
python -c "import duckdb; print('✓ DuckDB Python package imported successfully')"

# Create data directory if it doesn't exist
mkdir -p /app/data

echo "✓ DuckDB instance is ready"
echo "✓ Data directory: /app/data"
echo "✓ Container will stay running for 1 hour"

# Create tables
duckdb /app/data/currency_tracker.db < /app/scripts/create_tables.sql
echo "✓ Tables created successfully"

# Keep container running for 1 hour (3600 seconds)
sleep 3600 
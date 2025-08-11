#!/bin/bash

# Development script for currency-track dashboard with hot-reloading

echo "Starting currency-track development environment with hot-reloading..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo ".env file not found. Please create one with your database credentials."
    exit 1
fi

# Stop any existing containers
echo "Stopping existing containers..."
docker-compose -f compose.yaml down 2>/dev/null || true

# Start development environment
echo "Starting development environment..."
docker-compose -f compose.dev.yaml up --build

echo "Development environment started!"
echo "Dashboard available at: http://localhost:8050"
echo "Hot-reloading is enabled - changes to your code will automatically reload!"
echo ""
echo "To stop the environment, run: docker-compose -f compose.dev.yaml down"
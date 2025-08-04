#!/bin/bash

# Read environment variables
source .env

# Generate the datasource config with actual values
cat > dashboard/provisioning/datasources/postgres.yml << EOF
apiVersion: 1

datasources:
  - name: grafana-postgresql-datasource
    type: postgres
    url: currency-track-database:5432
    database: currency_tracker
    user: postgres
    secureJsonData:
      password: $POSTGRES_PASSWORD
    jsonData:
      sslmode: disable
EOF 
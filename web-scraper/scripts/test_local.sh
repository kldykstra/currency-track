#!/bin/bash
set -e

# List s3 buckets and fetch currencytrack-development bucket name
export S3_BUCKET=$(aws s3 ls | grep currencytrack-development | awk '{print $3}')
export S3_KEY_PREFIX="ecb-exchange-rates/"

PROJECT_ROOT=$(dirname $(dirname $(realpath $0)))

# Activate the uv virtual environment
if [ -d "$PROJECT_ROOT/.venv" ]; then
  source $PROJECT_ROOT/.venv/bin/activate
else
  echo "Virtual environment $PROJECT_ROOT/.venv not found. Please create it with 'uv venv .venv' first."
  exit 1
fi

echo "Running lambda_handler in $PROJECT_ROOT"

# Run the lambda_handler function in main.py with dummy event/context
# output the results to a log file
PYTHONPATH="$PROJECT_ROOT" python -c '
import lambda_function
lambda_function.lambda_handler({}, None)
' > $PROJECT_ROOT/test_local.log 2>&1
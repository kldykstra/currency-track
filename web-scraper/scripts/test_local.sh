#!/bin/bash
set -e

# Activate the uv virtual environment
if [ -d "$PROJECT_ROOT/.venv" ]; then
  source $PROJECT_ROOT/.venv/bin/activate
else
  echo "Virtual environment $PROJECT_ROOT/.venv not found. Please create it with 'uv venv .venv' first."
  exit 1
fi

# Run the lambda_handler function in main.py with dummy event/context
# output the results to a log file
PYTHONPATH="$PROJECT_ROOT" python -c '
import main
main.lambda_handler({}, None)
' > $PROJECT_ROOT/test_local.log 2>&1
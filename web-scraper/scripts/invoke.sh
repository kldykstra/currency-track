#!/bin/bash
set -e

# Usage: ./invoke.sh <function-name> [payload-json-file]

if [ -z "$1" ]; then
  echo "Usage: $0 <function-name> [payload-json-file]"
  exit 1
fi

FUNCTION_NAME="$1"

aws lambda invoke \
    --function-name "$FUNCTION_NAME" \
    response.json

echo "Lambda response:"
cat response.json
rm response.json 
#! /bin/bash

# ------------------------------- Shell Setup -------------------------------

# set the project root to one directory up
export PROJECT_ROOT=$(dirname $(dirname $(realpath $0)))

# ------------------------------- Python Setup -------------------------------

pyenv install 3.13.5
pyenv local 3.13.5

# Create a virtual environment
uv venv $PROJECT_ROOT/.venv

# Activate the virtual environment
source $PROJECT_ROOT/.venv/bin/activate

# Install dependencies
uv pip install -r $PROJECT_ROOT/requirements.txt

# ------------------------------- AWS Setup -------------------------------
export AWS_REGION=eu-north-1

# Set the AWS profile
export AWS_PROFILE=currencytrack-developer-400144345451

# List s3 buckets and fetch currencytrack-development bucket name
S3_BUCKET=$(aws s3 ls | grep currencytrack-development | awk '{print $3}')

# If the bucket doesn't exist, create it
if [ -z "$S3_BUCKET" ]; then
    s3uuiddev=$(uuidgen | tr -d - | tr '[:upper:]' '[:lower:]')
    S3_BUCKET="currencytrack-development-$s3uuiddev"
    aws s3api create-bucket \
        --bucket $S3_BUCKET \
        --region $AWS_REGION \
        --create-bucket-configuration LocationConstraint=$AWS_REGION
fi

# export bucket name and prefix
export S3_BUCKET
export S3_KEY_PREFIX="ecb-exchange-rates/"
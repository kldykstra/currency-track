# !/bin/bash

LAMBDA_FUNCTION_NAME="currencyTrackScraperProd"
S3_PREFIX="ecb-exchange-rates/"

# ------------------------------- Shell Setup -------------------------------

# set the project root to one directory up
export PROJECT_ROOT=$(dirname $(dirname $(realpath $0)))

# ------------------------------- AWS Setup -------------------------------

# List s3 buckets and fetch currencytrack-production bucket name
S3_BUCKET=$(aws s3 ls | grep currencytrack-production | awk '{print $3}')

# If the bucket doesn't exist, create it
if [ -z "$S3_BUCKET" ]; then
    s3uuiddev=$(uuidgen | tr -d - | tr '[:upper:]' '[:lower:]')
    S3_BUCKET="currencytrack-production-$s3uuiddev"
    aws s3api create-bucket \
        --bucket $S3_BUCKET \
        --region $AWS_REGION \
        --create-bucket-configuration LocationConstraint=$AWS_REGION
fi

# ------------------------------- Bundle and Deploy -------------------------

# remove the zip file if it exists
rm $PROJECT_ROOT/lambda.zip

# create a zip file of the lambda function and dependencies
cd $PROJECT_ROOT
zip $PROJECT_ROOT/lambda.zip lambda_function.py

# add python dependencies to the zip file without copying file structure
cd $PROJECT_ROOT/.venv/lib/python3.13/site-packages/
zip -r $PROJECT_ROOT/lambda.zip .

# deploy the lambda function to an existing function
aws lambda update-function-code \
    --function-name $LAMBDA_FUNCTION_NAME \
    --zip-file fileb://$PROJECT_ROOT/lambda.zip \
    --region $AWS_REGION

# wait for the lambda function to be updated
aws lambda wait function-updated --function-name $LAMBDA_FUNCTION_NAME --region $AWS_REGION

# update the lambda function configuration
aws lambda update-function-configuration \
    --function-name $LAMBDA_FUNCTION_NAME \
    --region $AWS_REGION \
    --timeout 300 \
    --memory-size 1024 \
    --environment "Variables={S3_BUCKET=$S3_BUCKET,S3_KEY_PREFIX=$S3_PREFIX}"

# ------------------------------- Clean Up ----------------------------------

# delete the zip file
rm $PROJECT_ROOT/lambda.zip
#! /bin/bash

# login to aws if not already logged in
if ! aws sts get-caller-identity > /dev/null 2>&1; then
    aws sso login --profile $AWS_PROFILE
fi
#!/usr/bin/env bash

# Verify that there is a config file
# Make sure it is valid json
# Parse requirements file
# make a zip of all to temp director
dst="$TMPDIR/lambda.zip"
zip -r dst lambda_function.py config.json env/lib/python2.7/site-packages/requests/ env/lib/python2.7/site-packages/requests-2.9.1.dist-info/
aws lambda update-function-code --function-name $LAMBDA_FN_NAME  --zip-file fileb://$TMPDIR/lambda.zip
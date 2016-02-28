#!/usr/bin/env bash

set -euo pipefail
set -x

dst_zip="lambda-$(date +%s).zip"
dst="$TMPDIR$dst_zip"
temp="temp-$(date +%s)"
temp_dir="$TMPDIR$temp"

create_zip() {
    mkdir "$temp_dir"

    # TODO Make a distribution requirements file for production use
    # https://github.com/helveticafire/lambda-s3-imgix-purger/issues/9

    cp -r env/lib/python2.7/site-packages/requests/ "$temp_dir/requests/"
    cp -r env/lib/python2.7/site-packages/requests-2.9.1.dist-info/ "$temp_dir/requests-2.9.1.dist-info/"

    # TODO Verify that there is a config file
    # https://github.com/helveticafire/lambda-s3-imgix-purger/issues/7
    # TODO Ensure config file is valid json
    # https://github.com/helveticafire/lambda-s3-imgix-purger/issues/8

    cp {lambda_function.py,config.json} "$temp_dir/."

    pushd "$temp_dir"

    zip -r "$dst" *

    popd
    echo "Created uploadable zip at: $dst"
}

check_fn_name() {
    echo "$LAMBDA_FN_NAME" > /dev/null
}

check_role_arn() {
    echo "$LAMBDA_ROLE_ARN" > /dev/null
}

update() {
    check_fn_name
    create_zip
    aws lambda update-function-code --function-name "$LAMBDA_FN_NAME" --zip-file fileb://"$dst" --publish
}

create() {
    check_fn_name
    check_role_arn
    create_zip

    # TODO Make create-function more configurable using --cli-input-json
    # https://github.com/helveticafire/lambda-s3-imgix-purger/issues/12

    aws lambda create-function --function-name "$LAMBDA_FN_NAME" \
                               --runtime "python2.7" \
                               --role "$LAMBDA_ROLE_ARN" \
                               --handler "lambda_function.lambda_handler" \
                               --description "An Amazon S3 trigger that purges Imgix for the object that has been updated." \
                               --memory-size 128 \
                               --timeout 3 \
                               --zip-file fileb://"$dst" \
                               --publish
}

# call arguments verbatim:
"$@"

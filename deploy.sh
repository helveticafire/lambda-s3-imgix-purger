#!/usr/bin/env bash

set -euo pipefail
set -x

dst_zip="lambda-$(date +%s).zip"
dst="$TMPDIR$dst_zip"
temp="temp-$(date +%s)"
temp_dir="$TMPDIR$temp"

check_config_exists() {
    if [ -f config.json ]; then
        echo "config.json exists"
        return 1
    else
        echo "NO config.json"
        return 0
    fi
}

check_config_is_valid() {
    if [ $(python check_conf.py "config.json") = 1 ]; then
        echo "config.json is valid"
        return 1
    else
        echo "config.json ***NOT*** valid"
        return 0
    fi
}

check_config() {
    if check_config_exists || check_config_is_valid; then
        return 0
    else
        return 1
    fi
}

create_zip() {
    if check_config; then
        echo "problem with config.json"
        exit 1
    fi
    mkdir "$temp_dir"

    # TODO Make a distribution requirements file for production use
    # https://github.com/helveticafire/lambda-s3-imgix-purger/issues/9

    cp -r env/lib/python2.7/site-packages/requests/ "$temp_dir/requests/"
    cp -r env/lib/python2.7/site-packages/requests-2.9.1.dist-info/ "$temp_dir/requests-2.9.1.dist-info/"

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

check_fn_exists() {
    b=$(aws lambda list-functions | jq -e '.Functions[].FunctionName')
    if [ "$b" == "\"$LAMBDA_FN_NAME\"" ]; then
        echo "--- Function exists"
        return 1
    else
        echo "--- No Function exists"
        return 0
    fi
}

run() {
    if check_fn_exists; then
        echo "No Function exists"
        echo "Creating function"
        create
    else
        echo "Function exists"
        echo "Updating function"
        update
    fi
}

# call arguments verbatim:
"$@"

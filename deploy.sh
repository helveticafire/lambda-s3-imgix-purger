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

update() {
    check_fn_name
    create_zip
    aws lambda update-function-code --function-name "$LAMBDA_FN_NAME" --zip-file fileb://"$dst" --publish
}

# call arguments verbatim:
"$@"

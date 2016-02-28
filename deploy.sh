#!/usr/bin/env bash

set -euo pipefail
set -x

# TODO Verify that there is a config file
# https://github.com/helveticafire/lambda-s3-imgix-purger/issues/7
# TODO Ensure config file is valid json
# https://github.com/helveticafire/lambda-s3-imgix-purger/issues/8
# TODO Make a distribution requirements file for production use
# https://github.com/helveticafire/lambda-s3-imgix-purger/issues/9

dst_zip="lambda-$(date +%s).zip"
dst="$TMPDIR$dst_zip"

cp -r env/lib/python2.7/site-packages/requests/ requests/
cp -r env/lib/python2.7/site-packages/requests-2.9.1.dist-info/ requests-2.9.1.dist-info/

zip -r "$dst" lambda_function.py config.json requests requests-2.9.1.dist-info

rm -rf requests/
rm -rf requests-2.9.1.dist-info/

aws lambda update-function-code --function-name "$LAMBDA_FN_NAME"  --zip-file fileb://"$dst" --publish

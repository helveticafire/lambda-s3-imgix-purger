#!/usr/bin/env bash

set -euo pipefail
set -x

# TODO Verify that there is a config file
# TODO Make sure it is valid json
# TODO Parse requirements file

dst_zip="lambda-$(date +%s).zip"
dst="$TMPDIR$dst_zip"

zip -r "$dst" lambda_function.py config.json env/lib/python2.7/site-packages/requests/ env/lib/python2.7/site-packages/requests-2.9.1.dist-info/

aws lambda update-function-code --function-name "$LAMBDA_FN_NAME"  --zip-file fileb://"$dst"

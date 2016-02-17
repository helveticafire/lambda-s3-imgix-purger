#!/usr/bin/env bash

set -euo pipefail
set -x

# TODO Verify that there is a config file
# TODO Make sure it is valid json
# TODO Parse requirements file

dst_zip="lambda-$(date +%s).zip"
dst="$TMPDIR$dst_zip"

cp -r env/lib/python2.7/site-packages/requests/ requests/
cp -r env/lib/python2.7/site-packages/requests-2.9.1.dist-info/ requests-2.9.1.dist-info/

zip -r "$dst" lambda_function.py config.json requests requests-2.9.1.dist-info

rm -rf requests/
rm -rf requests-2.9.1.dist-info/

aws lambda update-function-code --function-name "$LAMBDA_FN_NAME"  --zip-file fileb://"$dst" --publish

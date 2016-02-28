#!/usr/bin/env bash

set -euo pipefail
set -x

# Uses the AWS CLI and jq to create an IAM role for _

check_role_name() {
    echo "$LAMBDA_ROLE_NAME" > /dev/null
}

check_policy_name() {
    echo "$LAMBDA_POLICY_NAME" > /dev/null
}

check_role_name
check_policy_name

# Create the role
aws iam create-role --role-name "$LAMBDA_ROLE_NAME" --assume-role-policy-document file://lambda_iam_role.json

# Create the policy
policy_arn=$(aws iam create-policy --policy-name "$LAMBDA_POLICY_NAME" --policy-document file://lambda_iam_policy.json | jq -r '.Policy.Arn')

# Attach the role to the policy
aws iam attach-role-policy --role-name "$LAMBDA_ROLE_NAME" --policy-arn "$policy_arn"

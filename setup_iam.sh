#!/usr/bin/env bash

set -euo pipefail
set -x

# Uses the AWS CLI and jq to create an IAM role for _

role_name="lambda_imgix_purge"
policy_name="lambda_imgix_purge_policy"

# Create the role
aws iam create-role --role-name $role_name --assume-role-policy-document file://lambda_iam_role.json

# Create the policy
policy_arn=$(aws iam create-policy --policy-name $policy_name --policy-document file://lambda_iam_policy.json | jq -r '.Policy.Arn')

# Attach the role to the policy
aws iam attach-role-policy --role-name $role_name --policy-arn "$policy_arn"

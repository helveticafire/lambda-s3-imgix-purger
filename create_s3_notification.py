#!/usr/bin/env python

import json
import boto3
import sys
import os
import uuid


def create_s3_notification(bucket, lambda_function_arn):
    print('Creating bucket-notification-configuration.json')
    with open('bucket-notification-configuration.template.json') as template_file:
        try:
            template = json.load(template_file)
        except (ValueError, AttributeError, TypeError) as err:
            # print('Config was not valid, error: {}, {}'.format(err, config_file.read()))
            return {}
    template['Bucket'] = bucket
    template['NotificationConfiguration']['LambdaFunctionConfigurations'][0]['Id'] = str(uuid.uuid4())
    template['NotificationConfiguration']['LambdaFunctionConfigurations'][0]['LambdaFunctionArn'] = lambda_function_arn
    with open('bucket-notification-configuration.json', 'w') as f_conf:
        json.dump(template, f_conf, indent=4, sort_keys=True)


if __name__ == '__main__':
    create_s3_notification(os.environ['TARGET_BUCKET'],
                           'arn:aws:lambda:eu-west-1:292109689229:function:imgix-purge')


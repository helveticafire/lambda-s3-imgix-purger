from __future__ import print_function

import json
import urllib
import requests

print('Loading function')


def lambda_handler(event, context):
    # print("Received event: " + json.dumps(event, indent=2))

    print('Handler started!')
    # TODO: Validate s3 notification event
    # https://github.com/helveticafire/lambda-s3-imgix-purger/issues/1
    key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key']).decode('utf8')
    # TODO: Handle keys that end in / forward lash indicating director not a file
    # https://github.com/helveticafire/lambda-s3-imgix-purger/issues/2
    purge_endpoint = 'https://api.imgix.com/v2/image/purger'
    results = {}
    with open('config.json') as config_file:
        config = json.load(config_file)
        domains = config['domains']
        for domain, v in domains.iteritems():
            for scheme in v['schemes']:
                to_purge = scheme + '://' + domain + '/' + key
                print('Going to purge: ' + to_purge)
                req = requests.post(purge_endpoint, auth=(config['api_key'], ''), data={'url': to_purge})
                print(to_purge + ' response status code: ' + str(req.status_code))
                results[to_purge] = req.status_code
    return results

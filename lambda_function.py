from __future__ import print_function

import json
import urllib
import requests
import os.path

print('Loading function')


def lambda_handler(event, context):
    # print("Received event: " + json.dumps(event, indent=2))

    print('Handler started!')
    event_type = type(event)
    if event_type is not dict:
        print('Event was not a dict, it was {}'.format(event_type))
        return {}

    try:
        key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key']).decode('utf8')
    except KeyError as err:
        print('Event dict was not valid, error: {}'.format(err))
        return {}
    except IndexError as err:
        print('Event dict was not valid, error: {}'.format(err))
        return {}
    except TypeError as err:
        print('Event dict was not valid, error: {}'.format(err))
        return {}
    if key == '':
        print('Event dict was not valid, key not set')
        return {}
    if key.endswith('/'):
        print('Key cannot be a directory')
        return {}

    purge_endpoint = 'https://api.imgix.com/v2/image/purger'
    results = {}
    config_file_name = 'config.json'
    if not os.path.isfile(config_file_name):
        print('There is no config file')
        return {}

    with open(config_file_name) as config_file:
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

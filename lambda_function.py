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
    except (KeyError, IndexError, TypeError)as err:
        print('Event dict was not valid, error: {}'.format(err))
        return {}

    if key == '':
        print('Event dict was not valid, key not set')
        return {}
    if key.endswith('/'):
        print('Key cannot be a directory')
        return {}

    config_file_name = 'config.json'
    if not os.path.isfile(config_file_name):
        print('There is no config file')
        return {}

    purge_endpoint = 'https://api.imgix.com/v2/image/purger'
    results = {}
    with open(config_file_name) as config_file:
        try:
            config = json.load(config_file)
        except (ValueError, AttributeError, TypeError) as err:
            print('Config was not valid, error: {}, {}'.format(err, config_file.read()))
            return {}

        try:
            domains = config['domains']
            api_key = config['api_key']
        except (KeyError, TypeError) as err:
            print('Config was not valid, error: {}, {}'.format(err, config))
            return {}

        type_domains = type(domains)
        if type_domains is not dict:
            print('Domains was not a dict, it was {}'.format(type_domains))
            return {}
        if len(domains) < 1:
            print('Domains has no items')
            return {}

        type_api_key = type(api_key)
        if type_api_key is not unicode:
            print('api_key was not a unicode, it was {}'.format(type_api_key))
            return {}
        if len(api_key) <= 1:
            print('api_key needs to have a value')
            return {}

        allow_schemes = ['http', 'https']
        for k, v in domains.iteritems():
            if len(k) < 1:
                print('Config was not valid - schemes has no items')
                return {}
            if '/' in k:
                print('Config was not valid - Domains cannot contain forward lash')
                return {}
            if not k.endswith('.imgix.net'):
                # see https://docs.imgix.com/setup/serving-images
                print('Config was not valid - Domains must end with .imgix.net was {}'.format(k))
                return {}

            type_v = type(v)
            if type_v is not dict:
                print('{} must be a dict value, it was {}'.format(v, type_v))
                return {}

            try:
                schemes = v['schemes']
            except (KeyError, TypeError) as err:
                print('Config was not valid - schemes, error: {}, {}'.format(err, config))
                return {}

            type_schemes = type(schemes)
            if type_schemes is not list:
                print('{} must be a list, it was {}'.format(v, type_schemes))
                return {}

            for scheme in schemes:
                if scheme not in allow_schemes:
                    print('Config was not valid - schemes only allow http; https: value was {}'.format(scheme))
                    return {}
                to_purge = scheme + '://' + k + '/' + key
                print('Going to purge: ' + to_purge)
                resp = requests.post(purge_endpoint, auth=(api_key, ''), data={'url': to_purge})
                print(to_purge + ' response status code: ' + str(resp.status_code))
                results[to_purge] = resp.status_code
    print('Handler finished!')
    return results

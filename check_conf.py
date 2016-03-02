from jsonschema import validate, ValidationError
import os.path
import json
import sys


def validate_config(config_file_name):
    # print("validating config file {}".format(config_file_name))
    if not os.path.isfile(config_file_name):
        # print('There is no config file')
        return False

    schema = {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "id": "http://jsonschema.net",
        "type": "object",
        "properties": {
            "api_key": {
                "id": "http://jsonschema.net/api_key",
                "type": "string",
                "pattern": "^\w+$"
            },
            "domains": {
                "id": "http://jsonschema.net/domains",
                "type": "object",
                "patternProperties": {
                    "^\\w+.imgix.net$": {
                        "id": "http://jsonschema.net/domains/^\\w.imgix.net+$",
                        "type": "object",
                        "properties": {
                            "schemes": {
                                "id": "http://jsonschema.net/domains/^[\\w.]+$/schemes",
                                "type": "array",
                                "items": {"type": "string",
                                          "pattern": "^https?$"},
                                "minItems": 1,
                                "maxItems": 2,
                            }
                        },
                        "required": ["schemes"]
                    }
                },
                "additionalProperties": False,
                "minProperties": 1
            }
        },
        "required": ["api_key", "domains"]
    }
    with open(config_file_name) as config_file:
        try:
            config = json.load(config_file)
        except (ValueError, AttributeError, TypeError) as err:
            # print('Config was not valid, error: {}, {}'.format(err, config_file.read()))
            return False
        try:
            validate(config, schema)
        except ValidationError as err:
            # print('Config was not valid, error: {}, {}'.format(err, config_file.read()))
            return False
        return True


if __name__ == '__main__':
    result = None
    if validate_config(sys.argv[1]):
        result = '1'
    else:
        result = '0'
    sys.stdout.write(result)

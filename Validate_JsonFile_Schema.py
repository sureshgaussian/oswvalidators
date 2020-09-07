from jsonschema import Draft7Validator
from config import DefaultConfigs
import json
import os
import ntpath


def error_capture(key,errors,index):

    errordict = {
        "required":errors.message + " for " + str(errors.schema_path[index-1]),
        "maxItems": errors.message + " min for " + str(errors.schema_path[index-1]),
        "minItems": errors.message + " max for " + str(errors.schema_path[index-1]),
        "maximum":  errors.message + " allowed for property " +  str( errors.schema_path[index-1]),
        "minimum": errors.message + " allowed for property " + str( errors.schema_path[index-1]),
        "additionalProperties": (errors.message.split('(')[-1]).split(' ')[0] + " is not a valid OSW tag",
        "const": "'" + str(errors.schema_path[index-1]) + "':" + errors.message,
        "enum": errors.message + " that are allowed for " + str( errors.schema_path[index-1]),
        "anyOf": errors.message.split('}')[0] + "} missing required supporting tags"
    }
    
    return errordict.get(key, errors.message + " MISSED CAPTURING THIS " + errors.schema_path[index])


def validate_json_schema(geojson_path=None, schema_path=None, writePath=None):
    # Read schema and json files

    with open(geojson_path) as fp:
        geojson = json.load(fp)
    with open(schema_path) as fp:
        schema = json.load(fp)

    validator = Draft7Validator(schema)
    errors = validator.iter_errors(geojson)

    invalid_ids = dict()  # A dictionary to hold IDs of invalid nodes and error messages
    for error in errors:
        if error.path[1] not in invalid_ids.keys():
            invalid_ids.update({error.path[1]: list()})
        index = len(error.schema_path) - 1
        error_message = error_capture(error.schema_path[index], error, index)
        invalid_ids[error.path[1]].append(error_message)

    return invalid_ids


if __name__ == '__main__':
    cf = DefaultConfigs()

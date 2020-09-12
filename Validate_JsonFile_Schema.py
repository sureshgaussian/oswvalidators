from jsonschema import Draft7Validator
from config import DefaultConfigs
import json
import os
import ntpath
import argparse

def minItems_error(errors,index):
    if len(errors.schema_path)==8 and errors.schema_path[7]=='minItems' and errors.schema_path[4]=='geometry':
        return str(errors.instance) + ". LineString(Way) Geometry should contain atleast 2 coordinate"
    else:

        return errors.message + " max for " + str(errors.schema_path[index - 1])

def maxItems_error(errors,index):
    if len(errors.schema_path)==8 and errors.schema_path[7]=='maxItems' and errors.schema_path[4]=='geometry':
        return str(errors.instance) + " - Point Geometry should contain only 1 coordinate"
    else:

        return errors.message + " min for " + str(errors.schema_path[index - 1])

def type_item_error(errors):
    if len(errors.schema_path)==10 and errors.schema_path[6]=='coordinates' and errors.schema_path[4]=='geometry' and errors.schema_path[9]=="type":
        return str(errors.instance) + " - please remove the extra points. Point Geometry should contain only 1 coordinate"



def error_capture(key,errors,index):

    errordict = {
        "required":errors.message + " for " + str(errors.schema_path[index-1]),
        "maxItems": maxItems_error(errors,index),
        "minItems": minItems_error(errors,index),
        "maximum":  errors.message + " allowed for property " +  str( errors.schema_path[index-1]),
        "minimum": errors.message + " allowed for property " + str( errors.schema_path[index-1]),
        "additionalProperties": (errors.message.split('(')[-1]).split(' ')[0] + " is not a valid OSW tag",
        "const": "'" + str(errors.schema_path[index-1]) + "':" + errors.message,
        "enum": errors.message + " that are allowed for " + str( errors.schema_path[index-1]),
        "anyOf": errors.message.split('}')[0] + "} missing required supporting tags",
        "additionalItems": str(errors.instance) + " - Only one of the coordinate or point should be there",
        "type": type_item_error(errors)
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
        # print(error.schema_path)
        index = len(error.schema_path) - 1
        error_message = error_capture(error.schema_path[index], error, index)
        invalid_ids[error.path[1]].append(error_message)

    return invalid_ids


if __name__ == '__main__':
    cf = DefaultConfigs()
    parser = argparse.ArgumentParser(description='Run Pipeline')
    parser.add_argument('--jsonInputPath', help="geo_json path input", required=True)
    parser.add_argument('--schemaInputPath', help="schema path input", required=True)
    parser.add_argument('--writePath', help="output path", required=True)
    args = parser.parse_args()
    result = validate_json_schema(args.jsonInputPath, args.schemaInputPath)
    asjson = json.dumps(result)
    if json.loads(asjson):
        print('Generated validation')
        valid_file = open(args.writePath, "w")
        valid_file.write(asjson)
        valid_file.close()
    else:
        print('error generating validation')
    

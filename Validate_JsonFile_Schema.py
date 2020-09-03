from jsonschema import Draft7Validator
from config import DefaultConfigs
import json
import os
import ntpath


def error_capture(key, errors, index):
    errordict = {
        "required": errors.message + " for " + errors.schema_path[index - 1],
        "maxItems": errors.message + " for " + errors.schema_path[index - 1],
        "minItems": errors.message + " for " + errors.schema_path[index - 1],
        "maximum": errors.message + " allowed for property " + errors.schema_path[index - 1],
        "minimum": errors.message + " allowed for property " + errors.schema_path[index - 1],
        "additionalProperties": errors.message,
        "const": "'" + errors.schema_path[index - 1] + "':" + errors.message
    }
    return errordict.get(key, errors.message + " MISSED CAPTURING THIS " + errors.schema_path[index])


def validate_json_schema(geojson_path=None, schema_path=None, writePath=None):
    # Read schema and json files

    # valid_save_path = os.path.join(writePath,
    #                                (ntpath.basename(geojson_path).split('.')[0].split("\\")[
    #                                     -1] + '_schema_valid.geojson'))
    # invalid_save_path = os.path.join(writePath,
    #                                  (ntpath.basename(geojson_path).split('.')[0].split("\\")[
    #                                       -1] + '_schema_invalid.geojson'))
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

    # invalid_json = geojson.copy()
    # valid_json = geojson.copy()
    # invalid_json['features'] = []
    #
    # # Add invalid nodes and error message to invalid_json
    # for invalid_id, msg in invalid_ids.items():
    #     # print(invalid_id, msg)
    #     invalid_json['features'].append(geojson['features'][invalid_id])
    #     invalid_json['features'][-1].update({"fixme": msg})

    # # Dump the json to valid and invalid files
    # with open(invalid_save_path, 'w') as fp:
    #     json.dump(invalid_json, fp, indent=4)
    #
    # for ind in sorted(invalid_ids.keys(), reverse=True):
    #     del valid_json['features'][ind]
    # with open(valid_save_path, 'w') as fp:
    #     json.dump(valid_json, fp, indent=4)

    return invalid_ids


if __name__ == '__main__':
    cf = DefaultConfigs()

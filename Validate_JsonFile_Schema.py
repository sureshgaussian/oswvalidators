from jsonschema import Draft7Validator
from config import DefaultConfigs
import json
import sys


def validate_json_schema(geojson_path=None, schema_path=None):
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
        invalid_ids[error.path[1]].append(
            "Error Message : " + error.message + ". Schema Path : " + str(error.schema_path))

    invalid_json = geojson.copy()
    valid_json = geojson.copy()
    invalid_json['features'] = []

    # Add invalid nodes and error message to invalid_json
    for invalid_id, msg in invalid_ids.items():
        # print(invalid_id, msg)
        invalid_json['features'].append(geojson['features'][invalid_id])
        invalid_json['features'][-1].update({"fixme": msg})

    # Dump the json to valid and invalid files
    with open(cf.path_invalid_nodes, 'w') as fp:
        json.dump(invalid_json, fp, indent=4)

    for ind in sorted(invalid_ids.keys(), reverse=True):
        del valid_json['features'][ind]
    with open(cf.path_valid_nodes, 'w') as fp:
        json.dump(valid_json, fp, indent=4)


if __name__ == '__main__':
    cf = DefaultConfigs()
    validate_json_schema(cf.test_nodes_json, cf.node_schema)
    validate_json_schema(cf.test_ways_json, cf.ways_schema)

from jsonschema import Draft7Validator
from config import DefaultConfigs
import json
import os
import ntpath


def validate_json_schema(geojson_path = None, schema_path = None, writePath = None):
    # Read schema and json files

    valid_save_path = os.path.join(writePath,
                                       (ntpath.basename(geojson_path).split('.')[0].split("\\")[-1] + '_schema_valid.geojson'))
    invalid_save_path = os.path.join(writePath,
                                       (ntpath.basename(geojson_path).split('.')[0].split("\\")[-1] + '_schema_invalid.geojson'))
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
        schema_path = str()
        for i in error.schema_path:
            schema_path += i + '/'
        invalid_ids[error.path[1]].append(
            "Error Message : " + error.message + ". Schema Path : " + schema_path[:-1])

    invalid_json = geojson.copy()
    valid_json = geojson.copy()
    invalid_json['features'] = []

    # Add invalid nodes and error message to invalid_json
    for invalid_id, msg in invalid_ids.items():
        # print(invalid_id, msg)
        invalid_json['features'].append(geojson['features'][invalid_id])
        invalid_json['features'][-1].update({"fixme": msg})


    # Dump the json to valid and invalid files
    with open(invalid_save_path, 'w') as fp:
        json.dump(invalid_json, fp, indent=4)

    for ind in sorted(invalid_ids.keys(), reverse=True):
        del valid_json['features'][ind]
    with open(valid_save_path, 'w') as fp:
        json.dump(valid_json, fp, indent=4)


if __name__ == '__main__':
    cf = DefaultConfigs()
    validate_json_schema(nodes_file, cf.node_schema, cf.writePath)
    validate_json_schema(ways_file, cf.ways_schema, cf.writePath)

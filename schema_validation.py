from jsonschema import Draft7Validator
from config import DefaultConfigs
import json

cf = DefaultConfigs()

#Read schema and json files
with open(cf.test_schema) as fp:
    json_schema = json.load(fp)
with open(cf.test_geojson) as fp:
    sample_json = json.load(fp)

validator = Draft7Validator(json_schema)
errors = validator.iter_errors(sample_json)

invalid_ids = dict()  # A dictionary to hold IDs of invalid nodes and error messages
for error in errors:
    invalid_ids.update({error.path[-1]: list()})
    for suberror in error.context:
        invalid_ids[error.path[-1]].append(suberror.message)

invalid_nodes_json = sample_json.copy()
valid_nodes_json = sample_json.copy()
invalid_nodes_json['features'] = []

# Add invalid nodes and error message to invalid_nodes_json
for invalid_id, msg in invalid_ids.items():
    invalid_nodes_json['features'].append(sample_json['features'][invalid_id])
    invalid_nodes_json['features'][-1].update({"error": msg})

# Dump the json to valid and invalid files
with open(cf.path_invalid_nodes, 'w') as fp:
    json.dump(invalid_nodes_json, fp, indent=4)

for ind in sorted(invalid_ids.keys(), reverse=True):
    del valid_nodes_json['features'][ind]
with open(cf.path_valid_nodes, 'w') as fp:
    json.dump(valid_nodes_json, fp, indent=4)
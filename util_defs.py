from itertools import chain
import copy
import os
import json
import ntpath


def save_file(path, json_file):
    with open(path, 'w') as fp:
        json.dump(json_file, fp, indent=4)


def merge_dicts(dict1, dict2):
    merged_dict = copy.deepcopy(dict1)
    if dict2.keys():
        for id, msgs in dict2.items():
            if id not in merged_dict.keys():
                merged_dict[id] = msgs
            else:
                merged_dict[id].extend(msgs)
    return merged_dict


def write_outputs(utild, cf, nodes_dict, ways_dict):
    
    invalid_nodes_json = copy.deepcopy(utild.nodes_json)
    invalid_nodes_json['features'] = []
    invalid_ways_json = copy.deepcopy(utild.ways_json)
    invalid_ways_json['features'] = []
    valid_nodes_json = copy.deepcopy(utild.nodes_json)
    valid_ways_json = copy.deepcopy(utild.ways_json)

    for id, msg in sorted(nodes_dict.items(), reverse=True):
        valid_nodes_json['features'].pop(id)
        invalid_nodes_json['features'].append(utild.nodes_json['features'][id])
        invalid_nodes_json['features'][-1].update({"fixme": msg})

    for id, msg in sorted(ways_dict.items(), reverse=True):
        valid_ways_json['features'].pop(id)
        invalid_ways_json['features'].append(utild.ways_json['features'][id])
        invalid_ways_json['features'][-1].update({"fixme": msg})

    valid_nodes_save_path = os.path.join(cf.writePath,(ntpath.basename(utild.nodes_file).split('.')[0] + '_valid.geojson'))
    save_file(valid_nodes_save_path, valid_nodes_json)

    invalid_nodes_save_path = os.path.join(cf.writePath,(ntpath.basename(utild.nodes_file).split('.')[0] + '_invalid.geojson'))
    save_file(invalid_nodes_save_path, invalid_nodes_json)

    valid_ways_save_path = os.path.join(cf.writePath,(ntpath.basename(utild.ways_file).split('.')[0] + '_valid.geojson'))
    save_file(valid_ways_save_path, valid_ways_json)

    invalid_ways_save_path = os.path.join(cf.writePath,(ntpath.basename(utild.ways_file).split('.')[0] + '_invalid.geojson'))
    save_file(invalid_ways_save_path, invalid_ways_json)

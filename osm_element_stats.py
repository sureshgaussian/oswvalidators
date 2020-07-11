# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 18:45:50 2020

@author: rtgun

Beginner script template for some validations.
"""
import json
from glob import glob
import os


def get_property_set(features_list):
    #Check keys in each of the properties element
    prop_set = set()
    for ind, ft in enumerate(data_dict['features']):
      prop_keys = list(ft['properties'].keys())
      prop_set.update(prop_keys)
    print('Property set {}'.format(prop_set))    
    return prop_set

def get_geometry_type_set(features_list):
    #Get geometry type values from features list
    geom_type_set = set()
    for ind, ft in enumerate(features_list):
      geom_type = ft['geometry']['type']
      geom_type_set.add(geom_type)
    print('Geometry Type set : {}'.format(geom_type_set))
    return geom_type_set

if __name__ == '__main__':
    
    path = "E:\oswvalidators\OSW\TestData"
    os.chdir(path)
    json_files = glob("*.geojson")
    print("Number of json files :", len(json_files))
    print(json_files)
    
    # json_files = [i for i in json_files if 'broken' not in i]
    
    
    for ind, file in enumerate(json_files):
        print('-'*10)
        print('File Name : {}'.format(file))
        with open(file) as data_json:
            data_dict = json.load(data_json)
    
        property_set = get_property_set(data_dict['features'])        
        geom_type_set = get_geometry_type_set(data_dict['features'])

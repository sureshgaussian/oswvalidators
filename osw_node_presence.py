# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 17:28:28 2020

@author: rtgun
"""

import json
import numpy as np
import pandas as pd
from glob import glob
import os

def get_node_sidewalk_set(elems):
  '''
  elems : elements dictionary from df
  node_id_set : set of node ids
  sidewalk_elements : list of sidewalk elements
  '''
  node_id_set = set()
  sidewalk_elements = []
  for elem in elems:
    if(elem['type'] == "node"):
      node_id_set.add(elem['id'])
      continue
    # break
    elif(elem['type'] == "way"):
      if set({"footway", "highway"}).issubset(set(elem['tags'].keys())):
        if(elem['tags']['highway'] == "footway" and elem['tags']['footway'] == "sidewalk"):
          sidewalk_elements.append(elem)
  return node_id_set, sidewalk_elements

if __name__ == '__main__':
    
    path = "E:\oswvalidators\OSW\TestData"
    os.chdir(path)
    json_files = glob("*.json")
    json_files.sort()
    print("Number of json files :", len(json_files))
    print(json_files)
    
    for ind, file in enumerate(json_files):
        with open(file) as json_data:
            df = json.load(json_data)
    
    print(df.keys())
    elems = df['elements']
    node_set, sidewalk_elements = get_node_sidewalk_set(elems)
    print('Number of nodes : {}'.format(len(node_set)))
    print('Number of Sidewalk elements : {}'.format(len(sidewalk_elements)))

    missing_nodes = []
    for sw_e in sidewalk_elements:
        for node in sw_e['nodes']:
            if(node not in node_set):
                missing_nodes.append(node)
    print('Validation : Failed -- Missing Nodes : {} from way id : {} '.format(missing_nodes, sw_e['id'])) if len(missing_nodes) else print('Validation : Success')

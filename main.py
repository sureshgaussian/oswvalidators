import argparse as ag
import os
from intersectingValidation import readJsonFile,intersectLineStringInValidFormat,geojsonWrite

from glob import glob 
from node_connectivity import plot_nodes_vs_ways, subgraph_eda, get_invalidNodes, geometry_type_validation
import json
import networkx as nx
import pickle
import numpy as np
import sys
from config import DefaultConfigs
from util_data import UtilData
import time
import ntpath

if __name__ == '__main__':
    parser = ag.ArgumentParser()
    parser.add_argument("--GeoJSON", help="GeoJSON filepath absolute path ", default = os.path.join(os.getcwd(), "OSW\TestData"))
    parser.add_argument("--validation", help="type of validation", default = 'intersectingvalidation')
    parser.add_argument("--writePath",help="output directory to write the validation errors", default = os.path.join(os.getcwd(), "OSW\TestData\Output"))
    args = parser.parse_args()
    cf = DefaultConfigs(args)
    path = args.GeoJSON
    outputDirectory = args.writePath

    json_files = glob(os.path.join(path,"*.geojson"))
    json_files = sorted([i for i in json_files if cf.file_filter in i])
    print("Number of json files :", len(json_files))
    nodes_files = sorted([x for x in json_files if 'node' in x])
    ways_files = sorted([x for x in json_files if 'node' not in x])

    for ind, (nodes_file, ways_file) in enumerate(zip(nodes_files, ways_files)):  
        print('-'*10)
        print('Processing File : \n{}\n{}'.format(ntpath.basename(nodes_file), ntpath.basename(ways_file)))
        with open(nodes_file) as data_json:
            node_json = json.load(data_json)
        with open(ways_file) as data_json:
            way_json = json.load(data_json)    
            
        dutil = UtilData(nodes_file, ways_file, cf)
        
        if cf.validation == 'intersectingvalidation':
            intersectLineStringInValidFormat(dutil.ways_json, "brunnel", cf)

        if cf.do_all_validations:
            geometry_type_validation(dutil)
            get_invalidNodes(dutil,cf)
            
        if cf.do_all_eda:
            plot_nodes_vs_ways(dutil)
            subgraph_eda(dutil)

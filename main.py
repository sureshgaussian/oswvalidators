import argparse as ag
import os
# from intersectingValidation import readJsonFile,intersectLineStringInValidFormat,jsonWrite,geojsonWrite

from glob import glob 
from node_connectivity import get_ways, plot_nodes_vs_ways, get_coord_dict, split_geojson_file
from node_connectivity import geometry_type_validation, get_coord_df, get_isolated_way_ids
from node_connectivity import get_way_from_subgraph, get_invalidNodes, subgraph_eda
import json
import networkx as nx
import pickle
import numpy as np
import sys
from config import DefaultConfigs


if __name__ == '__main__':

    parser = ag.ArgumentParser()
    parser.add_argument("--GeoJSON", help="GeoJSON filepath absolute path ", default = os.path.join(os.getcwd(), "OSW\TestData"))
    parser.add_argument("--validation", help="type of validation", default = 'eda')
    parser.add_argument("--writePath",help="output directory to write the validation errors", default = os.path.join(os.getcwd(), "OSW\TestData\Outputfiles"))
    args = parser.parse_args()
    path = args.GeoJSON
    outputDirectory = args.writePath
    
    cf = DefaultConfigs(args)
    
    if(args.validation=="intersectingvalidation"):
        dataDict = readJsonFile(path)
        invalidWaysID, dictInvalidFormatID, violatingWayFeatures = intersectLineStringInValidFormat(dataDict, "brunnel")
        pathWrite = outputDirectory + "/invalidWays.geojson"
        pathWriteInvalidFormat = outputDirectory + "/InvalidFormat.geojson"
        invalidGeoJsonIntersection = outputDirectory + "/invalidGeoJsonIntersection.geojson"

        jsonWrite(pathWrite, invalidWaysID)
        jsonWrite(pathWriteInvalidFormat, dictInvalidFormatID)
        geojsonWrite(invalidGeoJsonIntersection, violatingWayFeatures, dataDict)

    if(args.validation == "eda"):
        json_files = glob(os.path.join(path,"*.geojson"))
        json_files = sorted([i for i in json_files if cf.file_filter in i])
        print("Number of json files :", len(json_files))
        print(json_files)
        node_files = sorted([x for x in json_files if 'node' in x])
        way_files = sorted([x for x in json_files if 'node' not in x])

        for ind, (node_file, way_file) in enumerate(zip(node_files, way_files)):  
            print('-'*10)
            print('Processing File : \n{}\n{}'.format(node_file, way_file))
            with open(node_file) as data_json:
                node_json = json.load(data_json)
            with open(way_file) as data_json:
                way_json = json.load(data_json)       
            nodes_list = get_ways(node_json['features'], cf)    
            ways_list = get_ways(way_json['features'], cf)          
            plot_nodes_vs_ways(ways_list)          
            node_way_dict = get_coord_dict(nodes_list, ways_list)
            invalid_nodes = get_invalidNodes(node_way_dict, node_json, node_file, cf)        
            geometry_type_validation(way_file, cf)         
            isolated_way_ids = get_isolated_way_ids(ways_list, node_way_dict)         
            split_geojson_file(way_file, node_way_dict, cf)         
            subgraph_eda(ways_list, isolated_way_ids)
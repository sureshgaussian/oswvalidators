import argparse as ag
import os
from intersectingValidation import readJsonFile,intersectLineStringInValidFormat,geojsonWrite

from glob import glob 
from node_connectivity import plot_nodes_vs_ways, subgraph_eda
import json
import networkx as nx
import pickle
import numpy as np
import sys
from config import DefaultConfigs
from util_data import UtilData
import time

if __name__ == '__main__':
    parser = ag.ArgumentParser()
    parser.add_argument("--GeoJSON", help="GeoJSON filepath absolute path ", default = os.path.join(os.getcwd(), "OSW\TestData"))
    parser.add_argument("--validation", help="type of validation", default = 'eda')
    parser.add_argument("--writePath",help="output directory to write the validation errors", default = os.path.join(os.getcwd(), "OSW\TestData\Output"))
    args = parser.parse_args()
    cf = DefaultConfigs(args)
    path = args.GeoJSON
    outputDirectory = args.writePath

    if(args.validation=="intersectingvalidation"):
        start_time = time.time()

        data = readJsonFile(path)
        intersectingNodeGeoJSON, invalidWayGeoJSONFormat, violatingWayFeatures = intersectLineStringInValidFormat(data,"brunnel")
        pathWrite = outputDirectory + "/recommendedIntersections.geojson"
        pathWriteInvalidFormat = outputDirectory + "/InvalidGeometryFormat.geojson"
        pathInvalidGeoJsonIntersection = outputDirectory + "/WaysMissingIntersection.geojson"

        geojsonWrite(pathWriteInvalidFormat, invalidWayGeoJSONFormat, data)
        geojsonWrite(pathInvalidGeoJsonIntersection, violatingWayFeatures, data)
        geojsonWrite(pathWrite, intersectingNodeGeoJSON, data)
        print("--- %s seconds ---" % (time.time() - start_time))

    if(args.validation == "eda"):
        json_files = glob(os.path.join(path,"*.geojson"))
        json_files = sorted([i for i in json_files if cf.file_filter in i])
        print("Number of json files :", len(json_files))
        print(json_files)
        nodes_files = sorted([x for x in json_files if 'node' in x])
        ways_files = sorted([x for x in json_files if 'node' not in x])

        for ind, (nodes_file, ways_file) in enumerate(zip(nodes_files, ways_files)):  
            print('-'*10)
            print('Processing File : \n{}\n{}'.format(nodes_file, ways_file))
            with open(nodes_file) as data_json:
                node_json = json.load(data_json)
            with open(ways_file) as data_json:
                way_json = json.load(data_json)    
                
            dutil = UtilData(nodes_file, ways_file, cf)
            if cf.do_all_validations:
                dutil.all_validations(cf)
            if cf.do_all_eda:
                plot_nodes_vs_ways(dutil)
                subgraph_eda(dutil)

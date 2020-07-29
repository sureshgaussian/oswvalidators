import argparse as ag
import os
from intersectingValidation import readJsonFile,intersectLineStringInValidFormat,jsonWrite,geojsonWrite

from glob import glob 
from node_connectivity import get_ways, plot_nodes_vs_ways, get_coord_dict, split_geojson_file
from node_connectivity import geometry_type_validation, get_coord_df, get_isolated_way_ids
from node_connectivity import get_way_from_subgraph
import json
import networkx as nx
import pickle


if __name__ == '__main__':

    parser = ag.ArgumentParser()
    parser.add_argument("--GeoJSON", help="GeoJSON filepath absolute path ")
    parser.add_argument("--validation", help="type of validation")
    parser.add_argument("--writePath",help="output directory to write the validation errors")
    args = parser.parse_args()
    path = args.GeoJSON
    outputDirectory = args.writePath
    
    if not args.GeoJSON:
        path = os.path.join(os.getcwd(), "OSW\TestData")
    if not args.validation:
        args.validation = "eda"
    if not args.writePath:
        outputDirectory = path

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
        json_files = [i for i in json_files if 'redmond.' in i]
        print("Number of json files :", len(json_files))
        for ind, file in enumerate(json_files):  
            print('-'*10)
            print('Processing File : {}'.format(file))
            with open(file) as data_json:
                data_dict = json.load(data_json)
        
            ways = get_ways(data_dict['features'])
            plot_nodes_vs_ways(ways)
            coord_dict = get_coord_dict(ways)            
            geometry_type_validation(file)
            
            isolated_way_ids = get_isolated_way_ids(ways, coord_dict)
            
            split_geojson_file(file)
             
            Connected_Ways = ways.copy()
            for x in sorted(isolated_way_ids, reverse = True):  
                del Connected_Ways[x] 
        
            print("Number of ways in the file : ", len(ways))
            print("Number of isolated ways: ", len(isolated_way_ids))
            print("Number of Connected ways in the file : ", len(Connected_Ways))
            
            Connected_df = get_coord_df(Connected_Ways)
            Connected_FG = nx.from_pandas_edgelist(Connected_df, source='origin', target='dest')
            print("Is Connected ? : ", nx.is_connected(Connected_FG))
            print("Number of Connected Components : ", nx.number_connected_components(Connected_FG))
                
            subgraphs = [Connected_FG.subgraph(c).copy() for c in nx.connected_components(Connected_FG)]
                          
            pickle.dump(subgraphs, open(os.path.join(path, 'subgraphs.pkl'), 'wb'))
            subgraphs = pickle.load(open(os.path.join(path, 'subgraphs.pkl'), 'rb'))
            
            pickle.dump(Connected_df, open(os.path.join(path, 'Connected_df.pkl'), 'wb'))
            Connected_df = pickle.load(open(os.path.join(path, 'Connected_df.pkl'), 'rb'))
            
            nx.draw_networkx(subgraphs[1])
            
            sgraph = subgraphs[1]
            ways_set = get_way_from_subgraph(subgraphs[1], Connected_df)
            print("sgraph_ways {}".format(ways_set))  
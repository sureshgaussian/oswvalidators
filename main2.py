# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 18:38:19 2020

@author: rtgun
"""

import argparse as ag
import os
from glob import glob 
from node_connectivity import get_ways, plot_nodes_vs_ways, get_coord_dict, split_geojson_file
from node_connectivity import geometry_type_validation, get_coord_df, get_isolated_way_ids
from node_connectivity import get_way_from_subgraph
import json
import networkx as nx
import pickle

if __name__ == '__main__':
    parser = ag.ArgumentParser()
    parser.add_argument("--GeoJSON", help="GeoJSON filepath absolute path")
    parser.add_argument("--validation", help="type of validation")
    parser.add_argument("--writePath",help="output directory to write the validation errors")
    args = parser.parse_args()
    # path = args.GeoJSON
    outputDirectory = args.writePath
    path = os.path.join(os.getcwd(), "OSW\TestData")
    os.chdir(path)
    json_files = glob("*.geojson")
    json_files = [i for i in json_files if 'redmond.' in i]
    print("Number of json files :", len(json_files))
    if not args.validation:
        args.validation = "eda"

    if(args.validation == "eda"):
        for ind, file in enumerate(json_files):  
            print('-'*10)
            print('Processing File : {}'.format(file))
            with open(file) as data_json:
                data_dict = json.load(data_json)
        
            Ways = get_ways(data_dict['features'])
            plot_nodes_vs_ways(Ways)
            # break
            coord_dict = get_coord_dict(Ways)
            
            geometry_type_validation(file)
            
            df = get_coord_df(Ways)
            
            isolated_way_ids = get_isolated_way_ids(Ways, coord_dict)
            
            split_geojson_file(file)
             
            Connected_Ways = Ways.copy()
            for x in sorted(isolated_way_ids, reverse = True):  
                del Connected_Ways[x] 
        
            #printing modified list
            print("Number of ways in the file : ", len(Ways))
            print("Number of isolated ways: ", len(isolated_way_ids))
            print("Number of Connected ways in the file : ", len(Connected_Ways))
            
            
            Connected_df = get_coord_df(Connected_Ways)
            Connected_FG = nx.from_pandas_edgelist(Connected_df, source='origin', target='dest')
            print("Is Connected ? : ", nx.is_connected(Connected_FG))
            print("Number of Connected Components : ", nx.number_connected_components(Connected_FG))
                
            S = [Connected_FG.subgraph(c).copy() for c in nx.connected_components(Connected_FG)]
                    
        
            pickle.dump(S, open('S.pkl', 'wb'))
            S = pickle.load(open('S.pkl', 'rb'))
            
            pickle.dump(Connected_df, open('Connected_df.pkl', 'wb'))
            Connected_df = pickle.load(open('Connected_df.pkl', 'rb'))
            
            pickle.dump(df, open('ways_df.pkl', 'wb'))
            df = pickle.load(open('ways_df.pkl', 'rb'))
                    
            nx.draw_networkx(S[1])
            
            sgraph = S[1]
            ways_set = get_way_from_subgraph(S[1], df)
            print("sgraph_ways {}".format(ways_set))        
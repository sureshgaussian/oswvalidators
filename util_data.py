# -*- coding: utf-8 -*-
"""
Utility Data Class to store intermediate data structures for reuse.
"""

import os
import json
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import ntpath
import networkx as nx

class UtilData():
    def __init__(self, nodes_file, ways_file, cf):

        self.nodes_file = nodes_file
        self.ways_file = ways_file
        
        self.nodes_list = []
        self.ways_list = []
        
        self.coord_dict = dict()
        self.one_node_ls_ids = []

        # self.node_way_dict = dict()
        self.invalid_nodes = []
        self.isolated_way_ids = []
        
        with open(nodes_file) as data_json:
            self.nodes_json = json.load(data_json)
        with open(ways_file) as data_json:
            self.ways_json = json.load(data_json)
        
        #Construct the utility data
        self.nodes_list = self.get_coords_list(self.nodes_json['features'], cf)    
        self.ways_list = self.get_coords_list(self.ways_json['features'], cf)
        self.get_coord_dict() 
        
    def all_validations(self, cf):
                            
        self.get_invalidNodes(cf)        
        self.geometry_type_validation()         
        self.get_isolated_ways()         
        self.split_geojson_file(cf)
        
    def get_coords_list(self, features_list, cf):
        '''
        Returns list of list of coordinates.
        Outer list is the element
        Inner list is the coordinates within an element
        '''
        coord_list = []
        filter_sidewalks = cf.filter_sidewalks # Set True to include just sidewalks. Otherways all ways are returned
        for elem in features_list:
            if(filter_sidewalks):
                if (elem['properties']['footway'] == 'sidewalk'):
                    coord_list.append(elem['geometry']['coordinates'])
            else:
                coord_list.append(elem['geometry']['coordinates'])
        return coord_list
    
    def get_coord_dict(self):
        '''
        Returns dictionary of coordinate
        keys : unique coordinates
        values : all ways to which the coord belongs
        '''
        coord_dict = dict()
        for elem in self.nodes_list:
            if(str(elem) not in coord_dict.keys()):
                coord_dict[str(elem)] = list()
        
        for id, elem in enumerate(self.ways_list):
            for point in elem:
                if(str(point) not in coord_dict.keys()):
                    coord_dict[str(point)] = [id]
                else:
                    coord_dict[str(point)].append(id)
        self.coord_dict = coord_dict
    
    def get_isolated_ways(self):
        '''
        Get ways to be discared (ways that are not part of any other ways)
        '''
        isolated_way_ids = set()
        for id, elem in enumerate(self.ways_list):
            ctr = 0
            for point in elem:
                if len(self.coord_dict[str(point)]) > 1:
                    break
                else:
                    ctr += 1
            if ctr == len(elem):
                isolated_way_ids.update([id])
        self.isolated_way_ids = isolated_way_ids
    
    def split_geojson_file(self, cf):
        '''
        Splits the geojson file based on connectivity with with other ways
        and save into two files :
        1. file_connected.geojson (ways that are connected to atleast one other way)
        2. file_disconnected.geojson (ways that are not connected to any other way)
        ---
        Args : file - .geojson file to be split 
        Returns : None
        '''
        connected_way_ids = set(np.arange(len(self.ways_list))) - set(self.isolated_way_ids)   
        
        connected_ways = self.ways_json.copy()
        connected_ways['features'] = []
        disconnected_ways = self.ways_json.copy()
        disconnected_ways['features'] = []
        
        disconnected_ways['features'] = [self.ways_json['features'][ind] for ind in self.isolated_way_ids]
        connected_ways['features'] = [self.ways_json['features'][ind] for ind in connected_way_ids]
        
        connected_save_path = os.path.join(cf.writePath, (ntpath.basename(self.ways_file).split('.')[0] + '_connected.geojson'))
        disconnected_save_path = os.path.join(cf.writePath, (ntpath.basename(self.ways_file).split('.')[0] + '_disconnected.geojson'))
    
        with open(connected_save_path, 'w') as fp:
            json.dump(connected_ways,fp, indent = 4)
        with open(disconnected_save_path, 'w') as fp:
            json.dump(disconnected_ways,fp, indent = 4) 
        print("ways_file split into {} and {}".format(connected_save_path,disconnected_save_path))
    
    def get_invalidNodes(self, cf):
        '''
        A node is invalid if it is not part of any way.
        Dump the invalid nodes into a {filename}_invalid.geojson
        '''
        vals = np.array(list(self.coord_dict.values()))            
        invalid_nodes = [ind for ind, val in enumerate(vals) if len(val) == 0]
        invalid_nodes_json = self.nodes_json.copy()
        invalid_nodes_json['features'] = []
        [invalid_nodes_json['features'].append(self.nodes_json['features'][ind]) for ind in invalid_nodes]
        
        invalid_save_path = os.path.join(cf.writePath, (ntpath.basename(self.nodes_file).split('.')[0] + '_invalid.geojson'))
        with open(invalid_save_path, 'w') as fp:
            json.dump(invalid_nodes_json,fp, indent = 4) 
        print('Invalid Nodes dumped to {}'.format(self.nodes_file.split('.')[0] + '_invalid.geojson'))


    def get_coord_df(self, coords_list):
        '''
        Return df with two columns origin and dest for starting and ending nodes of the way
        This is needed for connected component of networkx package
        '''
        data = {'origin':[], 'dest': []}
        df = pd.DataFrame(data)
        for elem in coords_list:
            df = df.append({'origin':str(elem[0]), 'dest':str(elem[-1])}, ignore_index=True)
        return df 
    
    def geometry_type_validation(self):
        '''
        Geojson Geometry type validations : https://tools.ietf.org/html/rfc7946#section-3.1.4
        Gets number of linestrings that has only one node
        '''
        one_node_ls_ids = []
        [one_node_ls_ids.append(ind) for ind, way in enumerate(self.ways_list) if len(way) == 1]
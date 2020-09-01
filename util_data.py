# -*- coding: utf-8 -*-
"""
Utility Data Class to store intermediate data structures for reuse.
Idea : All the data related to json files should be in the object of this class.
Any validations that need to READ-ONLY this data can be defined as members outside the class.
Any validations that needs to UPDATE the data shoulb be defined as members of the class UtilData.

Tentative Sequence of operations :

#Build the Utildata
0. Read the nodes and ways files as json objects
1. Build nodes and ways list
2. Build Coord dict
3. Get ways that has only one node.
4. Build coordinate df (for subgraps)
5. Get isolated ways
6. Split json file into connected and disconnected

#EDA
'''
01. Plot #Nodes vs #Ways
02. Plot a random subgraph
'''

#Sequence of validations
'''
01. Check if each node is part of the ways (from coord_dict)
02. Lineintersection
'''

"""
import os
import json
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import ntpath
import time
import networkx as nx


class UtilData:
    def __init__(self, nodes_file, ways_file, cf):

        self.nodes_file = nodes_file
        self.ways_file = ways_file

        self.nodes_list = []
        self.ways_list = []

        self.connected_ways = dict()  # Add connected and disconnected data
        self.disconnected_ways = dict()

        self.coord_dict = dict()
        self.one_node_ls_ids = []

        self.invalid_nodes = []
        self.isolated_way_ids = []

        with open(nodes_file) as data_json:
            self.nodes_json = json.load(data_json)
        with open(ways_file) as data_json:
            self.ways_json = json.load(data_json)

        # Construct the utility data
        self.nodes_list = self.get_coords_list(self.nodes_json['features'], cf)
        self.ways_list = self.get_coords_list(self.ways_json['features'], cf)
        self.get_coord_dict()
        self.get_one_node_ways()
        self.get_isolated_ways()
        self.split_ways_geojson_file(cf)
        self.get_coord_df()

    def get_coords_list(self, features_list, cf):
        """
        Returns list of list of coordinates.
        Outer list corresponds to an element (Node/Way)
        Inner list corresponds to coordinates within an element
        Ex : [[[e1_x1, e1_y1], [e1_x2, e1_y2]], [[e2_x3, e2_y3]]]
        """
        coord_list = []
        filter_sidewalks = cf.filter_sidewalks  # Set True to include just sidewalks. Otherways all ways are returned
        for elem in features_list:
            if filter_sidewalks and 'footway' in elem['properties']:
                if elem['properties']['footway'] == 'sidewalk':
                    coord_list.append(elem['geometry']['coordinates'])
            else:
                coord_list.append(elem['geometry']['coordinates'])
        return coord_list

    def get_coord_dict(self):
        """
        Returns dictionary of coordinates
        keys : unique coordinates
        values : all ways to which the coordinate belongs
        """
        coord_dict = dict()
        for elem in self.nodes_list:
            if str(elem) not in coord_dict.keys():
                coord_dict[str(elem)] = list()

        for id, elem in enumerate(self.ways_list):
            for point in elem:
                if str(point) not in coord_dict.keys():
                    coord_dict[str(point)] = [id]
                else:
                    coord_dict[str(point)].append(id)
        self.coord_dict = coord_dict

    def get_isolated_ways(self):
        """
        A way is isolated if none of it's nodes are part of any other way
        This is with an assumption that every intersection is marked as a node.
        """
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

    def split_ways_geojson_file(self, cf):
        """
        Splits the geojson file based on connectivity with with other ways
        and save into two files :
        1. FileName_connected.geojson (ways that are connected to at least one other way)
        2. FileName_disconnected.geojson (ways that are not connected to any other way)
        """

        connected_ways = self.ways_json.copy()
        connected_ways['features'] = []
        disconnected_ways = self.ways_json.copy()
        disconnected_ways['features'] = []

        disconnected_ways['features'] = [self.ways_json['features'][ind] for ind in self.isolated_way_ids]
        connected_way_ids = set(np.arange(len(self.ways_list))) - set(self.isolated_way_ids)
        connected_ways['features'] = [self.ways_json['features'][ind] for ind in connected_way_ids]

        self.connected_ways = connected_ways
        self.disconnected_ways = disconnected_ways

        connected_save_path = os.path.join(cf.writePath,
                                           (ntpath.basename(self.ways_file).split('.')[0] + '_connected.geojson'))
        disconnected_save_path = os.path.join(cf.writePath,
                                              (ntpath.basename(self.ways_file).split('.')[0] + '_disconnected.geojson'))

        with open(connected_save_path, 'w') as fp:
            json.dump(connected_ways, fp, indent=4)
        with open(disconnected_save_path, 'w') as fp:
            json.dump(disconnected_ways, fp, indent=4)
        print("ways_file split into {} and {}".format(ntpath.basename(connected_save_path),
                                                          ntpath.basename(disconnected_save_path)))

    def get_coord_df(self):
        """
        Return df with two columns origin and dest for starting and ending nodes of the way
        This is needed for connected component of networkx package
        """
        data = {'origin': [], 'dest': []}
        df = pd.DataFrame(data)
        for elem in self.ways_list:
            df = df.append({'origin': str(elem[0]), 'dest': str(elem[-1])}, ignore_index=True)
        self.ways_df = df

    def get_one_node_ways(self):
        """
        Geojson Geometry type validations : https://tools.ietf.org/html/rfc7946#section-3.1.4
        Gets number of linestrings that has only one node
        """
        # start_time = time.time()
        one_node_ls_ids = []
        self.one_node_ls_ids = [one_node_ls_ids.append(ind) for ind, way in enumerate(self.ways_list) if len(way) == 1]
        # print("--- %s seconds ---" % (time.time() - start_time))

# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 20:17:16 2020

@author: rtgun
"""
import os
class DefaultConfigs():
    
    def __init__(self, args):
        self.GeoJSON = args.GeoJSON
        self.validation = args.validation
        self.writePath = args.writePath
        if not os.path.exists(self.writePath):
            os.mkdir(self.writePath)

        self.file_filter = 'ms_campus'      #for now filter just by substring. To be extended to regex
        self.filter_sidewalks = False
        
        self.do_all_validations = True
        
        #Useful data structures for reuse
        self.ways = []
        self.nodes_list = []
        self.ways_list = []
        self.node_way_dict = []
        self.invalid_nodes = []
        self.isolated_ways = []
        
        #EDA
        '''
        01. Plot #Nodes vs #Ways
        02. Plot a random subgraph
        '''
        
        #Sequence of validations
        '''
        01. Check if each node is part of the ways
        02. Geometry type validation (Linestring should have atleast 2 nodes)
        03. 
        '''
        
        ##paths for Output files to be generated
        #Ravi
        self.path_invalid_nodes = ''
        self.path_connected_json = ''
        self.path_disconnected_json = ''
        #Karthik
        self.path_invalidWays = ''
        self.path_InvalidFormat = ''
        self.path_invalidGeoJsonIntersection = ''
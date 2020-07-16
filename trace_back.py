# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 16:19:07 2020

@author: rtgun
"""
import numpy as np
import os
import pandas as pd
import json
from glob import glob
import matplotlib.pylab as plt
import networkx as nx
import pickle

def get_way_from_subgraph(sgraph, df):
    '''
    Networkx gives subgraphs. This function is to infer the 'way id' from the given subgraph.
    Args : subgraph and df
    Retruns : set of ways that belong to subgraph
    '''   
    way_set = set()
    for ind, edge in enumerate(sgraph.edges):        
        #Coordinates can be interchanged between origin and dest. Hence checking both ways
        #either s1 or s2 gets a value which is index of the way from df, the given edge belongs to        
        s1 = pd.Series((df['origin'] == edge[-1]) & (df['dest'] == edge[0]))
        s2 = pd.Series((df['origin'] == edge[0]) & (df['dest'] == edge[-1]))        
        s = s1[s1].index.tolist() + s2[s2].index.tolist()
        way_set.update(s)        
    return list(way_set)

path = "E:\oswvalidators\OSW\TestData"
os.chdir(path)
S = pickle.load(open('S.pkl', 'rb'))
Connected_df = pickle.load(open('Connected_df.pkl', 'rb'))
ways_df = pickle.load(open('ways_df.pkl', 'rb'))


# print(ways_df.shape[0])
ways_set = get_way_from_subgraph(S[0], ways_df)
print(ways_set)
# print(S[1].edges)
# print(ways_df.iloc[ways_set])

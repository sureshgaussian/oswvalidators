import numpy as np
import pandas as pd
import json
import matplotlib.pylab as plt
import networkx as nx
import os
import ntpath
import time




#####EDA Plots


def plot_nodes_vs_ways(utild):
    '''
    Plot frequency distribution of #Nodes in each way
    TO DO : CHECK IF NODES SHOULD MEAN ALL THE NODES OR JUST NODES FROM WAYS
    '''
    coord_freq_dict = dict()
    for elem in utild.ways_list:
        if(len(elem) not in coord_freq_dict.keys()):
            coord_freq_dict[len(elem)] = 1
        else:
            coord_freq_dict[len(elem)] += 1
    lists = sorted(coord_freq_dict.items())
    x, y = zip(*lists)
    plt.xlim((0, 10))
    plt.bar(x, y)
    plt.title("#Nodes vs #Ways")
    plt.show()


def subgraph_eda(utild):
    '''
    Calculates the number of subgraphs from the given ways_list
    Plots a subraph and it's edges
    '''
    Connected_Ways = utild.ways_list.copy()
    for x in sorted(utild.isolated_way_ids, reverse = True):  
        del Connected_Ways[x] 
    print("Number of ways in the file : ", len(utild.ways_list))
    print("Number of isolated ways: ", len(utild.isolated_way_ids))
    print("Number of Connected ways in the file : ", len(Connected_Ways))
    
    Connected_df = utild.ways_df
    Connected_FG = nx.from_pandas_edgelist(Connected_df, source='origin', target='dest')
    print("Number of Connected Components : ", nx.number_connected_components(Connected_FG))    
    subgraphs = [Connected_FG.subgraph(c).copy() for c in nx.connected_components(Connected_FG)]
    #Plot the 2nd subgraph as a sample
    nx.draw_networkx(subgraphs[1])
    ways_set = get_way_from_subgraph(subgraphs[1], Connected_df)
    print("sgraph[{}]_ways {}".format(1,ways_set)) 


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


#### Validations


def get_invalidNodes(dutil, cf):
    '''
    A node is invalid if it is not part of any way.
    Dump the invalid nodes into a {filename}_invalid.geojson
    '''
    vals = np.array(list(dutil.coord_dict.values()))            
    invalid_nodes = [ind for ind, val in enumerate(vals) if len(val) == 0]
    invalid_nodes_json = dutil.nodes_json.copy()
    invalid_nodes_json['features'] = []
    [invalid_nodes_json['features'].append(dutil.nodes_json['features'][ind]) for ind in invalid_nodes]
    
    invalid_save_path = os.path.join(cf.writePath, (ntpath.basename(dutil.nodes_file).split('.')[0] + '_invalid.geojson'))
    with open(invalid_save_path, 'w') as fp:
        json.dump(invalid_nodes_json,fp, indent = 4) 
    print('Invalid Nodes dumped to {}'.format(dutil.nodes_file.split('.')[0] + '_invalid.geojson'))

def geometry_type_validation(dutil):
    '''
    Geojson Geometry type validations : https://tools.ietf.org/html/rfc7946#section-3.1.4
    Gets number of linestrings that has only one node
    '''
    start_time = time.time()
    one_node_ls_ids = []
    [one_node_ls_ids.append(ind) for ind, way in enumerate(dutil.ways_list) if len(way) == 1]
    print("--- %s seconds ---" % (time.time() - start_time))
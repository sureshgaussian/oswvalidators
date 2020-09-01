import numpy as np
import pandas as pd
import json
import matplotlib.pylab as plt
import networkx as nx
import os
import ntpath
import time


#####EDA Plots

def plot_nodes_vs_ways(utild, cf):
    """
    Plot frequency distribution of #Nodes in each way
    TO DO : CHECK IF NODES SHOULD MEAN ALL THE NODES OR JUST NODES FROM WAYS
    """
    coord_freq_dict = dict()
    for elem in utild.ways_list:
        if len(elem) not in coord_freq_dict.keys():
            coord_freq_dict[len(elem)] = 1
        else:
            coord_freq_dict[len(elem)] += 1
    lists = sorted(coord_freq_dict.items())
    x, y = zip(*lists)
    plt.xlim((0, 10))
    plt.bar(x, y)
    plt.title("Node distribution (limited to 10 nodes)")
    plt.xlabel("Number of Nodes")
    plt.ylabel("Number of Ways")
    # plt.show(block=False)
    save_path = os.path.join(cf.writePath, "EDA",
                             (ntpath.basename(utild.ways_file).split('.')[0] + "_NodesVsWays.PNG"))
    plt.savefig(save_path, format="PNG")
    plt.clf()


def subgraph_eda(utild, cf):
    """
    Calculates the number of subgraphs from the given ways_list
    Plots a subraph and it's edges
    """
    print("Number of ways in the file : ", len(utild.ways_list))
    print("Number of isolated ways: ", len(utild.disconnected_ways['features']))
    print("Number of Connected ways: ", len(utild.connected_ways['features']))

    connected_df = utild.ways_df
    connected_FG = nx.from_pandas_edgelist(connected_df, source='origin', target='dest')
    print("Number of Connected Components : ", nx.number_connected_components(connected_FG))
    subgraphs = [connected_FG.subgraph(c).copy() for c in nx.connected_components(connected_FG)]
    save_path = os.path.join(cf.writePath, "EDA",
                             (ntpath.basename(utild.ways_file).split('.')[0] + "_SampleSubgraph.PNG"))
    for i in range(len(subgraphs)):
        if 2 < len(subgraphs[i]) < 10:
            print("Printing subgraph{} edges : \n{}".format(i, subgraphs[i].edges))
            nx.draw_networkx(subgraphs[i])
            ways_set = get_way_from_subgraph(subgraphs[i], connected_df)
            plt.savefig(save_path, format="PNG")
            plt.clf()
            print("sgraph[{}]_ways {}".format(i, ways_set))
            break


def get_way_from_subgraph(sgraph, df):
    """
    Networkx gives subgraphs. This function is to infer the 'way id' from the given subgraph.
    Args : subgraph and df
    Retruns : set of ways that belong to subgraph
    """
    ways_set = set()
    for ind, edge in enumerate(sgraph.edges):
        # Coordinates can be interchanged between origin and dest. Hence checking both ways
        # either s1 or s2 gets a value which is index of the way from df, the given edge belongs to
        s1 = pd.Series((df['origin'] == edge[-1]) & (df['dest'] == edge[0]))
        s2 = pd.Series((df['origin'] == edge[0]) & (df['dest'] == edge[-1]))
        s = s1[s1].index.tolist() + s2[s2].index.tolist()
        ways_set.update(s)
    return list(ways_set)


#### Validations

def get_invalidNodes(utild, cf):
    """
    A node is invalid if it is not part of any way and has no property assigned to it.
    Dump the invalid nodes into a {filename}_invalid.geojson
    """
    vals = np.array(list(utild.coord_dict.values()), dtype=object)
    invalid_nodes = [ind for ind, val in enumerate(vals) if
                     (len(val) == 0 and len(utild.ways_json['features'][ind]['properties']) == 0)]
    invalid_nodes_json = utild.nodes_json.copy()
    invalid_nodes_json['features'] = []
    [invalid_nodes_json['features'].append(utild.nodes_json['features'][ind]) for ind in invalid_nodes]

    invalid_save_path = os.path.join(cf.writePath,
                                     (ntpath.basename(utild.nodes_file).split('.')[0] + '_invalid.geojson'))
    with open(invalid_save_path, 'w') as fp:
        json.dump(invalid_nodes_json, fp, indent=4)
    print('Invalid Nodes dumped to {}'.format(ntpath.basename(invalid_save_path)))

import numpy as np
import pandas as pd
import json
import matplotlib.pylab as plt
import networkx as nx
import os
import ntpath
import copy
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

def save_file(path, json_file):
    with open(path, 'w') as fp:
        json.dump(json_file, fp, indent=4)

#### Validations

def get_invalidNodes(utild, cf):
    """
    From nodes_dict(N) and ways_dict(W),
    1. N ^ W : ?? only for optimization
    2. N - W : Remaining nodes are invalid if they don't have at least one property
    3. W - N : Ways contain points that are not listed in the nodes file

    """

    error_nodes_dict = dict()
    error_ways_dict = dict()
    invalid_nodes_json = copy.deepcopy(utild.nodes_json)
    invalid_nodes_json['features'] = []
    invalid_ways_json = copy.deepcopy(utild.ways_json)
    invalid_ways_json['features'] = []
    valid_nodes_json = copy.deepcopy(utild.nodes_json)
    valid_ways_json = copy.deepcopy(utild.ways_json)

    # Nodes - Ways : The remaining nodes should have properties
    diff_nodes = set(utild.nodes_coord_dict.keys()) - set(utild.ways_coord_dict.keys())
    for node in diff_nodes:
        node_id = utild.nodes_coord_dict[node]
        if 'properties' not in utild.nodes_json['features'][node_id].keys() or not len(utild.nodes_json['features'][node_id]['properties']):
            if node_id not in error_nodes_dict.keys():
                error_nodes_dict[node_id] = ["Point properties cannot be empty unless it is part of a way"]

    # Ways - Nodes : Ways containing the remaining nodes are invalid. The nodes should be present in nodes file
    diff_ways = set(utild.ways_coord_dict.keys()) - set(utild.nodes_coord_dict.keys())
    for node in diff_ways:
        for way_id in utild.ways_coord_dict[node]:
            if way_id not in error_ways_dict.keys():
                error_ways_dict[way_id] = [str("Point " + node + " is not present in Nodes file")]
            else:
                error_ways_dict[way_id].append(str("Point " + node + " is not present in Nodes file"))

    for id, msg in sorted(error_nodes_dict.items(), reverse=True):
        valid_nodes_json['features'].pop(id)
        invalid_nodes_json['features'].append(utild.nodes_json['features'][id])
        invalid_nodes_json['features'][-1].update({"fixme": msg})

    for id, msg in sorted(error_ways_dict.items(), reverse=True):
        valid_ways_json['features'].pop(id)
        invalid_ways_json['features'].append(utild.ways_json['features'][id])
        invalid_ways_json['features'][-1].update({"fixme": msg})

    valid_nodes_save_path = os.path.join(cf.writePath,
                                     (ntpath.basename(utild.nodes_file).split('.')[0] + '_valid.geojson'))
    save_file(valid_nodes_save_path, valid_nodes_json)

    invalid_nodes_save_path = os.path.join(cf.writePath,
                                     (ntpath.basename(utild.nodes_file).split('.')[0] + '_invalid.geojson'))
    save_file(invalid_nodes_save_path, invalid_nodes_json)

    valid_ways_save_path = os.path.join(cf.writePath,
                                     (ntpath.basename(utild.ways_file).split('.')[0] + '_valid.geojson'))
    save_file(valid_ways_save_path, valid_ways_json)
    invalid_ways_save_path = os.path.join(cf.writePath,
                                     (ntpath.basename(utild.ways_file).split('.')[0] + '_invalid.geojson'))
    save_file(invalid_ways_save_path, invalid_ways_json)
import numpy as np
import pandas as pd
import json
import matplotlib.pylab as plt
        
def get_ways(features_list):
    '''
    Returns list of list of coordinates.
    Outer list is the element
    Inner list is the coordinates within an element
    '''
    coord_list = []
    filter_sidewalks = False # Set True to include just sidewalks. Otherways all ways are returned
    for elem in features_list:
        if(filter_sidewalks):
            if (elem['properties']['footway'] == 'sidewalk'):
                coord_list.append(elem['geometry']['coordinates'])
        else:
            coord_list.append(elem['geometry']['coordinates'])
    return coord_list

def get_coord_dict(nodes_list, ways_list):
    '''
    Returns dictionary of coordinate
    keys : unique coordinates
    values : all ways to which the coord belongs
    '''
    coord_dict = dict()
    for elem in nodes_list:
        if(str(elem) not in coord_dict.keys()):
            coord_dict[str(elem)] = list()
    
    for id, elem in enumerate(ways_list):
        for point in elem:
            if(str(point) not in coord_dict.keys()):
                coord_dict[str(point)] = [id]
            else:
                coord_dict[str(point)].append(id)
    return coord_dict

def get_coord_df(coord_list):
    '''
    Return df with two columns origin and dest for starting and ending nodes of the way
    This is needed for connected component of networkx package
    '''
    data = {'origin':[], 'dest': []}
    df = pd.DataFrame(data)
    for elem in coord_list:
        df = df.append({'origin':str(elem[0]), 'dest':str(elem[-1])}, ignore_index=True)
    return df

def plot_nodes_vs_ways(coord_list):
    '''
    Plot frequency distribution of #Nodes in each way
    '''
    coord_freq_dict = dict()
    for elem in coord_list:
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

def get_isolated_way_ids(coord_list, coord_dict):
    '''
    Get ways to be discared (ways that are not part of any other ways)
    '''
    disc_way_ids = set()
    for id, elem in enumerate(coord_list):
        ctr = 0
        for point in elem:
            if len(coord_dict[str(point)]) > 1:
                break
            else:
                ctr += 1
        if ctr == len(elem):
            disc_way_ids.update([id])
    return disc_way_ids

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

def split_geojson_file(file):
    '''
    Splits the geojson file based on connectivity with with other ways
    and save into two files :
    1. file_connected.geojson (ways that are connected to atleast one other way)
    2. file_disconnected.geojson (ways that are not connected to any other way)
    ---
    Args : file - .geojson file to be split 
    Returns : None
    '''
    with open(file) as data_json:
        data_dict = json.load(data_json)    
    all_ways = get_ways(data_dict['features'])
    
    coord_dict = get_coord_dict(all_ways)
    disconnected_way_ids = get_isolated_way_ids(all_ways, coord_dict)
    connected_way_ids = set(np.arange(len(all_ways))) - set(disconnected_way_ids)   
    
    connected_ways = data_dict.copy()
    connected_ways['features'] = []
    disconnected_ways = data_dict.copy()
    disconnected_ways['features'] = []
    
    disconnected_ways['features'] = [data_dict['features'][ind] for ind in disconnected_way_ids]
    connected_ways['features'] = [data_dict['features'][ind] for ind in connected_way_ids]
    
    with open(file.split('.')[0] + '_connected.geojson', 'w') as fp:
        json.dump(connected_ways,fp, indent = 4)
    with open(file.split('.')[0] + '_disconnected.geojson', 'w') as fp:
        json.dump(disconnected_ways,fp, indent = 4) 
    # print("Ways in connected.json : {}".format(len(connected_ways['features'])))
    # print("Ways in disconnected.json : {}".format(len(disconnected_ways['features'])))

def get_invalidNodes(node_way_dict, node_json, node_file):
    '''
    A node is invalid if it is not part of any way.
    Dump the invalid nodes into a {filename}_invalid.geojson
    '''
    vals = np.array(list(node_way_dict.values()))            
    invalid_nodes = [ind for ind, val in enumerate(vals) if len(val) == 0]
    invalid_nodes_json = node_json.copy()
    invalid_nodes_json['features'] = []
    [invalid_nodes_json['features'].append(node_json['features'][ind]) for ind in invalid_nodes]
    with open(node_file.split('.')[0] + '_invalid.geojson', 'w') as fp:
        json.dump(invalid_nodes_json,fp, indent = 4) 
    print('Invalid Nodes dumped to {}'.format(node_file.split('.')[0] + '_invalid.geojson'))

def geometry_type_validation(file):
    '''
    Geojson Geometry type validations : https://tools.ietf.org/html/rfc7946#section-3.1.4
    Gets number of linestrings that has just one node
    '''
    with open(file) as data_json:
        data_dict = json.load(data_json)
    Ways = get_ways(data_dict['features'])
    Ways = np.array(Ways)
    one_node_ls_ids = []
    [one_node_ls_ids.append(ind) for ind, way in enumerate(Ways) if len(way) == 1]
    # print(len(Ways[one_node_ls_ids]))
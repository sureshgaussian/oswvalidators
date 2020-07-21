import numpy as np
import os
import pandas as pd
import json
from glob import glob
import matplotlib.pylab as plt
import networkx as nx
import pickle


'''
0 [ [1, 2], [2, 3]]
1 [ [1, 2], [2, 4]]
2 [ [1, 3], [2, 5]]
3 [ [1, 4], [2, 6]]
'''
        
def get_ways(features_list):
    '''
    Returns list of list of coordinates.
    Outer list is the element
    Inner list is the coordinates within an element
    '''
    coord_list = []
    for elem in features_list:
        if(elem['properties']['footway'] == 'sidewalk'):
            coord_list.append(elem['geometry']['coordinates'])
    return coord_list

def get_coord_dict(coord_list):
    '''
    Returns dictionary of coordinate
    keys : unique coordinates
    values : all ways to which the coord belongs
    '''
    coord_dict = dict()
    for id, elem in enumerate(coord_list):
        for point in elem:
            if(str(point) not in coord_dict.keys()):
                coord_dict[str(point)] = [id]
            else:
                coord_dict[str(point)].append(id)
    return coord_dict

def get_coord_df(coord_list):
    '''
    Return df with two columns: origin and dest
    ******** Note to Rakesh : This to be used for connected components in networkx
    '''
    data = {'origin':[], 'dest': []}
    df = pd.DataFrame(data)
    for elem in coord_list:
        # df = df.append([str(elem[0]), str(elem[-1])])
        df = df.append({'origin':str(elem[0]), 'dest':str(elem[-1])}, ignore_index=True)
    return df

def plot_nodes_vs_ways(coord_list):
    '''
    #Nodes vs #Ways
    '''
    coord_freq_dict = dict()
    for elem in coord_list:
        if(len(elem) not in coord_freq_dict.keys()):
            coord_freq_dict[str(len(elem))] = 1
        else:
            coord_freq_dict[str(len(elem))] += 1
    x, y = zip(sorted(*coord_freq_dict.items()))
    # print(x)
    plt.plot(x, y)
    plt.show()

def get_isolated_way_ids(coord_list, coord_dict):
    '''
    Get way IDs to be discared (ways that are not part of any other ways)
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
    
    disconnected_ways['features'] = [data_dict['features'][ind] for ind in isolated_way_ids]
    connected_ways['features'] = [data_dict['features'][ind] for ind in connected_way_ids]
    
    with open(file.split('.')[0] + '_connected.geojson', 'w') as fp:
        json.dump(connected_ways,fp, indent = 4)
    with open(file.split('.')[0] + '_disconnected.geojson', 'w') as fp:
        json.dump(disconnected_ways,fp, indent = 4) 
    # print("Ways in connected.json : {}".format(len(connected_ways['features'])))
    # print("Ways in disconnected.json : {}".format(len(disconnected_ways['features'])))


if __name__ == '__main__':
    path = "E:\oswvalidators\OSW\TestData"
#     path = "E:\MAGDEBURG\SURESH\OSW\OSW\TestData" # Change the path here to a relative one in the git folder structure
    os.chdir(path)
    json_files = glob("*.geojson")
    json_files = [i for i in json_files if 'redmond.' in i]
    print("Number of json files :", len(json_files))
    
    for ind, file in enumerate(json_files):
        print('-'*10)
        print('Processing File : {}'.format(file))
        with open(file) as data_json:
            data_dict = json.load(data_json)
    
        Ways = get_ways(data_dict['features'])
        
        coord_dict = get_coord_dict(Ways)
        # print("Coordinates Dictionary : \n", coord_dict)
        
        df = get_coord_df(Ways)
#         print("DataFrame : \n{}".format(df))
        print("list : {} and df : {}".format(len(Ways), len(df.index)))
        
        isolated_way_ids = get_isolated_way_ids(Ways, coord_dict)
        
        split_geojson_file(file)
        
#         print(coord_dict.items())  
        Connected_Ways = Ways.copy()
        for x in sorted(isolated_way_ids, reverse = True):  
            del Connected_Ways[x] 
    
        #printing modified list
        print("Number of ways (sidewalks) in the file : ", len(Ways))
        print("Number of isolated ways: ", len(isolated_way_ids))
        print("Number of Connected ways in the file : ", len(Connected_Ways))
        
        
        Connected_df = get_coord_df(Connected_Ways)
        Connected_FG = nx.from_pandas_edgelist(Connected_df, source='origin', target='dest')
        print("Is Connected ? : ", nx.is_connected(Connected_FG))
        print("Number of Connected Components : ", nx.number_connected_components(Connected_FG))
            
        cc = nx.connected_components(Connected_FG)
        # for ind, x in enumerate(cc):
        #     print('\n',ind,":", x)
            
        S = [Connected_FG.subgraph(c).copy() for c in nx.connected_components(Connected_FG)]
                

        pickle.dump(S, open('S.pkl', 'wb'))
        S = pickle.load(open('S.pkl', 'rb'))
        
        pickle.dump(Connected_df, open('Connected_df.pkl', 'wb'))
        Connected_df = pickle.load(open('Connected_df.pkl', 'rb'))
        
        pickle.dump(df, open('ways_df.pkl', 'wb'))
        df = pickle.load(open('ways_df.pkl', 'rb'))
                
        
        print(len(S))
        print(S[1].edges)
        nx.draw_networkx(S[1])
        
        sgraph = S[1]
        ways_set = get_way_from_subgraph(S[1], df)
        print("sgraph_ways {}".format(ways_set))
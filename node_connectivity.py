



import numpy as np
import os
import pandas as pd
import json
from glob import glob



'''
0 [ [1, 2], [2, 3]]
1 [ [1, 2], [2, 4]]
2 [ [1, 3], [2, 5]]
3 [ [1, 4], [2, 6]]
'''


def get_coord_list(features_list):
    '''
    Returns list of list of coordinates.
    Outer list is the element
    Inner list is the coordinates within an element
    '''
    coord_list = []
    for elem in features_list:
        coord_list.append(elem['geometry']['coordinates'])
    return coord_list

def get_coord_dict(coord_list):
    '''
    Returns dictionary of coordinate
    keys : unique coordinates
    values : ways to which the coord belongs
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

def get_disc_way_ids(coord_list, coord_dict):
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

if __name__ == '__main__':
    path = "E:\oswvalidators\OSW\TestData"
    os.chdir(path)
    json_files = glob("*.geojson")
    print("Number of json files :", len(json_files))
    print(json_files)
    
    json_files = [i for i in json_files if 'redmon_test' in i]
    print(json_files)    
    
    
    for ind, file in enumerate(json_files):
        print('-'*10)
        print('File Name : {}'.format(file))
        with open(file) as data_json:
            data_dict = json.load(data_json)
    
        coord_list = get_coord_list(data_dict['features'])
        print(len(coord_list))
        coord_dict = get_coord_dict(coord_list)
        print(coord_dict)
        
        df = get_coord_df(coord_list)
        print("DataFrame : \n{}".format(df))
        
        disc_way_ids = get_disc_way_ids(coord_list, coord_dict)
        # print(coord_dict.items())  
        print(disc_way_ids)
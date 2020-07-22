# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 16:07:46 2020

@author: Karthik
"""
import json
from shapely.geometry import LineString
from shapely.geometry import Point

def getGeomertyType(way):
    '''
    Returns the type of way

    Parameters
    ----------
    way : TYPE
        GeoJson file with a way extracted.
        eg) dataDict["features"][itemNumber or wayNumber]

    Returns
    -------
    TYPE
        way.

    '''
    return way["geometry"]["type"]



def isValidGeometryType(way):
    '''
    checks if the Geomerty is valid according to the tag in way

    Parameters
    ----------
    way : TYPE
        GeoJson file with a way extracted.
        eg) dataDict["features"][itemNumber or wayNumber].

    Returns
    -------
    bool

    '''
    
    wayType = getGeomertyType(way)
    if(wayType == "LineString"):
        try:
            LineString(way["geometry"]["coordinates"])
            return True
        except:
            # print("invalid way ",way)
            return False

    if(wayType == "Point"):
        try:
            Point(way["geometry"]["coordinates"])
            print("point")
            return True
        except:
            print("invalid way ",way)

def readJsonFile(path):
    '''
    To read Jsonfile with the given path

    Parameters
    ----------
    path : TYPE
        path of the json file.

    Returns
    -------
    dataDict : TYPE
        Json file.

    '''
    with open(path,'r') as data_json:
        dataDict = json.load(data_json)
        return dataDict
    

def intersectLineStringInValidFormat(dataDict,skipTag):
    '''
    
    Returns the LineStrings which are intersecting but doesnt have a intersecting,
    Point between them. If Brunnel field isnt null/none, we dont consider it as a intersection.

    Parameters
    ----------
    dataDict : TYPE
        Dictionary which chich contains GeoJson file

    Returns
    -------
    dictToJson : Dictionary
        Returns the LineStrings which are intersecting but doesnt have a intersecting,
        Point between them. If Brunnel field isnt null/none, we dont consider it as a intersection.

    '''
    
    dictToJsonID = {}
    dictInvalidFormatID = {}

    dictSize = len(dataDict["features"])
    for iteratorI in range(dictSize):
        brunnel = dataDict["features"][iteratorI]["properties"][skipTag]
        if(brunnel != None):
            continue
        try:
            wayI = LineString(dataDict["features"][iteratorI]["geometry"]["coordinates"])
        except:
            # print("invalid way",dataDict["features"][iteratorI])
            dictInvalidFormatID[iteratorI] = iteratorI
            continue
        
        beginJ = iteratorI+1
        for iteratorJ in range(beginJ,dictSize,1):
            # Not implemented due to execution speed.
            # if(isValidGeometryType(dataDict["features"][iteratorJ])==False):
            #     continue
            try:
                wayJ = LineString(dataDict["features"][iteratorJ]["geometry"]["coordinates"])
            except:
                continue
           
            if(wayI.intersects(wayJ)):
                if(wayI.touches(wayJ)!=True):
                    intersection = wayI.intersection(wayJ)
                    if(str(intersection) in dictToJsonID):
                        dictToJsonID[str(intersection)].append({"way"+str(iteratorI):iteratorI,"way"+str(iteratorJ):iteratorJ})
                    else:
                        dictToJsonID[str(intersection)] = {"way"+str(iteratorI):iteratorI,"way"+str(iteratorJ):iteratorJ}

    return dictToJsonID,dictInvalidFormatID
                
                
def jsonWrite(path,invalidWays):
    with open(path.split('.')[0] + '.geojson', 'w') as fp:
        json.dump(invalidWays,fp, indent = 4)
    
if __name__ == '__main__':
    path = "D:/project/oswvalidators/OSW/TestData/redmond.geojson"
    dataDict = readJsonFile(path)
    invalidWays,dictInvalidFormatID = intersectLineStringInValidFormat(dataDict,"brunnel")
    pathWrite = "D:/project/oswvalidators/OSW/TestData/invalidWays.geojson"
    pathWriteInvalidFormat = "D:/project/oswvalidators/OSW/TestData/InvalidFormat.geojson"

    jsonWrite(pathWrite, invalidWays)
    jsonWrite(pathWriteInvalidFormat, dictInvalidFormatID)
    
    
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 16:07:46 2020

@author: Karthik
"""
import json
from shapely.geometry import LineString
from shapely.geometry import Point
import os
def getGeometryType(way):
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
    checks if the Geomerty is valid according to the geometric tag in way

    Parameters
    ----------
    way : TYPE
        GeoJson file with a way extracted.
        eg) dataDict["features"][itemNumber or wayNumber].

    Returns
    -------
    bool

    '''
    
    wayType = getGeometryType(way)
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
        
    skipTag : Type
        Tog to skip checking the validation. Example brunnel

    Returns
    -------
    dictToJson : Dictionary
        Returns the LineStrings which are intersecting but doesnt have a intersecting,
        Point between them. If Brunnel field isnt null/none, we dont consider it as a intersection.
    dictInvalidFormatID : List
        Returns the ID for the ways with invalid dataformat
    violatingWayFeatures : Dictionary
        

    '''
    
    dictToJsonID = {}
    dictInvalidFormatID = []
    violatingWayFeatures = []
    dictSize = len(dataDict["features"])
    for iteratorI in range(dictSize):
        brunnel = dataDict["features"][iteratorI]["properties"][skipTag]
        if(brunnel != None):
            continue
        singleWayI = dataDict["features"][iteratorI]["geometry"]["coordinates"]

        try:
            wayI = LineString(singleWayI)
        except:
            dictInvalidFormatID.append(iteratorI)
            continue
        
        beginJ = iteratorI+1
        for iteratorJ in range(beginJ,dictSize,1):
            # Not implemented due to execution speed.
            # if(isValidGeometryType(dataDict["features"][iteratorJ])==False):
            #     continue
            singleWayJ = dataDict["features"][iteratorJ]["geometry"]["coordinates"]
            brunnel = dataDict["features"][iteratorJ]["properties"][skipTag]
            if(brunnel != None):
                continue
            try:
                wayJ = LineString(singleWayJ)
            except:
                continue
           
            if(wayI.intersects(wayJ)):
                if(wayI.touches(wayJ)!=True):
                    intersection = wayI.intersection(wayJ)
                    if(str(intersection) in dictToJsonID):
                        dictToJsonID[str(intersection)].append([iteratorI,iteratorJ])                
                    else:
                        dictToJsonID[str(intersection)] = [iteratorI,iteratorJ]
                        
                    # for creating the violating way features appending to dictionary based on dictionary size
                    if(len(violatingWayFeatures)==0):
                        violatingWayFeatures=[dataDict["features"][iteratorI]]
                        violatingWayFeatures.append(dataDict["features"][iteratorJ])

                    else:
                        violatingWayFeatures.append(dataDict["features"][iteratorI])
                        violatingWayFeatures.append(dataDict["features"][iteratorJ])

                        
    return dictToJsonID,dictInvalidFormatID,violatingWayFeatures
                
                
def geojsonWrite(path,invalidWays,originalGeoJsonFile):
    '''
    To write the given invalid ways in the GeoJson format

    Parameters
    ----------
    path : TYPE
        path to write the json file.
    invalidWays : TYPE
        list of invalid paths with its attributes.
    originalGeoJsonFile : TYPE
        actutal json file given for validation.

    Returns
    -------
    None.

    '''
    invalidPaths = originalGeoJsonFile.copy()
    invalidPaths['features'] = invalidWays
    with open(path.split('.')[0] + '.geojson', 'w') as fp:
        json.dump(invalidPaths,fp, indent = 4)
    
                
def jsonWrite(path,invalidWays):
    '''
    To write dictionary to json format

    Parameters
    ----------
    path : TYPE
        path for the json write.
    invalidWays : TYPE
        Invalid ways to write.

    Returns
    -------
    None.

    '''
    with open(path.split('.')[0] + '.json', 'w') as fp:
        json.dump(invalidWays,fp, indent = 4)
        
if __name__ == '__main__':
    pathTest = os.path.join(os.getcwd(), "OSW\TestData")
    os.chdir(pathTest)
    path = pathTest + "\redmond.geojson"
    dataDict = readJsonFile(path)
    invalidWaysID,dictInvalidFormatID,violatingWayFeatures = intersectLineStringInValidFormat(dataDict,"brunnel")
    pathWrite = pathTest + "\invalidWays.geojson"
    pathWriteInvalidFormat = pathTest + "\InvalidFormat.geojson"
    invalidGeoJsonIntersection = pathTest+ "\invalidGeoJsonIntersection.geojson"

    jsonWrite(pathWrite, invalidWaysID)
    jsonWrite(pathWriteInvalidFormat, dictInvalidFormatID)
    geojsonWrite(invalidGeoJsonIntersection, violatingWayFeatures, dataDict)
    
    # path = "D:/project/oswvalidators/OSW/TestData/redmond.geojson"
    # dataDict = readJsonFile(path)
    # invalidWaysID,dictInvalidFormatID,violatingWayFeatures = intersectLineStringInValidFormat(dataDict,"brunnel")
    # pathWrite = "D:/project/oswvalidators/OSW/TestData/invalidWays.geojson"
    # pathWriteInvalidFormat = "D:/project/oswvalidators/OSW/TestData/InvalidFormat.geojson"
    # invalidGeoJsonIntersection = "D:/project/oswvalidators/OSW/TestData/invalidGeoJsonIntersection.geojson"

    # jsonWrite(pathWrite, invalidWaysID)
    # jsonWrite(pathWriteInvalidFormat, dictInvalidFormatID)
    # geojsonWrite(invalidGeoJsonIntersection, violatingWayFeatures, dataDict)
    
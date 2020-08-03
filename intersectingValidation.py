import json
import pandas as pd
from shapely.geometry import LineString, Point, Polygon, MultiPoint


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
    with open(path, 'r') as data_json:
        dataDict = json.load(data_json)
        return dataDict


def geometryFormat(geometryDatarow):
    if (geometryDatarow[0]["type"] == "LineString"):
        try:
            return LineString(geometryDatarow[0]["coordinates"])
        except:
            return "invalid"
    if (geometryDatarow[0]["type"] == "Point"):
        try:
            return Point(geometryDatarow[0]["coordinates"])
        except:
            return "invalid"
    if (geometryDatarow[0]["type"] == "Polygon"):
        try:
            return Polygon(geometryDatarow[0]["coordinates"])
        except:
            return "invalid"


def indexInvalidGeometryType(geometryData):
    dataInvalidGeoJsonFormat = geometryData.apply(geometryFormat, axis=1)
    ind_drop = dataInvalidGeoJsonFormat[dataInvalidGeoJsonFormat.apply(lambda row: row == 'invalid')].index

    return ind_drop


def brunnelcheck(x, skipTag):
    if (x[0]["brunnel"] == None):
        return False
    else:
        return True


def geojsonWrite(path, invalidWays, originalGeoJsonFile):
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
        json.dump(invalidPaths, fp, indent=4)


def intersectLineStringInValidFormat(geoJSONdata, skipTag):
    featuresData = pd.DataFrame(geoJSONdata["features"])
    geometryData = pd.DataFrame(featuresData["geometry"])
    propertyData = pd.DataFrame(featuresData["properties"])
    invalidWayGeoJSONFormat = []
    intersectingNodeGeoJSON = []
    violatingWayFeatures = []

    brunnelValid = pd.DataFrame(propertyData.apply(brunnelcheck, args=(skipTag,), axis=1))
    invalidGeometryIndex = indexInvalidGeometryType(geometryData).values.tolist()
    for counter in range(len(geoJSONdata["features"])):
        if counter in invalidGeometryIndex:
            invalidWayGeoJSONFormat.append(geoJSONdata["features"][counter])

    brunnelExist = brunnelValid[brunnelValid[0].apply(lambda row: row == True)].index
    geometryDataFormat = geometryData.apply(geometryFormat, axis=1)
    geometryDataFormatCopy = geometryDataFormat.copy()

    for rowIdI, wayI in geometryDataFormat.iteritems():
        if (rowIdI == len(geometryDataFormat) / 2):
            print("half way through... please wait")

        if (wayI == "invalid" or rowIdI in brunnelExist):
            continue
        for rowIdJ, wayJ in geometryDataFormatCopy.iteritems():
            if (rowIdI >= rowIdJ or wayJ == "invalid" or rowIdJ in brunnelExist):
                continue
            if (wayI.intersects(wayJ) and wayI.touches(wayJ) != True):
                intersection = wayI.intersection(wayJ)
                if (type(intersection) == type(LineString())):
                    continue
                elif type(intersection) == type(Point()):
                    roundedIntersection = tuple(round(dimension, 7) for dimension in intersection.coords[0])
                    if (roundedIntersection in wayI.coords[:]) or (roundedIntersection in wayJ.coords[:]):
                        continue
                    intersectingNodeGeoJSON.append(
                        {"type": "Feature", "geometry": {"type": "Point", "coordinates": roundedIntersection}})

                elif (type(intersection) == type(MultiPoint())):
                    appendPoints = []
                    for point in intersection:
                        roundedIntersection = tuple(round(dimension, 7) for dimension in point.coords[0])
                        if (roundedIntersection in wayI.coords[:]) or (roundedIntersection in wayJ.coords[:]):
                            continue
                        appendPoints.append(roundedIntersection)

                    if (len(appendPoints) > 1):
                        intersectingNodeGeoJSON.append(
                            {"type": "Feature", "geometry": {"type": "MultiPoint", "coordinates": appendPoints}})
                    else:
                        intersectingNodeGeoJSON.append(
                            {"type": "Feature", "geometry": {"type": "Point", "coordinates": appendPoints[0]}})

                else:
                    print("Invalid format Support not given yet")
                    exit(0)

                if (len(violatingWayFeatures) == 0):
                    violatingWayFeatures = [geoJSONdata["features"][rowIdI]]
                    violatingWayFeatures.append(geoJSONdata["features"][rowIdJ])

                else:
                    violatingWayFeatures.append(geoJSONdata["features"][rowIdI])
                    violatingWayFeatures.append(geoJSONdata["features"][rowIdJ])

    return intersectingNodeGeoJSON, invalidWayGeoJSONFormat, violatingWayFeatures

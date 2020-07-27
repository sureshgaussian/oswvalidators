import argparse as ag
import os
from intersectingValidation import readJsonFile,intersectLineStringInValidFormat,jsonWrite,geojsonWrite

if __name__ == '__main__':

    parser = ag.ArgumentParser()
    parser.add_argument("--GeoJSON", help="GeoJSON filepath absolute path ")
    parser.add_argument("--validation", help="type of validation")
    parser.add_argument("--writePath",help="output directory to write the validation errors")
    args = parser.parse_args()
    path = args.GeoJSON
    outputDirectory = args.writePath

    if(args.validation=="intersectingvalidation"):
        dataDict = readJsonFile(path)
        invalidWaysID, dictInvalidFormatID, violatingWayFeatures = intersectLineStringInValidFormat(dataDict, "brunnel")
        pathWrite = outputDirectory + "/invalidWays.geojson"
        pathWriteInvalidFormat = outputDirectory + "/InvalidFormat.geojson"
        invalidGeoJsonIntersection = outputDirectory + "/invalidGeoJsonIntersection.geojson"

        jsonWrite(pathWrite, invalidWaysID)
        jsonWrite(pathWriteInvalidFormat, dictInvalidFormatID)
        geojsonWrite(invalidGeoJsonIntersection, violatingWayFeatures, dataDict)
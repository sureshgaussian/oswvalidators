import json

with open('TestData/Test10/bellevue3.geojson') as json_file:
    data = json.load(json_file)

nodeFile = dict()
nodeFile["type"] = "FeatureCollection"
nodeFile["features"] = list()

waysFile = dict()
waysFile["type"] = "FeatureCollection"
waysFile["features"] = list()

for feature in data['features']:
    id = feature['id']
    idType = id.split('/')
    if idType[0] == 'node':
        nodeFile["features"].append(feature)
    else:
        waysFile["features"].append(feature)

with open('TestData/Test10/input/bellevue3_node.geojson', 'w') as f:
    json.dump(nodeFile, f)

with open('TestData/Test10/input/bellevue3_ways.geojson', 'w') as f:
    json.dump(waysFile, f)

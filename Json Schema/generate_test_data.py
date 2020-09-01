# get the required imports
import pandas as pd
import random
import json
import argparse

def build_dictionary(df, Tags):
    Dictionary = {}
    for index, row in df.iterrows():
        Tags_values = []
        for column in df.columns:
            if not (pd.isna(row[column])):
                Tags_values.append(row[column])
        Dictionary.update({Tags[index] : Tags_values})
    Dictionary.update({"troubles" : ['rakesh', 'ravi' , 'karthik']})
    return Dictionary

def generate_coordinates(num_entries):
	Coordinates = []
	
	for i in range(0,num_entries):
		longitude = round(random.uniform(-180.0,180.0),7)
		latitude = round(random.uniform(-90.0,90.0),7)
		coord = '[' + str(longitude) + ',' + str(latitude) + ']'
		Coordinates.append(coord)
	return Coordinates


def generate_test_nodes(num_entries, Dictionary, Coordinates):
	i = 1
	header_string = '{"type": "FeatureCollection","features": ['
	Tags = []
	for keys in Dictionary.keys():
		Tags.append(keys)
	while i <= num_entries:
		test_string = '\n' + '{"type": "Feature", "geometry": {"type": "Point", "coordinates": ' + random.choice(Coordinates) + '},'
		test_string = test_string + ' "properties": {"id": "node' + str(i) + '"}},'
		i = i + 1
		header_string = header_string + test_string
	
	#header_string = header_string[0:len(header_string)-1]	
	i = 1
	while i <= num_entries:
		test_string = '\n' + '{"type": "Feature", "geometry": {"type": "Point", "coordinates": ' + random.choice(Coordinates) + '},'
		test_string = test_string + ' "properties": {"id": "node' + str(num_entries+i) + '",'
		tag = random.choice(Tags)
		values = Dictionary[tag]
		value = random.choice(values)
		test_string = test_string + '"' + tag + '":' + (str(value) if str(value).isnumeric() else '"' + value + '"') + '}},'
		header_string = header_string + test_string
		i = i + 1
	header_string = header_string[0:len(header_string)-1] + '\n]}'
	return header_string
	

def generate_test_ways(num_entries, Dictionary, Coordinates):
	i = 1
	header_string = '{"type": "FeatureCollection","features": ['
	Tags = []
	for keys in Dictionary.keys():
		Tags.append(keys)
	while i <= num_entries:
		test_string = '\n' + '{"type": "Feature","geometry": {"type": "LineString", "coordinates": ['
		# Assign a random number of coordinates to the way
		for j in range(2,random.randint(3,10)):
			test_string = test_string + random.choice(Coordinates) + ','
		
		test_string = test_string[0:len(test_string)-1] + ']}, "properties": {"id": "way' + str(i) + '", '
		
		for x in range(1,4):
			tag = random.choice(Tags)
			values = Dictionary[tag]
			value = random.choice(values)

			test_string = test_string + '"' + tag + '": ' + (str(value) if str(value).isnumeric() else '"' + value + '"') + ', '
        
		test_string = test_string[0:len(test_string)-2] + '}},'
		header_string = header_string + test_string
		i = i + 1
    
	header_string = header_string[0:len(header_string)-1] + '\n]}'
	return header_string

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Run Pipeline')
	#parser.add_argument('--generate', help="Nodes: Generate Test nodes, \n Ways: Generate Test Ways",type=str, required=True)
	parser.add_argument('--number', help="Number of nodes / ways to generate", type=int, required=True)
	args = parser.parse_args()
    
	print("Reading the input file")
	df = pd.read_excel('OSW_Tags.xlsx',sheet_name='Tags') # read the file into a dataframe
	
	Pointsdf = df[df['Geometry']=='Point'] 
	Pointsdf.reset_index(drop=True, inplace=True) # reset the index for future use
	
	Linesdf = df[df['Geometry']=='LineString'] 
	Linesdf.reset_index(drop=True, inplace=True) # reset the index for future use
	
	Coordinates = generate_coordinates(args.number*3) # Generate a list of input*3 coordinates to pick from
	
	Point_Tags = Pointsdf.Tag.values.tolist()
	Pointsdf.drop(columns=['Tag','type', 'Geometry'], inplace=True)
	Line_Tags = Linesdf.Tag.values.tolist()
	Linesdf.drop(columns=['Tag','type','Geometry'], inplace=True)
	
	PointsDictionary = build_dictionary(Pointsdf, Point_Tags)
	PointsDictionary.update(timing = [1,2,3,4,5,6,7,8])
	LinesDictionary = build_dictionary(Linesdf, Line_Tags)
	LinesDictionary.update(length = [i for i in range(0,100)])
	LinesDictionary.update(incline = [i for i in range(0,10)])
	LinesDictionary.update(width = [i for i in range(0,100)])
	
	Nodes = generate_test_nodes(args.number, PointsDictionary, Coordinates)
	Ways = generate_test_ways(args.number, LinesDictionary, Coordinates)
	
	if json.loads(Nodes):
		print('Generated Nodes Successfully \n')
		Nodes_file = open("Sample_nodes.json", "w")
		Nodes_file.write(Nodes)
		Nodes_file.close()
	else:
		print('Error Generating Nodes data')
	
	#print(Ways)
	if json.loads(Ways):
		print('Generated Ways Successfully \n')
		Ways_file = open("Sample_ways.json", "w")
		Ways_file.write(Ways)
		Ways_file.close()
	else:
		print('Error Generating Nodes data')
	
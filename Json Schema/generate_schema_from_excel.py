# get the required imports
import pandas as pd
import json
import warnings
warnings.filterwarnings("ignore")

def build_properties(tags, types, df):
	integer_types = ''
	string_types = ''
	
	for index, row in df.iterrows():
		if types[index] == 'integer' or types[index] == 'number':
			i = 0
			int_string = '"' + tags[index] + '": {"type":"' + types[index] + '"'
			for column in df.columns:
				if not (pd.isna(row[column])):
					if i==0:
						int_string = int_string + ',"minimum" :' + str(row[column])
					if i==1:
						int_string = int_string + ',"maximum":' + str(row[column])
					i = i + 1
			int_string = int_string + '}'
			integer_types = integer_types + int_string + ','
			
		if types[index] == 'string':
			string_enum = '"' + tags[index] + '": {"type":"string","enum":['
			for column in df.columns:
				if not (pd.isna(row[column])):
					string_enum = string_enum + '"' + row[column] + '",'
			string_enum = string_enum[0:len(string_enum)-1] + ']}'
			string_types = string_types + string_enum + ','

	properties_string = integer_types + string_types[0:len(string_types)-1]
	return properties_string


def build_dependecies(dependencies):

	children = dependencies["Tag"].values.tolist()
	dependencies.drop(columns=['Tag'], inplace=True)
	dependency_string = ''
	for index, row in dependencies.iterrows():
		dp_string = '"' + children[index] + '": {"anyOf": ['
		for column in dependencies.columns:
			if not (pd.isna(row[column])):
				parent_key = row[column].split('=')[0]
				parent_value = row[column].split('=')[1]
				child_string = '{"required": ["' + parent_key + '"], "properties":{'
				child_string = child_string + '"' + parent_key + '": {"type": "string", "const" : "' + parent_value + '"}}},'
		dependency_string = dependency_string + dp_string + child_string[0:len(child_string)-1] + ']},'
		
	dependency_string = dependency_string[0:len(dependency_string)-1]

	return dependency_string

def generate_nodes_schema(tags, types, df, dependencies):
	
	print("Generating Nodes Schema")
	point_properties = build_properties(tags, types, df)
	point_dependencies = build_dependecies(dependencies)
	
	nodes_schema_string = '''{
  "title": "root",
  "type": "object",
  "required": 
  [
    "type",
    "features"
  ],
  "additionalProperties": false,
  "properties": 
  {
    "type": 
    {
      "title": "Feature Collection",
      "type": "string",
      "default": "FeatureCollection",
      "enum": ["FeatureCollection"]
    },
    "features": 
    {
      "title": "features array",
      "type": "array",
      "minItems": 1,
      "additionalItems": false,
      "items": 
      {
        "title": "FeatureObject",
        "type": "object",
        "required": ["type","geometry"],
        "additionalProperties": false,
        "properties": 
        {
          "type": 
          {
            "title": "FeatureType",
            "type": "string",
            "default": "Feature",
            "enum": ["Feature"]
          },
          "geometry": 
          {
            "title": "geometryObject",
            "type": "object",
            "required": ["type","coordinates"],
            "additionalProperties": false,
            "properties": 
            {
              "type": 
              {
                "title": "GeometryType",
                "type": "string",
                "default": "Point",
                "enum": ["Point"]
              },
              "coordinates": 
              {
                "title": "coordinates",
                "type": "array",
                 "minItems": 2,
                 "maxItems": 2,
      			"additionalItems": false,
                "items": [
                {
                  "type": "number",
				  "minimum": -180.0,
				  "maximum": 180.0
                },
				{
                  "type": "number",
				  "minimum": -90.0,
				  "maximum": 90.0
                }]
               }
            }
          },
          "properties":
          {
            "title": "propertiesObject",
            "type": "object",
            "additionalProperties": false,
            "properties": {"id": {"type": "string"},''' + point_properties + '''},
			"dependencies": {''' + point_dependencies + '''}
          }
        }
      }
    }
  }
}'''

	return nodes_schema_string
	

def generate_ways_schema(tags, types, df, dependencies):
	
	print("Generating Ways Schema")
	line_properties = build_properties(tags, types, df)
	line_dependencies = build_dependecies(dependencies)

	
	ways_schema_string = '''{
  "title": "root",
  "type": "object",
  "required": 
  [
    "type",
    "features"
  ],
  "additionalProperties": false,
  "properties": 
  {
    "type": 
    {
      "title": "Feature Collection",
      "type": "string",
      "default": "FeatureCollection",
      "enum": ["FeatureCollection"]
    },
    "features": 
    {
      "title": "features array",
      "type": "array",
      "minItems": 1,
      "additionalItems": false,
      "items": 
      {
        "title": "FeatureObject",
        "type": "object",
        "required": ["type","geometry"],
        "additionalProperties": false,
        "properties": 
        {
          "type": 
          {
            "title": "FeatureType",
            "type": "string",
            "default": "Feature",
            "enum": ["Feature"]
          },
          "geometry": 
          {
            "title": "geometryObject",
            "type": "object",
            "required": ["type","coordinates"],
            "additionalProperties": false,
            "properties": 
            {
              "type": 
              {
                "title": "GeometryType",
                "type": "string",
                "default": "LineString",
                "enum": ["LineString"]
              },
              "coordinates": 
              {
                "title": "coordinates",
                "type": "array",
                 "minItems": 2,
                "items": [
                {
				  "type": "array",
				  "additionalItems": false,
				  "items": [
				  {
					  "type": "number",
					  "minimum": -180.0,
					  "maximum": 180.0
				  },
				  {
                  "type": "number",
				  "minimum": -90.0,
				  "maximum": 90.0
                }]}]
               }
            }
          },
          "properties":
          {
            "title": "propertiesObject",
            "type": "object",
            "additionalProperties": false,
            "properties":  {"id": {"type": "string"},''' + line_properties + '''},
			"dependencies": {''' + line_dependencies + '''}
          }
        }
      }
    }
  }
}'''

	return ways_schema_string
	
	
if __name__ == '__main__':
	print("Reading the Excel file")
	df = pd.read_excel('OSW_Tags.xlsx', sheet_name='Tags') 
	dependencies = pd.read_excel('OSW_Tags.xlsx', sheet_name='Parents')
	
	# Remove all those lines which do not have a dependency
	dependencies = dependencies[dependencies['Prereqs'] != 'None']
	#dependencies['Tag'] = [dependencies['Prereqs'].str.split('=').values[i][0] for i in range(dependencies.shape[0])]
	dependencies.rename(columns = {'Tags':'Tag'}, inplace = True) 

	pointsdf = df[df['Geometry'] == 'Point'].sort_values(by=['type'])
	pointsdf.reset_index(drop=True, inplace=True) # reset the index for future use
	
	linesdf = df[df['Geometry'] == 'LineString'].sort_values(by=['type'])
	linesdf.reset_index(drop=True, inplace=True) # reset the index for future use
	
	point_tags = pointsdf.Tag.values.tolist()
	point_types = pointsdf.type.values.tolist()
	pointsdp = pd.merge(pointsdf.Tag, dependencies, on='Tag', how='inner')
	pointsdf.drop(columns=['Tag','Geometry', 'type'], inplace=True)
	
	line_tags = linesdf.Tag.values.tolist()
	line_types = linesdf.type.values.tolist()
	linesdp = pd.merge(linesdf.Tag, dependencies, on='Tag', how='inner')
	linesdf.drop(columns=['Tag','Geometry', 'type'], inplace=True)
	
	nodes_schema = generate_ways_schema(point_tags, point_types, pointsdf, pointsdp)
	ways_schema = generate_ways_schema(line_tags, line_types, linesdf, linesdp)
	
	if json.loads(nodes_schema):
		print('Generated Nodes schema Successfully \n')
		nodes_file = open("Nodes_schema.json", "w")
		nodes_file.write(nodes_schema)
		nodes_file.close()
	else:
		print('Error Generating Nodes Schema')
	
	if json.loads(ways_schema):
		print('Generated Ways schema Successfully \n')
		ways_file = open("Ways_schema.json", "w")
		ways_file.write(ways_schema)
		ways_file.close()
	else:
		print('Error Generating Ways Schema')
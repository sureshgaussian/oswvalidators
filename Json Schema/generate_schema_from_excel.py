# get the required imports
import pandas as pd
import json
import warnings
warnings.filterwarnings("ignore")

def build_properties(Tags, Types, df):
	integer_types = ''
	string_types = ''
	
	for index, row in df.iterrows():
		if Types[index] == 'integer' or Types[index] == 'number':
			i = 0
			int_string = '"' + Tags[index] + '": {"type":"' + Types[index] + '"'
			for column in df.columns:
				if not (pd.isna(row[column])):
					if i==0:
						int_string = int_string + ',"minimum" :' + str(row[column])
					if i==1:
						int_string = int_string + ',"maximum":' + str(row[column])
					i = i + 1
			int_string = int_string + '}'
			integer_types = integer_types + int_string + ','
			
		if Types[index] == 'string':
			string_enum = '"' + Tags[index] + '": {"type":"string","enum":['
			for column in df.columns:
				if not (pd.isna(row[column])):
					string_enum = string_enum + '"' + row[column] + '",'
			string_enum = string_enum[0:len(string_enum)-1] + ']}'
			string_types = string_types + string_enum + ','

	String = integer_types + string_types[0:len(string_types)-1]
	return String


def build_dependecies(dependencies):

	Children = dependencies["Tags"].values.tolist()
	Parent_key = [dependencies['Prereqs'].str.split('=').values[i][0] for i in range(dependencies.shape[0])]
	Parent_value = [dependencies['Prereqs'].str.split('=').values[i][1] for i in range(dependencies.shape[0])]
	
	String = ''
	
	for i in range(0,len(Children)):
		child_string = '"' + Children[i] + '":{"required" : ["' + Parent_key[i] + '"], "properties": {"' + Parent_key[i] + '":'
		child_string = child_string + '{"type": "string", "const": "' + Parent_value[i] + '"}}},'
		String = String + child_string
	String = String[0:len(String)-1]
	return String

def generate_nodes_schema(Tags, Types, df, dependencies):
	
	print("Generating Nodes Schema")
	Point_Properties = build_properties(Tags, Types, df)
	Point_dependencies = build_dependecies(dependencies)
	
	String = '''{
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
            "properties": {"id": {"type": "string"},''' + Point_Properties + '''},
			"dependencies": {''' + Point_dependencies + '''}
          }
        }
      }
    }
  }
}'''

	return String
	

def generate_ways_schema(Tags, Types, df, dependencies):
	
	print("Generating Ways Schema")
	Line_Properties = build_properties(Tags, Types, df)
	Line_dependencies = build_dependecies(dependencies)

	
	String = '''{
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
            "properties":  {"id": {"type": "string"},''' + Line_Properties + '''},
			"dependencies": {''' + Line_dependencies + '''}
          }
        }
      }
    }
  }
}'''

	return String
	
	
if __name__ == '__main__':
	print("Reading the Excel file")
	df = pd.read_excel('OSW_Tags.xlsx', sheet_name='Tags') 
	dependencies = pd.read_excel('OSW_Tags.xlsx', sheet_name='Parents')
	
	# Remove all those lines which do not have a dependency
	dependencies = dependencies[dependencies['Prereqs'] != 'None']
	dependencies['Tag'] = [dependencies['Prereqs'].str.split('=').values[i][0] for i in range(dependencies.shape[0])]
	
	Pointsdf = df[df['Geometry'] == 'Point'].sort_values(by=['type'])
	Pointsdf.reset_index(drop=True, inplace=True) # reset the index for future use
	
	Linesdf = df[df['Geometry'] == 'LineString'].sort_values(by=['type'])
	Linesdf.reset_index(drop=True, inplace=True) # reset the index for future use
	
	Point_Tags = Pointsdf.Tag.values.tolist()
	Point_Types = Pointsdf.type.values.tolist()
	Pointsdp = pd.merge(Pointsdf.Tag, dependencies, on='Tag', how='inner')
	Pointsdf.drop(columns=['Tag','Geometry', 'type'], inplace=True)
	
	Line_Tags = Linesdf.Tag.values.tolist()
	Line_Types = Linesdf.type.values.tolist()
	Linesdp = pd.merge(Linesdf.Tag, dependencies, on='Tag', how='inner')
	Linesdf.drop(columns=['Tag','Geometry', 'type'], inplace=True)
	
	Nodes_schema = generate_nodes_schema(Point_Tags, Point_Types, Pointsdf, Pointsdp)
	Ways_schema = generate_ways_schema(Line_Tags, Line_Types, Linesdf, Linesdp)
	
	
	if json.loads(Nodes_schema):
		print('Generated Nodes schema Successfully \n')
		Nodes_file = open("Nodes_schema.json", "w")
		Nodes_file.write(Nodes_schema)
		Nodes_file.close()
	else:
		print('Error Generating Nodes Schema')
	
	if json.loads(Ways_schema):
		print('Generated Ways schema Successfully \n')
		Ways_file = open("Ways_schema.json", "w")
		Ways_file.write(Ways_schema)
		Ways_file.close()
	else:
		print('Error Generating Ways Schema')
"""
Config file
Command line arguments overwrites these configs
This object saves the input and output paths
"""
import os
import ntpath


class DefaultConfigs:

    def __init__(self, args=None):
        if args:
            self.inputPath = args.inputPath
            self.validation = args.validation
            self.writePath = args.writePath
        else:
            self.GeoJSON = os.path.join(os.getcwd(), "TestData\input")
            self.validation = "intersectingvalidation"
            self.writePath = os.path.join(os.getcwd(), "TestData\Output")
        
        if not os.path.exists(self.writePath):
            os.mkdir(self.writePath)

        self.test_nodes_json = os.path.join(os.getcwd(), "TestData\input", "ms_campus_nodes.geojson")
        self.test_ways_json = os.path.join(os.getcwd(), "TestData\input", "ms_campus_ts.geojson")

        self.node_schema = os.path.join(os.getcwd(), "Json Schema", "Nodes_schema.json")
        self.ways_schema = os.path.join(os.getcwd(), "Json Schema", "Ways_schema.json")

        self.file_filter = 'ms_campus_'  # for now filter just by substring. TODO :  extended to regex
        self.filter_sidewalks = False  # Filter only side walks for further processing
        self.validation = ''
        self.do_all_validations = False
        self.do_eda = False
        self.do_schema_validations = True


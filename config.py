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
            self.GeoJSON = os.path.join(os.getcwd(), "OSW\TestData\input")
            self.validation = "intersectingvalidation"
            self.writePath = os.path.join(os.getcwd(), "OSW\TestData\Output")

        if not os.path.exists(self.writePath):
            os.mkdir(self.writePath)

        self.test_geojson = os.path.join(os.getcwd(), "OSW\TestData", "test_ms_campus_nodes.geojson")
        self.test_schema = os.path.join(os.getcwd(), "OSW\TestData", "test_schema.json")
        self.file_filter = 'ms_campus_'  # for now filter just by substring. TODO :  extended to regex
        self.filter_sidewalks = False  # Filter only side walks for further processing
        self.validation = 'intersectingvalidation'
        self.do_all_validations = True
        self.do_eda = True
        self.generate_output_paths()

    def generate_output_paths(self):
        ##paths for Output files to be generated
        # Ravi
        self.path_invalid_nodes = os.path.join(self.writePath, 'test_nodes_invalid.geojson')
        self.path_valid_nodes = os.path.join(self.writePath, 'test_nodes_valid.geojson')
        self.path_connected_json = ''
        self.path_disconnected_json = ''
        self.path_plot_nodes_vs_ways = os.path.join(self.writePath, 'NodesVsWays.jpg')
        self.path_plot_random_subgraph = os.path.join(self.writePath, 'RandomSubgraph.jpg')
        # Karthik
        self.path_invalidWays = ''


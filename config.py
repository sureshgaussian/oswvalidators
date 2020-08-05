'''
Config file
Command line arguments overwrites these configs
This object saves the input and output paths
'''
import os
import ntpath
class DefaultConfigs():
    
    def __init__(self, args):
        self.GeoJSON = args.GeoJSON
        self.validation = args.validation
        self.writePath = args.writePath
        if not os.path.exists(self.writePath):
            os.mkdir(self.writePath)

        self.file_filter = 'ms_campus'      #for now filter just by substring. To be extended to regex
        self.filter_sidewalks = False
        
        self.do_all_validations = True
        self.do_all_eda = True
        self.save_plots = True
        self.generate_output_paths()
        
    def generate_output_paths(self):
        ##paths for Output files to be generated
        #Ravi
        self.path_invalid_nodes = ''
        self.path_connected_json = ''
        self.path_disconnected_json = ''
        self.path_plot_nodes_vs_ways = os.path.join(self.writePath, 'NodesVsWays.jpg')
        self.path_plot_random_subgraph = os.path.join(self.writePath, 'RandomSubgraph.jpg')
        #Karthik
        self.path_invalidWays = ''
        self.path_invalidFormat = os.path.join(self.writePath, 'InvalidGeometryFormat.geojson')
        self.path_suggestedIntersectingWays = os.path.join(self.writePath, 'WaysMissingIntersection.geojson')
        self.path_recommendedIntersections = os.path.join(self.writePath, 'recommendedIntersections.geojson')

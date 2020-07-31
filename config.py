'''
Config file
Command line arguments overwrites these configs
This object saves the input and output paths
'''
import os
import ntpath
class DefaultConfigs():
    
    def __init__(self, args = None):
        
        if args:
            self.GeoJSON = args.GeoJSON
            self.validation = args.validation
            self.writePath = args.writePath
        
            if not os.path.exists(self.writePath):
                os.mkdir(self.writePath)

        self.file_filter = 'ms_campus'      #for now filter just by substring. To be extended to regex
        self.filter_sidewalks = False
        
        self.do_all_validations = True
        self.do_all_eda = True
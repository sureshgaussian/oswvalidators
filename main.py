import argparse as ag
import os
from intersectingValidation import intersectLineStringInValidFormat
from glob import glob
from node_connectivity import plot_nodes_vs_ways, subgraph_eda, get_invalidNodes
from config import DefaultConfigs
from util_data import UtilData
import ntpath

if __name__ == '__main__':
    parser = ag.ArgumentParser()
    parser.add_argument("--inputPath", help="Relative input path to GeoJSON files",
                        default=os.path.join(os.getcwd(), "OSW\TestData\input"))
    parser.add_argument("--validation", help="Type of validation", default='intersectingvalidation')
    parser.add_argument("--writePath", help="Relative output path to write the validation errors",
                        default=os.path.join(os.getcwd(), "OSW\TestData\Output"))
    args = parser.parse_args()
    cf = DefaultConfigs(args)
    inputPath = args.inputPath
    writePath = args.writePath

    json_files = glob(os.path.join(inputPath, "*.geojson"))
    if cf.file_filter:
        print("Filtering")
        json_files = sorted([i for i in json_files if cf.file_filter in i])
    print("Number of geojson files :", len(json_files))
    nodes_files = sorted([x for x in json_files if 'node' in x])
    ways_files = sorted([x for x in json_files if 'node' not in x])

    for ind, (nodes_file, ways_file) in enumerate(zip(nodes_files, ways_files)):
        print('Processing File : \n{}\n{}'.format(ntpath.basename(nodes_file), ntpath.basename(ways_file)))
        utild = UtilData(nodes_file, ways_file, cf)
        if cf.validation == 'intersectingvalidation':
            print("--" * 10)
            print("intersectingvalidation")
            print("--" * 10)
            intersectLineStringInValidFormat(utild.ways_json, "brunnel", cf)

        if cf.do_eda:
            print("--" * 10)
            print("eda")
            print("--" * 10)
            plot_nodes_vs_ways(utild, cf)
            subgraph_eda(utild, cf)

        if cf.do_all_validations:
            print("--" * 10)
            print("all validations")
            print("--" * 10)
            get_invalidNodes(utild, cf)

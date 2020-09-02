import argparse as ag
import os
from intersectingValidation import intersectLineStringInValidFormat
from glob import glob
from node_connectivity import plot_nodes_vs_ways, subgraph_eda, get_invalidNodes
from config import DefaultConfigs
from util_data import UtilData
from Validate_JsonFile_Schema import validate_json_schema
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
    print("Reading files from :",cf.inputPath)
    print("Number of geojson files :", len(json_files))
    nodes_files = sorted([x for x in json_files if 'node' in x])
    ways_files = sorted([x for x in json_files if 'node' not in x])

    for ind, (nodes_file, ways_file) in enumerate(zip(nodes_files, ways_files)):
        print('Processing the following files : \n{}\n {}'.format(ntpath.basename(nodes_file),
                                                                  ntpath.basename(ways_file)))
        if cf.do_all_validations or cf.do_schema_validations:
            validate_json_schema(nodes_file, cf.node_schema, cf.writePath)
            validate_json_schema(ways_file, cf.ways_schema, cf.writePath)

        utild = UtilData(nodes_file, ways_file, cf)
        # get_invalidNodes(utild, cf)
        if cf.do_all_validations or cf.validation == 'intersectingvalidation':
            print("--" * 10)
            print("performing checks to see if any Ways which are intersecting have a missing intersecting node")
            print("--" * 10)
            intersectLineStringInValidFormat(utild.ways_json, "brunnel", cf, ntpath.basename(ways_file))

        if cf.do_eda:
            print("--" * 10)
            print("eda")
            print("--" * 10)
            plot_nodes_vs_ways(utild, cf)
            subgraph_eda(utild, cf)
    print("\n Output files written at the following location",cf.writePath)
